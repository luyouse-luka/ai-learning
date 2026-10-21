# Week 4 学习日志 · 组件拆分与 Prompt 工程

> 2026-10-20 目录迁移：应用代码现位于 `frontend/` 与 `backend/`；本日志旧路径按根目录 [README](../README.md) 的映射阅读，按周练习与日志继续保留。

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
| 6 | 主线 | **Pinia 入门**：把提升上去的状态搬进 store，对照 Day 5 那版看省掉了什么 | `stores/summarize.ts` | ☑ 指导下完成迁移，构建通过，ly 确认浏览器三条验证通过；学源阅读与旧代码清理仍待核实 | 2 / 3 |
| 7 | — | 巩固：三版对照（单组件 / props 提升 / Pinia）+ Week 4 总复盘 + **目录重构**（Week 3 欠的） | — | ◐ 三版对照、目录迁移、V2 接入及真实 PDF 验证完成；正式复盘已批改，周自检 5/6，独立发现项待证据 | 2.5 / 3 |

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
- [x] **目录重构** —— 2026-10-20 按 ly 选定结构将应用移至根目录 `frontend/` + `backend/`，各周练习、样本与日志保留；当前入口与映射见根 README，历史日志保留当时路径。
      验证：迁移前后构建通过，根配置和实验路径、健康/静态/422/400 检查通过，Vite `/api/health` 联调 200；详见本日迁移记录及 `tools/verify_workspace_layout.py`。
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

- [x] 能用 5 段结构写出一个 200+ 字的 system prompt，并说清每段在管什么 —— 2026-10-21 ly 贴出 backend/prompts.py 的 V2 并说明五段用途；结构项通过，不代表效果或接口接入通过。
- [x] 至少 3 种 prompt 技法真用在 `/summarize` 上，**有前后对照的实测输出**（不是「感觉变好了」） —— 2026-10-21 ly 导入包含角色/示例/负向约束的 V2；未 strip 的 V1/V2 输出保存在 day2_v1.txt、day2_v2.txt。真实 attention.pdf 调用 V2 接口返回 200、285 字符、未截断，缺文件 422 / 非 PDF 400 通过，证据 day7_api_v2_2026-10-21.json。接入按教练两处指导完成；本项证明已应用并留存对照，不代表各技法独立增益已证实。
- [x] 能说清 props 和 emit 各自的方向，并答出「**子组件不许直接改 props**」及其原因 —— 2026-10-21 ly 说明父传子、父组件维护值，并解释 emit 的事件名和载荷；教练补明单向数据流与通过事件请求修改。
- [x] 拆出的子组件能独立跑通，父组件只负责协调 —— 2026-10-21 ly 正确说明 FilePicker / FileUploader / ResultPanel 职责；运行证据沿用 Day 3/4/6 的构建及本人浏览器确认，本轮未重新操作浏览器；独立指职责分离，不要求脱离必要 props 单独运行。
- [x] 能说出「状态提升」难受在哪，以及 Pinia 具体省掉了哪一步（**要能举出自己代码里的行**） —— 2026-10-21 ly 对照 props、provide/inject 与 Pinia，说明去掉 App 的结果声明和传递，并举出 useSummarizeStore() / summarizeStore.result.cost；唯一 result 实际仍由 store 维护。
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

### Day 6 接续验收（2026-10-20）

