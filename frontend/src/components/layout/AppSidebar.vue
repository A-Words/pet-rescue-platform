<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const menuItems = [
  { index: '/admin', label: '仪表盘', icon: 'Odometer' },
  { index: '/admin/pets', label: '宠物管理', icon: 'House' },
  { index: '/admin/clues', label: '线索管理', icon: 'Search' },
  { index: '/admin/applications', label: '申请审核', icon: 'Document' },
  { index: '/admin/statistics', label: '数据统计', icon: 'DataAnalysis' },
  { index: '/admin/reminders', label: '回访提醒', icon: 'Bell' },
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
  margin: -20px;
}

.admin-sidebar {
  background: #fff;
  border-right: 1px solid #e4e7ed;
}

.sidebar-menu {
  border-right: none;
  padding-top: 10px;
}

.admin-main {
  flex: 1;
  padding: 20px;
  background: #f5f7fa;
}
</style>
