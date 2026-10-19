# Week 4 学习日志 · 组件拆分与 Prompt 工程

> 目标：**把 `FileUploader.vue` 拆成多组件**（引出 props/emit + Pinia），AI 线开 Prompt 工程阶段 2 正题。
> 教学合约：`../week1/CLAUDE.md` ｜ 上一周：`../week3/README.md` ｜ 总路线：`../LEARNING-PLAN.md`
>
> 建立于 2026-09-21（Week 4 Day 1 开课时）。

---

## Week 4 是什么

| 轨道 | Week 4 的位置 | 本周只做到哪 |
|---|---|---|
| **主线**（总纲 9 个月） | **阶段一 · 第 1 个月第 2 周** → 触第 2 个月 | 组件拆分（props/emit）→ 状态提升 → Pinia 入门 |
| **AI 线**（可并行） | **阶段 2 · 第 2 周**（指南第 3-6 周） | Prompt 黄金 5 段结构 + 8 大技法挑 3 个真用上 |

**主轨比例 5 : 2**（沿用 Week 3）—— Day 1-2 给 AI 线，Day 3-7 给主线。

---

## 排期约束

| 约束 | 出处 | 对本周的后果 |
|---|---|---|
| AI 线阶段 2 给 **4 周** | `[AI §三]` 红线 | 本周只做 5 段结构 + 3 个技法，**测试集/LangSmith 不排** |
| 主线阶段一给 **3 个月** | `[总纲 §二]` | 本周到 Pinia 入门为止，**Tailwind 不排**（第 3 个月） |
| 每周至少一个能发出去的产出 | `[总纲 §九]` | 周末必须有：**拆完的多组件版能跑 + prompt 前后对照** |
| **卡 2 小时必停** | `[FS §八]`，压过合约规则 2 | 卡住直接找教练要方向，不硬扛 |
| 每天 **2-3 小时** | ly 08-09 自报 | 按 `[总纲 §九]` 节奏模板排 |
| `/summarize` **不许公开到公网** | `[总纲 §三]` 红线 | 零鉴权，JWT 属阶段二。本周起 ly 在**本机**跑前后端 |

---

## 7 天进度表

| Day | 轨道 | 主题 | 文件 | 状态 | 复盘得分 |
|---|---|---|---|---|---|
| 1 | 清账 + AI 线 | **ly 本人跑满四条路径**（清 Week 3 自检⑤）+ **Prompt 黄金 5 段结构** | `week2/api/prompts.py`（新建） | ☑ | 1.5 / 3 |
| 2 | AI 线 | **8 大技法挑 3 个**（Role / Few-shot / Negative）真改进 `/summarize` 的 prompt，前后对照 | `week2/api/prompts.py` | ☑ | 1 / 3（09-23 补答） |
| 3 | 主线 | **组件拆分（一）**：从 `FileUploader.vue` 切出「选文件」子组件，**props 往下传** | `components/FilePicker.vue` | ☑ 正课、动手与测试通过；与 Day 4 合并复盘 | 合并 2 / 3 |
| 4 | 主线 | **组件拆分（二）**：切出「结果展示」子组件，**emit 往上抛** | `components/ResultPanel.vue` | ☑ 动手与验证通过；非空检查误解已讲解，后续回顾 | 同上，不另计 |
| 5 | 主线 | **状态提升**：三个组件都要读的状态放哪？先用「提到父组件」做一版，**亲眼看见 props 钻透** | 同上 | ☑ 动手、学源及 props/inject 两版验证已有通过记录；10-19 正式复盘完成 | 2.5 / 3 |
| 6 | 主线 | **Pinia 入门**：把提升上去的状态搬进 store，对照 Day 5 那版看省掉了什么 | `stores/summarize.ts` | ◐ 回顾已答并订正；进入 Setup Store 讲解，待阅读学源和填写首个 store | — |
| 7 | — | 巩固：三版对照（单组件 / props 提升 / Pinia）+ Week 4 总复盘 + **目录重构**（Week 3 欠的） | — | ☐ | — |

> **为什么 Day 5 要先做「明知会难受」的 props 提升版**：Pinia 的价值只有在**先痛过一次**之后才看得见。
> 直接上 Pinia 会变成「照着文档敲三件套」，说不出它解决了什么。
> 这一条是刻意安排的教学顺序，**不是绕远路**（合约规则 10：教学权宜必须当场标注）。

### 📚 本周学源挂载（合约规则 12）

| Day | 学源 | **只看这一节**（别扩散） | 预算 | 出处 | 落地？ |
|---|---|---|---|---|---|
| 1 | `LEARNING-PLAN.md` §5 阶段 2 那节 | 「Prompt 黄金 5 段结构」5 行 + 「8 大技法」标题行。**不看防幻觉/测试集** | 15 min | `§5:383` | ☐ |
| 2 | Anthropic Prompt Engineering 文档 | Role prompting + Few-shot 两节。**跳过 CoT / 长上下文技巧** | 30 min | `§5:386` | ☐ 待 ly 自报 |
| 3 | cn.vuejs.org | 「组件基础 → Props」一节。**跳过 props 校验、透传 attributes** | 30 min | `§2:148` | ☐ |
| 4 | cn.vuejs.org | 「组件事件 emit」一节 + `defineEmits`。**跳过 v-model 自定义** | 30 min | `§2:148` | ☐ |
| 5 | cn.vuejs.org | 「provide/inject」一节 —— 原定只阅读；10-16 按 ly 提问追加对照实验 | 20 min | `§2:148` | ☑ ly 确认已读，已落地 App provide / CostPanel inject；实际阅读时长未自报 |
| 6 | pinia.vuejs.org | 「Defining a Store」+「State」两节。**跳过 getters 高级用法、插件** | 40 min | `§2:151` | ☐ |

