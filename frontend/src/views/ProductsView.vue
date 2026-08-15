<script setup lang="ts">
import { onMounted } from 'vue'
import { useProductsStore } from '@/stores/products'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import AppNavbar from '@/components/layout/AppNavbar.vue'
import StatsOverview from '@/components/products/StatsOverview.vue'
import ProductFilters from '@/components/products/ProductFilters.vue'
import ProductCard from '@/components/products/ProductCard.vue'
import ProductTable from '@/components/products/ProductTable.vue'
import ProductScoreModal from '@/components/products/ProductScoreModal.vue'
import LiveTaskProgress from '@/components/ui/LiveTaskProgress.vue'
import { Sparkles, ShoppingBag, RefreshCw } from 'lucide-vue-next'

const productsStore = useProductsStore()

onMounted(() => {
  productsStore.fetchProducts()
})
</script>

<template>
  <div class="flex h-screen overflow-hidden bg-slate-950">
    <!-- Sidebar -->
    <AppSidebar />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col min-w-0 overflow-hidden">
      <AppNavbar />

      <main class="flex-1 overflow-y-auto p-6 space-y-6">
        <!-- Page Title & Header -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h1 class="text-2xl font-bold text-white tracking-tight">Аналітика товарів Amazon</h1>
            <p class="text-xs text-slate-400 mt-1">
              Рейтинг перспективності товарів на основі Best Sellers, Google Trends та AI
            </p>
          </div>
        </div>

        <!-- 0. Live Real-time Task Progress & Debug Terminal -->
        <LiveTaskProgress />

        <!-- 1. Stats Overview Cards -->
        <StatsOverview />

        <!-- 2. Filters & Actions Bar -->
        <ProductFilters />

        <!-- 3. Loading State -->
        <div v-if="productsStore.isLoading" class="p-12 text-center">
          <RefreshCw class="w-8 h-8 text-emerald-400 animate-spin mx-auto mb-3" />
          <p class="text-sm font-medium text-slate-300">Завантаження аналітичних даних...</p>
        </div>

        <!-- 4. Empty State -->
        <div
          v-else-if="productsStore.filteredProducts.length === 0"
          class="p-12 rounded-2xl bg-slate-900/40 border border-slate-800 text-center max-w-md mx-auto"
        >
          <div class="w-12 h-12 rounded-2xl bg-slate-800 text-slate-400 flex items-center justify-center mx-auto mb-3">
            <ShoppingBag class="w-6 h-6" />
          </div>
          <h3 class="text-base font-bold text-white">Товарів не знайдено</h3>
          <p class="text-xs text-slate-400 mt-1 mb-4">
            Спробуйте змінити фільтри або запустіть парсинг нових товарів з Amazon Best Sellers.
          </p>
          <button
            @click="productsStore.triggerScrape"
            class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-xs transition-colors"
          >
            Спарсити Amazon
          </button>
        </div>

        <!-- 5. Content Views -->
        <div v-else>
          <!-- Grid View -->
          <div
            v-if="productsStore.viewMode === 'grid'"
            class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 2xl:grid-cols-5 gap-5"
          >
            <ProductCard
              v-for="product in productsStore.filteredProducts"
              :key="product.id"
              :product="product"
              @inspect="productsStore.openScoreModal"
            />
          </div>

          <!-- Table View -->
          <div v-else>
            <ProductTable
              :products="productsStore.filteredProducts"
              @inspect="productsStore.openScoreModal"
            />
          </div>
        </div>
      </main>
    </div>

    <!-- AI Score Breakdown Modal -->
    <ProductScoreModal
      :product="productsStore.selectedProductForModal"
      @close="productsStore.closeScoreModal"
    />
  </div>
</template>
