from loguru import logger
from fastapi import (
    APIRouter,
    Depends,
    FastAPI,
    HTTPException,
    Request,
    status
)
from langchain_core.messages import HumanMessage, AIMessage

from src.repositories.user import UserRepository
from src.repositories.document import DocumentRepository
from src.repositories.session import SessionRepository, SessionCreate, SessionFilters
from src.repositories.session_report import SessionReportRepository
from src.routes.sessions.datatypes import (
    CreateSessionRequest,
    CreateSessionResponse,
    TurnRequest,
    TurnResponse,
    ReportResponse,
    SessionResponse
)
from src.agents.leveling_graph.graph import build_leveling_graph


router = APIRouter(prefix="/sessions", tags=["sessions"])


def init_app(app: FastAPI) -> None:
    app.include_router(router)


@router.get("/", response_model=list[SessionResponse], status_code=status.HTTP_200_OK)
async def list_sessions(
    user_id: int | None = None,
    document_id: int | None = None,
    case_type: str | None = None,
    session_status: str | None = None,
    session_repo: SessionRepository = Depends(),
) -> list[SessionResponse]:
    """
    Lista sessões com filtros opcionais.
    """
    try:
        filters = SessionFilters(
            user_id=user_id,
            document_id=document_id,
            case_type=case_type,
            status=session_status,
        )
        sessions = await session_repo.get_all(filters)
        return [
            SessionResponse(
                id=s.id,
                user_id=s.user_id,
                document_id=s.document_id,
                case_type=s.case_type,
                status=s.status,
                started_at=s.started_at,
                completed_at=s.completed_at
            ) for s in sessions
        ]
    except Exception as e:
        logger.error(f"Erro ao listar sessões: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar sessões"
        )


@router.post("/", response_model=CreateSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    body: CreateSessionRequest,
    request: Request,
    user_repo: UserRepository = Depends(),
    doc_repo: DocumentRepository = Depends(),
    session_repo: SessionRepository = Depends(),
) -> CreateSessionResponse:
    """
    Cria uma nova sessão de nivelamento e executa o grafo até a primeira pergunta.
    O checkpointer salva o snapshot e o grafo pausa via interrupt_after.
    """
    try:
        user = await user_repo.get_by_id(body.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="user_id não encontrado"
            )
            
        doc = await doc_repo.get_by_id(body.document_id)
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="document_id não encontrado"
            )

        if doc.status != "completed":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="documento ainda não está processado"
            )

        existing_session = await session_repo.get_by_user_id_and_document_id(body.user_id, body.document_id)
        if existing_session:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="sessão já existe para este usuário e documento",
            )

        session_data = SessionCreate(
            user_id=body.user_id,
            document_id=body.document_id,
            case_type="case1",
            status="active",
        )
        session = await session_repo.create(session_data, commit=True)

        graph = build_leveling_graph(request.app.state.checkpointer)

        initial_state = {
            "messages": [],
            "session_id": session.id,
            "document_id": doc.id,
            "class_name": doc.class_name,
            "prerequisites": doc.prerequisites,
        }
        config = {"configurable": {"thread_id": f"leveling_{session.id}"}}

        logger.info(f"Executando leveling_graph para sessão {session.id}")
        final_state = await graph.ainvoke(initial_state, config=config)

        first_message = final_state.get("messages", [])[-1].content

        return CreateSessionResponse(
            session_id=session.id,
            status=session.status,
            first_message=first_message
        )
    except HTTPException:
        raise
    except Exception as e:
        msg = f"Erro ao criar a sessão para o usuário {body.user_id} e documento {body.document_id}"
        logger.error(f"{msg}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=msg
        )


