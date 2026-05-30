<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useLostPetsStore } from '@/stores/lostPets'

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
const loading = ref(false)

async function handleSubmit() {
  if (!form.value.pet_name || !form.value.description || !form.value.lost_date || !form.value.lost_location || !form.value.contact_info) {
    ElMessage.warning('请填写所有必填字段')
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
      <el-form :model="form" label-width="100px" label-position="top">
        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="宠物名称" required>
              <el-input v-model="form.pet_name" placeholder="请输入宠物名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="宠物类型" required>
              <el-select v-model="form.pet_type" style="width: 100%">
                <el-option label="狗" value="dog" />
                <el-option label="猫" value="cat" />
                <el-option label="鸟" value="bird" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="品种">
              <el-input v-model="form.breed" placeholder="如：金毛、英短" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="毛色">
              <el-input v-model="form.color" placeholder="如：白色、棕色" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别">
              <el-select v-model="form.gender" style="width: 100%">
                <el-option label="公" value="male" />
                <el-option label="母" value="female" />
                <el-option label="未知" value="unknown" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="年龄描述">
              <el-input v-model="form.age_description" placeholder="如：约2岁" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="走失日期" required>
              <el-date-picker v-model="form.lost_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="悬赏金额">
              <el-input-number v-model="form.reward_amount" :min="0" :precision="2" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="走失地点" required>
              <el-input v-model="form.lost_location" placeholder="请输入走失地点" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="救助站">
              <el-input v-model="form.rescue_station" placeholder="请输入负责救助站" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="联系方式" required>
              <el-input v-model="form.contact_info" placeholder="手机号或微信号" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="详细描述" required>
              <el-input v-model="form.description" type="textarea" :rows="4" placeholder="请详细描述宠物特征、走失经过等" />
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
