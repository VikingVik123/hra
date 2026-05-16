<template>
  <div class="min-h-screen" :class="isDarkMode ? 'bg-gray-900' : 'bg-gray-50'">
    <!-- Navigation Bar -->
    <nav class="border-b" :class="isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'">
      <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <span class="text-2xl">📋</span>
          <h1 class="text-xl font-bold" :class="isDarkMode ? 'text-white' : 'text-gray-900'">Interview Gen</h1>
        </div>
        <button
          @click="toggleTheme"
          class="p-2 rounded-lg transition-colors"
          :class="isDarkMode ? 'bg-gray-700 hover:bg-gray-600 text-yellow-400' : 'bg-gray-100 hover:bg-gray-200 text-gray-700'"
        >
          {{ isDarkMode ? '☀️' : '🌙' }}
        </button>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="max-w-4xl mx-auto px-6 py-12">
      <!-- Header Section -->
      <div class="text-center mb-12">
        <h2 class="text-5xl font-bold mb-4" :class="isDarkMode ? 'text-white' : 'text-gray-900'">
          Interview Questions
        </h2>
        <p class="text-gray-500 text-lg">
          Enter a job title to generate three thoughtful, role-specific interview questions.
        </p>
      </div>

      <!-- Input Form Card -->
      <div class="mb-12 p-8 rounded-xl border" :class="isDarkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'">
        <div class="flex gap-3">
          <input
            v-model="jobTitle"
            type="text"
            placeholder="Customer Success Manager"
            class="flex-1 px-4 py-3 rounded-lg border transition-colors outline-none text-lg"
            :class="[
              isDarkMode 
                ? 'bg-gray-700 border-gray-600 text-white placeholder-gray-400 focus:border-blue-500' 
                : 'bg-gray-50 border-gray-300 text-gray-900 placeholder-gray-500 focus:border-blue-500'
            ]"
            @keyup.enter="generateQuestions"
            :disabled="loading"
          />
          <button
            @click="generateQuestions"
            :disabled="loading || !jobTitle.trim()"
            class="px-8 py-3 rounded-lg font-semibold transition-colors flex items-center gap-2"
            :class="[
              loading || !jobTitle.trim()
                ? isDarkMode ? 'bg-gray-700 text-gray-500 cursor-not-allowed' : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                : isDarkMode ? 'bg-blue-600 hover:bg-blue-700 text-white' : 'bg-blue-600 hover:bg-blue-700 text-white'
            ]"
          >
            <span v-if="loading" class="animate-spin">⟳</span>
            <span v-else>🚀</span>
            <span>Generate</span>
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading && questions.length === 0" class="text-center py-12">
        <div class="animate-spin text-4xl mb-4">⟳</div>
        <p class="text-gray-500 text-lg">Generating interview questions...</p>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="mb-8 p-4 rounded-lg bg-red-100 border border-red-300">
        <p class="text-red-800 font-semibold">Error</p>
        <p class="text-red-700">{{ error }}</p>
      </div>

      <!-- Results Section -->
      <div v-if="questions.length > 0" class="space-y-6">
        <div class="text-center mb-8">
          <h3 class="text-2xl font-bold mb-2" :class="isDarkMode ? 'text-white' : 'text-gray-900'">
            Questions for {{ jobTitle }}
          </h3>
          <p class="text-gray-500">
            Generated with <span class="font-semibold capitalize">{{ selectedModel }}</span> model
          </p>
        </div>

        <!-- Questions Grid -->
        <div class="grid gap-6">
          <div
            v-for="(question, index) in questions"
            :key="index"
            class="p-6 rounded-xl border-2 transition-colors"
            :class="isDarkMode ? 'bg-gray-800 border-blue-500 hover:border-blue-400' : 'bg-white border-blue-300 hover:border-blue-500'"
          >
            <div class="flex gap-3">
              <div class="flex-shrink-0 w-8 h-8 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold text-sm">
                {{ index + 1 }}
              </div>
              <div class="flex-1">
                <p class="text-lg font-semibold mb-2" :class="isDarkMode ? 'text-white' : 'text-gray-900'">
                  {{ question.text || question }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex gap-3 mt-8 justify-center">
          <button
            @click="copyQuestions"
            class="px-6 py-3 rounded-lg font-semibold transition-colors"
            :class="isDarkMode ? 'bg-green-600 hover:bg-green-700 text-white' : 'bg-green-600 hover:bg-green-700 text-white'"
          >
            📋 Copy Questions
          </button>
          <button
            @click="reset"
            class="px-6 py-3 rounded-lg font-semibold transition-colors"
            :class="isDarkMode ? 'bg-gray-700 hover:bg-gray-600 text-white' : 'bg-gray-300 hover:bg-gray-400 text-gray-900'"
          >
            🔄 Generate New
          </button>
        </div>
      </div>

      <!-- Empty State Message -->
      <div v-if="!loading && questions.length === 0 && jobTitle.trim()" class="text-center py-12">
        <p class="text-gray-500 text-lg">Click "Generate" to create interview questions</p>
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
const isDarkMode = ref(true)

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
