#!/usr/bin/env python3
"""
Anti-FOMO Daily — News Fetcher (No-AI Mode)
============================================
Fetches RSS feeds → picks top 3 per category → writes public/data.json.
No LLM required! Titles and summaries come directly from the RSS feed.

Usage:
    python scripts/fetch_and_summarize.py
"""

from __future__ import annotations

import json
import re
import traceback
from datetime import datetime, timezone
from pathlib import Path

import feedparser

# ─── Configuration ───────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH  = PROJECT_ROOT / "public" / "data.json"

RSS_FEEDS: dict[str, list[dict[str, str]]] = {
    "ai": [
        {"name": "MIT Technology Review", "url": "https://www.technologyreview.com/feed/"},
        {"name": "Ars Technica – AI",     "url": "https://feeds.arstechnica.com/arstechnica/technology-lab"},
    ],
    "politics": [
        {"name": "Al Jazeera",       "url": "https://www.aljazeera.com/xml/rss/all.xml"},
        {"name": "BBC News – World", "url": "https://feeds.bbci.co.uk/news/world/rss.xml"},
    ],
    "stocks": [
        {"name": "CNBC – Markets",          "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258"},
        {"name": "MarketWatch – Top Stories","url": "https://feeds.marketwatch.com/marketwatch/topstories/"},
    ],
}

ITEMS_PER_CATEGORY = 3

# ─── Fetch & Build ──────────────────────────────────────────────────

def clean_html(text: str) -> str:
    """Strip HTML tags from RSS descriptions."""
    return re.sub(r"<[^>]+>", "", text).strip()


def fetch_category(category: str) -> list[dict]:
    """Fetch RSS, pick top articles, format for the frontend."""
    feeds = RSS_FEEDS.get(category, [])
    all_articles: list[dict] = []

    for feed_info in feeds:
        name, url = feed_info["name"], feed_info["url"]
        try:
            print(f"  📡 {name}...")
            parsed = feedparser.parse(url)
            if parsed.bozo and not parsed.entries:
                print(f"  ⚠️  {name}: feed error, skipping")
                continue

            for entry in parsed.entries[:10]:
                title = entry.get("title", "").strip()
                desc  = clean_html(entry.get("summary", entry.get("description", "")))[:300]
                link  = entry.get("link", "")

                pub_date = ""
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6],
                                        tzinfo=timezone.utc).strftime("%Y-%m-%d")

                all_articles.append({
                    "title": title,
                    "summary": desc,
                    "source": name,
                    "date": pub_date or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    "link": link,
                })

            print(f"  ✅ {name}: {len(parsed.entries)} articles")
        except Exception as exc:
            print(f"  ❌ {name}: {exc}")
            traceback.print_exc()

    # Pick top N (they're already sorted by recency from the feed)
    top = all_articles[:ITEMS_PER_CATEGORY]

    # Format for frontend: use same text for all 3 languages (no AI translation)
    prefix = category[:3]
    result = []
    for i, a in enumerate(top):
        result.append({
            "id": f"{prefix}-{i+1}",
            "title":   {"zh": a["title"], "en": a["title"], "de": a["title"]},
            "summary": {"zh": a["summary"], "en": a["summary"], "de": a["summary"]},
            "source":  a["source"],
            "date":    a["date"],
        })

    return result


def main() -> None:
    print("=" * 56)
    print("  Anti-FOMO Daily — News Fetcher (No-AI Mode)")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 56)

    output = {"generatedAt": datetime.now(timezone.utc).isoformat()}

    for category, key in [("ai", "aiNews"), ("politics", "politicsNews"), ("stocks", "stockNews")]:
        print(f"\n📂 {category.upper()}")
        output[key] = fetch_category(category)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    total = sum(len(output[k]) for k in ["aiNews", "politicsNews", "stockNews"])
    print(f"\n{'=' * 56}")
    print(f"  ✅ Done! Wrote {total} items to {OUTPUT_PATH}")
    print(f"{'=' * 56}")


if __name__ == "__main__":
    main()
