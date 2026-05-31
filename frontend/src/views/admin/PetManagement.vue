<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { adoptablePetsApi } from '@/api/adoptablePets'
import type { AdoptablePet } from '@/types/models'
import { petTypeLabels, healthStatusLabels, formatDate } from '@/utils/format'
import ImageUploader from '@/components/common/ImageUploader.vue'

const pets = ref<AdoptablePet[]>([])
const total = ref(0)
const loading = ref(false)
const page = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const editingPet = ref<Partial<AdoptablePet>>({})
const isEdit = ref(false)

const form = ref({
  pet_name: '',
  pet_type: 'dog',
  breed: '',
  color: '',
  gender: 'unknown',
  age_months: null as number | null,
  description: '',
  health_status: 'healthy',
  is_vaccinated: false,
  is_dewormed: false,
  is_sterilized: false,
  rescue_station: '',
  intake_date: '',
  photo_urls: [] as string[],
})
type PetForm = typeof form.value

const formRef = ref<FormInstance>()
const rules: FormRules<PetForm> = {
  pet_name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
  intake_date: [{ required: true, message: '请选择入站日期', trigger: 'change' }],
}

onMounted(() => {
  loadPets()
})

async function loadPets() {
  loading.value = true
  try {
    const res = await adoptablePetsApi.list({ page: page.value, page_size: pageSize.value })
    pets.value = res.data.items
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

function openAdd() {
  isEdit.value = false
  form.value = {
    pet_name: '', pet_type: 'dog' as const, breed: '', color: '', gender: 'unknown' as const,
    age_months: null, description: '', health_status: 'healthy' as const,
    is_vaccinated: false, is_dewormed: false, is_sterilized: false,
    rescue_station: '', intake_date: '', photo_urls: [],
  }
  dialogVisible.value = true
  formRef.value?.clearValidate()
}

function openEdit(pet: AdoptablePet) {
  isEdit.value = true
  editingPet.value = pet
  form.value = {
    pet_name: pet.pet_name,
    pet_type: pet.pet_type || 'dog',
    breed: pet.breed || '',
    color: pet.color || '',
    gender: pet.gender || 'unknown',
    age_months: pet.age_months ?? null,
    description: pet.description || '',
    health_status: pet.health_status || 'healthy',
    is_vaccinated: pet.is_vaccinated,
    is_dewormed: pet.is_dewormed,
    is_sterilized: pet.is_sterilized,
    rescue_station: pet.rescue_station || '',
    intake_date: pet.intake_date,
    photo_urls: pet.photo_urls || [],
  }
  dialogVisible.value = true
  formRef.value?.clearValidate()
}

async function handleSave() {
  const isValid = await formRef.value?.validate().catch(() => false)
  if (!isValid) {
    return
  }
  try {
    if (isEdit.value && editingPet.value.id) {
      await adoptablePetsApi.update(editingPet.value.id, form.value as any)
      ElMessage.success('更新成功')
    } else {
      await adoptablePetsApi.create(form.value as any)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    loadPets()
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '操作失败')
  }
}

async function handleDelete(id: string) {
  try {
    await ElMessageBox.confirm('确定要删除此宠物吗？', '确认')
    await adoptablePetsApi.delete(id)
    ElMessage.success('删除成功')
    loadPets()
  } catch {}
}
</script>

<template>
  <div>
    <div class="page-header">
      <el-row justify="space-between" align="middle">
        <el-col :xs="24" :sm="12"><h2>宠物管理</h2></el-col>
        <el-col :xs="24" :sm="12" class="page-actions">
          <el-button type="primary" @click="openAdd">添加宠物</el-button>
        </el-col>
      </el-row>
    </div>

    <div class="responsive-table" style="--table-min-width: 960px">
      <el-table v-loading="loading" :data="pets" border max-height="640">
        <el-table-column prop="pet_name" label="名称" width="120" />
        <el-table-column label="类型" width="80">
          <template #default="{ row }">{{ petTypeLabels[row.pet_type] }}</template>
        </el-table-column>
        <el-table-column prop="breed" label="品种" width="120" />
        <el-table-column label="健康状态" width="100">
          <template #default="{ row }">{{ healthStatusLabels[row.health_status] }}</template>
        </el-table-column>
        <el-table-column label="疫苗" width="70">
          <template #default="{ row }">
            <el-tag :type="row.is_vaccinated ? 'success' : 'info'" size="small">
              {{ row.is_vaccinated ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="驱虫" width="70">
          <template #default="{ row }">
            <el-tag :type="row.is_dewormed ? 'success' : 'info'" size="small">
              {{ row.is_dewormed ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="入站日期" width="120">
          <template #default="{ row }">{{ formatDate(row.intake_date) }}</template>
        </el-table-column>
        <el-table-column prop="adoption_status" label="状态" width="100" />
        <el-table-column label="操作" width="160">
          <template #default="{ row }">
            <el-button size="small" @click="openEdit(row as AdoptablePet)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div v-if="total > pageSize" style="margin-top: 16px; display: flex; justify-content: center;">
      <el-pagination :current-page="page" :page-size="pageSize" :total="total" layout="prev, pager, next"
        @current-change="(p: number) => { page = p; loadPets() }" />
    </div>

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑宠物' : '添加宠物'"
      width="min(600px, calc(100vw - 24px))"
      class="pet-form-dialog"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px" label-position="top">
        <el-row :gutter="16">
          <el-col :xs="24" :sm="12">
            <el-form-item label="名称" prop="pet_name"><el-input v-model="form.pet_name" /></el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-form-item label="类型" prop="pet_type">
              <el-select v-model="form.pet_type" style="width: 100%">
                <el-option label="狗" value="dog" /><el-option label="猫" value="cat" />
                <el-option label="鸟" value="bird" /><el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-form-item label="品种" prop="breed"><el-input v-model="form.breed" /></el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-form-item label="颜色" prop="color"><el-input v-model="form.color" /></el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="form.gender" style="width: 100%">
                <el-option label="公" value="male" /><el-option label="母" value="female" />
                <el-option label="未知" value="unknown" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-form-item label="年龄(月)" prop="age_months"><el-input-number v-model="form.age_months" :min="0" style="width: 100%" /></el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-form-item label="健康状态" prop="health_status">
              <el-select v-model="form.health_status" style="width: 100%">
                <el-option label="健康" value="healthy" /><el-option label="治疗中" value="treating" />
                <el-option label="慢性病" value="chronic" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-form-item label="入站日期" prop="intake_date">
              <el-date-picker v-model="form.intake_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :xs="12" :sm="8">
            <el-form-item label="已疫苗" prop="is_vaccinated"><el-switch v-model="form.is_vaccinated" /></el-form-item>
          </el-col>
          <el-col :xs="12" :sm="8">
            <el-form-item label="已驱虫" prop="is_dewormed"><el-switch v-model="form.is_dewormed" /></el-form-item>
          </el-col>
          <el-col :xs="12" :sm="8">
            <el-form-item label="已绝育" prop="is_sterilized"><el-switch v-model="form.is_sterilized" /></el-form-item>
          </el-col>
          <el-col :xs="24">
            <el-form-item label="救助站" prop="rescue_station"><el-input v-model="form.rescue_station" /></el-form-item>
          </el-col>
          <el-col :xs="24">
            <el-form-item label="描述" prop="description"><el-input v-model="form.description" type="textarea" :rows="3" /></el-form-item>
          </el-col>
          <el-col :xs="24">
            <el-form-item label="宠物照片" prop="photo_urls"><ImageUploader v-model="form.photo_urls" /></el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.page-actions {
  text-align: right;
}

:deep(.pet-form-dialog .el-dialog__body) {
  max-height: min(70vh, 680px);
  overflow-y: auto;
}

@media (max-width: 560px) {
  :deep(.pet-form-dialog) {
    margin-top: 12px;
    margin-bottom: 12px;
  }

  :deep(.pet-form-dialog .el-dialog__header),
  :deep(.pet-form-dialog .el-dialog__body),
  :deep(.pet-form-dialog .el-dialog__footer) {
    padding-left: 16px;
    padding-right: 16px;
  }

  :deep(.pet-form-dialog .el-dialog__footer) {
    display: flex;
    gap: 12px;
  }

  :deep(.pet-form-dialog .el-dialog__footer .el-button) {
    flex: 1;
    margin-left: 0;
  }

  .page-actions {
    margin-top: 12px;
    text-align: left;
  }
}
</style>
