<script setup lang="ts">
import { useProductsStore } from '@/stores/products'
import { Search, SlidersHorizontal, LayoutGrid, Table, Play, Sparkles, RefreshCw } from 'lucide-vue-next'

const productsStore = useProductsStore()
</script>

<template>
  <div class="p-4 rounded-2xl bg-slate-900/60 border border-slate-800/80 flex flex-col lg:flex-row items-stretch lg:items-center justify-between gap-4">
    <!-- Search and filters -->
    <div class="flex flex-wrap items-center gap-3 flex-1">
      <!-- Search input -->
      <div class="relative min-w-[240px] flex-1 max-w-md">
        <Search class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
        <input
          v-model="productsStore.searchQuery"
          type="text"
          placeholder="Пошук за назвою або категорією..."
          class="w-full pl-10 pr-4 py-2 rounded-xl bg-slate-800/60 border border-slate-700/60 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/30 transition-all"
        />
      </div>

      <!-- Category Selector -->
      <div class="relative min-w-[180px]">
        <select
          v-model="productsStore.selectedCategory"
          class="w-full px-3.5 py-2 rounded-xl bg-slate-800/60 border border-slate-700/60 text-sm text-slate-200 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/30 appearance-none cursor-pointer pr-8"
        >
          <option value="all">Всі категорії ({{ productsStore.products.length }})</option>
          <option
            v-for="cat in productsStore.categories.filter((c) => c !== 'all')"
            :key="cat"
            :value="cat"
          >
            {{ cat }}
          </option>
        </select>
        <SlidersHorizontal class="w-3.5 h-3.5 text-slate-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
      </div>

      <!-- Min Score Filter -->
      <div class="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-slate-800/60 border border-slate-700/60 text-xs text-slate-300">
        <span>Мін. Score:</span>
        <input
          v-model.number="productsStore.minScore"
          type="range"
          min="0"
          max="90"
          step="10"
          class="w-20 accent-emerald-500 cursor-pointer"
        />
        <span class="font-bold text-emerald-400 min-w-[28px] text-right">{{ productsStore.minScore }}+</span>
      </div>
    </div>

    <!-- Actions & View mode switch -->
    <div class="flex items-center gap-2.5 shrink-0 justify-end">
      <!-- View mode switch -->
      <div class="flex items-center p-1 rounded-xl bg-slate-800/60 border border-slate-700/60 text-slate-400">
        <button
          @click="productsStore.viewMode = 'grid'"
          title="Сітка карток"
          class="p-1.5 rounded-lg transition-colors"
          :class="productsStore.viewMode === 'grid' ? 'bg-slate-700 text-white shadow-sm' : 'hover:text-slate-200'"
        >
          <LayoutGrid class="w-4 h-4" />
        </button>
        <button
          @click="productsStore.viewMode = 'table'"
          title="Аналітична таблиця"
          class="p-1.5 rounded-lg transition-colors"
          :class="productsStore.viewMode === 'table' ? 'bg-slate-700 text-white shadow-sm' : 'hover:text-slate-200'"
        >
          <Table class="w-4 h-4" />
        </button>
      </div>

      <!-- Scrape button -->
      <button
        @click="productsStore.triggerScrape"
        :disabled="productsStore.isScraping"
        class="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white border border-slate-700 text-sm font-medium transition-all shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <RefreshCw class="w-4 h-4" :class="{ 'animate-spin': productsStore.isScraping }" />
        <span>{{ productsStore.isScraping ? 'Парсинг...' : 'Спарсити Amazon' }}</span>
      </button>

      <!-- Score button -->
      <button
        @click="productsStore.triggerScore"
        :disabled="productsStore.isScoring"
        class="flex items-center gap-2 px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-sm transition-all shadow-lg shadow-emerald-600/20 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Sparkles class="w-4 h-4" :class="{ 'animate-pulse': productsStore.isScoring }" />
        <span>{{ productsStore.isScoring ? 'Оцінюємо...' : 'AI Score' }}</span>
      </button>
    </div>
  </div>
</template>
