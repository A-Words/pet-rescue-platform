<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAdminStore } from '@/stores/admin'

const store = useAdminStore()

onMounted(async () => {
  await store.fetchDashboard()
})

const stats = [
  { key: 'active_lost_pets', label: '寻找中的走失宠物', color: '#e6a23c' },
  { key: 'available_adoptable', label: '可领养宠物', color: '#67c23a' },
  { key: 'pending_applications', label: '待审核申请', color: '#409eff' },
  { key: 'pending_clues', label: '待处理线索', color: '#f56c6c' },
  { key: 'overdue_reminders', label: '逾期回访', color: '#909399' },
]
</script>

<template>
  <div>
    <div class="page-header">
      <h2>管理仪表盘</h2>
    </div>

    <el-row :gutter="20">
      <el-col v-for="item in stats" :key="item.key" :span="4" :offset="item.key === 'active_lost_pets' ? 2 : 0">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value" :style="{ color: item.color }">
            {{ store.dashboard?.[item.key as keyof typeof store.dashboard] ?? '-' }}
          </div>
          <div class="stat-label">{{ item.label }}</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.stat-card {
  text-align: center;
  padding: 20px;
}

.stat-value {
  font-size: 36px;
  font-weight: 700;
}

.stat-label {
  margin-top: 8px;
  font-size: 14px;
  color: #909399;
}
</style>
