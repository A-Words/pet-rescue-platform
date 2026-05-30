import api from './index'
import type { LostPet, PaginatedResponse } from '@/types/models'

export const lostPetsApi = {
  list(params: Record<string, any>) {
    return api.get<PaginatedResponse<LostPet>>('/lost-pets', { params })
  },
  getDetail(id: string) {
    return api.get<LostPet>(`/lost-pets/${id}`)
  },
  create(data: Partial<LostPet>) {
    return api.post<LostPet>('/lost-pets', data)
  },
  update(id: string, data: Partial<LostPet>) {
    return api.put<LostPet>(`/lost-pets/${id}`, data)
  },
  delete(id: string) {
    return api.delete(`/lost-pets/${id}`)
  },
  updateStatus(id: string, status: string) {
    return api.patch(`/lost-pets/${id}/status`, { status })
  },
  getMy() {
    return api.get<LostPet[]>('/lost-pets/my')
  },
}
