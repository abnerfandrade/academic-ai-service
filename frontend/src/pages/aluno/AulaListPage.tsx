import { useNavigate } from 'react-router-dom'
import { toast } from 'sonner'
import { useEffect } from 'react'
import { useDocuments } from '../../hooks/useDocuments'
import { useSessions } from '../../hooks/useSessions'
import { DocumentCard } from '../../components/document/DocumentCard'
import { useUserStore } from '../../stores/useUserStore'
import { Skeleton } from '@/components/ui/skeleton'
import { Button } from '@/components/ui/button'
import { ArrowLeft } from 'lucide-react'

export function AulaListPage() {
  const navigate = useNavigate()
  const { user } = useUserStore()
  const { data: documents, isLoading: isLoadingDocs } = useDocuments({ doc_status: 'completed' })
  const { data: sessions, isLoading: isLoadingSessions } = useSessions({ user_id: user?.id }, !!user)

  const isLoading = isLoadingDocs || isLoadingSessions

  useEffect(() => {
    if (!user) {
      toast.error('Selecione um usuário para continuar.')
      navigate('/usuarios', { state: { redirectTo: '/aluno' } })
    }
  }, [user, navigate])

  const handleStart = async (documentId: number) => {
    if (!user) {
      toast.error('Selecione um usuário antes de iniciar.')
      navigate('/usuarios', { state: { redirectTo: '/aluno' } })
      return
    }
    // Redireciona imediatamente para a página de nivelamento passando o documentId
    navigate(`/aluno/nivelamento/novo`, { state: { documentId } })
  }

  const handleViewReport = (sessionId: number) => {
    navigate(`/aluno/nivelamento/${sessionId}/relatorio`)
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <Button variant="ghost" onClick={() => navigate('/')}>
        <ArrowLeft size={16} className="mr-2" /> Voltar
      </Button>
      <h1 className="text-2xl font-bold">Aulas disponíveis</h1>
      {user && (
        <p className="text-sm text-muted-foreground">
          Logado como: <span className="font-medium text-foreground">{user.name}</span>
        </p>
      )}
      {isLoading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 3 }).map((_, i) => <Skeleton key={i} className="h-48 rounded-xl" />)}
        </div>
      ) : documents?.length === 0 ? (
        <p className="text-muted-foreground text-sm">Nenhuma aula disponível no momento.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {documents?.map((doc) => {
            const docSession = sessions?.find(s => s.document_id === doc.id)
            return (
              <DocumentCard
                key={doc.id}
                document={doc}
                session={docSession}
                onStart={handleStart}
                onViewReport={handleViewReport}
              />
            )
          })}
        </div>
      )}
    </div>
  )
}
