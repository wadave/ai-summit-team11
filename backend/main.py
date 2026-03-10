"""Entry point for the End-to-End Content Engine.

- Local dev:  adk web backend/
- Cloud Run:  uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000
"""

from pathlib import Path

from fastapi.staticfiles import StaticFiles
from google.adk.cli.fast_api import get_fast_api_app
from starlette.responses import FileResponse

PROJECT_ROOT = str(Path(__file__).parent.parent)
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"

app = get_fast_api_app(
    agents_dir=PROJECT_ROOT,
    web=True,
    allow_origins=["*"],
)


@app.get("/")
async def serve_frontend():
    return FileResponse(FRONTEND_DIR / "index.html")


app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
