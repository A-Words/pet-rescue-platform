<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { foundCluesApi } from '@/api/foundClues'
import { lostPetsApi } from '@/api/lostPets'
import type { LostPet } from '@/types/models'
import ImageUploader from '@/components/common/ImageUploader.vue'

const route = useRoute()
const router = useRouter()

const pet = ref<LostPet | null>(null)
const form = ref({
  description: '',
  found_location: '',
  found_date: '',
  contact_info: '',
  photo_urls: [] as string[],
})
const loading = ref(false)

onMounted(async () => {
  const id = route.params.id as string
  const res = await lostPetsApi.getDetail(id)
  pet.value = res.data
})

async function handleSubmit() {
  if (!form.value.description || !form.value.found_location || !form.value.found_date || !form.value.contact_info) {
    ElMessage.warning('请填写所有必填字段')
    return
  }
  loading.value = true
  try {
    await foundCluesApi.submit(route.params.id as string, form.value)
    ElMessage.success('线索提交成功')
    router.push(`/lost-pets/${route.params.id}`)
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '提交失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="clue-submit-page">
    <div class="page-header">
      <h2>提交发现线索</h2>
      <p v-if="pet">为 <strong>{{ pet.pet_name }}</strong> 提交线索</p>
    </div>

    <el-card>
      <el-form :model="form" label-width="100px" label-position="top">
        <el-form-item label="发现地点" required>
          <el-input v-model="form.found_location" placeholder="请输入发现地点" />
        </el-form-item>
        <el-form-item label="发现日期" required>
          <el-date-picker v-model="form.found_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="详细描述" required>
          <el-input v-model="form.description" type="textarea" :rows="4" placeholder="请详细描述发现情况" />
        </el-form-item>
        <el-form-item label="联系方式" required>
          <el-input v-model="form.contact_info" placeholder="手机号或微信号" />
        </el-form-item>
        <el-form-item label="现场照片">
          <ImageUploader v-model="form.photo_urls" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">提交线索</el-button>
          <el-button @click="router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped>
.clue-submit-page {
  max-width: 700px;
  margin: 0 auto;
}
</style>