- ly 要求重开 Day 6；三条不计分回顾（v-if 卸载、status/result 独立、provide 当前 null 与原 ref 的区别）均答对。
- ly 表示不会写后，教练给出完整 Setup Store 示例；ly 在原 counter.ts 中填写，按指导改名 summarize.ts，并补齐 setResult 接受 null。后续组件按教练逐处指导迁移，不计作独立盲写。
- 当前数据流：唯一 result 保存在 summarize store；FileUploader 调用 setResult 清空及保存响应，ResultPanel 仍接收非空 prop，CostPanel 直接读取 store，App 不再维护或传递结果。
- 教练执行 pnpm run build，vue-tsc 类型检查与 Vite 生产构建均通过。最后一次源码检查仍见部分旧注释与未使用导入，已告知清理；此后清理结果未独立核实。
- ly 在三条浏览器验收要求后回复「完成」：记为本人确认初始隐藏、成功后摘要与费用出现且数值一致、再次上传时旧结果清空并成功更新。教练未独立操作浏览器或调用模型；失败路径本轮未验。官方学源是否阅读及实际时长仍未自报。
- 正式复盘三题待答：① 当前唯一 result 保存在哪个文件？② store 内部与组件通过 store 访问 result 时各是否需要 .value？③ 若删掉上传前 setResult(null)，一次成功后再次上传失败，CostPanel 会隐藏还是仍显示上次费用，为什么？答完点评后再收尾 Day 6。
- 文件清单：本轮学习代码涉及 week3/frontend/src/stores/counter.ts → summarize.ts、App.vue、components/FileUploader.vue、components/CostPanel.vue；教练本次仅修改 LEARNING-PLAN.md、week1/CLAUDE.md、week4/README.md 保存进度，未提交或推送。

### Day 6 正式复盘批改（2026-10-20）：2 / 3

- Q1：ly 答 store/summarize 文件，状态归属正确，1 / 1；Q2：store 内部 result.value、组件 summarizeStore.result，两处均正确，1 / 1。
- Q3：ly 答会隐藏，理由为 result 更新会隐藏，0 / 1。题设删掉了上传前 setResult(null)，第二次请求失败不执行成功分支，只修改 status/errorMsg；store 的 result 保留上次响应，CostPanel 的 v-if 仍成立，旧费用继续显示。ResultPanel 另受 status === 'done' 约束，失败后隐藏，不能用它的显示状态推断 CostPanel。
- 下一接续点：Day 7 不计分回顾优先复习「状态独立、失败路径不自动清空共享结果」，再做三版对照和原定目录重构。Day 6 实现、验收和复盘完成；学源阅读与旧代码清理尚未核实，不据此补记已读或已清理。
- 本次仅更新 LEARNING-PLAN.md、week1/CLAUDE.md、week4/README.md；未改源码、重跑构建、提交或推送。

### Day 6 Git 保存接续点（2026-10-20，ly 授权记录并推送）

- 保存 Pinia 迁移及正式复盘 2/3；下次从 Day 7 的不计分回顾开始，优先复习「失败不会自动清空旧结果」，再做三版对照与目录重构，不重复 Day 6 动手验收。
- 保存前 fetch，HEAD 与 origin/master 无分叉；重新执行 pnpm run build，类型检查与生产构建通过。浏览器三条验证沿用 ly 本轮确认，失败路径未实测，学源阅读未自报。
- 复查确认 App、FileUploader、CostPanel 中部分旧 props/emit/provide 注释和 TODO 仍保留，后续清理；未代写或改变业务逻辑，仅清理新 store 一处行尾空格。
- 本次文件清单：LEARNING-PLAN.md、week1/CLAUDE.md、week4/README.md、week3/frontend/src/App.vue、components/FileUploader.vue、components/CostPanel.vue、stores/counter.ts（删除）、stores/summarize.ts（新增）；后五项均位于 week3/frontend/src。仅暂存这份清单，.env、.venv 与 dist 不在本次变更中。

### Day 7 开课与三版对照（2026-10-20）

