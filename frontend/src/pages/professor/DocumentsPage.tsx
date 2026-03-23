import { useNavigate } from 'react-router-dom'
import { useDocuments } from '../../hooks/useDocuments'
import { StatusBadge } from '../../components/document/StatusBadge'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { ArrowLeft, Plus } from 'lucide-react'

export function DocumentsPage() {
  const navigate = useNavigate()
  const { data: documents, isLoading } = useDocuments()

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <Button variant="ghost" onClick={() => navigate('/')}>
          <ArrowLeft size={16} className="mr-2" /> Voltar
        </Button>
        <Button onClick={() => navigate('/professor/upload')}>
          <Plus size={16} className="mr-2" /> Nova aula
        </Button>
      </div>
      <h1 className="text-2xl font-bold">Aulas enviadas</h1>
      {isLoading
        ? Array.from({ length: 3 }).map((_, i) => <Skeleton key={i} className="h-16 w-full rounded-lg" />)
        : documents?.length === 0
          ? <p className="text-muted-foreground text-sm">Nenhuma aula enviada ainda.</p>
          : (
            <div className="space-y-3">
              {documents?.map((doc) => (
                <div key={doc.id} className="border rounded-lg p-4 flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold">{doc.class_name}</h3>
                    <p className="text-sm text-muted-foreground">{new Date(doc.created_at).toLocaleDateString('pt-BR')}</p>
                  </div>
                  <StatusBadge status={doc.status} />
                </div>
              ))}
            </div>
          )}
    </div>
  )
}
