from urllib import response
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",)

MODEL = "llama-3.3-70b-versatile"

def generate_llm_reply(message: str, emotion: str) -> str:
    prompt = f"""
You are a supportive close friend.

User message: {message}
Detected emotion: {emotion}

Rules:
- Be warm and human
- Validate feelings first
- Keep replies short (1–3 sentences)
- Do not sound like a therapist
- Do not give heavy advice immediately
- Ask gentle follow-up sometimes
- Use revelent emojis to express empathy and understanding
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
#     # Handle provider/API errors
#     if response.error:
#         print("OpenRouter Error:", response.error)
#         return (
#             "I'm having a little trouble reaching the AI service right now. "
#             "Please try again in a few moments."
#         )

# # Handle unexpected empty responses
#     if not response.choices:
#         print("No choices returned:", response)
#         return (
#             "Sorry, I couldn't generate a response this time. "
#             "Please try again."
#         )
    # print(response)
    # print(response.model_dump())
     
    return response.choices[0].message.content