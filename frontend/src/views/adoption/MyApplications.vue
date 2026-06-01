<script setup lang="ts">
import { onMounted } from 'vue'
import { useAdoptionApplicationsStore } from '@/stores/adoptionApplications'
import { applicationStatusLabels, applicationStatusTypes, formatDate } from '@/utils/format'

const store = useAdoptionApplicationsStore()

onMounted(() => {
  store.fetchMyApplications()
})

async function handleCancel(applicationId: string) {
  try {
    await ElMessageBox.confirm('确定要取消此申请吗？', '确认')
    await store.cancelApplication(applicationId)
    ElMessage.success('申请已取消')
  } catch {}
}
</script>

<template>
  <div>
    <div class="page-header">
      <h2>我的申请</h2>
    </div>

    <div class="responsive-table" style="--table-min-width: 560px">
      <el-table v-loading="store.loading" :data="store.applications" border max-height="640">
        <el-table-column label="宠物名称" min-width="120">
          <template #default="{ row }">{{ row.pet?.pet_name || '-' }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="(applicationStatusTypes[row.status] as any)" size="small">
              {{ applicationStatusLabels[row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="申请时间" width="160">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'pending'"
              type="danger"
              size="small"
              @click="handleCancel(row.application_id)"
            >
              取消
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div v-if="!store.loading && store.applications.length === 0" style="text-align: center; padding: 60px; color: #909399;">
      暂无申请记录
    </div>
  </div>
</template>
