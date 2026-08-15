<script setup lang="ts">
import type { Product } from '@/api/products'
import ScoreBadge from '@/components/ui/ScoreBadge.vue'
import { Star, ExternalLink, Sparkles } from 'lucide-vue-next'

defineProps<{
  products: Product[]
}>()

const emit = defineEmits<{
  (e: 'inspect', product: Product): void
}>()
</script>

<template>
  <div class="rounded-2xl border border-slate-800/80 bg-slate-900/60 overflow-hidden shadow-sm">
    <div class="overflow-x-auto">
      <table class="w-full text-left text-sm text-slate-300">
        <thead class="bg-slate-950/60 text-xs uppercase tracking-wider text-slate-400 border-b border-slate-800/80">
          <tr>
            <th scope="col" class="py-3.5 px-4 font-semibold">Товар</th>
            <th scope="col" class="py-3.5 px-4 font-semibold">Категорія</th>
            <th scope="col" class="py-3.5 px-4 font-semibold text-right">Ціна</th>
            <th scope="col" class="py-3.5 px-4 font-semibold text-center">Рейтинг</th>
            <th scope="col" class="py-3.5 px-4 font-semibold text-right">Відгуки</th>
            <th scope="col" class="py-3.5 px-4 font-semibold text-center">Тренд</th>
            <th scope="col" class="py-3.5 px-4 font-semibold text-center">AI Score</th>
            <th scope="col" class="py-3.5 px-4 font-semibold text-right">Дії</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-800/60">
          <tr
            v-for="product in products"
            :key="product.id"
            class="hover:bg-slate-800/40 transition-colors group cursor-pointer"
            @click="emit('inspect', product)"
          >
            <!-- Product Info (Image + Title) -->
            <td class="py-3.5 px-4 max-w-xs sm:max-w-sm">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-lg bg-slate-950 p-1 shrink-0 border border-slate-800 flex items-center justify-center">
                  <img
                    :src="product.image_url"
                    :alt="product.name"
                    class="max-w-full max-h-full object-contain"
                    loading="lazy"
                    @error="($event.target as HTMLImageElement).src = 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=100&q=80'"
                  />
                </div>
                <div class="font-medium text-slate-100 group-hover:text-emerald-300 transition-colors line-clamp-2">
                  {{ product.name }}
                </div>
              </div>
            </td>

            <!-- Category -->
            <td class="py-3.5 px-4 whitespace-nowrap">
              <span class="px-2.5 py-1 rounded-md bg-slate-800 text-xs font-medium text-slate-300">
                {{ product.category }}
              </span>
            </td>

            <!-- Price -->
            <td class="py-3.5 px-4 text-right font-bold text-white whitespace-nowrap">
              <span v-if="product.price > 0">${{ product.price.toFixed(2) }}</span>
              <span v-else class="text-xs text-slate-500 font-normal">N/A</span>
            </td>

            <!-- Rating -->
            <td class="py-3.5 px-4 text-center whitespace-nowrap">
              <div class="inline-flex items-center gap-1 font-semibold text-amber-400">
                <Star class="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                <span>{{ product.rating.toFixed(1) }}</span>
              </div>
            </td>

            <!-- Reviews -->
            <td class="py-3.5 px-4 text-right font-mono text-xs text-slate-400 whitespace-nowrap">
              {{ product.number_of_reviews.toLocaleString() }}
            </td>

            <!-- Trend Score -->
            <td class="py-3.5 px-4 text-center whitespace-nowrap">
              <span v-if="product.trend_score" class="font-medium text-sky-400 text-xs">
                {{ Math.round(product.trend_score) }}
              </span>
              <span v-else class="text-xs text-slate-600">—</span>
            </td>

            <!-- Score -->
            <td class="py-3.5 px-4 text-center whitespace-nowrap">
              <ScoreBadge :score="product.score" size="sm" />
            </td>

            <!-- Actions -->
            <td class="py-3.5 px-4 text-right whitespace-nowrap" @click.stop>
              <div class="flex items-center justify-end gap-2">
                <button
                  @click="emit('inspect', product)"
                  title="AI Аналіз"
                  class="p-1.5 rounded-lg text-emerald-400 hover:bg-emerald-500/20 transition-colors"
                >
                  <Sparkles class="w-4 h-4" />
                </button>
                <a
                  :href="product.product_url"
                  target="_blank"
                  rel="noopener noreferrer"
                  title="Відкрити на Amazon"
                  class="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
                >
                  <ExternalLink class="w-4 h-4" />
                </a>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