> 落地判据（规则 12）：**当天代码里有没有一处，是因为读了它才那样写的？** 复盘时写出来。答不出 = 等于没看。

---

## 从 Week 3 结转的债

- [-] **Week 3 自检⑤** —— **09-21 ly 决定跳过，不再排期**。当天实跑到一半的结果如实留档：
      **路径 2 ☑** 400 /「上传的文件不是 PDF」，与期望逐字一致；
      **路径 4 ☑** 502，且 `console.error` 打出 `HTTP 502: ` **冒号后为空** ——
      实证了 Vite 代理自造 502 是空响应体（Week 3 那条独立发现），同时证明 09-18 把
      `console.error` 挪到 `switch` 之前生效了（留在 `default` 里这行永不打印）；
      **路径 1 ✗ 未对上** 期望 200 实得 400「PDF 提取出来是空的」，未做 `attention.pdf` 控制变量实验，真因未定；
      **路径 3 ☐ 未跑**。
      ⚠️ 因此「ly 本人跑满四条」这条针对瓶颈 4 的硬要求**Week 3、Week 4 连续两周未兑现**，记在案
- [ ] **目录重构** —— `week1/week2/week3` 混着 AI 线和前端线，候选 `stage1-frontend/` + `stage3-ai/{week1,week2}`。
      改路径要连带改 `week1/CLAUDE.md` / 各 README / `LEARNING-PLAN.md` / memory 全部引用（推到 Day 7）
- [ ] `week3/day7_review.md` Part 2 的 Day 6·Day 7 两行、Part 3/4/5 若干栏
- [ ] **Learn Git Branching**（1 小时，`§2:129`）—— 主线第 1 个月的 Git 那条一直没动
- [ ] `deepseek-chat` 硬编码 8 处（week1 各脚本），该模型 2026-07-24 已弃用
- [ ] PDF 解析换 PyMuPDF / pdfplumber（`pypdf` 已暴露页码污染）

---

## 当前瓶颈（教练盯的四条，Week 3 结转）

1. **知道了没调用**（第 8 次）—— 答案就在自己写过的文件里，不翻。判据：做决定时那个文件有没有被打开过
2. **静默 bug 意识** —— 「没有 A ≠ 有 B」四张脸：没报错≠有结果 / 判据没变红≠功能对 / 函数写了≠被调用 / 参数传了≠生效
3. **变量作用域·生命周期**（第 5 次）—— 问「谁在维护它」不够，必须再问「**它活多久**」：函数返回就没了？进程退出就没了？
4. **能写 ≠ 能自查** —— Week 3 已开张 2 条独立发现的 bug（均早于教练指出）。**本周要求不降回 0**

---

## Week 4 结束自检（Day 7 填）

> 记号（`LEARNING-PLAN.md §0`）：`[x]` = 过，**后面必须跟证据**；`[ ]` = 未过；
> `[x]*` = 教练代填，答案不是 ly 产出的。**全部 ☑ 才解锁 Week 5。**

- [ ] 能用 5 段结构写出一个 200+ 字的 system prompt，并说清每段在管什么
- [ ] 至少 3 种 prompt 技法真用在 `/summarize` 上，**有前后对照的实测输出**（不是「感觉变好了」）
- [ ] 能说清 props 和 emit 各自的方向，并答出「**子组件不许直接改 props**」及其原因
- [ ] 拆出的子组件能独立跑通，父组件只负责协调
- [ ] 能说出「状态提升」难受在哪，以及 Pinia 具体省掉了哪一步（**要能举出自己代码里的行**）
- [ ] 「我自己独立发现的 bug」≥ 1 条，且在教练指出之前

---

## Day 1 复盘题（2026-09-21，原文留档）

> 出题前按规则 6 自查：三个标准答案均可逐字写出；Q3 的前提已核
> （`week2/api/main.py:264` 有 `detail="上游返回了空内容"`）。

**Q1（易）** 5 段结构里 **Constraint 和 Format 的区别**是什么？
从你自己的 `SYSTEM_PROMPT` 里各举一个例子。三句话之内。

**Q2（中）** 今天说「**示例胜过描述**」。这句话背后的机制是什么？
另外：为什么「**首行缩进**」这个要求**特别**需要示例，而不是靠文字描述？

**Q3（难）** 今天路径 4 你看到 `console.error` 打出 `HTTP 502: `，冒号后面是空的。
现在换一个场景：**后端活着**，但 DeepSeek 返回了空内容，后端按 `main.py:264` 的护栏返 502。
① 这时那行 `console.error` 会打出什么？
② 和今天看到的有什么不同？
③ 这个不同能用来做什么？

### 得分：**1.5 / 3**

| 题 | 判 | 理由 |
|---|---|---|
| Q1 | ☑ | Constraint/Format 区别与两个例子都对 |
| Q2 | ◑ | ① 答成现象（「更明确/更模糊」）未答到机制；② 答到，且角度教练没给过 |
| Q3 | ☐ | 不会；且把题面的「后端活着」读成了「后端中断」 |

