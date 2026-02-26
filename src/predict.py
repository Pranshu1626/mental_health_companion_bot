import joblib
from src.utils import clean_text

model = joblib.load("models/emotion_model.joblib")

ANXIETY_KEYWORDS = [
    "stress",
    "stressed",
    "overthinking",
    "overthink",
    "overwhelmed",
    "pressure",
    "falling behind",
    "anxious",
    "worry",
    "worried",
    "tired"
]

SAD_KEYWORDS = [
    "alone",
    "lonely",
    "sad",
    "empty",
    "hopeless",
    "bad day"
]


def predict_emotion(text: str):
    text_lower = text.lower()
    for w in ANXIETY_KEYWORDS:
        if w in text_lower:
            return "anxiety"

    for w in SAD_KEYWORDS:
        if w in text_lower:
            return "sadness"
    text = clean_text(text)
    return model.predict([text])[0]
