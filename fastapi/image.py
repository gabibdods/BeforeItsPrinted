from PIL import Image
import pytesseract
from .models import ParsedExam, ExamSection, Question

def parse_image(path: str) -> ParsedExam:
    text = pytesseract.image_to_string(Image.open(path))
    questions = [
        Question(question_text = line.strip(), type = "short_answer")
        for line in text.slip('\n') if '?' in line
    ]
    return ParsedExam(
        title = "Short Answers Image Exam",
        sections = [ExamSection(type = "short_answer", questions = questions)]
    )