<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { useAdminStore } from '@/stores/admin'
import { reminderStatusLabels, reminderStatusTypes, formatDate } from '@/utils/format'

const store = useAdminStore()
const completeDialogVisible = ref(false)
const completingReminderId = ref('')
const completeForm = ref({ visit_date: '', visit_notes: '' })
type CompleteForm = typeof completeForm.value

const completeFormRef = ref<FormInstance>()
const completeRules: FormRules<CompleteForm> = {}

onMounted(() => {
  store.fetchReminders({ page: 1, page_size: 20 })
})

function openComplete(reminderId: string) {
  completingReminderId.value = reminderId
  completeForm.value = { visit_date: '', visit_notes: '' }
  completeDialogVisible.value = true
}

async function handleComplete() {
  const isValid = await completeFormRef.value?.validate().catch(() => false)
  if (!isValid) {
    return
  }
  try {
    await store.updateReminder(completingReminderId.value, {
      status: 'completed',
      visit_date: completeForm.value.visit_date,
      visit_notes: completeForm.value.visit_notes,
    })
    ElMessage.success('已标记为完成')
    completeDialogVisible.value = false
    store.fetchReminders({ page: 1, page_size: 20 })
  } catch (err: any) {
    ElMessage.error(err.response?.data?.detail || '操作失败')
  }
}
</script>

<template>
  <div>
    <div class="page-header">
      <h2>回访提醒</h2>
    </div>

    <div class="responsive-table" style="--table-min-width: 720px">
      <el-table v-loading="store.loading" :data="store.reminders" border max-height="640">
        <el-table-column prop="reminder_date" label="提醒日期" width="120">
          <template #default="{ row }">{{ formatDate(row.reminder_date) }}</template>
        </el-table-column>
        <el-table-column prop="visit_date" label="回访日期" width="120">
          <template #default="{ row }">{{ formatDate(row.visit_date) }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="(reminderStatusTypes[row.status] as any)" size="small">
              {{ reminderStatusLabels[row.status] }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="visit_notes" label="回访记录" show-overflow-tooltip min-width="200" />
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button v-if="row.status !== 'completed'" size="small" type="primary" @click="openComplete(row.reminder_id)">
              完成
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="completeDialogVisible" title="记录回访" width="500px">
      <el-form ref="completeFormRef" :model="completeForm" :rules="completeRules" label-width="80px">
        <el-form-item label="回访日期" prop="visit_date">
          <el-date-picker v-model="completeForm.visit_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="回访记录" prop="visit_notes">
          <el-input v-model="completeForm.visit_notes" type="textarea" :rows="3" placeholder="回访情况记录" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="completeDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleComplete">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>
