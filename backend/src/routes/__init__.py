from fastapi import FastAPI
from src.routes import documents, sessions, health


def init_app(app: FastAPI) -> None:
    documents.init_app(app)
    sessions.init_app(app)
    health.init_app(app)
