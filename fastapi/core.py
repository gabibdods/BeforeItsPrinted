import pdfplumber
import re
from models import SubQuestion, Question

def parse_questions(path):
    questions = []
    current_question_id = None
    current_question_text = []
    current_question_options = []
    current_question_answer = None

    subquestions = []
    current_sub_id = None
    current_sub_text = []
    current_sub_options = []
    current_sub_answer = None

    def flush_main_question():
        nonlocal questions, current_question_id, current_question_text, current_question_options, current_question_answer, subquestions
        if current_question_id and current_question_text:
            question_type = "multiple_choice" if current_question_options else "open_answer"
            questions.append(Question(
                id = current_question_id,
                text = "\n".join(current_question_text).strip(),
                type = question_type,
                options = current_question_options if current_question_options else None,
                answer = current_question_answer,
                subquestions = subquestions if subquestions else None
            ))
        current_question_id = None
        current_question_text = []
        current_question_options = []
        current_question_answer = None
        subquestions = []

    def flush_subquestion():
        nonlocal subquestions, current_sub_id, current_sub_text, current_sub_options, current_sub_answer
        if current_sub_id and current_sub_text:
            sub_type = "multiple_choice" if current_sub_options else "open_answer"
            subquestions.append(SubQuestion(
                id = current_sub_id,
                text = "\n".join(current_sub_text).strip(),
                type = sub_type,
                options = current_sub_options if current_sub_options else None,
                answer = current_sub_answer,
            ))
        current_sub_id = None
        current_sub_text = []
        current_sub_options = []
        current_sub_answer = None
        subquestions = []

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            lines = text.split('\n')
            for line in lines:
                line = line.strip()

                p_match = re.match(r"^(P\d+)\s*[:：]?\s*(.*)", line)
                n_match = re.match(r"^(\d+)[\-–]\s*(.*)", line)
                q_match = re.match(r"^Question\s+(\d+)\)\s*(.*)", line, re.IGNORECASE)
                sub_match = re.match(r"^([a-zA-Z])\)\s*(.*)", line)
                option_match = re.match(r"^\*?([A-H])[).:\-]\s*(.*)", line)
                answer_match = re.match(r"(?i)^correct answer\s*[:\-]?\s*([A-H])", line)

                if option_match:
                    label, option_text = option_match.groups()
                    formatted_option = f"{label}) {option_text}"
                    if current_sub_id:
                        current_sub_options.append(formatted_option)
                        if line.startswith("*"):
                            current_sub_answer = label
                    elif current_question_id:
                        current_question_options.append(formatted_option)
                        if line.startswith("*"):
                            current_question_answer = label
                elif answer_match:
                    answer_label = answer_match.group(1).upper()
                    if current_sub_id:
                        current_sub_answer = answer_label
                    elif current_question_id:
                        current_question_answer = answer_label
                elif p_match:
                    flush_subquestion()
                    flush_main_question()
                    current_question_id = p_match.group(1)
                    rest = p_match.group(2)
                    current_question_text = [rest] if rest else []
                elif n_match:
                    flush_subquestion()
                    flush_main_question()
                    current_question_id = f"Q{n_match.group(1)}"
                    rest = n_match.group(2)
                    current_question_text = [rest] if rest else []
                elif q_match:
                    flush_subquestion()
                    flush_main_question()
                    current_question_id = f"Q{q_match.group(1)}"
                    rest = q_match.group(2)
                    current_question_text = [rest] if rest else []
                elif sub_match and current_question_id:
                    flush_subquestion()
                    current_sub_id = f"{current_question_id}{sub_match.group(1)}"
                    current_sub_text = [sub_match.group(2)]
                else:
                    if current_sub_id:
                        current_sub_text.append(line)
                    elif current_question_id:
                        current_question_text.append(line)
        flush_subquestion()
        flush_main_question()
    return questions