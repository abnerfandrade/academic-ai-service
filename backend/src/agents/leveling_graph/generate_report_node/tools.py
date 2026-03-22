import asyncio
from langchain.tools import tool, ToolRuntime
from qdrant_client import models

from src.services.vector_store.retriever import VectorStoreRetriever
from src.core.logger import logger
from .state import GenerateReportState


@tool
async def search_document_chunks_for_concepts(queries: list[str], runtime: ToolRuntime[None, GenerateReportState]) -> str:
    """
    Busca chunks de documentos referentes a aulas a partir de uma lista de queries semânticas.
    Use esta ferramenta para encontrar conceitos e tópicos do material da aula (documento) 
    para poder embasar e formular o relatório sobre as fraquezas e pontos fortes do aluno.
    Envie uma lista contendo queries otimizadas e abrangentes com base nos conceitos abordados.
    """
    session_id = runtime.state.get("session_id")
    document_id = runtime.state.get("document_id")
    class_name = runtime.state.get("class_name")

    log = logger.bind(
        graph="leveling_graph",
        node="generate_report_search_chunks",
        session_id=session_id,
        document_id=document_id,
        class_name=class_name
    )
    log.debug(f"Buscando chunks para document_id={document_id} com {len(queries)} queries")

    retriever = VectorStoreRetriever()

    qdrant_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.document_id",
                match=models.MatchValue(value=document_id),
            )
        ]
    )

    search_tasks = [
        asyncio.to_thread(
            retriever.search,
            query=query,
            k=3,
            score_threshold=0.7,
            filter=qdrant_filter
        )
        for query in queries
    ]
    search_results = await asyncio.gather(*search_tasks, return_exceptions=True)

    seen_chunks = set()
    deduped_chunks = []
    error_count = 0

    for chunks in search_results:
        if isinstance(chunks, Exception):
            log.error(f"Erro na busca: {chunks}")
            error_count += 1
            continue

        for chunk in chunks:
            chunk_index = chunk.metadata.get("chunk_index")
            if chunk_index not in seen_chunks:
                seen_chunks.add(chunk_index)
                deduped_chunks.append(chunk)

    if not deduped_chunks:
        if error_count > 0:
            return "Ocorreu um erro temporário no banco de dados vetorial durante a busca. Por favor, tente novamente."
        return "Nenhum chunk encontrado para estas consultas."

    deduped_chunks.sort(key=lambda d: d.metadata.get("chunk_index", 0))

    formatted_results = []
    for chunk in deduped_chunks:
        chunk_idx = chunk.metadata.get("chunk_index", "N/A")

        log.debug(f"Processando chunk {chunk_idx} com conteúdo: {chunk.page_content[:50]}...")
        formatted_results.append(f"[chunk {chunk_idx}]\n{chunk.page_content}")

    return "\n\n---\n\n".join(formatted_results)
