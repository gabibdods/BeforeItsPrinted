from core import parse_questions

def parse_txt(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return parse_questions(text)