import cv2
import base64
from langchain_core.messages import HumanMessage
from .rate_limiter import RateLimiter

rate_limiter = RateLimiter(rpm=10)  # 👈 YOUR LIMIT
 # free tier safe


def encode_frame(frame):
    _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
    return base64.b64encode(buf).decode()

def verify_change_with_llm(llm, segment, previous_context=None):
    
    before_b64 = encode_frame(segment["before"])
    after_b64 = encode_frame(segment["after"])

    prompt = f"""
You are analyzing a UI automation video.

Two images are shown:
- BEFORE a UI change
- AFTER a UI change

Time: {segment['start']:.2f}s → {segment['end']:.2f}s
Change ratio: {segment['change_ratio']:.3f}

Previous context:
{previous_context or "None"}

Task:
1. Describe what changed.
2. Identify the user action (click, typing, navigation, etc.) if visible.
3. Be concise (1–2 sentences).
"""

    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{before_b64}"}},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{after_b64}"}}
        ]
    )

    rate_limiter.wait()
    return llm.invoke([message]).content
