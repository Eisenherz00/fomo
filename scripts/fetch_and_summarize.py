#!/usr/bin/env python3
"""
Anti-FOMO Daily — News Fetcher & Summariser
============================================
Fetches RSS feeds → sends ONE batch to the LLM → writes public/data.json.

Usage:
    cd scripts
    cp .env.example .env   # fill in your API key
    pip install -r requirements.txt
    python fetch_and_summarize.py
"""

from __future__ import annotations

import json
import os
import sys
import re
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

import feedparser
from dotenv import load_dotenv
from openai import OpenAI

# ─── Configuration ───────────────────────────────────────────────────

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH  = PROJECT_ROOT / "public" / "data.json"

RSS_FEEDS: dict[str, list[dict[str, str]]] = {
    "ai": [
        {"name": "MIT Technology Review", "url": "https://www.technologyreview.com/feed/"},
        {"name": "Ars Technica – AI",     "url": "https://feeds.arstechnica.com/arstechnica/technology-lab"},
    ],
    "politics": [
        {"name": "Al Jazeera – News",  "url": "https://www.aljazeera.com/xml/rss/all.xml"},
        {"name": "BBC News – World",   "url": "https://feeds.bbci.co.uk/news/world/rss.xml"},
    ],
    "stocks": [
        {"name": "CNBC – Markets",          "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258"},
        {"name": "MarketWatch – Top Stories","url": "https://feeds.marketwatch.com/marketwatch/topstories/"},
    ],
}

MAX_ARTICLES_PER_FEED = 8

# ─── LLM Client ─────────────────────────────────────────────────────

def _build_llm_client() -> tuple[OpenAI, str]:
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()

    if provider == "deepseek":
        api_key = os.getenv("DEEPSEEK_API_KEY", "")
        model   = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        client  = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    elif provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY", "")
        model   = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite")
        client  = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    else:
        api_key = os.getenv("OPENAI_API_KEY", "")
        model   = os.getenv("OPENAI_MODEL", "gpt-4o")
        client  = OpenAI(api_key=api_key)

    if not api_key:
        print(f"⚠️  No API key for provider '{provider}'. Set it in .env")
        sys.exit(1)

    return client, model

# ─── Stage 1: Fetch RSS ──────────────────────────────────────────────

def fetch_rss(category: str) -> list[dict]:
    feeds = RSS_FEEDS.get(category, [])
    articles: list[dict] = []

    for feed_info in feeds:
        name, url = feed_info["name"], feed_info["url"]
        try:
            print(f"  📡 {name}...")
            parsed = feedparser.parse(url)
            if parsed.bozo and not parsed.entries:
                print(f"  ⚠️  {name}: feed error, skipping")
                continue

            for entry in parsed.entries[:MAX_ARTICLES_PER_FEED]:
                published = ""
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6],
                                         tzinfo=timezone.utc).strftime("%Y-%m-%d")
                articles.append({
                    "title":       entry.get("title", "").strip(),
                    "description": entry.get("summary", entry.get("description", "")).strip()[:300],
                    "source":      name,
                    "date":        published or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                })
            print(f"  ✅ {name}: {min(len(parsed.entries), MAX_ARTICLES_PER_FEED)} articles")
        except Exception as exc:
            print(f"  ❌ {name}: {exc}")
            continue

    return articles

# ─── Stage 2: ONE LLM call for all categories ───────────────────────

SYSTEM_PROMPT = dedent("""\
    You are "Anti-FOMO Daily", an elite intelligence analyst.
    Read ALL the raw news articles below (grouped by category),
    then produce a concise daily briefing in strict JSON.

    Rules:
    1. For EACH of the 3 categories (ai, politics, stocks), pick the 3 most important stories.
    2. Write a short title and a 2-3 sentence summary for each.
    3. Every title and summary must have 3 language versions: zh (Simplified Chinese), en (English), de (German).
    4. Keep tone professional, neutral, informative.
    5. Return ONLY valid JSON — no markdown fences, no extra text.

    Required JSON shape:
    {
      "aiNews": [
        {"id": "ai-1", "title": {"zh":"..","en":"..","de":".."}, "summary": {"zh":"..","en":"..","de":".."}, "source": "..", "date": "YYYY-MM-DD"},
        {"id": "ai-2", ...},
        {"id": "ai-3", ...}
      ],
      "politicsNews": [
        {"id": "pol-1", ...}, {"id": "pol-2", ...}, {"id": "pol-3", ...}
      ],
      "stockNews": [
        {"id": "stk-1", ...}, {"id": "stk-2", ...}, {"id": "stk-3", ...}
      ]
    }
""")


def summarize_all(client: OpenAI, model: str, all_articles: dict[str, list[dict]]) -> dict:
    """Send ALL categories in one LLM call to avoid rate limits."""

    sections = []
    for cat, label in [("ai", "AI / FRONTIER SCIENCE"), ("politics", "GLOBAL POLITICS"), ("stocks", "STOCK MARKET")]:
        articles = all_articles.get(cat, [])
        if not articles:
            continue
        items = "\n".join(
            f"- [{a['source']}] {a['title']}: {a['description']}"
            for a in articles
        )
        sections.append(f"=== {label} ===\n{items}")

    user_msg = "\n\n".join(sections)
    print(f"\n🤖 Calling LLM ({model}) — single batch ({len(user_msg)} chars)...")

    # Retry with backoff for rate limits
    for attempt in range(5):
        try:
            response = client.chat.completions.create(
                model=model,
                temperature=0.3,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": user_msg},
                ],
            )
            raw = response.choices[0].message.content or "{}"
            print(f"   ✅ Response received ({len(raw)} chars)")
            break
        except Exception as exc:
            if "429" in str(exc) or "rate" in str(exc).lower() or "quota" in str(exc).lower():
                wait = 20 * (attempt + 1)
                print(f"   ⏳ Rate limited (attempt {attempt+1}/5), waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"   ❌ LLM error: {exc}")
                traceback.print_exc()
                return {}
    else:
        print("   ❌ All retries exhausted")
        return {}

    # Clean markdown fences
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw.strip())

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"   ❌ Invalid JSON: {exc}")
        print(f"      First 500 chars: {raw[:500]}")
        return {}

    return data

# ─── Main ────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 56)
    print("  Anti-FOMO Daily — News Fetcher")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 56)

    client, model = _build_llm_client()

    # Stage 1 — fetch all categories
    all_articles: dict[str, list[dict]] = {}
    for category in ("ai", "politics", "stocks"):
        print(f"\n📂 {category.upper()}")
        all_articles[category] = fetch_rss(category)

    # Stage 2 — ONE LLM call
    result = summarize_all(client, model, all_articles)

    # Stage 3 — write
    output = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "aiNews":       result.get("aiNews", []),
        "politicsNews": result.get("politicsNews", []),
        "stockNews":    result.get("stockNews", []),
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    total = sum(len(v) for v in [output["aiNews"], output["politicsNews"], output["stockNews"]])
    print(f"\n{'=' * 56}")
    print(f"  ✅ Done! Wrote {total} items to {OUTPUT_PATH}")
    print(f"{'=' * 56}")


if __name__ == "__main__":
    main()
