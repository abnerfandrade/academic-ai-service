from contextlib import asynccontextmanager

from fastapi import FastAPI
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from src import middlewares, routes
from src.core.config import settings
from src.core.logger import setup_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncPostgresSaver.from_conn_string(settings.CHECKPOINTER_URL) as checkpointer:
        await checkpointer.setup()
        app.state.checkpointer = checkpointer
        yield


def create_app() -> FastAPI:
    setup_logger()

    app = FastAPI(
        title="Academic AI Service API",
        version="1.0.0",
        lifespan=lifespan,
    )

    middlewares.init_app(app)
    routes.init_app(app)

    return app
