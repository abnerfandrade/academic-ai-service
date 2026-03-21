from src.db.database import Base, db


async def create_all_tables():
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


__all__ = ["db", "Base", "create_all_tables"]