- 已按 ly 指令执行 git pull --ff-only，更新至 04e5675，未覆盖本地未跟踪文件。
- 三条不计分回顾：① 假设删除上传前 setResult(null)，先成功一次再失败且失败仅改 status/errorMsg，CostPanel 隐藏还是显示旧费用？② store 内和组件中读取结果分别如何写？③ v-if 从真变假时卸载组件还是只清空文字？
- ly 原答：①「继续显示上次的费用，因为调用失败，不会调用result」；②「内部 summarizeRespose.result.value，组件直接调用 summarizeResponse.result」；③「组件会被卸载」。
- 订正：Q1 判断正确，准确原因是失败分支未更新或清空 store.result，旧值保留；result 是状态而非被调用的函数。Q2 组件通过 store.result 的访问层级正确，变量名以声明为准；本项目为 summarizeStore.result。store 内部 result 直接由 ref 声明，读取用 result.value，不再加外层对象。Q3 题面未明确 v-if 位置，作废，不归为学习者错误：组件标签上的 v-if 可卸载该组件，但当前 Pinia 版 App 的 CostPanel 标签无条件，v-if 位于 CostPanel 内部 section，只移除 section，CostPanel 实例保留。教练核对源码后纠正此前将其直接判对的说明。
- 已核对三版真实来源：82a658b 的父提交中 FileUploader 保存 result 且内联展示；f6bd30e 中 App 保存 result，FileUploader emit 更新、ResultPanel 接收 prop；04e5675 中 summarize store 保存 result，FileUploader 调 setResult、CostPanel 直接读取，ResultPanel 仍接收 prop。Day 5 provide/inject 作为附加对照，状态仍由 App 保存。
- 本日先对照状态归属与读写路径，再清理迁移遗留，随后核对目录迁移范围及引用并做 Week 4 自检。首步动手交给 ly：清理 App.vue 内已失效的 ref/provide 注释、旧 result 声明及 result-change/条件渲染说明，保留当前可执行代码；完成后教练检查。尚未修改源码或移动目录。
- 本段学源：复看 Pinia「Defining a Store → Using the store」，预算 10 min，跳过插件、SSR、getter 高级用法，出处 LEARNING-PLAN.md §2 Pinia 条目及本周学源挂载表；三版对照另读项目历史。阅读完成尚待 ly 自报；目录迁移所需资料在进入该步骤前给出。
- 本轮文件清单：week4/README.md、LEARNING-PLAN.md、week1/CLAUDE.md；仅更新学习记录，未运行构建、浏览器验收、模型调用、提交或推送。Day 7 与 Week 4 未标记完成。

#### 清理暂缓，进入目录重构准备

- ly 删除了 App.vue 脚本区的旧 ref/provide 注释和 CostPanel.vue 的三个旧导入注释；App.vue 两条模板说明及 CostPanel.vue 三条旧 TODO 仍保留。ly 明确要求「忽略，开始下一个」，剩余注释清理暂缓，不标记全部清理完成。两份组件的现有改动由 ly 完成，教练未覆盖。
- 迁移前基线：在原 week3/frontend 运行 pnpm build，类型检查与 Vite 构建通过；通过根 .venv 的 FastAPI TestClient 调用现有 /health，HTTP 200、status=ok、api_key_configured=true；未调用模型。该结果不代表真实上传或失败路径已经重验。
- 已发现路径依赖：main.py 用 BASE_DIR.parent.parent 定位根 .env；prompts.py 用相对父目录定位 week2 样本和 week4 输出；Vite/TypeScript 的 src 别名基于前端自身目录。移动后须对应调整并重验。
- 旧文档只有 stage1-frontend/ + stage3-ai/ 候选，尚未定稿。已向 ly 提出一次结构选择：推荐 frontend/ + backend/ 放应用代码，week1–week4 保留练习与日志；另一选项沿用旧阶段式归档。等待结构选择期间未移动目录、修改后端或升级依赖。
- 本轮文件清单：week4/README.md、LEARNING-PLAN.md、week1/CLAUDE.md（教练更新），App.vue、CostPanel.vue（ly 已有改动）；未提交或推送。

#### 目录迁移与验证（2026-10-20）

