from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class Question(BaseModel):
    question_text: str
    options: Optional[List[str]] = None
    answer: Optional[str] = None
    difficulty: Optional = None
    topic: Optional[str] = None
    type: str

    model_config = ConfigDict(arbitrary_types_allowed = True)

class ExamSection(BaseModel):
    type: str
    questions: List[Question]

class ParsedExam(BaseModel):
    title: str
    sections: List[ExamSection]