<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
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
type FoundClueForm = typeof form.value

const formRef = ref<FormInstance>()
const rules: FormRules<FoundClueForm> = {
  found_location: [{ required: true, message: '请输入发现地点', trigger: 'blur' }],
  found_date: [{ required: true, message: '请选择发现日期', trigger: 'change' }],
  description: [{ required: true, message: '请输入详细描述', trigger: 'blur' }],
  contact_info: [{ required: true, message: '请输入联系方式', trigger: 'blur' }],
}
const loading = ref(false)

onMounted(async () => {
  const id = route.params.id as string
  const res = await lostPetsApi.getDetail(id)
  pet.value = res.data
})

async function handleSubmit() {
  const isValid = await formRef.value?.validate().catch(() => false)
  if (!isValid) {
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
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" label-position="top">
        <el-form-item label="发现地点" prop="found_location">
          <el-input v-model="form.found_location" placeholder="请输入发现地点" />
        </el-form-item>
        <el-form-item label="发现日期" prop="found_date">
          <el-date-picker v-model="form.found_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="详细描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="4" placeholder="请详细描述发现情况" />
        </el-form-item>
        <el-form-item label="联系方式" prop="contact_info">
          <el-input v-model="form.contact_info" placeholder="手机号或微信号" />
        </el-form-item>
        <el-form-item label="现场照片" prop="photo_urls">
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
