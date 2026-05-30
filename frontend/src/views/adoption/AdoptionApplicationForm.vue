<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { adoptablePetsApi } from '@/api/adoptablePets'
import { useAdoptionApplicationsStore } from '@/stores/adoptionApplications'
import type { AdoptablePet } from '@/types/models'

const route = useRoute()
const router = useRouter()
const appStore = useAdoptionApplicationsStore()

const pet = ref<AdoptablePet | null>(null)
const form = ref({
  pet_id: '',
  applicant_name: '',
  applicant_phone: '',
  applicant_address: '',
  applicant_id_number: '',
  housing_type: 'own',
  has_other_pets: false,
  adoption_reason: '',
  experience_description: '',
})
const loading = ref(false)

onMounted(async () => {
  const id = route.params.id as string
  form.value.pet_id = id
  const res = await adoptablePetsApi.getDetail(id)
  pet.value = res.data
})

async function handleSubmit() {
  if (!form.value.applicant_name || !form.value.applicant_phone || !form.value.applicant_address || !form.value.applicant_id_number || !form.value.adoption_reason) {
    ElMessage.warning('请填写所有必填字段')
    return
  }
  loading.value = true
  try {
    await appStore.submitApplication(form.value)
    ElMessage.success('申请提交成功')
    router.push('/my/applications')
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '提交失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="apply-page">
    <div class="page-header">
      <h2>领养申请</h2>
      <p v-if="pet">申请领养：{{ pet.pet_name }}</p>
    </div>

    <el-card>
      <el-form :model="form" label-width="120px" label-position="top">
        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="姓名" required>
              <el-input v-model="form.applicant_name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="手机号" required>
              <el-input v-model="form.applicant_phone" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="住址" required>
              <el-input v-model="form.applicant_address" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="身份证号" required>
              <el-input v-model="form.applicant_id_number" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="住房类型">
              <el-select v-model="form.housing_type" style="width: 100%">
                <el-option label="自有住房" value="own" />
                <el-option label="租房" value="rent" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="是否已有宠物">
              <el-switch v-model="form.has_other_pets" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="领养原因" required>
              <el-input v-model="form.adoption_reason" type="textarea" :rows="3" placeholder="请说明您的领养原因" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="养宠经验">
              <el-input v-model="form.experience_description" type="textarea" :rows="3" placeholder="请描述您的养宠经验（选填）" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">提交申请</el-button>
          <el-button @click="router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped>
.apply-page {
  max-width: 800px;
  margin: 0 auto;
}
</style>
