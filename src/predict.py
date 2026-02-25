import joblib
from src.utils import clean_text

model = joblib.load("models/emotion_model.joblib")

def predict_emotion(text: str):
    text = clean_text(text)
    return model.predict([text])[0]