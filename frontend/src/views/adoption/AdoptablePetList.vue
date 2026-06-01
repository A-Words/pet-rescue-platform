<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAdoptablePetsStore } from '@/stores/adoptablePets'
import { petTypeLabels, genderLabels, healthStatusLabels } from '@/utils/format'

const router = useRouter()
const store = useAdoptablePetsStore()

const filters = ref({
  page: 1,
  page_size: 12,
  pet_type: '',
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
      <h2>领养中心</h2>
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
      <el-button type="primary" @click="handleSearch">搜索</el-button>
    </div>

    <div v-loading="store.loading" class="card-grid">
      <el-card
        v-for="pet in store.pets"
        :key="pet.adoptable_pet_id"
        class="pet-card"
        shadow="hover"
        @click="router.push(`/adoption/${pet.adoptable_pet_id}`)"
      >
        <div class="pet-photo">
          <img v-if="pet.photo_urls?.length" :src="pet.photo_urls[0]" :alt="pet.pet_name" />
          <div v-else class="no-photo">暂无照片</div>
        </div>
        <div class="pet-info">
          <h3>{{ pet.pet_name }}</h3>
          <p>{{ petTypeLabels[pet.pet_type] || pet.pet_type }} {{ pet.breed || '' }}</p>
          <p>{{ genderLabels[pet.gender || 'unknown'] }} {{ pet.age_months ? `${Math.floor(pet.age_months / 12)}岁${pet.age_months % 12}月` : '' }}</p>
          <div class="tags">
            <el-tag v-if="pet.is_vaccinated" type="success" size="small">已疫苗</el-tag>
            <el-tag v-if="pet.is_dewormed" type="success" size="small">已驱虫</el-tag>
            <el-tag v-if="pet.is_sterilized" type="success" size="small">已绝育</el-tag>
            <el-tag size="small">{{ healthStatusLabels[pet.health_status] }}</el-tag>
          </div>
        </div>
      </el-card>
    </div>

    <div v-if="!store.loading && store.pets.length === 0" style="text-align: center; padding: 60px; color: #909399;">
      暂无可领养宠物
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

.tags {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
  margin-top: 8px;
}
</style>
