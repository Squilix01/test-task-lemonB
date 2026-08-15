<script setup lang="ts">
import { useProductsStore } from '@/stores/products'
import { ShoppingCart, Award, Sparkles, TrendingUp } from 'lucide-vue-next'

const productsStore = useProductsStore()
</script>

<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
    <!-- Stat 1: Total Scraped -->
    <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800/80 shadow-sm relative overflow-hidden group">
      <div class="flex items-center justify-between">
        <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Всього товарів</span>
        <div class="p-2 rounded-xl bg-slate-800/80 text-slate-300">
          <ShoppingCart class="w-4 h-4" />
        </div>
      </div>
      <div class="mt-3 flex items-baseline gap-2">
        <span class="text-2xl font-bold text-white tracking-tight">{{ productsStore.stats.totalCount }}</span>
        <span class="text-xs text-slate-500 font-medium">в базі даних</span>
      </div>
    </div>

    <!-- Stat 2: High Potential (Score 75+) -->
    <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800/80 shadow-sm relative overflow-hidden group">
      <div class="flex items-center justify-between">
        <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Топ-потенціал (75+)</span>
        <div class="p-2 rounded-xl bg-emerald-500/10 text-emerald-400">
          <Award class="w-4 h-4" />
        </div>
      </div>
      <div class="mt-3 flex items-baseline gap-2">
        <span class="text-2xl font-bold text-emerald-400 tracking-tight">{{ productsStore.stats.topScoredCount }}</span>
        <span class="text-xs text-emerald-500/80 font-medium">перспективних товарів</span>
      </div>
    </div>

    <!-- Stat 3: Average AI Score -->
    <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800/80 shadow-sm relative overflow-hidden group">
      <div class="flex items-center justify-between">
        <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Середній AI Score</span>
        <div class="p-2 rounded-xl bg-amber-500/10 text-amber-400">
          <Sparkles class="w-4 h-4" />
        </div>
      </div>
      <div class="mt-3 flex items-baseline gap-2">
        <span class="text-2xl font-bold text-amber-300 tracking-tight">{{ productsStore.stats.avgScore }}/100</span>
        <span class="text-xs text-slate-500 font-medium">по базі</span>
      </div>
    </div>

    <!-- Stat 4: Scored / Unscored -->
    <div class="p-5 rounded-2xl bg-slate-900/60 border border-slate-800/80 shadow-sm relative overflow-hidden group">
      <div class="flex items-center justify-between">
        <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Оцінено AI</span>
        <div class="p-2 rounded-xl bg-sky-500/10 text-sky-400">
          <TrendingUp class="w-4 h-4" />
        </div>
      </div>
      <div class="mt-3 flex items-baseline gap-2">
        <span class="text-2xl font-bold text-sky-300 tracking-tight">
          {{ productsStore.stats.scoredCount }} / {{ productsStore.stats.totalCount }}
        </span>
        <span class="text-xs text-slate-500 font-medium">готово до аналізу</span>
      </div>
    </div>
  </div>
</template>
