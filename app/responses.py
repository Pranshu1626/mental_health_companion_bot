import random

human_responses = {
    "sadness": [
        "I'm really sorry you're feeling this way. You don't have to go through it alone.",
        "That sounds heavy… I'm here with you. Do you want to talk about it?",
        "It makes sense to feel like this sometimes. I'm listening."
    ],
    "anxiety": [
        "That sounds overwhelming. Let's slow down together.",
        "I can hear the stress in that. You're safe to talk here.",
        "Anxiety can feel loud. We can take this one step at a time."
    ],
    "anger": [
        "That sounds really frustrating.",
        "I get why you'd feel angry about that.",
        "It's okay to feel angry. Want to tell me what happened?"
    ],
    "joy": [
        "That makes me smile 🙂",
        "I'm really happy for you.",
        "That sounds like a good moment."
    ],
    "neutral": [
        "I'm here with you.",
        "Tell me more.",
        "I'm listening."
    ]
}

def generate_reply(emotion, user_text):
    base = random.choice(human_responses.get(emotion, human_responses["neutral"]))

    return base