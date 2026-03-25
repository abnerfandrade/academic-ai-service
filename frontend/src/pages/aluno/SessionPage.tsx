import { useEffect, useRef } from 'react'
import { useNavigate, useParams, useLocation } from 'react-router-dom'
import { toast } from 'sonner'
import { ChatWindow } from '../../components/chat/ChatWindow'
import { ChatInput } from '../../components/chat/ChatInput'
import { Button } from '@/components/ui/button'
import { useSessionStore } from '../../stores/useSessionStore'
import { useUserStore } from '../../stores/useUserStore'
import { sessionsApi } from '../../api/sessions'
import { FileText } from 'lucide-react'

export function SessionPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { sessionId } = useParams<{ sessionId: string }>()
  const { user } = useUserStore()
  const {
    messages, sessionStatus, isSending, isCreatingSession,
    addMessage, setSessionStatus, setIsSending, setSession, setIsCreatingSession,
    sessionId: storedSessionId,
  } = useSessionStore()
  
  const initRef = useRef(false)

  // Inicializa sessão se a rota for 'novo'
  useEffect(() => {
    if (sessionId === 'novo') {
      const documentId = location.state?.documentId
      const caseType = location.state?.caseType || 'case1'
      
      if (!documentId || !user) {
        navigate('/aluno', { replace: true })
        return
      }
      
      if (initRef.current) return
      initRef.current = true
      
      const createSession = async () => {
        setIsCreatingSession(true)
        try {
          const res = await sessionsApi.create({ user_id: user.id, document_id: documentId, case_type: caseType })
          setSession(res.data.session_id, documentId, res.data.first_message, caseType)
          navigate(`/aluno/sessao/${res.data.session_id}`, { replace: true })
        } catch (err: any) {
          const status = err?.response?.status
          if (status === 409) toast.error('Você já tem uma sessão ativa para esta aula.')
          else toast.error('Erro ao iniciar. Tente novamente.')
          navigate('/aluno', { replace: true })
        } finally {
          setIsCreatingSession(false)
        }
      }

      createSession()
    } else {
      // Guard: se store vazio e não for 'novo', redireciona
      if (!storedSessionId) navigate('/aluno', { replace: true })
    }
  }, [sessionId, location.state, user, storedSessionId, navigate, setIsCreatingSession, setSession])

  const handleSend = async (text: string) => {
    if (!sessionId || sessionId === 'novo') return
    addMessage({ role: 'human', content: text })
    setIsSending(true)
    try {
      const res = await sessionsApi.turn(Number(sessionId), { student_message: text })
      addMessage({ role: 'ai', content: res.data.agent_message })
      
      if (res.data.session_status === 'generating_report') {
        setSessionStatus('generating_report')
        const reportRes = await sessionsApi.generateReport(Number(sessionId))
        addMessage({ role: 'ai', content: reportRes.data.agent_message })
        if (reportRes.data.session_status === 'completed') {
          setSessionStatus('completed')
        }
      } else if (res.data.session_status === 'completed') {
        setSessionStatus('completed')
      }
    } catch {
      toast.error('Erro ao enviar resposta. Tente novamente.')
    } finally {
      setIsSending(false)
    }
  }

  // Define o título da página baseado no state temporário (enquanto cria) ou no store (quando carregado)
  const storeCaseType = useSessionStore(state => state.caseType)
  const currentCaseType = (sessionId === 'novo' ? location.state?.caseType : storeCaseType) || 'case1'
  const pageTitle = currentCaseType === 'case2' ? 'Consolidação' : 'Nivelamento'

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto border-x">
      <div className="border-b px-4 py-3 flex items-center justify-between">
        <h2 className="font-semibold">{pageTitle}</h2>
        {sessionStatus === 'completed' && (
          <Button
            size="sm"
            onClick={() => navigate(`/aluno/sessao/${sessionId}/relatorio`)}
          >
            <FileText size={16} className="mr-2" />
            Ver meu resultado
          </Button>
        )}
      </div>
      <ChatWindow 
        messages={messages} 
        isSending={isSending} 
        isCreatingSession={isCreatingSession} 
        caseType={currentCaseType as 'case1' | 'case2'} 
      />
      <ChatInput
        onSend={handleSend}
        disabled={isSending || isCreatingSession || sessionStatus !== 'active'}
      />
    </div>
  )
}
