import { create } from 'zustand'
import type { ChatMessage, SessionStatus } from '../types/session'

interface SessionStore {
  sessionId: number | null
  documentId: number | null
  messages: ChatMessage[]
  sessionStatus: SessionStatus | null
  isSending: boolean
  isCreatingSession: boolean
  setSession: (sessionId: number, documentId: number, firstMessage: string) => void
  addMessage: (msg: ChatMessage) => void
  setSessionStatus: (status: SessionStatus) => void
  setIsSending: (val: boolean) => void
  setIsCreatingSession: (val: boolean) => void
  reset: () => void
}

export const useSessionStore = create<SessionStore>()((set) => ({
  sessionId: null,
  documentId: null,
  messages: [],
  sessionStatus: null,
  isSending: false,
  isCreatingSession: false,
  setSession: (sessionId, documentId, firstMessage) =>
    set({
      sessionId,
      documentId,
      messages: [{ role: 'ai', content: firstMessage }],
      sessionStatus: 'active',
      isCreatingSession: false,
    }),
  addMessage: (msg) =>
    set((state) => ({ messages: [...state.messages, msg] })),
  setSessionStatus: (status) => set({ sessionStatus: status }),
  setIsSending: (val) => set({ isSending: val }),
  setIsCreatingSession: (val) => set({ isCreatingSession: val }),
  reset: () =>
    set({ sessionId: null, documentId: null, messages: [], sessionStatus: null, isSending: false, isCreatingSession: false }),
}))
