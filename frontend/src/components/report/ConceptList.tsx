import { Badge } from '@/components/ui/badge'
import { CheckCircle, XCircle } from 'lucide-react'

interface Props {
  strengths: string[]
  weaknesses: string[]
}

export function ConceptList({ strengths, weaknesses }: Props) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <h3 className="flex items-center gap-2 font-semibold text-green-600 mb-2">
          <CheckCircle size={18} /> Conceitos dominados
        </h3>
        <div className="flex flex-wrap gap-2">
          {strengths.length === 0
            ? <p className="text-sm text-muted-foreground">Nenhum</p>
            : strengths.map((s) => <Badge key={s} className="bg-green-100 text-green-800">{s}</Badge>)
          }
        </div>
      </div>
      <div>
        <h3 className="flex items-center gap-2 font-semibold text-red-600 mb-2">
          <XCircle size={18} /> Lacunas identificadas
        </h3>
        <div className="flex flex-wrap gap-2">
          {weaknesses.length === 0
            ? <p className="text-sm text-muted-foreground">Nenhuma</p>
            : weaknesses.map((w) => <Badge key={w} className="bg-red-100 text-red-800">{w}</Badge>)
          }
        </div>
      </div>
    </div>
  )
}
