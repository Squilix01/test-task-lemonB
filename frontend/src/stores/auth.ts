import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi, type LoginPayload, type RegisterPayload, type UserResponse } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const user = ref<UserResponse | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  async function login(payload: LoginPayload) {
    isLoading.value = true
    error.value = null
    try {
      const data = await authApi.login(payload)
      token.value = data.access_token
      localStorage.setItem('access_token', data.access_token)
      await fetchMe()
      return true
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Невірний логін або пароль'
      return false
    } finally {
      isLoading.value = false
    }
  }

  async function register(payload: RegisterPayload) {
    isLoading.value = true
    error.value = null
    try {
      await authApi.register(payload)
      // Auto login after register
      return await login(payload)
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Помилка при реєстрації'
      return false
    } finally {
      isLoading.value = false
    }
  }

  async function fetchMe() {
    if (!token.value) return
    try {
      user.value = await authApi.getMe()
    } catch {
      logout()
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('access_token')
  }

  return {
    token,
    user,
    isLoading,
    error,
    isAuthenticated,
    login,
    register,
    fetchMe,
    logout,
  }
})
