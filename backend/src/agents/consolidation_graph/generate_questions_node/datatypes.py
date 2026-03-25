from pydantic import BaseModel, Field


class QuestionItem(BaseModel):
    question: str = Field(..., description="A pergunta elaborada para o aluno")
    concept_tag: str = Field(..., description="Tag referente ao objetivo de aprendizado testado por esta pergunta")


class QuestionsOutput(BaseModel):
    questions: list[QuestionItem] = Field(..., description="Lista de perguntas geradas")
