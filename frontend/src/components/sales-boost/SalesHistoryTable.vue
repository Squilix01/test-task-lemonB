<script setup lang="ts">
import type { SalesHistoryItem } from '@/api/salesBoost'
import { Trash2 } from 'lucide-vue-next'

defineProps<{
  items: SalesHistoryItem[]
}>()

const emit = defineEmits<{
  (e: 'delete', id: number): void
}>()
</script>

<template>
  <div class="rounded-2xl border border-slate-800/80 bg-slate-900/60 overflow-hidden shadow-sm">
    <div class="p-4 border-b border-slate-800/80 flex items-center justify-between">
      <h3 class="text-sm font-bold text-white uppercase tracking-wider">
        База минулих продажів ({{ items.length }})
      </h3>
    </div>

    <div class="overflow-x-auto">
      <table class="w-full text-left text-sm text-slate-300">
        <thead class="bg-slate-950/60 text-xs uppercase tracking-wider text-slate-400 border-b border-slate-800/80">
          <tr>
            <th scope="col" class="py-3 px-4 font-semibold">Назва товару</th>
            <th scope="col" class="py-3 px-4 font-semibold">Категорія</th>
            <th scope="col" class="py-3 px-4 font-semibold text-right">Ціна</th>
            <th scope="col" class="py-3 px-4 font-semibold text-right">Продажі</th>
            <th scope="col" class="py-3 px-4 font-semibold text-right">Виручка</th>
            <th scope="col" class="py-3 px-4 font-semibold text-right">Маржа</th>
            <th scope="col" class="py-3 px-4 font-semibold text-right">Дії</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800/60">
          <tr v-if="items.length === 0">
            <td colspan="7" class="py-8 text-center text-slate-500 text-xs">
              Записів не знайдено. Завантажте CSV-файл вище.
            </td>
          </tr>

          <tr
            v-for="item in items"
            :key="item.id"
            class="hover:bg-slate-800/40 transition-colors"
          >
            <td class="py-3 px-4 font-medium text-slate-100 max-w-xs">
              {{ item.name }}
            </td>
            <td class="py-3 px-4 whitespace-nowrap">
              <span class="px-2 py-0.5 rounded bg-slate-800 text-xs text-slate-300">
                {{ item.category }}
              </span>
            </td>
            <td class="py-3 px-4 text-right font-semibold text-white whitespace-nowrap">
              ${{ item.price.toFixed(2) }}
            </td>
            <td class="py-3 px-4 text-right text-slate-300 font-mono text-xs whitespace-nowrap">
              {{ item.number_of_sales ? item.number_of_sales.toLocaleString() : '—' }}
            </td>
            <td class="py-3 px-4 text-right text-emerald-400 font-mono text-xs whitespace-nowrap">
              {{ item.revenue ? `$${item.revenue.toLocaleString()}` : '—' }}
            </td>
            <td class="py-3 px-4 text-right text-slate-300 font-mono text-xs whitespace-nowrap">
              {{ item.margin ? `${item.margin}%` : '—' }}
            </td>
            <td class="py-3 px-4 text-right whitespace-nowrap">
              <button
                @click="emit('delete', item.id)"
                title="Видалити запис"
                class="p-1.5 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 transition-colors"
              >
                <Trash2 class="w-4 h-4" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
