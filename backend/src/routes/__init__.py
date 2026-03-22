from fastapi import FastAPI
from src.routes import users, documents, sessions, health


def init_app(app: FastAPI) -> None:
    users.init_app(app)
    documents.init_app(app)
    sessions.init_app(app)
    health.init_app(app)