**教练自己的一处错，已当场纠正**：正课里说「Constraint 是**负向**的」说窄了 ——
「用中文回复」是正向限定但同样是 Constraint。准确表述 = **把某个维度的可选范围收窄**，
与用不用否定句无关。ly 的 Q1 答案「让模型不要干什么」就是照这句错表述来的。

**ly 独立贡献 1 条（记入瓶颈 4 的正面栏）**：Q2② 指出「首行缩进」的**「首行」二字本身有歧义**
（整篇第一行 vs 每段第一行）—— 教练正课给的理由是另一个（纯文本空白字符易被丢弃），
ly 这条更基础，排在前面。

**今天最值得记的一条**：ly 在 Q2② 已经摸到了 Q2① 的答案（那个歧义正是「理解环节」出的错），
但没把它从具体例子抽象成一般机制。**「具体例子 → 一般机制」这一步 = 瓶颈 4 在概念层面的样子。**

### Day 1 状态

- 正课 ☑ Prompt 黄金 5 段结构（五段讲法 + 4 个递进例子 + 连回 `SYSTEM_PROMPT`）
- 额外教了 **抽取式 vs 生成式摘要**（起因：ly 认为「总结」与「提炼核心思想」同义）
- 结论：ly 的 `SYSTEM_PROMPT` **缺 Role 和 Example 两段**，第 1 条是 Task/Constraint 混写 → Day 2 的活
- 学源 `§5:383` 已报（15 min），落地判据留到 Day 2 复盘验
- ⑤ 四条路径 ly 决定跳过，见上方结转债那条

---

## Day 2（2026-09-22）· 三个技法 + 三轮控制变量实验

### 做了什么

- 正课：**Role Prompting / Few-shot / Negative Prompt** 三个技法，各按规则 11 五段讲完
- 额外讲 **Format 与 Example 的区别**（ly 提问触发）：Format 是规格（about 输出），
  Example 是样品（is 输出）；**Format 覆盖所有情况，示例只覆盖它演到的那一种**，
  所以 Format 的职责之一是**给示例解绑**——指认示例里哪些特征是规则、哪些只是这一例碰巧如此
- ly 写完 V2 五段，跑通首轮；教练接手做了两轮控制变量

### 三轮改了什么

| 轮 | 改动（每轮只改一处） | 判据 | 结果 |
|---|---|---|---|
| r1 | ly 的 V2 首版：补 Role / 拆 Task / 抄 V1 的 format / 一段示例（半角缩进、无闭标签） | 首段是否缩进 | ✗ |
| r2 | **只改示例**：两段、全角空格、补 `</example>`、去掉「输出：」后的尾随空格 | 同上 | ✗ |
| r3 | **只改 format**：「首行缩进」→「每一个段落（包括第一段）都以两个全角空格开始」＋篇幅解绑 | 同上 | ✗ |

### 六次调用横排（原件在 `week4/day2_v{1,2}_r{1,2,3}.txt`）

| | 字数 | 段数 | 各段开头 |
|---|---|---|---|
| V1 r1 / r2 / r3 | 292 / 285 / 373 | 2 / 2 / 3 | 首段均无缩进，后续段均 `　　` |
| V2 r1 / r2 / r3 | 341 / 453 / 259 | 2 / 3 / 2 | 同上 |

### 结论一：首段缩进 **prompt 层改不动**，改走路 B

六次调用**第一段全部未缩进，零例外**；r3 已在 format 里写死「包括第一段」「两个全角空格」，照样无效。
推断：模型用的是**西文排版惯例**（首段不缩进、后续段才缩进），而中文惯例是每段都缩。

→ **Day 4 拆 `ResultPanel.vue` 时**：summary 按 `\n\n` 切数组 `v-for` 渲染，每个 `<p>` 给 `text-indent: 2em`，
同时删掉 V2 format 里缩进那半句。**这不是退而求其次，是三轮实验排除了路 A。**

### 结论二：其余四个量全在漂，n=1 的对照判不出效应

字数 259–453、段数 2–3、书名号有无——**全在漂**。
唯独「首段不缩进」六次零例外。**「不漂」比「漂」更有信息量**：漂的量分不清是改动的功劳还是运气。

### ⚠️ 教练两个结论当天作废（都是 n=2 就下判断）

1. ~~「V2 点明论文标题 = Role 起作用」~~ —— r3 的 V1（无 Role）点了标题，V2 反而没点
2. ~~「V1 噪声底线 7 字」~~ —— r3 的 V1 跳到 373，噪声本身就有 88 字；
   由此~~「V2 的 112 字变化远超噪声」~~一并作废

### ly 的判据表问题（瓶颈 2 的新一张脸）

填的四行里只有「字数」合格。「段数」填「分段」、「首段开头」填「缩进」——
**用『缩进』判『缩进』，判据与被判对象是同一个模糊词，这个判据永远判不出问题**。
实证：r1 的实得是「第 1 段没缩、第 2 段缩了」，而「缩进」这两个字**判不出这算不算兑现**。

由此登记 **瓶颈 2 的第五张脸**：

```
没报错 ≠ 有结果 ／ 判据没变红 ≠ 功能对 ／ 函数写了 ≠ 被调用 ／ 参数传了 ≠ 生效
判据没抓到 ≠ 没发生          ← 09-22 新增
```

根因同 Day 1：**改的地方没测，测的地方没改**——改的是 Role 与 Example，测的四个量全在 Format 层。

### 遗留（未修，等 ly 决定）

