import { apiClient } from './client'

export interface Product {
  id: number
  name: string
  category: string
  price: number
  rating: number
  number_of_reviews: number
  product_url: string
  image_url: string
  score: number | null
  reasoning: string | null
  trend_score: number | null
  boost_score: number | null
  created_at?: string
  updated_at?: string
}

export interface ProductListResponse {
  products?: Product[]
  items?: Product[]
  total: number
}

export interface TaskTriggerResponse {
  task_id: string
  status: string
}

export interface TaskStatusResponse {
  state: 'PENDING' | 'PROGRESS' | 'SUCCESS' | 'FAILURE'
  current: number
  total: number
  status: string
  product?: string
  title?: string
  engine?: string
  has_llm?: boolean | null
  result?: any
}

export const productsApi = {
  async getProducts(skip = 0, limit = 100, sortByScore = true): Promise<ProductListResponse> {
    const response = await apiClient.get<ProductListResponse>('/api/products', {
      params: { skip, limit, sort_by_score: sortByScore },
    })
    return response.data
  },

  async triggerScrape(): Promise<TaskTriggerResponse> {
    const response = await apiClient.post<TaskTriggerResponse>('/api/products/scrape')
    return response.data
  },

  async triggerScore(): Promise<TaskTriggerResponse> {
    const response = await apiClient.post<TaskTriggerResponse>('/api/products/score')
    return response.data
  },

  async getTaskStatus(taskId: string): Promise<TaskStatusResponse> {
    const response = await apiClient.get<TaskStatusResponse>(`/api/products/tasks/${taskId}`)
    return response.data
  },
}
