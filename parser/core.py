import re
from models import SubQuestion, Question
from typing import List, Optional, Dict

_INTERROGATIVE_OR_TASK_START = re.compile(
    r"^(what|why|where|how|who|when|which|explain|describe|write|compute|prove|show|justify|derive|define|list|state|compare|evaluate|discuss)\b",
    re.IGNORECASE,
)

def _ends_sentence(s: str) -> bool:
    s = s.rstrip()
    return s.endswith(".") or s.endswith("?")

def _is_bullet_like(s: str) -> bool:
    return bool(re.match(r"^(\-|\*|•|—)\s+\S", s))

def _word_count(s: str) -> int:
    return len(s.strip().split())

def _looks_like_unlabeled_option(s: str) -> bool:
    if not s.strip():
        return False
    if _INTERROGATIVE_OR_TASK_START.match(s):
        return False
    if s.strip().endswith("?"):
        return False
    if re.match(r"^([A-Ha-h]|[1-9])[\)\.\:\-]\s+\S", s):
        return False
    return _word_count(s) <= 12 or _is_bullet_like(s)

def _looks_like_unlabeled_subquestion(s: str) -> bool:
    return s.strip().endswith("?") or bool(_INTERROGATIVE_OR_TASK_START.match(s))

def parse_questions(text: str):
    questions: List[Question] = []

    current_question_id: Optional[str] = None
    current_question_text: List[str] = []
    current_question_options: List[str] = []
    current_question_answer: Optional[str] = None
    question_text_ended: bool = False

    subquestions: List[SubQuestion] = []
    current_sub_id: Optional[str] = None
    current_sub_text: List[str] = []
    current_sub_options: List[str] = []
    current_sub_answer: Optional[str] = None
    sub_text_ended: bool = False

    next_sub_letter_ord: int = ord("a")

    answer_key_map: Dict[str, str] = {}

    def flush_main_question():
        nonlocal questions, current_question_id, current_question_text, current_question_options
        nonlocal current_question_answer, subquestions, question_text_ended, next_sub_letter_ord
        if isinstance(current_question_id, str) and (current_question_text or subquestions):
            qtype = "multiple_choice" if current_question_options else "open_answer"
            questions.append(
                Question(
                    id=current_question_id,
                    text="\n".join(current_question_text).strip(),
                    type=qtype,
                    options=current_question_options if current_question_options else None,
                    answer=current_question_answer or answer_key_map.get(current_question_id),
                    subquestions=subquestions if subquestions else None,
                )
            )
        current_question_id = None
        current_question_text = []
        current_question_options = []
        current_question_answer = None
        subquestions = []
        question_text_ended = False
        next_sub_letter_ord = ord("a")

    def flush_subquestion():
        nonlocal subquestions, current_sub_id, current_sub_text, current_sub_options, current_sub_answer, sub_text_ended
        if isinstance(current_sub_id, str) and current_sub_text:
            stype = "multiple_choice" if current_sub_options else "open_answer"
            subquestions.append(
                SubQuestion(
                    id=current_sub_id,
                    text="\n".join(current_sub_text).strip(),
                    type=stype,
                    options=current_sub_options if current_sub_options else None,
                    answer=current_sub_answer,
                )
            )
        current_sub_id = None
        current_sub_text = []
        current_sub_options = []
        current_sub_answer = None
        sub_text_ended = False

    lines = text.split("\n")
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        line = (
            line.replace("–", "-")
            .replace("—", "-")
            .replace("：", ":")
            .replace("“", '"')
            .replace("”", '"')
            .replace("’", "'")
        )
        p_match = re.match(r"^(P\d+)[\s:：\-]*([\s\S]*)$", line, re.IGNORECASE)
        n_match = re.match(r"^(\d+)\s*[\.\-:\)\]]\s*([\s\S]*)$", line)
        q_match = re.match(r"^question\s+(\d+)[\.\)\-:]?\s*([\s\S]*)$", line, re.IGNORECASE)
        sub_match = re.match(r"^([a-h])[\)\.\-:\]]\s*([\s\S]*)$", line, re.IGNORECASE)
        option_match = re.match(r"^\*?\s*([a-hA-H]|[1-9])[\)\.\:\-]\s*([\s\S]+)$", line)
        answer_match = re.match(r"(?i)^correct\s+answer\s*[:\-]?\s*([a-hA-H])", line)
        answer_key_line = re.match(r"^(\d+)\s*[\.\-:\)\]]\s*([a-hA-H])\s*$", line)
        if option_match and (current_question_id or current_sub_id):
            label, option_text = option_match.groups()
            formatted = f"{label.upper()}) {option_text.strip()}"
            if current_sub_id:
                current_sub_options.append(formatted)
            else:
                current_question_options.append(formatted)
            continue
        if answer_match:
            answer_label = answer_match.group(1).upper()
            if current_sub_id:
                current_sub_answer = answer_label
            elif current_question_id:
                current_question_answer = answer_label
            continue

        if answer_key_line:
            qnum, ans = answer_key_line.groups()
            answer_key_map[f"Q{qnum}"] = ans.upper()
            continue
        if p_match or n_match or q_match:
            flush_subquestion()
            flush_main_question()
            if p_match:
                current_question_id = p_match.group(1)
                rest = (p_match.group(2) or "").strip()
            elif n_match:
                current_question_id = f"Q{n_match.group(1)}"
                rest = (n_match.group(2) or "").strip()
            else:
                current_question_id = f"Q{q_match.group(1)}"
                rest = (q_match.group(2) or "").strip()
            if rest:
                current_question_text = [rest]
                question_text_ended = _ends_sentence(rest)
            continue
        if sub_match and current_question_id:
            flush_subquestion()
            current_sub_id = f"{current_question_id}{sub_match.group(1).lower()}"
            first = (sub_match.group(2) or "").strip()
            current_sub_text = [first] if first else []
            sub_text_ended = _ends_sentence(first)
            continue
        if current_question_id and not current_sub_id and _looks_like_unlabeled_subquestion(line):
            flush_subquestion()
            current_sub_id = f"{current_question_id}{chr(next_sub_letter_ord)}"
            next_sub_letter_ord += 1
            current_sub_text = [line]
            sub_text_ended = _ends_sentence(line)
            continue
        if current_sub_id:
            if sub_text_ended and _looks_like_unlabeled_option(line):
                line = re.sub(r"^(\-|\*|•|—)\s+", "", line).strip()
                current_sub_options.append(line)
            else:
                current_sub_text.append(line)
                if _ends_sentence(line):
                    sub_text_ended = True
        elif current_question_id:
            if _looks_like_unlabeled_subquestion(line):
                flush_subquestion()
                current_sub_id = f"{current_question_id}{chr(next_sub_letter_ord)}"
                next_sub_letter_ord += 1
                current_sub_text = [line]
                sub_text_ended = _ends_sentence(line)
            else:
                if question_text_ended and _looks_like_unlabeled_option(line):
                    line = re.sub(r"^(\-|\*|•|—)\s+", "", line).strip()
                    current_question_options.append(line)
                else:
                    current_question_text.append(line)
                    if _ends_sentence(line):
                        question_text_ended = True
        else:
            continue
    flush_subquestion()
    flush_main_question()
    return questions

