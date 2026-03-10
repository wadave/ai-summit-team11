"""Entry point for the End-to-End Content Engine.

- Local dev:  adk web app/
- Cloud Run:  uvicorn app.main:fast_api_app --host 0.0.0.0 --port 8080
"""

from google.adk.apps.app import App
from google.adk.apps.fast_api_app import FastAPIApp

from .agent import root_agent

app = App(name="app", root_agent=root_agent)

fast_api_app = FastAPIApp(app=app, enable_playground=True)