- ly 选择根目录 `frontend/` + `backend/`。已将 `week3/frontend/` 的应用文件移至 `frontend/`，`week2/api/` 移至 `backend/`；按周样本、练习和学习日志保留，教学合约仍为 `week1/CLAUDE.md`。
- 路径调整：backend/main.py 从新位置定位根 `.env`；backend/prompts.py 显式定位仓库根，样本仍读取 week2/attention_extracted.txt、对照输出仍写入 week4；frontend/src/types/api.ts 的后端出处更新为 backend/main.py。请求、状态管理、模型参数和业务逻辑均未改写。
- 当前启动步骤统一见根 README.md，前端 README 更新；week2/week3/week4 日志入口补迁移映射，旧学习记录中的旧路径作为历史保留。LEARNING-PLAN.md 与教学合约更新当前入口。
- Windows pnpm 依赖使用绝对目录链接，迁移后按原锁文件离线重建，复用 312 个缓存包、下载 0 个包。43 个已跟踪应用文件逐项校验，只有预定的两份后端路径配置、前端 README 和类型文件出处注释内容变化；其余 39 个文件（包含 ly 两份组件修改）保持一致，根 `.env`、锁文件保持不变。
- 迁移后实测：frontend 的 pnpm build（类型检查 + 生产构建）通过；`.venv/Scripts/python.exe tools/verify_workspace_layout.py` 从无关工作目录验证根配置、Prompt 输入/输出路径以及健康 200、静态页 200、缺少文件 422、非 PDF 400；全部通过，无模型调用。
- 临时启动本次自己的 backend.main:app 和 Vite，实测后端健康、前端页面及 Vite `/api/health` 均 200；两次工具管理的服务会话已停止。未将此记为浏览器交互或真实 PDF 上传验收。
- 有意遗留：旧依赖缓存 frontend/.migration-node-modules/、week3/frontend/node_modules/ 的链接已解除，余下普通文件的递归删除被自动审批拒绝（仅返回 blocked by policy）；保留并通过根 .gitignore 忽略。旧路径无应用入口，不应从旧目录启动；缓存不属于源码迁移清单。CostPanel 与 FileUploader 的历史教学注释按 ly 要求暂缓清理。
- 文件清单：43 个应用文件从 week3/frontend、week2/api 映射至 frontend、backend；新增 README.md、tools/verify_workspace_layout.py、docs/superpowers/plans/2026-10-20-app-directory-migration.md；修改 .gitignore、LEARNING-PLAN.md、week1/CLAUDE.md、week2/README.md、week3/README.md、week4/README.md。具体内容变更为 backend/main.py、backend/prompts.py、frontend/README.md、frontend/src/types/api.ts；App.vue、CostPanel.vue 保留 ly 先前改动。
- 接续点：目录迁移验证完成，Week 4 六项结束自检与 Day 7 正式复盘尚未完成；不标记本周或课程月完成。未提交、推送或部署。
- 只读复核：后端仅有路径和启动示例变化，前端保留 ly 既有修改；未发现迁移导致的运行回归。复核发现教学合约一条当前启动说明仍指向旧 frontend README，已修正为根 README / frontend README。

#### Day 7 Git 保存接续点（2026-10-20，ly 授权推送）

- 保存 frontend/ + backend/ 目录迁移、路径修正、根启动说明、可复跑验证脚本、三版对照及回顾记录。App.vue、CostPanel.vue 保留 ly 的注释清理改动；其余暂缓清理的教学注释继续保留。
- 下次从 Week 4 六项结束自检开始，再完成 Day 7 正式复盘；不重复目录迁移或 Day 6 动手验收。Week 4、Day 7 及课程月验收尚未标记完成。
- 提交清单：应用的 43 个文件按旧目录映射迁移；.gitignore、README.md、LEARNING-PLAN.md、week1/CLAUDE.md、week2/README.md、week3/README.md、week4/README.md、tools/verify_workspace_layout.py、docs/superpowers/plans/2026-10-20-app-directory-migration.md。根 .env、.venv、依赖、构建产物和旧依赖缓存均忽略；两份 Zone.Identifier 未跟踪文件不纳入提交。

### Day 7 结束自检接续（2026-10-21）

