import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME", "qwen2.5-coder:3b"),
    base_url=os.getenv("OLLAMA_URL", "http://localhost:11434/v1"),
    api_key="ollama",  # required by the client but ignored by Ollama
    temperature=0.2,
    streaming=True,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert coding assistant. Preferred programming "
               "language: {language}. Answer concisely and put all code "
               "inside fenced markdown code blocks."),
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])

chain = prompt | llm | StrOutputParser()

MAX_TURNS = 10  # exchanges remembered per session
sessions: dict[str, list] = {}


async def stream_answer(session_id: str, question: str, language: str):
    history = sessions.setdefault(session_id, [])
    reply = ""
    async for chunk in chain.astream(
        {"question": question, "language": language, "history": history}
    ):
        reply += chunk
        yield chunk
    history += [HumanMessage(question), AIMessage(reply)]
    del history[:-MAX_TURNS * 2]


def clear_history(session_id: str):
    sessions.pop(session_id, None)