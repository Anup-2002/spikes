import os
import subprocess
def add_logo(video_path, logo_path, output_path):

    if not os.path.exists(video_path):
        raise FileNotFoundError(
            f"Video file not found: {video_path}"
        )

    if not os.path.exists(logo_path):
        raise FileNotFoundError(
            f"Logo file not found: {logo_path}"
        )

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-i",
        logo_path,
        "-filter_complex",
        "overlay=10:10",
        output_path
    ]

    try:

        subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )

        return output_path

    except subprocess.CalledProcessError as e:

        raise Exception(
            f"FFmpeg processing failed: {e.stderr}"
        )
