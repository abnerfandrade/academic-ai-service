from typing import List, Optional
from sqlalchemy import select, update, delete
from src.db.models import SessionReport
from src.repositories.base import BaseRepository
from .datatypes import SessionReportCreate, SessionReportUpdate, SessionReportFilters
from .exceptions import SessionReportNotFoundError, SessionReportCreateError, SessionReportUpdateError, SessionReportDeleteError


class SessionReportRepository(BaseRepository[SessionReport, SessionReportCreate, SessionReportUpdate, SessionReportFilters]):
    async def create(self, data: SessionReportCreate) -> SessionReport:
        try:
            new_report = SessionReport(**data.model_dump())

            self.session.add(new_report)
            await self.session.flush()
            await self.session.refresh(new_report)

            return new_report
        except Exception as e:
            raise SessionReportCreateError(f"Erro ao criar relatório da sessão: {str(e)}")

    async def get_by_id(self, id: int) -> Optional[SessionReport]:
        try:
            query = select(SessionReport).where(SessionReport.id == id)
            result = await self.session.execute(query)

            return result.scalar_one_or_none()
        except Exception as e:
            raise Exception(f"Erro ao buscar o relatório {id}: {e}") from e

    async def get_all(self, filters: Optional[SessionReportFilters] = None) -> List[SessionReport]:
        try:
            query = select(SessionReport)

            if filters:
                filter_map = {
                    "session_id": lambda v: query.where(SessionReport.session_id == v),
                    "case_type": lambda v: query.where(SessionReport.case_type == v),
                    "score_min": lambda v: query.where(SessionReport.overall_score >= v),
                    "score_max": lambda v: query.where(SessionReport.overall_score <= v),
                    "created_before": lambda v: query.where(SessionReport.created_at <= v),
                    "created_after": lambda v: query.where(SessionReport.created_at >= v),
                }
                for field, apply_filter in filter_map.items():
                    value = getattr(filters, field, None)
                    if value is not None:
                        query = apply_filter(value)

            result = await self.session.execute(query)
            return list(result.scalars().all())
        except Exception as e:
            raise Exception(f"Erro ao buscar relatórios: {e}") from e

    async def update(self, id: int, data: SessionReportUpdate) -> SessionReport:
        try:
            report = await self.get_by_id(id)
            if report is None:
                raise SessionReportNotFoundError(f"Relatório {id} não encontrado")

            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(report, field, value)

            await self.session.flush()
            await self.session.refresh(report)

            return report
        except SessionReportNotFoundError:
            raise
        except Exception as e:
            raise SessionReportUpdateError(f"Erro ao atualizar relatório {id}: {str(e)}")

    async def delete(self, id: int) -> None:
        try:
            report = await self.get_by_id(id)
            if report is None:
                raise SessionReportNotFoundError(f"Relatório {id} não encontrado")

            await self.session.delete(report)
            await self.session.flush()

            return True
        except SessionReportNotFoundError:
            raise
        except Exception as e:
            raise SessionReportDeleteError(f"Erro ao deletar relatório {id}: {str(e)}")
