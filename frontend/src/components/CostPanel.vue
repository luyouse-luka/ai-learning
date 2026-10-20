<script setup lang="ts">
// TODO: Import SummarizeResponse from '@/types/api'.

import { useSummarizeStore } from '@/stores/summarize'
// TODO: Declare a required result prop of type SummarizeResponse.

const summarizeStore = useSummarizeStore()
</script>

<template>
  <section v-if="summarizeStore.result">
    <h2>本次费用</h2>
    <!-- TODO: Display cost and model from the result prop. -->
       <p>费用：{{ summarizeStore.result.cost }}</p>
  <p>模型：{{ summarizeStore.result.model }}</p>
  </section>
</template>
