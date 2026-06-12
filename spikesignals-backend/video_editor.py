import subprocess

def add_logo(video_path, logo_path, output_path):

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

    subprocess.run(cmd)

    return output_path