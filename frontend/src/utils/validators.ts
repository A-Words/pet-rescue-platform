export const required = { required: true, message: '此字段为必填项', trigger: 'blur' }

export const email = { type: 'email' as const, message: '请输入有效的邮箱地址', trigger: 'blur' }

export const phone = {
  pattern: /^1[3-9]\d{9}$/,
  message: '请输入有效的手机号',
  trigger: 'blur',
}
