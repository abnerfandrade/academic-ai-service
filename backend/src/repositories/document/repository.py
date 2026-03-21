from typing import List, Optional
from sqlalchemy import select
from src.db.models import Document
from src.repositories.base import BaseRepository
from .datatypes import DocumentCreate, DocumentUpdate, DocumentFilters
from .exceptions import DocumentNotFoundError, DocumentCreateError, DocumentUpdateError, DocumentDeleteError


class DocumentRepository(BaseRepository[Document, DocumentCreate, DocumentUpdate, DocumentFilters]):
    async def create(self, data: DocumentCreate) -> Document:
        try:
            new_doc = Document(**data.model_dump())

            self.session.add(new_doc)
            await self.session.flush()
            await self.session.refresh(new_doc)

            return new_doc
        except Exception as e:
            raise DocumentCreateError(f"Erro ao criar documento: {str(e)}")

    async def get_by_id(self, id: int) -> Optional[Document]:
        try:
            query = select(Document).where(Document.id == id)
            result = await self.session.execute(query)

            return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Erro ao buscar o documento {id}: {e}") from e

    async def get_all(self, filters: Optional[DocumentFilters] = None) -> List[Document]:
        try:
            query = select(Document)

            if filters:
                filter_map = {
                    "class_name": lambda v: query.where(Document.class_name == v),
                    "status": lambda v: query.where(Document.status == v),
                    "created_before": lambda v: query.where(Document.created_at <= v),
                    "created_after": lambda v: query.where(Document.created_at >= v),
                }
                for field, apply_filter in filter_map.items():
                    value = getattr(filters, field, None)
                    if value is not None:
                        query = apply_filter(value)

            result = await self.session.execute(query)
            return list(result.scalars().all())
        except Exception as e:
            raise Exception(f"Erro ao buscar documentos: {e}") from e

    async def update(self, id: int, data: DocumentUpdate) -> Document:
        try:
            doc = await self.get_by_id(id)
            if doc is None:
                raise DocumentNotFoundError(f"Documento {id} não encontrado")

            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(doc, field, value)

            await self.session.flush()
            await self.session.refresh(doc)

            return doc
        except DocumentNotFoundError:
            raise
        except Exception as e:
            raise DocumentUpdateError(f"Erro ao atualizar documento {id}: {str(e)}")

    async def delete(self, id: int) -> None:
        try:
            doc = await self.get_by_id(id)
            if doc is None:
                raise DocumentNotFoundError(f"Documento {id} não encontrado")

            await self.session.delete(doc)
            await self.session.flush()

            return True
        except DocumentNotFoundError:
            raise
        except Exception as e:
            raise DocumentDeleteError(f"Erro ao deletar documento {id}: {str(e)}")
