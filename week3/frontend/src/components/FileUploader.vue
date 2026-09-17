<script setup lang="ts">
// Day 5 · 第一个组件：选文件 + 上传按钮          ← 已完成
// Day 6 · 接通真接口：Axios + UI 三态机          ← 今天
//
// 今天不搬家：文件仍留在 components/，Day 7 目录重构时再一起挪。
// 现在搬会把 Day 5 复盘里的所有文件引用打断，换来的只是"位置好看"。

// ---------------------------------------------------------------
// TODO【6.1】import（外围，直接给，不是考点）
//   axios 已装好（1.20.0，教练装的）。你要引三样：
//     ① ref、computed        ← 从 'vue'
//     ② axios                ← 默认导出
//     ③ SummarizeResponse    ← 从 '@/types/api'（Day 4 你自己写的那份，今天开始用它）
//   ⚠️ 类型只在编译期存在，引它用 `import type { ... }`
// ---------------------------------------------------------------
import { ref, computed } from 'vue'
import axios from 'axios'
import type { SummarizeResponse } from '@/types/api'

// ---------------------------------------------------------------
// Day 5 的三个状态（保留）
// ---------------------------------------------------------------
const selectedFile = ref<File | null>(null) // ts 泛型 只准装 File 或 null，别装别的 默认值（null）
const errorMsg = ref('')
// ---------------------------------------------------------------
// TODO【6.2】把 isUploading 升级成三态（Day 5 的 isUploading 已删，这里重建）
//   原生版 index.html 用的是 setState('idle'|'loading'|'done'|'error')
//   Vue 版不需要那个函数，只需要一个 ref 装住当前状态。
//   ⚠️ 类型写成字面量联合类型（Day 4 学的联合类型，这次是字符串字面量）：
//      ref<'idle' | 'loading' | 'done' | 'error'>('idle')
//   这样拼错 'lodaing' 时 TS 当场报错，而不是运行时界面卡住
// ---------------------------------------------------------------
const status = ref<'idle' | 'loading' | 'done' | 'error'>('idle')


// ---------------------------------------------------------------
// TODO【6.3】结果状态
//   成功时后端返回 6 个字段 —— 你 Day 4 已经给它写过 interface 了。
//   没结果时是 null，所以类型是 `SummarizeResponse | null`
//   ⚠️ 这里不许写 any。写了 any，Day 4 那个文件整天白写
// ---------------------------------------------------------------
const result = ref<SummarizeResponse | null>(null)

// ---------------------------------------------------------------
// TODO【6.4】canSubmit —— 今天 computed 的落点
//   Day 5 你把判断写在模板里：:disabled="!selectedFile || isUploading"
//   今天状态变多了，模板里那行会长到读不懂。抽出来：
//     const canSubmit = computed(() => ???)
//   条件：选了文件 且 不在 loading
//   ⚠️ computed 返回的是 ref，script 里读它要 .value；模板里不要
// ---------------------------------------------------------------
// 拍板 B（09-17）：不再因「没选文件」禁用按钮，改由 handleSubmit 校验并显示原因
const canSubmit = computed(() => status.value !== 'loading')

// ---------------------------------------------------------------
// Day 5 的 handleFileChange（保留，但有一处要补 —— 见 6.5 的 ⚠️）
// ---------------------------------------------------------------
function handleFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  selectedFile.value = input.files?.[0] ?? null
}

// ---------------------------------------------------------------
// TODO【6.5】handleSubmit —— 今天的主干
//   顺序（原生版 index.html【C】区是同一套，可以对着看）：
//     ① 进 loading，清掉上一次的 errorMsg 和 result
//     ② 造 FormData，append 的字段名必须是 "file"
//        （出处：后端 main.py `async def summarize(file: UploadFile...)` 的参数名）
//     ③ await axios.post(接口地址, fd)
//     ④ 成功 → 结果写进 6.3，状态进 'done'
//     ⑤ 失败 → 交给 6.6，状态进 'error'
//
//   接口地址不要写死 'http://127.0.0.1:8000/summarize'：
//     Day 3 你配了代理、Day 3 你写了 .env.development 的 VITE_API_BASE=/api
//     读法 → import.meta.env.VITE_API_BASE
//   ⚠️ 不要自己设 Content-Type。浏览器会带 boundary 自动填，手写就 422
//      （Week 2 Day 4 速查表里的原话，这次同样成立）
//   ⚠️ 上一次的结果必须在 ① 就清掉 —— 不清的话，用户会对着上一个 PDF 的
//      总结以为是这一个的。原生版【A】区那 4 行"先清"就是干这个的
// ---------------------------------------------------------------
const handleSubmit = () => {
  errorMsg.value = '' // 每次点击先清掉上一次的错误，避免文案一直挂着
  if (selectedFile.value) {
    console.log(selectedFile.value.name)
  } else {
    // 拍板 B（09-17）：按钮不再因「没选文件」而禁用，校验挪进这里。
    // 所以这个分支不再是死代码，也必须要 return —— 否则会带着 null 继续往下发请求。
    errorMsg.value = 'No file selected'
    status.value = 'error' // 状态得进 error，模板的错误块才显示得出来
    return
  }
  status.value = 'loading' // ① 进 loading
  result.value = null // ① 清掉上一次的结果
  const formData = new FormData() // ② 造 FormData
  formData.append('file', selectedFile.value as File) // ② append 的字段
  axios.post(`${import.meta.env.VITE_API_BASE}/summarize`, formData) // ③  axios.post
    .then((response) => {
      result.value = response.data // 成功 写进result 
      status.value = 'done' // 状态进 'done'
    })
    .catch((err) => {
      errorMsg.value = toUserMessage(err) // 失败 交给6.6
      status.value = 'error' // 状态进 'error'
    })
}

