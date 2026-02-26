from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import random
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.reply_engine import generate_final_reply

from src.recommendations import get_recommendations

from src.predict import predict_emotion
# from app.responses import responses
from app.responses import generate_reply



app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def home():
    return FileResponse("app/static/index.html")

@app.post("/chat")
def chat(message: str):
    emotion = predict_emotion(message)

    reply = generate_final_reply(message, emotion)

    message_lower = message.lower()

    VIDEO_INTENT = ["video", "watch", "suggest", "recommend", "help me calm", "what should i do"]

    show_recs = (
        emotion in ["anxiety", "sadness"] or
        any(w in message_lower for w in VIDEO_INTENT)
    )

    video, image = get_recommendations(emotion) if show_recs else (None, None)

    return {
        "emotion": emotion,
        "reply": reply,
        "video": video,
        "image": image
    }
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/ui")
def ui():
    return FileResponse("app/static/index.html")

@app.get("/")
def home():
    return {"message": "API is running"}