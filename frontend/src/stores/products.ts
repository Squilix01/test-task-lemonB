import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { productsApi, type Product } from '@/api/products'
import { useToastStore } from './toast'

export interface ActiveTaskState {
  id: string
  type: 'scrape' | 'score'
  title: string
  progress: number
  statusText: string
  currentProduct?: string
  logs: string[]
  isDone: boolean
  isError: boolean
}

export const useProductsStore = defineStore('products', () => {
  const toast = useToastStore()

  const products = ref<Product[]>([])
  const total = ref(0)
  const isLoading = ref(false)
  const isScraping = ref(false)
  const isScoring = ref(false)
  const activeTask = ref<ActiveTaskState | null>(null)

  // Filters & display state
  const searchQuery = ref('')
  const selectedCategory = ref('all')
  const minScore = ref(0)
  const viewMode = ref<'grid' | 'table'>('grid')
  const selectedProductForModal = ref<Product | null>(null)

  const categories = computed(() => {
    const list = Array.isArray(products.value) ? products.value : []
    const set = new Set<string>()
    list.forEach((p) => {
      if (p && p.category) set.add(p.category)
    })
    return ['all', ...Array.from(set)]
  })

  const filteredProducts = computed(() => {
    const list = Array.isArray(products.value) ? products.value : []
    return list.filter((p) => {
      if (!p) return false
      const matchesSearch =
        !searchQuery.value ||
        (p.name && p.name.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
        (p.category && p.category.toLowerCase().includes(searchQuery.value.toLowerCase()))

      const matchesCategory =
        selectedCategory.value === 'all' || p.category === selectedCategory.value

      const matchesScore =
        minScore.value === 0 || (p.score !== null && p.score >= minScore.value)

      return matchesSearch && matchesCategory && matchesScore
    })
  })

  const stats = computed(() => {
    const list = Array.isArray(products.value) ? products.value : []
    const totalCount = list.length
    const scoredCount = list.filter((p) => p && p.score !== null).length
    const topScoredCount = list.filter((p) => p && (p.score || 0) >= 75).length
    const avgScore =
      scoredCount > 0
        ? Math.round(
            list.reduce((acc, p) => acc + (p.score || 0), 0) / scoredCount
          )
        : 0

    return {
      totalCount,
      scoredCount,
      topScoredCount,
      avgScore,
    }
  })

  async function fetchProducts() {
    isLoading.value = true
    try {
      const data = await productsApi.getProducts(0, 100, true)
      products.value = data.products || data.items || []
      total.value = data.total || products.value.length
    } catch (err: any) {
      toast.show('Помилка', 'Не вдалося завантажити список товарів', 'error')
    } finally {
      isLoading.value = false
    }
  }

  function addLog(msg: string) {
    if (!activeTask.value) return
    const time = new Date().toLocaleTimeString('uk-UA')
    activeTask.value.logs.push(`[${time}] ${msg}`)
  }

  async function pollTask(taskId: string, type: 'scrape' | 'score') {
    const interval = setInterval(async () => {
      try {
        const res = await productsApi.getTaskStatus(taskId)
        if (!activeTask.value || activeTask.value.id !== taskId) {
          clearInterval(interval)
          return
        }

        if (res.title) {
          activeTask.value.title = res.title
        }

        const pct = res.total > 0 ? Math.min(100, Math.round((res.current / res.total) * 100)) : 0
        activeTask.value.progress = pct
        activeTask.value.statusText = res.status
        activeTask.value.currentProduct = res.product

        if (res.status && !activeTask.value.logs.some((l) => l.includes(res.status))) {
          addLog(res.status)
        }

        if (res.state === 'SUCCESS') {
          clearInterval(interval)
          activeTask.value.isDone = true
          activeTask.value.progress = 100
          addLog('Успішно завершено!')
          toast.show('Готово', type === 'scrape' ? 'Парсинг товарів успішно завершено!' : 'Скоринг товарів завершено!', 'success')
          if (type === 'scrape') isScraping.value = false
          if (type === 'score') isScoring.value = false
          await fetchProducts()
        } else if (res.state === 'FAILURE') {
          clearInterval(interval)
          activeTask.value.isError = true
          addLog(`Помилка: ${res.status}`)
          toast.show('Помилка', `Задача завершилась з помилкою: ${res.status}`, 'error')
          if (type === 'scrape') isScraping.value = false
          if (type === 'score') isScoring.value = false
        }
      } catch (err) {
        // network or auth error during polling
      }
    }, 1200)
  }

  async function triggerScrape() {
    isScraping.value = true
    try {
      const res = await productsApi.triggerScrape()
      activeTask.value = {
        id: res.task_id,
        type: 'scrape',
        title: 'Парсинг Amazon Best Sellers',
        progress: 10,
        statusText: 'Запуск Playwright воркера...',
        logs: [`[${new Date().toLocaleTimeString('uk-UA')}] Запуск задачі парсингу Amazon Best Sellers...`],
        isDone: false,
        isError: false,
      }
      pollTask(res.task_id, 'scrape')
    } catch (err: any) {
      toast.show('Помилка', 'Не вдалося запустити парсинг', 'error')
      isScraping.value = false
    }
  }

  async function triggerScore() {
    isScoring.value = true
    try {
      const res = await productsApi.triggerScore()
      activeTask.value = {
        id: res.task_id,
        type: 'score',
        title: 'Скоринг товарів...',
        progress: 5,
        statusText: 'Підготовка аналізу...',
        logs: [`[${new Date().toLocaleTimeString('uk-UA')}] Запуск оцінювання потенціалу товарів...`],
        isDone: false,
        isError: false,
      }
      pollTask(res.task_id, 'score')
    } catch (err: any) {
      toast.show('Помилка', 'Не вдалося запустити скоринг', 'error')
      isScoring.value = false
    }
  }

  function dismissTask() {
    activeTask.value = null
  }

  function openScoreModal(product: Product) {
    selectedProductForModal.value = product
  }

  function closeScoreModal() {
    selectedProductForModal.value = null
  }

  return {
    products,
    total,
    isLoading,
    isScraping,
    isScoring,
    activeTask,
    searchQuery,
    selectedCategory,
    minScore,
    viewMode,
    categories,
    filteredProducts,
    stats,
    selectedProductForModal,
    fetchProducts,
    triggerScrape,
    triggerScore,
    dismissTask,
    openScoreModal,
    closeScoreModal,
  }
})
