# Mental Health Companion Chatbot (Breathe)

An AI-powered mental health companion chatbot that:
- **Detects emotion** from a user’s text message (ML model)
- Responds with an **empathetic, supportive reply**
- Optionally returns **wellness recommendations** (video/image suggestions) for certain emotions/intents
- Includes a clean **web chat UI** served by a **FastAPI** backend

> ⚠️ This project is for supportive conversation and educational purposes only. It is **not** a replacement for professional mental health care.

---

## Demo (Local)

1. Start the backend
2. Open the app in your browser at: `http://127.0.0.1:8000`
3. Type a message → the API returns:
   - `emotion`
   - `reply`
   - optional `video` + `image` recommendations

---

## Features

- Emotion classification from text (scikit-learn pipeline)
- FastAPI backend with a `/api/chat` endpoint
- Single-page chat UI (HTML/CSS/JS) served from FastAPI
- Optional recommendations for **sadness/anxiety** or “recommend/watch/help me calm…” intents
- Environment variable support via `python-dotenv`
- Docker support for easy deployment

---

## Tech Stack

**Frontend**
- HTML, CSS, JavaScript (single page UI)

**Backend**
- FastAPI
- Uvicorn
- CORS enabled (currently `allow_origins=["*"]`)

**Machine Learning**
- Python
- scikit-learn
- TF‑IDF Vectorizer + Logistic Regression (typical setup for text emotion classification)
- NLTK
- joblib

**Utilities**
- pandas, numpy
- Jupyter Notebook (experiments/training)

---

## API Endpoints

- `GET /api/health` → simple health check
- `POST /api/chat` → main chat endpoint

Example request:
```json
{ "message": "I feel stressed and overwhelmed lately." }
```

Example response (shape):
```json
{
  "emotion": "anxiety",
  "reply": "…empathetic reply…",
  "video": "…optional…",
  "image": "…optional…"
}
```

---

## Project Structure

```text
mental_health_companion_bot/
├── app/
│   ├── main.py                 # FastAPI app + routes
│   └── static/
│       └── index.html          # Chat UI
├── src/
│   ├── __init__.py
│   ├── prepare_data.py
│   ├── train.py
│   ├── predict.py
│   ├── reply_engine.py
│   ├── recommendations.py
│   ├── llm_service.py
│   └── utils.py
├── data/
│   ├── raw/
│   └── processed/
├── models/
│   └── emotion_model.joblib
├── notebooks/
│   └── emotion_model.ipynb
├── requirements.txt
└── Dockerfile
```

> Note: In your README previously you had `src/_init_.py` — in Python it should be `src/__init__.py`.

---

## Setup (Local)

### 1) Clone
```bash
git clone https://github.com/Pranshu1626/mental_health_companion_bot.git
cd mental_health_companion_bot
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) (Optional) Environment variables
Your project loads environment variables using `python-dotenv`, so you can create a `.env` file if needed (for example for OpenAI usage in `src/llm_service.py`).

Example:
```bash
# .env
OPENAI_API_KEY=your_key_here
```

### 4) Run the app
```bash
uvicorn app.main:app --reload
```

Open:
```text
http://127.0.0.1:8000
```

---

## Data + Training (Optional / If you want to retrain)

### Data preparation
Put the dataset files inside:
```text
data/raw/
```

Then run:
```bash
python -m src.prepare_data
```

### Train the model
```bash
python -m src.train
```

The trained model is expected to be saved as:
```text
models/emotion_model.joblib
```

---

## Run with Docker

Build:
```bash
docker build -t mental-health-bot .
```

Run:
```bash
docker run -p 8000:8000 mental-health-bot
```

Open:
```text
http://127.0.0.1:8000
```

---

## How It Works (High Level)

1. User types a message in the web UI
2. UI calls `POST /api/chat`
3. Backend:
   - predicts emotion via `src.predict`
   - generates a supportive reply via `src.reply_engine`
   - optionally attaches recommendations via `src.recommendations`
4. UI displays the bot response

---

## Future Improvements

- Upgrade emotion model to a transformer (e.g., DistilBERT)
- Conversation memory + personalization
- Crisis/self-harm risk detection + safe escalation flow
- Stronger safety guardrails and refusal handling
- RAG-based coping strategies and curated resources

---

## Disclaimer

This chatbot is **not a replacement for professional mental health support**.
If you or someone you know is in immediate danger or considering self-harm, contact local emergency services or a trusted professional right away.

---

## Author

**Pranshu Patel**