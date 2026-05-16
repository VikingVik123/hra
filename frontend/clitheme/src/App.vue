<template>
  <div class="min-h-screen font-mono" style="font-family: 'Courier New', monospace;">
    <!-- Terminal Window -->
    <div class="flex flex-col h-screen" :class="themeClasses.container">
      <!-- Terminal Header -->
      <div class="px-4 py-2 flex items-center justify-between border-b" :class="themeClasses.header">
        <div class="flex gap-2">
          <div class="w-3 h-3 rounded-full bg-red-500"></div>
          <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
          <div class="w-3 h-3 rounded-full bg-green-500"></div>
        </div>
        <span class="text-xs" :class="themeClasses.headerText">BASH — INTERVIEW.SH</span>
        <button
          @click="toggleTheme"
          class="text-xs transition-colors px-2 py-1 rounded"
          :class="themeClasses.themeBtn"
          :title="isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'"
        >
          {{ isDarkMode ? '☀' : '🌙' }}
        </button>
      </div>

      <!-- Terminal Content -->
      <div class="flex-1 overflow-y-auto p-6 space-y-4" :class="themeClasses.content">
        <!-- Logo/Header -->
        <div class="text-center mb-8 text-2xl font-bold" :class="themeClasses.logo">
          <div class="mb-2">╔══════════════════════════╗</div>
          <div>║   INTERVIEW-GEN          ║</div>
          <div class="mb-2">╚══════════════════════════╝</div>
        </div>

        <!-- Welcome Message -->
        <div v-if="!started" class="space-y-4">
          <div :class="themeClasses.text">
            <p>Welcome to Interview Questions Generator v1.0</p>
            <p class="mt-2" :class="themeClasses.subtext">Enter a job title to generate three thoughtful, role-specific</p>
            <p :class="themeClasses.subtext">interview questions.</p>
          </div>

          <!-- Job Title Input -->
          <div class="mt-6">
            <p :class="themeClasses.label">$ job title</p>
            <div class="flex gap-2 mt-1">
              <span :class="themeClasses.prompt">&gt;</span>
              <input
                v-model="jobTitle"
                type="text"
                placeholder="Customer Success Manager"
                class="flex-1 bg-transparent outline-none"
                :class="themeClasses.input"
                @keyup.enter="handleJobTitleEnter"
                :disabled="loading"
              />
            </div>
          </div>

          <!-- Model Selection -->
          <div v-if="jobTitle.trim() && started" class="mt-6">
            <p :class="themeClasses.label">$ model</p>
            <div class="flex gap-2 mt-1">
              <span :class="themeClasses.prompt">&gt;</span>
              <select
                v-model="selectedModel"
                class="bg-transparent outline-none"
                :class="themeClasses.input"
              >
                <option value="gemini">gemini</option>
                <option value="groq">groq</option>
              </select>
            </div>
          </div>

          <!-- Generate Command -->
          <div v-if="started" class="mt-6">
            <p :class="themeClasses.label">$</p>
            <button
              @click="handleGenerateClick"
              class="flex items-center gap-2 transition-colors"
              :class="themeClasses.button"
              :disabled="loading"
            >
              <span v-if="loading" class="animate-spin">⟳</span>
              <span v-else>*</span>
              <span>generate</span>
            </button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading && !questions.length" :class="themeClasses.loading">
          waiting for input<span class="animate-pulse">...</span>
        </div>

        <!-- Error Display -->
        <div v-if="error" class="border p-4" :class="themeClasses.error">
          <p>ERROR: {{ error }}</p>
        </div>

        <!-- Results Display -->
        <div v-if="questions.length > 0" class="space-y-4 mt-8">
          <div :class="themeClasses.text">
            <p>Questions for: <span class="font-bold" :class="themeClasses.highlight">{{ jobTitle }}</span></p>
            <p class="mt-2" :class="themeClasses.subtext">Using model: <span :class="themeClasses.highlight">{{ selectedModel }}</span></p>
          </div>

          <div class="border p-4 space-y-4 mt-6" :class="themeClasses.resultBox">
            <div
              v-for="(question, index) in questions"
              :key="question.id"
              class="border-l-2 pl-4"
              :class="themeClasses.questionItem"
            >
              <div class="font-bold" :class="themeClasses.questionText">
                Q{{ index + 1 }}: <span :class="themeClasses.highlight">{{ question.text }}</span>
              </div>
              <div class="text-sm mt-1" :class="themeClasses.category">
                Category: <span :class="themeClasses.categoryName">{{ question.category }}</span>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="mt-6 space-y-2">
            <button
              @click="reset"
              class="transition-colors"
              :class="themeClasses.button"
            >
              $ <span class="underline">reset</span> - Generate new questions
            </button>
            <button
              @click="copyQuestions"
              class="transition-colors"
              :class="themeClasses.button"
            >
              $ <span class="underline">copy</span> - Copy questions to clipboard
            </button>
          </div>
        </div>
      </div>

      <!-- Terminal Footer -->
      <div class="px-6 py-3 border-t text-xs" :class="themeClasses.footer">
        <p>INTERVIEW-GEN v1.0 — Type <span :class="themeClasses.highlight">help</span> for commands</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'

