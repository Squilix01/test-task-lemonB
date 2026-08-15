<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { LogOut, User, Sparkles } from 'lucide-vue-next'

const authStore = useAuthStore()
const router = useRouter()

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <header class="h-16 border-b border-slate-800/80 bg-slate-900/60 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-30">
    <div class="flex items-center gap-3">
      <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium">
        <Sparkles class="w-3.5 h-3.5" />
        <span>AI Analytics Active</span>
      </div>
    </div>

    <div class="flex items-center gap-4">
      <div class="flex items-center gap-2.5 px-3 py-1.5 rounded-xl bg-slate-800/60 border border-slate-700/60 text-sm">
        <div class="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-semibold text-xs">
          {{ authStore.user?.username?.charAt(0).toUpperCase()  }}
        </div>
        <span class="font-medium text-slate-200">{{ authStore.user?.username  }}</span>
      </div>

      <button
        @click="handleLogout"
        title="Вийти з системи"
        class="flex items-center gap-2 px-3 py-1.5 rounded-xl text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition-colors text-sm font-medium"
      >
        <LogOut class="w-4 h-4" />
        <span>Вийти</span>
      </button>
    </div>
  </header>
</template>
