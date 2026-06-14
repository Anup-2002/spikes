import requests
import os

ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN")

def upload_video(video_path, title):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    payload = {
        "post_info": {
            "title": title
        }
    }

    return {
        "status": "ready_for_tiktok_upload",
        "title": title
    }