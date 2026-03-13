# 🧠 Mental Health Companion Chatbot

An AI-powered Mental Health Companion Chatbot that detects user emotions from text and provides empathetic, supportive responses.
The system is designed to help students cope with stress, anxiety, loneliness, and everyday emotional challenges through safe conversational support.

---

## 🚀 Features

* Emotion detection using Machine Learning (GoEmotions dataset)
* Human-like empathetic responses
* Interactive chat UI
* FastAPI backend for real-time interaction
* End-to-end ML pipeline (data → training → API → UI)
* Modular project structure for scalability

---

## 🧩 Tech Stack

**Frontend**

* HTML
* CSS
* JavaScript

**Backend**

* FastAPI
* Uvicorn

**Machine Learning**

* Python
* Scikit-learn
* TF-IDF Vectorizer
* Logistic Regression
* NLTK

**Tools**

* Pandas
* Joblib
* Jupyter Notebook

---

## 📁 Project Structure

```
mental_health_bot/
│
├── app/
│   ├── main.py
│   ├── responses.py
│   └── static/
│       └── index.html
│
├── src/
│   ├── _init_.py  #this should be empty
│   ├── train.py
│   ├── predict.py
│   ├── prepare_data.py
│   ├── utils.py
│   ├── reply_engine.py
│   ├── recommendations.py
│   └── llm_service.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   └── emotion_model.joblib
│
├── notebooks/
│   └── emotion_model.ipynb
│
└── requirements.txt
```

---

## ⚙️ Installation

```bash
git clone https://github.com/Pranshu1626/mental_health_companion_bot
cd mental_health_bot
pip install -r requirements.txt
```

---

## 📊 Data Preparation

Place GoEmotions dataset files inside:

```
data/raw/
```

Then run:

```bash
python -m src.prepare_data
```

---

## 🧠 Train Model

```bash
python -m src.train
```

This will generate:

```
models/emotion_model.joblib
```

---

## ▶️ Run Backend

```bash
uvicorn app.main:app --reload
```

Open in browser:

```
http://127.0.0.1:8000
```

---

## 💬 How It Works

1. User enters text in UI
2. Backend predicts emotion using trained model
3. Response engine generates empathetic reply
4. Chat interface displays supportive conversation

---

## 🎯 Use Cases

* Student emotional support
* Stress monitoring tools
* Wellness apps


---

## 🔮 Future Improvements

* Transformer model (DistilBERT)
* Conversation memory
* Crisis risk detection
* Voice interface
* Personalization
* RAG-based coping suggestions

---

## ⚠️ Disclaimer

This chatbot is **not a replacement for professional mental health support**.
It is intended for supportive conversation and educational purposes only.

---

## 👤 Author

Pranshu Patel

---

