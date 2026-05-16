<template>
  <div class="min-h-screen font-mono" :class="isDarkMode ? 'bg-black text-green-400' : 'bg-gray-100 text-gray-900'" style="font-family: 'Courier New', monospace;">
    <!-- Terminal Header -->
    <div class="border-b px-6 py-4" :class="isDarkMode ? 'bg-gray-800 border-green-900' : 'bg-gray-300 border-gray-400'">
      <div class="flex justify-between items-center">
        <h1 class="text-lg font-bold">$ INTERVIEW-GEN v1.0</h1>
        <button @click="toggleTheme" class="text-xs px-2 py-1 rounded transition-colors" :class="isDarkMode ? 'bg-gray-700 hover:bg-gray-600' : 'bg-gray-400 hover:bg-gray-500'">
          {{ isDarkMode ? '☀' : '🌙' }}
        </button>
      </div>
    </div>

    <!-- Terminal Content -->
    <div class="min-h-[calc(100vh-80px)] flex flex-col p-6">
      <div class="flex-1 space-y-4 max-w-4xl">
        <!-- Welcome Message -->
        <div v-if="!jobTitle && !loading" class="space-y-2">
          <p>Welcome to Interview Questions Generator</p>
          <p :class="isDarkMode ? 'text-green-500' : 'text-gray-600'">Enter a job title to generate interview questions</p>
        </div>

        <!-- Job Title Input -->
        <div class="space-y-2">
          <p :class="isDarkMode ? 'text-green-300' : 'text-gray-700'">$ job title</p>
          <div class="flex gap-2">
            <span :class="isDarkMode ? 'text-green-400' : 'text-gray-800'">&gt;</span>
            <input
              v-model="jobTitle"
              type="text"
              placeholder="Customer Success Manager"
              class="flex-1 bg-transparent outline-none"
              :class="isDarkMode ? 'text-green-400 placeholder-green-700' : 'text-gray-800 placeholder-gray-500'"
              @keyup.enter="handleJobTitleEnter"
              :disabled="loading"
            />
          </div>
        </div>

        <!-- Model Selection Button (shows after job title entered) -->
        <div v-if="jobTitle.trim()" class="space-y-2">
          <p :class="isDarkMode ? 'text-green-300' : 'text-gray-700'">$ model</p>
          <div class="flex gap-2">
            <span :class="isDarkMode ? 'text-green-400' : 'text-gray-800'">&gt;</span>
            <button
              @click="showModelModal = true"
              :disabled="loading"
              class="text-left flex-1 px-3 py-1 rounded transition-colors"
              :class="isDarkMode ? 'bg-gray-800 text-green-400 hover:bg-gray-700' : 'bg-gray-300 text-gray-800 hover:bg-gray-400'"
            >
              {{ selectedModel }}
            </button>
          </div>
        </div>

        <!-- Generate Button -->
        <div v-if="jobTitle.trim()" class="space-y-2">
          <p :class="isDarkMode ? 'text-green-300' : 'text-gray-700'">$</p>
          <button
            @click="generateQuestions"
            :disabled="loading"
            class="flex items-center gap-2 transition-colors"
            :class="[
              loading || !jobTitle.trim()
                ? isDarkMode ? 'text-gray-600' : 'text-gray-500'
                : isDarkMode ? 'text-green-400 hover:text-green-300' : 'text-gray-800 hover:text-gray-600'
            ]"
          >
            <span v-if="loading" class="animate-spin">⟳</span>
            <span v-else>*</span>
            <span>generate</span>
          </button>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="space-y-2 mt-6" :class="isDarkMode ? 'text-green-500' : 'text-gray-600'">
          <p>⟳ generating questions...</p>
          <p class="animate-pulse">waiting for API response...</p>
        </div>

        <!-- Error Display -->
        <div v-if="error" class="border p-4 mt-6" :class="isDarkMode ? 'border-red-600 text-red-500' : 'border-red-400 text-red-600'">
          <p>ERROR: {{ error }}</p>
        </div>

        <!-- Results Display -->
        <div v-if="questions.length > 0 && !loading" class="mt-8 space-y-4">
          <div :class="isDarkMode ? 'text-green-300' : 'text-gray-700'">
            <p>Questions for: <span :class="isDarkMode ? 'text-cyan-400' : 'text-blue-700'" class="font-bold">{{ jobTitle }}</span></p>
            <p :class="isDarkMode ? 'text-green-500' : 'text-gray-600'" class="text-sm">Model: {{ selectedModel }}</p>
          </div>

          <div class="border p-4 space-y-4" :class="isDarkMode ? 'border-green-600' : 'border-gray-400'">
            <div
              v-for="(question, index) in questions"
              :key="index"
              class="border-l-2 pl-4"
              :class="isDarkMode ? 'border-green-600' : 'border-gray-400'"
            >
              <div class="font-bold" :class="isDarkMode ? 'text-green-400' : 'text-gray-800'">
                Q{{ index + 1 }}: <span :class="isDarkMode ? 'text-cyan-300' : 'text-blue-600'">{{ question.text || question }}</span>
              </div>
              <div class="text-sm mt-1" :class="isDarkMode ? 'text-green-600' : 'text-gray-600'">
                Category: <span :class="isDarkMode ? 'text-green-500' : 'text-gray-700'">{{ question.category }}</span>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="mt-6 space-y-2">
            <button
              @click="copyQuestions"
              class="transition-colors"
              :class="isDarkMode ? 'text-green-400 hover:text-green-300' : 'text-gray-800 hover:text-gray-600'"
            >
              $ <span class="underline">copy</span> - Copy to clipboard
            </button>
            <button
              @click="reset"
              class="transition-colors"
              :class="isDarkMode ? 'text-green-400 hover:text-green-300' : 'text-gray-800 hover:text-gray-600'"
            >
              $ <span class="underline">reset</span> - Start over
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Model Selection Modal -->
    <div v-if="showModelModal" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
      <div class="rounded-lg p-6 max-w-sm w-full mx-4 border-2" :class="isDarkMode ? 'bg-gray-900 border-green-600' : 'bg-gray-50 border-gray-400'">
        <p class="font-bold mb-4" :class="isDarkMode ? 'text-green-400' : 'text-gray-900'">Select Model:</p>
        
        <div class="space-y-3 mb-6">
          <button
            v-for="model in ['gemini', 'groq']"
            :key="model"
            @click="selectModel(model)"
            class="w-full p-3 rounded border-2 text-left capitalize font-semibold transition-all"
            :class="[
              selectedModel === model
                ? isDarkMode ? 'border-cyan-400 bg-gray-800 text-cyan-400' : 'border-blue-600 bg-blue-50 text-blue-900'
                : isDarkMode ? 'border-gray-700 bg-gray-800 text-green-400 hover:border-green-600' : 'border-gray-300 bg-gray-100 text-gray-900 hover:bg-gray-200'
            ]"
          >
            {{ model }}
            <span v-if="selectedModel === model" class="block text-xs mt-1">✓ selected</span>
          </button>
        </div>

        <button
          @click="showModelModal = false"
          class="w-full px-4 py-2 rounded font-semibold transition-colors"
          :class="isDarkMode ? 'bg-gray-800 hover:bg-gray-700 text-green-400 border border-green-600' : 'bg-gray-300 hover:bg-gray-400 text-gray-900'"
        >
          Done
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const jobTitle = ref('')
const selectedModel = ref('gemini')
const questions = ref([])
const loading = ref(false)
const error = ref('')
const isDarkMode = ref(true)
const showModelModal = ref(false)

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

console.log('🌐 API_BASE_URL:', API_BASE_URL)

onMounted(() => {
  console.log('✅ App mounted!')
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
  console.log('🔹 Job title entered:', jobTitle.value)
  // Job title is entered, user can now select model or directly generate
}

const selectModel = (model) => {
  console.log('🔹 Model selected:', model)
  selectedModel.value = model
  showModelModal.value = false
}

const generateQuestions = async () => {
  console.log('🔹 Generate button clicked!')
  
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
    console.log('📊 Response OK:', response.ok)

    if (!response.ok) {
      const errorData = await response.json()
      console.error('❌ Error response:', errorData)
      throw new Error(errorData.detail || `HTTP ${response.status}: Failed to generate questions`)
    }

    const data = await response.json()
    console.log('✅ Success! Got', data.questions?.length || 0, 'questions')
    console.log('📄 Questions:', data.questions)
    questions.value = data.questions || []
  } catch (err) {
    error.value = err.message || 'An error occurred while generating questions'
    console.error('❌ Full error:', err)
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
  selectedModel.value = 'gemini'
}
</script>

<style scoped>
input:disabled,
button:disabled {
  opacity: 0.6;
}
</style>