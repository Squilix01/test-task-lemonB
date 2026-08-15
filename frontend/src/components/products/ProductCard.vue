<script setup lang="ts">
import type { Product } from '@/api/products'
import ScoreBadge from '@/components/ui/ScoreBadge.vue'
import { Star, ExternalLink, Sparkles, TrendingUp } from 'lucide-vue-next'

defineProps<{
  product: Product
}>()

const emit = defineEmits<{
  (e: 'inspect', product: Product): void
}>()
</script>

<template>
  <div
    class="group rounded-2xl bg-slate-900/70 border border-slate-800/90 hover:border-slate-700/90 transition-all duration-200 flex flex-col overflow-hidden hover:shadow-xl hover:shadow-slate-950/50"
  >
    <!-- Image Header with Badges -->
    <div class="relative h-48 bg-slate-950/80 p-4 flex items-center justify-center overflow-hidden border-b border-slate-800/60">
      <img
        :src="product.image_url"
        :alt="product.name"
        class="max-h-full max-w-full object-contain group-hover:scale-105 transition-transform duration-300"
        loading="lazy"
        @error="($event.target as HTMLImageElement).src = 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&q=80'"
      />

      <!-- Score badge overlay -->
      <div class="absolute top-3 right-3">
        <ScoreBadge :score="product.score" size="sm" />
      </div>

      <!-- Category & Boost tag overlay -->
      <div class="absolute bottom-3 left-3 flex items-center gap-1.5">
        <span class="text-[11px] font-medium px-2 py-0.5 rounded-md bg-slate-900/90 border border-slate-800 text-slate-300 backdrop-blur-sm">
          {{ product.category }}
        </span>

        <span
          v-if="(product.boost_score || 0) > 0"
          class="text-[10px] font-bold px-1.5 py-0.5 rounded-md bg-emerald-500/20 border border-emerald-500/30 text-emerald-300 backdrop-blur-sm flex items-center gap-1"
          title="Товар отримав додаткові бали завдяки збігу з базою Sales Boost"
        >
          <Sparkles class="w-3 h-3 text-emerald-400" />
          <span>+{{ Math.round(product.boost_score!) }} Boost</span>
        </span>
      </div>
    </div>

    <!-- Card Content -->
    <div class="p-4 flex-1 flex flex-col justify-between">
      <div>
        <h3
          class="font-medium text-sm text-slate-100 line-clamp-2 group-hover:text-emerald-300 transition-colors leading-snug"
          :title="product.name"
        >
          {{ product.name }}
        </h3>

        <!-- Metrics row -->
        <div class="mt-3 flex items-center justify-between text-xs text-slate-400">
          <div class="flex items-center gap-1.5 font-medium text-amber-400">
            <Star class="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
            <span>{{ product.rating.toFixed(1) }}</span>
            <span class="text-slate-500">({{ product.number_of_reviews.toLocaleString() }})</span>
          </div>

          <div v-if="product.trend_score" class="flex items-center gap-1 text-sky-400 font-medium">
            <TrendingUp class="w-3.5 h-3.5" />
            <span>Тренд: {{ Math.round(product.trend_score) }}</span>
          </div>
        </div>
      </div>

      <!-- Price & Actions Footer -->
      <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between gap-2">
        <div class="font-bold text-lg text-white">
          <span v-if="product.price > 0">${{ product.price.toFixed(2) }}</span>
          <span v-else class="text-xs text-slate-500 font-normal">Ціна за запитом</span>
        </div>

        <div class="flex items-center gap-1.5">
          <button
            @click="emit('inspect', product)"
            class="flex items-center gap-1 px-2.5 py-1.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 text-xs font-medium border border-emerald-500/20 transition-colors"
          >
            <Sparkles class="w-3 h-3" />
            <span>AI Аналіз</span>
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
      </div>
    </div>
  </div>
</template>
