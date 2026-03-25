import io
import asyncio
from pathlib import Path
from markitdown import MarkItDown
from loguru import logger


class DocumentExtractor:
    def __init__(self):
        self.md = MarkItDown()

    async def extract(self, content: bytes, filename: str) -> str:
        try:
            ext = Path(filename).suffix
            log = logger.bind(service="document_extractor", filename=filename, ext=ext)

            log.debug(f"Iniciando a extração do documento '{filename}'")

            text = await asyncio.to_thread(self.extract_sync, content, filename)
            log.info(f"Extração concluída | chars={len(text)}")

            return text

        except Exception as e:
            log.exception(f"Falha ao extrair texto do documento '{filename}'. Erro: {str(e)}")
            raise

    def extract_sync(self, content: bytes, filename: str) -> str:
        log = logger.bind(service="text_extractor", filename=filename)

        try:
            log.debug(f"Iniciando extração de texto do arquivo '{filename}'")

            ext = Path(filename).suffix
            result = self.md.convert_stream(io.BytesIO(content), file_extension=ext)

            log.debug(f"Extração de texto concluída | chars={len(result.text_content)}")
            return result.text_content

        except Exception as e:
            log.exception(f"Falha ao extrair texto do arquivo '{filename}'. Erro: {str(e)}")
            raise
