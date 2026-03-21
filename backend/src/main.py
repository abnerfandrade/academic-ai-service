from fastapi import FastAPI

from src import middlewares, routes
from src.core.logger import setup_logger


def create_app() -> FastAPI:
    setup_logger()

    app = FastAPI(
        title="Academic AI Service API",
        version="1.0.0",
    )

    middlewares.init_app(app)
    routes.init_app(app)

    return app
