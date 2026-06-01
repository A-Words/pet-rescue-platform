import api from './index'
import type { LostPet, PaginatedResponse } from '@/types/models'

export const lostPetsApi = {
  list(params: Record<string, any>) {
    return api.get<PaginatedResponse<LostPet>>('/lost-pets', { params })
  },
  getDetail(lostPetId: string) {
    return api.get<LostPet>(`/lost-pets/${lostPetId}`)
  },
  create(data: Partial<LostPet>) {
    return api.post<LostPet>('/lost-pets', data)
  },
  update(lostPetId: string, data: Partial<LostPet>) {
    return api.put<LostPet>(`/lost-pets/${lostPetId}`, data)
  },
  delete(lostPetId: string) {
    return api.delete(`/lost-pets/${lostPetId}`)
  },
  updateStatus(lostPetId: string, status: string) {
    return api.patch(`/lost-pets/${lostPetId}/status`, { status })
  },
  getMy() {
    return api.get<LostPet[]>('/lost-pets/my')
  },
}
