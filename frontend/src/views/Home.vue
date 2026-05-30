<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<template>
  <div class="home">
    <div class="hero">
      <h1>宠物走失找回与领养救助平台</h1>
      <p>帮助走失宠物回家，为流浪动物寻找温暖的家</p>
      <div class="hero-actions">
        <el-button type="primary" size="large" @click="router.push('/lost-pets')">
          查看走失宠物
        </el-button>
        <el-button size="large" @click="router.push('/adoption')">
          浏览领养中心
        </el-button>
      </div>
    </div>

    <div class="features">
      <el-row :gutter="24">
        <el-col :span="8">
          <el-card class="feature-card">
            <h3>发布走失信息</h3>
            <p>快速发布宠物走失信息，上传照片和描述，让更多人帮助寻找</p>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="feature-card">
            <h3>提交发现线索</h3>
            <p>发现疑似走失宠物时，提交线索帮助宠物主人找回爱宠</p>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="feature-card">
            <h3>领养救助宠物</h3>
            <p>浏览待领养宠物信息，提交领养申请，给流浪动物一个家</p>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<style scoped>
.home {
  max-width: 100%;
}

.hero {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #409eff 0%, #53a8ff 100%);
  border-radius: 12px;
  color: #fff;
  margin-bottom: 40px;
}

.hero h1 {
  font-size: 36px;
  margin-bottom: 12px;
}

.hero p {
  font-size: 18px;
  opacity: 0.9;
  margin-bottom: 30px;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.features {
  max-width: 900px;
  margin: 0 auto;
}

.feature-card {
  text-align: center;
  height: 100%;
}

.feature-card h3 {
  font-size: 20px;
  margin-bottom: 12px;
  color: #409eff;
}

.feature-card p {
  color: #606266;
  line-height: 1.6;
}
</style>
