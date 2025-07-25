import re
from models import SubQuestion, Question

def parse_questions(text: str):
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

    answer_key_map = {}

    def flush_main_question():
        nonlocal questions, current_question_id, current_question_text, current_question_options, current_question_answer, subquestions
        if isinstance(current_question_id, str) and current_question_text:
            question_type = "multiple_choice" if current_question_options else "open_answer"
            questions.append(Question(
                id=current_question_id,
                text="\n".join(current_question_text).strip(),
                type=question_type,
                options=current_question_options if current_question_options else None,
                answer=current_question_answer or answer_key_map.get(current_question_id),
                subquestions=subquestions if subquestions else None
            ))
        current_question_id = None
        current_question_text = []
        current_question_options = []
        current_question_answer = None
        subquestions = []

    def flush_subquestion():
        nonlocal subquestions, current_sub_id, current_sub_text, current_sub_options, current_sub_answer
        if isinstance(current_sub_id, str) and current_sub_text:
            sub_type = "multiple_choice" if current_sub_options else "open_answer"
            subquestions.append(SubQuestion(
                id=current_sub_id,
                text="\n".join(current_sub_text).strip(),
                type=sub_type,
                options=current_sub_options if current_sub_options else None,
                answer=current_sub_answer,
            ))
        current_sub_id = None
        current_sub_text = []
        current_sub_options = []
        current_sub_answer = None

    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        line = line.replace('–', '-').replace('—', '-').replace('：', ':') \
                   .replace('“', '"').replace('”', '"').replace("’", "'")

        p_match = re.match(r"^(P\d+)[\s:：\-]*([\s\S]*)$", line, re.IGNORECASE)
        n_match = re.match(r"^(\d+)\s*[\.\-:\)\]]\s*([\s\S]*)$", line)
        q_match = re.match(r"^question\s+(\d+)[\.\)\-:]?\s*([\s\S]*)$", line, re.IGNORECASE)
        sub_match = re.match(r"^([a-z])[\)\.\-:\]]\s*([\s\S]*)$", line, re.IGNORECASE)
        option_match = re.match(r"^\*?\s*([a-hA-H])[\)\.\:\-]\s*([\s\S]*)$", line)
        answer_match = re.match(r"(?i)^correct\s+answer\s*[:\-]?\s*([a-hA-H])", line)
        answer_key_line = re.match(r"^(\d+)\s*[\.\-:\)\]]\s*([a-hA-H])\s*$", line)

        if option_match:
            label, option_text = option_match.groups()
            formatted_option = f"{label.upper()}) {option_text}"
            if current_sub_id:
                current_sub_options.append(formatted_option)
                if line.lstrip().startswith("*"):
                    current_sub_answer = label.upper()
            elif current_question_id:
                current_question_options.append(formatted_option)
                if line.lstrip().startswith("*"):
                    current_question_answer = label.upper()
        elif answer_match:
            answer_label = answer_match.group(1).upper()
            if current_sub_id:
                current_sub_answer = answer_label
            elif current_question_id:
                current_question_answer = answer_label
        elif answer_key_line:
            qnum, ans = answer_key_line.groups()
            answer_key_map[f"Q{qnum}"] = ans.upper()
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
            current_sub_id = f"{current_question_id}{sub_match.group(1).lower()}"
            current_sub_text = [sub_match.group(2)]
        else:
            if current_sub_id:
                current_sub_text.append(line)
            elif current_question_id:
                current_question_text.append(line)

    flush_subquestion()
    flush_main_question()

    return questions

