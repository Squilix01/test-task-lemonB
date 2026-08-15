import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Toast {
  id: string
  title: string
  message: string
  type: 'success' | 'error' | 'info'
}

export const useToastStore = defineStore('toast', () => {
  const toasts = ref<Toast[]>([])

  function show(title: string, message: string, type: 'success' | 'error' | 'info' = 'info', duration = 4000) {
    const id = Math.random().toString(36).substring(2, 9)
    toasts.value.push({ id, title, message, type })

    setTimeout(() => {
      remove(id)
    }, duration)
  }

  function remove(id: string) {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }

  return {
    toasts,
    show,
    remove,
  }
})
