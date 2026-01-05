from utils.time_utils import seconds_to_mmss

def align_plans(agent_steps, ocr_results):
    for step in agent_steps:
        closest = min(
            ocr_results,
            key=lambda x: abs(x["timestamp_sec"] - step["timestamp_sec"])
        )
        step["aligned_frame_id"] = closest["frame_id"]
        step["aligned_timestamp"] = seconds_to_mmss(
            closest["timestamp_sec"]
        )
    return agent_steps
