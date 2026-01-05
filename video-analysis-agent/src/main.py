from pathlib import Path
import yaml
import json
from dotenv import load_dotenv

from video.frame_extractor import extract_key_frames
from ocr.ocr_engine import ocr_frames
from ocr.deduplicate import deduplicate_ocr
from agent.agent_logs import load_agent_steps
from alignment.aligner import align_plans
from llm.gemini_client import run_gemini_analysis

# --------------------------------------------------
# ENV + BASE PATH SETUP
# --------------------------------------------------
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_PATH = BASE_DIR / "config" / "config.yaml"
VIDEO_PATH = BASE_DIR / "data" / "video" / "video.webm"
LOG_PATH = BASE_DIR / "data" / "logs" / "agent_inner_logs.json"
THUMB_DIR = BASE_DIR / "data" / "outputs" / "thumbnails"
OUTPUT_REPORT = BASE_DIR / "data" / "outputs" / "final_report.md"

# --------------------------------------------------
# LOAD CONFIG
# --------------------------------------------------
if not CONFIG_PATH.exists():
    raise FileNotFoundError(f"Config not found: {CONFIG_PATH}")

with open(CONFIG_PATH, "r") as f:
    cfg = yaml.safe_load(f)

# --------------------------------------------------
# PIPELINE
# --------------------------------------------------
if not VIDEO_PATH.exists():
    raise FileNotFoundError(f"Video file not found: {VIDEO_PATH}")

print(f"Processing video: {VIDEO_PATH}")

frames = extract_key_frames(
    video_path=str(VIDEO_PATH),
    diff_threshold=cfg["video"]["diff_threshold"],
    thumb_dir=str(THUMB_DIR)
)
print(f"Extracted {len(frames)} key frames")
ocr_raw = ocr_frames(
    frames,
    confidence_threshold=cfg["ocr"]["confidence_threshold"]
)
print("ocr raw", ocr_raw)

ocr_clean = deduplicate_ocr(
    ocr_raw,
    similarity_threshold=cfg["ocr"]["similarity_threshold"]
)

print("OCR CLEANED", ocr_clean)
# agent_steps = load_agent_steps(LOG_PATH)
# agent_steps = align_plans(agent_steps, ocr_clean)

# # --------------------------------------------------
# # BUILD LLM CONTEXT
# # --------------------------------------------------
# context = "## Agent Planning Steps\n"
# for s in agent_steps:
#     context += (
#         f"- [{s['aligned_timestamp']}] "
#         f"(Frame {s['aligned_frame_id']}): {s['content']}\n"
#     )

# context += "\n## UI Observations (OCR)\n"
# for o in ocr_clean:
#     context += (
#         f"- [{o['timestamp_mmss']}] "
#         f"(Frame {o['frame_id']}, Conf {o['avg_confidence']:.1f}%): "
#         f"{o['text']}\n"
#     )

# # --------------------------------------------------
# # LLM ANALYSIS
# # --------------------------------------------------
# report = run_gemini_analysis(
#     context=context,
#     model=cfg["llm"]["model"],
#     temperature=cfg["llm"]["temperature"]
# )

# OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)

# with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
#     f.write(report)

# print(f"✅ Analysis complete. Report saved to:\n{OUTPUT_REPORT}")
