<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { useLostPetsStore } from '@/stores/lostPets'
import ImageUploader from '@/components/common/ImageUploader.vue'

const router = useRouter()
const store = useLostPetsStore()

const form = ref({
  pet_name: '',
  pet_type: 'dog',
  breed: '',
  color: '',
  gender: 'unknown',
  age_description: '',
  description: '',
  lost_date: '',
  lost_location: '',
  rescue_station: '',
  contact_info: '',
  reward_amount: 0,
  photo_urls: [] as string[],
})
type LostPetForm = typeof form.value

const formRef = ref<FormInstance>()
const rules: FormRules<LostPetForm> = {
  pet_name: [{ required: true, message: '请输入宠物名称', trigger: 'blur' }],
  pet_type: [{ required: true, message: '请选择宠物类型', trigger: 'change' }],
  lost_date: [{ required: true, message: '请选择走失日期', trigger: 'change' }],
  lost_location: [{ required: true, message: '请输入走失地点', trigger: 'blur' }],
  contact_info: [{ required: true, message: '请输入联系方式', trigger: 'blur' }],
  description: [{ required: true, message: '请输入详细描述', trigger: 'blur' }],
}
const loading = ref(false)

async function handleSubmit() {
  const isValid = await formRef.value?.validate().catch(() => false)
  if (!isValid) {
    return
  }
  loading.value = true
  try {
    const payload = {
      ...form.value,
      rescue_station: form.value.rescue_station.trim() || undefined,
    }
    await store.publishPet(payload as any)
    ElMessage.success('发布成功')
    router.push('/lost-pets')
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '发布失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="publish-page">
    <div class="page-header">
      <h2>发布走失信息</h2>
    </div>

    <el-card>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" label-position="top">
        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="宠物名称" prop="pet_name">
              <el-input v-model="form.pet_name" placeholder="请输入宠物名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="宠物类型" prop="pet_type">
              <el-select v-model="form.pet_type" style="width: 100%">
                <el-option label="狗" value="dog" />
                <el-option label="猫" value="cat" />
                <el-option label="鸟" value="bird" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="品种" prop="breed">
              <el-input v-model="form.breed" placeholder="如：金毛、英短" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="毛色" prop="color">
              <el-input v-model="form.color" placeholder="如：白色、棕色" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="form.gender" style="width: 100%">
                <el-option label="公" value="male" />
                <el-option label="母" value="female" />
                <el-option label="未知" value="unknown" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="年龄描述" prop="age_description">
              <el-input v-model="form.age_description" placeholder="如：约2岁" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="走失日期" prop="lost_date">
              <el-date-picker v-model="form.lost_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="悬赏金额" prop="reward_amount">
              <el-input-number v-model="form.reward_amount" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="走失地点" prop="lost_location">
              <el-input v-model="form.lost_location" placeholder="请输入走失地点" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="救助站" prop="rescue_station">
              <el-input v-model="form.rescue_station" placeholder="请输入负责救助站" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="联系方式" prop="contact_info">
              <el-input v-model="form.contact_info" placeholder="手机号或微信号" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="详细描述" prop="description">
              <el-input v-model="form.description" type="textarea" :rows="4" placeholder="请详细描述宠物特征、走失经过等" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="宠物照片" prop="photo_urls">
              <ImageUploader v-model="form.photo_urls" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">发布</el-button>
          <el-button @click="router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<style scoped>
.publish-page {
  max-width: 800px;
  margin: 0 auto;
}
</style>
