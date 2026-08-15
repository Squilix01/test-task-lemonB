import { apiClient } from './client'

export interface LoginPayload {
  username: string
  password: string
}

export interface RegisterPayload {
  username: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface UserResponse {
  id: number
  username: string
}

export const authApi = {
  async login(payload: LoginPayload): Promise<TokenResponse> {
    const response = await apiClient.post<TokenResponse>('/api/auth/login', payload)
    return response.data
  },

  async register(payload: RegisterPayload): Promise<UserResponse> {
    const response = await apiClient.post<UserResponse>('/api/auth/register', payload)
    return response.data
  },

  async getMe(): Promise<UserResponse> {
    const response = await apiClient.get<UserResponse>('/api/auth/me')
    return response.data
  },
}
