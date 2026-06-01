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
  reviewApplication(applicationId: string, decision: string, notes?: string) {
    return api.post(`/admin/applications/${applicationId}/review`, { decision, review_notes: notes })
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
  updateReminder(reminderId: string, data: Partial<VisitReminder>) {
    return api.patch(`/admin/visit-reminders/${reminderId}`, data)
  },

  // Clues
  getClues(params: Record<string, any>) {
    return api.get<PaginatedResponse<FoundClue>>('/admin/clues', { params })
  },
  reviewClue(foundClueId: string, status: string, notes?: string) {
    return api.patch(`/found-clues/${foundClueId}/status`, { status, admin_notes: notes })
  },
}
