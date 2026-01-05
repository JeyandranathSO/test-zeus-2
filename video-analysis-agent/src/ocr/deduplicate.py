from difflib import SequenceMatcher

def deduplicate_ocr(results, similarity_threshold):
    unique = []

    for item in results:
        if not any(
            SequenceMatcher(None, item["text"], u["text"]).ratio()
            > similarity_threshold
            for u in unique
        ):
            unique.append(item)

    return unique
