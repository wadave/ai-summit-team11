"""Entry point for the End-to-End Content Engine.

- Local dev (backend):   uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000
- Local dev (frontend):  cd frontend && npm run dev
- Production:            Serve frontend/dist via this server
"""

import uuid
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse
from starlette.responses import FileResponse

from .agent import root_agent

FRONTEND_DIST = Path(__file__).parent.parent / "frontend" / "dist"
SAMPLE_CONTENT = Path(__file__).parent.parent / "sample-content"
APP_NAME = "content-engine"

session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

app = FastAPI(title="Content Engine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateSessionResponse(BaseModel):
    id: str


class RunRequest(BaseModel):
    session_id: str
    message: str


@app.post("/api/sessions", response_model=CreateSessionResponse)
async def create_session():
    session_id = str(uuid.uuid4())
    await session_service.create_session(
        app_name=APP_NAME,
        user_id="web-user",
        session_id=session_id,
    )
    return CreateSessionResponse(id=session_id)


@app.post("/api/run")
async def run_agent_sse(req: RunRequest):
    async def event_stream():
        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=req.message)],
        )
        async for event in runner.run_async(
            user_id="web-user",
            session_id=req.session_id,
            new_message=content,
        ):
            author = event.author or "system"
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.function_call:
                        yield {
                            "event": "tool_call",
                            "data": f'{{"author":"{author}","tool":"{part.function_call.name}"}}',
                        }
                    elif part.function_response:
                        yield {
                            "event": "tool_result",
                            "data": f'{{"author":"{author}","tool":"{part.function_response.name}"}}',
                        }
                    elif part.text:
                        import json

                        yield {
                            "event": "message",
                            "data": json.dumps(
                                {"author": author, "text": part.text}
                            ),
                        }
        yield {"event": "done", "data": "{}"}

    return EventSourceResponse(event_stream())


# Serve sample blog content for testing Campaign Generation
app.mount(
    "/blog", StaticFiles(directory=str(SAMPLE_CONTENT), html=True), name="blog"
)

# Serve built React frontend in production
if FRONTEND_DIST.exists():

    @app.get("/")
    async def serve_frontend():
        return FileResponse(FRONTEND_DIST / "index.html")

    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST)), name="frontend")
