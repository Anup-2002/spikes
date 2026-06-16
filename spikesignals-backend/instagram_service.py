import requests
import os

ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
IG_USER_ID = os.getenv("INSTAGRAM_USER_ID")

def publish_video(video_url, caption):

    if not ACCESS_TOKEN:
        return {
            "status": "error",
            "message": "INSTAGRAM_ACCESS_TOKEN missing"
        }

    if not IG_USER_ID:
        return {
            "status": "error",
            "message": "INSTAGRAM_USER_ID missing"
        }

    create_url = f"https://graph.facebook.com/v23.0/{IG_USER_ID}/media"

    payload = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "access_token": ACCESS_TOKEN
    }

    response = requests.post(
        create_url,
        data=payload
    )

    return response.json()