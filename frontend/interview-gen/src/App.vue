<template>
  <div class="min-h-screen transition-colors duration-300" :class="isDarkMode ? 'bg-gray-900 text-gray-100' : 'bg-gray-50 text-gray-900'">
    
    <header class="w-full border-b backdrop-blur sticky top-0 z-50 transition-colors" :class="isDarkMode ? 'bg-gray-900/80 border-gray-800' : 'bg-white/80 border-gray-200'">
      <div class="max-w-2xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
          <h1 class="text-base font-bold tracking-wider" :class="isDarkMode ? 'text-white' : 'text-gray-900'">IQG</h1>
        </div>
        <button
          @click="toggleTheme"
          class="p-2 rounded-xl transition-all duration-200 hover:scale-105 active:scale-95 opacity-60 hover:opacity-100"
          :class="isDarkMode ? 'text-gray-400' : 'text-gray-400'"
          aria-label="Toggle Theme"
        >
          {{ isDarkMode ? '☀️' : '🌙' }}
        </button>
      </div>
    </header>

    <main class="max-w-2xl mx-auto px-4 sm:px-6 py-8 sm:py-12 flex flex-col min-h-[calc(100vh-56px)]">
      
      <section class="text-center mb-8 sm:mb-10">
        <h2 class="text-3xl sm:text-4xl font-extrabold tracking-tight mb-3" :class="isDarkMode ? 'text-white' : 'text-gray-900'">
          Interview Questions
        </h2>
        <p class="text-sm text-gray-500 dark:text-gray-400 max-w-md mx-auto">
          Enter a job title to generate three thoughtful, role-specific interview questions.
        </p>
      </section>

      <section class="w-full mb-6">
        <div class="rounded-2xl border p-5 sm:p-6 shadow-sm transition-all" :class="isDarkMode ? 'bg-gray-800 border-gray-700/60' : 'bg-white border-gray-200'">
          <div class="space-y-4">
            <div>
              <label class="block text-xs font-semibold uppercase tracking-wider mb-2 text-gray-400">Job Title</label>
              <input
                v-model="jobTitle"
                type="text"
                placeholder="e.g. Customer Support Manager"
                class="w-full px-4 py-2.5 rounded-xl border outline-none transition-all text-sm sm:text-base focus:ring-2 focus:ring-blue-500/20"
                :class="[
                  isDarkMode
                    ? 'bg-gray-700/50 border-gray-600 text-white placeholder-gray-500 focus:border-blue-500'
                    : 'bg-white border-gray-300 text-gray-900 placeholder-gray-400 focus:border-blue-500'
                ]"
                @keyup.enter="generateQuestions"
                :disabled="loading"
              />
            </div>
            
            <div class="flex gap-2 w-full">
              <button
                @click="selectedModel = 'gemini'"
                :disabled="loading"
                class="px-3 py-2 rounded-lg border font-medium transition-all text-xs flex items-center justify-center gap-1.5 cursor-pointer disabled:cursor-not-allowed"
                :class="[
                  selectedModel === 'gemini'
                    ? isDarkMode
                      ? 'bg-blue-600 border-blue-500 text-white shadow-lg shadow-blue-500/30'
                      : 'bg-blue-600 border-blue-600 text-white shadow-lg shadow-blue-500/30'
                    : isDarkMode
                      ? 'bg-gray-700/50 border-gray-600 text-gray-300 hover:border-gray-500'
                      : 'bg-gray-100 border-gray-300 text-gray-700 hover:border-gray-400'
                ]"
              >
                <span></span>
                <span>Gemini</span>
              </button>
              
              <button
                @click="selectedModel = 'groq'"
                :disabled="loading"
                class="px-3 py-2 rounded-lg border font-medium transition-all text-xs flex items-center justify-center gap-1.5 cursor-pointer disabled:cursor-not-allowed"
                :class="[
                  selectedModel === 'groq'
                    ? isDarkMode
                      ? 'bg-blue-600 border-blue-500 text-white shadow-lg shadow-blue-500/30'
                      : 'bg-blue-600 border-blue-600 text-white shadow-lg shadow-blue-500/30'
                    : isDarkMode
                      ? 'bg-gray-700/50 border-gray-600 text-gray-300 hover:border-gray-500'
                      : 'bg-gray-100 border-gray-300 text-gray-700 hover:border-gray-400'
                ]"
              >
                <span></span>
                <span>Groq</span>
              </button>
            </div>
              
            <button
              @click="generateQuestions"
              :disabled="loading || !jobTitle.trim()"
              class="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-xl flex items-center justify-center gap-2 transition-all shadow-sm active:scale-[0.98] disabled:opacity-40 disabled:cursor-not-allowed disabled:transform-none text-sm w-full"
            >
              <span v-if="loading" class="animate-spin text-base">⟳</span>
              {{ loading ? 'Generating...' : 'Generate' }}
            </button>
          </div>
        </div>
      </section>

      <div v-if="error" class="w-full mb-6">
        <div class="p-4 rounded-xl border flex items-center gap-3 text-sm" :class="isDarkMode ? 'bg-red-950/40 border-red-900 text-red-200' : 'bg-red-50 border-red-200 text-red-700'">
          <span></span>
          <p>{{ error }}</p>
        </div>
      </div>

      <div v-if="copied" class="w-full mb-6">
        <div class="p-4 rounded-xl border flex items-center gap-3 text-sm bg-green-500/10 border-green-500/20 text-green-500">
          <span>✓</span>
          <p>Questions successfully copied to clipboard!</p>
        </div>
      </div>

      <div v-if="loading && questions.length === 0" class="text-center py-12 flex flex-col items-center justify-center flex-1">
        <div class="animate-spin text-4xl text-blue-500 mb-4">⟳</div>
        <p class="text-gray-500 text-sm">Crafting tailored technical questions...</p>
      </div>

      <div v-if="!loading && questions.length === 0" class="text-center py-12 border-2 border-dashed rounded-2xl flex flex-col items-center justify-center flex-1 p-6" :class="isDarkMode ? 'border-gray-800' : 'border-gray-200'">
        <div class="text-4xl mb-3 opacity-80">💭</div>
        <p class="text-gray-400 text-sm">Your structured interview pool will populate here.</p>
      </div>

      <section v-if="questions.length > 0 && !loading" class="w-full mb-6 animate-fadeIn">
        <div class="rounded-2xl border p-5 sm:p-6" :class="isDarkMode ? 'bg-gray-800 border-gray-700/60' : 'bg-white border-gray-200'">
          
          <div class="text-center mb-6 border-b pb-4" :class="isDarkMode ? 'border-gray-700' : 'border-gray-100'">
            <h3 class="text-xl font-bold mb-1" :class="isDarkMode ? 'text-white' : 'text-gray-900'">
              Target: {{ generatedJobTitle }}
            </h3>
            <p class="text-xs text-gray-400">
              Engineered via <span class="font-semibold uppercase tracking-wider text-blue-500">{{ generatedModel }}</span> Engine
            </p>
          </div>

          <div class="space-y-4 mb-6">
            <div
              v-for="(question, index) in questions"
              :key="index"
              class="p-4 rounded-xl border transition-all hover:border-blue-500/40"
              :class="isDarkMode ? 'bg-gray-700/30 border-gray-700' : 'bg-gray-50/70 border-gray-200'"
            >
              <div class="flex gap-3">
                <div class="flex-shrink-0 w-6 h-6 bg-blue-500/10 text-blue-500 flex items-center justify-center rounded-lg text-xs font-bold">
                  {{ index + 1 }}
                </div>
                <div class="flex-1 space-y-2">
                  <p class="text-sm sm:text-base leading-relaxed font-medium" :class="isDarkMode ? 'text-gray-100' : 'text-gray-800'">
                    {{ question.text || question }}
                  </p>
                  
                  <div v-if="question.category" class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-md text-xs font-medium bg-blue-500/10 text-blue-400 border border-blue-500/10 capitalize">
                    <span class="w-1 h-1 rounded-full bg-blue-400"></span>
                    {{ question.category }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="flex flex-col sm:flex-row gap-3 justify-end border-t pt-4" :class="isDarkMode ? 'border-gray-700' : 'border-gray-100'">
            <button
              @click="reset"
              class="px-4 py-2 font-medium rounded-xl transition-all text-sm w-full sm:w-auto order-2 sm:order-1 text-center"
              :class="isDarkMode ? 'bg-gray-700 hover:bg-gray-600 text-gray-300' : 'bg-gray-100 hover:bg-gray-200 text-gray-700'"
            >
              Clear
            </button>
            <button
              @click="copyQuestions"
              class="px-5 py-2 bg-green-600 hover:bg-green-700 text-white font-medium rounded-xl transition-all text-sm w-full sm:w-auto order-1 sm:order-2 flex items-center justify-center gap-1.5 shadow-sm active:scale-95"
            >
              <span></span> Copy
            </button>
          </div>
        </div>
      </section>

      <footer class="w-full text-center py-6 text-xs text-gray-400 mt-auto border-t" :class="isDarkMode ? 'border-gray-800' : 'border-gray-200'">
        <p>Built for focused interview prep.</p>
      </footer>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const jobTitle = ref('')
const selectedModel = ref('gemini')
const questions = ref([])
const loading = ref(false)
const error = ref('')
const isDarkMode = ref(false)
const copied = ref(false)

// Snapshots to keep title updates clean during active generations
const generatedJobTitle = ref('')
const generatedModel = ref('')

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://hra-be.vercel.app'

onMounted(() => {
  // Sync localstorage theme state reliably on initialization
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    isDarkMode.value = savedTheme === 'dark'
  } else {
    isDarkMode.value = window.matchMedia('(prefers-color-scheme: dark)').matches
  }
})

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
}

