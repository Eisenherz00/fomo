#!/usr/bin/env python3
"""
Anti-FOMO Daily — News Fetcher & Summariser
============================================
Fetches RSS feeds → sends to LLM for summarisation & trilingual translation
→ writes public/data.json that the Next.js frontend reads at runtime.

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
import traceback
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

import feedparser
from dotenv import load_dotenv
from openai import OpenAI

# ─── Configuration ───────────────────────────────────────────────────

load_dotenv()                       # reads scripts/.env

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH  = PROJECT_ROOT / "public" / "data.json"

# RSS feeds per category
RSS_FEEDS: dict[str, list[dict[str, str]]] = {
    "ai": [
        {
            "name": "MIT Technology Review",
            "url":  "https://www.technologyreview.com/feed/",
        },
        {
            "name": "Ars Technica – AI",
            "url":  "https://feeds.arstechnica.com/arstechnica/technology-lab",
        },
    ],
    "politics": [
        {
            "name": "Al Jazeera – News",
            "url":  "https://www.aljazeera.com/xml/rss/all.xml",
        },
        {
            "name": "BBC News – World",
            "url":  "https://feeds.bbci.co.uk/news/world/rss.xml",
        },
    ],
    "stocks": [
        {
            "name": "CNBC – Markets",
            "url":  "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258",
        },
        {
            "name": "MarketWatch – Top Stories",
            "url":  "https://feeds.marketwatch.com/marketwatch/topstories/",
        },
    ],
}

# Max articles to send to the LLM per category (controls token usage)
MAX_ARTICLES_PER_CATEGORY = 15

# ─── LLM Client Setup ───────────────────────────────────────────────

def _build_llm_client() -> tuple[OpenAI, str]:
    """
    Return an (OpenAI-compatible client, model_name) tuple.
    Supports: openai, deepseek, gemini — all via OpenAI SDK.
    """
    provider = os.getenv("LLM_PROVIDER", "openai").lower()

    if provider == "deepseek":
        api_key = os.getenv("DEEPSEEK_API_KEY", "")
        model   = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        client  = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    elif provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY", "")
        model   = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        client  = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    else:  # openai (default)
        api_key = os.getenv("OPENAI_API_KEY", "")
        model   = os.getenv("OPENAI_MODEL", "gpt-4o")
        client  = OpenAI(api_key=api_key)

    if not api_key:
        print(f"⚠️  Warning: No API key found for provider '{provider}'.")
        print(f"   Set the appropriate env var in scripts/.env")
        sys.exit(1)

    return client, model

# ─── Stage 1: Fetch RSS ──────────────────────────────────────────────

def fetch_rss(category: str) -> list[dict]:
    """
    Fetch and merge articles from all RSS feeds for a given category.
    Gracefully skips feeds that fail.
    """
    feeds = RSS_FEEDS.get(category, [])
    articles: list[dict] = []

    for feed_info in feeds:
        name = feed_info["name"]
        url  = feed_info["url"]
        try:
            print(f"  📡 Fetching {name}...")
            parsed = feedparser.parse(url)

            if parsed.bozo and not parsed.entries:
                print(f"  ⚠️  {name}: feed returned errors, skipping.")
                continue

            for entry in parsed.entries[:MAX_ARTICLES_PER_CATEGORY]:
                # Extract a clean publish date
                published = ""
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6],
                                         tzinfo=timezone.utc).strftime("%Y-%m-%d")

                articles.append({
                    "title":       entry.get("title", "").strip(),
                    "description": entry.get("summary", entry.get("description", "")).strip(),
                    "link":        entry.get("link", ""),
                    "source":      name,
                    "date":        published or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                })

            print(f"  ✅ {name}: got {min(len(parsed.entries), MAX_ARTICLES_PER_CATEGORY)} articles")

        except Exception as exc:
            print(f"  ❌ {name}: failed ({exc})")
            traceback.print_exc()
            continue

    return articles

# ─── Stage 2: LLM Summarisation ─────────────────────────────────────

SYSTEM_PROMPT = dedent("""\
    You are "Anti-FOMO Daily", an elite intelligence analyst.
    Your job: read a batch of raw news articles, then produce a
    **concise daily briefing** — exactly 3 items — in strict JSON.

    Rules:
    1. Pick the 3 most important, non-overlapping stories.
    2. For each story write a short `title` and a 2-3 sentence `summary`.
    3. Every `title` and `summary` must have three language versions:
       `zh` (Simplified Chinese), `en` (English), `de` (German).
    4. Keep the tone professional, neutral, and informative.
    5. The `source` field should reflect the original news outlet.
    6. The `date` field should be YYYY-MM-DD.
    7. Return ONLY valid JSON — no markdown fences, no commentary.

    Required JSON shape (array of exactly 3 objects):
    [
      {
        "id": "<category>-1",
        "title":   { "zh": "...", "en": "...", "de": "..." },
        "summary": { "zh": "...", "en": "...", "de": "..." },
        "source":  "...",
        "date":    "YYYY-MM-DD"
      },
      ...
    ]
