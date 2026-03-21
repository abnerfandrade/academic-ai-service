from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class DocumentCreate(BaseModel):
    class_name: str = Field(..., description="O nome da classe do documento")
    filename: str = Field(..., description="O nome do arquivo do documento")
    status: str = Field(..., description="O status do documento")
    error_detail: Optional[str] = Field(None, description="Detalhes do erro caso o processamento falhe")

class DocumentUpdate(BaseModel):
    class_name: Optional[str] = Field(None, description="O nome da classe do documento")
    filename: Optional[str] = Field(None, description="O nome do arquivo do documento")
    status: Optional[str] = Field(None, description="O status do documento")
    error_detail: Optional[str] = Field(None, description="Detalhes do erro caso o processamento falhe")

class DocumentFilters(BaseModel):
    class_name: Optional[str] = Field(None, description="Filtrar por nome da classe")
    status: Optional[str] = Field(None, description="Filtrar por status")
    created_after: Optional[datetime] = Field(None, description="Filtrar por data de criação após")
    created_before: Optional[datetime] = Field(None, description="Filtrar por data de criação antes")
