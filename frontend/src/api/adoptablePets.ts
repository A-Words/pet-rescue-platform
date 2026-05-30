import api from './index'
import type { AdoptablePet, PaginatedResponse } from '@/types/models'

export const adoptablePetsApi = {
  list(params: Record<string, any>) {
    return api.get<PaginatedResponse<AdoptablePet>>('/adoptable-pets', { params })
  },
  getDetail(id: string) {
    return api.get<AdoptablePet>(`/adoptable-pets/${id}`)
  },
  create(data: Partial<AdoptablePet>) {
    return api.post<AdoptablePet>('/adoptable-pets', data)
  },
  update(id: string, data: Partial<AdoptablePet>) {
    return api.put<AdoptablePet>(`/adoptable-pets/${id}`, data)
  },
  delete(id: string) {
    return api.delete(`/adoptable-pets/${id}`)
  },
  updateStatus(id: string, status: string) {
    return api.patch(`/adoptable-pets/${id}/status`, { status })
  },
}
