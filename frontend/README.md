AI Landing Page Generator

An AI-powered multi-agent system that generates marketing landing pages from Google Play Store applications.

The system extracts app information from a Google Play URL, analyzes the app’s marketing positioning, generates landing page content using AI agents, and produces a mobile-optimized landing page with dynamic CTA behavior.

This project was built as part of an AI Agent Developer home assignment.

Features
Google Play Store app extraction
AI-generated landing page copy
LangGraph multi-agent workflow
Dynamic CTA modes:
Google Play Install
Stripe Subscription
Screenshot selection agent
Mobile-first landing page renderer
FastAPI backend
Next.js frontend
Structured JSON output
Loading pipeline visualization
Tech Stack
Backend
Python
FastAPI
LangGraph
Pydantic
Google Play Scraper
Gemini / Claude APIs
Frontend
Next.js
React
TypeScript
Tailwind CSS
Project Structure
ai-landing-agent/
│
├── backend/
│   ├── agents/
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── workflows/
│   └── main.py
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── types/
│   └── public/
│
└── README.md
Architecture Overview

The system uses a graph-based multi-agent workflow implemented with LangGraph.

Each agent is responsible for a single task in the pipeline.

Workflow
Google Play URL
    ↓
Extraction Agent
    ↓
Marketing Intelligence Agent
    ↓
Screenshot Selection Agent
    ↓
Copywriter Agent
    ↓
CTA Agent
    ↓
Final Payload Assembly
    ↓
Frontend Renderer
Agents
1. Extraction Agent

Responsible for extracting application metadata from Google Play.

Extracted data includes:

app title
description
icon
screenshots
ratings
reviews
installs
Input
Google Play URL
Output
{
  "title": "...",
  "description": "...",
  "screenshots": []
}
2. Marketing Intelligence Agent

Analyzes the extracted app data and generates structured marketing insights.

The agent identifies:

target audience
value proposition
key benefits
hero messaging
strongest reviews
conversion-focused positioning
Purpose

This separates strategic marketing analysis from copy generation.

3. Screenshot Selection Agent

Chooses which screenshots should appear in:

the hero section
the screenshot gallery

Current implementation uses deterministic heuristics based on Google Play ordering.

The architecture allows replacing this node with a multimodal screenshot-ranking model in the future.

4. Copywriter Agent

Generates structured landing page content.

The output includes:

hero section
features
benefits
social proof
FAQ
metadata
media gallery

The agent receives:

extracted app data
marketing insights
selected screenshots
CTA mode
5. CTA Agent

Responsible for deterministic CTA behavior.

Supported modes:

Install Mode

Redirects users directly to the Google Play Store.

Stripe Subscription Mode

Redirects users to a Stripe Payment Link.

This design keeps payment logic deterministic and separate from LLM behavior.

Why LangGraph

LangGraph was chosen to model the system as a graph-based multi-agent workflow rather than a sequential script.

Benefits:

modular architecture
isolated responsibilities
easier testing
future extensibility
support for branching and retries
clearer agent orchestration

Each node owns one responsibility and communicates through shared workflow state.

API
Health Check
GET /health
Generate Landing Page
POST /generate-landing-page
Request
{
  "googlePlayUrl": "https://play.google.com/store/apps/details?id=com.spotify.music",
  "ctaMode": "install"
}
Stripe Mode Example
{
  "googlePlayUrl": "https://play.google.com/store/apps/details?id=com.spotify.music",
  "ctaMode": "stripe_subscription",
  "stripeCheckoutUrl": "https://buy.stripe.com/example"
}
Running the Project
1. Clone the Repository
git clone <repository-url>
cd ai-landing-agent
Backend Setup
1. Navigate to backend
cd backend
2. Create virtual environment
Windows
python -m venv venv
venv\\Scripts\\activate
Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Create .env
GEMINI_API_KEY=your_key
CLAUDE_API_KEY=your_key
5. Run backend
uvicorn main:app --reload

Backend runs on:

http://127.0.0.1:8000

Swagger docs:

http://127.0.0.1:8000/docs
Frontend Setup
1. Navigate to frontend
cd frontend
2. Install dependencies
npm install
3. Create .env.local
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
4. Run frontend
npm run dev

Frontend runs on:

http://localhost:3000
Example Test URLs
Spotify
https://play.google.com/store/apps/details?id=com.spotify.music
Notion
https://play.google.com/store/apps/details?id=notion.id
ChatGPT
https://play.google.com/store/apps/details?id=com.openai.chatgpt
Strava
https://play.google.com/store/apps/details?id=com.strava
Architectural Decisions
Separation of Responsibilities

Each agent handles one responsibility only.

This improves:

maintainability
testing
scalability
future extensibility
Deterministic CTA Logic

Payment and redirect behavior should not depend on LLM output.

For that reason, CTA generation is handled by a dedicated deterministic agent.

Structured Outputs

All AI-generated content uses structured Pydantic schemas.

Benefits:

predictable frontend rendering
schema validation
safer API contracts
easier debugging
Frontend/Backend Separation

The backend is responsible for:

orchestration
AI generation
business logic

The frontend is responsible for:

rendering
user interaction
preview flow
Future Improvements

Potential future enhancements:

multimodal screenshot ranking
A/B testing agent
SEO optimization agent
localization support
template system
analytics integration
dynamic Stripe Checkout session generation
persistent database storage
HTML export
CMS integration
Notes

For the MVP version:

Stripe mode uses a preconfigured Stripe Payment Link
Screenshot ranking uses deterministic heuristics
Landing pages are stored locally in browser storage for preview

These decisions were made to keep the architecture clean while focusing on the agent workflow and system design.