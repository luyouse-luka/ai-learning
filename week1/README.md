


# LLM API Week 1 学习日志


> 目标：7 天从零掌握 LLM API 调用全流程，每天产出可运行代码 + 复盘笔记。
> 配套：`/home/ly/project/screen-ai-deepdive.pdf` 第二章
> 教学合约：见 `CLAUDE.md`

---

## 学者水平评估（教练填，截至 2026-06-15 / Day 5）

> 此节由 Claude Code 根据每日复盘 + 出题得分客观评估，每周更新一次。不夸饰。

**出题得分轨迹**：Day1 1.8 → Day2 1.5 → Day3 2.1 → Day4 2.7 → Day5 2.0 → Day6 1.8（满分 3）

**2026-07-21 更新**：已插做 **Week 0.5 Python 急救**（list/dict + 文件读写/try-except + 结业脚本「读文件→调 API→存 JSON」，全部跑通）。回来做 **Day7 综合考核 Part 2 得 8/10**（过线）。messages 结构等老症结基本焊死，语法地基补上。**剩 Day7 Part 3 大盲写未做**——那是解锁 Week 2 的真门槛。

**已掌握（能独立解释）**
- temperature / top_p / 采样原理（Day4 讲得清楚，2.7 分）
- 流式输出 stream=True + delta vs message 的区别
- 用类比消化抽象概念的能力不错

**仍是短板（反复出现，未内化）**
1. **Python 语法生疏**：循环、`with open`、f-string、方法链都要现查 —— 这是拖慢一切的根
2. **`client.chat.completions.create` 调用链反复遗忘**（Day2、Day5 都卡）
3. **messages 结构（数组套字典 / system·user·assistant）反复遗忘**（Day5 又卡）
4. **独立写代码仍困难**：每一步都依赖问 AI，没形成「先想再写」的习惯

**根因判断**：概念是学了，但没转成肌肉记忆；缺少间隔复习，学完即忘。

**对策（已写进下方计划）**
- 每天开头 2 分钟「默写」：不看代码手写出上一天的 API 调用骨架
- 每周末设 1 个「巩固日」，不学新东西，只重写本周所有脚本一遍
- Python 基础语法单独补，不混在 LLM 任务里学

---

## 准备工作（Day 0，建议 30 分钟内完成）

- [ ] 注册 DeepSeek 账号：https://platform.deepseek.com
- [ ] 充值 10 元（够用 1 个月以上）
- [ ] 获取 API Key
- [ ] 复制 `.env.example` 为 `.env`，填入真实 key
- [ ] 安装依赖：`pip install -r requirements.txt`
- [ ] 读完 `CLAUDE.md`（5 分钟）

```bash
cp .env.example .env
# 编辑 .env 填入真实 key
pip install -r requirements.txt
```

---

## 7 天进度表

| Day | 主题 | 文件 | 状态 | 耗时 |
|---|---|---|---|---|
| 1 | Hello World 第一次调用 | `day1_hello.py` | ☐ | √ |
| 2 | messages 多轮对话 | `day2_chat.py` | ☐ |  √ |
| 3 | 流式输出 streaming | `day3_stream.py` | ☐ | √ |
| 4 | 参数实验（temperature 等）| `day4_params.py` | ☐ | √ |
| 5 | AI 翻译工具 | `day5_translate.py` | ☑ | √ (复盘 2.0/3) |
| 6 | 代码注释生成器 | `day6_code_doc.py` | ☐ |  |
| 7 | 复盘 + 综合考核 | `day7_review.md` | ☐ |  |

---

## 每日复盘模板（每天结束花 5 分钟写）

复制下面模板，填入每天的实际内容。

```markdown
### Day N · 2026-MM-DD

**今天学到的最关键 1 件事**：
（一句话）

**最难的点 / 卡了多久**：

**踩的坑**：
1. 
2. 

**Claude Code 帮到我的方式**（具体例子）：

**明天开始前要复习的 1 个概念**：

**今天的 Claude Code 出题得分**：__/3
```

---

## 每日复盘记录

> ⬇️ 每天结束后向下追加，不要修改之前的记录

### Day 1 · 待填

（开始 day 1 时把"### Day N"这行复制下来填）

**今天学习到的最关键 1 件事**：
尝试第一次调用跑动模型

