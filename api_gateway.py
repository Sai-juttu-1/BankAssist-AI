"""FastAPI gateway for the Northwind BankAssist demo."""

import json
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import AIMessage, HumanMessage
from pydantic import BaseModel, Field

from bankassist_Ic import ask, llm_with_tools, stream_answer
from router import route_question

app = FastAPI(
    title="BankAssist API Gateway",
    description="API Gateway for the fictional Northwind BankAssist demo",
    version="1.2.0",
)


class ChatRequest(BaseModel):
    """Incoming chat request."""

    question: str = Field(
        min_length=1,
        max_length=2000,
        description="The user's banking question",
    )
    session_id: str = Field(
        default="default",
        min_length=1,
        max_length=100,
        description="Optional conversation session identifier",
    )


class ChatResponse(BaseModel):
    """Response payload returned by a single-turn chat call."""

    session_id: str
    answer: str
    tool_steps: list[str] = []
    turns: int = 0


SESSION_HISTORY: dict[str, list[Any]] = {}


def build_messages(session_id: str, question: str) -> list[Any]:
    """Return the prior message history plus the latest user prompt."""
    history = SESSION_HISTORY.setdefault(session_id, [])
    return [*history, HumanMessage(content=question.strip())]


def sse(event: str, data: dict[str, Any]) -> str:
    """Format one Server-Sent Event."""
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


@app.get("/health")
def health_check():
    """Health endpoint used by the Streamlit frontend."""
    return {
        "status": "healthy",
        "message": "BankAssist API is running",
    }


@app.post("/chat")
def chat(request: ChatRequest):
    """Route a question and return the assistant's answer."""
    question = request.question.strip()
    if not question:
        raise HTTPException(
            status_code=422,
            detail="Question cannot be empty or whitespace only.",
        )

    route = route_question(question)
    history = SESSION_HISTORY.setdefault(request.session_id, [])

    tool_steps: list[str] = []
    answer = ""

    try:
        for kind, value in stream_answer(llm_with_tools, question):
            if kind == "tool":
                tool_steps.append(value)
            elif kind == "done":
                answer = value
    except Exception as error:
        print(f"BankAssist actual error: {error!r}", flush=True)

        raise HTTPException(
            status_code=502,
            detail=(
                "BankAssist could not get a response from the AI provider. "
                "Check the backend terminal and .env configuration."
            ),
        ) from error
        

    history.extend(
        [
            HumanMessage(content=question),
            AIMessage(content=answer),
        ]
    )

    return {
        "session_id": request.session_id,
        "question": question,
        "route": route,
        "answer": answer,
        "tool_steps": tool_steps,
        "turns": len(history) // 2,
    }


@app.post("/chat/stream")
def chat_stream(request: ChatRequest):
    """Stream answer tokens and tool events using Server-Sent Events."""
    question = request.question.strip()
    if not question:
        raise HTTPException(
            status_code=422,
            detail="Question cannot be empty or whitespace only.",
        )

    history = SESSION_HISTORY.setdefault(request.session_id, [])

    def events():
        try:
            for kind, value in stream_answer(llm_with_tools, question):
                if kind == "tool":
                    yield sse("tool", {"text": value})
                elif kind == "done":
                    answer = value
                    yield sse("done", {"text": answer})
                    history.extend(
                        [
                            HumanMessage(content=question),
                            AIMessage(content=answer),
                        ]
                    )
        except Exception:
            yield sse(
                "error",
                {
                    "text": (
                        "BankAssist could not get a response from the AI provider. "
                        "Check the backend terminal and .env configuration."
                    )
                },
            )

    return StreamingResponse(
        events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.delete("/sessions/{session_id}")
def forget_session(session_id: str):
    """Delete conversation history for a given session."""
    deleted = SESSION_HISTORY.pop(session_id, None) is not None
    return {"session_id": session_id, "deleted": deleted}