import { useQuery } from '@tanstack/react-query'
import { sessionsApi } from '../api/sessions'
import type { SessionFilters } from '../types/session'

export function useSessions(filters?: SessionFilters, enabled: boolean = true) {
  return useQuery({
    queryKey: ['sessions', filters],
    queryFn: () => sessionsApi.list(filters).then((r) => r.data),
    enabled: enabled,
  })
}