**最难的点 / 卡了多久**：
不知道每一步该写什么代码，传什么参数，每做一步都需要问ai如何做，是否正确，如何填写，一直卡在这里，一直在等待

**踩的坑**：
1. api key只能写在.env的文件中，避免泄露
2. 需要通过 一些方法 os.getenv 去获取变量
3. system与user的先后顺序需要注意
4.system代表用户的指令，需要先设置user的prompt，然后再设置system的prompt，是给模型的设定
5.真正"代表模型说的话"的是 assistant
**今天的 Claude Code 出题得分**：1.8/3
---

## 关键概念笔记（用自己的话写）

> ⚠️ 不要直接复制 AI 的解释。必须用自己的话写一遍。
1.首先调用api，需要先安装依赖（本地linux环境 安装：openai 和 python-dotenv），获取api key，设置环境变量
2.设置message信息，构造message数组
3.调用调用 client.chat.completions.create() 需要正确传递参数
4.402 Insufficient Balance： 服务器是先验身份(key)、再查余额的。你能走到"余额不足(402)"这一步,说明请求成功送达、key 验证通过、messages/create 也都没毛病 —— 否则会先卡在 401 或代码报错,根本到不了 402。所以 402 是"万事俱备、只差钱"的信号。



### Day 2 · 待填

**今天学习到的最关键 1 件事**：
尝试多轮对话以及记住上下文

**最难的点 / 卡了多久**：
1. 语法问题，关于一些方法调用不熟练，比如openAi,os.getenv,对于py语法不熟练，看见条件控制的clear，exit等忘记怎么进行处理，对于client.chat.completions.create的的方法比较陌生，不太明白这一串的具体含义，比如client是之前AI 客户端对象,用来发送请求,接收回复,.chat调用聊天大模型,.completions让模型自动补全回答,.create()用来发起请求,核心动作是告诉模型开始回答,括号内两个必填参数,是模型接口的强制要求
2. 运行中碰到中文的编码问题，虽然不是本次任务解决的主要学习目标，但是影响了测试运行
3. 每次todo，仍然出现之前的问题，对每一个流程在尝试用代码进行表现出来的时候比较困难

**踩的坑**：
1. 输入代码的过程中有些代码凭借着代码补全的功能才能完整输出，比如assistant_reply = response.choices[0].message.content代码补全时这里用的.text，并且我也无法检查出错误，用过运行并且让模型来进行解决的
2. response.choices[0].message.content的完整性，choices是真个答案的大盒子，【0】是推荐答案，message是assistant回复的内容，content才是具体的文本内容
3. todo整个流程的完整性需要保证,之前少了打印出assistant的回复结果

**今天的 Claude Code 出题得分**： 1.5/3
---

## 关键概念笔记（用自己的话写）

> ⚠️ 不要直接复制 AI 的解释。必须用自己的话写一遍。
history 是记录对话历史，每次调用api时，都会把上一次的对话历史一起传给模型，这样模型就能记住上下文，从而进行多轮对话 [先追加 user → 再发请求 → 再追加 assistant]
response 是模型的回复结果，response.choices[0].message.content 就是模型回复的文本内容

### Day 3 · 待填

**今天学习到的最关键 1 件事**：
尝试对话采用流式的方式输出

**最难的点 / 卡了多久**：
1. 理解stream是什么,以及正确的用法,比如stream=True，streaming=False, stream = client.chat.completions.create(model="deepseek-chat", messages=history, stream=True)
2. 学习了py语法中的try 和expect的用法,用来解决当ai在流式回复中中断当前回复,并能储存记忆,把中断的assitant也加入了history中,并且进行下一轮对话


**踩的坑**：
1. 额外了解了模型幻觉的相关知识,当他不知道问题的答案时就会强行补充一个他认为正确答案,比如没有联网的情况下,他无法获取今天的日期,只能获取之前训练时最多的日期，导致模型幻觉


**今天的 Claude Code 出题得分**： 2.1/3
---

## 关键概念笔记（用自己的话写）

> ⚠️ 不要直接复制 AI 的解释。必须用自己的话写一遍。
1. history 是记录对话历史，每次调用api时，都会把上一次的对话历史一起传给模型，这样模型就能记住上下文，从而进行多轮对话 [先追加 user → 再发请求 → 再追加 assistant]
   response 是模型的回复结果，response.choices[0].message.content 就是模型回复的文本内容
