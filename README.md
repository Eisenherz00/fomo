# Anti-FOMO Daily

> Your daily 10-minute intel briefing on **AI**, **Global Politics**, and **Markets** — in three languages (中文 / EN / DE).

## Architecture

```
┌────────────────────┐     ┌──────────────┐     ┌────────────────────┐
│  RSS Feeds         │────▶│  Python      │────▶│  public/data.json  │
│  (MIT Tech Review, │     │  Fetcher +   │     │  (consumed by the  │
│   BBC, CNBC, etc.) │     │  AI Summary) │     │   Next.js app)     │
└────────────────────┘     └──────────────┘     └────────────────────┘
        GitHub Actions: runs every 12 h (04:30 & 16:30 UTC)
```

| Layer      | Tech                              |
| ---------- | --------------------------------- |
| Frontend   | Next.js 16, React 19, Tailwind v4 |
| Backend    | Python 3.12 (feedparser + openai) |
| AI         | OpenAI / Gemini / DeepSeek        |
| CI/CD      | GitHub Actions (scheduled CRON)   |
| Hosting    | Vercel / any static host          |

## Getting Started

### Prerequisites

- **Node.js** ≥ 20 & **npm**
- **Python** ≥ 3.11 (for the data pipeline)

### Install & Run

```bash
# Frontend
npm install
npm run dev          # → http://localhost:3000

# Python data pipeline (optional — mock data is bundled)
python3 -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
cp scripts/.env.example scripts/.env   # fill in your API key(s)
python scripts/fetch_and_summarize.py
```

### Environment Variables

Copy `scripts/.env.example` to `scripts/.env` and fill in at least one provider key:

| Variable          | Description                          | Default              |
| ----------------- | ------------------------------------ | -------------------- |
| `LLM_PROVIDER`    | `openai` \| `gemini` \| `deepseek`  | `openai`             |
| `OPENAI_API_KEY`  | OpenAI API key                       | —                    |
| `OPENAI_MODEL`    | Model name                           | `gpt-4o-mini`        |
| `GEMINI_API_KEY`  | Google Gemini API key                | —                    |
| `GEMINI_MODEL`    | Model name                           | `gemini-2.0-flash-lite` |
| `DEEPSEEK_API_KEY`| DeepSeek API key                     | —                    |
| `DEEPSEEK_MODEL`  | Model name                           | `deepseek-chat`      |

## CI/CD

The GitHub Actions workflow (`.github/workflows/update-news.yml`) runs twice daily, fetches RSS, generates AI summaries, and commits `public/data.json` to `main`.

## License

MIT
