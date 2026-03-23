import { useEffect, useRef } from 'react'
import { ChatBubble } from './ChatBubble'
import type { ChatMessage } from '../../types/session'

interface Props {
  messages: ChatMessage[]
  isSending: boolean
  isCreatingSession?: boolean
}

export function ChatWindow({ messages, isSending, isCreatingSession }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isSending, isCreatingSession])

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-3">
      {messages.map((msg, i) => (
        <ChatBubble key={i} role={msg.role} content={msg.content} />
      ))}
      {isCreatingSession && (
        <div className="flex justify-start">
          <div className="bg-muted rounded-2xl px-4 py-3 text-sm text-muted-foreground italic rounded-tl-none animate-pulse">
            Gerando perguntas de nivelamento...
          </div>
        </div>
      )}
      {!isCreatingSession && isSending && (
        <div className="flex justify-start">
          <div className="bg-muted rounded-2xl px-4 py-3 text-sm text-muted-foreground italic rounded-tl-none">
            Digitando...
          </div>
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  )
}
