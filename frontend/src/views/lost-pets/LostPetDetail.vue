<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useLostPetsStore } from '@/stores/lostPets'
import { useUserStore } from '@/stores/user'
import { foundCluesApi } from '@/api/foundClues'
import type { FoundClue } from '@/types/models'
import { petTypeLabels, genderLabels, lostPetStatusLabels, lostPetStatusTypes, clueStatusLabels, formatDate } from '@/utils/format'

const route = useRoute()
const router = useRouter()
const petStore = useLostPetsStore()
const userStore = useUserStore()

const pet = computed(() => petStore.currentPet)
const clues = ref<FoundClue[]>([])
const isOwner = computed(() => userStore.user?.id === pet.value?.user_id)

onMounted(async () => {
  const id = route.params.id as string
  await petStore.fetchPetDetail(id)
  if (isOwner.value || userStore.isAdmin) {
    try {
      const res = await foundCluesApi.listForPet(id)
      clues.value = res.data
    } catch {}
  }
})

async function updateStatus(status: string) {
  try {
    await petStore.updateStatus(route.params.id as string, status)
    ElMessage.success('状态更新成功')
    petStore.fetchPetDetail(route.params.id as string)
  } catch {
    ElMessage.error('状态更新失败')
  }
}
</script>

<template>
  <div v-loading="petStore.loading" class="detail-page">
    <template v-if="pet">
      <div class="page-header">
        <el-row justify="space-between" align="middle">
          <el-col>
            <h2>{{ pet.pet_name }}</h2>
          </el-col>
          <el-col :span="6" style="text-align: right">
            <el-tag :type="(lostPetStatusTypes[pet.status] as any)" size="large">
              {{ lostPetStatusLabels[pet.status] }}
            </el-tag>
          </el-col>
        </el-row>
      </div>

      <el-row :gutter="24">
        <el-col :span="10">
          <div class="photo-section">
            <el-carousel v-if="pet.photo_urls?.length" height="300px">
              <el-carousel-item v-for="(url, idx) in pet.photo_urls" :key="idx">
                <img :src="url" :alt="pet.pet_name" class="carousel-img" />
              </el-carousel-item>
            </el-carousel>
            <div v-else class="no-photo">暂无照片</div>
          </div>
        </el-col>
        <el-col :span="14">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="宠物类型">{{ petTypeLabels[pet.pet_type] }}</el-descriptions-item>
            <el-descriptions-item label="品种">{{ pet.breed || '-' }}</el-descriptions-item>
            <el-descriptions-item label="颜色">{{ pet.color || '-' }}</el-descriptions-item>
            <el-descriptions-item label="性别">{{ genderLabels[pet.gender || 'unknown'] }}</el-descriptions-item>
            <el-descriptions-item label="年龄">{{ pet.age_description || '-' }}</el-descriptions-item>
            <el-descriptions-item label="悬赏金额">{{ pet.reward_amount ? `¥${pet.reward_amount}` : '无' }}</el-descriptions-item>
            <el-descriptions-item label="走失日期" :span="2">{{ formatDate(pet.lost_date) }}</el-descriptions-item>
            <el-descriptions-item label="走失地点" :span="2">{{ pet.lost_location }}</el-descriptions-item>
            <el-descriptions-item label="联系方式" :span="2">{{ pet.contact_info }}</el-descriptions-item>
            <el-descriptions-item label="详细描述" :span="2">{{ pet.description }}</el-descriptions-item>
          </el-descriptions>

          <div class="actions" style="margin-top: 16px">
            <el-button
              v-if="userStore.isLoggedIn && !isOwner && pet.status === 'active'"
              type="warning"
              @click="router.push(`/lost-pets/${pet.id}/clue`)"
            >
              提交发现线索
            </el-button>
            <el-button
              v-if="isOwner && pet.status === 'active'"
              type="success"
              @click="updateStatus('found')"
            >
              标记为已找回
            </el-button>
            <el-button
              v-if="isOwner && pet.status !== 'closed'"
              @click="updateStatus('closed')"
            >
              关闭此信息
            </el-button>
          </div>
        </el-col>
      </el-row>

      <div v-if="clues.length > 0" class="clues-section">
        <h3>发现线索 ({{ clues.length }})</h3>
        <div class="responsive-table" style="--table-min-width: 760px">
          <el-table :data="clues" border max-height="640">
            <el-table-column prop="found_location" label="发现地点" />
            <el-table-column prop="found_date" label="发现日期" width="120">
              <template #default="{ row }">{{ formatDate(row.found_date) }}</template>
            </el-table-column>
            <el-table-column prop="description" label="描述" show-overflow-tooltip />
            <el-table-column prop="contact_info" label="联系方式" width="140" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag size="small">{{ clueStatusLabels[row.status] }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
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

.clues-section {
  margin-top: 30px;
}

.clues-section h3 {
  margin-bottom: 16px;
}
</style>
