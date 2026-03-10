# SPEC: The End-to-End Content Engine

## 1. Technical Environment
- **Platform**: Google Cloud Platform
- **Deployment**: Agent Engine (Vertex AI Reasoning Engines)
- **Framework**: Google ADK (Agent Development Kit)
- **Region**: `us-central1`
- **Variables**:
    - `GOOGLE_CLOUD_PROJECT`: [Project ID]
    - `GOOGLE_CLOUD_LOCATION`: `us-central1`

---

## 2. System Architecture (Strategy-to-Execution Pattern)

The system is decoupled into two phases coordinated by a **Content Engine Orchestrator**.

### AI Agent Team
1.  **Orchestrator Agent**:
    - Central hub for task routing and state management.
    - Uses Gemini 2.5 Flash for rapid decision making.
2.  **SEO Strategist (Phase 1)**:
    - **Goal**: Opportunity Discovery.
    - **Activities**: Audit internal content, analyze competitive SEO data, identify content gaps.
3.  **Creative Agent (Phase 2)**:
    - **Goal**: Campaign Generation.
    - **Activities**: Deconstruct long-form content, generate multi-channel text assets, suggest/generate visuals.

---

## 3. Data Integration & Tools (MCP)

### Phase 1 Tools:
- `blog_auditor`: Scrapes and analyzes existing company blog/sitemap.
- `market_analyzer`: Ingests competitive SEO data (via external API integration or sample data).

### Phase 2 Tools:
- `content_parser`: Extracts structured themes from blog posts.
- `asset_generator`: specialized templates for Social, Email, and Ads.
- `visual_suggester`: Connects to Brand Image Library or invokes Imagen for generation.

---

## 4. Directory Structure (ADK Standard)
```text
/ai-summit-team11
├── app/
│   ├── agent.py          # Orchestrator & Agent definitions
│   ├── tools.py          # Tool/Skill definitions
│   └── main.py           # Entry point (Reasoning Engine wrapper)
├── brain/                # Persistent context & artifacts
├── SCOPE.md              # Business requirements
├── SPEC.md               # Technical specification
└── README.md
```

---

## 5. Security & Auth
- **Identity**: Principle of Least Privilege (PoLP) using a dedicated Service Account.
- **Secrets**: Google Secret Manager for all API keys (SEO data, etc.).
- **Privacy**: No customer data is used for model training.
