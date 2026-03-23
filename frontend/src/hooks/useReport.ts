import { useQuery } from '@tanstack/react-query'
import { sessionsApi } from '../api/sessions'

export function useReport(sessionId: number | null) {
  return useQuery({
    queryKey: ['report', sessionId],
    queryFn: () => sessionsApi.getReport(sessionId!).then((r) => r.data),
    enabled: sessionId !== null,
    retry: false,
  })
}
