from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    id: int = Field(..., description="ID do usuário")
    name: str = Field(..., description="O nome do usuário")
    email: EmailStr = Field(..., description="O e-mail do usuário")
    created_at: datetime = Field(..., description="Data de criação do usuário")

    class Config:
        from_attributes = True
