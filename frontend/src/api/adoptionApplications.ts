import api from './index'
import type { AdoptionApplication } from '@/types/models'

export const adoptionApplicationsApi = {
  create(data: Partial<AdoptionApplication>) {
    return api.post<AdoptionApplication>('/adoption-applications', data)
  },
  getMy() {
    return api.get<AdoptionApplication[]>('/adoption-applications/my')
  },
  getDetail(applicationId: string) {
    return api.get<AdoptionApplication>(`/adoption-applications/${applicationId}`)
  },
  cancel(applicationId: string) {
    return api.patch(`/adoption-applications/${applicationId}/cancel`)
  },
}
