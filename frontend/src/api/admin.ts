import api from './index'
import type {
  AdoptionApplication,
  DashboardOverview,
  FoundClue,
  MonthlyStatistics,
  PaginatedResponse,
  VisitReminder,
} from '@/types/models'

export const adminApi = {
  // Applications
  getApplications(params: Record<string, any>) {
    return api.get<PaginatedResponse<AdoptionApplication>>('/admin/applications', { params })
  },
  reviewApplication(id: string, decision: string, notes?: string) {
    return api.post(`/admin/applications/${id}/review`, { decision, review_notes: notes })
  },

  // Statistics
  getStatistics(year: number, month: number, rescueStation?: string) {
    return api.get<MonthlyStatistics>('/admin/statistics', {
      params: { year, month, rescue_station: rescueStation || undefined },
    })
  },
  getDashboardOverview() {
    return api.get<DashboardOverview>('/admin/statistics/overview')
  },

  // Visit Reminders
  getReminders(params: Record<string, any>) {
    return api.get<PaginatedResponse<VisitReminder>>('/admin/visit-reminders', { params })
  },
  updateReminder(id: string, data: Partial<VisitReminder>) {
    return api.patch(`/admin/visit-reminders/${id}`, data)
  },

  // Clues
  getClues(params: Record<string, any>) {
    return api.get<PaginatedResponse<FoundClue>>('/admin/clues', { params })
  },
  reviewClue(id: string, status: string, notes?: string) {
    return api.patch(`/found-clues/${id}/status`, { status, admin_notes: notes })
  },
}
