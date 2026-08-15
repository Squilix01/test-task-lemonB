<script setup lang="ts">
import type { Product } from '@/api/products'
import ScoreBadge from '@/components/ui/ScoreBadge.vue'
import { X, Sparkles, ExternalLink, TrendingUp, Award, Star, MessageSquare } from 'lucide-vue-next'

const props = defineProps<{
  product: Product | null
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()
</script>

<template>
  <div
    v-if="product"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in"
    @click.self="emit('close')"
  >
    <div class="relative w-full max-w-2xl rounded-3xl bg-slate-900 border border-slate-800 shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
      <!-- Header -->
      <div class="p-6 border-b border-slate-800/80 flex items-start justify-between gap-4 bg-slate-950/40">
        <div class="flex items-start gap-4">
          <div class="w-16 h-16 rounded-2xl bg-slate-950 p-2 border border-slate-800 shrink-0 flex items-center justify-center">
            <img
              :src="product.image_url"
              :alt="product.name"
              class="max-w-full max-h-full object-contain"
            />
          </div>
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="px-2 py-0.5 rounded-md bg-slate-800 text-[11px] font-semibold text-slate-300">
                {{ product.category }}
              </span>
              <span v-if="product.price > 0" class="text-sm font-bold text-emerald-400">
                ${{ product.price.toFixed(2) }}
              </span>
            </div>
            <h2 class="font-bold text-base text-white line-clamp-2 leading-snug">
              {{ product.name }}
            </h2>
          </div>
        </div>

        <button
          @click="emit('close')"
          class="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors shrink-0"
        >
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Body Scrollable Content -->
      <div class="p-6 overflow-y-auto space-y-6 flex-1">
        <!-- Main Score Hero Card -->
        <div class="p-5 rounded-2xl bg-gradient-to-br from-slate-950 to-slate-900 border border-slate-800/80 flex items-center justify-between gap-4">
          <div>
            <span class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Загальний AI Потенціал</span>
            <div class="text-3xl font-extrabold text-white mt-1 flex items-baseline gap-2">
              <span :class="{
                'text-emerald-400': (product.score || 0) >= 80,
                'text-amber-400': (product.score || 0) >= 50 && (product.score || 0) < 80,
                'text-rose-400': (product.score || 0) < 50 && product.score !== null,
                'text-slate-400': product.score === null
              }">
                {{ product.score !== null ? product.score : '—' }}
              </span>
              <span class="text-slate-500 text-base font-normal">/ 100</span>
            </div>
          </div>

          <ScoreBadge :score="product.score" size="lg" />
        </div>

        <!-- AI Reasoning Box -->
        <div class="p-5 rounded-2xl bg-emerald-950/20 border border-emerald-500/20">
          <div class="flex items-center gap-2 text-emerald-400 font-semibold text-sm mb-2">
            <Sparkles class="w-4 h-4" />
            <span>Аналітичне обґрунтування</span>
          </div>
          <p class="text-sm text-slate-200 leading-relaxed whitespace-pre-line font-medium">
            {{ product.reasoning || 'Аналіз для даного товару ще не згенеровано. Натисніть кнопку «AI Score» на панелі керування.' }}
          </p>
        </div>

        <!-- Breakdown Grid -->
        <div>
          <h3 class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
            Компоненти оцінки товару
          </h3>

          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <!-- Rating Points -->
            <div class="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 text-center">
              <div class="flex items-center justify-center gap-1 text-amber-400 mb-1">
                <Star class="w-4 h-4 fill-amber-400" />
                <span class="text-sm font-bold">{{ product.rating.toFixed(1) }}</span>
              </div>
              <span class="text-[11px] text-slate-400 font-medium">Рейтинг товару</span>
            </div>

            <!-- Reviews Points -->
            <div class="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 text-center">
              <div class="flex items-center justify-center gap-1 text-slate-200 mb-1">
                <MessageSquare class="w-4 h-4 text-slate-400" />
                <span class="text-sm font-bold">{{ product.number_of_reviews.toLocaleString() }}</span>
              </div>
              <span class="text-[11px] text-slate-400 font-medium">Відгуків покупців</span>
            </div>

            <!-- Trend Points -->
            <div class="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 text-center">
              <div class="flex items-center justify-center gap-1 text-sky-400 mb-1">
                <TrendingUp class="w-4 h-4" />
                <span class="text-sm font-bold">{{ product.trend_score ? Math.round(product.trend_score) : '—' }}</span>
              </div>
              <span class="text-[11px] text-slate-400 font-medium">Google Trends</span>
            </div>

            <!-- Sales Boost Points -->
            <div class="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 text-center">
              <div class="flex items-center justify-center gap-1 text-emerald-400 mb-1">
                <Award class="w-4 h-4" />
                <span class="text-sm font-bold">+{{ product.boost_score ? Math.round(product.boost_score) : 0 }}</span>
              </div>
              <span class="text-[11px] text-slate-400 font-medium">Sales Boost бонус</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="p-4 px-6 border-t border-slate-800/80 bg-slate-950/40 flex items-center justify-between">
        <a
          :href="product.product_url"
          target="_blank"
          rel="noopener noreferrer"
          class="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white text-xs font-semibold transition-all border border-slate-700"
        >
          <span>Відкрити товар на Amazon</span>
          <ExternalLink class="w-3.5 h-3.5" />
        </a>

        <button
          @click="emit('close')"
          class="px-5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold transition-all shadow-lg shadow-emerald-600/20"
        >
          Зрозуміло
        </button>
      </div>
    </div>
  </div>
</template>
