#!/usr/bin/env python3
"""
Anti-FOMO Daily — News Fetcher & Summariser
============================================
Fetches RSS feeds → tries AI (respects LLM_PROVIDER) → falls back to raw RSS.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

import feedparser

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH  = PROJECT_ROOT / "public" / "data.json"

# Provider cascade order: preferred provider first, then fallbacks
DEFAULT_PROVIDERS = ["openai", "gemini", "deepseek"]

RSS_FEEDS = {
    "ai": [
        {"name": "MIT Technology Review", "url": "https://www.technologyreview.com/feed/"},
        {"name": "Ars Technica – AI",     "url": "https://feeds.arstechnica.com/arstechnica/technology-lab"},
    ],
    "politics": [
        {"name": "Al Jazeera",       "url": "https://www.aljazeera.com/xml/rss/all.xml"},
        {"name": "BBC News – World", "url": "https://feeds.bbci.co.uk/news/world/rss.xml"},
    ],
    "stocks": [
        {"name": "CNBC – Markets",           "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258"},
        {"name": "MarketWatch – Top Stories", "url": "https://feeds.marketwatch.com/marketwatch/topstories/"},
    ],
}

# ─── RSS Fetching ────────────────────────────────────────────────────

def clean_html(text: str) -> str:
    """Strip HTML tags from a string."""
    return re.sub(r"<[^>]+>", "", text).strip()

def fetch_rss(category: str) -> list[dict]:
    """Fetch and normalise RSS entries for a given category."""
    articles: list[dict] = []
    for feed in RSS_FEEDS.get(category, []):
        try:
            print(f"  📡 {feed['name']}...")
            parsed = feedparser.parse(feed["url"])
            if parsed.bozo and not parsed.entries:
                print(f"  ⚠️  {feed['name']}: feed returned bozo with no entries")
                continue
            for entry in parsed.entries[:8]:
                pub = ""
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    pub = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).strftime("%Y-%m-%d")
                articles.append({
                    "title": entry.get("title", "").strip(),
                    "summary": clean_html(entry.get("summary", entry.get("description", "")))[:300],
                    "source": feed["name"],
                    "date": pub or datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    "url": entry.get("link", ""),
                })
            print(f"  ✅ {feed['name']}: {min(len(parsed.entries), 8)} items")
        except Exception as e:
            print(f"  ❌ {feed['name']}: {e}")
            traceback.print_exc()
    return articles

def raw_fallback(category: str, articles: list[dict]) -> list[dict]:
    """Format raw RSS as frontend-compatible items (no translation)."""
    prefix = category[:3]
    return [
        {
            "id": f"{prefix}-{i+1}",
            "title":   {"zh": a["title"], "en": a["title"], "de": a["title"]},
            "summary": {"zh": a["summary"], "en": a["summary"], "de": a["summary"]},
            "source": a["source"],
            "date": a["date"],
            "url": a.get("url", ""),
        }
        for i, a in enumerate(articles[:3])
    ]

# ─── AI Summarisation ───────────────────────────────────────────────

SYSTEM_PROMPT = dedent("""\
    You are "Anti-FOMO Daily", an elite intelligence analyst.
    Read ALL raw articles below (grouped by category) and produce a daily briefing.

    Rules:
    1. For EACH category (ai, politics, stocks), pick the 3 most important stories.
    2. For the TITLE: faithfully translate the original article title into all 3 languages. Do NOT rewrite or paraphrase the title.
    3. For the SUMMARY: write a concise 2-3 sentence summary in all 3 languages.
    4. Every title and summary must have 3 languages: zh (Simplified Chinese), en (English), de (German).
    5. Keep tone professional, neutral, informative.
    6. Use the EXACT date provided with each article. Do NOT invent dates.
    7. Copy the EXACT url provided with each article into the "url" field.
    8. Return ONLY valid JSON — no markdown fences, no extra text.

    Required JSON shape:
    {
      "aiNews": [
        {"id": "ai-1", "title": {"zh":"..","en":"..","de":".."}, "summary": {"zh":"..","en":"..","de":".."}, "source": "..", "date": "YYYY-MM-DD", "url": "https://..."},
        {"id": "ai-2", ...}, {"id": "ai-3", ...}
      ],
      "politicsNews": [{"id": "pol-1", ...}, ...],
      "stockNews": [{"id": "stk-1", ...}, ...]
    }