// ---------------------------------------------------------------
// TODO【6.6】toUserMessage(err) —— 错误分类，今天的第二个核心
//   axios 和 fetch 在这里行为相反（正课讲过）：4xx/5xx 也会进 catch。
//   所以 catch 里第一件事不是看 status，是先问：
//
//       err.response 在不在？
//         在   → 服务器回话了，按 err.response.status 分类（Day 4 那 7 个码）
//         不在 → 网络层：后端没起 / 隧道断了 / 超时
//
//   每一类给用户看什么，判据是一句话（原生版【D】区的原话）：
//       「用户看完这句，知道下一步该干什么吗？」
//       "Error 413" ❌   "文件 14.2 MB，超过 10 MB 上限，请换一个" ✅
//   ⚠️ 500 是特例：后端的 detail 是给你看的，不该原样丢给用户（想想为什么）
//   ⚠️ 422 的 detail 是**数组**不是字符串。真实形状（09-10 实跑，不是 /docs 的示例值）：
//       {"detail":[{"type":"missing","loc":["body","file"],"msg":"Field required","input":null}]}
//      取文案要从数组里挑，直接 textContent 会显示 [object Object]
// ---------------------------------------------------------------
function toUserMessage(err: any): string {
  if (err.response) {
    switch (err.response.status) {
      case 400:
        return `文件 ${selectedFile.value?.name} 不是 PDF，请换一个`
      case 413:
        return `文件 ${((selectedFile.value?.size || 0) / (1024 * 1024)).toFixed(1)} MB，超过 10 MB 上限，请换一个`
      case 422:
        return `文件 ${err.response.data.detail[0].msg}，请换一个`
      case 500:
        return ` 服务器内部错误，请截图发给教练 `
      case 502:
        return `后端服务未启动，请先运行后端（Week 2 Day 3）`
      default:
        return `未知错误，请稍后重试`
    }
  } else {
    return `网络异常，请检查后重试`
  }
}
const buttonText = computed(() => {
  switch (status.value) {
    case 'idle':
      return '上传'
    case 'loading':
      return '生成中…'
    case 'error':
      return '重试'
    case 'done':
      return '上传'
  }
})
// ---------------------------------------------------------------
// TODO【6.8】读了学源才答得出的一题（正课**故意没讲**，答不出就是没读）
//   把答案写在每问后面，写完再往下做 6.7。
//
//   Q1: computed 和 methods（普通函数）都能算出同一个值。
//       官方文档明说了 computed 有一个 methods 没有的特性，是什么？一个词。
//       答：缓存
//
//   Q2: 下面这个 computed 有什么问题？一句话。
//         const list = computed(() => { fetchData(); return items.value })
//       答：不应该吧fetchData放在computed里，因为computed是用来计算值的，而fetchData是一个副作用操作，可能会导致不必要的重复请求。
//
//   Q3: 「能用 computed 就别用 watch」—— 那什么时候**必须**用 watch？
//       用你自己的话说一句，不要抄标题。
//       答：当需要做一整个操作，而不是只获取一个值时，比如监听某个数据变化后执行一系列逻辑操作，这时候就需要使用watch。
//
//   出处：cn.vuejs.org「计算属性」整节 + 「侦听器」开头两节
// ---------------------------------------------------------------

</script>

<template>
  <!-- Day 5 的三个元素（保留） -->
  <input type="file" accept="application/pdf" @change="handleFileChange" />
  <button @click="handleSubmit"  :disabled="!canSubmit">{{ buttonText }}</button>
  <!-- ---------------------------------------------------------------
       TODO【6.7】模板三态 + 结果
       原生版是 6 个 DOM 属性手动开关（setState 那 20 行）；
       这里只写"什么状态显示什么"，剩下的 Vue 自己做。

       要有四处：
         ① 按钮：disabled 绑 6.4 的 canSubmit（取反）；文字随状态变
            （idle「上传」／ loading「生成中…」／ error「重试」）
         ② loading 提示：v-if 绑 status === 'loading'
         ③ 错误块：v-if 绑 status === 'error'，显示 6.6 算出来的文案
         ④ 结果块：v-if 绑 status === 'done'，里面：
              - summary（注意换行要保住：white-space: pre-wrap）
              - input_tokens / output_tokens / cost / model 四个数
              - truncated 为 true 时**多一块警告**，false 时那块根本不存在
                ⚠️ 这不是"显示一个值"，是"条件显示"——Week 2 你在这栽过
         ⚠️ v-if 和 v-show 今天选 v-if。理由自己想，Day 7 我会问
       --------------------------------------------------------------- -->
  <p v-if="status === 'loading'">生成中…</p>
  <p v-else-if="status === 'error'">{{ errorMsg }}</p>
  <section v-else-if="status === 'done'">
    <h2>结果</h2>
    <p class="summary">{{ result?.summary }}</p>
    <p>input_tokens: {{ result?.input_tokens }}</p>
    <p>output_tokens: {{ result?.output_tokens }}</p>
    <p>cost: {{ result?.cost }}</p>
    <p>model: {{ result?.model }}</p>
    <p v-if="result?.truncated">⚠️ 警告：内容被截断，请换一个 PDF</p>
  </section>
</template>

<style scoped>
/* 唯一的功能性样式：不写这行，后端 summary 里的换行会被全压成一行 */
.summary {
  white-space: pre-wrap;
}
</style>
