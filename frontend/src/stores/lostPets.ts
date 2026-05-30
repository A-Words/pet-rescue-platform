import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { LostPet } from '@/types/models'
import { lostPetsApi } from '@/api/lostPets'

export const useLostPetsStore = defineStore('lostPets', () => {
  const pets = ref<LostPet[]>([])
  const total = ref(0)
  const loading = ref(false)
  const currentPet = ref<LostPet | null>(null)

  async function fetchPets(params: Record<string, any> = {}) {
    loading.value = true
    try {
      const res = await lostPetsApi.list(params)
      pets.value = res.data.items
      total.value = res.data.total
    } finally {
      loading.value = false
    }
  }

  async function fetchPetDetail(id: string) {
    loading.value = true
    try {
      const res = await lostPetsApi.getDetail(id)
      currentPet.value = res.data
      return res.data
    } finally {
      loading.value = false
    }
  }

  async function publishPet(data: Partial<LostPet>) {
    const res = await lostPetsApi.create(data)
    return res.data
  }

  async function updatePet(id: string, data: Partial<LostPet>) {
    const res = await lostPetsApi.update(id, data)
    return res.data
  }

  async function deletePet(id: string) {
    await lostPetsApi.delete(id)
    pets.value = pets.value.filter((p) => p.id !== id)
  }

  async function updateStatus(id: string, status: string) {
    await lostPetsApi.updateStatus(id, status)
  }

  return { pets, total, loading, currentPet, fetchPets, fetchPetDetail, publishPet, updatePet, deletePet, updateStatus }
})
