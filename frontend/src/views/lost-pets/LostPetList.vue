<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useLostPetsStore } from '@/stores/lostPets'
import { petTypeLabels, lostPetStatusLabels, lostPetStatusTypes, formatDate } from '@/utils/format'

const router = useRouter()
const store = useLostPetsStore()

const filters = ref({
  page: 1,
  page_size: 12,
  pet_type: '',
  status: '',
  keyword: '',
})

onMounted(() => {
  loadPets()
})

async function loadPets() {
  const params: Record<string, any> = {
    page: filters.value.page,
    page_size: filters.value.page_size,
  }
  if (filters.value.pet_type) params.pet_type = filters.value.pet_type
  if (filters.value.status) params.status = filters.value.status
  if (filters.value.keyword) params.keyword = filters.value.keyword
  await store.fetchPets(params)
}

function handleSearch() {
  filters.value.page = 1
  loadPets()
}

function handlePageChange(page: number) {
  filters.value.page = page
  loadPets()
}
</script>

<template>
  <div>
    <div class="page-header">
      <div class="page-header-row">
        <h2>走失宠物</h2>
        <el-button type="primary" @click="router.push('/lost-pets/publish')">发布走失信息</el-button>
      </div>
    </div>

    <div class="filter-bar">
      <el-input
        v-model="filters.keyword"
        placeholder="搜索宠物名称、品种..."
        style="width: 240px"
        @keyup.enter="handleSearch"
        clearable
      />
      <el-select v-model="filters.pet_type" placeholder="宠物类型" clearable @change="handleSearch">
        <el-option label="狗" value="dog" />
        <el-option label="猫" value="cat" />
        <el-option label="鸟" value="bird" />
        <el-option label="其他" value="other" />
      </el-select>
      <el-select v-model="filters.status" placeholder="状态" clearable @change="handleSearch">
        <el-option label="寻找中" value="active" />
        <el-option label="已找回" value="found" />
        <el-option label="已关闭" value="closed" />
      </el-select>
      <el-button type="primary" @click="handleSearch">搜索</el-button>
    </div>

    <div v-loading="store.loading" class="card-grid">
      <el-card
        v-for="pet in store.pets"
        :key="pet.id"
        class="pet-card"
        shadow="hover"
        @click="router.push(`/lost-pets/${pet.id}`)"
      >
        <div class="pet-photo">
          <img v-if="pet.photo_urls?.length" :src="pet.photo_urls[0]" :alt="pet.pet_name" />
          <div v-else class="no-photo">暂无照片</div>
        </div>
        <div class="pet-info">
          <h3>{{ pet.pet_name }}</h3>
          <p>{{ petTypeLabels[pet.pet_type] || pet.pet_type }} {{ pet.breed || '' }}</p>
          <p class="location">走失地点：{{ pet.lost_location }}</p>
          <p class="date">走失日期：{{ formatDate(pet.lost_date) }}</p>
          <el-tag :type="(lostPetStatusTypes[pet.status] as any) || 'info'" size="small">
            {{ lostPetStatusLabels[pet.status] || pet.status }}
          </el-tag>
        </div>
      </el-card>
    </div>

    <div v-if="!store.loading && store.pets.length === 0" style="text-align: center; padding: 60px; color: #909399;">
      暂无走失宠物信息
    </div>

    <div v-if="store.total > filters.page_size" style="margin-top: 20px; display: flex; justify-content: center;">
      <el-pagination
        :current-page="filters.page"
        :page-size="filters.page_size"
        :total="store.total"
        layout="prev, pager, next"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<style scoped>
.page-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.pet-card {
  cursor: pointer;
  transition: transform 0.2s;
}

.pet-card:hover {
  transform: translateY(-2px);
}

.pet-photo {
  height: 180px;
  overflow: hidden;
  border-radius: 4px;
  margin-bottom: 12px;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pet-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-photo {
  color: #c0c4cc;
  font-size: 14px;
}

.pet-info h3 {
  font-size: 16px;
  margin-bottom: 4px;
}

.pet-info p {
  font-size: 13px;
  color: #606266;
  margin-bottom: 4px;
}

.pet-info .location,
.pet-info .date {
  font-size: 12px;
  color: #909399;
}
</style>
