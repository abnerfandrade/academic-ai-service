import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { BookOpen, Clock } from 'lucide-react'
import { StatusBadge } from './StatusBadge'
import type { DocumentResponse } from '../../types/document'
import type { SessionResponse } from '../../types/session'

interface Props {
  document: DocumentResponse
  sessions?: SessionResponse[]
  onStart: (documentId: number, caseType: 'case1' | 'case2') => void
  onViewReport?: (sessionId: number) => void
}

export function DocumentCard({ document, sessions = [], onStart, onViewReport }: Props) {
  const sessionCase1 = sessions.find(s => s.case_type === 'case1')
  const sessionCase2 = sessions.find(s => s.case_type === 'case2')

  const isCompleted1 = sessionCase1?.status === 'completed'
  const isActive1 = sessionCase1?.status === 'active'

  const isCompleted2 = sessionCase2?.status === 'completed'
  const isActive2 = sessionCase2?.status === 'active'

  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <div className="flex items-center justify-between">
          <BookOpen className="text-blue-500" size={20} />
          <StatusBadge status={document.status} />
        </div>
        <CardTitle className="text-lg mt-2">{document.class_name}</CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground flex items-center gap-1">
          <Clock size={14} />
          {new Date(document.created_at).toLocaleDateString('pt-BR')}
        </p>
      </CardContent>
      <CardFooter className="flex flex-col gap-3 border-t pt-4">
        {/* Bloco Case 1 */}
        <div className="w-full flex flex-col gap-2">
          <span className="text-xs font-semibold text-muted-foreground uppercase">Nivelamento (Pré-aula)</span>
          {isCompleted1 ? (
            <Button variant="secondary" className="w-full" onClick={() => onViewReport?.(sessionCase1!.id)}>
              Ver Relatório
            </Button>
          ) : isActive1 ? (
            <Button disabled variant="outline" className="w-full">
              Em andamento...
            </Button>
          ) : (
            <Button className="w-full" variant="outline" onClick={() => onStart(document.id, 'case1')}>
              Iniciar Nivelamento
            </Button>
          )}
        </div>

        {/* Bloco Case 2 */}
        <div className="w-full flex flex-col gap-2 pt-2 border-t border-dashed">
          <span className="text-xs font-semibold text-muted-foreground uppercase">Consolidação (Pós-aula)</span>
          {isCompleted2 ? (
            <Button variant="secondary" className="w-full" onClick={() => onViewReport?.(sessionCase2!.id)}>
              Ver Relatório
            </Button>
          ) : isActive2 ? (
            <Button disabled variant="outline" className="w-full">
              Em andamento...
            </Button>
          ) : (
            <Button className="w-full" onClick={() => onStart(document.id, 'case2')}>
              Iniciar Consolidação
            </Button>
          )}
        </div>
      </CardFooter>
    </Card>
  )
}
