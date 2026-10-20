import { ref  } from 'vue'
import { defineStore } from 'pinia'
import type { SummarizeResponse } from '@/types/api'

export const useSummarizeStore = defineStore('summarize', () => {
  const result = ref<SummarizeResponse | null>(null)
  function setResult(newResult: SummarizeResponse | null) {
    result.value = newResult
  }
  return { result, setResult }
})
