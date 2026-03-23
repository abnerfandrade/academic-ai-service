import api from './axios'
import type {
  CreateSessionRequest,
  CreateSessionResponse,
  TurnRequest,
  TurnResponse,
  ReportResponse,
  SessionResponse,
  SessionFilters,
} from '../types/session'

export const sessionsApi = {
  create: (body: CreateSessionRequest) =>
    api.post<CreateSessionResponse>('/sessions', body),

  turn: (sessionId: number, body: TurnRequest) =>
    api.post<TurnResponse>(`/sessions/${sessionId}/turn`, body),

  getReport: (sessionId: number) =>
    api.get<ReportResponse>(`/sessions/${sessionId}/report`),

  list: (filters?: SessionFilters) =>
    api.get<SessionResponse[]>('/sessions/', { params: filters }),
}
