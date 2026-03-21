from typing import List, Optional
from sqlalchemy import select
from src.db.models import User
from src.repositories.base import BaseRepository
from .datatypes import UserCreate, UserUpdate, UserFilters
from .exceptions import UserNotFoundError, UserCreateError, UserUpdateError, UserDeleteError


class UserRepository(BaseRepository[User, UserCreate, UserUpdate, UserFilters]):
    async def create(self, data: UserCreate) -> User:
        try:
            new_user = User(**data.model_dump())

            self.session.add(new_user)
            await self.session.flush()
            await self.session.refresh(new_user)

            return new_user
        except Exception as e:
            raise UserCreateError(f"Erro ao criar usuário: {str(e)}")

    async def get_by_id(self, id: int) -> Optional[User]:
        try:
            query = select(User).where(User.id == id)
            result = await self.session.execute(query)

            return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Erro ao buscar o usuário {id}: {e}") from e

    async def get_all(self, filters: Optional[UserFilters] = None) -> List[User]:
        try:
            query = select(User)

            if filters:
                filter_map = {
                    "name": lambda v: query.where(User.name.ilike(f"%{v}%")),
                    "email": lambda v: query.where(User.email == v),
                    "created_before": lambda v: query.where(User.created_at <= v),
                    "created_after": lambda v: query.where(User.created_at >= v),
                }
                for field, apply_filter in filter_map.items():
                    value = getattr(filters, field, None)
                    if value is not None:
                        query = apply_filter(value)

            result = await self.session.execute(query)
            return list(result.scalars().all())
        except Exception as e:
            raise Exception(f"Erro ao buscar usuários: {e}") from e

    async def update(self, id: int, data: UserUpdate) -> User:
        try:
            user = await self.get_by_id(id)
            if user is None:
                raise UserNotFoundError(f"Usuário {id} não encontrado")

            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(user, field, value)

            await self.session.flush()
            await self.session.refresh(user)

            return user
        except UserNotFoundError:
            raise
        except Exception as e:
            raise UserUpdateError(f"Erro ao atualizar usuário {id}: {str(e)}")

    async def delete(self, id: int) -> None:
        try:
            user = await self.get_by_id(id)
            if user is None:
                raise UserNotFoundError(f"Usuário {id} não encontrado")

            await self.session.delete(user)
            await self.session.flush()

            return True
        except UserNotFoundError:
            raise
        except Exception as e:
            raise UserDeleteError(f"Erro ao deletar usuário {id}: {str(e)}")
