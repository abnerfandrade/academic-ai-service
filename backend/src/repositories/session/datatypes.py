from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    user_id: int = Field(..., description="ID do usuário que iniciou a sessão")
    document_id: int = Field(..., description="ID do documento associado à sessão")
    case_type: str = Field(..., description="Tipo de case (ex: 'case1', 'case2', 'case3')")
    status: str = Field(..., description="Status da sessão")


class SessionUpdate(BaseModel):
    case_type: Optional[str] = Field(None, description="Tipo do caso")
    status: Optional[str] = Field(None, description="Status da sessão")
    completed_at: Optional[datetime] = Field(None, description="Timestamp de quando a sessão foi finalizada")


class SessionFilters(BaseModel):
    user_id: Optional[int] = Field(None, description="Filtrar por ID do usuário")
    document_id: Optional[int] = Field(None, description="Filtrar por ID do documento")
    case_type: Optional[str] = Field(None, description="Filtrar por tipo do caso")
    status: Optional[str] = Field(None, description="Filtrar por status")
    started_after: Optional[datetime] = Field(None, description="Filtrar por data de início após")
    started_before: Optional[datetime] = Field(None, description="Filtrar por data de início antes")