- `summarize()` 的 `.strip()` 挡不住 `content=None`（Day 5 修过它的镜像：「`or ""` 防不住 `''`」）
- `MAX_OUTPUT_TOKENS = 1500` 定义了但没传进 `create()` —— 死变量，「定义了 ≠ 生效」
- V2 的 Role 是「语言模型训练师」，属**训练做这件事的人**而非**做这件事的人**，差一层
- 判据表期望值仍是「小于四百」这类口语，未改成可机械判定的写法

### 文件清单

`week2/api/prompts.py`（V2 五段 + 示例 + format 三轮改动、`measure()`、落盘）
`week4/day2_v1_r{1,2,3}.txt`、`week4/day2_v2_r{1,2,3}.txt`（六次原件）
`week4/README.md`（本节）

### Day 2 复盘题（原文留档，**ly 拍板推到 Day 3 一起答**）

> 出题前按规则 6 自查：三个标准答案均可逐字写出；Q2/Q3 的前提为本日六次实测数据。

**Q1（易）** Format 和 Example 的区别，两句话说清。
然后举一个例子说明 **Format 的职责之一是「给示例解绑」**——解绑什么？

**Q2（中）** 今天六次调用里，只有一个量完全没漂。是哪个？
**为什么「它不漂」这件事，比其它量怎么漂更有信息量？**

**Q3（难）** 今天定了缩进走路 B。
① 这个决定的依据是什么？
② 如果只跑了**第一轮**就决定走路 B，这个依据成不成立？为什么？

---

## Day 3（2026-09-23）· props + Day 2 复盘补答

### 间隔回顾（规则 9，不计分）

| 条 | 题 | 判 |
|---|---|---|
| ① 昨天 | 瓶颈 2 新增的第五张脸原话 | ☐ 答案：**判据没抓到 ≠ 没发生** |
| ② 前天 | 后端自己返 502 时 `console.error` 打什么 | ☑ `HTTP 502: 上游返回了空内容` |
| ③ 上周 | `computed` 比普通函数多了什么 | ☑ 缓存（依赖没变不重算） |

### Day 2 复盘题批改：**1 / 3**

**Q1 ◑** —— 「Format 负责排版形状」对；但把区别定在「有没有解释」上不准。
准确分界：**Format 是规格（about 输出），Example 是样品（is 输出）**。
后半「解绑」不会 → 解绑的是**示例里那些只是碰巧如此的特征**（长度、段数会被一起学走）。
这句逐字写在 `prompts.py` format 段末尾「篇幅与段数以上方 constraint 为准，不参照示例的长度」——
但那半句是教练 r3（`79fd48e`）改的，不是 ly 写的，**不记瓶颈 1**。

**Q2 ☐** —— 答「小于 400 字」。错两层：
① 题问**六次输出里观察到的量**，答成了 **prompt 里写的话** → 瓶颈 2 第四张脸「参数传了 ≠ 生效」；
② 即便按输出看，字数是漂得第二狠的（极差 203），不是没漂的那个。正确答案 = **首段不缩进**（六次零例外）。

**Q3 ☐** —— 依据不是「六次都失败」，是 **r2/r3 的两次排除法**：
r2 只改示例 → 排除「示例写得不好」；r3 只改 format → 排除「话说得不够死」。
只跑第一轮：**依据不成立** —— n=1 的失败同时兼容三种解释，分不清就没有依据，只有猜测。

### ⚠️ 新发现：「400 字」这条约束**从来没有口径**（今天最值钱的一条）

批 Q2 时重数了六个文件，三种口径：

```
                len(s)   非空白   纯汉字
V1 r1            292      285      229
V1 r2            285      281      237
V1 r3            373      353      262
V2 r1            341      324      234
V2 r2            453      432      340    ← len 口径破 400，纯汉字口径没破
V2 r3            259      250      209
```

`measure()` 数的是 `len(s)`（含换行、含全角空格），**同一份输出换个数法结论相反**。
判据表那格填的是「小于四百」，没说数什么 → **这格判不出对错**。

**这是 09-22「用『缩进』判『缩进』」的第二个实例，同一个病**：
判据和被判对象共用一个没定义口径的词，判据恒绿。
→ 瓶颈 2 第五张脸「判据没抓到 ≠ 没发生」再添一条注脚：**口径没定义 = 判据没抓到**。

### 正课：props（规则 11 五段）

- ① 大白话：父给子的**出厂配置**，子只能读不能改
- ② 官方：注册在组件上的自定义 attribute，**单向下行绑定（one-way down binding）**
- ③ 拆词：单向的意义 = **把状态的修改入口收窄到一处**，排查时只看那一处
- ④ 四个递进例子：静态值 / `:` 动态求值（`disabled="false"` 是真值这个坑）/ 传引用类型（`props.obj.x = 1` **Vue 拦不住**，单向是君子协定不是墙）/ 函数也能当 prop
- ⑤ 连回代码：`<FilePicker accept="..." :disabled="!canSubmit" :onPick="handleFileChange" />`

**拆组件的判据**（不是「文件太长」）：有自己的内部逻辑 / 要在多处复用 / 改 A 区时怕碰坏 B 区。
「选文件」中第一和第三条。

**状态放哪**：`selectedFile` **留在父组件**，因为 `handleSubmit` 要读它 ——
**取决于「谁要用它」，不取决于「谁产生它」**。

### ⚠️ 教学权宜，已当场标注（规则 10）

