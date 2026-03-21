from abc import ABC, abstractmethod
from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.db.database import db, Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
FiltersSchemaType = TypeVar("FiltersSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType, FiltersSchemaType], ABC):
    model: Type[ModelType]

    def __init__(self, session: AsyncSession = Depends(db)):
        self.session = session

    @abstractmethod
    async def create(self, data: CreateSchemaType) -> ModelType:
        """Create a new record."""
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[ModelType]:
        """Get a record by ID."""
        pass

    @abstractmethod
    async def get_all(self, filters: Optional[FiltersSchemaType] = None) -> List[ModelType]:
        """Get all records with optional filtering."""
        pass

    @abstractmethod
    async def update(self, id: int, data: UpdateSchemaType) -> ModelType:
        """Update an existing record."""
        pass

    @abstractmethod
    async def delete(self, id: int) -> None:
        """Delete a record."""
        pass
