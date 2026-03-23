interface Props { score: number }

export function ScoreMeter({ score }: Props) {
  const percent = Math.round(score * 100)
  const color = percent >= 70 ? 'bg-green-500' : percent >= 40 ? 'bg-yellow-500' : 'bg-red-500'

  return (
    <div className="flex flex-col items-center gap-2">
      <span className="text-4xl font-bold">{percent}%</span>
      <div className="w-full h-3 bg-muted rounded-full overflow-hidden">
        <div className={`h-full rounded-full transition-all ${color}`} style={{ width: `${percent}%` }} />
      </div>
      <span className="text-sm text-muted-foreground">Pontuação geral</span>
    </div>
  )
}
