import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer

from src.utils import clean_text

df = pd.read_csv("data/processed/dataset.csv")

df = df.dropna(subset=["text", "label"])
df["text"] = df["text"].astype(str).apply(clean_text)

X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42
)

model = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=20000)),
    ("clf", LogisticRegression(max_iter=1000))
])

model.fit(X_train, y_train)

print("Accuracy:", model.score(X_test, y_test))

import os
os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/emotion_model.joblib")

print("Model saved → models/emotion_model.joblib")