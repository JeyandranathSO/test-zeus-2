import cv2
import json
from pathlib import Path
from .video_loader import normalize_video
from .frame_diff import compute_frame_diff

def detect_change_segments(
    video_path,
    fps=2,
    change_threshold=0.05
):
    video_path = normalize_video(video_path)
    cap = cv2.VideoCapture(video_path)

    native_fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    step = max(native_fps // fps, 1)

    segments = []
    prev_frame = None
    prev_ts = None
    frame_id = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id % step == 0:
            ts = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000

            if prev_frame is not None:
                ratio, _, _ = compute_frame_diff(prev_frame, frame)

                if ratio > change_threshold:
                    segments.append({
                        "start": prev_ts,
                        "end": ts,
                        "before": prev_frame.copy(),
                        "after": frame.copy(),
                        "change_ratio": ratio
                    })

            prev_frame = frame.copy()
            prev_ts = ts

        frame_id += 1

    cap.release()
    return segments
