"""Entry point for the End-to-End Content Engine.

- Local dev (backend):   uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000
- Local dev (frontend):  cd frontend && npm run dev
- Production:            Serve frontend/dist via this server
"""

from pathlib import Path

from google.adk.cli.fast_api import get_fast_api_app

PROJECT_ROOT = str(Path(__file__).parent.parent)
FRONTEND_DIST = Path(__file__).parent.parent / "frontend" / "dist"

app = get_fast_api_app(
    agents_dir=PROJECT_ROOT,
    web=False,
    allow_origins=["*"],
)

# Serve built React frontend in production
if FRONTEND_DIST.exists():
    from fastapi.staticfiles import StaticFiles
    from starlette.responses import FileResponse

    @app.get("/")
    async def serve_frontend():
        return FileResponse(FRONTEND_DIST / "index.html")

    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST)), name="frontend")
