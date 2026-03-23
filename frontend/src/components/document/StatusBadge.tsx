import { Badge } from '@/components/ui/badge'
import type { DocumentStatus } from '../../types/document'

const config: Record<DocumentStatus, { label: string; variant: 'default' | 'secondary' | 'destructive' | 'outline' }> = {
  queued:     { label: 'Na fila',       variant: 'secondary' },
  processing: { label: 'Processando',   variant: 'default' },
  completed:  { label: 'Pronto',        variant: 'default' },   // adicione classe verde via className
  failed:     { label: 'Erro',          variant: 'destructive' },
}

export function StatusBadge({ status }: { status: DocumentStatus }) {
  const { label, variant } = config[status]
  return (
    <Badge
      variant={variant}
      className={status === 'completed' ? 'bg-green-500 text-white' : undefined}
    >
      {label}
    </Badge>
  )
}
