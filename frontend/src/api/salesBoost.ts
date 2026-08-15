import { apiClient } from './client'

export interface SalesHistoryItem {
  id: number
  name: string
  category: string
  keywords: string[] | string
  price: number
  number_of_sales?: number
  revenue?: number
  cost_price?: number
  margin?: number
  first_sale_date?: string
  created_at?: string
}

export interface SalesHistoryListResponse {
  items: SalesHistoryItem[]
  total: number
  skip: number
  limit: number
}

export interface CsvUploadResponse {
  status: string
  imported_count: number
}

export const salesBoostApi = {
  async getSalesHistory(skip = 0, limit = 100): Promise<SalesHistoryListResponse> {
    const response = await apiClient.get<SalesHistoryListResponse>('/api/sales-boost', {
      params: { skip, limit },
    })
    return response.data
  },

  async uploadCsv(file: File): Promise<CsvUploadResponse> {
    const formData = new FormData()
    formData.append('file', file)
    const response = await apiClient.post<CsvUploadResponse>('/api/sales-boost/csv', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  async createItem(data: {
    name: string
    category: string
    price: number
    rating?: number
    number_of_reviews?: number
    keywords?: string
    product_url?: string
    image_url?: string
  }): Promise<SalesHistoryItem> {
    const response = await apiClient.post<SalesHistoryItem>('/api/sales-boost', data)
    return response.data
  },

  async deleteItem(id: number): Promise<{ status: string }> {
    const response = await apiClient.delete<{ status: string }>(`/api/sales-boost/${id}`)
    return response.data
  },
}
