import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { BookOpen, Clock } from 'lucide-react'
import { StatusBadge } from './StatusBadge'
import type { DocumentResponse } from '../../types/document'
import type { SessionResponse } from '../../types/session'

interface Props {
  document: DocumentResponse
  session?: SessionResponse
  onStart: (documentId: number) => void
  onViewReport?: (sessionId: number) => void
}

export function DocumentCard({ document, session, onStart, onViewReport }: Props) {
  const isCompleted = session?.status === 'completed'
  const isActive = session?.status === 'active'

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
      <CardFooter>
        {isCompleted ? (
          <Button variant="secondary" className="w-full" onClick={() => onViewReport?.(session.id)}>
            Ver Relatório
          </Button>
        ) : isActive ? (
          <Button disabled variant="outline" className="w-full">
            Nivelamento em andamento
          </Button>
        ) : (
          <Button className="w-full" onClick={() => onStart(document.id)}>
            Iniciar Nivelamento
          </Button>
        )}
      </CardFooter>
    </Card>
  )
}
