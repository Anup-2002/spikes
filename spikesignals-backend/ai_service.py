import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_hashtags(transcript):

    prompt = f"""
    Analyze this video transcript.

    Generate:
    1. A short social media caption
    2. 15 relevant hashtags

    Transcript:
    {transcript}
    """

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    return response.output_text