<script setup lang="ts">
// Day 5 · 第一个组件：选文件 + 上传按钮
// 今天只做「选」和「点」，真正发请求是 Day 6（Axios + UI 三态机）
// Day 4 的契约类型在 @/types/api.ts，今天用不上，Day 6 接上

// ---------------------------------------------------------------
// TODO【5.1】从 vue 引入 ref
//   一行 import。只引 ref，不要引 reactive —— 今天三个状态没有一个适合 reactive
// ---------------------------------------------------------------
import { ref } from 'vue'

// ---------------------------------------------------------------
// TODO【5.2】三个响应式状态，各一行
//   selectedFile : 选中的文件，没选时是 null  → 类型标注 ref<File | null>(null)
//   isUploading  : 是否正在上传（今天不会真变 true，先建出来给 Day 6 用）
//   errorMsg     : 给用户看的错误文案，没错时是空串
//   ⚠️ script 里读写这三个必须带 .value；模板里不带（自动解包）
// ---------------------------------------------------------------
const selectedFile = ref<File | null>(null)
const isUploading = ref(false)
const errorMsg = ref('')

// ---------------------------------------------------------------
// TODO【5.3】handleFileChange(e: Event)
//   file input 用不了 v-model（它的 value 是只读的），只能在 change 事件里读
//   步骤：① e.target 断言成 HTMLInputElement ② 取 .files?.[0] ③ 写进 5.2 的状态
//   ⚠️ 用户点了「取消」时 files 是空的，这时该存 null，不是 undefined
// ---------------------------------------------------------------
function handleFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  selectedFile.value = input.files?.[0] ?? null
}

// ---------------------------------------------------------------
// TODO【5.7】读了学源才答得出的一题（09-10 新增，正课**故意没讲**）
//   把答案直接写在下面这两行注释后面，写完再往下做 5.4。
//
//   const state = reactive({ n: ref(0) })
//   Q1: 在 script 里读这个 n，写 state.n 还是 state.n.value ？  答：
//   应写 state.n
//   const arr = reactive([ ref(0) ])
//   Q2: 在 script 里读第一个元素，写 arr[0] 还是 arr[0].value ？答：
//  应写 arr[0].value
//   Q3: 两个答案如果不一样，为什么？一句话。                    答：
//  因为 reactive 对象的属性会解包 ref，而数组元素不会解包 ref

//   出处：cn.vuejs.org「响应式基础」这一页**末尾**那段讲 ref 解包细节的小节
//        （ref 作为 reactive 对象属性时会怎样 + 数组/Map 的例外）。
//   ⚠️ 这三问在今天正课里一个字没提 —— 答不出就是没读，别猜。
// ---------------------------------------------------------------


// ---------------------------------------------------------------
// TODO【5.4】handleSubmit()
//   今天不发请求。只 console.log 出选中的文件名
//   目的：证明「点按钮 → 读到了 5.2 的状态」这条链路是通的
// ---------------------------------------------------------------
const handleSubmit = () => {
  errorMsg.value = '' // 每次点击先清掉上一次的错误，避免文案一直挂着
  if (selectedFile.value) {
    console.log(selectedFile.value.name)
  } else {
    errorMsg.value = 'No file selected'
  }
}
</script>

<template>
  <!-- TODO【5.5】三个元素，都在这里：
       ① <input type="file" accept="application/pdf">  用 @change 绑 5.3
       ② <button>上传</button>                          用 @click 绑 5.4
                                                        用 :disabled 绑「没选文件 或 正在上传」
       ③ <p> 显示 errorMsg                              用 v-if 让没错时根本不渲染
       ⚠️ 模板里写状态名不加 .value -->
       <input type="file" accept="application/pdf" @change="handleFileChange" />
       <button @click="handleSubmit" :disabled="!selectedFile || isUploading">上传</button>
       <p v-if="errorMsg">{{ errorMsg }}</p>
</template>

<style scoped>

/* TODO【5.6】能看清就行，样式不是今天的考点 */

</style>
