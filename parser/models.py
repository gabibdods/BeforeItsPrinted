from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class SubQuestion(BaseModel):
    id: str
    text: str
    type: str = "open_answer"
    options: Optional[List[str]] = None
    answer: Optional[str] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

class Question(BaseModel):
    id: str
    text: str
    type: str = "open_answer"
    options: Optional[List[str]] = None
    answer: Optional[str] = None
    subquestions: Optional[List[SubQuestion]] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

class ParsedExam(BaseModel):
    title: str
    questions: List[Question]
    model_config = ConfigDict(arbitrary_types_allowed=True)