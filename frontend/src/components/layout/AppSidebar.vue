<script setup lang="ts">
import { useRoute } from 'vue-router'
import { LayoutDashboard, TrendingUp, Sparkles } from 'lucide-vue-next'

const route = useRoute()

const navigation = [
  {
    name: 'Товари Amazon',
    path: '/products',
    icon: LayoutDashboard,
    badge: 'Live',
  },
  {
    name: 'Sales Boost',
    path: '/sales-boost',
    icon: TrendingUp,
    badge: 'CSV',
  },
]
</script>

<template>
  <aside class="w-64 border-r border-slate-800/80 bg-slate-900/40 flex flex-col shrink-0">
    <!-- Brand Logo -->
    <div class="h-16 px-6 flex items-center gap-3 border-b border-slate-800/80">
      <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-amber-400 to-emerald-500 flex items-center justify-center text-xl shadow-lg shadow-emerald-500/10">
        🍋
      </div>
      <div>
        <h1 class="font-bold text-sm text-white tracking-tight leading-none">e-Commerce Score</h1>
      </div>
    </div>

    <!-- Navigation links -->
    <nav class="p-4 space-y-1.5 flex-1">
      <div class="px-3 py-2 text-[11px] font-semibold tracking-wider text-slate-500 uppercase">
        Головне меню
      </div>

      <RouterLink
        v-for="item in navigation"
        :key="item.path"
        :to="item.path"
        class="flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all group"
        :class="[
          route.path === item.path
            ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/20 shadow-sm'
            : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50',
        ]"
      >
        <div class="flex items-center gap-3">
          <component
            :is="item.icon"
            class="w-4 h-4 transition-colors"
            :class="route.path === item.path ? 'text-emerald-400' : 'text-slate-400 group-hover:text-slate-300'"
          />
          <span>{{ item.name }}</span>
        </div>

        <span
          class="text-[10px] px-1.5 py-0.5 rounded font-semibold uppercase tracking-wider"
          :class="route.path === item.path ? 'bg-emerald-500/20 text-emerald-300' : 'bg-slate-800 text-slate-500'"
        >
          {{ item.badge }}
        </span>
      </RouterLink>
    </nav>
  </aside>
</template>