const generateQuestions = async () => {
  if (!jobTitle.value.trim()) {
    error.value = 'Please enter a job title'
    return
  }

  loading.value = true
  error.value = ''
  copied.value = false

  try {
    const response = await fetch(`${API_BASE_URL}/api/recommendations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        job_title: jobTitle.value.trim(),
        model: selectedModel.value,
      }),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || 'Failed to extract recommendations')
    }

    const data = await response.json()
    questions.value = data.questions || []
    
    // Pin metadata state to current response values
    generatedJobTitle.value = jobTitle.value
    generatedModel.value = selectedModel.value
  } catch (err) {
    error.value = err.message || 'An error occurred while generating questions'
    console.error('Generation error:', err)
    questions.value = []
  } finally {
    loading.value = false
  }
}

const copyQuestions = () => {
  if (!questions.value.length) return
  
  const text = questions.value
    .map((q, i) => `${i + 1}. ${q.text || q}${q.category ? ` [Category: ${q.category}]` : ''}`)
    .join('\n\n')

  navigator.clipboard.writeText(text)
    .then(() => {
      copied.value = true
      setTimeout(() => { copied.value = false }, 3500)
    })
    .catch(() => {
      error.value = 'Could not copy data automatically to clipboard.'
    })
}

const reset = () => {
  jobTitle.value = ''
  questions.value = []
  error.value = ''
  copied.value = false
}
</script>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(4px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fadeIn {
  animation: fadeIn 0.3s ease-out forwards;
}
</style>