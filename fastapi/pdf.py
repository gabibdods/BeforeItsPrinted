import pdfplumber
from models import ParsedExam, ExamSection, Question

def parse_pdf(path: str) -> ParsedExam:
    questions = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for line in lines:
                    if '?' in line:
                        questions.append(Question(
                            question_text = line.strip(),
                            type = "short_answer"
                        ))
    return ParsedExam(
        title = "Short Answers PDF Exam",
        sections = [ExamSection(type = "short_answer", questions = questions)]
    )