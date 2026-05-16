<template>
  <div class="min-h-screen" :class="isDarkMode ? 'bg-gray-900' : 'bg-white'">
    <!-- Header with Theme Toggle -->
    <div class="w-full border-b" :class="isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'">
      <div class="max-w-4xl mx-auto px-6 py-2 flex items-center justify-between">
        <div>
          <h1 class="text-sm font-bold" :class="isDarkMode ? 'text-white' : 'text-gray-900'">IQG</h1>
        </div>
        <button
          @click="toggleTheme"
          class="p-2 rounded-lg transition-colors"
          :class="isDarkMode ? 'bg-gray-700 hover:bg-gray-600 text-yellow-400' : 'bg-gray-100 hover:bg-gray-200 text-gray-700'"
        >
          {{ isDarkMode ? '☀️' : '🌙' }}
        </button>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex flex-col items-center justify-center min-h-[calc(100vh-80px)] px-6">
      <!-- Title Section -->
      <div class="w-full text-center mb-8">
        <h2 class="text-5xl font-bold mb-2" :class="isDarkMode ? 'text-white' : 'text-gray-900'">Interview Questions</h2>
        <p class="text-gray-500 text-base">Enter a job title to generate three thoughtful, role-specific interview questions.</p>
      </div>

      <!-- Input Card -->
      <div class="w-full max-w-2xl mb-8">
        <div class="rounded-lg border p-6" :class="isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-300'">
          <div class="flex gap-3 mb-4">
            <input
              v-model="jobTitle"
              type="text"
              placeholder="Customer Success Manager"
              class="flex-1 px-4 py-2 rounded border outline-none transition-colors"
              :class="[
                isDarkMode
                  ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400 focus:border-blue-500'
                  : 'bg-white border-gray-300 text-gray-900 placeholder-gray-500 focus:border-blue-500'
              ]"
              @keyup.enter="generateQuestions"
              :disabled="loading"
            />
          </div>
          <div class="flex gap-3">
            <select
              v-model="selectedModel"
              class="flex-1 px-4 py-2 rounded border outline-none transition-colors"
              :class="[
                isDarkMode
                  ? 'bg-gray-700 border-gray-600 text-white focus:border-blue-500'
                  : 'bg-white border-gray-300 text-gray-900 focus:border-blue-500'
              ]"
              :disabled="loading"
            >
              <option value="gemini">Gemini</option>
              <option value="groq">Groq</option>
            </select>
            <button
              @click="generateQuestions"
              :disabled="loading || !jobTitle.trim()"
              class="px-6 py-2 bg-black text-white font-semibold rounded flex items-center gap-2 hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="loading" class="animate-spin">⟳</span>
              Generate
            </button>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading && questions.length === 0" class="text-center py-12">
        <div class="animate-spin text-4xl mb-4">⟳</div>
        <p class="text-gray-500 text-lg">Generating interview questions...</p>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="w-full max-w-2xl mb-8">
        <div class="p-4 rounded-lg" :class="isDarkMode ? 'bg-red-900 border border-red-700 text-red-200' : 'bg-red-50 border border-red-200 text-red-700'">
          {{ error }}
        </div>
      </div>

      <!-- Results Section -->
      <div v-if="questions.length > 0" class="w-full max-w-2xl mb-8">
        <div class="rounded-lg border p-6" :class="isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-300'">
          <div class="text-center mb-6">
            <h3 class="text-2xl font-bold mb-2" :class="isDarkMode ? 'text-white' : 'text-gray-900'">
              Questions for {{ jobTitle }}
            </h3>
            <p class="text-gray-500 text-sm">
              Generated with <span class="font-semibold capitalize">{{ selectedModel }}</span> model
            </p>
          </div>

          <!-- Questions List -->
          <div class="space-y-4 mb-6">
            <div
              v-for="(question, index) in questions"
              :key="index"
              class="p-4 rounded border"
              :class="isDarkMode ? 'bg-gray-700 border-gray-600' : 'bg-gray-50 border-gray-200'"
            >
              <div class="flex gap-3">
                <div class="flex-shrink-0 w-6 h-6 bg-blue-500 text-white flex items-center justify-center rounded-full text-xs font-bold">
                  {{ index + 1 }}
                </div>
                <p class="text-sm leading-relaxed" :class="isDarkMode ? 'text-gray-100' : 'text-gray-900'">
                  {{ question.text || question }}
                </p>
              </div>
            </div>
          </div>

          <div class="flex gap-3 justify-center">
            <button
              @click="copyQuestions"
              class="px-4 py-2 bg-green-600 text-white font-semibold rounded hover:bg-green-700 transition-colors"
            >
              Copy Questions
            </button>
            <button
              @click="reset"
              class="px-4 py-2 font-semibold rounded transition-colors"
              :class="isDarkMode ? 'bg-gray-700 hover:bg-gray-600 text-white' : 'bg-gray-300 hover:bg-gray-400 text-gray-900'"
            >
              Generate New
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && questions.length === 0 && !jobTitle.trim()" class="text-center py-12">
        <div class="text-5xl mb-3">💭</div>
        <p class="text-gray-500 text-base">Your interview questions will appear here.</p>
      </div>

      <!-- Footer -->
      <div class="w-full text-center py-6 text-xs text-gray-500 border-t mt-12" :class="isDarkMode ? 'border-gray-700' : 'border-gray-200'">
        <p>Built for focused interview prep.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const jobTitle = ref('')
const selectedModel = ref('gemini')
const questions = ref([])
const loading = ref(false)
const error = ref('')
const isDarkMode = ref(false)

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

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
  questions.value = []

  try {
    const response = await fetch(`${API_BASE_URL}/api/recommendations`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        job_title: jobTitle.value,
        model: selectedModel.value,
      }),
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Failed to generate questions')
    }

    const data = await response.json()
    questions.value = data.questions || []
  } catch (err) {
    error.value = err.message || 'An error occurred while generating questions'
    console.error('Generation error:', err)
  } finally {
    loading.value = false
  }
}

const copyQuestions = () => {
  const text = questions.value
    .map((q, i) => `${i + 1}. ${q.text || q}`)
    .join('\n\n')

  navigator.clipboard.writeText(text).then(() => {
    alert('Questions copied to clipboard!')
  }).catch(() => {
    alert('Failed to copy to clipboard')
  })
}

const reset = () => {
  jobTitle.value = ''
  questions.value = []
  error.value = ''
}
</script>

<style scoped>
input:disabled,
button:disabled {
  opacity: 0.6;
}
</style>
