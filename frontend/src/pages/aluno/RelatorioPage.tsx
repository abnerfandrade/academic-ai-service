import { useParams, useNavigate } from 'react-router-dom'
import { useReport } from '../../hooks/useReport'
import { ScoreMeter } from '../../components/report/ScoreMeter'
import { ConceptList } from '../../components/report/ConceptList'
import { RecommendationsMd } from '../../components/report/RecommendationsMd'
import { QuestionReview } from '../../components/report/QuestionReview'
import { Skeleton } from '@/components/ui/skeleton'
import { Button } from '@/components/ui/button'
import { ArrowLeft, Home } from 'lucide-react'
import { useSessionStore } from '../../stores/useSessionStore'

export function RelatorioPage() {
  const { sessionId } = useParams<{ sessionId: string }>()
  const navigate = useNavigate()
  const { reset } = useSessionStore()
  const { data: report, isLoading, isError } = useReport(sessionId ? Number(sessionId) : null)

  const handleGoHome = () => {
    reset()
    navigate('/')
  }

  if (isLoading) return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <Skeleton className="h-8 w-48" />
      <Skeleton className="h-24 w-full" />
      <Skeleton className="h-48 w-full" />
    </div>
  )

  if (isError) return (
    <div className="max-w-3xl mx-auto p-6 text-center space-y-4">
      <p className="text-muted-foreground">Relatório ainda não disponível. Aguarde o encerramento da sessão.</p>
      <Button onClick={() => navigate(-1)}>Voltar ao chat</Button>
    </div>
  )

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-8">
      <div className="flex items-center justify-between">
        <Button variant="ghost" onClick={() => navigate(-1)}>
          <ArrowLeft size={16} className="mr-2" /> Voltar
        </Button>
        <Button variant="outline" onClick={handleGoHome}>
          <Home size={16} className="mr-2" /> Início
        </Button>
      </div>
      <h1 className="text-2xl font-bold">Seu relatório de nivelamento</h1>
      <ScoreMeter score={report!.overall_score} />
      <ConceptList strengths={report!.strengths} weaknesses={report!.weaknesses} />
      <div>
        <h2 className="text-lg font-semibold mb-3">Recomendações de estudo</h2>
        <RecommendationsMd content={report!.recommendations} />
      </div>
      <div>
        <h2 className="text-lg font-semibold mb-3">Revisão do questionário</h2>
        <QuestionReview questions={report!.questions} />
      </div>
    </div>
  )
}