Vue 支持函数 prop；通知父组件通常使用组件事件 emit（Day 4）。
今天保留 `:onPick`，是为了 Day 4 对照 `props.onPick(file)` 与 `emit('pick', file)`。
迁移时还要调整声明和父组件绑定，不能只替换调用语句。
2026-10-13 更正旧记录：「函数 prop 在 Vue 中不合法」和「跨组件通信一律 emit」均不准确。

### 📚 学源已报（规则 12）

cn.vuejs.org「组件基础 → **Props**」整节 ／ **30 min** ／
跳过 props 校验（type/required/default）、透传 attributes（`$attrs`）、Boolean 强制转换 ／ 出处 `§2:148`。
落地判据留到复盘验：**今天代码里哪一行是因为读了它才那样写的？**

### ⚠️ 教练翻车一次

上一轮回复里口头写了「骨架已建」，**实际一个工具调用都没有**，文件不存在。
ly 说「推送 git」时才暴露。违反全局铁律 9（用真工具调用）。已补建，并在此留档。

### 文件清单

- `week3/frontend/src/components/FilePicker.vue`（**新建**，79 行，全是 TODO，实现未填）
- `week4/README.md`（本节 + 进度表 Day 2/Day 3 两行）

### Day 3 动手验收（2026-10-13 更新）

- [x] 【3.1】声明 `accept`、`disabled` 和完整函数签名的 `onPick`；`defineProps<...>()` 已调用。
- [x] 【3.2】子组件读取文件并调用 `props.onPick(input.files?.[0] ?? null)`。
- [x]* 【3.3】Q1 由 ly 回答；Q2/Q3 经教练讲解后填入参考答案，不计为独立答题通过。
- [x] 【3.4】绑定 `props.accept`、`props.disabled` 和 `@change`；模板可使用 `props.` 前缀。
- [x] 父组件引入并使用 FilePicker，通过函数 prop 更新自己的 selectedFile；旧处理函数已注释保留。
- [x] `pnpm build` 通过，含 TypeScript 检查和 Vite 构建。
- [x] 后端依赖检查通过，直连 `/health` 与代理 `/api/health` 均返回 HTTP 200。
- [x] 项目自带 `attention.pdf` 经 `/api/summarize` 返回 HTTP 200、有效摘要、`truncated: false`；ly 随后确认浏览器测试通过。
- [ ] 正式 Day 3 复盘未出题、未评分；文档阅读时长未自报。

### 本次环境恢复与验证边界

- Windows 本地使用 pnpm 11.20.0 与项目 Node 24.19.0；Axios、Router、Pinia 的现有配置已核对，未重复创建。
- 后端使用根目录 `.venv`，前端监听 127.0.0.1:5174，后端监听 127.0.0.1:8000。
- 本次 502 由后端未启动引起；已补齐依赖和本机配置，恢复前后端链路。
- 根目录 `.env` 和 `.venv/` 被 Git 忽略，不进入提交。新机器须自行安装依赖并配置密钥。
- 推送前复查：前端已重新启动，但当前本机密钥配置为空，后端启动被 SDK 拒绝；此前真实上传成功的记录仍有效，后端再次启动前须补回本机配置。
- 后续更新（2026-10-13）：本机密钥已重新配置，ly 明确授权提交并推送根目录 `.env`（含密钥）；本次将其强制加入 Git 跟踪，`.venv/` 仍忽略。此前「.env 不进入提交」描述的是上一次推送，本次决定已改变；未重新验证后端启动。
- 上传成功路径已验；未重新验证全部错误码、截断场景和 loading 时的禁用交互。

### Day 4 计划（2026-10-13 留档）

1. 学习组件事件和 defineEmits，将 FilePicker 的 onPick 函数 prop 改成 pick 事件，父组件用 @pick 接收。
2. 拆出 ResultPanel.vue，以 props 接收结果，保留摘要换行、token、成本、模型名和截断提示。
3. 构建并验证上传后的结果展示。学源：Vue「组件事件」与 defineEmits，预算 30 分钟。

### Day 4 开课与 emit 验收（2026-10-14）

