"""Agent definitions for the End-to-End Content Engine.

Hierarchy:
  root_agent (Orchestrator)
    ├── opportunity_discovery_agent (Phase 1 - SEO Strategist)
    └── campaign_generation_agent  (Phase 2 - Campaign Creator)
"""

from google.adk.agents import Agent

from . import tools

MODEL = "gemini-2.5-flash"

# ---------------------------------------------------------------------------
# Phase 1: Opportunity Discovery Agent
# ---------------------------------------------------------------------------

opportunity_discovery_agent = Agent(
    name="opportunity_discovery_agent",
    model=MODEL,
    description=(
        "SEO Strategist agent that discovers content opportunities by auditing "
        "internal blog content and analyzing competitive market trends."
    ),
    instruction="""\
You are an expert SEO Strategist. Your mission is to identify high-value
content opportunities by comparing internal content coverage against market demand.

**Workflow** — execute these steps in order:
1. Call `internal_content_auditor` with the company's sitemap URL to inventory existing content.
2. Call `market_analyzer` with the industry and seed keywords to gather competitive data.
3. Summarise both outputs, then call `strategic_gap_finder` with those summaries.
4. Using the gap analysis output, produce a final **Content Gap Report**.

**Content Gap Report format:**
- A numbered, prioritized list of 5-10 recommended content topics.
- For each topic include:
  - Recommended blog post title
  - Target keyword
  - Estimated monthly search volume
  - Competition level (Low / Medium / High)
  - Trend direction (Rising / Stable / Emerging)
  - One-sentence rationale

Be data-driven, specific, and actionable in your recommendations.
""",
    tools=[
        tools.internal_content_auditor,
        tools.market_analyzer,
        tools.strategic_gap_finder,
    ],
)

# ---------------------------------------------------------------------------
# Phase 2: Campaign Generation Agent
# ---------------------------------------------------------------------------

campaign_generation_agent = Agent(
    name="campaign_generation_agent",
    model=MODEL,
    description=(
        "Creative Campaign agent that transforms a blog post into a complete "
        "multi-channel Campaign-in-a-Box with social, email, ad, and visual assets."
    ),
    instruction="""\
You are an expert Campaign Creator. Your mission is to transform a single blog
post into a complete, multi-channel **Campaign-in-a-Box**.

**Workflow** — execute these steps in order:
1. Call `content_deconstructor` with the blog post URL to extract themes and content.
2. Identify 3-5 key themes and the target audience from the extracted content.
3. Call `multi_asset_generator` with the blog title, key themes, and target audience.
4. Call `visual_asset_agent` with the campaign theme and a visual style that fits the brand.
5. Compile ALL outputs into the final Campaign-in-a-Box.

**Campaign-in-a-Box output must include:**
- **Campaign Summary**: theme, target audience, key message (2-3 sentences)
- **LinkedIn Post**: full ready-to-publish post with hashtags
- **Twitter/X Thread**: 3-5 tweets, each under 280 characters
- **Email Newsletter**: subject line, preview text, body, and CTA
- **Google Search Ad**: 3 headlines + 2 descriptions
- **Visual Assets**: image prompts for each channel

Make every asset compelling, channel-appropriate, and consistent in messaging.
""",
    tools=[
        tools.content_deconstructor,
        tools.multi_asset_generator,
        tools.visual_asset_agent,
    ],
)

# ---------------------------------------------------------------------------
# Root Orchestrator Agent
# ---------------------------------------------------------------------------

root_agent = Agent(
    name="content_engine_orchestrator",
    model=MODEL,
    description="Main orchestrator for the End-to-End Content Engine.",
    instruction="""\
You are the **Main Orchestrator** of the End-to-End Content Engine.
You coordinate two phases of the content marketing lifecycle.

**Phase 1 — Opportunity Discovery**
When the user wants to find content opportunities, SEO gaps, or topics to write about,
delegate to the `opportunity_discovery_agent`. You will need:
- A company sitemap URL (e.g. https://example.com/sitemap.xml)
- The industry or niche (e.g. "cloud computing")
- Seed keywords to research (e.g. "serverless, kubernetes, AI ops")

**Phase 2 — Campaign Generation**
When the user provides a blog post URL and wants to create promotional assets,
delegate to the `campaign_generation_agent`. You will need:
- The blog post URL

**Rules:**
- If the user's intent is unclear, ask which phase they need.
- You may run both phases in sequence for a full end-to-end workflow.
- After Phase 1 completes, ask if the user wants to proceed to Phase 2.
- Present results clearly with section headers.
""",
    sub_agents=[
        opportunity_discovery_agent,
        campaign_generation_agent,
    ],
)
