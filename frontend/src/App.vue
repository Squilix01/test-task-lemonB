<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import ToastContainer from '@/components/ui/ToastContainer.vue'

const authStore = useAuthStore()

onMounted(() => {
  if (authStore.isAuthenticated) {
    authStore.fetchMe()
  }
})
</script>

<template>
  <div class="min-h-screen bg-slate-950 text-slate-100 font-['Inter',sans-serif]">
    <RouterView />
    <ToastContainer />
  </div>
</template>
