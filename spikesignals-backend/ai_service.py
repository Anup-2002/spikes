import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=api_key)


def generate_hashtags(transcript):

    if not transcript.strip():
        raise ValueError("Transcript cannot be empty")

    prompt = f"""
    Analyze the following video transcript.

    Generate:
    1. A short engaging social media caption.
    2. Exactly 15 relevant hashtags.

    Transcript:
    {transcript}
    """

    try:

        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        return response.output_text

    except Exception as e:

        raise Exception(
            f"OpenAI API Error: {str(e)}"
        )
