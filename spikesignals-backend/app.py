from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import os

from video_editor import add_logo
from email_service import send_email
from ai_service import generate_hashtags

from instagram_service import publish_video

from youtube_service import (
    upload_video as youtube_upload_video,
    get_trending_videos
)

from tiktok_service import (
    upload_video as tiktok_upload_video
)

app = FastAPI()

os.makedirs("uploads", exist_ok=True)
os.makedirs("output", exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "SpikeSignals Backend Running"
    }


@app.post("/process-video")
async def process_video(file: UploadFile = File(...)):

    input_path = f"uploads/{file.filename}"

    with open(input_path, "wb") as f:
        f.write(await file.read())

    output_path = f"output/edited_{file.filename}"

    add_logo(
        input_path,
        "logos/logo.png",
        output_path
    )

    return {
        "status": "success",
        "output_file": output_path
    }


class EmailRequest(BaseModel):
    receiver: str
    subject: str
    body: str


@app.post("/send-email")
def send_email_api(data: EmailRequest):

    try:

        send_email(
            data.receiver,
            data.subject,
            data.body
        )

        return {
            "status": "success",
            "message": "Email sent"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


class TranscriptRequest(BaseModel):
    transcript: str


@app.post("/generate-caption")
def generate_caption(data: TranscriptRequest):

    try:

        result = generate_hashtags(
            data.transcript
        )

        return {
            "status": "success",
            "result": result
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


class YouTubeUpload(BaseModel):
    video_path: str
    title: str
    description: str


@app.post("/upload-youtube")
def upload_to_youtube(data: YouTubeUpload):

    try:

        video_id = youtube_upload_video(
            data.video_path,
            data.title,
            data.description
        )

        return {
            "status": "success",
            "video_id": video_id,
            "youtube_url": f"https://youtu.be/{video_id}"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/trending-videos")
def trending_videos():

    try:

        videos = get_trending_videos()

        return {
            "status": "success",
            "videos": videos
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


class InstagramRequest(BaseModel):
    video_url: str
    caption: str


@app.post("/publish-instagram")
def publish_instagram(data: InstagramRequest):

    try:

        result = publish_video(
            data.video_url,
            data.caption
        )

        return result

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


class TikTokRequest(BaseModel):
    video_url: str
    title: str


@app.post("/publish-tiktok")
def publish_tiktok(data: TikTokRequest):

    try:

        result = tiktok_upload_video(
            data.video_url,
            data.title
        )

        return result

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


class PublishRequest(BaseModel):
    video_path: str
    title: str
    description: str
    caption: str


@app.post("/publish-all")
def publish_all(data: PublishRequest):

    try:

        edited_video = (
            f"output/edited_{os.path.basename(data.video_path)}"
        )

        add_logo(
            data.video_path,
            "logos/logo.png",
            edited_video
        )

        try:

            youtube_id = youtube_upload_video(
                edited_video,
                data.title,
                data.description
            )

            youtube_result = {
                "status": "success",
                "video_id": youtube_id,
                "url": f"https://youtu.be/{youtube_id}"
            }

        except Exception as e:

            youtube_result = {
                "status": "error",
                "message": str(e)
            }

        instagram_result = {
            "status": "not_executed",
            "message": "Requires public video URL and Instagram credentials"
        }

        tiktok_result = {
            "status": "not_executed",
            "message": "Requires public video URL and TikTok credentials"
        }

        return {
            "status": "success",
            "edited_video": edited_video,
            "youtube": youtube_result,
            "instagram": instagram_result,
            "tiktok": tiktok_result
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }