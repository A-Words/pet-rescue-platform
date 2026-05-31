<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAdminStore } from '@/stores/admin'

const store = useAdminStore()

const now = new Date()
const year = ref(new Date(now.getFullYear(), 0, 1))
const month = ref(now.getMonth() + 1)
const rescueStation = ref('')

onMounted(() => {
  loadStats()
})

function loadStats() {
  store.fetchStatistics(year.value.getFullYear(), month.value, rescueStation.value.trim())
}

function handleFilterChange() {
  loadStats()
}
</script>

<template>
  <div>
    <div class="page-header">
      <h2>数据统计</h2>
    </div>

    <div class="filter-bar">
      <el-date-picker
        v-model="year"
        type="year"
        placeholder="选择年份"
        @change="handleFilterChange"
        style="width: 120px"
      />
      <el-select v-model="month" @change="handleFilterChange" style="width: 100px">
        <el-option v-for="m in 12" :key="m" :label="`${m}月`" :value="m" />
      </el-select>
      <el-input
        v-model="rescueStation"
        placeholder="救助站"
        clearable
        @change="handleFilterChange"
        @clear="handleFilterChange"
        style="width: 180px"
      />
    </div>

    <div class="stats-grid" v-if="store.statistics">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ store.statistics.total_lost_reports }}</div>
          <div class="stat-label">走失上报总数</div>
        </el-card>
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value" style="color: #67c23a">{{ store.statistics.successful_recoveries }}</div>
          <div class="stat-label">成功找回数</div>
        </el-card>
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value" style="color: #409eff">{{ store.statistics.recovery_rate }}%</div>
          <div class="stat-label">找回率</div>
        </el-card>
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value" style="color: #e6a23c">{{ store.statistics.total_found_clues }}</div>
          <div class="stat-label">线索总数</div>
        </el-card>
    </div>

    <div class="stats-grid stats-grid-secondary" v-if="store.statistics">
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value">{{ store.statistics.total_adoption_applications }}</div>
          <div class="stat-label">领养申请总数</div>
        </el-card>
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value" style="color: #67c23a">{{ store.statistics.approved_adoptions }}</div>
          <div class="stat-label">通过申请数</div>
        </el-card>
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value" style="color: #409eff">{{ store.statistics.adoption_success_rate }}%</div>
          <div class="stat-label">领养成功率</div>
        </el-card>
        <el-card class="stat-card" shadow="hover">
          <div class="stat-value" style="color: #67c23a">{{ store.statistics.confirmed_clues }}</div>
          <div class="stat-label">确认线索数</div>
        </el-card>
    </div>
  </div>
</template>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 20px;
}

.stats-grid-secondary {
  margin-top: 20px;
}

@media (max-width: 560px) {
  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
  }
}
</style>
