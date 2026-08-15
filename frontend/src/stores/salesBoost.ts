import { defineStore } from 'pinia'
import { ref } from 'vue'
import { salesBoostApi, type SalesHistoryItem } from '@/api/salesBoost'
import { useToastStore } from './toast'

export const useSalesBoostStore = defineStore('salesBoost', () => {
  const toast = useToastStore()

  const items = ref<SalesHistoryItem[]>([])
  const total = ref(0)
  const isLoading = ref(false)
  const isUploading = ref(false)

  async function fetchSalesHistory() {
    isLoading.value = true
    try {
      const data = await salesBoostApi.getSalesHistory(0, 100)
      items.value = data.items || []
      total.value = data.total || items.value.length
    } catch {
      toast.show('Помилка', 'Не вдалося завантажити історію продажів', 'error')
    } finally {
      isLoading.value = false
    }
  }

  async function uploadCsv(file: File) {
    isUploading.value = true
    try {
      const res = await salesBoostApi.uploadCsv(file)
      toast.show('Успішно', `Імпортовано ${res.imported_count} записів з CSV файлу!`, 'success')
      await fetchSalesHistory()
      return true
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Не вдалося обробити CSV файл'
      toast.show('Помилка імпорту', msg, 'error')
      return false
    } finally {
      isUploading.value = false
    }
  }

  async function createItem(payload: {
    name: string
    category: string
    price: number
    rating?: number
    number_of_reviews?: number
    keywords?: string
    product_url?: string
    image_url?: string
  }) {
    isLoading.value = true
    try {
      const newItem = await salesBoostApi.createItem(payload)
      items.value.unshift(newItem)
      total.value += 1
      toast.show('Успішно додано', `Товар "${newItem.name.slice(0, 30)}..." додано в базу Sales Boost!`, 'success')
      return true
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Не вдалося створити запис'
      toast.show('Помилка', msg, 'error')
      return false
    } finally {
      isLoading.value = false
    }
  }

  async function deleteItem(id: number) {
    try {
      await salesBoostApi.deleteItem(id)
      items.value = items.value.filter((item) => item.id !== id)
      total.value = Math.max(0, total.value - 1)
      toast.show('Видалено', 'Запис успішно видалено з бази Sales Boost', 'info')
    } catch {
      toast.show('Помилка', 'Не вдалося видалити запис', 'error')
    }
  }

  return {
    items,
    total,
    isLoading,
    isUploading,
    fetchSalesHistory,
    uploadCsv,
    createItem,
    deleteItem,
  }
})
