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

  async function fetchPetDetail(lostPetId: string) {
    loading.value = true
    try {
      const res = await lostPetsApi.getDetail(lostPetId)
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

  async function updatePet(lostPetId: string, data: Partial<LostPet>) {
    const res = await lostPetsApi.update(lostPetId, data)
    return res.data
  }

  async function deletePet(lostPetId: string) {
    await lostPetsApi.delete(lostPetId)
    pets.value = pets.value.filter((p) => p.lost_pet_id !== lostPetId)
  }

  async function updateStatus(lostPetId: string, status: string) {
    await lostPetsApi.updateStatus(lostPetId, status)
  }

  return { pets, total, loading, currentPet, fetchPets, fetchPetDetail, publishPet, updatePet, deletePet, updateStatus }
})
