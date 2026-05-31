<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const form = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  phone: '',
})
type RegisterForm = typeof form.value

const formRef = ref<FormInstance>()
const rules: FormRules<RegisterForm> = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] },
  ],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    {
      validator: (_rule, value, callback) => {
        if (value !== form.value.password) {
          callback(new Error('两次密码输入不一致'))
          return
        }
        callback()
      },
      trigger: ['blur', 'change'],
    },
  ],
}
const loading = ref(false)

async function handleRegister() {
  const isValid = await formRef.value?.validate().catch(() => false)
  if (!isValid) {
    return
  }
  loading.value = true
  try {
    await userStore.register({
      username: form.value.username,
      email: form.value.email,
      password: form.value.password,
      phone: form.value.phone || undefined,
    })
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '注册失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="register-page">
    <el-card class="register-card">
      <h2>用户注册</h2>
      <el-form ref="formRef" :model="form" :rules="rules" @submit.prevent="handleRegister" label-position="top">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="form.confirmPassword" type="password" placeholder="请再次输入密码" show-password />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号（选填）" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleRegister" style="width: 100%">
            注册
          </el-button>
        </el-form-item>
      </el-form>
      <div class="register-footer">
        已有账号？<router-link to="/login">立即登录</router-link>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 140px);
}

.register-card {
  width: 420px;
}

.register-card h2 {
  text-align: center;
  margin-bottom: 24px;
  color: #303133;
}

.register-footer {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
  color: #909399;
}

.register-footer a {
  color: #409eff;
}
</style>
