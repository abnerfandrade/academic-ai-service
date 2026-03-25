import asyncio
from langchain.tools import tool, ToolRuntime
from qdrant_client import models
from loguru import logger

from src.services.vector_store.retriever import VectorStoreRetriever
from src.agents.consolidation_graph.state import ConsolidationState


@tool
async def search_chunks_for_evaluation(query: str, runtime: ToolRuntime[None, ConsolidationState]) -> str:
    """
    Busca chunks de documentos referentes à aula a partir de uma query semântica.
    Use esta ferramenta para encontrar o conteúdo específico do material da aula relacionado ao objetivo avaliado.
    A busca ajudará a embasar sua correção da resposta do aluno.
    Envie uma única query otimizada com base no objetivo avaliado e na pergunta feita.
    """
    session_id = runtime.state.get("session_id")
    document_id = runtime.state.get("document_id")
    class_name = runtime.state.get("class_name")

    log = logger.bind(
        graph="consolidation_graph",
        node="search_chunks_for_evaluation",
        session_id=session_id,
        document_id=document_id,
        class_name=class_name
    )
    log.debug(f"Buscando chunks para document_id={document_id} com a query: '{query}'")

    retriever = VectorStoreRetriever()

    qdrant_filter = models.Filter(
        must=[
            models.FieldCondition(
                key="metadata.document_id",
                match=models.MatchValue(value=document_id),
            )
        ]
    )

    try:
        results = await asyncio.to_thread(
            retriever.search,
            query=query,
            k=3,
            score_threshold=0.7,
            filter=qdrant_filter
        )
        
        if not results:
            return "Nenhum conteúdo específico encontrado na aula para esta consulta."

        formatted_results = [f"[chunk {r.metadata.get('chunk_index', 'N/A')}]\n{r.page_content}" for r in results]
        return "\n\n---\n\n".join(formatted_results)

    except Exception as e:
        log.error(f"Erro ao buscar chunks no Qdrant: {e}")
        return "Ocorreu um erro temporário no banco de dados vetorial durante a busca. Por favor, tente novamente."
