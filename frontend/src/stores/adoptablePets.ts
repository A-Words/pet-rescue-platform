import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { AdoptablePet } from '@/types/models'
import { adoptablePetsApi } from '@/api/adoptablePets'

export const useAdoptablePetsStore = defineStore('adoptablePets', () => {
  const pets = ref<AdoptablePet[]>([])
  const total = ref(0)
  const loading = ref(false)
  const currentPet = ref<AdoptablePet | null>(null)

  async function fetchPets(params: Record<string, any> = {}) {
    loading.value = true
    try {
      const res = await adoptablePetsApi.list(params)
      pets.value = res.data.items
      total.value = res.data.total
    } finally {
      loading.value = false
    }
  }

  async function fetchPetDetail(id: string) {
    loading.value = true
    try {
      const res = await adoptablePetsApi.getDetail(id)
      currentPet.value = res.data
      return res.data
    } finally {
      loading.value = false
    }
  }

  return { pets, total, loading, currentPet, fetchPets, fetchPetDetail }
})
