<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  score: number | null
  size?: 'sm' | 'md' | 'lg'
}>()

const badgeClass = computed(() => {
  if (props.score === null) {
    return 'bg-slate-800 text-slate-400 border-slate-700'
  }
  if (props.score >= 80) {
    return 'bg-emerald-950/80 text-emerald-300 border-emerald-500/40 ring-1 ring-emerald-500/20'
  }
  if (props.score >= 50) {
    return 'bg-amber-950/80 text-amber-300 border-amber-500/40 ring-1 ring-amber-500/20'
  }
  return 'bg-rose-950/80 text-rose-300 border-rose-500/40 ring-1 ring-rose-500/20'
})

const sizeClass = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'text-xs px-2 py-0.5 font-medium'
    case 'lg':
      return 'text-base px-3.5 py-1.5 font-bold'
    default:
      return 'text-sm px-2.5 py-1 font-semibold'
  }
})
</script>

<template>
  <span
    class="inline-flex items-center gap-1.5 rounded-full border transition-colors shadow-sm"
    :class="[badgeClass, sizeClass]"
  >
    <span
      class="w-1.5 h-1.5 rounded-full"
      :class="{
        'bg-slate-500': score === null,
        'bg-emerald-400 animate-pulse': score !== null && score >= 80,
        'bg-amber-400': score !== null && score >= 50 && score < 80,
        'bg-rose-400': score !== null && score < 50,
      }"
    />
    <span v-if="score !== null">{{ score }}/100</span>
    <span v-else>Не оцінено</span>
  </span>
</template>