""")

def summarize_with_llm(
    client: OpenAI,
    model: str,
    category: str,
    articles: list[dict],
) -> list[dict]:
    """
    Send raw articles to the LLM and get back 3 trilingual summaries.
    """
    if not articles:
        print(f"  ⚠️  No articles for '{category}', using empty result.")
        return []

    # Build the user message with all article data
    articles_text = "\n\n---\n\n".join(
        f"Title: {a['title']}\n"
        f"Source: {a['source']}\n"
        f"Date: {a['date']}\n"
        f"Description: {a['description'][:500]}"
        for a in articles
    )

    category_labels = {
        "ai":       "AI / Frontier Science",
        "politics": "Global Politics",
        "stocks":   "Stock Market",
    }

    user_msg = (
        f"Category: {category_labels.get(category, category)}\n"
        f"ID prefix: {category[:3]}\n\n"
        f"Here are today's raw articles:\n\n{articles_text}"
    )

    print(f"  🤖 Calling LLM ({model}) for '{category}'...")
    print(f"     Sending {len(articles)} articles ({len(user_msg)} chars)")
    response = client.chat.completions.create(
        model=model,
        temperature=0.3,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_msg},
        ],
    )

    raw = response.choices[0].message.content or "[]"
    print(f"     LLM response length: {len(raw)} chars")

    # Strip markdown code fences if the model included them
    raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw.strip())

    try:
        items = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"  ❌ LLM returned invalid JSON for '{category}': {exc}")
        print(f"     Raw response (first 300 chars): {raw[:300]}")
        return []

    # Validate shape
    if not isinstance(items, list):
        items = [items]

    # Ensure correct id prefix
    for i, item in enumerate(items):
        item["id"] = f"{category[:3]}-{i + 1}"

    print(f"  ✅ Got {len(items)} items for '{category}'")
    return items[:3]

# ─── Stage 3: Assemble & Write ──────────────────────────────────────

def main() -> None:
    print("=" * 56)
    print("  Anti-FOMO Daily — News Fetcher")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 56)

    client, model = _build_llm_client()

    all_data: dict[str, list[dict]] = {}

    for category in ("ai", "politics", "stocks"):
        print(f"\n📂 Category: {category.upper()}")

        # Stage 1 — fetch
        articles = fetch_rss(category)
        if not articles:
            print(f"  ⚠️  No articles fetched for '{category}', skipping LLM.")
            all_data[category] = []
            continue

        # Stage 2 — summarise
        try:
            items = summarize_with_llm(client, model, category, articles)
        except Exception as exc:
            print(f"  ❌ LLM call failed for '{category}': {exc}")
            traceback.print_exc()
            items = []

        all_data[category] = items

    # Stage 3 — write output
    output = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "aiNews":       all_data.get("ai", []),
        "politicsNews": all_data.get("politics", []),
        "stockNews":    all_data.get("stocks", []),
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    total = sum(len(v) for v in all_data.values())
    print(f"\n{'=' * 56}")
    print(f"  ✅ Done! Wrote {total} items to {OUTPUT_PATH}")
    print(f"{'=' * 56}")


if __name__ == "__main__":
    main()
