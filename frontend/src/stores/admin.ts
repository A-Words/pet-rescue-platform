import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { AdoptionApplication, DashboardOverview, FoundClue, MonthlyStatistics, VisitReminder } from '@/types/models'
import { adminApi } from '@/api/admin'

export const useAdminStore = defineStore('admin', () => {
  const dashboard = ref<DashboardOverview | null>(null)
  const statistics = ref<MonthlyStatistics | null>(null)
  const reminders = ref<VisitReminder[]>([])
  const applications = ref<AdoptionApplication[]>([])
  const clues = ref<FoundClue[]>([])
  const loading = ref(false)

  async function fetchDashboard() {
    const res = await adminApi.getDashboardOverview()
    dashboard.value = res.data
  }

  async function fetchStatistics(year: number, month: number, rescueStation?: string) {
    const res = await adminApi.getStatistics(year, month, rescueStation)
    statistics.value = res.data
  }

  async function fetchApplications(params: Record<string, any> = {}) {
    loading.value = true
    try {
      const res = await adminApi.getApplications(params)
      applications.value = res.data.items
    } finally {
      loading.value = false
    }
  }

  async function reviewApplication(id: string, decision: string, notes?: string) {
    await adminApi.reviewApplication(id, decision, notes)
  }

  async function fetchReminders(params: Record<string, any> = {}) {
    loading.value = true
    try {
      const res = await adminApi.getReminders(params)
      reminders.value = res.data.items
    } finally {
      loading.value = false
    }
  }

  async function updateReminder(id: string, data: Partial<VisitReminder>) {
    await adminApi.updateReminder(id, data)
  }

  async function fetchClues(params: Record<string, any> = {}) {
    loading.value = true
    try {
      const res = await adminApi.getClues(params)
      clues.value = res.data.items
    } finally {
      loading.value = false
    }
  }

  async function reviewClue(id: string, status: string, notes?: string) {
    await adminApi.reviewClue(id, status, notes)
  }

  return {
    dashboard, statistics, reminders, applications, clues, loading,
    fetchDashboard, fetchStatistics, fetchApplications, reviewApplication,
    fetchReminders, updateReminder, fetchClues, reviewClue,
  }
})