def to_exam_json(questions: List[Question],
                 topics: List[str],
                 difficulty: str,
                 fmt: List[str],
                 flatten_subquestions: bool = True) -> Dict:
    def _map_q(id_, text, qtype, options):
        return {
            "id": id_,
            "text": text,
            "type": "mcq" if (qtype == "multiple_choice") else "short",
            **({"options": options} if options else {})
        }
    items = []
    for q in questions:
        items.append(_map_q(q.id, q.text, q.type, q.options))
        if q.subquestions:
            if flatten_subquestions:
                for s in q.subquestions:
                    items.append(_map_q(s.id, s.text, s.type, s.options))
            else:
                items[-1]["subquestions"] = [
                    _map_q(s.id, s.text, s.type, s.options) for s in q.subquestions
                ]
    exam = {
        "metadata": {
            "topics": topics,
            "difficulty": difficulty,
            "length": len(items) if flatten_subquestions else len(questions),
            "format": fmt,
        },
        "questions": items if flatten_subquestions else [
            {k: v for k, v in qd.items() if k != "subquestions"} for qd in items
        ]
    }
    return exam

def make_training_record(raw_text: str,
                         controls: Dict[str, object],
                         flatten_subquestions: bool = True) -> Dict[str, str]:
    qs = parse_questions(raw_text)
    topics = list(controls.get("topics", []))
    difficulty = str(controls.get("difficulty", "medium"))
    fmt = list(controls.get("format", ["mcq"]))

    exam = to_exam_json(qs, topics=topics, difficulty=difficulty, fmt=fmt,
                        flatten_subquestions=flatten_subquestions)

    control_str = f"topics={','.join(topics)}; difficulty={difficulty}; length={controls.get('length', exam['metadata']['length'])}; format={'+'.join(fmt)}"

    import json
    return {
        "input": control_str,
        "output": json.dumps(exam, ensure_ascii=False)
    }
