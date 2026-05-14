# AI Landing Page Generator

A multi-agent AI system that takes a Google Play Store URL and automatically generates a complete, conversion-optimised landing page for a mobile app.

---

## How it works

The backend runs a **LangGraph** pipeline where each node is a specialised AI agent:

```
Google Play URL
      │
      ▼
[1] Extraction Agent  ─── scrapes app metadata, screenshots, reviews
      │
      ▼
[2] Marketing Agent   ─── identifies target audience, value proposition, emotional hooks
      │
      ▼
[3] Screenshot Agent  ─── selects the strongest screenshots for the page
      │
      ▼
[4] Copywriter Agent  ─── generates hero, features, benefits, social proof, FAQ, SEO metadata
      │
      ▼
[5] CTA Agent         ─── configures CTA mode (Play Store install or Stripe subscription)
      │
      ▼
  Final Payload  →  Next.js frontend renders the live landing page
```

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend API | Python · FastAPI |
| Agent orchestration | LangGraph |
| LLM | Claude Sonnet (`claude-sonnet-4-20250514`) via LangChain |
| App data extraction | `google-play-scraper` |
| Frontend | Next.js 16 · React 19 · TypeScript |
| Styling | Tailwind CSS v4 |

---

## Project structure

```
ai-landing-agent/
├── backend/
│   ├── main.py                    # FastAPI app entry point
│   ├── api/
│   │   └── routes.py              # POST /generate-landing-page
│   ├── agents/
│   │   ├── extraction_agent.py    # Google Play scraper
│   │   ├── marketing_agent.py     # Marketing analysis
│   │   ├── screenshot_agent.py    # Screenshot selection
│   │   ├── copywriter_agent.py    # Landing page copy
│   │   └── cta_agent.py           # CTA configuration
│   ├── workflows/
│   │   └── landing_graph.py       # LangGraph pipeline definition
│   ├── models/
│   │   └── schemas.py             # Pydantic request/response models
│   ├── services/
│   │   ├── llm_service.py         # Claude / Gemini client setup
│   │   ├── playstore_service.py   # Play Store data fetcher
│   │   └── file_service.py        # Output file helpers
│   └── outputs/                   # JSON snapshots of generated pages
└── frontend/
    ├── app/
    │   ├── page.tsx               # Generator UI (URL input + progress)
    │   └── layout.tsx             # Root layout
    └── src/
        ├── components/
        │   └── LandingPagePreview.tsx  # Rendered landing page
        ├── lib/
        │   └── api.ts             # API client
        └── types/
            └── landing-page.ts    # Shared TypeScript types
```

---

## Getting started

### Prerequisites

- Python 3.11+
- Node.js 20+
- An [Anthropic API key](https://console.anthropic.com/)

### 1 — Backend

```bash
cd backend

# create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# install dependencies
pip install fastapi uvicorn langgraph langchain-anthropic langchain-google-genai google-play-scraper python-dotenv pydantic

# configure environment variables
cp .env.example .env
# edit .env and set your ANTHROPIC_API_KEY

# start the server
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

### 2 — Frontend

```bash
cd frontend

npm install
npm run dev
```

The UI will be available at `http://localhost:3000`.

---

## Environment variables

### `backend/.env`

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | Claude API key |
| `GOOGLE_API_KEY` | No | Gemini API key (fallback LLM) |

### `frontend/.env.local`

| Variable | Required | Description |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | Yes | Backend base URL (e.g. `http://localhost:8000`) |

---

## API reference

### `POST /generate-landing-page`

**Request body**

```json
{
  "googlePlayUrl": "https://play.google.com/store/apps/details?id=com.spotify.music",
  "ctaMode": "install",
  "stripeCheckoutUrl": null,
  "customCtaButtonText": null,
  "planId": null
}
```

`ctaMode` accepts `"install"` or `"stripe_subscription"`.  
When `ctaMode` is `"stripe_subscription"`, `stripeCheckoutUrl` is required.

**Response** — `FinalLandingPagePayload`

```json
{
  "app_name": "Spotify",
  "app_icon": "https://...",
  "google_play_url": "https://...",
  "landing_page": {
    "hero": { "headline": "...", "subheadline": "...", "primary_cta_text": "..." },
    "features": [...],
    "benefits": [...],
    "social_proof": [...],
    "media_gallery": [...],
    "faq": [...],
    "metadata": { "title": "...", "description": "..." }
  },
  "cta": { "mode": "install", "text": "...", "url": "...", "message": "..." },
  "screenshot_selection": { ... }
}
```

### `GET /health`

Returns `{ "status": "ok" }`.

---

## CTA modes

| Mode | Behaviour |
|---|---|
| `install` | CTA button links directly to the Google Play Store listing |
| `stripe_subscription` | CTA button links to a Stripe Checkout session; copy is subscription-focused |

---

## Development notes

- LangGraph state is typed via `LandingGraphState` in [backend/workflows/landing_graph.py](backend/workflows/landing_graph.py).
- All agent outputs are validated by Pydantic models defined in [backend/models/schemas.py](backend/models/schemas.py).
- Generated JSON payloads are saved to `backend/outputs/` for debugging.
- The frontend stores the last generated payload in `localStorage` to pass it to the `/preview` route without a re-request.
