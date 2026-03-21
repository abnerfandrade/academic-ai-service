from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    id: int = Field(..., description="Identificador único do documento")
    class_name: str = Field(..., description="O nome da classe do documento")
    filename: str = Field(..., description="Nome do arquivo enviado")
    status: Literal["queued", "processing", "completed", "failed"] = Field(
        default="queued", description="Status do processamento do documento"
    )


class DocumentResponse(BaseModel):
    id: int = Field(..., description="Identificador único do documento")
    class_name: str = Field(..., description="O nome da classe do documento")
    filename: str = Field(..., description="Nome do arquivo enviado")
    filehash: str = Field(..., description="Hash do arquivo enviado")
    status: Literal["queued", "processing", "completed", "failed"] = Field(
        ..., description="Status do processamento do documento"
    )
    error_detail: Optional[str] = Field(None, description="Detalhes do erro caso o processamento falhe")
    created_at: datetime = Field(..., description="Data de criação do registro")
    updated_at: Optional[datetime] = Field(None, description="Data da última atualização")
