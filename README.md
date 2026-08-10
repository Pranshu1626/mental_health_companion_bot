# MindMate — Mental Health Companion Chatbot

MindMate is a FastAPI-based, AI-powered mental health companion chatbot that detects emotion from user messages with a local model and generates short, empathetic replies using a connected LLM. It is intended as a learning/prototype system and not a replacement for professional care.

> ⚠️ Important Disclaimer  
> This project provides supportive conversational responses for educational and prototyping purposes only. It is **not** medical advice, **not** a diagnostic tool, and **not** a substitute for licensed mental health care. If someone is in immediate danger, contact local emergency services.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Live Demo](#live-demo)
- [Tech Stack](#tech-stack)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [1) Clone the Repository](#1-clone-the-repository)
  - [2) Create & Activate Virtual Environment](#2-create--activate-virtual-environment)
  - [3) Install Dependencies](#3-install-dependencies)
  - [4) Configure Environment Variables](#4-configure-environment-variables)
  - [5) Run the Application](#5-run-the-application)
- [Run with Docker](#run-with-docker)
- [API Reference](#api-reference)
- [Security & Privacy Notes](#security--privacy-notes)
- [Limitations](#limitations)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [License](#license)
- [Author](#author)

---

## Overview

MindMate aims to make first-line emotional support more accessible by:

- detecting emotion from user text using a local ML model (scikit-learn + joblib),
- generating emotionally aware replies through an LLM API,
- optionally suggesting wellness media, and
- serving everything through a lightweight FastAPI web application with a static HTML/CSS/JS UI.

---

## Key Features

- Emotion detection from user messages (keyword heuristics + scikit-learn model).
- Empathetic chat replies via an LLM client (the repository's LLM client is currently configured to use a Groq/OpenAI-compatible endpoint).
- Optional video/image recommendations for certain emotions.
- Web UI: landing page, login flow, and chat interface (served from `app/static`).
- Optional Supabase integration for storing chat history and public keys.
- Docker support for reproducible deployment.

---

## Live Demo

- Homepage: https://mental-health-companion-bot.onrender.com

Local UIs (after running):
- Landing page: http://127.0.0.1:8000/
- Chat UI: http://127.0.0.1:8000/chat

---

## Tech Stack

### Frontend
- HTML, CSS, JavaScript (served as static files from `app/static`)

### Backend
- FastAPI + Uvicorn

### ML / NLP
- scikit-learn, joblib, nltk, pandas, numpy

### LLM
- openai-compatible client usage (configured in `src/llm_service.py`); environment key expected by the current code: `GROQ_API_KEY`

### Optional Data Layer
- Supabase (requires `SUPABASE_URL` and `SUPABASE_KEY`)

### DevOps
- Dockerfile included

---

## How It Works

1. User sends a message via the chat UI.
2. The backend (POST /api/chat) calls `src/predict.predict_emotion`.
   - A small set of keyword checks short-circuit to "anxiety" or "sadness".
   - Otherwise the pre-trained scikit-learn model in `models/emotion_model.joblib` is used.
3. `src/reply_engine.generate_final_reply` calls `src/llm_service.generate_llm_reply` to build a supportive reply.
4. `src/recommendations.get_recommendations` may return video/image suggestions for certain emotions or user intents.
5. If Supabase is configured, messages are persisted in the `messages` table.

---

## Project Structure

```text
mental_health_companion_bot/
├── app/
│   ├── main.py                  # FastAPI app + routes + static UI serving
│   └── static/                  # landing/login/chat UI + assets
├── src/
│   ├── predict.py               # emotion prediction logic (keywords + model)
│   ├── llm_service.py           # LLM request logic & prompt
│   ├── reply_engine.py          # response orchestration
│   ├── recommendations.py       # media recommendations
│   ├── prepare_data.py          # preprocessing utilities
│   ├── train.py                 # model training script
│   └── utils.py                 # text cleaning helpers
├── models/
│   └── emotion_model.joblib     # trained emotion model (required)
├── notebooks/
│   └── emotion_model.ipynb      # experimentation/training notebook
├── data/
│   ├── raw/
│   └── processed/
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## Getting Started

### 1) Clone the Repository

```bash
git clone https://github.com/Pranshu1626/mental_health_companion_bot.git
cd mental_health_companion_bot
```

### 2) Create & Activate Virtual Environment

```bash
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

### 3) Install Dependencies

```bash
pip install -r requirements.txt
```

Note: requirements.txt currently includes `python-dotenv` twice — removing the duplicate is safe.

### 4) Configure Environment Variables

Create a `.env` file in the project root. The code expects:

```bash
# Required for LLM responses (current code uses GROQ/OpenAI-compatible endpoint)
GROQ_API_KEY=your_api_key_here

# Optional (enables chat history + public-key endpoints)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

If you adapt the LLM client in `src/llm_service.py` to another provider (e.g., OpenRouter), update the environment variable name and client configuration accordingly.

### 5) Run the Application

```bash
uvicorn app.main:app --reload
```

Open:
- http://127.0.0.1:8000/
- http://127.0.0.1:8000/chat

---

## Run with Docker

### Build Image

```bash
docker build -t mindmate .
```

### Run Container

```bash
docker run --rm -p 8000:8000 \
  -e GROQ_API_KEY="your_key" \
  -e SUPABASE_URL="your_url" \
  -e SUPABASE_KEY="your_key" \
  mindmate
```

Open http://127.0.0.1:8000/

---

## API Reference

### Health Checks
- `GET /health`
- `GET /api/health`

### Chat Endpoints
- `POST /api/chat`
- `POST /chat`

Example request body:

```json
{
  "message": "I feel stressed and overwhelmed lately.",
  "user_id": "optional-user-id",
  "conversation_history": []
}
```

Shape of response:

```json
{
  "emotion": "anxiety",
  "reply": "...supportive reply...",
  "video": { "title": "...", "url": "..." },
  "image": "https://...",
  "encrypted": false
}
```

Optional Supabase-backed endpoints (require SUPABASE_* env vars):
- `GET /api/history/{user_id}`
- `DELETE /api/history/{user_id}`
- `POST /api/user/public-key`

---

## Security & Privacy Notes

- Treat chat messages as sensitive data.
- Limit database access and use strict row-level policies when enabling persistence.
- Avoid storing raw personal PII; consider encryption at rest for stored messages.
- Add rate-limiting, abuse protections, and monitoring for public deployments.
- For safety-critical applications, implement a crisis escalation flow and localized emergency resources.

---

## Limitations

- Not a replacement for clinical evaluation.
- Emotion detection uses a small keyword list and a simple scikit-learn model — accuracy will vary.
- LLM responses depend on external API availability and model behavior.
- No explicit QA, automated tests, or CI pipeline in the repo yet.

---

## Contributing

Contributions welcome:
1. Fork the repo.
2. Create a feature branch.
3. Commit and push changes.
4. Open a pull request with tests and a clear description.

Suggested areas: model calibration, safety prompts, tests, UI/UX, accessibility, CI.

---

## Roadmap

- Add automated tests (API + inference)
- Add CI
- Improve model calibration and confidence handling
- Add crisis-safety workflow
- Add retrieval-based knowledge base with citations
- Multilingual support and analytics

---

## License

No license file is currently present. If you plan to open-source this project, add a LICENSE file (for example MIT, Apache-2.0, or GPL-3.0).

---

## Troubleshooting & Notes

- If you see `FileNotFoundError` for `models/emotion_model.joblib`, run `src/train.py` (inspect and adapt) or provide a trained model at `models/emotion_model.joblib`.
- If LLM calls fail, confirm `GROQ_API_KEY` is set and that `src/llm_service.py` is configured correctly for your provider and endpoint.
- Duplicate `python-dotenv` in requirements — harmless but tidy to remove.
- If switching to OpenRouter/OpenAI, update `src/llm_service.py` to use the appropriate client and env variable (`OPENROUTER_API_KEY` or `OPENAI_API_KEY`) and update this README accordingly.

---

## Author

**Pranshu Patel**  
GitHub: [@Pranshu1626](https://github.com/Pranshu1626)
