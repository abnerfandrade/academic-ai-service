from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.middlewares import request_id


def init_app(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_middleware = app.middleware("http")
    register_middleware(request_id.middleware)
