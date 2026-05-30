<script setup lang="ts">
import AppHeader from '@/components/layout/AppHeader.vue'
</script>

<template>
  <div id="app">
    <AppHeader />
    <main class="main-content">
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
</style>
