import json
from pathlib import Path

def load_agent_steps(path):
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Agent log not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        logs = json.load(f)

    steps = []

    # CASE 1: logs is a list
    if isinstance(logs, list):
        for idx, entry in enumerate(logs):

            # 1a: list of dicts
            if isinstance(entry, dict):
                msg = entry.get("message") or entry.get("content") or ""
                ts = entry.get("timestamp_sec") or entry.get("timestamp") or idx

                if "plan" in json.dumps(entry).lower():
                    steps.append({
                        "timestamp_sec": float(ts),
                        "content": msg
                    })

            # 1b: list of strings
            elif isinstance(entry, str):
                if "plan" in entry.lower():
                    steps.append({
                        "timestamp_sec": float(idx),
                        "content": entry
                    })

    # CASE 2: logs is a dict
    elif isinstance(logs, dict):
        for key, value in logs.items():

            # dict of dicts
            if isinstance(value, dict):
                msg = value.get("message") or value.get("content") or ""
                ts = value.get("timestamp_sec") or key

                if "plan" in json.dumps(value).lower():
                    steps.append({
                        "timestamp_sec": float(ts),
                        "content": msg
                    })

            # dict of strings
            elif isinstance(value, str):
                if "plan" in value.lower():
                    steps.append({
                        "timestamp_sec": float(key) if str(key).isdigit() else 0.0,
                        "content": value
                    })

    if not steps:
        raise ValueError(
            "No planning steps detected in agent logs. "
            "Check log format or 'plan' keyword."
        )

    return steps