const jobTitle = ref('')
const selectedModel = ref('gemini')
const questions = ref([])
const loading = ref(false)
const error = ref('')
const isDarkMode = ref(true)
const started = ref(false)
const modelSelected = ref(false)

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

console.log('API Base URL:', API_BASE_URL)

const themeClasses = computed(() => {
  return {
    container: isDarkMode.value ? 'bg-black text-green-400' : 'bg-gray-100 text-gray-900',
    header: isDarkMode.value ? 'bg-gray-800 border-green-900' : 'bg-gray-300 border-gray-400',
    headerText: isDarkMode.value ? 'text-gray-400' : 'text-gray-600',
    themeBtn: isDarkMode.value ? 'text-gray-400 hover:text-green-400' : 'text-gray-600 hover:text-gray-800',
    content: isDarkMode.value ? 'bg-black' : 'bg-gray-100',
    logo: isDarkMode.value ? 'text-green-400' : 'text-gray-800',
    text: isDarkMode.value ? 'text-green-400' : 'text-gray-800',
    subtext: isDarkMode.value ? 'text-green-500' : 'text-gray-700',
    label: isDarkMode.value ? 'text-green-300' : 'text-gray-700',
    prompt: isDarkMode.value ? 'text-green-400' : 'text-gray-800',
    input: isDarkMode.value ? 'text-green-400 placeholder-green-700' : 'text-gray-800 placeholder-gray-500',
    button: isDarkMode.value ? 'text-green-400 hover:text-green-300' : 'text-gray-800 hover:text-gray-600',
    loading: isDarkMode.value ? 'text-green-500' : 'text-gray-700',
    error: isDarkMode.value ? 'text-red-500 border-red-500' : 'text-red-700 border-red-700',
    highlight: isDarkMode.value ? 'text-cyan-400' : 'text-blue-700',
    resultBox: isDarkMode.value ? 'border-green-600' : 'border-gray-400',
    questionItem: isDarkMode.value ? 'border-green-600' : 'border-gray-400',
    questionText: isDarkMode.value ? 'text-green-400' : 'text-gray-800',
    category: isDarkMode.value ? 'text-green-600' : 'text-gray-600',
    categoryName: isDarkMode.value ? 'text-green-500' : 'text-gray-700',
    footer: isDarkMode.value ? 'bg-gray-900 border-green-900 text-green-600' : 'bg-gray-300 border-gray-400 text-gray-700',
  }
})

onMounted(() => {
  console.log('✅ App mounted successfully!')
  console.log('🌐 API_BASE_URL:', API_BASE_URL)
  
  // Check localStorage for theme preference
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme) {
    isDarkMode.value = savedTheme === 'dark'
  }
})

const toggleTheme = () => {
  isDarkMode.value = !isDarkMode.value
  localStorage.setItem('theme', isDarkMode.value ? 'dark' : 'light')
}

const handleJobTitleEnter = () => {
  console.log('🔹 Enter key pressed, jobTitle:', jobTitle.value)
  if (jobTitle.value.trim()) {
    started.value = true
    console.log('🟢 started set to true')
  }
}

const handleGenerateClick = async () => {
  console.log('🔹 Generate button clicked!')
  console.log('jobTitle:', jobTitle.value)
  console.log('selectedModel:', selectedModel.value)
  
  if (!jobTitle.value.trim()) {
    error.value = 'Please enter a job title'
    console.error('❌ Job title is empty')
    return
  }

  loading.value = true
  error.value = ''
  questions.value = []

  const payload = {
    job_title: jobTitle.value,
    model: selectedModel.value,
  }

  const url = `${API_BASE_URL}/api/recommendations`
  console.log('🌐 Sending POST to:', url)
  console.log('📦 Payload:', payload)

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })

    console.log('📊 Response status:', response.status)

    if (!response.ok) {
      const errorData = await response.json()
      console.error('❌ Error response:', errorData)
      throw new Error(errorData.detail || `HTTP ${response.status}: Failed to generate questions`)
    }

    const data = await response.json()
    console.log('✅ Success! Got', data.questions?.length || 0, 'questions')
    questions.value = data.questions || []
  } catch (err) {
    error.value = err.message || 'An error occurred while generating questions'
    console.error('❌ Full error:', err)
  } finally {
    loading.value = false
  }
}

const reset = () => {
  jobTitle.value = ''
  selectedModel.value = 'gemini'
  questions.value = []
  error.value = ''
  started.value = false
  modelSelected.value = false
}

const copyQuestions = () => {
  const text = questions.value
    .map((q, i) => `Q${i + 1}: ${q.text}\nCategory: ${q.category}`)
    .join('\n\n')
  
  navigator.clipboard.writeText(text).then(() => {
    // Show copy success message
    const oldError = error.value
    error.value = 'Questions copied to clipboard!'
    setTimeout(() => {
      error.value = oldError
    }, 2000)
  })
}
</script>

<style scoped>
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

.dark ::-webkit-scrollbar-thumb {
  background: #475569;
}

.dark ::-webkit-scrollbar-thumb:hover {
  background: #64748b;
}
</style>
