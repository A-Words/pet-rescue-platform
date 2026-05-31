<script setup lang="ts">
import { ref, watch } from 'vue'
import { Plus } from '@element-plus/icons-vue'
import type { UploadProps, UploadRequestOptions, UploadUserFile } from 'element-plus'
import { uploadApi } from '@/api/upload'

const props = withDefaults(defineProps<{
  modelValue: string[]
  limit?: number
}>(), {
  limit: 6,
})

const emit = defineEmits<{
  'update:modelValue': [value: string[]]
}>()

const fileList = ref<UploadUserFile[]>([])

function toFileList(urls: string[]): UploadUserFile[] {
  return urls.map((url, index) => ({
    name: `图片${index + 1}`,
    url,
    status: 'success',
    uid: index,
  }))
}

watch(
  () => props.modelValue,
  (urls) => {
    fileList.value = toFileList(urls || [])
  },
  { immediate: true },
)

function syncUrls() {
  emit('update:modelValue', fileList.value.map((file) => file.url).filter(Boolean) as string[])
}

const beforeUpload: UploadProps['beforeUpload'] = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt5M = file.size / 1024 / 1024 < 5

  if (!isImage) {
    ElMessage.warning('只能上传图片文件')
    return false
  }
  if (!isLt5M) {
    ElMessage.warning('图片大小不能超过 5MB')
    return false
  }

  return true
}

async function uploadImage(options: UploadRequestOptions) {
  try {
    const res = await uploadApi.image(options.file)
    options.onSuccess?.(res.data)
  } catch (err) {
    options.onError?.(err as Parameters<UploadRequestOptions['onError']>[0])
  }
}

const handleSuccess: UploadProps['onSuccess'] = (response, file) => {
  file.url = response.url
  syncUrls()
}

const handleRemove: UploadProps['onRemove'] = () => {
  syncUrls()
}

const handleError: UploadProps['onError'] = () => {
  ElMessage.error('图片上传失败')
}
</script>

<template>
  <el-upload
    v-model:file-list="fileList"
    action="#"
    list-type="picture-card"
    :limit="limit"
    :before-upload="beforeUpload"
    :http-request="uploadImage"
    :on-success="handleSuccess"
    :on-remove="handleRemove"
    :on-error="handleError"
    accept="image/*"
  >
    <el-icon><Plus /></el-icon>
  </el-upload>
</template>
