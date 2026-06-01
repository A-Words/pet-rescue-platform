import api from './index'
import type { FoundClue } from '@/types/models'

export const foundCluesApi = {
  submit(lostPetId: string, data: Partial<FoundClue>) {
    return api.post<FoundClue>(`/found-clues/lost-pets/${lostPetId}/clues`, data)
  },
  listForPet(lostPetId: string) {
    return api.get<FoundClue[]>(`/found-clues/lost-pets/${lostPetId}/clues`)
  },
  getDetail(foundClueId: string) {
    return api.get<FoundClue>(`/found-clues/${foundClueId}`)
  },
  updateStatus(foundClueId: string, status: string, notes?: string) {
    return api.patch(`/found-clues/${foundClueId}/status`, { status, admin_notes: notes })
  },
  getMy() {
    return api.get<FoundClue[]>('/found-clues/my')
  },
}