2. delta 是数学符号 Δ,意思是"增量 / 变化量"。delta.content = 这一个 chunk 相比上一块,新蹦出来的那一小段。 
    message = 完整的一整条消息。


### Day 4 · 待填

**今天学习到的最关键 1 件事**：
验证temperature 对于模型的影响

**最难的点 / 卡了多久**：
1.循环取出response的内容插入results中
2.关于使用with open()的用法，用来处理文件的读写操作，比如with open('file.txt', 'r') as f: f.read() ,读取文件内容以及json.dump的用法是怎么把字典写成 JSON 字符串，
3.当打印结果时  print(f"{temp}: {outs[0]}\n")  f 是 f-string，用于格式化字符串，在字符串里直接嵌入变量、表达式，让字符串拼接更简单直观，比如f"{temp}: {outs[0]}\n" 就是将temp和outs[0]的内容插入到字符串中，并且换行

**踩的坑**：
1.关于本地venv环境配置问题 
  cd ~/AI_Workstation/week1        # 目录 2026-08-05 由 ai-learning 更名
  rm -rf venv                          # 删掉坏的
  python3 -m venv venv                 # 本地重新建
  source venv/bin/activate             # 激活（成功后提示符会出现 (venv) 前缀）
  pip install -r requirements.txt      # 装 openai + python-dotenv
  python day4_params.py                # 再跑

**今天的 Claude Code 出题得分**： 2.7 / 3
---

## 关键概念笔记（用自己的话写）

> ⚠️ 不要直接复制 AI 的解释。必须用自己的话写一遍。
temperature的底层原理： 
    模型每生成一个token 都会先给词表每一个候选的token打一个分（logtis），然后用一个叫softmax的函数把这些分数变成「加起来等于 100% 的概率」 再按概率抽签决定是哪一个
    temperature =0，永远会选择概率最高的 叫greedy / 贪心解码 （等于0时退化成贪心解码，每一步都选当前概率最高的那个 token，没有抽签的随机性，所以三次走的「路径」完全一样 → 输出一字不差）
    temperature=2 是一颗被磨圆的骰子，每个面机会都差不多，结果完全不可控。
- temperature  : 0-2，控制随机性。0=确定，1=平衡，2=极度发散，
- top_p        : 0-1，核采样阈值。和 temperature 不要同时调
- max_tokens   : 限制单次回复最大长度
- frequency_penalty : -2 到 2，避免重复词
- presence_penalty  : -2 到 2，鼓励引入新话题

top_p： 只在「概率累加到 p 为止」的那批 token 里抽签，即只在前几名token里候选
top_p 和 temperature 在采样时是两道工序叠加——top_p 先把候选 token「砍成一小撮」，temperature 再在这撮里「重新分配概率」。两个一起动，它们会互相纠缠、效果难以预测，不是简单相加。所以不光是「实验上分不清」，是「机制上就乱套」。

max_tokens ：限制模型单次回复的最大长度，单位是 token（一个 token 大约等于 4 个英文字符或 2 个中文字符）


### Day 5 · 待填

**今天学习到的最关键 1 件事**：
做一个中英翻译的工具

**最难的点 / 卡了多久**：
1.对于之前的知识出现了遗忘的现象，message的理解不够深刻，其实就是一个数组，里面存着一个个的字典，字典里面有着system，user，assitant的信息
2.不会写提示词中的JSON格式，这是之前没有接触到的内容 
3.few-shoy 实例也应是json格式
4.约束条件就是一段大白话的语言，并且需要确定性


**踩的坑**：
1.message 内部必须要输入system和user的信息，但是assistant的信息是自动的，不需要手动输入，初始化的时候甚至可以忽略掉system和user的信息，但是当在对话中时，就需要补全message 的user 以及system，system + user → 模型有规矩（system），也有具体任务（user 里的 text），如果在tranlate中传进去user 的text的话，那么模型将永远不知道你要翻译的内容
2.client.chat.completions.create 又忘记了具体表示的意思 可见之前进行复习
3.text = text.encode('utf-8', 'ignore').decode('utf-8') 防御技巧,避免输入中文不显示   
- .encode('utf-8', 'ignore')：把字符串转成 UTF-8 字节，遇到 \udce7 这种编不了的残片 → ignore 直接跳过丢掉
- .decode('utf-8')：再转回干净的字符串
4.
**今天的 Claude Code 出题得分**： 2 / 3
---

