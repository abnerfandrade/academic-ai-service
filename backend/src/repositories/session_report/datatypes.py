from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class SessionReportCreate(BaseModel):
    session_id: int = Field(..., description="ID da sessão à qual este relatório pertence")
    case_type: str = Field(..., description="Tipo do caso")
    questions: Dict[str, Any] = Field(..., description="Perguntas e respostas no relatório")
    overall_score: float = Field(..., description="Pontuação geral da sessão")
    strengths: Optional[List[Any]] = Field(default_factory=list, description="Pontos fortes identificados")
    weaknesses: Optional[List[Any]] = Field(default_factory=list, description="Pontos fracos identificados")
    recommendations: str = Field(..., description="Recomendações para o usuário")

class SessionReportUpdate(BaseModel):
    case_type: Optional[str] = Field(None, description="Tipo do caso")
    questions: Optional[Dict[str, Any]] = Field(None, description="Perguntas e respostas no relatório")
    overall_score: Optional[float] = Field(None, description="Pontuação geral da sessão")
    strengths: Optional[List[Any]] = Field(None, description="Pontos fortes identificados")
    weaknesses: Optional[List[Any]] = Field(None, description="Pontos fracos identificados")
    recommendations: Optional[str] = Field(None, description="Recomendações para o usuário")

class SessionReportFilters(BaseModel):
    session_id: Optional[int] = Field(None, description="Filtrar por ID da sessão")
    case_type: Optional[str] = Field(None, description="Filtrar por tipo do caso")
    score_min: Optional[float] = Field(None, description="Filtrar por pontuação geral mínima")
    score_max: Optional[float] = Field(None, description="Filtrar por pontuação geral máxima")
    created_after: Optional[datetime] = Field(None, description="Filtrar por data de criação após")
    created_before: Optional[datetime] = Field(None, description="Filtrar por data de criação antes")
