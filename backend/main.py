"""Entry point for the End-to-End Content Engine.

- Local dev:  adk web backend/
- Cloud Run:  uvicorn backend.main:fast_api_app --host 0.0.0.0 --port 8080
"""

from pathlib import Path

from fastapi.staticfiles import StaticFiles
from google.adk.apps.app import App
from google.adk.apps.fast_api_app import FastAPIApp
from starlette.responses import FileResponse

from .agent import root_agent

app = App(name="backend", root_agent=root_agent)

fast_api_app = FastAPIApp(app=app, enable_playground=True)

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"


@fast_api_app.get("/")
async def serve_frontend():
    return FileResponse(FRONTEND_DIR / "index.html")


fast_api_app.mount(
    "/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static"
)
