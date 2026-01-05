import subprocess
import shutil
from pathlib import Path
import cv2

def normalize_video(video_path: str) -> str:
    path = Path(video_path)

    # If already MP4, return as-is
    if path.suffix.lower() == ".mp4":
        return str(path)

    # Check if OpenCV can read the file directly
    cap = cv2.VideoCapture(str(path))
    if cap.isOpened():
        ret, _ = cap.read()
        cap.release()
        if ret:
            # OpenCV can read it, no need to normalize
            return str(path)

    # If normalization is needed, check if ffmpeg is available
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path is None:
        raise FileNotFoundError(
            "ffmpeg is not installed or not in PATH. "
            "Please install ffmpeg from https://ffmpeg.org/download.html "
            "or add it to your system PATH. "
            "Alternatively, ensure your video file can be read by OpenCV."
        )

    out = path.with_suffix(".normalized.mp4")
    if out.exists():
        return str(out)

    subprocess.run(
        [
            ffmpeg_path, "-y",
            "-i", str(path),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            str(out)
        ],
        check=True
    )

    return str(out)
