from typing import List, Optional
from sqlalchemy import select, update, delete
from src.db.models import SessionMessage
from src.repositories.base import BaseRepository
from .datatypes import SessionMessageCreate, SessionMessageUpdate, SessionMessageFilters
from .exceptions import SessionMessageNotFoundError, SessionMessageCreateError, SessionMessageUpdateError, SessionMessageDeleteError


class SessionMessageRepository(BaseRepository[SessionMessage, SessionMessageCreate, SessionMessageUpdate, SessionMessageFilters]):
    async def create(self, data: SessionMessageCreate) -> SessionMessage:
        try:
            new_msg = SessionMessage(**data.model_dump())

            self.session.add(new_msg)
            await self.session.flush()
            await self.session.refresh(new_msg)

            return new_msg
        except Exception as e:
            raise SessionMessageCreateError(f"Erro ao criar mensagem da sessão: {str(e)}")

    async def get_by_id(self, id: int) -> Optional[SessionMessage]:
        try:
            query = select(SessionMessage).where(SessionMessage.id == id)
            result = await self.session.execute(query)

            return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Erro ao buscar a mensagem {id}: {e}") from e

    async def get_all(self, filters: Optional[SessionMessageFilters] = None) -> List[SessionMessage]:
        try:
            query = select(SessionMessage)

            if filters:
                filter_map = {
                    "session_id": lambda v: query.where(SessionMessage.session_id == v),
                    "type": lambda v: query.where(SessionMessage.type == v),
                    "created_before": lambda v: query.where(SessionMessage.created_at <= v),
                    "created_after": lambda v: query.where(SessionMessage.created_at >= v),
                }
                for field, apply_filter in filter_map.items():
                    value = getattr(filters, field, None)
                    if value is not None:
                        query = apply_filter(value)

            result = await self.session.execute(query)
            return list(result.scalars().all())
        except Exception as e:
            raise Exception(f"Erro ao buscar mensagens: {e}") from e

    async def update(self, id: int, data: SessionMessageUpdate) -> SessionMessage:
        try:
            msg = await self.get_by_id(id)
            if msg is None:
                raise SessionMessageNotFoundError(f"Mensagem {id} não encontrada")

            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(msg, field, value)

            await self.session.flush()
            await self.session.refresh(msg)

            return msg
        except SessionMessageNotFoundError:
            raise
        except Exception as e:
            raise SessionMessageUpdateError(f"Erro ao atualizar mensagem {id}: {str(e)}")

    async def delete(self, id: int) -> None:
        try:
            msg = await self.get_by_id(id)
            if msg is None:
                raise SessionMessageNotFoundError(f"Mensagem {id} não encontrada")

            await self.session.delete(msg)
            await self.session.flush()

            return True
        except SessionMessageNotFoundError:
            raise
        except Exception as e:
            raise SessionMessageDeleteError(f"Erro ao deletar mensagem {id}: {str(e)}")
