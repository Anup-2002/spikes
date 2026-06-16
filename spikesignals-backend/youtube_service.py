import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload"
]


def get_youtube_service():

    creds = None

    if not os.path.exists("client_secret.json"):
        raise FileNotFoundError(
            "client_secret.json not found"
        )

    if os.path.exists("token.pickle"):

        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds:

        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json",
            SCOPES
        )

        creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build(
        "youtube",
        "v3",
        credentials=creds
    )


def upload_video(
    video_path,
    title,
    description
):

    if not os.path.exists(video_path):
        raise FileNotFoundError(
            f"Video file not found: {video_path}"
        )

    if not title:
        raise ValueError(
            "Video title is required"
        )

    youtube = get_youtube_service()

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "private"
            }
        },
        media_body=MediaFileUpload(video_path)
    )

    try:

        response = request.execute()

        return response["id"]

    except Exception as e:

        raise Exception(
            f"YouTube upload failed: {str(e)}"
        )


def get_trending_videos():

    youtube = get_youtube_service()

    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode="IN",
        maxResults=10
    )

    try:

        response = request.execute()

        videos = []

        for item in response["items"]:

            videos.append({
                "videoId": item["id"],
                "title": item["snippet"]["title"],
                "channel": item["snippet"]["channelTitle"],
                "thumbnail": item["snippet"]["thumbnails"]["high"]["url"],
                "views": item["statistics"].get(
                    "viewCount",
                    "0"
                )
            })

        return videos

    except Exception as e:

        raise Exception(
            f"Failed to fetch trending videos: {str(e)}"
        )
