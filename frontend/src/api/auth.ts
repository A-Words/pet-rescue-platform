import api from './index'
import type { User } from '@/types/models'

export interface LoginData {
  username: string
  password: string
}

export interface RegisterData {
  username: string
  email: string
  password: string
  phone?: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export const authApi = {
  login(data: LoginData) {
    const formData = new URLSearchParams()
    formData.append('username', data.username)
    formData.append('password', data.password)
    return api.post<TokenResponse>('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
  },
  register(data: RegisterData) {
    return api.post<User>('/auth/register', data)
  },
  getMe() {
    return api.get<User>('/auth/me')
  },
  updateMe(data: Partial<User>) {
    return api.put<User>('/auth/me', data)
  },
}
