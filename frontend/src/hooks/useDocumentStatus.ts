import { useQuery } from '@tanstack/react-query'
import { documentsApi } from '../api/documents'

export function useDocumentStatus(documentId: number | null) {
  return useQuery({
    queryKey: ['doc-status', documentId],
    queryFn: () => documentsApi.getStatus(documentId!).then((r) => r.data),
    enabled: documentId !== null,
    refetchInterval: (query) => {
      const status = query.state.data?.status
      return status === 'queued' || status === 'processing' ? 3000 : false
    },
  })
}
