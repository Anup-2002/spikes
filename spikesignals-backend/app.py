from fastapi import FastAPI, UploadFile, File
from video_editor import add_logo
from pydantic import BaseModel
from email_service import send_email
from ai_service import generate_hashtags
from pydantic import BaseModel
from youtube_service import upload_video, get_trending_videos
from pydantic import BaseModel
import os

app = FastAPI()

os.makedirs("uploads", exist_ok=True)
os.makedirs("output", exist_ok=True)

@app.get("/")
def home():
    return {"message": "SpikeSignals Backend Running"}

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

    send_email(
        data.receiver,
        data.subject,
        data.body
    )

    return {
        "status": "success",
        "message": "Email sent"
    }
class TranscriptRequest(BaseModel):
    transcript: str
@app.post("/generate-caption")
def generate_caption(data: TranscriptRequest):

    result = generate_hashtags(
        data.transcript
    )

    return {
        "status": "success",
        "result": result
    }
class YouTubeUpload(BaseModel):
    video_path: str
    title: str
    description: str
@app.post("/upload-youtube")
def upload_to_youtube(data: YouTubeUpload):

    video_id = upload_video(
        data.video_path,
        data.title,
        data.description
    )

    return {
        "status": "success",
        "video_id": video_id,
        "youtube_url": f"https://youtu.be/{video_id}"
    }
@app.get("/trending-videos")
def trending_videos():

    videos = get_trending_videos()

    return {
        "status": "success",
        "videos": videos
    }