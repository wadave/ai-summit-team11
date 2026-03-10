# The End-to-End Content Engine

An integrated, multi-agent AI system that automates the entire content marketing lifecycle — from identifying high-value SEO opportunities to generating a complete, multi-channel campaign with a single click.

## The Problem

Content marketing is slow, disconnected, and inefficient. Marketing teams spend weeks manually researching what to write about, often missing key trends competitors are capturing. Once a blog post is published, it sits idle — creating social posts, emails, and ads takes even more time, leading to inconsistent promotion and low ROI.

## The Solution

The Content Engine operates in two phases:

| Phase | Agent | What it does |
|-------|-------|-------------|
| **1 — Opportunity Discovery** | SEO Strategist | Audits your blog, analyzes competitive SEO data, and produces a prioritized Content Gap Report |
| **2 — Campaign Generation** | Campaign Creator | Deconstructs a blog post and generates a full Campaign-in-a-Box (LinkedIn, Twitter/X, email, search ads, visuals) |

## Architecture

```
Orchestrator Agent
├── Opportunity Discovery Agent (Phase 1)
│   ├── internal_content_auditor   — scrapes sitemap, inventories existing content
│   ├── market_analyzer            — competitive SEO / trend data
│   └── strategic_gap_finder       — identifies content gaps
└── Campaign Generation Agent (Phase 2)
    ├── content_deconstructor      — extracts themes from a blog post
    ├── multi_asset_generator      — channel-specific copy (social, email, ads)
    └── visual_asset_agent         — Imagen prompts & image suggestions
```

## Project Structure

```
ai-summit-team11/
├── backend/                 # Google ADK agents & FastAPI server
│   ├── agent.py             # Orchestrator + sub-agent definitions
│   ├── tools.py             # 6 tool functions (3 per phase)
│   ├── main.py              # FastAPI entry point (serves API + built frontend)
│   └── .env                 # GCP environment variables
├── frontend/                # React + TypeScript UI (Vite)
│   ├── src/
│   │   ├── App.tsx          # Main app with phase tabs
│   │   ├── api.ts           # ADK API client with SSE streaming
│   │   └── components/      # Phase1, Phase2, LogPanel, ResultsPanel
│   ├── package.json
│   └── vite.config.ts       # Dev proxy to backend on :8000
├── docs/                    # Design & planning documents
│   ├── SCOPE.md             # Business requirements & success criteria
│   ├── SPEC.md              # Technical specification
│   └── SYSTEM_DESIGN.md     # Detailed system design & architecture
├── Dockerfile               # Cloud Run container
├── pyproject.toml           # Python dependencies (uv)
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- Node.js 18+
- A Google Cloud project with Vertex AI enabled

### Setup

```bash
# Install backend dependencies
uv sync

# Install frontend dependencies
cd frontend && npm install && cd ..

# Configure environment
cp backend/.env backend/.env.local
# Edit backend/.env.local with your GCP project ID
```

### Run Locally (Development)

Start the backend and frontend in separate terminals:

```bash
# Terminal 1 — Backend API (port 8000)
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Terminal 2 — Frontend dev server (port 3000, proxies API to :8000)
cd frontend && npm run dev
```

Open **http://localhost:3000** in your browser.

### Run Locally (Production Build)

```bash
# Build the frontend
cd frontend && npm run build && cd ..

# Start the backend (serves built frontend at /)
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Open **http://localhost:8000**.

### Deploy to Cloud Run

```bash
docker build -t content-engine .
docker run -p 8000:8000 content-engine
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | Google ADK (Agent Development Kit) |
| LLM | Gemini 2.5 Flash |
| Image Gen | Imagen on Vertex AI |
| Deployment | Vertex AI Agent Engine / Cloud Run |
| Cloud | GCP (BigQuery, Secret Manager, GCS) |
| Frontend | React, TypeScript, Vite, CSS Modules |

## Success Metrics

- **25%** increase in organic search traffic
- **2x** campaign launch speed
- **100%** of priority content gets a Campaign-in-a-Box

## Docs

- [SCOPE.md](docs/SCOPE.md) — Business requirements, KPIs, and timeline
- [SPEC.md](docs/SPEC.md) — Technical specification and agent/tool definitions
- [SYSTEM_DESIGN.md](docs/SYSTEM_DESIGN.md) — Full system architecture, data flow, and UI design
