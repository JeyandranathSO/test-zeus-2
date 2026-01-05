# Video Analysis Agent

This project analyzes an autonomous agent by aligning its internal planning
steps with UI interactions observed in a video recording.

## Features
- Frame-difference-based video processing
- OCR with confidence filtering
- Planning step alignment
- Gemini LLM-based analysis
- Full traceability with frame IDs and thumbnails

## Run
```bash
pip install -r requirements.txt
python src/main.py