- ly 要求问题一次发齐；已批改本轮回答。六项自检目前 4 项通过，Prompt 三技法的接口落地与独立发现 bug 两项未通过；不另计正式复盘分数。ly 暂时想不起独立 bug，不代编记录；Day 1 的「首行」歧义仅有独立问题贡献记录，未擅自等同本项通过。
- 五段结构回答正确。三种技法是 Role Prompting、示例提示（本版本仅一组输入/输出，严格称 one-shot）、负向约束；V1/V2 是两版 prompt，与技法数量不同。当前 backend/main.py 仍使用旧 SYSTEM_PROMPT，V2 仅在 backend/prompts.py 的实验中。六份输出存在，但不能据此断言三种技法分别有效；r1 由 ly 实做，r2/r3 是教练接手。
- 复核发现旧缩进归因不成立：backend/prompts.py 的 summarize() 在落盘前对 content 调用 .strip()。本地无模型验证显示，字符串开头的两个 U+3000 会被移除，第二段开头保留，足以制造旧记录中的现象。原始 API 内容未保存，无法还原当时模型是否生成首段缩进；上文「prompt 层改不动」「西文排版惯例」「三轮实验排除了路 A」不再作为有效结论。ResultPanel 用 CSS 排版的实现保留，但理由应为展示层统一控制，不能引用上述实验作模型能力证据。
- 本轮只读核查应用与旧输出，运行 .strip() 最小验证；未修改核心代码、调用模型、重新构建或进行浏览器验收。学源补充：Anthropic Prompting best practices 的 Use examples effectively / Give Claude a role / Control the format of responses，复看预算 10 min，跳过模型专属、thinking 与 agents 小节；核查日期 2026-10-21，https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices 。该文档针对 Claude，DeepSeek 的具体效果仍需本项目实测；ly 阅读未自报。
- 同日代码检查：ly 已去掉 backend/prompts.py 返回 content 时的 .strip()。教练提取当前实际 summarize / measure 函数，用模拟响应验证两个 U+3000 开头的文本原样返回、首段前缀原样检测；两条断言通过，无 API 请求、无输出文件写入。measure 中 if p.strip() 仅筛除空白行，不改写保留下来的 p；compare 将返回文本直接落盘。真实模型对照尚未重跑，旧六份输出不能恢复已丢失的空白。
- ly 授权继续跑对照后，教练执行 `.venv/Scripts/python.exe -m backend.prompts`，退出码 0，两版分别完成一次模型调用并保存未 strip 的文本至 week4/day2_v1.txt、day2_v2.txt；旧 r1/r2/r3 六份文件保留。使用同一 week2/attention_extracted.txt、脚本配置的 deepseek-v4-flash，只换 system prompt；temperature / max_tokens 均未显式传入，不能把未接线的 MAX_OUTPUT_TOKENS=1500 当作生效参数。原始文本指未裁剪的 message.content，不含完整响应元数据；脚本未记录 usage，故本轮不报告 token / 费用。
- 本轮跑前判据为 len(s) <= 400（含空白与标点的总字符数），以及每个非空段落以两个 U+3000 开头。落盘后读取复核：V1 为 304 字符、2 段、2/2 段缩进；V2 为 319 字符、3 段、3/3 段缩进；两版均通过两项判据。首段前四字符分别为 '\\u3000\\u3000《A' 与 '\\u3000\\u3000论文'。旧模型无法首段缩进的结论已被本轮反例进一步否定；单轮不能证明长期稳定性、V2 语义质量优于 V1 或各技法的独立效果。本轮未做摘要事实核验、接口接入或浏览器验收。
- 接口接入检查：ly 已在 backend/main.py 导入 SYSTEM_PROMPT_V2 as SYSTEM_PROMPT，并移除旧字符串定义。教练导入实际模块，断言 main.SYSTEM_PROMPT 与 prompts.SYSTEM_PROMPT_V2 为同一对象，POST /summarize 路由处理函数及其全局 SYSTEM_PROMPT 均对应当前 V2；通过。tools/verify_workspace_layout.py 的目录/配置/实验路径、健康 200、静态页 200、缺文件 422、非 PDF 400 均通过，无模型调用。未启动或重启常驻服务，未验证真实 PDF 成功响应和浏览器。
- ly 授权启动后端并做真实 PDF 验证：教练启动本地 uvicorn backend.main:app，监听 127.0.0.1:8000（本轮 PID 20928，工具会话 84457），保留运行。通过真实 HTTP 上传 week2/attention.pdf，7.692 秒返回 200；六字段类型与非空摘要校验通过，285 字符、2 段、truncated=false、input_tokens=10501、output_tokens=705、model=deepseek-v4-flash。服务返回 cost=0.00166754，按项目现有常量计算，不作为已核实账单费用。运行中服务缺文件 422、非 PDF 400、健康 200 均通过，边界请求未调用模型。本轮一次真实总结请求；最初 httpx 客户端探针因依赖不可导入在发请求前退出，改用标准库完成，未安装依赖或重试总结。
- 原始 HTTP 响应、PDF SHA256、时间、耗时及七条明确判据保存为 week4/day7_api_v2_2026-10-21.json。接口仍有 content.strip()，因此首段空格在接口响应中被清掉；这是现有返回处理，展示缩进由 ResultPanel 的 CSS 控制，本轮未改，不将它归因于模型。未进行浏览器操作或摘要事实核验。
- Day 7 正式复盘批改：2.5/3。Q1 旧定义在导入之后赋值会覆盖 V2，正确，1/1；Q2 判断不能证明 V2 更好正确，但理由未涉及单次采样、两版同时改动多处与因果无法分离，也未指出被推翻的旧模型首段缩进结论，0.5/1。V1 实际也有「首行缩进」，只是未像 V2 细化到每段及全角空格，不能说 V1 完全没有缩进要求；Q3 正确识别删除清空后失败不更新 result、status 独立，因此费用仍显示，1/1。教练补充解释不计为本人独立答题。
- 排期订正：教练前一轮说「复盘后进入课程月验收」过早。LEARNING-PLAN.md §1 与本周定位是主线第 1 个月第 2 周；§2 第 1 个月的 Git / Vite / TypeScript 条目尚有未完成或待核验证据，当前不能认定课程月结束。先核对并补齐必修内容，完成后再按 §0 做官方资料更新及功能/变式月验收；本轮未执行或宣称月验收完成。
- 下一接续点：正式复盘完成，六项自检仍为 5/6；仅独立发现 bug 尚缺本人证据，不代编或把教练发现计为本人发现。V2 及真实正常/边界路径已验证，不重复调用模型；先补周自查证据并核对课程第 1 个月剩余条目，Week 4 尚未全部收尾。文件清单：week4/README.md、LEARNING-PLAN.md、week1/CLAUDE.md（教练记录）、backend/prompts.py、backend/main.py（ly 修改）、week4/day2_v1.txt、week4/day2_v2.txt、week4/day7_api_v2_2026-10-21.json（新验证输出）；未提交、推送或部署。

