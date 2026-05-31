<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { useAdminStore } from '@/stores/admin'
import { clueStatusLabels, clueStatusTypes, formatDate } from '@/utils/format'

const store = useAdminStore()
const reviewDialogVisible = ref(false)
const reviewingClueId = ref('')
const reviewForm = ref({ status: 'confirmed', admin_notes: '' })
type ReviewForm = typeof reviewForm.value

const reviewFormRef = ref<FormInstance>()
const reviewRules: FormRules<ReviewForm> = {
  status: [{ required: true, message: '请选择审核结果', trigger: 'change' }],
}

onMounted(() => {
  store.fetchClues({ page: 1, page_size: 20 })
})

function openReview(id: string) {
  reviewingClueId.value = id
  reviewForm.value = { status: 'confirmed', admin_notes: '' }
  reviewDialogVisible.value = true
}

async function handleReview() {
  const isValid = await reviewFormRef.value?.validate().catch(() => false)
  if (!isValid) {
    return
  }
  try {
    await store.reviewClue(reviewingClueId.value, reviewForm.value.status, reviewForm.value.admin_notes)
    ElMessage.success('审核成功')
    reviewDialogVisible.value = false
    store.fetchClues({ page: 1, page_size: 20 })
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '审核失败')
  }
}
</script>

<template>
  <div>
    <div class="page-header">
      <h2>线索管理</h2>
    </div>

    <div class="responsive-table" style="--table-min-width: 840px">
      <el-table v-loading="store.loading" :data="store.clues" border max-height="640">
        <el-table-column prop="found_location" label="发现地点" min-width="150" />
        <el-table-column prop="found_date" label="发现日期" width="120">
          <template #default="{ row }">{{ formatDate(row.found_date) }}</template>
        </el-table-column>
        <el-table-column prop="description" label="描述" show-overflow-tooltip min-width="200" />
        <el-table-column prop="contact_info" label="联系方式" width="140" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="(clueStatusTypes[row.status] as any)" size="small">
              {{ clueStatusLabels[row.status] }}
            </el-tag>
          </template>
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

    <el-dialog v-model="reviewDialogVisible" title="审核线索" width="500px">
      <el-form ref="reviewFormRef" :model="reviewForm" :rules="reviewRules" label-width="80px">
        <el-form-item label="审核结果" prop="status">
          <el-radio-group v-model="reviewForm.status">
            <el-radio value="confirmed">确认</el-radio>
            <el-radio value="rejected">拒绝</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="admin_notes">
          <el-input v-model="reviewForm.admin_notes" type="textarea" :rows="3" placeholder="审核备注（选填）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="reviewDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleReview">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>
