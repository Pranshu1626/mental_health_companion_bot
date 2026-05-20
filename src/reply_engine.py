import os
from src.llm_service import generate_llm_reply

def generate_final_reply(message, emotion):
    return generate_llm_reply(message, emotion)