#### 课程第 1 个月基础项核对与接续（2026-10-21）

| 条目 | 当前证据 | 尚待完成 |
| --- | --- | --- |
| Git / GitHub | 仓库已有提交历史；其中有教练代操作 | 本人分支、PR、回退及计划列出的日常命令练习，不能以有提交直接判掌握 |
| Vite | 脚手架、代理与健康接口联调、别名、开发环境变量、类型检查及生产构建已有记录 | 开发/生产环境变量差异与部署后的接口地址解释、验证 |
| TypeScript | 接口、联合、可选属性、注解、泛型和断言已用于当前代码；有效 strict=true | 泛型迁移、工具类型、断言边界等的独立解释与练习 |

- 当前实际安装 Vite 8.2.0、TypeScript 6.0.3；通过包版本查询和 vue-tsc --showConfig 核对，另有 noUncheckedIndexedAccess=true。pnpm 按现有锁文件恢复本地依赖，缓存复用 312、下载 0；package.json 与 pnpm-lock.yaml 无改动。未升级依赖、未重跑模型或浏览器验收。
- FileUploader 当前错误参数已是 unknown，并使用 axios.isAxiosError<ApiError>；旧 Week 3 的 any 待清理说明不再作为当前任务。Vite 8 已改用 Rolldown/Oxc，LEARNING-PLAN.md §2 的旧 Rollup 说明按官方迁移文档订正：https://vite.dev/guide/migration.html 。
- 下一步学源：Learn Git Branching 中文版 https://learngitbranching.js.org/?locale=zh_CN ，只做 Introduction Sequence 的 Introduction to Git Commits 与 Branching in Git 两关，预算 20 分钟；跳过 merge/rebase、远端与剩余关卡。官方关卡出处 https://learngitbranching.js.org/generatedDocs/levels.html ，计划出处 LEARNING-PLAN.md §2 第 1 个月 Git 条目。
- 操作由 ly 在网页模拟仓库完成，教练不代做，不改变真实仓库；提交两关各自使用的命令顺序及是否通关后检查。最初仅安排练习；后续 ly 反馈前两关已完成，按本人反馈记录，教练未独立复核命令，Git 总项仍待后续练习。Day 7 正式复盘仍 2.5/3，周自检仍 5/6，课程月未完成。
- 接续安排：基础篇 Merging in Git 与 Rebase Introduction（第 3/4 关），预算 20–30 分钟，学源及计划出处同上；只完成这两关，暂跳过高级篇、远端与真实仓库操作。按网页引导操作，记录命令顺序与提交图变化，完成后一起反馈。随后 ly 反馈第 3/4 关完成，基础篇前四关按本人反馈记录；未独立复核命令，不据此认定已掌握 merge/rebase。
- 真实项目接续：由 ly 在项目根运行 git status --short、git log --oneline -5、git diff -- backend/main.py、git diff -- backend/prompts.py，预算 15 分钟，输出一起反馈；本段先查看状态/历史/实际差异，随后再讲暂存和分块提交。教练已只读确认两个后端文件存在未提交差异，未操作暂存、提交、回退或远端。学源为 Pro Git 中文 §2.2 的“检查当前文件状态”“查看已暂存和未暂存的修改”及 §2.3 的基本日志示例，跳过本段之外高级选项；出处 LEARNING-PLAN.md §2 Git 的 12 命令条目。链接：https://git-scm.com/book/zh/v2/Git-基础-记录每次更新到仓库 、https://git-scm.com/book/zh/v2/Git-基础-查看提交历史 。操作结果待本人反馈。
- 本人已贴 status/log 与 main.py 的部分 diff，随后正确概括 main.py 导入 V2 并删除旧 prompt、prompts.py 去掉返回内容的 strip；教练复核当前源码差异相符，暂存区为空。下一步讲工作区/暂存区/提交及暂存后继续修改的边界，由 ly 用 git add -p -- backend/prompts.py 只选择 strip 修复，再用 git diff --cached 检查文件清单及内容；随后 ly 贴出暂存状态，教练只读核对 cached 文件清单仅有 backend/prompts.py、cached diff 仅去掉 strip，且该文件无额外未暂存差异，暂存练习通过；本人随后完成提交 1b5a0bd（fix: preserve leading whitespace in prompt comparisons）；教练核对该提交仅含 prompts.py 的 1 行删除/1 行新增，暂存区为空。下一步由本人按同一流程独立暂存并提交 main.py 的 V2 接入（导入 V2、删除旧定义两块放在一起），提交说明用 feat:，完成后反馈最新提交、文件清单和状态；本人已完成提交 cbaaeda（feat: use V2 prompt for PDF summaries）；教练核对仅修改 backend/main.py，两块改动齐全，暂存区为空。本次依照教练具体命令操作，不标记为完全独立完成。下一步由本人用 git add -- 明确列出 LEARNING-PLAN.md、week1/CLAUDE.md、week4/README.md 及 day2_v1.txt、day2_v2.txt、day7_api_v2_2026-10-21.json 六份文件，检查 cached 文件清单后归档；旧 week3/frontend 迁移残留不纳入。已有学源 Pro Git §2.2“跟踪新文件”“暂存已修改的文件”，复看 5 分钟、实操 5 分钟，跳过删除/移动与撤销；出处 LEARNING-PLAN.md §2 Git 日常提交条目。后续归档已完成，提交 0c789d6 包含上述六份文件。教练未代暂存或提交。学源 Pro Git §7.2“暂存补丁”一节，预算阅读 5 分钟 + 实操 10 分钟，跳过 add -i 菜单与补丁手动编辑，出处 LEARNING-PLAN.md §2 的 add -p / diff --staged。https://git-scm.com/book/zh/v2/Git-工具-交互式暂存 。
- 本段文件清单：LEARNING-PLAN.md、week4/README.md、week1/CLAUDE.md，仅同步学习证据与下一步；未提交、推送或部署。
- Git 分支练习核对：笔记正文经 amend 纳入 f498d41；master reflog 记录 Fast-forward，当前 master 指向 f498d41；codex/git-practice 与误拼的 codex/git-practive 已清理，原备份分支保留。以上由本人依指导操作，教练只读核对，不记为独立掌握。周自检仍 5/6，独立 bug 证据待补。
- 接续 stash / stash pop（LEARNING-PLAN.md §2 的 12 命令条目）：布置时以三份尚未提交的学习记录练习收起和恢复，预算阅读 5 分钟、实操 10 分钟。学源 Pro Git §7.3 的贮藏与应用贮藏，以及 git-stash 官方文档的 push / pop；跳过清理、包含未跟踪/忽略文件及多条贮藏恢复。尚未收到本人执行输出，未验收；判据为仅三份记录被收起、恢复前后内容一致、HEAD 仍为 f498d41，且本次贮藏成功恢复后从列表移除。https://git-scm.com/book/zh/v2/Git-工具-贮藏与清理 、https://git-scm.com/docs/git-stash 。

