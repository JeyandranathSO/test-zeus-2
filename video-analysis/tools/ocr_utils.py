import cv2
import pytesseract

def extract_text(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return " ".join(text.split())
