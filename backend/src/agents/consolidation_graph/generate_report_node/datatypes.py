from pydantic import BaseModel, Field


class GenerateReportOutput(BaseModel):
    recommendations: str = Field(
        ..., description="Relatório final em Markdown com diagnóstico, recomendação de revisão ancorada no material da aula e score."
    )
