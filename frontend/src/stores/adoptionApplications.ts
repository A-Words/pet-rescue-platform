import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { AdoptionApplication } from '@/types/models'
import { adoptionApplicationsApi } from '@/api/adoptionApplications'

export const useAdoptionApplicationsStore = defineStore('adoptionApplications', () => {
  const applications = ref<AdoptionApplication[]>([])
  const loading = ref(false)

  async function fetchMyApplications() {
    loading.value = true
    try {
      const res = await adoptionApplicationsApi.getMy()
      applications.value = res.data
    } finally {
      loading.value = false
    }
  }

  async function submitApplication(data: Partial<AdoptionApplication>) {
    const res = await adoptionApplicationsApi.create(data)
    return res.data
  }

  async function cancelApplication(id: string) {
    await adoptionApplicationsApi.cancel(id)
    const app = applications.value.find((a) => a.id === id)
    if (app) app.status = 'cancelled'
  }

  return { applications, loading, fetchMyApplications, submitApplication, cancelApplication }
})
