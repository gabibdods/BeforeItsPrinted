from docx import Document
from core import parse_questions

def parse_docx(path: str):
    doc = Document(path)
    text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    return parse_questions(text)