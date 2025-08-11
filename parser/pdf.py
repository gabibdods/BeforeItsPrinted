import pdfplumber
from core import parse_questions

def parse_pdf(path: str):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return parse_questions(text)