from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    class_name: str = Field(..., description="Aula a qual o documento pertence")
    filename: str = Field(..., description="Nome do documento")
    filehash: str = Field(..., description="Hash do documento enviado")
    status: str = Field(..., description="Status do documento")
    error_detail: Optional[str] = Field(None, description="Detalhes do erro caso o processamento falhe")


class DocumentUpdate(BaseModel):
    class_name: Optional[str] = Field(None, description="Aula a qual o documento pertence")
    filename: Optional[str] = Field(None, description="Nome do documento")
    status: Optional[str] = Field(None, description="Status do documento")
    error_detail: Optional[str] = Field(None, description="Detalhes do erro caso o processamento falhe")


class DocumentFilters(BaseModel):
    id: Optional[int] = Field(None, description="Filtrar pelo id do documento")
    class_name: Optional[str] = Field(None, description="Filtrar por nome da aula")
    filename: Optional[str] = Field(None, description="Filtrar por nome do documento")
    status: Optional[str] = Field(None, description="Filtrar por status")
    created_after: Optional[datetime] = Field(None, description="Filtrar por data de criação após")
    created_before: Optional[datetime] = Field(None, description="Filtrar por data de criação antes")
