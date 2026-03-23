import api from './axios'
import type { UserResponse, CreateUserRequest, UserFilters } from '../types/user'

export const usersApi = {
  create: (body: CreateUserRequest) =>
    api.post<UserResponse>('/users/', body),

  list: (filters?: UserFilters) =>
    api.get<UserResponse[]>('/users/', { params: filters }),

  delete: (userId: number) =>
    api.delete(`/users/${userId}`),
}
