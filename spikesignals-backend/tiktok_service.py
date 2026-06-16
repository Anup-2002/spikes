import requests
import os

ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN")

def upload_video(video_url, title):

    if not ACCESS_TOKEN:
        return {
            "status": "error",
            "message": "TIKTOK_ACCESS_TOKEN missing"
        }

    url = "https://open.tiktokapis.com/v2/post/publish/video/init/"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "post_info": {
            "title": title,
            "privacy_level": "PUBLIC_TO_EVERYONE"
        },

        "source_info": {
            "source": "PULL_FROM_URL",
            "video_url": video_url
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload
    )

    return response.json()