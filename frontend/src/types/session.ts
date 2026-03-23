export type SessionStatus = 'active' | 'generating_report' | 'completed' | 'abandoned'

export interface SessionFilters {
  user_id?: number
  document_id?: number
  case_type?: string
  status?: string
}

export interface SessionResponse {
  id: number
  user_id: number
  document_id: number
  case_type: string
  status: SessionStatus
  started_at: string
  completed_at: string | null
}

export interface CreateSessionRequest {
  user_id: number
  document_id: number
}

export interface CreateSessionResponse {
  session_id: number
  status: SessionStatus
  first_message: string
}

export interface TurnRequest {
  student_message: string
}

export interface TurnResponse {
  agent_message: string
  session_status: SessionStatus
}

export interface QuestionReviewItem {
  question: string
  student_answer: string
  is_correct: boolean
  concept_tag: string
  justification: string
}

export interface ReportResponse {
  overall_score: number
  strengths: string[]
  weaknesses: string[]
  recommendations: string
  questions: QuestionReviewItem[]
}

export interface ChatMessage {
  role: 'ai' | 'human'
  content: string
}