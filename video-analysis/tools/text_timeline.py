import cv2
from .ocr_utils import extract_text
from .video_loader import normalize_video

def build_text_timeline(video_path, fps=2):
    video_path = normalize_video(video_path)
    cap = cv2.VideoCapture(video_path)

    native_fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    step = max(native_fps // fps, 1)

    timeline = []
    frame_id = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id % step == 0:
            timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            text = extract_text(frame)

            timeline.append({
                "time": round(timestamp, 2),
                "text": text
            })

        frame_id += 1

    cap.release()
    return timeline
