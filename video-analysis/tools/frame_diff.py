import cv2
import numpy as np

def compute_frame_diff(before, after, pixel_thresh=30):
    """
    Returns:
    - change_ratio (0–1)
    - binary diff mask
    - heatmap image
    """
    gray1 = cv2.cvtColor(before, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(after, cv2.COLOR_BGR2GRAY)

    diff = cv2.absdiff(gray1, gray2)
    mask = diff > pixel_thresh

    change_ratio = mask.sum() / mask.size

    heatmap = cv2.applyColorMap(
        cv2.normalize(diff, None, 0, 255, cv2.NORM_MINMAX),
        cv2.COLORMAP_JET
    )

    return change_ratio, mask.astype("uint8") * 255, heatmap
