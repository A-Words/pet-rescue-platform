export const petTypeLabels: Record<string, string> = {
  dog: '狗',
  cat: '猫',
  bird: '鸟',
  other: '其他',
}

export const genderLabels: Record<string, string> = {
  male: '公',
  female: '母',
  unknown: '未知',
}

export const lostPetStatusLabels: Record<string, string> = {
  active: '寻找中',
  found: '已找回',
  closed: '已关闭',
}

export const lostPetStatusTypes: Record<string, string> = {
  active: 'warning',
  found: 'success',
  closed: 'info',
}

export const clueStatusLabels: Record<string, string> = {
  pending: '待审核',
  confirmed: '已确认',
  rejected: '已拒绝',
}

export const clueStatusTypes: Record<string, string> = {
  pending: 'warning',
  confirmed: 'success',
  rejected: 'danger',
}

export const applicationStatusLabels: Record<string, string> = {
  pending: '待审核',
  approved: '已通过',
  rejected: '已拒绝',
  cancelled: '已取消',
}

export const applicationStatusTypes: Record<string, string> = {
  pending: 'warning',
  approved: 'success',
  rejected: 'danger',
  cancelled: 'info',
}

export const healthStatusLabels: Record<string, string> = {
  healthy: '健康',
  treating: '治疗中',
  chronic: '慢性病',
}

export const reminderStatusLabels: Record<string, string> = {
  pending: '待回访',
  completed: '已完成',
  overdue: '已逾期',
}

export const reminderStatusTypes: Record<string, string> = {
  pending: 'warning',
  completed: 'success',
  overdue: 'danger',
}

export function formatDate(date: string | undefined): string {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

export function formatDateTime(date: string | undefined): string {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN')
}
