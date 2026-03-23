export interface UserResponse {
  id: number
  name: string
  email: string
  created_at: string
}

export interface CreateUserRequest {
  name: string
  email: string
}

export interface UserFilters {
  name?: string
  email?: string
  created_after?: string
  created_before?: string
}