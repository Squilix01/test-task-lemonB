<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { Sparkles, Lock, User, ArrowRight, AlertCircle, RefreshCw } from 'lucide-vue-next'

const authStore = useAuthStore()
const router = useRouter()

const isRegister = ref(false)
const username = ref('')
const password = ref('')

async function handleSubmit() {
  let success = false
  if (isRegister.value) {
    success = await authStore.register({
      username: username.value,
      password: password.value,
    })
  } else {
    success = await authStore.login({
      username: username.value,
      password: password.value,
    })
  }

  if (success) {
    router.push('/products')
  }
}
</script>

<template>
  <div class="min-h-screen bg-slate-950 flex flex-col justify-center items-center p-4 relative overflow-hidden">
    <!-- Ambient glow background -->
    <div class="absolute -top-40 -left-40 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
    <div class="absolute -bottom-40 -right-40 w-96 h-96 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />

    <div class="w-full max-w-md relative z-10">
      <!-- Logo Header -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-14 h-14 rounded-3xl bg-gradient-to-br from-amber-400 to-emerald-500 text-3xl shadow-xl shadow-emerald-500/10 mb-4">
          🍋
        </div>
        <h1 class="text-2xl font-extrabold text-white tracking-tight">e-Commerce Score</h1>
        <p class="text-xs text-slate-400 mt-1.5">
          Платформа автоматизованого AI-скорингу товарів Amazon
        </p>
      </div>

      <!-- Main Login / Register Card -->
      <div class="rounded-3xl bg-slate-900/80 border border-slate-800 p-8 shadow-2xl backdrop-blur-xl">
        <!-- Tab Selector -->
        <div class="grid grid-cols-2 p-1 rounded-xl bg-slate-950/60 border border-slate-800 mb-6 text-xs font-semibold">
          <button
            type="button"
            @click="isRegister = false"
            class="py-2 rounded-lg transition-all"
            :class="!isRegister ? 'bg-slate-800 text-white shadow-sm' : 'text-slate-400 hover:text-white'"
          >
            Вхід
          </button>
          <button
            type="button"
            @click="isRegister = true"
            class="py-2 rounded-lg transition-all"
            :class="isRegister ? 'bg-slate-800 text-white shadow-sm' : 'text-slate-400 hover:text-white'"
          >
            Реєстрація
          </button>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- Username Input -->
          <div>
            <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Ім'я користувача
            </label>
            <div class="relative">
              <User class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                v-model="username"
                type="text"
                required
                placeholder="Введіть логін"
                class="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950/80 border border-slate-800 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/30 transition-all"
              />
            </div>
          </div>

          <!-- Password Input -->
          <div>
            <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Пароль
            </label>
            <div class="relative">
              <Lock class="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                v-model="password"
                type="password"
                required
                placeholder="••••••••"
                class="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950/80 border border-slate-800 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/30 transition-all"
              />
            </div>
          </div>

          <!-- Error Alert -->
          <div v-if="authStore.error" class="p-3 rounded-xl bg-rose-950/40 border border-rose-500/30 text-xs text-rose-300 flex items-center gap-2">
            <AlertCircle class="w-4 h-4 shrink-0 text-rose-400" />
            <span>{{ authStore.error }}</span>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="authStore.isLoading"
            class="w-full mt-2 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold text-sm transition-all shadow-lg shadow-emerald-600/20 flex items-center justify-center gap-2 disabled:opacity-50"
          >
            <RefreshCw v-if="authStore.isLoading" class="w-4 h-4 animate-spin" />
            <span>{{ isRegister ? 'Створити акаунт' : 'Увійти в панель' }}</span>
            <ArrowRight v-if="!authStore.isLoading" class="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  </div>
</template>
