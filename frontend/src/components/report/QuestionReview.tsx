import { CheckCircle, XCircle } from 'lucide-react'
import type { QuestionReviewItem } from '../../types/session'

interface Props { questions: QuestionReviewItem[] }

export function QuestionReview({ questions }: Props) {
  return (
    <div className="space-y-4">
      {questions.map((q, i) => (
        <div key={i} className="border rounded-lg p-4 space-y-2">
          <div className="flex items-start justify-between gap-2">
            <p className="font-medium text-sm">{q.question}</p>
            {q.is_correct
              ? <CheckCircle className="text-green-500 shrink-0" size={18} />
              : <XCircle className="text-red-500 shrink-0" size={18} />
            }
          </div>
          <p className="text-sm text-muted-foreground">
            <span className="font-medium text-foreground">Sua resposta:</span> {q.student_answer}
          </p>
          <p className="text-xs text-muted-foreground italic">{q.justification}</p>
          <span className="text-xs bg-slate-100 text-slate-700 rounded px-2 py-0.5 inline-block">
            {q.concept_tag}
          </span>
        </div>
      ))}
    </div>
  )
}
