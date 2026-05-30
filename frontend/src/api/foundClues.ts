import api from './index'
import type { FoundClue } from '@/types/models'

export const foundCluesApi = {
  submit(petId: string, data: Partial<FoundClue>) {
    return api.post<FoundClue>(`/lost-pets/${petId}/clues`, data)
  },
  listForPet(petId: string) {
    return api.get<FoundClue[]>(`/lost-pets/${petId}/clues`)
  },
  getDetail(id: string) {
    return api.get<FoundClue>(`/found-clues/${id}`)
  },
  updateStatus(id: string, status: string, notes?: string) {
    return api.patch(`/found-clues/${id}/status`, { status, admin_notes: notes })
  },
  getMy() {
    return api.get<FoundClue[]>('/found-clues/my')
  },
}
