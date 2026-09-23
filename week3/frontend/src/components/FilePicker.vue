<script setup lang="ts">
// Day 3 · props —— 从 FileUploader.vue 切出「选文件」这一块
//
// 今天只做 props（父 → 子）。往上回传用的 onPick 是教学权宜：
// Vue 的地道做法是 emit（Day 4），今天先用函数 prop，是为了 Day 4 有个能对照的旧版本。
// 真实项目里跨组件通信一律用 emit，函数 prop 是 React 习惯，写进 Vue 会被 review 打回。

// ---------------------------------------------------------------
// TODO【3.1】defineProps —— 今天的核心
//   defineProps 不用 import。两种写法，用泛型那种：
//     const props = defineProps<{ ... }>()
//   三个 prop：
//     accept     string                        传给 <input> 的 accept
//     disabled   boolean                       loading 时禁掉
//     onPick     (file: File | null) => void   选完文件往上回传
//   ⚠️ onPick 的类型要写完整函数签名，不是 Function —— 写 Function 等于 any，
//      Day 4 你自己写的那份 types/api.ts 就白写了
// ---------------------------------------------------------------


// ---------------------------------------------------------------
// TODO【3.2】handleChange —— 把 FileUploader.vue:58-61 那三行搬过来，改最后一行
//   原来是：
//     function handleFileChange(e: Event) {
//       const input = e.target as HTMLInputElement
//       selectedFile.value = input.files?.[0] ?? null
//     }
//   ⚠️ 这里没有 selectedFile —— 它留在父组件（因为 handleSubmit 要读它）。
//      所以最后一行不是赋值给谁，是把挖出来的 File 交给 props.onPick
//   ⚠️ `input.files?.[0]` 的类型是 File | undefined，而 onPick 要 File | null。
//      `?? null` 那半句为什么不能省？想清楚再写，我会问
// ---------------------------------------------------------------


// ---------------------------------------------------------------
// TODO【3.3】读了学源才答得出的三问（正课**故意没讲**，答不出就是没读）
//   答案写在每问后面，写完再动模板。
//
//   Q1: defineProps 在 <script setup> 里不需要 import 就能用。
//       官方管这种东西叫什么？一个词。
//       答：
//
//   Q2: 文档明说「所有 props 都遵循单向绑定原则」，
//       并给了两个「你确实想改 prop」的常见场景 + 各自的正确做法。
//       写出其中一个场景和它的做法。
//       答：
//
//   Q3: 文档里 props 用 camelCase 声明，模板里却可以用 kebab-case 传。
//       为什么两边可以不一样？
//       答：
//
//   出处：cn.vuejs.org「组件基础 → Props」整节（跳过 props 校验、透传 attributes）
// ---------------------------------------------------------------
</script>

<template>
  <!-- ---------------------------------------------------------------
       TODO【3.4】一个 <input type="file">，三处绑定
         accept    绑 props 的 accept    —— 要不要冒号？想清楚再写
         disabled  绑 props 的 disabled  —— 要不要冒号？和上面一样吗？
         @change   绑 3.2 的函数
       ⚠️ 模板里读 props 不写 props. 前缀，直接写名字
       ⚠️ 冒号写错不会报错，界面会静默坏掉 —— 这就是瓶颈 2 的样子
       --------------------------------------------------------------- -->
</template>

<!--
  ===============================================================
  父组件 FileUploader.vue 那边你要动三处，我没替你改：

    ① <script> 顶部 import FilePicker
    ② 模板第 181 行那个 <input type="file" ...> 整行换成 <FilePicker ... />
       三个 props 怎么传，看 3.1
    ③ handleFileChange 的签名要改 —— 它现在收的是 Event，
       但 FilePicker 往上给的已经是 File | null 了。函数体会短很多

  ⚠️ 改完 ③ 之前先想：这个函数还需要 `as HTMLInputElement` 那行吗？
  ===============================================================
-->
