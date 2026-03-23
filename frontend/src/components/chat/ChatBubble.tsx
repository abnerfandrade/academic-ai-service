import { cn } from '../../lib/utils'

interface Props {
  role: 'ai' | 'human'
  content: string
}

export function ChatBubble({ role, content }: Props) {
  const isAI = role === 'ai'
  return (
    <div className={cn('flex w-full', isAI ? 'justify-start' : 'justify-end')}>
      <div
        className={cn(
          'max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed',
          isAI
            ? 'bg-muted text-foreground rounded-tl-none'
            : 'bg-primary text-primary-foreground rounded-tr-none'
        )}
      >
        {content}
      </div>
    </div>
  )
}
