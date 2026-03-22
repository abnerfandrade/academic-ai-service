from pydantic import BaseModel, Field


class EvaluationOutput(BaseModel):
    is_correct: bool = Field(
        ..., description="Indica se a resposta do aluno está correta ou demonstra conhecimento suficiente do conceito."
    )
    justification: str = Field(
        ..., description="Justificativa para a avaliação da resposta do aluno."
    )
