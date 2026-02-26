import os
from app.responses import generate_reply

LLM_ENABLED = os.getenv("OPENROUTER_API_KEY") is not None


if LLM_ENABLED:
    try:
        from src.llm_service import generate_llm_reply
    except:
        LLM_ENABLED = False

print("Using LLM:", LLM_ENABLED)
def generate_final_reply(message, emotion):

    if LLM_ENABLED:
        try:
            return generate_llm_reply(message, emotion)
        except:
            return generate_reply(emotion, message)

    return generate_reply(emotion, message)