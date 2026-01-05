def diff_text(prev, curr):
    prev_words = set(prev.lower().split())
    curr_words = set(curr.lower().split())

    return {
        "added": list(curr_words - prev_words),
        "removed": list(prev_words - curr_words)
    }

def build_text_change_log(timeline):
    changes = []

    for i in range(1, len(timeline)):
        diff = diff_text(
            timeline[i-1]["text"],
            timeline[i]["text"]
        )

        if diff["added"] or diff["removed"]:
            changes.append({
                "time": timeline[i]["time"],
                "added": diff["added"],
                "removed": diff["removed"]
            })

    return changes