- Day 3 不计分回顾：状态归属回答正确；未取到文件时的 undefined 与 null 混淆；父组件函数 prop 的绑定与接收函数经讲解订正。正式 Day 3 复盘仍未做。
- 已讲解组件事件、defineEmits、事件参数及类型声明；学源已报，预算 30 分钟，阅读完成情况未自报。
- ly 完成 FilePicker 的 pick 事件声明与触发、删除 onPick prop，父组件改用 @pick 更新 selectedFile。
- 教练执行 `pnpm build`，TypeScript 检查与 Vite 构建均通过；本次未启动前后端，未重新验证浏览器选择文件或真实上传。
- 已实际创建 ResultPanel.vue 待填写骨架；下一步由 ly 声明 result prop、迁移结果展示和样式，随后完成分段缩进。
- 后续验收：ly 已填写 ResultPanel，迁移六字段展示与 summary 样式，父组件通过 `status === 'done' && result !== null` 保证子组件接收非空结果；模板中的可见 `//` 文本已改成 HTML 注释。`pnpm build` 再次通过。下一步摘要分段与首行缩进，浏览器展示及真实上传尚未重验。
- 最新验收：摘要分段、首尾空白清理、空段过滤及 `text-indent: 2em` 已实现，旧全文摘要节点已删除。使用 Vue 编译器与服务端渲染，以明确标注的测试数据检查：摘要仅显示一次，截断提示 true/false 两分支通过，scoped 样式编译通过；但 input_tokens、output_tokens、cost、model 四个展示节点同时被删除，元数据展示检查未通过，待 ly 恢复。构建仍通过；本次无模型调用，未测浏览器视觉与真实上传。检查命令直接经标准输入运行，未创建临时文件。
- 再次检查：四个元数据展示行已恢复，标签及测试值的服务端渲染检查通过；但 ly 同时恢复旧全文摘要节点并注释 v-for，测试摘要实际仅生成一个 p，分段/去首尾空白/空段过滤未作用于展示。computed 仍存在；下一步恢复分段摘要节点、移除旧全文节点，保留四字段。测试先移除 HTML 注释再统计实际摘要节点，避免注释内的模板代码污染判据。截断提示两分支仍通过。
- 最后一次代码检查：ly 删除旧全文摘要节点并恢复 v-for，四字段保留。同一测试数据实际生成两个摘要 p，内容分别为「第一段测试」「第二段测试」，分段、trim 和空段过滤通过；四字段标签和值、截断提示 true/false 两分支及 scoped 样式编译均通过。pnpm build 的类型检查与构建通过。摘要目前位于元数据和截断提示之后，属于展示顺序选择；可移到标题之后。无模型调用，浏览器视觉、迁移后真实上传与正式复盘仍待完成；未代写核心代码，未创建临时文件。
- 文件清单：`week3/frontend/src/components/FilePicker.vue`、`FileUploader.vue`（ly 修改）、`ResultPanel.vue`（教练提供骨架）；`week4/README.md`、`LEARNING-PLAN.md`、`week1/CLAUDE.md`（更新进度）。
- 有意保留：FilePicker 的 Day 3 历史教学注释仍提及 onPick，不代表当前实现仍使用函数 prop。
- 浏览器验收：ly 确认上一轮给出的浏览器测试全部通过，包括 loading 提示与禁用、summarize 返回 200、摘要无重复与段落缩进、四字段展示及 truncated=false 时无警告。这是 ly 的实测反馈，教练未独立操作浏览器；truncated=true 分支的验证仍来自此前服务端渲染测试。Day 3 / Day 4 动手阶段收尾，下一步三题复盘，待 ly 作答后记录结果。

### Day 3 / Day 4 合并收尾复盘（2026-10-14）

- 合并三题得分 2 / 3，不拆成两份独立成绩。Q1：ly 回答通过 emit pick 传文件、selectedFile 由父组件修改，正确。Q2：ly 将额外非空检查归因于 idle 或其他状态，未答到 status 与 result 独立；idle 已被 status 条件挡住，教练讲解 done 本身不能证明 result 非空，不计独立通过。Q3：ly 回答依赖变化触发 computed 更新，正确；题面明确假设 ResultPanel 保持挂载。
- Day 3 / Day 4 收尾，非空检查纳入后续间隔回顾；官方学源阅读完成情况仍未自报，不补造完成记录。
- Day 5 首步：以假设新增、与 ResultPanel 并列的 CostPanel 展示同一结果 cost/model 为场景，回顾 result 的状态归属与传递。仅提出场景问题，待 ly 回答后讲解；尚未创建 CostPanel 或修改核心代码。
- 本次保存的接续问题：新增与 ResultPanel 并列的 CostPanel 后，共用的 result 应由哪个组件维护、怎样传给两个子组件？ly 尚未作答；下次从这里继续，不重复 Day 3 / Day 4 动手验收。
- Git 保存：本次原始推送被 GitHub 密钥保护拦截，原因是此前尚未发布的提交跟踪了根目录 .env。保留本机配置文件与旧提交的本地备份，从待推送历史排除 .env；推送范围为组件代码、学习进度及修正后的本机启动文档。`.env` 和 `.venv/` 继续忽略，不绕过 GitHub 保护。

### Day 5 状态提升（2026-10-15）

- 场景回顾：ly 回答共用 result 由 FileUploader 维护、通过 prop 传给两个子组件，正确，不计分。随后讲解状态提升与逐级传递；目前上移属于教学安排，CostPanel 尚未创建。
- ly 在教练示例指导下完成：App 持有唯一的 result ref，通过 prop 传给 FileUploader；FileUploader 经 result-change 通知清空与成功结果，再把收到的 prop 传给 ResultPanel。status、selectedFile、errorMsg 仍由 FileUploader 维护。
- 已讲解模板自动解包 ref 与 script 函数中使用 .value 的区别；事件处理箭头函数写在模板中时仍属于模板表达式。ly 已更正模板赋值并恢复 ApiError 类型导入。
- 教练执行 pnpm build，vue-tsc 类型检查与 Vite 构建均通过；未运行浏览器交互或调用模型。下一步先验证上传成功及再次上传时清除旧结果，再加入 App 下的 CostPanel 观察共享状态；Day 5 尚未完成，未出正式复盘题。
- 后续浏览器验收：ly 确认上传后摘要与四字段展示、再次上传时 loading 清除旧结果并显示新结果两条通过，教练未独立操作浏览器。已创建 CostPanel.vue 的 TODO 骨架，待 ly 声明非空 result prop、展示 cost/model，并在 App 中以 result 非空为条件接入；CostPanel 不维护另一份结果或调用接口。ResultPanel 原有 cost/model 暂时保留，作为两个读取者数值一致的对照，属于本轮有意重复展示。
- 文件清单：week3/frontend/src/App.vue、week3/frontend/src/components/FileUploader.vue（ly 修改）；ResultPanel.vue 仅有 ly 的缩进变化；week4/README.md、LEARNING-PLAN.md、week1/CLAUDE.md（教练更新进度）。核心代码未由教练代改。
- 新增文件：week3/frontend/src/components/CostPanel.vue（教练创建 TODO 骨架，尚未接入 App；实现由 ly 填写）。

