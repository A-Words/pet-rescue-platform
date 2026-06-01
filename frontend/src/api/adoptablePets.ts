import api from './index'
import type { AdoptablePet, PaginatedResponse } from '@/types/models'

export const adoptablePetsApi = {
  list(params: Record<string, any>) {
    return api.get<PaginatedResponse<AdoptablePet>>('/adoptable-pets', { params })
  },
  getDetail(adoptablePetId: string) {
    return api.get<AdoptablePet>(`/adoptable-pets/${adoptablePetId}`)
  },
  create(data: Partial<AdoptablePet>) {
    return api.post<AdoptablePet>('/adoptable-pets', data)
  },
  update(adoptablePetId: string, data: Partial<AdoptablePet>) {
    return api.put<AdoptablePet>(`/adoptable-pets/${adoptablePetId}`, data)
  },
  delete(adoptablePetId: string) {
    return api.delete(`/adoptable-pets/${adoptablePetId}`)
  },
  updateStatus(adoptablePetId: string, status: string) {
    return api.patch(`/adoptable-pets/${adoptablePetId}/status`, { status })
  },
}
