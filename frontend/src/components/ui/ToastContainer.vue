<script setup lang="ts">
import { useToastStore } from '@/stores/toast'
import { CheckCircle2, AlertCircle, Info, X } from 'lucide-vue-next'

const toastStore = useToastStore()
</script>

<template>
  <div class="fixed bottom-5 right-5 z-50 flex flex-col gap-2 max-w-sm w-full pointer-events-none">
    <TransitionGroup
      enter-active-class="transform ease-out duration-300 transition"
      enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
      enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-for="toast in toastStore.toasts"
        :key="toast.id"
        class="pointer-events-auto flex items-start gap-3 p-4 rounded-xl border shadow-xl bg-slate-900/95 backdrop-blur-md transition-all"
        :class="{
          'border-emerald-500/30 text-emerald-100': toast.type === 'success',
          'border-rose-500/30 text-rose-100': toast.type === 'error',
          'border-sky-500/30 text-sky-100': toast.type === 'info',
        }"
      >
        <div class="mt-0.5 shrink-0">
          <CheckCircle2 v-if="toast.type === 'success'" class="w-5 h-5 text-emerald-400" />
          <AlertCircle v-else-if="toast.type === 'error'" class="w-5 h-5 text-rose-400" />
          <Info v-else class="w-5 h-5 text-sky-400" />
        </div>

        <div class="flex-1">
          <h4 class="text-sm font-semibold text-white">{{ toast.title }}</h4>
          <p class="text-xs mt-0.5 text-slate-300 leading-relaxed">{{ toast.message }}</p>
        </div>

        <button
          @click="toastStore.remove(toast.id)"
          class="shrink-0 text-slate-400 hover:text-white transition-colors p-1"
        >
          <X class="w-4 h-4" />
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>
