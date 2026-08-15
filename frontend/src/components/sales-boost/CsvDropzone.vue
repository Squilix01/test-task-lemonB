<script setup lang="ts">
import { ref } from 'vue'
import { useSalesBoostStore } from '@/stores/salesBoost'
import { UploadCloud, FileText, CheckCircle2, AlertCircle, RefreshCw } from 'lucide-vue-next'

const salesBoostStore = useSalesBoostStore()
const isDragging = ref(false)
const selectedFile = ref<File | null>(null)
const error = ref<string | null>(null)

function handleDragOver(e: DragEvent) {
  e.preventDefault()
  isDragging.value = true
}

function handleDragLeave() {
  isDragging.value = false
}

function handleDrop(e: DragEvent) {
  e.preventDefault()
  isDragging.value = false
  if (e.dataTransfer?.files && e.dataTransfer.files.length > 0) {
    validateAndSetFile(e.dataTransfer.files[0])
  }
}

function handleFileInput(e: Event) {
  const target = e.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    validateAndSetFile(target.files[0])
  }
}

function validateAndSetFile(file: File) {
  error.value = null
  if (!file.name.endsWith('.csv')) {
    error.value = 'Будь ласка, оберіть файл у форматі .CSV'
    selectedFile.value = null
    return
  }
  selectedFile.value = file
}

async function upload() {
  if (!selectedFile.value) return
  const success = await salesBoostStore.uploadCsv(selectedFile.value)
  if (success) {
    selectedFile.value = null
  }
}
</script>

<template>
  <div class="rounded-2xl border border-slate-800/80 bg-slate-900/60 p-6">
    <div class="max-w-xl mx-auto">
      <div class="text-center mb-5">
        <h2 class="text-lg font-bold text-white tracking-tight">Імпорт історії успішних продажів</h2>
        <p class="text-xs text-slate-400 mt-1">
          Завантажте CSV-файл для підсилення AI-скорингу новинок на основі минулих кейсів.
        </p>
      </div>

      <!-- Dropzone Area -->
      <div
        @dragover="handleDragOver"
        @dragleave="handleDragLeave"
        @drop="handleDrop"
        class="border-2 border-dashed rounded-2xl p-8 text-center transition-all cursor-pointer relative"
        :class="[
          isDragging
            ? 'border-emerald-400 bg-emerald-500/10 scale-[1.01]'
            : 'border-slate-700/80 hover:border-slate-600 bg-slate-950/40 hover:bg-slate-950/60',
        ]"
      >
        <input
          type="file"
          accept=".csv"
          @change="handleFileInput"
          class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
        />

        <div class="flex flex-col items-center">
          <div class="w-12 h-12 rounded-2xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center mb-3">
            <UploadCloud class="w-6 h-6" />
          </div>

          <div v-if="!selectedFile">
            <p class="text-sm font-semibold text-slate-200">
              Перетягніть файл сюди або <span class="text-emerald-400 underline">оберіть на диску</span>
            </p>
            <p class="text-xs text-slate-500 mt-1">
              Підтримуються стандартні колонки: Назва, Категорія, Кількість продажів, Виручка ($), Собівартість ($), Маржинальність (%), Дата першого продажу
            </p>
          </div>

          <div v-else class="flex items-center gap-3 p-3 rounded-xl bg-slate-900 border border-slate-700 text-left">
            <FileText class="w-6 h-6 text-emerald-400 shrink-0" />
            <div>
              <div class="font-semibold text-sm text-white">{{ selectedFile.name }}</div>
              <div class="text-xs text-slate-400">
                {{ (selectedFile.size / 1024).toFixed(1) }} KB
              </div>
            </div>
            <CheckCircle2 class="w-5 h-5 text-emerald-400 ml-3" />
          </div>
        </div>
      </div>

      <!-- Error message -->
      <div v-if="error" class="mt-3 flex items-center gap-2 text-xs text-rose-400 justify-center">
        <AlertCircle class="w-4 h-4" />
        <span>{{ error }}</span>
      </div>

      <!-- Upload button -->
      <div v-if="selectedFile" class="mt-4 flex justify-center">
        <button
          @click="upload"
          :disabled="salesBoostStore.isUploading"
          class="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-semibold transition-all shadow-lg shadow-emerald-600/20 disabled:opacity-50"
        >
          <RefreshCw v-if="salesBoostStore.isUploading" class="w-4 h-4 animate-spin" />
          <span>{{ salesBoostStore.isUploading ? 'Обробка...' : 'Завантажити та обробити' }}</span>
        </button>
      </div>
    </div>
  </div>
</template>