- 本轮归档（用户明确要求记录进度并推送）：同步 LEARNING-PLAN.md、week1/CLAUDE.md、week4/README.md，记录已完成的 amend / 快进合并 / 分支清理与 stash 待验收状态；提交和远端同步由教练执行，不记为本人独立 Git 练习。推送目标 origin/master，包含此前四次本地提交；旧 week3/frontend 迁移残留不纳入。当前三份记录内容与布置 stash 时的 SHA256 一致、贮藏列表为空，但这不能证明已执行过收起和恢复。归档后这三份记录不再有待提交差异，下次 stash 练习先新增小幅笔记修改。

#### Git stash 实操验收（2026-10-21）

- ly 在本轮教练指导下新增末尾第 4 条练习笔记，使用限定 week4/README.md 的 stash push 收起，再执行 stash pop 恢复；教练仅执行只读检查，未代操作。
- 收起后已跟踪文件无待提交差异，新 stash 的 diff 仅含该笔记及原文件末尾换行变化；恢复前后 git hash-object 均为 bd52503a7a696092215a52b97aef6c69791e4f69，HEAD 保持 e6ee019。练习 stash 已移除，原 r-pull-20260910 旧 stash 保留；两个 Zone.Identifier 文件始终未跟踪。该步验收通过，不记为独立掌握。
- 下一接续点：由 ly 检查三份学习记录的 diff、明确暂存范围并提交，反馈提交及状态后核对；随后继续剩余 Git 命令。周自检仍 5/6，独立 bug 证据仍待补，Git 总项与课程月均未完成。
- 文件清单：LEARNING-PLAN.md、week1/CLAUDE.md、week4/README.md；保留 ly 的第 4 条练习笔记，仅更新进度，未提交或推送。

