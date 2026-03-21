from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class SessionMessageCreate(BaseModel):
    session_id: int = Field(..., description="ID da sessão à qual esta mensagem pertence")
    type: str = Field(..., description="Tipo da mensagem (ex: 'human', 'ai', 'system')")
    content: str = Field(..., description="Conteúdo da mensagem")
    additional_kwargs: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Metadados adicionais para a mensagem")
    response_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Metadados do provedor de IA")
    tool_call_id: Optional[str] = Field(None, description="ID da chamada de ferramenta, se aplicável")
    tool_name: Optional[str] = Field(None, description="Nome da ferramenta chamada, se aplicável")

class SessionMessageUpdate(BaseModel):
    content: Optional[str] = Field(None, description="Conteúdo da mensagem")
    additional_kwargs: Optional[Dict[str, Any]] = Field(None, description="Metadados adicionais para a mensagem")
    response_metadata: Optional[Dict[str, Any]] = Field(None, description="Metadados do provedor de IA")

class SessionMessageFilters(BaseModel):
    session_id: Optional[int] = Field(None, description="Filtrar por ID da sessão")
    type: Optional[str] = Field(None, description="Filtrar por tipo da mensagem")
    created_after: Optional[datetime] = Field(None, description="Filtrar por data de criação após")
    created_before: Optional[datetime] = Field(None, description="Filtrar por data de criação antes")
