<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { useAdminStore } from '@/stores/admin'
import { applicationStatusLabels, applicationStatusTypes, formatDate } from '@/utils/format'

const store = useAdminStore()
const reviewDialogVisible = ref(false)
const reviewingAppId = ref('')
const reviewForm = ref({ decision: 'approved', review_notes: '' })
type ReviewForm = typeof reviewForm.value

const reviewFormRef = ref<FormInstance>()
const reviewRules: FormRules<ReviewForm> = {
  decision: [{ required: true, message: '请选择审核结果', trigger: 'change' }],
}

onMounted(() => {
  store.fetchApplications({ page: 1, page_size: 20 })
})

function openReview(id: string) {
  reviewingAppId.value = id
  reviewForm.value = { decision: 'approved', review_notes: '' }
  reviewDialogVisible.value = true
}

async function handleReview() {
  const isValid = await reviewFormRef.value?.validate().catch(() => false)
  if (!isValid) {
    return
  }
  try {
    await store.reviewApplication(reviewingAppId.value, reviewForm.value.decision, reviewForm.value.review_notes)
    ElMessage.success('审核完成')
    reviewDialogVisible.value = false
    store.fetchApplications({ page: 1, page_size: 20 })
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '审核失败')
  }
}
</script>

<template>
  <div>
    <div class="page-header">
      <h2>申请审核</h2>
    </div>

    <div class="responsive-table" style="--table-min-width: 1040px">
      <el-table v-loading="store.loading" :data="store.applications" border max-height="640">
        <el-table-column label="申请人" width="120">
          <template #default="{ row }">{{ row.applicant_name }}</template>
        </el-table-column>
        <el-table-column label="联系电话" width="130">
          <template #default="{ row }">{{ row.applicant_phone }}</template>
        </el-table-column>
        <el-table-column label="宠物" width="120">
          <template #default="{ row }">{{ row.pet?.pet_name || '-' }}</template>
        </el-table-column>
        <el-table-column label="住房类型" width="100">
          <template #default="{ row }">{{ row.housing_type === 'own' ? '自有' : row.housing_type === 'rent' ? '租房' : '其他' }}</template>
        </el-table-column>
        <el-table-column prop="adoption_reason" label="领养原因" show-overflow-tooltip min-width="200" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="(applicationStatusTypes[row.status] as any)" size="small">
              {{ applicationStatusLabels[row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="申请时间" width="120">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button v-if="row.status === 'pending'" size="small" type="primary" @click="openReview(row.id)">
              审核
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="reviewDialogVisible" title="审核领养申请" width="500px">
      <el-form ref="reviewFormRef" :model="reviewForm" :rules="reviewRules" label-width="80px">
        <el-form-item label="审核结果" prop="decision">
          <el-radio-group v-model="reviewForm.decision">
            <el-radio value="approved">通过</el-radio>
            <el-radio value="rejected">拒绝</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="审核备注" prop="review_notes">
          <el-input v-model="reviewForm.review_notes" type="textarea" :rows="3" placeholder="审核备注（选填）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="reviewDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleReview">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>
