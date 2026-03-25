from pydantic import BaseModel, Field


class EvaluationOutput(BaseModel):
    is_correct: bool = Field(
        ..., description="Indica se a resposta demonstra compreensão adequada do conceito ensinado."
    )
    justification: str = Field(
        ..., description="Justificativa para a avaliação, explicando acertos ou lacunas. Tom formativo, máximo de 2 frases."
    )
