import sys
import logging
from loguru import logger
from src.core.contexts import get_request_id
from src.core.config import settings


class InterceptHandler(logging.Handler):
    """
    Intercepta logs do logging padrão e os redireciona para o loguru, preservando o nível de log e a estrutura de contexto.
    """
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def context_patcher(record):
    """Adiciona informações de contexto (request_id, duration_ms) a cada registro de log do loguru."""
    record["extra"]["request_id"] = get_request_id()
    record["extra"]["duration_ms"] = record.get('extra', {}).get('duration_ms', 0)


def setup_logger():
    logger.remove()
    logger.configure(patcher=context_patcher)

    if settings.ENVIRONMENT == "production":
        logger.add(
            sys.stdout,
            serialize=True,
            level=settings.LOG_LEVEL,
            enqueue=True
        )
    else:
        logger.add(
            sys.stdout,
            colorize=True,
            format=("<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{extra[request_id]}</cyan> | "
                    "<cyan>{extra[duration_ms]}ms</cyan> | <level>{name}:{function}:{line} - {message}</level>"),
            level=settings.LOG_LEVEL
        )

    logging.basicConfig(handlers=[InterceptHandler()], level=logging.WARNING)

    logging.getLogger("src").setLevel(settings.LOG_LEVEL)

    loggers_to_silence = ["uvicorn", "uvicorn.error", "fastapi"]
    for logger_name in loggers_to_silence:
        mod_logger = logging.getLogger(logger_name)
        mod_logger.handlers = [InterceptHandler()]
        mod_logger.propagate = False

    logging.getLogger("uvicorn.access").handlers = []
    logging.getLogger("uvicorn.access").propagate = False

    logging.getLogger("pdfminer").setLevel(logging.ERROR)


__all__ = ["logger", "setup_logger"]