## 关键概念笔记（用自己的话写）

> ⚠️ 不要直接复制 AI 的解释。必须用自己的话写一遍。
1.json.loads 是将JSON格式的字符串转换为Python对象，因为response.choices[0].message.content返回的是 json格式的字符串，但是必须要经过解析成json才能识别
2. response_format={"type": "json_object"} —— 强制模型只吐 JSON
3. 调用api的具体流程：　
  client.chat.completions.create(...)   ← ① 拨电话，把请求发出去
          ↓
  response                              ← ② 模型回了个大盒子
          ↓
  response.choices[0].message.content   ← ③ 层层拆开，挖出那张纸条（字符串）
          ↓
  json.loads(content)                   ← ④ 把纸条录入成表格（字典），能取值了

  response_format 是在 ① 那步顺带交代的一个要求，保证 ③ 挖出来的纸条是干净的 JSON，④ 才不会解析失败。
          ↓
  json.loads(content)                   ← ④ 把纸条录入成表格（字典），能取值了

  response_format 是在 ① 那步顺带交代的一个要求，保证 ③ 挖出来的纸条是干净的 JSON，④ 才不会解析失败。

  4.对于输入纯数字出现了报错问题,做了两层修复: 1.修复代码加.get 方法,解决程序不会崩溃的问题,2.修复prompt 提示词约束,修复数字输入的输出还是错的/缺译文的问题
  5. result.get方法当键值不存在时，报错兜底，返回空的字符或者是列表（在方法里可选，比如result['key'] key不存在直接就会报错，但是 result.get('difficult_phrases', []) 则会返回空列表
  
### Day 6 · 待填

**今天学习到的最关键 1 件事**：
今天学习做一个代码文件注释生成器

**最难的点 / 卡了多久**：
1. 当文件过长或者果断是如何设置max_tokens，设置小于或者等于字符长度，那么文件过长如果被截断那么就不能正确理解上下文意思，返回的文件也就是废品文件，如果max_tokens设置过大，则会造成一些资源浪费，所以设置为len（code）*2 简单又安全，即max_tokens =  min(len(code*2),8000) 限制最大长度为8000个字符，这样就不会出现截断的问题，但是这样就限制了模型的回复长度，如果回复长度过长，那么模型就会无法回复，所以需要根据实际情况进行调整
2.对于些prompt比较生疏，思考一下应该是不知道代码注释器功能和作用所以不知从何下手，
3.

**踩的坑**：
1. max_tokens = len(code) * 2(len() 不是 .length,记住)，语法问题
2. with open() 的用法,今天关于打开文件后，不需要使用.close()关闭

**今天的 Claude Code 出题得分**： 1.8 / 3
---

## 关键概念笔记（用自己的话写）
1. 引入pathlib工具，专门处理路径的工具， path（"/demo.py"）,处理路径两种思路 第一是字符串进行手动拼接，在返回至new_path= with_name()
2. 了解了ast.parse(code)可以判断代码合法性，并进行了测试，但是有些符号的改变比如+改为*的等是无法识别出错误的
### messages 数组
messages=[{"role": "system","content": "你是AI机器人，很高兴为您服务。"},{"role":"user","content":"你能介绍一下自己吗？"}]

### token
一个 token 大约等于 4 个英文字符或 2 个中文字符 
不是「字」,是「常见片段」
 这是个经验平均值,不是精确换算。英文里 the(3字母)、ing、tion 这种高频片段一个 token 就装下三四个字母,平均下来1 token ≈ 4 个英文字符。中文信息密度高,一个字常常就是 1 个 token,所以1 token ≈ 1~2 个汉字
类似 模型的乐高积木,常用词一块、生僻词几块;英文约 4 字符一块,中文约 1~2 字一块;钱和上限都按块数算
（待填）

### temperature
temperature 是模型的随机性，控制模型的输出的多样性，值越大，输出越多样化，值越小，输出越单一
temperature  : 0-2，控制随机性。0=确定，1=平衡，2=极度发散

### streaming
streaming 意思流式输出
  stream=True 是告诉模型开始流式输出，streaming=False 是告诉模型停止流式输出，stream = client.chat.completions.create(model="deepseek-chat", messages=history, stream=True) ,也就是让ai的回复出现打印机出现的效果,能够极大提高用户体验