@router.post("/{session_id}/turn", response_model=TurnResponse, status_code=status.HTTP_200_OK)
async def process_turn(
    session_id: int,
    body: TurnRequest,
    request: Request,
    session_repo: SessionRepository = Depends(),
) -> TurnResponse:
    """
    Recebe a resposta do aluno. O checkpointer retoma o grafo automaticamente
    a partir do ponto de interrupção (após ask_question).
    """
    try:
        session = await session_repo.get_by_id(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sessão não encontrada"
            )

        if session.status != "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A sessão não está ativa"
            )

        graph = build_leveling_graph(request.app.state.checkpointer)
        config = {"configurable": {"thread_id": f"leveling_{session_id}"}}

        state_snapshot = await graph.aget_state(config)
        next_nodes = state_snapshot.next if state_snapshot else []

        if "generate_report" in next_nodes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O relatório está pronto para ser gerado. Chame o endpoint /generate-report em vez disso."
            )

        await graph.aupdate_state(
            config,
            {"messages": [HumanMessage(content=body.student_message)]},
            as_node="ask_question",
        )

        logger.info(f"Retomando leveling_graph para sessão {session_id}, turno do usuário")
        final_state = await graph.ainvoke(None, config=config)

        report_in_state = final_state.get("report")
        
        state_snapshot = await graph.aget_state(config)
        next_nodes = state_snapshot.next if state_snapshot else []
        
        current_status = "active"
        if report_in_state:
            current_status = "completed"
        elif "generate_report" in next_nodes:
            current_status = "generating_report"

        agent_message = final_state.get("messages", [])[-1].content

        return TurnResponse(
            agent_message=agent_message,
            session_status=current_status
        )
    except HTTPException:
        raise
    except Exception as e:
        msg = f"Erro ao processar o turno para a sessão {session_id}"
        logger.error(f"{msg}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=msg
        )


@router.post("/{session_id}/generate-report", response_model=TurnResponse, status_code=status.HTTP_200_OK)
async def trigger_generate_report(
    session_id: int,
    request: Request,
    session_repo: SessionRepository = Depends(),
) -> TurnResponse:
    """
    Retoma a execução do grafo a partir do nó generate_report.
    """
    try:
        session = await session_repo.get_by_id(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sessão não encontrada"
            )

        if session.status != "active":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A sessão não está ativa"
            )

        graph = build_leveling_graph(request.app.state.checkpointer)
        config = {"configurable": {"thread_id": f"leveling_{session_id}"}}

        state_snapshot = await graph.aget_state(config)
        next_nodes = state_snapshot.next if state_snapshot else []

        if "generate_report" not in next_nodes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O relatório não está pronto para ser gerado. Responda a todas as perguntas."
            )

        logger.info(f"Retomando leveling_graph para sessão {session_id}, gerando relatório")
        final_state = await graph.ainvoke(None, config=config)

        report_in_state = final_state.get("report")
        current_status = "completed" if report_in_state else "active"

        agent_message = final_state.get("messages", [])[-1].content

        return TurnResponse(
            agent_message=agent_message,
            session_status=current_status
        )
    except HTTPException:
        raise
    except Exception as e:
        msg = f"Erro ao gerar o relatório para a sessão {session_id}"
        logger.error(f"{msg}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=msg
        )


@router.get("/{session_id}/report", response_model=ReportResponse, status_code=status.HTTP_200_OK)
async def get_report(
    session_id: int,
    session_repo: SessionRepository = Depends(),
    report_repo: SessionReportRepository = Depends(),
) -> ReportResponse:
    """
    Retorna o relatório completo gerado pelo nó generate_report.
    Disponível apenas após a sessão estar com status 'completed'.
    """
    try:
        session = await session_repo.get_by_id(session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sessão não encontrada"
            )

        if session.status != "completed":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Sessão ainda não foi concluída"
            )

        report = await report_repo.get_by_session_id(session_id)
        if not report:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Relatório não encontrado para esta sessão"
            )

        return ReportResponse(
            overall_score=report.overall_score,
            strengths=report.strengths,
            weaknesses=report.weaknesses,
            recommendations=report.recommendations,
            questions=report.questions,
        )
    except HTTPException:
        raise
    except Exception as e:
        msg = f"Erro buscar o relatório da sessão {session_id}"
        logger.error(f"{msg}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=msg
        )
