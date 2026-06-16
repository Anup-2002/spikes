import requests
import os

ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN")


def upload_video(video_url, title):

    if not ACCESS_TOKEN:
        return {
            "status": "error",
            "message": "TIKTOK_ACCESS_TOKEN missing"
        }

    if not video_url:
        return {
            "status": "error",
            "message": "Video URL is required"
        }

    if not title:
        return {
            "status": "error",
            "message": "Title is required"
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

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )
        if response.status_code not in [200, 201]:
            return {
                "status": "error",
                "message": response.text
            }
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
