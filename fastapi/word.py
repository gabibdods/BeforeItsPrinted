import docx
from .models import ParsedExam, ExamSection, Question

def parse_docx(path: str) -> ParsedExam:
    doc = docx.Document(path)
    questions = [
        Question(question_text = para.text.strip(), type = "short_answer")
        for para in doc.paragraphs if '?' in para.text
    ]
    return ParsedExam(
        title = "Short Answers Word Exam",
        sections = [ExamSection(type = "short_answer", questions = questions)]
    )