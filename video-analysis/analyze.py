from tools.change_detector import detect_change_segments
from tools.change_verifier import verify_change_with_llm
from langchain_google_genai import ChatGoogleGenerativeAI

GOOGLE_API_KEY = "AIzaSyCLL5au3Yyd-2004GL8Av7Bsc64hFf34uA"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=GOOGLE_API_KEY
)

segments = detect_change_segments(
    video_path="data/video.webm",
    fps=2,
    change_threshold=0.05
)

events = []
prev_context = None

for seg in segments:
    obs = verify_change_with_llm(llm, seg, prev_context)
    prev_context = obs

    events.append({
        "start": round(seg["start"], 2),
        "end": round(seg["end"], 2),
        "change_ratio": round(seg["change_ratio"], 3),
        "observation": obs
    })

for e in events:
    print(f"[{e['start']}s → {e['end']}s] {e['observation']}")
