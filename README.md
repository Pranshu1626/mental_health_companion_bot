# MindMate — Mental Health Companion Chatbot

MindMate is a lightweight mental-health companion chatbot that:
- **Detects emotion** from user text (local ML model)
- Generates a **supportive, friend-like response** (LLM via OpenRouter)
- Optionally provides **wellness recommendations** (videos/images)
- Ships with a **web UI** (landing + login + chat) served by a **FastAPI** backend
- Can optionally **store chat history** in **Supabase**

> Important: This project is for supportive conversation and educational purposes only.  
> It is **not** medical advice and is **not a substitute** for professional mental health care.

---

## Demo (Local)

1. Start the server (instructions below)
2. Open in your browser:
   - Landing page: `http://127.0.0.1:8000/`
   - Chat UI: `http://127.0.0.1:8000/chat`

The chat UI calls the API and returns:
- `emotion`
- `reply`
- optional `video` + `image` recommendations

---

## Features

- Emotion classification from text (scikit-learn model loaded from `models/emotion_model.joblib`)
- FastAPI backend API:
  - `POST /api/chat` (and `POST /chat`) — main chat endpoint
  - `GET /api/history/{user_id}` — fetch stored history (Supabase)
  - `DELETE /api/history/{user_id}` — delete stored history (Supabase)
  - `POST /api/user/public-key` — store public key (Supabase; for optional encrypted workflows)
- Web UI served from FastAPI (`app/static/landing.html`, `login.html`, `index.html`)
- Dockerfile included for containerized deployment

---

## Tech Stack

**Frontend**
- HTML / CSS / JavaScript (static pages served by FastAPI)

**Backend**
- FastAPI + Uvicorn

**ML / NLP**
- scikit-learn, TF‑IDF-style text pipeline (trained offline)
- NLTK, joblib

**LLM**
- OpenRouter (OpenAI-compatible SDK) using `OPENROUTER_API_KEY`

**Database (optional)**
- Supabase (`SUPABASE_URL`, `SUPABASE_KEY`)

---

## Architecture (High Level)

1. User types in the web chat UI
2. UI calls `POST /api/chat` with:
   - `message`
   - optional `conversation_history` (last messages)
   - optional `user_id` (if you want Supabase persistence)
3. Backend:
   - predicts emotion via `src/predict.py`
   - generates a response via `src/llm_service.py`
   - optionally attaches a recommended video/image via `src/recommendations.py`
   - optionally writes messages to Supabase if configured

---

## Project Structure

```text
mental_health_companion_bot/
├── app/
│   ├── main.py                  # FastAPI app + API routes + serving UI pages
│   └── static/                  # landing/login/chat UI + assets
├── src/
│   ├── predict.py               # emotion prediction (keywords + model)
│   ├── llm_service.py           # LLM response generation via OpenRouter
│   ├── reply_engine.py          # glue layer for generating final reply
│   ├── recommendations.py       # optional video/image suggestions
│   ├── prepare_data.py          # dataset preprocessing (optional)
│   ├── train.py                 # model training (optional)
│   └── utils.py                 # text cleaning utilities
├── models/
│   └── emotion_model.joblib
├── notebooks/
│   └── emotion_model.ipynb
├── data/
│   ├── raw/
│   └── processed/
├── requirements.txt
└── Dockerfile
```

---

## Setup (Local)

### 1) Clone
```bash
git clone https://github.com/Pranshu1626/mental_health_companion_bot.git
cd mental_health_companion_bot
```

### 2) Create a virtual environment (recommended)
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Configure environment variables (optional but recommended)

Create a `.env` file in the repo root:

```bash
# Required for LLM replies (OpenRouter)
OPENROUTER_API_KEY=your_openrouter_key

# Optional: enable Supabase history + public-key endpoints
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_service_or_anon_key
```

Notes:
- If Supabase vars are not set, the app still runs, but history storage is disabled.
- `load_dotenv()` is called inside `app/main.py`, so `.env` is loaded automatically.

### 5) Run
```bash
uvicorn app.main:app --reload
```

Open:
- `http://127.0.0.1:8000/` (landing)
- `http://127.0.0.1:8000/chat` (chat UI)

---

## Run with Docker

Build:
```bash
docker build -t mindmate .
```

Run:
```bash
docker run --rm -p 8000:8000 \
  -e OPENROUTER_API_KEY="your_key" \
  -e SUPABASE_URL="your_url" \
  -e SUPABASE_KEY="your_key" \
  mindmate
```

Open:
```text
http://127.0.0.1:8000/
```

---

## API Quick Reference

- `GET /api/health` → API health check
- `POST /api/chat` → main chat endpoint

Example request:
```json
{
  "message": "I feel stressed and overwhelmed lately.",
  "user_id": "optional-user-id",
  "conversation_history": []
}
```

Example response (shape):
```json
{
  "emotion": "anxiety",
  "reply": "…supportive reply…",
  "video": { "title": "…", "url": "…" },
  "image": "https://…",
  "encrypted": false
}
```

---

## Safety, Privacy, and Disclaimer

- This is a **support tool**, not therapy.
- Do **not** use it for emergency situations.
- If you plan to store conversations (Supabase), treat messages as **sensitive data**:
  - restrict database access
  - avoid logging raw user text in production
  - consider encryption-at-rest + secure key handling
- Consider adding a dedicated **crisis flow** (self-harm detection + local emergency resources).

---

## Roadmap Ideas (to help it stand out)

- Add a hosted demo (Render/Fly.io) + screenshots/GIF
- Add crisis-safe guardrails + explicit “what the bot will do” policy
- Add tests (API + model) and GitHub Actions CI
- Replace keyword overrides with a calibrated model thresholding approach
- Add a curated coping-strategies knowledge base (RAG) with citations

---

## Author
Pranshu Patel