### Day 5 接续（2026-10-16）

- 非空条件回顾：ly 回答 `v-if="result !== null"`，正确，不计分。
- ly 已填写 CostPanel 的非空 result prop 与 cost/model 展示，在 App 中导入并通过 `v-if="result"`、`:result="result"` 接入。当前 result 仅有对象或 null 两种值，此条件符合要求；ResultPanel 的重复字段按原安排保留作对照。
- 教练执行 `cd week3/frontend` 后运行 `pnpm build`，类型检查与 Vite 构建通过。尚未验证此次接入后的浏览器交互，未调用模型；下一步由 ly 检查初始隐藏、成功后两处数值一致、再次上传时费用面板随旧结果清空。Day 5 尚未完成。
- 文件清单：week3/frontend/src/App.vue、week3/frontend/src/components/CostPanel.vue（ly 修改）；week4/README.md（教练记录）。
- 浏览器验收：ly 确认此次 CostPanel 接入后的三条验证通过（初始隐藏、上传成功后 cost/model 与结果区一致、再次上传时旧费用清空并更新）；教练未独立操作浏览器。本日继续学习逐级传递的代价，provide/inject 仅按学源了解用途，暂不改代码；Day 5 尚未正式收尾、未出复盘题。同步更新 LEARNING-PLAN.md 与 week1/CLAUDE.md 的当前位置。
- 学源与对照实验：ly 确认已读，随后主动尝试在 App 提供 result、CostPanel 注入，范围由原定只阅读扩为小型对照实验。最初再次 ref(null) 生成独立状态，且 inject 类型误写为普通结果；教练说明原因与对应写法后，ly 已改为提供原 result、以 Ref<SummarizeResponse | null> 注入、模板条件渲染并读取 cost/model，移除 App 对 CostPanel 的 result prop 绑定。教练重跑 pnpm build，类型检查与构建通过；此次 inject 版浏览器行为尚待 ly 验证，不沿用 props 版验收。未调用模型，未出正式复盘题。文件清单：App.vue、CostPanel.vue（ly 修改），week4/README.md、LEARNING-PLAN.md、week1/CLAUDE.md（教练更新）；FileUploader.vue、ResultPanel.vue 的现有差异仅为空白，未由教练修改。
- Git 保存接续点（ly 授权记录并推送）：本轮保存状态提升代码、CostPanel TODO 骨架及三份进度文档；下一次从填写 CostPanel 的 result prop、展示 cost/model、在 App 中非空接入继续，尚未完成 Day 5。保存前重新执行 pnpm build 通过，fetch 后本地与 origin/master 无分叉；教练仅清理 App.vue、FileUploader.vue 各一处行尾空格。文件清单为 App.vue、FileUploader.vue、ResultPanel.vue、CostPanel.vue、week4/README.md、LEARNING-PLAN.md、week1/CLAUDE.md；.env 与 .venv 仍忽略。

### Day 5 正式复盘（2026-10-16 出题，2026-10-19 完成）

ly 确认 inject 版初始隐藏、上传成功后两处数值一致、再次上传清空并更新三条浏览器验证通过；教练未独立操作浏览器。动手与验证完成，以下三题待答，尚未评分或标记 Day 5 完成。

本次 Git 保存接续点（ly 授权记录并推送）：保留 App 提供同一 result ref、CostPanel 注入的当前版本；下次直接回答以下三题，由教练逐题点评后收尾 Day 5，不重复已完成的动手和浏览器验收。Pinia 留到 Day 6。此前本会话的 pnpm build 已通过，之后未改功能代码；保存时仅清理 ResultPanel.vue 一处行尾空格，该文件因此与 HEAD 一致。提交文件清单：week3/frontend/src/App.vue、components/CostPanel.vue、components/FileUploader.vue（仅新增空行），week4/README.md、LEARNING-PLAN.md、week1/CLAUDE.md。

1. 当前代码中，唯一一份 result 状态由哪个组件保存？只答组件名。
2. FileUploader 发出 `emit('result-change', null)` 后，等页面完成更新，CostPanel 还会显示旧费用吗？回答「会 / 不会」，并用一句话说明原因。
3. 假设 App 初始 result 为 `ref<SummarizeResponse | null>(null)`，把 `provide('result', result)` 改成 `provide('result', result.value)`，其他代码保持当前写法。上传成功后 App 的 result.value 已有结果，CostPanel 能显示费用吗？回答「能 / 不能」，并说明 provide 执行时实际提供了什么。

本次记录文件清单：week4/README.md、LEARNING-PLAN.md、week1/CLAUDE.md。源码未由教练修改。

#### 2026-10-19 作答与批改：2.5 / 3

