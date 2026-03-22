from typing import List
from pydantic import EmailStr
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Query

from src.repositories.user import UserRepository, UserCreate, UserFilters
from src.repositories.user.exceptions import UserNotFoundError, UserCreateError, UserDeleteError
from src.routes.users.datatypes import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


def init_app(app: FastAPI) -> None:
    app.include_router(router)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    user_repo: UserRepository = Depends(),
) -> UserResponse:
    try:
        user = await user_repo.create(data)

        return UserResponse.model_validate(user)
    except UserCreateError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar usuário: {str(e)}"
        )


@router.get("/", response_model=List[UserResponse])
async def list_users(
    name: str | None = Query(None, description="Filtrar por nome"),
    email: EmailStr | None = Query(None, description="Filtrar por e-mail"),
    created_after: str | None = Query(None, description="Filtrar por data de criação após"),
    created_before: str | None = Query(None, description="Filtrar por data de criação antes"),
    user_repo: UserRepository = Depends(),
) -> List[UserResponse]:
    try:
        filters = UserFilters(
            name=name,
            email=email,
            created_after=created_after,
            created_before=created_before,
        )
        users = await user_repo.get_all(filters)

        return [UserResponse.model_validate(user) for user in users]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar usuários: {str(e)}"
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    user_repo: UserRepository = Depends(),
) -> None:
    try:
        await user_repo.delete(user_id)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except UserDeleteError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar usuário: {str(e)}"
        )
