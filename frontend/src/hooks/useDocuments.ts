import { useQuery } from '@tanstack/react-query'
import { documentsApi } from '../api/documents'
import type { DocumentFilters } from '../types/document'

export function useDocuments(filters?: DocumentFilters) {
  return useQuery({
    queryKey: ['documents', filters],
    queryFn: () => documentsApi.list(filters).then((r) => r.data),
    refetchInterval: (query) => {
      const docs = query.state.data
      const hasProcessing = docs?.some(d => d.status === 'queued' || d.status === 'processing')
      return hasProcessing ? 3000 : false
    },
  })
}
