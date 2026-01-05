import cv2
import numpy as np
import os

def extract_key_frames(video_path, diff_threshold, thumb_dir):
    os.makedirs(thumb_dir, exist_ok=True)

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        raise ValueError(f"Failed to open video file: {video_path}")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    if fps <= 0:
        raise ValueError(f"Invalid FPS detected: {fps}. Video may be corrupted.")

    prev_gray = None
    frame_idx = 0
    frame_id = 0
    frames = []
    first_frame_added = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Always add the first frame
        if prev_gray is None:
            timestamp = frame_idx / fps
            thumb_path = f"{thumb_dir}/frame_{frame_id}.jpg"
            cv2.imwrite(thumb_path, frame)

            frames.append({
                "frame_id": frame_id,
                "frame": frame,
                "timestamp_sec": timestamp,
                "thumbnail": thumb_path
            })
            frame_id += 1
            first_frame_added = True
        else:
            diff = cv2.absdiff(prev_gray, gray)
            score = np.mean(diff)

            if score > diff_threshold:
                timestamp = frame_idx / fps
                thumb_path = f"{thumb_dir}/frame_{frame_id}.jpg"
                cv2.imwrite(thumb_path, frame)

                frames.append({
                    "frame_id": frame_id,
                    "frame": frame,
                    "timestamp_sec": timestamp,
                    "thumbnail": thumb_path
                })
                frame_id += 1

        prev_gray = gray
        frame_idx += 1

    cap.release()
    return frames
