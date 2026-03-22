from pydantic import BaseModel, Field


class PrerequisitesOutput(BaseModel):
    concept_tags: list[str] = Field(..., description="Lista de tags de conceitos pré-requisitos")
