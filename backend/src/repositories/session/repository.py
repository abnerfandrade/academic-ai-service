from typing import List, Optional
from sqlalchemy import select
from src.db.models import Session
from src.repositories.base import BaseRepository
from .datatypes import SessionCreate, SessionUpdate, SessionFilters
from .exceptions import SessionNotFoundError, SessionCreateError, SessionUpdateError, SessionDeleteError


class SessionRepository(BaseRepository[Session, SessionCreate, SessionUpdate, SessionFilters]):
    async def create(self, data: SessionCreate, *, commit: bool = False) -> Session:
        try:
            new_session = Session(**data.model_dump())

            self.session.add(new_session)
            await self.session.flush()
            await self.session.refresh(new_session)

            if commit:
                await self.session.commit()

            return new_session
        except Exception as e:
            raise SessionCreateError(f"Erro ao criar sessão: {str(e)}")

    async def get_by_id(self, id: int) -> Optional[Session]:
        try:
            query = select(Session).where(Session.id == id)
            result = await self.session.execute(query)

            return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Erro ao buscar a sessão {id}: {e}") from e

    async def get_all(self, filters: Optional[SessionFilters] = None) -> List[Session]:
        try:
            query = select(Session)

            if filters:
                filter_map = {
                    "user_id": lambda v: query.where(Session.user_id == v),
                    "document_id": lambda v: query.where(Session.document_id == v),
                    "case_type": lambda v: query.where(Session.case_type == v),
                    "status": lambda v: query.where(Session.status == v),
                    "started_before": lambda v: query.where(Session.started_at <= v),
                    "started_after": lambda v: query.where(Session.started_at >= v),
                }
                for field, apply_filter in filter_map.items():
                    value = getattr(filters, field, None)
                    if value is not None:
                        query = apply_filter(value)

            result = await self.session.execute(query)
            return list(result.scalars().all())
        except Exception as e:
            raise Exception(f"Erro ao buscar sessões: {e}") from e

    async def update(self, id: int, data: SessionUpdate) -> Session:
        try:
            session_obj = await self.get_by_id(id)
            if session_obj is None:
                raise SessionNotFoundError(f"Sessão {id} não encontrada")

            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(session_obj, field, value)

            await self.session.flush()
            await self.session.refresh(session_obj)

            return session_obj
        except SessionNotFoundError:
            raise
        except Exception as e:
            raise SessionUpdateError(f"Erro ao atualizar sessão {id}: {str(e)}")

    async def delete(self, id: int) -> None:
        try:
            session_obj = await self.get_by_id(id)
            if session_obj is None:
                raise SessionNotFoundError(f"Sessão {id} não encontrada")

            await self.session.delete(session_obj)
            await self.session.flush()

            return True
        except SessionNotFoundError:
            raise
        except Exception as e:
            raise SessionDeleteError(f"Erro ao deletar sessão {id}: {str(e)}")

    async def get_by_user_id_and_document_id(self, user_id: int, document_id: int) -> Optional[Session]:
        try:
            query = select(Session).where(
                Session.user_id == user_id,
                Session.document_id == document_id
            )
            result = await self.session.execute(query)

            return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Erro ao buscar a sessão para o usuário {user_id} e documento {document_id}: {str(e)}")
