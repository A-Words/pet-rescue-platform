<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAdoptablePetsStore } from '@/stores/adoptablePets'
import { useUserStore } from '@/stores/user'
import { petTypeLabels, genderLabels, healthStatusLabels, formatDate } from '@/utils/format'

const route = useRoute()
const router = useRouter()
const store = useAdoptablePetsStore()
const userStore = useUserStore()

const pet = computed(() => store.currentPet)
const descriptionColumns = ref(2)

let detailMediaQuery: MediaQueryList | undefined

function updateDescriptionColumns() {
  descriptionColumns.value = detailMediaQuery?.matches ? 1 : 2
}

onMounted(async () => {
  detailMediaQuery = window.matchMedia('(max-width: 640px)')
  updateDescriptionColumns()
  detailMediaQuery.addEventListener('change', updateDescriptionColumns)

  await store.fetchPetDetail(route.params.adoptablePetId as string)
})

onBeforeUnmount(() => {
  detailMediaQuery?.removeEventListener('change', updateDescriptionColumns)
})
</script>

<template>
  <div v-loading="store.loading" class="detail-page">
    <template v-if="pet">
      <div class="page-header">
        <h2>{{ pet.pet_name }}</h2>
      </div>

      <el-row :gutter="24">
        <el-col :xs="24" :md="10">
          <div class="photo-section">
            <el-carousel v-if="pet.photo_urls?.length" height="300px">
              <el-carousel-item v-for="(url, idx) in pet.photo_urls" :key="idx">
                <img :src="url" :alt="pet.pet_name" class="carousel-img" />
              </el-carousel-item>
            </el-carousel>
            <div v-else class="no-photo">暂无照片</div>
          </div>
        </el-col>
        <el-col :xs="24" :md="14">
          <el-descriptions :column="descriptionColumns" border>
            <el-descriptions-item label="宠物类型">{{ petTypeLabels[pet.pet_type] }}</el-descriptions-item>
            <el-descriptions-item label="品种">{{ pet.breed || '-' }}</el-descriptions-item>
            <el-descriptions-item label="颜色">{{ pet.color || '-' }}</el-descriptions-item>
            <el-descriptions-item label="性别">{{ genderLabels[pet.gender || 'unknown'] }}</el-descriptions-item>
            <el-descriptions-item label="年龄">
              {{ pet.age_months ? `${Math.floor(pet.age_months / 12)}岁${pet.age_months % 12}月` : '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="健康状态">{{ healthStatusLabels[pet.health_status] }}</el-descriptions-item>
            <el-descriptions-item label="疫苗">
              <el-tag :type="pet.is_vaccinated ? 'success' : 'info'" size="small">
                {{ pet.is_vaccinated ? '已接种' : '未接种' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="驱虫">
              <el-tag :type="pet.is_dewormed ? 'success' : 'info'" size="small">
                {{ pet.is_dewormed ? '已完成' : '未完成' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="绝育">
              <el-tag :type="pet.is_sterilized ? 'success' : 'info'" size="small">
                {{ pet.is_sterilized ? '已绝育' : '未绝育' }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="救助站">{{ pet.rescue_station || '-' }}</el-descriptions-item>
            <el-descriptions-item label="入站日期">{{ formatDate(pet.intake_date) }}</el-descriptions-item>
            <el-descriptions-item label="描述" :span="descriptionColumns">{{ pet.description || '-' }}</el-descriptions-item>
          </el-descriptions>

          <div class="actions" style="margin-top: 16px">
            <el-button
              v-if="userStore.isLoggedIn && pet.adoption_status === 'available'"
              type="primary"
              size="large"
              @click="router.push(`/adoption/${pet.adoptable_pet_id}/apply`)"
            >
              申请领养
            </el-button>
            <el-button
              v-if="!userStore.isLoggedIn"
              type="primary"
              size="large"
              @click="router.push('/login')"
            >
              登录后申请领养
            </el-button>
          </div>
        </el-col>
      </el-row>
    </template>
  </div>
</template>

<style scoped>
.detail-page {
  max-width: 1000px;
  margin: 0 auto;
}

.photo-section {
  background: #f5f7fa;
  border-radius: 8px;
  overflow: hidden;
}

.carousel-img {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.no-photo {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #c0c4cc;
}
</style>
