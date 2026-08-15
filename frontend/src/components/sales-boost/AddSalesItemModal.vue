<script setup lang="ts">
import { ref } from 'vue'
import { useSalesBoostStore } from '@/stores/salesBoost'
import { Plus, X, Tag, DollarSign, Star, MessageSquare, Link, Image as ImageIcon, Sparkles } from 'lucide-vue-next'

const emit = defineEmits<{
  (e: 'close'): void
}>()

const salesBoostStore = useSalesBoostStore()

const name = ref('')
const category = ref('Electronics')
const price = ref<number | ''>(29.99)
const rating = ref<number | ''>(4.7)
const reviews = ref<number | ''>(1250)
const keywords = ref('')
const productUrl = ref('')
const imageUrl = ref('')
const isSubmitting = ref(false)

const categories = [
  'Electronics',
  'Home & Kitchen',
  'Beauty & Personal Care',
  'Clothing, Shoes & Jewelry',
  'Sports & Outdoors',
  'Toys & Games',
  'Health & Household',
  'Other',
]

async function handleSubmit() {
  if (!name.value || !category.value || price.value === '') return

  isSubmitting.value = true
  const success = await salesBoostStore.createItem({
    name: name.value,
    category: category.value,
    price: Number(price.value),
    rating: rating.value !== '' ? Number(rating.value) : 0,
    number_of_reviews: reviews.value !== '' ? Number(reviews.value) : 0,
    keywords: keywords.value,
    product_url: productUrl.value,
    image_url: imageUrl.value,
  })

  isSubmitting.value = false
  if (success) {
    emit('close')
  }
}
</script>

<template>
  <Teleport to="body">
    <div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fade-in">
      <!-- Centered Modal Card -->
      <div class="w-full max-w-lg rounded-3xl bg-slate-900 border border-slate-800 shadow-2xl p-6 relative overflow-hidden backdrop-blur-2xl">
        <!-- Ambient glow -->
        <div class="absolute -top-20 -right-20 w-52 h-52 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />

        <!-- Header -->
        <div class="flex items-center justify-between pb-4 border-b border-slate-800 relative z-10">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
              <Plus class="w-5 h-5" />
            </div>
            <div>
              <h2 class="text-base font-bold text-white tracking-tight">Додати товар вручну</h2>
              <p class="text-xs text-slate-400">Створення запису для бази Sales Boost</p>
            </div>
          </div>

          <button
            @click="emit('close')"
            class="p-1.5 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X class="w-5 h-5" />
          </button>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleSubmit" class="mt-5 space-y-4 relative z-10 max-h-[75vh] overflow-y-auto pr-1">
          <!-- Product Name -->
          <div>
            <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
              Назва товару <span class="text-rose-400">*</span>
            </label>
            <input
              v-model="name"
              type="text"
              required
              placeholder="напр. Sony WH-1000XM5 Wireless Headphones"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/30 transition-all"
            />
          </div>

          <!-- Category & Price -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                Категорія <span class="text-rose-400">*</span>
              </label>
              <select
                v-model="category"
                class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/30 transition-all"
              >
                <option v-for="cat in categories" :key="cat" :value="cat">
                  {{ cat }}
                </option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                Ціна ($) <span class="text-rose-400">*</span>
              </label>
              <div class="relative">
                <DollarSign class="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  v-model="price"
                  type="number"
                  step="0.01"
                  min="0"
                  required
                  placeholder="29.99"
                  class="w-full pl-8 pr-3.5 py-2.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/30 transition-all font-mono"
                />
              </div>
            </div>
          </div>

          <!-- Rating & Reviews -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                Рейтинг (0 - 5.0)
              </label>
              <div class="relative">
                <Star class="w-3.5 h-3.5 text-amber-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  v-model="rating"
                  type="number"
                  step="0.1"
                  min="0"
                  max="5"
                  placeholder="4.8"
                  class="w-full pl-8 pr-3.5 py-2.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/30 transition-all font-mono"
                />
              </div>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                Кількість відгуків / продажів
              </label>
              <div class="relative">
                <MessageSquare class="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  v-model="reviews"
                  type="number"
                  min="0"
                  placeholder="12000"
                  class="w-full pl-8 pr-3.5 py-2.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/30 transition-all font-mono"
                />
              </div>
            </div>
          </div>

          <!-- Keywords (Key for boost matching) -->
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
                Ключові слова (для AI Boost)
              </label>
              <span class="text-[10px] text-emerald-400 font-medium flex items-center gap-1">
                <Sparkles class="w-3 h-3" />
                Дає до +20 балів скорингу
              </span>
            </div>
            <textarea
              v-model="keywords"
              rows="2"
              placeholder="напр. wireless bluetooth headphones noise cancelling over ear audio"
              class="w-full px-3.5 py-2.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/30 transition-all"
            />
          </div>

          <!-- Product URL & Image URL -->
          <div class="space-y-3">
            <div>
              <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                Посилання на товар (Amazon URL)
              </label>
              <div class="relative">
                <Link class="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  v-model="productUrl"
                  type="url"
                  placeholder="https://www.amazon.com/dp/..."
                  class="w-full pl-8 pr-3.5 py-2.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/30 transition-all"
                />
              </div>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1.5">
                Посилання на фото (Image URL)
              </label>
              <div class="relative">
                <ImageIcon class="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  v-model="imageUrl"
                  type="url"
                  placeholder="https://images-na.ssl-images-amazon.com/..."
                  class="w-full pl-8 pr-3.5 py-2.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500/60 focus:ring-1 focus:ring-emerald-500/30 transition-all"
                />
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="pt-4 flex items-center justify-end gap-3 border-t border-slate-800">
            <button
              type="button"
              @click="emit('close')"
              class="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold transition-colors"
            >
              Скасувати
            </button>

            <button
              type="submit"
              :disabled="isSubmitting"
              class="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold transition-all shadow-lg shadow-emerald-600/20 flex items-center gap-1.5 disabled:opacity-50"
            >
              <Plus class="w-4 h-4" />
              <span>{{ isSubmitting ? 'Збереження...' : 'Зберегти товар' }}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>
