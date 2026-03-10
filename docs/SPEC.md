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
2.  **Opportunity Discovery Agent (Phase 1)**:
    - **Goal**: Opportunity Discovery.
    - **Activities**: Audit internal content, analyze competitive SEO data, identify content gaps.
3.  **Campaign Generation Agent (Phase 2)**:
    - **Goal**: Campaign Generation.
    - **Activities**: Deconstruct long-form content, generate multi-channel text assets (concurrently), suggest/generate visuals.

---

## 3. Data Integration & Tools (MCP)

### Phase 1 Tools:
- `internal_content_auditor`: Scrapes and analyzes existing company blog/sitemap to determine topic authority.
- `market_analyzer`: Ingests competitive SEO data (via external API integration or sample data) to find market opportunities.
- `strategic_gap_finder`: Compares internal content data against market data to produce a prioritized Content Gap Report.

### Phase 2 Tools:
- `content_deconstructor`: Extracts structured themes, key arguments, and data from a new blog post.
- `multi_asset_generator`: Generates text assets (social posts, email copy, ad variations) from deconstructed content; runs in parallel with `visual_asset_agent`.
- `visual_asset_agent`: Connects to Brand Image Library (GCS) or invokes Imagen on Vertex AI for image generation.

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
