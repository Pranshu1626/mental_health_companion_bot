import random

def get_recommendations(emotion):
    videos = VIDEO_RECS.get(emotion, [])
    images = IMAGE_RECS.get(emotion, [])

    video = random.choice(videos) if videos else None
    image = random.choice(images) if images else None

    return video, image

#Still woring on this

VIDEO_RECS = {
    "anxiety": [
        {
            "title": "5 Minute Breathing Exercise",
            "url": "https://www.youtube.com/watch?v=odADwWzHR24"
        },
        {
            "title": "Stop Overthinking",
            "url": "https://www.youtube.com/watch?v=ZToicYcHIOU"
        }
    ],
    "sadness": [
        {
            "title": "When You Feel Lonely",
            "url": "https://www.youtube.com/watch?v=k7X7sZzSXYs"
        }
    ],
    "joy": [
        {
            "title": "Celebrate Small Wins",
            "url": "https://www.youtube.com/watch?v=0yq5d1s0sG4"
        }
    ]
}

IMAGE_RECS = {
    "anxiety": [
        "https://images.unsplash.com/photo-1506126613408-eca07ce68773",
        "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee"
    ],
    "sadness": [
        "https://images.unsplash.com/photo-1494790108377-be9c29b29330"
    ]
}