### 不要报成 bug 的清单

- 未选文件时按钮可点击是现有设计，由 handleSubmit 显示 No file selected；只有 loading 时禁用。教练此前的按钮验收条件已更正。
- Day 3 保留函数 prop 是对照教学安排；Day 4 已迁移为 emit。
- 2026-10-20 起应用代码位于 frontend/ 与 backend/；旧路径的本地依赖残留被 Git 忽略，不是第二份应用，历史日志按根 README 的映射阅读。
- Day 5 的 provide/inject 是历史对照实验；Day 6 起 CostPanel 读取 Pinia store，FileUploader → ResultPanel 继续保留 props，属于展示组件的接口设计。

### 本次文件清单

- `week3/frontend/src/components/FilePicker.vue`、`FileUploader.vue`：ly 完成组件拆分与父子连接；教练仅更正误导性注释和空白。
- `week3/frontend/package.json`、`pnpm-lock.yaml`：固定 Windows 本地 pnpm/Node 运行时。
- `week3/frontend/README.md`：补齐前后端启动步骤和验证记录。
- `week4/README.md`、`LEARNING-PLAN.md`、`week1/CLAUDE.md`：更新当前位置、验收证据和下一步。


Git 实操记录
1. 三次提交分别保存了: 1. 去掉 .strip() 2. use V2 prompt for PDF summaries 3. record V2 verification and Git practice 
2. 暂存指的保存下一次提交准备采用的文件内容，提交完成不代表已经上传到 GitHub，提交是存入本机档案
3. 创建分支 git branch <branch-name>,切换分支 git switch / git checkout
4. stash 实操：这是一条尚未提交的练习笔记。