- Q1：ly 答「App」，正确，1 / 1；唯一 result ref 由 App 保存。
- Q2：ly 答「不会，result 会更新，costpanel 重新调用」，结论正确、机制不准确，0.5 / 1。教练订正：App 将 result 设为 null，父模板的 v-if 不成立，CostPanel 被移除，不是重新调用它来展示空值。
- Q3：ly 答「不能，实际就已经解包了」，正确识别取出当前值而非提供原 ref，1 / 1；教练补明：执行 provide 时 result.value 为 null，之后 App 替换 result.value 不会更新这份已提供的 null。不要泛化为所有 .value 都不具响应性；对象值需区分属性修改与整体替换。
- Day 5 正式收尾。此前两版构建及 ly 确认的浏览器验证沿用 10-16 记录，本轮未重跑构建、浏览器或模型调用；仅更新学习文档。
- 下一接续点：Week 4 Day 6，先做不计分的间隔回顾，再讲 Pinia；回顾优先覆盖条件渲染与 provide 原 ref / 当前值的区别。ly 要求题目一次发齐，后续回顾或复盘同轮给出全部题目，答案另轮点评。
- 文件清单：week4/README.md、LEARNING-PLAN.md、week1/CLAUDE.md。未修改功能代码，未提交或推送。

### Day 6 开课（2026-10-19，回顾完成，Pinia 入门）

- 已按合约一次发齐三条不计分回顾，原题如下；作答与后续进度见本节末尾。
  1. App 中的 result 变成 null 后，v-if="result" 不成立。此时 CostPanel 是被移除，还是仍保留、只把费用文字清空？
  2. status 和 result 是两个独立状态。只知道 status === 'done'，能否断定 result 一定不是 null？回答「能 / 不能」，说明一句原因。
  3. 假设 ResultPanel 保持挂载，父组件传入了另一份结果，其中 summary 发生变化。用于摘要分段的 computed 会自动更新，还是需要手动调用？
- ly 补充月度要求：每完成一个课程月的内容，及时核查技术发展并更新计划，确保所学能实际使用。流程已写入 LEARNING-PLAN.md §0/§11 与 week1/CLAUDE.md 规则 13；本轮未把任何课程月标为完成，未调整 Day 6 的 Pinia 安排。
- 文件清单：LEARNING-PLAN.md、week1/CLAUDE.md、week4/README.md；仅更新教学约定和接续点，未修改功能代码，未执行构建、模型调用、提交或推送。

#### 回顾批改与首步任务

- 不计分。Q1：ly 答「保留组件，清空费用文字」，错误；教练订正为 v-if 不成立会移除并卸载 CostPanel，再次成立时重新创建。Q2：ly 答「不能，……」，判断正确、原因未展开；教练补明 status 与 result 独立，设置 done 不会自动使 result 非空。Q3：ly 答「自动更新」，正确；摘要 computed 的依赖变化后，在下次读取时重新计算，无需手动调用。
- 已核对 package.json 声明 Pinia ^4.0.2，main.ts 已 app.use(createPinia())，src/stores/counter.ts 已有 Setup Store 示例。无需重复安装注册；本轮未运行安装或修改源码。
- 正课使用已有 counter 示例讲解 store、state、getter、action、defineStore 与 useStore；说明同一应用同一 Pinia 实例中的共享状态、store 属性解包及直接解构基本类型的陷阱。目标是将唯一 result 搬入 summarize store，上传请求和本地交互状态仍留在 FileUploader，ResultPanel 继续接收结果 prop。
- 已查官方资料：[Defining a Store](https://pinia.vuejs.org/core-concepts/)、[State](https://pinia.vuejs.org/core-concepts/state.html)、[Vue 条件渲染](https://vuejs.org/guide/essentials/conditional.html)，核查日期 2026-10-19。当天学源按挂载表预算 40 min，跳过插件、SSR 和 getters 高级用法，出处 LEARNING-PLAN.md §2 的 Pinia 条目；ly 是否阅读及实际时长尚未自报。
- 首步由 ly 新建 src/stores/summarize.ts，按对话 TODO 骨架填写 result 的 ref 声明、setResult 的赋值和 return。未创建该文件或代填核心实现；组件迁移、类型检查、构建、浏览器验证均待后续完成。
- 文件清单：week4/README.md、LEARNING-PLAN.md、week1/CLAUDE.md；本轮仅更新教学记录，未提交或推送。
- 2026-10-20 Git 保存接续点（ly 授权推送）：Day 6 正课及 TODO 骨架已在对话给出，当前 src/stores/summarize.ts 尚不存在。下次从阅读 Defining a Store 与 State、创建 useSummarizeStore 开始：声明初始 null 的 result ref、在 setResult 中保存新值、返回 result 和 setResult；完成后由教练检查再迁移组件。学源阅读尚未由 ly 确认，本日核心实现与验收均未完成。本次提交仅含上述三份学习文档。

### 不要报成 bug 的清单

- 未选文件时按钮可点击是现有设计，由 handleSubmit 显示 No file selected；只有 loading 时禁用。教练此前的按钮验收条件已更正。
- Day 3 保留函数 prop 是对照教学安排；Day 4 已迁移为 emit。
- 前端仍放在 week3/frontend，Week 4 的目录重构留到 Day 7。
- Day 5 按 ly 的提问新增 provide/inject 对照实验：CostPanel 改为注入，FileUploader → ResultPanel 仍保留 props 链，用于对照；共享结果仍只有 App 中一份。

### 本次文件清单

- `week3/frontend/src/components/FilePicker.vue`、`FileUploader.vue`：ly 完成组件拆分与父子连接；教练仅更正误导性注释和空白。
- `week3/frontend/package.json`、`pnpm-lock.yaml`：固定 Windows 本地 pnpm/Node 运行时。
- `week3/frontend/README.md`：补齐前后端启动步骤和验证记录。
- `week4/README.md`、`LEARNING-PLAN.md`、`week1/CLAUDE.md`：更新当前位置、验收证据和下一步。
