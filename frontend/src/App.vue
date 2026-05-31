<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import AppHeader from '@/components/layout/AppHeader.vue'

const route = useRoute()
const isAdminRoute = computed(() => route.path.startsWith('/admin'))
</script>

<template>
  <el-config-provider :locale="zhCn">
    <div id="app">
      <AppHeader />
      <main class="main-content" :class="{ 'admin-content': isAdminRoute }">
        <router-view />
      </main>
    </div>
  </el-config-provider>
</template>

<style scoped>
.main-content {
  min-height: calc(100vh - 60px);
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.main-content.admin-content {
  padding: 0;
  max-width: none;
}
</style>
