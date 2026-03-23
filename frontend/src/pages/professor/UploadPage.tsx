import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { UploadForm } from '../../components/document/UploadForm'
import { useDocumentStatus } from '../../hooks/useDocumentStatus'
import { StatusBadge } from '../../components/document/StatusBadge'
import { Button } from '@/components/ui/button'
import { ArrowLeft } from 'lucide-react'

export function UploadPage() {
  const navigate = useNavigate()
  const [uploadedId, setUploadedId] = useState<number | null>(null)
  const { data: statusData } = useDocumentStatus(uploadedId)

  return (
    <div className="max-w-lg mx-auto p-6 space-y-6">
      <Button variant="ghost" onClick={() => navigate('/')}>
        <ArrowLeft size={16} className="mr-2" /> Voltar
      </Button>
      <h1 className="text-2xl font-bold">Enviar aula</h1>
      <UploadForm onSuccess={(id) => setUploadedId(id)} />
      {uploadedId && statusData && (
        <div className="border rounded-lg p-4 flex items-center justify-between">
          <span className="text-sm">Status do processamento:</span>
          <StatusBadge status={statusData.status} />
        </div>
      )}
      <Button variant="outline" className="w-full" onClick={() => navigate('/professor/documentos')}>
        Ver todas as aulas
      </Button>
    </div>
  )
}
