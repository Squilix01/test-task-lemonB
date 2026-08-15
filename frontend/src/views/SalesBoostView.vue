<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSalesBoostStore } from '@/stores/salesBoost'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import AppNavbar from '@/components/layout/AppNavbar.vue'
import CsvDropzone from '@/components/sales-boost/CsvDropzone.vue'
import SalesHistoryTable from '@/components/sales-boost/SalesHistoryTable.vue'
import AddSalesItemModal from '@/components/sales-boost/AddSalesItemModal.vue'
import { TrendingUp, RefreshCw, Plus } from 'lucide-vue-next'

const salesBoostStore = useSalesBoostStore()
const showAddModal = ref(false)

onMounted(() => {
  salesBoostStore.fetchSalesHistory()
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
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 class="text-2xl font-bold text-white tracking-tight">Sales Boost — Історія продажів</h1>
            <p class="text-xs text-slate-400 mt-1">
              База успішних кейсів нашої компанії для автоматичного донарахування бонусних балів до AI-скорингу новинок
            </p>
          </div>

          <button
            @click="showAddModal = true"
            class="px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold transition-all shadow-lg shadow-emerald-600/20 flex items-center gap-2 shrink-0 self-start sm:self-auto"
          >
            <Plus class="w-4 h-4" />
            <span>Додати товар вручну</span>
          </button>
        </div>

        <!-- 1. CSV Dropzone Box -->
        <CsvDropzone />

        <!-- 2. Loading State -->
        <div v-if="salesBoostStore.isLoading" class="p-8 text-center">
          <RefreshCw class="w-6 h-6 text-emerald-400 animate-spin mx-auto mb-2" />
          <p class="text-xs font-medium text-slate-400">Оновлення бази історії...</p>
        </div>

        <!-- 3. Sales History Table -->
        <SalesHistoryTable
          v-else
          :items="salesBoostStore.items"
          @delete="salesBoostStore.deleteItem"
        />
      </main>
    </div>

    <!-- Manual Add Product Modal -->
    <AddSalesItemModal
      v-if="showAddModal"
      @close="showAddModal = false"
    />
  </div>
</template>
