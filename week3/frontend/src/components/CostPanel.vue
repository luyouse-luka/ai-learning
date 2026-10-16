<script setup lang="ts">
// TODO: Import SummarizeResponse from '@/types/api'.
import type { SummarizeResponse } from '@/types/api';
import {inject} from 'vue';
import type { Ref } from 'vue'
const result = inject<Ref<SummarizeResponse | null>>('result')

// TODO: Declare a required result prop of type SummarizeResponse.

</script>

<template>
  <section v-if="result">
    <h2>本次费用</h2>
    <!-- TODO: Display cost and model from the result prop. -->
       <p>费用：{{ result.cost }}</p>
  <p>模型：{{ result.model }}</p>
  </section>
</template>
