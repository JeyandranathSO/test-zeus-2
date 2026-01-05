def seconds_to_mmss(seconds: float) -> str:
    minutes = int(seconds // 60)
    sec = seconds % 60
    return f"{minutes:02d}:{sec:05.2f}"
