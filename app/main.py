from fastapi import FastAPI
import random
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.predict import predict_emotion
# from app.responses import responses
from app.responses import generate_reply


app = FastAPI()

@app.get("/")
def home():
    return FileResponse("app/static/index.html")

@app.post("/chat")
def chat(message: str):
    emotion = predict_emotion(message)

    reply = generate_reply(emotion, message)

    return {
        "emotion": emotion,
        "reply": reply
    }
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/ui")
def ui():
    return FileResponse("app/static/index.html")