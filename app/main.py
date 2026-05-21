import os
from dotenv import load_dotenv

load_dotenv()

import inspect
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from supabase import Client, create_client
from src.reply_engine import generate_final_reply

from src.predict import predict_emotion
from src.recommendations import get_recommendations


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PublicKeyRequest(BaseModel):
    user_id: str
    public_key: str


class ConversationMessage(BaseModel):
    role: str
    content: str
    emotion_detected: Optional[str] = None
    created_at: Optional[str] = None


class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    encrypted: bool = False
    conversation_history: List[ConversationMessage] = Field(default_factory=list)


def get_supabase_client() -> Client:
    if supabase is None:
        raise HTTPException(
            status_code=500,
            detail="Supabase is not configured. Set SUPABASE_URL and SUPABASE_KEY.",
        )

    return supabase


def build_message_with_history(message: str, history: List[ConversationMessage]) -> str:
    if not history:
        return message

    recent_history = history[-10:]
    history_lines = []

    for item in recent_history:
        role = item.role if item.role in {"user", "assistant"} else "user"
        history_lines.append(f"{role}: {item.content}")

    history_text = "\n".join(history_lines)
    return (
        "Recent conversation history:\n"
        f"{history_text}\n\n"
        "Current user message:\n"
        f"{message}"
    )


def model_to_dict(model: ConversationMessage) -> Dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()

    return model.dict()


def generate_reply(
    message: str,
    emotion: str,
    conversation_history: List[ConversationMessage],
) -> str:
    signature = inspect.signature(generate_final_reply)

    if "conversation_history" in signature.parameters:
        return generate_final_reply(
            message,
            emotion,
            conversation_history=[model_to_dict(item) for item in conversation_history[-10:]],
        )

    message_with_history = build_message_with_history(message, conversation_history)
    return generate_final_reply(message_with_history, emotion)


def save_message_to_supabase(
    user_id: Optional[str],
    role: str,
    content: str,
    emotion_detected: Optional[str] = None,
) -> None:
    if not user_id or supabase is None:
        return

    supabase.table("messages").insert(
        {
            "user_id": user_id,
            "role": role,
            "content": content,
            "emotion_detected": emotion_detected,
        }
    ).execute()


@app.get("/api/health")
def health():
    return {"message": "API is running"}


@app.post("/api/user/public-key")
async def save_public_key(payload: PublicKeyRequest):
    client = get_supabase_client()

    client.table("user_keys").upsert(
        {
            "user_id": payload.user_id,
            "public_key": payload.public_key,
        }
    ).execute()

    return {"message": "Public key saved"}


@app.get("/api/history/{user_id}")
async def get_history(user_id: str):
    client = get_supabase_client()

    response = (
        client.table("messages")
        .select("role, content, emotion_detected, created_at")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(20)
        .execute()
    )

    messages = list(reversed(response.data or []))
    return messages


@app.delete("/api/history/{user_id}")
async def delete_history(user_id: str):
    client = get_supabase_client()

    client.table("messages").delete().eq("user_id", user_id).execute()
    return {"message": "Chat history deleted"}


async def handle_chat(chat_data: ChatRequest) -> Dict[str, Any]:
    message = chat_data.message
    emotion = predict_emotion(message)
    reply = generate_reply(message, emotion, chat_data.conversation_history)

    try:
        save_message_to_supabase(
            user_id=chat_data.user_id,
            role="user",
            content=message,
            emotion_detected=emotion,
        )
        save_message_to_supabase(
            user_id=chat_data.user_id,
            role="assistant",
            content=reply,
            emotion_detected=emotion,
        )
    except Exception as exc:
        print(f"Supabase message save failed: {exc}")

    message_lower = message.lower()
    video_intent = [
        "video",
        "watch",
        "suggest",
        "recommend",
        "help me calm",
        "what should i do",
    ]
    show_recs = emotion in ["anxiety", "sadness"] or any(
        word in message_lower for word in video_intent
    )
    video, image = get_recommendations(emotion) if show_recs else (None, None)

    return {
        "emotion": emotion,
        "reply": reply,
        "video": video,
        "image": image,
        "encrypted": chat_data.encrypted,
    }


@app.post("/api/chat")
async def api_chat(chat_data: ChatRequest):
    return await handle_chat(chat_data)


@app.post("/chat")
async def chat(chat_data: ChatRequest):
    return await handle_chat(chat_data)


app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def root():
    return FileResponse("app/static/landing.html")


@app.exception_handler(404)
async def not_found(request: Request, exc):
    return FileResponse("app/static/index.html")

@app.get("/login")
async def login():
    return FileResponse("app/static/login.html")


@app.get("/chat")
async def chat_page():
    return FileResponse("app/static/index.html")
