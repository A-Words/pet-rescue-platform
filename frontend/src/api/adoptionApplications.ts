import api from './index'
import type { AdoptionApplication } from '@/types/models'

export const adoptionApplicationsApi = {
  create(data: Partial<AdoptionApplication>) {
    return api.post<AdoptionApplication>('/adoption-applications', data)
  },
  getMy() {
    return api.get<AdoptionApplication[]>('/adoption-applications/my')
  },
  getDetail(id: string) {
    return api.get<AdoptionApplication>(`/adoption-applications/${id}`)
  },
  cancel(id: string) {
    return api.patch(`/adoption-applications/${id}/cancel`)
  },
}
