# 💻 AI Code Assistant

A private, offline coding assistant that runs entirely on your own computer. Ask programming questions in English and get streamed answers from a local **Qwen2.5-Coder 3B** model, with chat memory and a programming language selector.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688)
![LangChain](https://img.shields.io/badge/LangChain-LLM%20framework-1c3c3c)
![Ollama](https://img.shields.io/badge/Ollama-local%20model-black)

## ✨ Features

- **Local and private:** the model runs through Ollama, so your code and questions never leave your computer.
- **Free to run:** no API key, no subscription, and no internet needed after the model is downloaded.
- **Streaming answers:** replies appear word by word as they are generated.
- **Chat memory:** remembers the last 10 exchanges per session, so follow-up questions work.
- **Language selector:** choose Python, JavaScript, TypeScript, Java, C++, C#, Go, Rust, SQL, or any language.
- **Clean chat UI:** dark theme, formatted code blocks, and a New Chat button.
- **Swappable model:** change the model or server address in `.env` without touching the code.

## 🧰 Tech Stack

| Technology | Role |
|---|---|
| Python | Backend language |
| FastAPI | Web framework and streaming API |
| LangChain | Prompt template, memory and model chain |
| Ollama + Qwen2.5-Coder 3B | Local language model |
| HTML, CSS, JavaScript | Chat interface |

## 🏗️ How It Works

```
Browser (HTML/CSS/JS)  →  FastAPI  →  LangChain (prompt + memory)  →  Ollama (Qwen2.5-Coder 3B)
        ↑___________________ streamed answer ______________________________|
```

1. The browser sends the question, the selected language and a session ID to FastAPI.
2. LangChain builds a prompt from the system instruction, the recent chat history and the question.
3. The prompt goes to the local model through Ollama's OpenAI-compatible API.
4. The answer is streamed back to the browser and displayed as it arrives.

## 📁 Project Structure

```
ai-code-assistant/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app and routes
│   └── llm.py           # LangChain chain, prompt and chat memory
├── templates/
│   └── index.html       # Chat page
├── static/
│   ├── style.css        # Styling
│   └── script.js        # Sending questions and reading the stream
├── run.py               # Starts the server
├── setup_project.py     # Creates the folders and empty files
├── requirements.txt
├── .env                 # Settings (not committed)
└── .gitignore
```


This project is released under the MIT License. See the `LICENSE` file for details.

## 🙏 Acknowledgements

[FastAPI](https://fastapi.tiangolo.com) · [LangChain](https://python.langchain.com) · [Ollama](https://ollama.com) · [Qwen2.5-Coder](https://github.com/QwenLM/Qwen2.5-Coder)
