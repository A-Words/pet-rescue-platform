export interface ApiResponse<T> {
  data: T
}

export interface ApiError {
  detail: string
}
