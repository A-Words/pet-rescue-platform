<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowDown } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const isLoggedIn = computed(() => userStore.isLoggedIn)
const isAdmin = computed(() => userStore.isAdmin)
const username = computed(() => userStore.user?.username || '')

function handleLogout() {
  userStore.logout()
  router.push('/login')
}
</script>

<template>
  <el-header class="app-header">
    <div class="header-left">
      <router-link to="/" class="logo">宠物救助系统</router-link>
      <el-menu mode="horizontal" :router="true" :ellipsis="false" class="nav-menu">
        <el-menu-item index="/lost-pets">走失宠物</el-menu-item>
        <el-menu-item index="/adoption">领养中心</el-menu-item>
        <el-menu-item v-if="isAdmin" index="/admin">管理后台</el-menu-item>
      </el-menu>
    </div>
    <div class="header-right">
      <template v-if="isLoggedIn">
        <el-dropdown>
          <span class="user-dropdown">
            {{ username }}
            <el-icon><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="router.push('/my/applications')">我的申请</el-dropdown-item>
              <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </template>
      <template v-else>
        <el-button type="primary" @click="router.push('/login')">登录</el-button>
        <el-button @click="router.push('/register')">注册</el-button>
      </template>
    </div>
  </el-header>
</template>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  padding: 0 20px;
  height: 60px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
  min-width: 0;
}

.logo {
  flex-shrink: 0;
  font-size: 20px;
  font-weight: 700;
  color: #409eff;
  cursor: pointer;
  white-space: nowrap;
}

.nav-menu {
  min-width: 0;
  border-bottom: none;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-dropdown {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  white-space: nowrap;
}

@media (max-width: 900px) {
  .app-header {
    gap: 12px;
    padding: 0 16px;
  }

  .header-left {
    gap: 12px;
    flex: 1;
  }

  .logo {
    font-size: 18px;
  }

  .nav-menu {
    flex: 1;
    overflow-x: auto;
    overflow-y: hidden;
  }

  .nav-menu :deep(.el-menu-item) {
    padding: 0 14px;
  }
}

@media (max-width: 560px) {
  .app-header {
    height: 56px;
    gap: 8px;
    padding: 0 12px;
  }

  .header-left {
    gap: 8px;
  }

  .logo {
    font-size: 16px;
  }

  .nav-menu :deep(.el-menu-item) {
    height: 56px;
    line-height: 56px;
    padding: 0 8px;
    font-size: 13px;
  }

  .nav-menu {
    --el-menu-horizontal-height: 56px;
    height: 56px;
  }

  .header-right {
    flex-shrink: 0;
  }

  .user-dropdown {
    font-size: 13px;
  }
}
</style>
