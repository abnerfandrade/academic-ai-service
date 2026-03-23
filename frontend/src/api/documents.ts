import api from './axios'
import type {
  DocumentResponse,
  DocumentUploadResponse,
  DocumentStatusResponse,
  DocumentFilters,
} from '../types/document'

export const documentsApi = {
  upload: (file: File, class_name: string) => {
    const form = new FormData()
    form.append('file', file)
    form.append('class_name', class_name)
    return api.post<DocumentUploadResponse>('/documents/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },

  getStatus: (documentId: number) =>
    api.get<DocumentStatusResponse>(`/documents/${documentId}/status`),

  list: (filters?: DocumentFilters) =>
    api.get<DocumentResponse[]>('/documents/', { params: filters }),
}
