<script setup lang="ts">
import { ref } from 'vue'
import { useProductsStore } from '@/stores/products'
import { Sparkles, RefreshCw, Terminal, CheckCircle2, AlertCircle, X, ChevronDown, ChevronUp, Cpu, Calculator } from 'lucide-vue-next'

const productsStore = useProductsStore()
const showLogs = ref(true)
</script>

<template>
  <!-- Fullscreen Modal Backdrop Overlay -->
  <Teleport to="body">
    <div
      v-if="productsStore.activeTask"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fade-in"
    >
      <!-- Centered Modal Card -->
      <div
        class="w-full max-w-lg rounded-3xl bg-slate-900 border border-slate-800 shadow-2xl p-6 relative overflow-hidden backdrop-blur-2xl transition-all"
        :class="{
          'border-emerald-500/40 shadow-emerald-500/10': productsStore.activeTask.isDone,
          'border-rose-500/40 shadow-rose-500/10': productsStore.activeTask.isError,
          'border-slate-700/80': !productsStore.activeTask.isDone && !productsStore.activeTask.isError,
        }"
      >
        <!-- Background Ambient Glow -->
        <div
          class="absolute -top-20 -right-20 w-60 h-60 rounded-full blur-3xl pointer-events-none transition-all"
          :class="{
            'bg-emerald-500/15': productsStore.activeTask.isDone || productsStore.activeTask.type === 'score',
            'bg-sky-500/15': productsStore.activeTask.type === 'scrape' && !productsStore.activeTask.isDone,
            'bg-rose-500/15': productsStore.activeTask.isError,
          }"
        />

        <!-- Header -->
        <div class="flex items-start justify-between gap-4 relative z-10">
          <div class="flex items-center gap-3.5">
            <!-- Dynamic State Icon -->
            <div
              class="w-11 h-11 rounded-2xl flex items-center justify-center shrink-0 border"
              :class="{
                'bg-emerald-500/20 text-emerald-400 border-emerald-500/30': productsStore.activeTask.isDone,
                'bg-rose-500/20 text-rose-400 border-rose-500/30': productsStore.activeTask.isError,
                'bg-slate-800 text-emerald-400 border-slate-700': !productsStore.activeTask.isDone && !productsStore.activeTask.isError,
              }"
            >
              <CheckCircle2 v-if="productsStore.activeTask.isDone" class="w-6 h-6 text-emerald-400" />
              <AlertCircle v-else-if="productsStore.activeTask.isError" class="w-6 h-6 text-rose-400" />
              <RefreshCw
                v-else
                class="w-5 h-5 animate-spin"
                :class="productsStore.activeTask.type === 'score' ? 'text-emerald-400' : 'text-sky-400'"
              />
            </div>

            <div>
              <div class="flex items-center gap-2">
                <h3 class="text-base font-bold text-white tracking-tight">
                  {{ productsStore.activeTask.title }}
                </h3>
              </div>

              <!-- Engine & Status Pills -->
              <div class="flex items-center gap-1.5 mt-1">
                <span
                  class="text-[10px] font-semibold px-2 py-0.5 rounded-md uppercase tracking-wider"
                  :class="{
                    'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30': productsStore.activeTask.isDone,
                    'bg-rose-500/20 text-rose-300 border border-rose-500/30': productsStore.activeTask.isError,
                    'bg-slate-800 text-slate-300 border border-slate-700': !productsStore.activeTask.isDone && !productsStore.activeTask.isError,
                  }"
                >
                  {{ productsStore.activeTask.isDone ? 'Завершено успішно' : productsStore.activeTask.isError ? 'Помилка виконання' : 'Обробка...' }}
                </span>
              </div>
            </div>
          </div>

          <!-- Close / Dismiss (if running, acts as minimize) -->
          <button
            @click="productsStore.dismissTask"
            class="p-1.5 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            title="Закрити / Згорнути"
          >
            <X class="w-5 h-5" />
          </button>
        </div>

        <!-- Current action text -->
        <div class="mt-4 p-3 rounded-xl bg-slate-950/60 border border-slate-800/80 relative z-10">
          <p class="text-xs text-slate-300 font-medium flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full shrink-0" :class="productsStore.activeTask.isDone ? 'bg-emerald-400' : 'bg-amber-400 animate-ping'" />
            <span class="truncate">{{ productsStore.activeTask.statusText }}</span>
          </p>
          <p v-if="productsStore.activeTask.currentProduct" class="text-[11px] text-slate-400 truncate mt-1 pl-3.5">
            Товар: {{ productsStore.activeTask.currentProduct }}
          </p>
        </div>

        <!-- Animated Progress Bar -->
        <div class="mt-4 relative z-10">
          <div class="flex items-center justify-between text-xs font-semibold text-slate-400 mb-1.5">
            <span>Прогрес:</span>
            <span class="text-white font-mono text-xs">{{ productsStore.activeTask.progress }}%</span>
          </div>

          <div class="w-full h-2.5 bg-slate-950 rounded-full overflow-hidden p-0.5 border border-slate-800">
            <div
              class="h-full rounded-full transition-all duration-500 relative"
              :class="{
                'bg-emerald-500': productsStore.activeTask.isDone || productsStore.activeTask.type === 'score',
                'bg-sky-500': productsStore.activeTask.type === 'scrape' && !productsStore.activeTask.isDone,
                'bg-rose-500': productsStore.activeTask.isError,
              }"
              :style="{ width: `${productsStore.activeTask.progress}%` }"
            >
              <div
                v-if="!productsStore.activeTask.isDone && !productsStore.activeTask.isError"
                class="absolute inset-0 bg-white/20 animate-pulse rounded-full"
              />
            </div>
          </div>
        </div>

        <!-- Live Debug Log Terminal (Collapsible) -->
        <div class="mt-4 relative z-10">
          <div class="flex items-center justify-between mb-1.5">
            <button
              @click="showLogs = !showLogs"
              class="flex items-center gap-1.5 text-[11px] font-semibold text-slate-400 hover:text-white transition-colors"
            >
              <Terminal class="w-3.5 h-3.5 text-emerald-400" />
              <span>Лог подій у реальному часі</span>
              <ChevronUp v-if="showLogs" class="w-3.5 h-3.5 text-slate-500" />
              <ChevronDown v-else class="w-3.5 h-3.5 text-slate-500" />
            </button>

            <span class="flex items-center gap-1 text-[10px] text-emerald-400 font-mono">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400" :class="{ 'animate-ping': !productsStore.activeTask.isDone }" />
              {{ productsStore.activeTask.isDone ? 'Finished' : 'Live' }}
            </span>
          </div>

          <div
            v-if="showLogs"
            class="p-3 rounded-xl bg-slate-950/95 border border-slate-800 font-mono text-[11px] text-slate-300 max-h-36 overflow-y-auto space-y-1 shadow-inner"
          >
            <div
              v-for="(log, idx) in productsStore.activeTask.logs"
              :key="idx"
              class="leading-relaxed flex items-start gap-1.5"
            >
              <span class="text-emerald-500 select-none">&gt;</span>
              <span :class="{ 'text-emerald-300 font-bold': idx === productsStore.activeTask.logs.length - 1 }">
                {{ log }}
              </span>
            </div>
          </div>
        </div>

        <!-- Modal Footer Actions -->
        <div class="mt-6 flex items-center justify-end gap-3 relative z-10 pt-4 border-t border-slate-800/80">
          <button
            v-if="!productsStore.activeTask.isDone && !productsStore.activeTask.isError"
            @click="productsStore.dismissTask"
            class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition-colors"
          >
            Згорнути у фон
          </button>

          <button
            v-else
            @click="productsStore.dismissTask"
            class="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold transition-all shadow-lg shadow-emerald-600/20"
          >
            Зрозуміло, закрити
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>
