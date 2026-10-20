<script setup lang="ts">
import type { SummarizeResponse } from '@/types/api'
import { computed } from 'vue'

// TODO: Declare a required result prop of type SummarizeResponse.
const props  = defineProps<{
result: SummarizeResponse
}>()
const paragraphs = computed(() => props.result.summary.split('\n\n').map(p => p.trim()).filter(p => p.length > 0))
// split('\n\n') 按两个连续换行切开，得到字符串数组。
// .map(...)：逐段处理。trim() 去掉每段首尾的空格和换行，包括模型输出的全角缩进空格。
// .filter(...)：只保留长度大于 0 的段落，避免生成空白 <p>。
</script>

<template>
    <!-- TODO: Move the result heading, summary, metadata, and truncation warning here. -->

    <section >
    <h2>结果</h2>
    <p>input_tokens: {{ result?.input_tokens }}</p>
    <p>output_tokens: {{ result?.output_tokens }}</p>
    <p>cost: {{ result?.cost }}</p>
    <p>model: {{ result?.model }}</p>
    <p v-if="props.result.truncated">⚠️ 警告：内容被截断，请换一个 PDF</p>
    <p v-for="(paragraph, index) in paragraphs" :key="index" class="summary">
   {{ paragraph }}
  </p>
  </section>
</template>

<style scoped>
/* Move the summary style here with the markup. */
.summary {
  white-space: pre-wrap;
  text-indent: 2em;
}
</style>
