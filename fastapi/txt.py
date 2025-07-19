from .models import ParsedExam, ExamSection, Question

def parse_txt(path: str) -> ParsedExam:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    questions = [
        Question(question_text = line.strip('\n'), type = "short_answer")
        for line in text.split('\n') if '?' in line
    ]
    return ParsedExam(
        title = "Short Answers Text Exam",
        sections = [ExamSection(type = "short_answer", questions = questions)]
    )