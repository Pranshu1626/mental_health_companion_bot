# MindMate — Mental Health Companion Chatbot

MindMate is an AI-powered **mental health companion chatbot** designed to provide empathetic, non-judgmental, and supportive conversations. It combines local emotion detection with LLM-generated responses and optional wellness recommendations in a clean web interface.

> ⚠️ **Important Disclaimer**
> This project is for supportive conversation and educational purposes only.
> It is **not** medical advice, **not** a diagnostic tool, and **not** a substitute for licensed mental health care.

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

- detecting emotion from user text using a local ML model,
- generating emotionally aware responses through an LLM,
- optionally suggesting supportive wellness content,
- serving everything through a lightweight FastAPI web application.

This repository is ideal for learning and building in areas like:

- applied NLP,
- emotion-aware chatbot systems,
- FastAPI-based product prototypes,
- safe AI interaction design.

---

## Key Features

- **Emotion Detection** from user messages (scikit-learn model).
- **Empathetic Chat Responses** generated via OpenRouter-compatible LLM API.
- **Optional Recommendations** such as videos/images for wellness support.
- **Web Experience** with landing page, login flow, and chat interface.
- **REST API** for chat, health checks, and optional history management.
- **Optional Supabase Integration** for storing conversation history and keys.
- **Docker Support** for consistent deployment environments.

---

## Live Demo

- **Homepage**: https://mental-health-companion-bot.onrender.com

For local development, once running:

- Landing page: `http://127.0.0.1:8000/`
- Chat UI: `http://127.0.0.1:8000/chat`

---

## Tech Stack

### Frontend
- HTML, CSS, JavaScript (served as static files)

### Backend
- FastAPI
- Uvicorn

### ML / NLP
- scikit-learn
- NLTK
- joblib

### LLM
- OpenRouter-compatible API (`OPENROUTER_API_KEY`)

### Optional Data Layer
- Supabase (`SUPABASE_URL`, `SUPABASE_KEY`)

### DevOps
- Docker

---

## How It Works

1. User sends a message via the chat interface.
2. Backend receives it through `POST /api/chat` (or `POST /chat`).
3. Emotion is predicted in `src/predict.py`.
4. Context-aware supportive reply is generated in `src/llm_service.py` and composed in `src/reply_engine.py`.
5. Optional media recommendations are selected via `src/recommendations.py`.
6. If configured, conversation data is persisted to Supabase.

---

## Project Structure

```text
mental_health_companion_bot/
├── app/
│   ├── main.py                  # FastAPI app + routes + UI serving
│   └── static/                  # landing/login/chat UI + assets
├── src/
│   ├── predict.py               # emotion prediction logic
│   ├── llm_service.py           # LLM response generation
│   ├── reply_engine.py          # response orchestration
│   ├── recommendations.py       # media recommendations
│   ├── prepare_data.py          # preprocessing utilities
│   ├── train.py                 # model training script
│   └── utils.py                 # text cleaning helpers
├── models/
│   └── emotion_model.joblib
├── notebooks/
│   └── emotion_model.ipynb
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

### 4) Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Required for LLM responses
OPENROUTER_API_KEY=your_openrouter_key

# Optional (enables chat history + public-key endpoints)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

Notes:
- If Supabase variables are missing, app features depending on Supabase are disabled.
- `.env` is loaded in the FastAPI app startup path.

### 5) Run the Application

```bash
uvicorn app.main:app --reload
```

Then open:
- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/chat`

---

## Run with Docker

### Build Image

```bash
docker build -t mindmate .
```

### Run Container

```bash
docker run --rm -p 8000:8000 \
  -e OPENROUTER_API_KEY="your_key" \
  -e SUPABASE_URL="your_url" \
  -e SUPABASE_KEY="your_key" \
  mindmate
```

Open: `http://127.0.0.1:8000/`

---

## API Reference

### Health Check
- `GET /api/health`

### Chat Endpoints
- `POST /api/chat`
- `POST /chat`

#### Example Request

```json
{
  "message": "I feel stressed and overwhelmed lately.",
  "user_id": "optional-user-id",
  "conversation_history": []
}
```

#### Example Response (shape)

```json
{
  "emotion": "anxiety",
  "reply": "...supportive reply...",
  "video": { "title": "...", "url": "..." },
  "image": "https://...",
  "encrypted": false
}
```

### Optional Supabase-Backed Endpoints
- `GET /api/history/{user_id}`
- `DELETE /api/history/{user_id}`
- `POST /api/user/public-key`

---

## Security & Privacy Notes

If you store user conversation data:

- Treat all chat messages as **sensitive data**.
- Limit database access with strict policies.
- Avoid storing or logging raw personal text when possible.
- Consider encryption at rest and secure key management.
- Add rate limiting and abuse protections for public deployments.

For safety-critical use, consider adding a dedicated crisis escalation flow and localized emergency resources.

---

## Limitations

- The system is not a replacement for clinical evaluation.
- Model quality depends on training data coverage and prompt quality.
- Emotion predictions can be imperfect and context-sensitive.
- External model/API availability can affect chatbot response quality.

---

## Contributing

Contributions are welcome.

1. Fork this repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request with a clear description.

Suggested contribution areas:
- model improvement and calibration,
- conversation safety and guardrails,
- test coverage,
- UI accessibility and UX upgrades,
- deployment and observability enhancements.

---

## Roadmap

- [ ] Add automated tests (API + inference + safety checks)
- [ ] Add CI pipeline using GitHub Actions
- [ ] Improve emotion model calibration and confidence handling
- [ ] Add explicit crisis-safety workflow and policy prompts
- [ ] Add retrieval-based coping strategy knowledge base with citations
- [ ] Add multilingual support
- [ ] Improve analytics and observability for production deployments

---

## License

No license file is currently defined in this repository.

If you plan to open-source this project for reuse, consider adding a license such as MIT, Apache-2.0, or GPL-3.0.

---

## Author

**Pranshu Patel**

GitHub: [@Pranshu1626](https://github.com/Pranshu1626)
