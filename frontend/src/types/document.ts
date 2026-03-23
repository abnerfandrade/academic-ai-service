export type DocumentStatus = 'queued' | 'processing' | 'completed' | 'failed'

export interface DocumentResponse {
  id: number
  class_name: string
  filename: string
  filehash: string
  status: DocumentStatus
  error_detail: string | null
  created_at: string
  updated_at: string
}

export interface DocumentUploadResponse {
  id: number
  class_name: string
  filename: string
  status: DocumentStatus
}

export interface DocumentStatusResponse {
  status: DocumentStatus
}

export interface DocumentFilters {
  id?: number
  class_name?: string
  filename?: string
  doc_status?: DocumentStatus
  created_after?: string
  created_before?: string
}