（待填）

### system prompt 的作用
    是提示模型成为什么/遵守什么
---

### useage 三个字段 
usage.prompt_tokens        输入 token 数（你发出去的：system + 历史 + 本轮 user）
usage.completion_tokens    输出 token 数（模型吐回来的）
usage.total_tokens         两者之和

### 重要补充 json dump/dumps 和 load/lods的用法
json.dump()	Python 对象 → 写入文件	                本地 json 文件（你现在用的）
json.dumps()	Python 对象 → 转为json 字符串	        内存字符串，需要自己 write 写入
json.load()	读取 json 文件 → 还原 Python 对象	读文件
json.loads()	json 字符串 → 还原 Python 对象	        读字符串

## 收藏的好 prompt（积累自己的 prompt 库）

| 场景 | Prompt | 效果 |
|---|---|---|
| | | |

---
## Week 1 结束自检（Day 7 填）

- [√] 能解释 messages / role / token / temperature 的作用
- [√] 能不查文档写出一个流式对话脚本
- [√] 理解为什么模型"没有记忆"（无状态）
- [√] 能估算一次调用的 token 数与成本
- [√] 至少做出 2 个自己真的会用的小工具

---

## 后续路线图（结合学者水平 + 2026 AI 现状，实时更新）

> 设计原则（针对你的遗忘问题）：
> 1. **每周第 1 天先复习上周**（默写核心代码骨架，答不出就回炉）
> 2. **每周最后 1 天是「巩固日」**——不学新东西，把本周脚本不看答案重写一遍
> 3. 新主题只在「上周自检全 ☑」后才解锁，宁慢勿夹生
>
> 为什么路线和旧版不同：2026 年的 LLM 应用主流已从「单次问答」转向
> **工具调用（function calling）→ 结构化输出 → Agent 多步自主 → MCP 接外部工具 → RAG 接私有知识**。
> 推理模型（如 DeepSeek-R1 类）也成了标配，会单独安排一天理解「思考 vs 回答」的区别。

### Week 1：API 调用基础 ✅（进行中，收尾 Day 6–7）
messages / 多轮 / 流式 / 参数 / 翻译工具 / 注释生成器 / 综合考核

### Week 0.5：Python 急救（插在 Week 1 和 2 之间，2–3 天）
> 你最大的瓶颈是语法，不补会一直拖后腿。只学和 LLM 开发强相关的：
- 数据结构：list / dict 增删查改、嵌套（对应 messages）
- `with open` 读写文件 + 异常 try/except
- f-string、列表推导式、函数定义与返回值
- 产出：不查文档独立写出一个「读文件 → 调 API → 存 JSON」的小脚本

### Week 2：实用小工具 + 结构化输出深化
- PDF / 长文总结器（练长上下文 + 分段策略）
- 邮件 / 文案起草助手（练 system prompt 工程）
- 强制 JSON 结构化输出（在 Day5 基础上做严格 schema 校验）
- 巩固日：重写本周 3 个脚本

### Week 3：工具调用（Function Calling / Tool Use）
> 2026 年应用层的核心技能。让模型不只「说」，还能「调函数干活」。
- 理解 tool 定义、模型如何决定调用、参数回填
- 做一个「天气查询 / 计算器」让模型自己决定何时调
- 巩固日

### Week 4：RAG 入门（接私有知识）
- embedding 是什么、向量相似度检索的直觉
- 把一份本地文档切块 → 检索 → 喂给模型回答
- 理解「为什么 RAG 能减少幻觉」（呼应 Day3 的幻觉笔记）

### Week 5：Agent + MCP 概念
- 单次调用 → 多步自主循环（plan → act → observe）的区别
- MCP（Model Context Protocol）是什么、为什么它在统一「模型接外部工具」的方式
- 做一个最小 Agent：能自己分几步完成一个任务

### Week 6：工程化 + 上线
- FastAPI 把工具包成 HTTP 接口
- 部署到云服务器（Vultr VPS 已有）
- 成本控制：token 估算、prompt 缓存、模型选型（推理模型 vs 普通模型何时用）

---

> ⚠️ **门槛规则不变**：只有当前 Week 自检全部 ☑，才解锁下一 Week。
> 进度慢不是问题，夹生才是问题。
