from typing import List
from datetime import datetime
from pydantic import BaseModel, Field


class CreateSessionRequest(BaseModel):
    user_id: int = Field(..., description="ID do usuário")
    document_id: int = Field(..., description="ID do documento")


class CreateSessionResponse(BaseModel):
    session_id: int = Field(..., description="ID da sessão criada")
    status: str = Field(..., description="Status da sessão")
    first_message: str = Field(..., description="Primeira mensagem do agente")


class TurnRequest(BaseModel):
    student_message: str = Field(..., description="Resposta ou mensagem do aluno")


class TurnResponse(BaseModel):
    agent_message: str = Field(..., description="Mensagem de resposta do agente")
    session_status: str = Field(..., description="Status atual da sessão ('active' ou 'completed')")


class SessionResponse(BaseModel):
    id: int = Field(..., description="ID da sessão")
    user_id: int = Field(..., description="ID do usuário")
    document_id: int = Field(..., description="ID do documento")
    case_type: str = Field(..., description="Tipo de case")
    status: str = Field(..., description="Status da sessão")
    started_at: datetime | None = None
    completed_at: datetime | None = None


class QuestionReview(BaseModel):
    question: str = Field(..., description="Pergunta feita ao aluno")
    student_answer: str = Field(..., description="Resposta do aluno")
    is_correct: bool = Field(..., description="Se a resposta demonstra domínio do conceito")
    justification: str = Field(..., description="Justificativa da avaliação")
    concept_tag: str = Field(..., description="Tag do conceito avaliado")


class ReportResponse(BaseModel):
    overall_score: float = Field(..., description="Pontuação geral (0.0 a 1.0)")
    strengths: List[str] = Field(..., description="Conceitos dominados pelo aluno")
    weaknesses: List[str] = Field(..., description="Lacunas identificadas")
    recommendations: str = Field(..., description="Conteúdo de reforço em markdown")
    questions: List[QuestionReview] = Field(..., description="Revisão completa do questionário")
