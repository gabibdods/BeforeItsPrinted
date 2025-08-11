import pytesseract
from PIL import Image
from core import parse_questions

def parse_image(path: str):
    img = Image.open(path)
    text = pytesseract.image_to_string(img)
    return parse_questions(text)
