<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { Bell, DataAnalysis, Document, House, Odometer, Search } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

const menuItems = [
  { index: '/admin', label: '仪表盘', icon: Odometer },
  { index: '/admin/pets', label: '宠物管理', icon: House },
  { index: '/admin/clues', label: '线索管理', icon: Search },
  { index: '/admin/applications', label: '申请审核', icon: Document },
  { index: '/admin/statistics', label: '数据统计', icon: DataAnalysis },
  { index: '/admin/reminders', label: '回访提醒', icon: Bell },
]
</script>

<template>
  <div class="admin-layout">
    <el-aside width="220px" class="admin-sidebar">
      <el-menu
        :default-active="route.path"
        :router="true"
        class="sidebar-menu"
      >
        <el-menu-item
          v-for="item in menuItems"
          :key="item.index"
          :index="item.index"
        >
          <el-icon><component :is="item.icon" /></el-icon>
          <span>{{ item.label }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-main class="admin-main">
      <router-view />
    </el-main>
  </div>
</template>

<style scoped>
.admin-layout {
  display: flex;
  min-height: calc(100vh - 60px);
}

.admin-sidebar {
  background: #fff;
  border-right: 1px solid #e4e7ed;
  box-shadow: 1px 0 4px rgba(0, 0, 0, 0.03);
}

.sidebar-menu {
  border-right: none;
  padding: 12px;
}

.sidebar-menu :deep(.el-menu-item) {
  height: 44px;
  margin-bottom: 4px;
  border-radius: 6px;
  color: #606266;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background: #ecf5ff;
  color: #409eff;
  font-weight: 600;
}

.admin-main {
  flex: 1;
  min-width: 0;
  padding: 24px;
  background: #f5f7fa;
}

@media (max-width: 900px) {
  .admin-layout {
    flex-direction: column;
    overflow-x: hidden;
  }

  .admin-sidebar {
    width: 100% !important;
    border-right: none;
    border-bottom: 1px solid #e4e7ed;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
  }

  .sidebar-menu {
    display: flex;
    gap: 8px;
    width: 100%;
    max-width: 100vw;
    overflow-x: auto;
    overflow-y: hidden;
    padding: 6px 12px;
    scrollbar-width: none;
  }

  .sidebar-menu::-webkit-scrollbar {
    display: none;
  }

  .sidebar-menu :deep(.el-menu-item) {
    flex: 0 0 auto;
    height: 40px;
    margin-bottom: 0;
    padding: 0 14px;
  }

  .admin-main {
    padding: 20px;
  }
}

@media (max-width: 560px) {
  .admin-main {
    padding: 16px 12px;
  }
}
</style>
