<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useAdminStore } from '@/stores/admin'
import { clueStatusLabels, clueStatusTypes, formatDate } from '@/utils/format'

const store = useAdminStore()
const reviewDialogVisible = ref(false)
const reviewingClueId = ref('')
const reviewForm = ref({ status: 'confirmed', admin_notes: '' })

onMounted(() => {
  store.fetchClues({ page: 1, page_size: 20 })
})

function openReview(id: string) {
  reviewingClueId.value = id
  reviewForm.value = { status: 'confirmed', admin_notes: '' }
  reviewDialogVisible.value = true
}

async function handleReview() {
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

    <el-table v-loading="store.loading" :data="store.clues" border>
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

    <el-dialog v-model="reviewDialogVisible" title="审核线索" width="500px">
      <el-form :model="reviewForm" label-width="80px">
        <el-form-item label="审核结果">
          <el-radio-group v-model="reviewForm.status">
            <el-radio value="confirmed">确认</el-radio>
            <el-radio value="rejected">拒绝</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注">
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
