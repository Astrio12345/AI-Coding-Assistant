from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.llm import stream_answer, clear_history

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="AI Code Assistant")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


class Question(BaseModel):
    question: str
    session_id: str
    language: str = "Any language"


class Session(BaseModel):
    session_id: str

@app.get("/")
async def index():
    return FileResponse(BASE_DIR / "templates" / "index.html")


@app.post("/api/ask")
async def ask_endpoint(body: Question):
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question is empty.")

    async def generate():
        try:
            async for chunk in stream_answer(
                body.session_id, body.question, body.language
            ):
                yield chunk
        except Exception as e:
            yield f"\n\n⚠️ Error: {e}"

    return StreamingResponse(generate(), media_type="text/plain")


@app.post("/api/clear")
async def clear_endpoint(body: Session):
    clear_history(body.session_id)
    return {"status": "cleared"}