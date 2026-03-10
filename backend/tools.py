"""Tool definitions for the End-to-End Content Engine.

Phase 1 Tools: internal_content_auditor, market_analyzer, strategic_gap_finder
Phase 2 Tools: content_deconstructor, multi_asset_generator, visual_asset_agent
"""

import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup


# ---------------------------------------------------------------------------
# Phase 1: Opportunity Discovery Tools
# ---------------------------------------------------------------------------


def internal_content_auditor(sitemap_url: str) -> dict:
    """Audits a company's existing blog content by fetching and analyzing its sitemap.

    Scrapes the sitemap.xml, visits each page, and extracts titles, headings,
    and meta descriptions to build a content inventory.

    Args:
        sitemap_url: The full URL to the company's sitemap.xml file.

    Returns:
        A dict with the content inventory including page titles and topics.
    """
    try:
        resp = requests.get(sitemap_url, timeout=15)
        resp.raise_for_status()

        root = ET.fromstring(resp.content)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [
            loc.text
            for loc in root.findall(".//sm:url/sm:loc", ns)
            if loc.text
        ]

        topics = []
        for url in urls[:20]:
            try:
                page = requests.get(url, timeout=10)
                soup = BeautifulSoup(page.content, "html.parser")
                title_tag = soup.find("title")
                h1_tag = soup.find("h1")
                meta_tag = soup.find("meta", attrs={"name": "description"})
                topics.append(
                    {
                        "url": url,
                        "title": title_tag.get_text(strip=True) if title_tag else "",
                        "heading": h1_tag.get_text(strip=True) if h1_tag else "",
                        "description": (
                            meta_tag["content"].strip()
                            if meta_tag and meta_tag.get("content")
                            else ""
                        ),
                    }
                )
            except Exception:
                topics.append({"url": url, "title": "", "heading": "", "description": ""})

        return {
            "status": "success",
            "total_pages_found": len(urls),
            "pages_analyzed": len(topics),
            "content_inventory": topics,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def market_analyzer(industry: str, seed_keywords: str) -> dict:
    """Analyzes market trends and competitive SEO landscape for a given industry.

    In production this would call an external SEO API (SEMrush, Ahrefs, etc.).
    Currently returns realistic sample data for demonstration.

    Args:
        industry: The industry or niche to analyze, e.g. "cloud computing".
        seed_keywords: Comma-separated seed keywords to research.

    Returns:
        A dict with trending topics, competitor keywords, and opportunity scores.
    """
    keywords = [k.strip() for k in seed_keywords.split(",")]

    return {
        "status": "success",
        "industry": industry,
        "data_source": "sample_competitive_data",
        "trending_topics": [
            {
                "topic": f"{industry} - AI automation trends",
                "search_volume": 12000,
                "competition": "medium",
                "trend": "rising",
            },
            {
                "topic": f"{industry} - cost optimization strategies",
                "search_volume": 8500,
                "competition": "high",
                "trend": "stable",
            },
            {
                "topic": f"{industry} - security best practices",
                "search_volume": 15000,
                "competition": "low",
                "trend": "rising",
            },
            {
                "topic": f"{industry} - serverless architecture",
                "search_volume": 6000,
                "competition": "medium",
                "trend": "rising",
            },
            {
                "topic": f"{industry} - sustainability and green IT",
                "search_volume": 4500,
                "competition": "low",
                "trend": "emerging",
            },
        ],
        "competitor_keywords": [
            {
                "keyword": kw,
                "estimated_monthly_volume": 5000 + i * 1200,
                "keyword_difficulty": 40 + i * 7,
            }
            for i, kw in enumerate(keywords)
        ],
    }


def strategic_gap_finder(
    internal_content_summary: str,
    market_data_summary: str,
) -> dict:
    """Compares internal content coverage against market opportunities to find gaps.

    Takes summaries of what the company already covers and what the market
    demands, then identifies high-value topics the company should create
    content for next.

    Args:
        internal_content_summary: Summary of topics the company currently covers.
        market_data_summary: Summary of trending market topics and competitor keywords.

    Returns:
        A structured gap analysis with instructions for prioritised ranking.
    """
    return {
        "status": "success",
        "task": "content_gap_analysis",
        "internal_content": internal_content_summary,
        "market_opportunities": market_data_summary,
        "analysis_criteria": {
            "primary": "High search volume with low or no internal coverage",
            "secondary": "Low competition score",
            "tertiary": "Rising or emerging trend direction",
        },
        "output_format": (
            "Return a prioritized Content Gap Report as a numbered list. "
            "For each gap include: rank, recommended blog post title, "
            "target keyword, estimated search volume, competition level, "
            "trend direction, and a one-sentence rationale."
        ),
    }


# ---------------------------------------------------------------------------
# Phase 2: Campaign Generation Tools
# ---------------------------------------------------------------------------


def content_deconstructor(blog_url: str) -> dict:
    """Fetches a blog post and extracts its key themes, structure, and content.

    Scrapes the page at the given URL and returns the title, headings,
    body text, and metadata for downstream campaign generation.

    Args:
        blog_url: The URL of the blog post to deconstruct.

    Returns:
        A dict with the extracted title, headings, body content, and word count.
    """
    try:
        resp = requests.get(blog_url, timeout=15)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.content, "html.parser")

        title_tag = soup.find("title")
        h1_tag = soup.find("h1")
        meta_tag = soup.find("meta", attrs={"name": "description"})

        headings = [
            {"level": tag, "text": el.get_text(strip=True)}
            for tag in ("h1", "h2", "h3")
            for el in soup.find_all(tag)
        ]

        paragraphs = [
            p.get_text(strip=True)
            for p in soup.find_all("p")
            if len(p.get_text(strip=True)) > 30
        ]
        full_text = "\n\n".join(paragraphs)

        return {
            "status": "success",
            "url": blog_url,
            "title": title_tag.get_text(strip=True) if title_tag else "",
            "main_heading": h1_tag.get_text(strip=True) if h1_tag else "",
            "meta_description": (
                meta_tag["content"].strip()
                if meta_tag and meta_tag.get("content")
                else ""
            ),
            "structure": headings,
            "content": full_text[:5000],
            "word_count": len(full_text.split()),
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


def multi_asset_generator(
    blog_title: str,
    key_themes: str,
    target_audience: str,
) -> dict:
    """Provides structured channel templates for multi-channel campaign asset generation.

    Returns format specifications for each marketing channel so the agent
    can generate tailored copy for LinkedIn, Twitter/X, email, and search ads.

    Args:
        blog_title: The title of the source blog post.
        key_themes: Comma-separated key themes and takeaways from the blog post.
        target_audience: Description of the target audience for the campaign.

    Returns:
        A dict with channel specs, tone guidelines, and generation instructions.
    """
    return {
        "status": "success",
        "source_title": blog_title,
        "key_themes": key_themes,
        "target_audience": target_audience,
        "channels": {
            "linkedin_post": {
                "format": "Professional thought-leadership post, 150-300 words, include 3-5 relevant hashtags",
                "tone": "authoritative, insightful, professional",
            },
            "twitter_thread": {
                "format": "3-5 tweet thread, each tweet under 280 characters, include hashtags",
                "tone": "concise, engaging, conversational",
            },
            "email_newsletter": {
                "format": "Subject line + preview text + body (200-400 words) + call-to-action button text",
                "tone": "informative, value-driven, personable",
            },
            "google_search_ad": {
                "format": "3 headline variations (max 30 chars each) + 2 description variations (max 90 chars each) + display URL path",
                "tone": "action-oriented, benefit-focused, urgent",
            },
        },
        "instructions": (
            "Generate ALL channel assets using the key themes provided. "
            "Each asset should highlight a different angle of the content. "
            "Ensure messaging is consistent across channels but adapted to each format and tone. "
            "Include the full generated text for each channel — not just a template."
        ),
    }


def visual_asset_agent(
    campaign_theme: str,
    visual_style: str,
) -> dict:
    """Generates image prompts and visual asset recommendations for the campaign.

    Produces Imagen-ready prompts for each channel and suggests how to source
    visuals from the brand image library.

    Args:
        campaign_theme: The main theme or topic for the visuals.
        visual_style: Desired visual style, e.g. "professional", "modern", "minimalist".

    Returns:
        A dict with per-channel image prompts, dimensions, and sourcing guidance.
    """
    return {
        "status": "success",
        "campaign_theme": campaign_theme,
        "visual_style": visual_style,
        "image_assets": [
            {
                "channel": "linkedin",
                "recommended_dimensions": "1200x627",
                "imagen_prompt": (
                    f"Professional banner image about {campaign_theme}, "
                    f"{visual_style} style, corporate setting, clean design, "
                    "no text overlay, high quality photography"
                ),
            },
            {
                "channel": "twitter",
                "recommended_dimensions": "1600x900",
                "imagen_prompt": (
                    f"Eye-catching social media graphic about {campaign_theme}, "
                    f"{visual_style} style, bold colors, space for text overlay, "
                    "modern digital art"
                ),
            },
            {
                "channel": "email_header",
                "recommended_dimensions": "600x200",
                "imagen_prompt": (
                    f"Subtle email header banner about {campaign_theme}, "
                    f"{visual_style} style, light background, minimal design"
                ),
            },
            {
                "channel": "search_ad_extension",
                "recommended_dimensions": "1200x628",
                "imagen_prompt": (
                    f"Clean product-focused image related to {campaign_theme}, "
                    f"{visual_style} style, white background, professional"
                ),
            },
        ],
        "sourcing_guidance": (
            "Use these prompts with Imagen on Vertex AI to generate images. "
            "Alternatively, search the brand image library in the GCS bucket "
            "for existing assets that match the campaign theme."
        ),
    }
