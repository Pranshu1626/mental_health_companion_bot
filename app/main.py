from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.reply_engine import generate_final_reply
from src.recommendations import get_recommendations
from src.predict import predict_emotion

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/api/health")
def health():
    return {"message": "API is running"}

@app.post("/api/chat")  
async def chat(chat_data: ChatRequest):
    message = chat_data.message
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

@app.get("/")
async def root():
    return FileResponse("app/static/index.html")

@app.exception_handler(404)
async def not_found(request: Request, exc):
    return FileResponse("app/static/index.html")
