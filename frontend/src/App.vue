<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from '@/components/layout/AppHeader.vue'

const route = useRoute()
const isAdminRoute = computed(() => route.path.startsWith('/admin'))
</script>

<template>
  <div id="app">
    <AppHeader />
    <main class="main-content" :class="{ 'admin-content': isAdminRoute }">
      <router-view />
    </main>
  </div>
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
