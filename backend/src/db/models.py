from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Float, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    sessions: Mapped[List["Session"]] = relationship("Session", back_populates="user")


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    class_name: Mapped[str] = mapped_column(String(255), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    filehash: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    error_detail: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    sessions: Mapped[List["Session"]] = relationship("Session", back_populates="document")


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id"), nullable=False)
    case_type: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="sessions")
    document: Mapped["Document"] = relationship("Document", back_populates="sessions")
    messages: Mapped[List["SessionMessage"]] = relationship("SessionMessage", back_populates="session")
    report: Mapped[Optional["SessionReport"]] = relationship("SessionReport", back_populates="session")


class SessionMessage(Base):
    __tablename__ = "session_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    additional_kwargs: Mapped[dict] = mapped_column(JSONB, server_default="{}", nullable=False)
    response_metadata: Mapped[dict] = mapped_column(JSONB, server_default="{}", nullable=False)
    tool_call_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    tool_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    session: Mapped["Session"] = relationship("Session", back_populates="messages")


class SessionReport(Base):
    __tablename__ = "session_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), unique=True, nullable=False)
    case_type: Mapped[str] = mapped_column(String(20), nullable=False)
    questions: Mapped[dict] = mapped_column(JSONB, nullable=False)
    overall_score: Mapped[float] = mapped_column(Float, nullable=False)
    strengths: Mapped[dict] = mapped_column(JSONB, server_default="[]", nullable=False)
    weaknesses: Mapped[dict] = mapped_column(JSONB, server_default="[]", nullable=False)
    recommendations: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    session: Mapped["Session"] = relationship("Session", back_populates="report")
