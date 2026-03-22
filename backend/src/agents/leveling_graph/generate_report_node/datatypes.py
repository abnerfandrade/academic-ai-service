from pydantic import BaseModel, Field


class GenerateReportOutput(BaseModel):
    recommendations: str = Field(..., description="Relatório de nivelamento em formato markdown")
