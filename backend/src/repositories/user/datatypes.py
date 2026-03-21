from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(..., description="O nome do usuário")
    email: EmailStr = Field(..., description="O e-mail do usuário")


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, description="O nome do usuário")
    email: Optional[EmailStr] = Field(None, description="O e-mail do usuário")


class UserFilters(BaseModel):
    name: Optional[str] = Field(None, description="Filtrar por nome (substring insensível a maiúsculas/minúsculas)")
    email: Optional[EmailStr] = Field(None, description="Filtrar por e-mail exato")
    created_after: Optional[datetime] = Field(None, description="Filtrar por data de criação após")
    created_before: Optional[datetime] = Field(None, description="Filtrar por data de criação antes")