""")


def _build_provider_order() -> list[str]:
    """Build provider cascade: preferred provider first, then remaining."""
    preferred = os.getenv("LLM_PROVIDER", "").strip().lower()
    if preferred and preferred in DEFAULT_PROVIDERS:
        remaining = [p for p in DEFAULT_PROVIDERS if p != preferred]
        return [preferred] + remaining
    return list(DEFAULT_PROVIDERS)


def try_ai(provider: str, all_articles: dict[str, list[dict]]) -> dict | None:
    """Try one LLM provider. Returns parsed JSON or None on failure."""
    try:
        from openai import OpenAI
    except ImportError:
        print(f"  ⚠️  openai package not installed, skipping {provider}")
        return None

    if provider == "gemini":
        key   = os.getenv("GEMINI_API_KEY", "")
        model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite")
        client = OpenAI(api_key=key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
    elif provider == "deepseek":
        key   = os.getenv("DEEPSEEK_API_KEY", "")
        model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        client = OpenAI(api_key=key, base_url="https://api.deepseek.com")
    else:  # openai
        key   = os.getenv("OPENAI_API_KEY", "")
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        client = OpenAI(api_key=key)

    if not key:
        print(f"  ⏭️  No API key for {provider}, skipping")
        return None

    sections: list[str] = []
    for cat, label in [("ai", "AI / FRONTIER SCIENCE"), ("politics", "GLOBAL POLITICS"), ("stocks", "STOCK MARKET")]:
        arts = all_articles.get(cat, [])
        if arts:
            items = "\n".join(f"- [{a['source']}] [{a['date']}] {a['title']}: {a['summary'][:150]} (url: {a.get('url', '')})" for a in arts)
            sections.append(f"=== {label} ===\n{items}")

    user_msg = "\n\n".join(sections)
    print(f"\n🤖 Trying {provider} ({model})...")

    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model=model, temperature=0.3,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": user_msg},
                ],
            )
            raw = resp.choices[0].message.content or "{}"
            # Strip markdown code fences if present
            raw = re.sub(r"^```(?:json)?\s*", "", raw.strip())
            raw = re.sub(r"\s*```$", "", raw.strip())
            data = json.loads(raw)

            # Ensure every news item has a url field (fallback to empty string)
            for key_name in ("aiNews", "politicsNews", "stockNews"):
                for item in data.get(key_name, []):
                    item.setdefault("url", "")

            print(f"   ✅ {provider} succeeded!")
            return data
        except json.JSONDecodeError as exc:
            print(f"   ❌ {provider}: invalid JSON — {exc}")
            return None
        except Exception as exc:
            if "429" in str(exc) or "quota" in str(exc).lower():
                wait = 20 * (attempt + 1)
                print(f"   ⏳ Rate limited ({attempt+1}/3), waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"   ❌ {provider} error: {exc}")
                return None

    print(f"   ❌ {provider}: retries exhausted")
    return None

# ─── Main ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Anti-FOMO Daily News Fetcher")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print result to stdout without writing data.json")
    args = parser.parse_args()

    print("=" * 56)
    print("  Anti-FOMO Daily — News Fetcher")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 56)

    # Stage 1: Fetch RSS
    all_articles: dict[str, list[dict]] = {}
    for cat in ("ai", "politics", "stocks"):
        print(f"\n📂 {cat.upper()}")
        all_articles[cat] = fetch_rss(cat)

    # Stage 2: Try AI providers in priority order
    provider_order = _build_provider_order()
    print(f"\n🔧 Provider order: {' → '.join(provider_order)}")

    ai_result = None
    for provider in provider_order:
        ai_result = try_ai(provider, all_articles)
        if ai_result and ai_result.get("aiNews"):
            break
        ai_result = None

    if ai_result:
        print("\n🎯 Using AI-generated summaries")
        output = {
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "aiNews":       ai_result.get("aiNews", []),
            "politicsNews": ai_result.get("politicsNews", []),
            "stockNews":    ai_result.get("stockNews", []),
        }
    else:
        print("\n📋 Using raw RSS (AI unavailable)")
        output = {
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "aiNews":       raw_fallback("ai", all_articles.get("ai", [])),
            "politicsNews": raw_fallback("politics", all_articles.get("politics", [])),
            "stockNews":    raw_fallback("stocks", all_articles.get("stocks", [])),
        }

    total = sum(len(output[k]) for k in ["aiNews", "politicsNews", "stockNews"])
    result_json = json.dumps(output, ensure_ascii=False, indent=2)

    if args.dry_run:
        print(f"\n{'=' * 56}")
        print(f"  🏃 DRY RUN — {total} items (not written to disk)")
        print(f"{'=' * 56}")
        print(result_json)
    else:
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_PATH.write_text(result_json, encoding="utf-8")
        print(f"\n{'=' * 56}")
        print(f"  ✅ Done! Wrote {total} items to {OUTPUT_PATH}")
        print(f"{'=' * 56}")

if __name__ == "__main__":
    main()
