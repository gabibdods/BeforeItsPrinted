from pydantic import BaseModel, ConfigDict

class Question(BaseModel):
    question_text: str
    options: list[str] | None = None
    answer: str | None = None
    difficulty: str | None = None
    topic: str | None = None
    type: str

    model_config = ConfigDict(arbitrary_types_allowed=True)

class ExamSection(BaseModel):
    type: str
    questions: list[Question]

class ParsedExam(BaseModel):
    title: str
    sections: list[ExamSection]