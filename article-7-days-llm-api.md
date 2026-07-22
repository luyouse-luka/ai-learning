# 在职转型者的 7 天 LLM API 入门实战：我把 AI 训练成了不肯替我写代码的教练

> 这是一篇失败细节比成功细节多的文章。
> 如果你想看"7 天速通 AI 应用开发"，可以关掉了。我第 7 天的盲写只考了 7.8 分，还是十分制。

---

## 一、先说我是谁，以及一个尴尬的前提

我平时的活是前端建站，WordPress、Shopify、把 Figma 稿还原成页面。2026 年了，这活越来越不值钱，我想往 AI 应用这边挪一挪。

尴尬的前提是：**我 Python 很烂。**

不是谦虚。是 `with open()` 要现查、f-string 要现查、`len()` 会写成 `.length` 的那种烂。

我一开始不觉得这是问题——不就是调个 API 吗，几行代码的事。

第 5 天我就知道自己错了。

---

## 二、我做的第一件事：不是写代码，是给 AI 立规矩

这可能是整件事里唯一聪明的决定。

我用 Claude Code 学，但我很清楚一个风险：**它太能干了。** 我说"帮我写个翻译工具"，它 30 秒就给我一个能跑的完整脚本。然后我复制、粘贴、运行成功、心满意足地关掉电脑——**什么都没学到。**

所以我在项目根目录写了一个 `CLAUDE.md`，把它按在教练的位置上：

```markdown
# 教学合约（Coach Mode）

## 角色定位
- 你（Claude Code）= 严格的技术教练 / 面试官
- 我（ly）= 学习者
- 我们之间不是"代写关系"，是"师徒关系"

## 5 条硬规则（不可破坏）

### 规则 1：不主动写完整代码
我说"帮我写 X"时，默认只给函数骨架 + TODO 注释，让我自己填实现。

### 规则 2：报错先讲原因不给修复
我贴报错时，第一轮回复只讲根本原因，不要直接给修复代码。

### 规则 3：先讲原理再讲代码
介绍新概念时，先用 2-3 句白话 + 类比，最后才给代码示例。

### 规则 4：主动出题考我
每天结束时出 3 道题，从易到难，我答完逐题点评。

### 规则 5：不夸我
不说"很棒！""完美！"。想夸我时改成"这个写法可以"，或者直接进入下一步。
```

还加了一节叫「检测我作弊的信号」：

```markdown
- ❌ 让你写完整代码却没说"请直接写"
- ❌ 报错直接问"怎么修"而不是先尝试自己读
- ❌ 连续 2 天没在 README.md 写复盘
- ❌ Tab 接受补全很多但不能解释为什么这样写
- ❌ 每天开头说不出上一天的 API 调用骨架

你应该提醒我，不要纵容。
```

**效果比我想的猛。**

我第 2 天贴了个报错想让它直接修，它回我：

> "等一下，按 CLAUDE.md 规则 2，我先只讲原因。你自己读一遍 traceback，告诉我它指向哪一行。"

我当时是真的有点火。但现在回头看，Week 1 里我真正记住的东西，全是在这种"被卡住"的时刻记住的。

**规则 5 也比看起来重要。** 每天结束它给我打分，分数是这样的：

```
Day1 1.8 → Day2 1.5 → Day3 2.1 → Day4 2.7 → Day5 2.0 → Day6 1.8   （满分 3）
```

你看，不是一路向上的。**第 5 天比第 4 天还低。** 如果它一直夸我"进步很大"，我根本不会发现自己在退步。

---

## 三、Day 1-6：每天一个坑

### Day 1 · 第一次调用

学的东西不多，就是把 key 塞进 `.env`，用 `os.getenv` 读出来。

坑在于——我根本不知道每一步该写什么。我在复盘里是这么写的：

> "不知道每一步该写什么代码，传什么参数，每做一步都需要问 ai 如何做，是否正确，如何填写，一直卡在这里，一直在等待。"

这句话我一个字都没改。这是第一天最真实的状态：**不是不会某个语法，是完全不知道从哪下手。**

那天有个意外收获，是我第一次觉得"报错也是信息"：

> **402 Insufficient Balance**：服务器是先验身份（key）、再查余额的。你能走到"余额不足（402）"这一步，说明请求成功送达、key 验证通过、messages/create 也都没毛病——否则会先卡在 401 或代码报错，根本到不了 402。所以 402 是"万事俱备、只差钱"的信号。

充了 10 块钱，到今天还没用完。

### Day 2 · 多轮对话，和那个我抄错的链条

这天学 `messages`。核心就一句话：**模型是没有记忆的，每次都得把整段历史重发一遍。**

```python
history = [{"role": "system", "content": "You are a helpful assistant."}]
# 先追加 user → 再发请求 → 再追加 assistant
history.append({"role": "user", "content": user_input})
```

这天的坑很丢人，我照实写在复盘里了：

> "输入代码的过程中有些代码凭借着代码补全的功能才能完整输出，比如 `assistant_reply = response.choices[0].message.content`，代码补全时这里用的 `.text`，并且我也无法检查出错误，用过运行并且让模型来进行解决的。"

**我被自动补全带着写错了，而且我自己看不出来。**

后来我把这条链拆开重新理解了一遍：

```
response.choices[0].message.content
   ↑        ↑     ↑     ↑       ↑
  大盒子   答案列表  第一个  这条消息  实际的文字
```

`choices` 是整个答案的大盒子，`[0]` 是推荐答案，`message` 是 assistant 这条消息，`content` 才是具体文本。

**这个链条我后来还是忘了两次。** 第 5 天忘一次，第 7 天考核盲写又掉了 `.message` 那一层。

### Day 3 · 流式输出，还有模型幻觉

流式就是打字机效果。开关是 `stream=True`。

```python
stream = client.chat.completions.create(
    model="deepseek-chat", messages=history, stream=True
)
for chunk in stream:
    delta = chunk.choices[0].delta.content
    if delta is not None:
        print(delta, end="", flush=True)
```

`delta` 这个词当时困扰了我一下，后来想通了：**delta 是数学里的 Δ，增量。** `delta.content` = 这一块相比上一块新蹦出来的那一小段。而 `message` 是完整的一整条。所以非流式拿 `message`，流式拿 `delta`。

这天的意外收获是**模型幻觉**。我问它今天星期几，它一本正经地编了一个。

> "当他不知道问题的答案时就会强行补充一个他认为正确答案，比如没有联网的情况下，他无法获取今天的日期，只能获取之前训练时最多的日期。"

这个认知在后面 Week 4 学 RAG 的时候会直接接上——RAG 存在的意义就是治这个病。

### Day 4 · temperature，唯一一次考到 2.7

这天是我 6 天里分数最高的一天，因为我真的搞懂了原理，而不是背了个"0 是确定，1 是平衡"。

模型每生成一个 token，会先给词表里每个候选打分（logits），再用 softmax 把分数变成加起来等于 100% 的概率，然后**按概率抽签**。

- `temperature = 0`：永远选概率最高的那个，退化成贪心解码。没有抽签，所以跑三次输出一字不差。
- `temperature = 2`：一颗被磨圆的骰子，每个面机会都差不多，结果完全不可控。

`top_p` 是另一道工序：只在"概率累加到 p 为止"的那批 token 里抽签，等于先把候选砍成一小撮。

**为什么两个不要一起调？** 不是"实验上分不清"，是**机制上就乱套**——top_p 先砍候选，temperature 再在这撮里重新分配概率，两个一起动会互相纠缠。

坑倒是个环境坑，venv 建坏了，重来一遍：

```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Day 5 · 第一次做"产品"，也是第一次崩

这天做中英翻译工具。代码几乎和 Day 1 一样，难的不是代码，是 **prompt**。

要让输出结构化，得开 JSON Mode：

```python
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    response_format={"type": "json_object"}   # 强制只吐 JSON
)
result = json.loads(response.choices[0].message.content)
```

（注意：开了这个，system prompt 里**必须出现 "json" 字样**，否则报错。）

system prompt 我写了角色 + 任务 + 输出格式 + few-shot + 约束五段。真正救命的是最后的约束条件，因为我测到了一个边界 case：**输入纯数字 "12345" 会崩。**

修了两层：

1. **代码层**：`result.get('difficult_phrases', [])` —— 用 `.get()` 兜底。`result['key']` 键不存在会直接报错，`.get()` 会返回默认值。
2. **prompt 层**：约束里加一条"数字时也必须返回 translation 字段，让输出结构永远一致"。

**只修代码不够，输出还是错的；只修 prompt 也不够，程序还是会崩。** 这是我第一次意识到 LLM 应用是"代码 + 提示词"两层都要防。

但这天分数掉到 2.0。因为：

> "对于之前的知识出现了遗忘的现象，message 的理解不够深刻，其实就是一个数组，里面存着一个个的字典。"
>
> "`client.chat.completions.create` 又忘记了具体表示的意思。"

**Day 2 学的东西，Day 5 忘了。**

### Day 6 · 长文本，和 max_tokens 的取舍

做代码注释生成器：读一个 `.py` 文件 → 让模型加注释 → 存成新文件。

新问题是长上下文。`max_tokens` 设小了输出被截断，返回一个残废文件；设大了浪费资源。我最后用的是：

```python
max_tokens = min(len(code) * 2, 8000)
```

加注释后的代码一定比原代码长，所以 `* 2`；但不能无限大，所以拿 8000 封顶。

这天还捡到一个很实用的东西——**用 `ast.parse()` 验证 AI 有没有把代码改坏**：

```python
def validate(code: str) -> bool:
    try:
        ast.parse(code)
        return True
    except SyntaxError as e:
        print(f"❌ AI 输出的代码语法错误: {e}")
        return False
```

AI 输出的代码不能盲目保存。语法过不了就拒绝写文件。

（但我也测出了它的边界：`+` 被改成 `*` 这种**语法合法、语义错了**的改动，`ast.parse` 抓不出来。）

坑还是语法：`len()` 不是 `.length`。以及 `with open()` 用完不需要 `.close()`。

---

## 四、中途急刹车：我插了一个 "Week 0.5"

Day 6 结束，分数 1.8，比第一天还低。

教练给我做了一次评估，结论很不客气：

> **根因判断**：概念是学了，但没转成肌肉记忆。
>
> **仍是短板**：
> 1. Python 语法生疏：循环、`with open`、f-string、方法链都要现查 —— **这是拖慢一切的根**
> 2. `client.chat.completions.create` 调用链反复遗忘
> 3. messages 结构反复遗忘
> 4. **独立写代码仍困难**：每一步都依赖问 AI，没形成「先想再写」的习惯

然后它建议我停下来，别往 Week 2 冲，插一个 **"Week 0.5：Python 急救"**。

只学和 LLM 开发强相关的那一小撮：

- `list` / `dict` 的增删查改和嵌套（**这就是 messages 的真身**）
- `with open` 读写 + `try/except`
- f-string、函数定义与返回值

产出是一个结业脚本：不查文档，独立写出「读文件 → 调 API → 存 JSON」。

**这三天是整个 Week 1 里性价比最高的三天。**

因为 `messages` 那个反复遗忘的老大难，在我把 `list` 套 `dict` 练熟之后，**突然就不忘了**。它一直不是"API 知识点"，它就是个嵌套数据结构，我以前忘它是因为我 Python 数据结构本来就不熟。

**如果你也是零基础转型，别学我拖到第 6 天才补。**

---

## 五、Day 7 上半场：10 道题考了 8 分

回来做综合考核。规则是我自己定的：10 道题，从概念到代码，难度递增，不给提示，答完给总分 + 最大盲点。

结果 **8/10**（过线是 7）。

对比这个会话刚开始时的默写只有 1.5 分 —— **概念题基本全通了，messages 结构彻底焊死。**

丢的 2 分很有代表性：

| 题 | 错在哪 |
|---|---|
| Q1 | 问 `content` 装什么，我说成了"定位描述"——其实它就是**这条消息实际说的话**，别想复杂 |
| Q5 | system prompt 的措辞说错 |
| Q7 | 算 token 成本，把 **200 看成了 500** |
| Q9 | 盲写调用链，漏了 `.message` 那一层；`from X import Y` 写反了 |

第三个盲点它单独拎出来说了：

> **拼写 + 看题精度**：except→expect、assistant→assitant、completions→compeletions、200→500。
> 真代码里全是 SyntaxError / NameError / API 拒绝，是效率的隐形杀手。

这条我原来觉得是小毛病。后面证明它一点都不小。

---

## 六、Day 7 下半场：盲写挑战，7.8 分

这是整个 Week 1 唯一真正的门槛。

**关掉所有编辑器、关掉所有文档、禁用 Tab 补全**，写一个流式对话脚本：

- 多轮对话有记忆
- `clear` 清空历史
- `tokens` 显示总消耗
- `exit` 优雅退出

限时 30 分钟，写完才允许第一次运行。

我写了 39 行。**第一次跑就跑起来了。**

然后教练读了一遍代码，把我按在地上摩擦。

### Bug 1：跑得通，但行为是错的

```python
elif user_input == "clear":
    history = [{"role": "system", "content": "You are a helpful assistant."}]
    # ← 这里少了 continue
history.append({"role": "user", "content": user_input})
```

我清空了历史，**然后代码继续往下走**，把 `"clear"` 这个字符串当成用户提问发给了 AI。

我的 `exit` 有 `break`，空输入有 `continue`，**只有 `clear` 没有出口**。

> 跑通不会报错的 bug 最危险，就是这一类。

### Bug 2：`tokens` 命令我根本没写

三个命令我交了两个。而且我原本的思路是错的——我打算"判断字符是中文还是英文，然后自己估算 token"。

**token 不是估出来的。** 中文一个字可能 1 个 token，英文 `unbelievable` 可能被切成 4 个。自己按字符数算误差能到 30%，而且**计费是按服务端实际用量走的，不是按你估的走**。

正确做法是问服务端要。非流式的响应里有现成的 `usage` 字段，但**流式默认不给**。得开一个参数：

```python
stream = client.chat.completions.create(
    model="deepseek-chat",
    messages=history,
    stream=True,
    stream_options={"include_usage": True}   # ← 就是它
)
```

我第一次是这么写的：

```python
..., stream=True, include_usage=True)
# TypeError: Completions.create() got an unexpected keyword argument 'include_usage'
```

**`stream_options` 不是布尔值，它是个容器**，`include_usage` 是装在容器里的那个布尔。

这个结构其实和 `messages` 完全同构：`messages` 是 list 装 dict，`stream_options` 是 dict 装键值。我学 messages 时懂了，换个参数名又不认识了。

开了之后，流的最后会多来一个 chunk 带着用量：

```python
if chunk.usage is not None:
    usage_info += chunk.usage.total_tokens
```

顺带记一下这三个数：

```
prompt_tokens=22      ← 你发进去的（整个 messages 的总量）
completion_tokens=14  ← 模型吐出来的
total_tokens=36       ← 合计
```

**`prompt_tokens` 是整个 messages 的总量，不是你最后那句话。** 多轮聊到第 20 轮，光输入就可能几千 token。所以 `clear` 命令不只是清屏，**它是个省钱按钮**。

（DeepSeek 还多给了 `prompt_cache_hit_tokens` —— 命中缓存的输入 token 便宜一个数量级。多轮对话里前面的历史是固定前缀，第二轮开始就会命中，所以重发历史没有想象中那么贵。）

### Bug 3：累加变量放错了层

```python
while True:
    ...
    usage_info = 0    # ← 每轮开头重置成 0
```

放在循环里面，每轮归零。它记录的是"本轮消耗"，不是"从启动到现在的累计"。

判断方法就一句话：**问自己"我要它活多久？"** 要活到整个会话结束，它就不能在每轮开头被重新赋值。

### Bug 4：`try` 包错了地方，等于没包

我原来的 `try` 只包住了流式循环，**API 调用那一行在 try 外面**。

```python
stream = client.chat.completions.create(...)   # ← 在 try 外面裸奔
try:
    for chunk in stream:
        ...
except KeyboardInterrupt:
    ...
```

后果：网络断了、key 过期了、余额没了 —— **脚本当场崩溃退出，聊了 20 轮的历史全丢**。

而且我的 `except` 只接 `KeyboardInterrupt`，那是用户按 Ctrl+C，压根不是 API 错误。

后来我改成两层，各管各的：

```python
try:                                    # 外层：包住整个 while
    while True:
        user_input = input("you: ").strip()
        ...
        try:                            # 内层：只包"可能失败的那几行"
            stream = client.chat.completions.create(...)
            for chunk in stream:
                ...
        except KeyboardInterrupt:       # Ctrl+C 打断输出 → 停这一轮
            print("Stream interrupted by user.")
            history.pop()
            continue
        except APIError as e:           # API 出错 → 提示一句，接着聊
            print(f"\n[API 出错] {e}")
            history.pop()
            continue
except KeyboardInterrupt:               # 在 input() 等待时 Ctrl+C → 优雅退出
    print("Chat session ended.")
```

有两个点我记了很久：

**第一，`try` 只保护它括起来的那几行，外面发生什么它一概不管。**

我一开始那个 `except KeyboardInterrupt` 好像"从来没生效过"——因为它只在 AI 正在吐字的那一两秒内有效，其余时间全裸奔。我在 `input()` 等待时按 Ctrl+C，异常在 try 管辖区之外抛出，没人接，程序直接崩。

**第二，`as e` 不是可选的装饰。**

```python
except APIError:        # 只能知道"出错了"
except APIError as e:   # 能知道是 401 key 无效、429 太频繁、还是连接超时
```

`as e` 是把飞过来的错误对象**接住并存进变量**。没有它，你知道出事了但不知道出了什么事。

（还有个小知识：`APIError` 是 `openai` 这个 **Python 库**提供的类，跟你连的是哪家服务商没关系。它是一堆具体错误的父类，接父类就能接住所有子类。我一开始还以为是"DeepSeek 没有这个东西"。)

### Bug 5：中断之后，我的对话历史被污染了

这个最隐蔽。

场景：我问"介绍一下 Python"，AI 刚吐了几个字，我按 Ctrl+C。

按我原来的代码走一遍：user 消息**已经进 history 了**，但 assistant 那条因为 `continue` 被跳过了。

结果 history 里留下一条**没有回复的孤儿 user 消息**。下一轮再 append，就变成两条连着的 user。

它长这样：

```
system    : You are a helpful assistant.
user      : 介绍一下 Python        ← 孤儿，没有对应的 assistant
user      : what is your name      ← 又一条 user
```

**这不是理论上的问题，它当场就咬了我。** 我下一句问的是 "what your name"，AI 回我：

> You asked two things — let me answer both:
> 1. **My name**: I'm DeepSeek...
> 2. **Introduction to Python**: ...

**它把我打断的那个问题又答了一遍。** 因为在它眼里，那条 user 消息还没被回应过。

怎么修？两个选项：

- **A：撤回那条 user** —— history 回到干净状态。代价是内容丢了。
- **B：把半截内容存成 assistant** —— 内容保住了。但 history 里埋着一条被掐断的 AI 回复，下一轮模型可能试图接着说下去。

我一开始觉得两个都不好，因为 **Ctrl+C 这个信号本身是有歧义的** —— 我可能是"这答案太长不想看了"，也可能是"我输错了想重来"。程序读不出我的意图。

教练给了个决策原则，我记下来了：

> **两个方案都有缺陷时，选那个"出错时更容易发现、更容易恢复"的。**
>
> A 丢内容，但代价是**看得见的**，而且 history 保持严格的 user/assistant 交替——这是个**不变量**，守住它，后面所有轮次都安全。
> B 保内容，但埋下的问题是**看不见的**，它只是让模型行为变怪，你还找不到原因。
>
> **宁可丢内容，不可让状态变脏。脏状态的 bug 是最难查的。**

选 A。就一行 `history.pop()`。

---

## 七、最贵的一个坑：我把因果关系搞反了

这个单独拎出来讲，因为它跟 API 一点关系都没有，但它是这一周我学到的最重要的东西。

盲写改到一半，程序开始报一个我看不懂的错：

```
UnicodeEncodeError: 'utf-8' codec can't encode characters
in position 141-142: surrogates not allowed
```

我观察了几次，得出一个结论：**"输入中文的时候中间加空格就会报错。"**

因为我崩掉的那次输入是 `今天星期 几`，而前一次成功的输入是纯英文。

教练把我这个结论直接否了，用的是我自己贴上去的报错原文：

```
can't encode character '\udce5' in position 1667
```

`\udc` 开头的这一段（U+DC80–U+DCFF）是 Python `surrogateescape` 机制的"赃物寄存处"：它把一个无法解码的**原始字节 0xNN 藏成 `\udcNN`**。

所以 `\udce5` = **原始字节 `0xE5`**。而 `0xE5` 是汉字 UTF-8 三字节序列的**首字节**。

**空格是 `0x20`，纯 ASCII，永远不可能编码失败。**

真凶是：我 Ctrl+C 打断了正在输出中文的流，终端输入通道里**残留了半个汉字的字节**，下一次 `input()` 把它读进来，Python 用兜底机制藏成了 `\udce5`，一路藏到发请求时才炸。

然后它指出我推理链条上的洞：

| 场次 | 有没有打断中文流 | 输入有没有空格 | 结果 |
|---|---|---|---|
| 上次 | **有** | 有 | 炸 |
| 这次 | **无** | 无 | 不炸 |

**两个变量同时变了。** 我只能得出"这两个因素至少有一个相关"，却直接归因给了空格。

证伪它只要一行命令：

```bash
python3 -c "print('今天星期 几'.encode('utf-8'))"
```

带空格的中文，直接编码，**它不会报错**。如果"中文加空格"真的会炸，这行就该炸。

我盯着这个错误猜了两轮，而验证只要 30 秒。

**这一周我学到的最贵的一课不是 API 怎么调，是：先看数据，再下结论；一次只动一个变量。**

（顺带，这个坑最后是这么解决的——一道守入口，一道守存储：

```python
sys.stdin.reconfigure(errors="replace")   # 入口：坏字节当场变成 �，不再偷偷藏起来

def sanitize(s: str) -> str:              # 存储：进 history 前再洗一遍
    return s.encode("utf-8", "surrogateescape").decode("utf-8", "replace")
```

第二个函数会先把 `\udce5` 还原成原始字节，再用 UTF-8 重读一次 —— 拼得成汉字就还原成汉字，拼不成才换 `�`。**尽量救回来，救不回来也不崩。**）

---

## 八、几个不写代码的收获

这些我觉得比语法值钱：

**1. 别猜，`print(repr())`。**

不知道响应里有什么，就把整个对象打印出来。比翻文档快，而且看到的是**你这个 API 真实返回的东西**，不是文档里的理想情况。

我实测的时候还发现：DeepSeek 把 usage 挂在最后一个正常 chunk 上，而不是像 OpenAI 官方文档说的那样另发一个空 `choices` 的 chunk。**"OpenAI 兼容"不等于"行为完全一致"** —— 文档、教程、包括教你的那个 AI，都可能和你手上这个 API 对不上。

**2. 两段式 traceback，修第二段。**

看到 `During handling of the above exception, another exception occurred`，第一段往往是你已经知道的那个（比如我故意改错 key 触发的 401），**第二段才是你代码本身的 bug**。

**3. `NameError` 永远只有一个意思：你用了一个没导入 / 没定义的名字。**

我在 `except APIError` 上栽了一次，因为我只加了 except 分支，忘了改 import 那行。

**4. 复制一个分支之后，记得改函数体。**

我的 `tokens` 命令一度是这样的：

```python
elif user_input == "tokens":
    history = [{"role": "system", "content": "..."}]   # ← 这是 clear 的活
    continue
```

我复制了 `clear` 分支，忘了改里面。输入 `tokens` 不显示 token，而是**把我的对话历史清空了**。

---

## 九、诚实的自评

复盘表里有一栏叫「我是否真的在"学"，还是在"让 Claude Code 替我学"？」

我的回答：

> - 有多少代码是我关掉编辑器、凭记忆能重写出来的？—— **60% 左右**
> - 我能不能不看任何参考、独立完成一个"AI 词典"工具？—— **较为困难。虽然了解流程和原因，但像 system prompt 的设计以及打印输出，可能需要借助工具或者以前写的代码。**

一周最大的三个踩坑，我写的是：

> 1. 遇到难得仍会退缩放弃，需要冷静下来，重新思考
> 2. 经常会使用代码补全得功能
> 3. （空着）

最重要的收获，第一条是：

> **每天都要保持学习，间隔了一段时间之后再次重启十分困难。**

这条是血泪。我中间断过几天，回来之后连 `messages` 长什么样都想不起来了。

盲写的两个分数我也一起放这儿，因为它们量的是两种不同的能力：

| | 分数 | 量的是什么 |
|---|---|---|
| **盲写原始成绩** | **7.8 / 10** | 关掉编辑器、不看文档，一次跑通的真实水位 |
| **修复后成绩** | 10 / 10 | 有人指出问题后能不能改对 |

**7.8 才是我的真实水平。** 后面那个 10 分是另一回事。

唯一让我有点底气的是：**这次拼写零扣分**。`completions`、`assistant`、`except`、`APIError`，包括 `from openai import OpenAI, APIError` 的方向，全对。这是我上次考核的三大盲点之一。

---

## 十、如果你也想这么学

给和我情况类似的人几条建议：

1. **先给 AI 立规矩，再开始学。** 一个 `CLAUDE.md` 教学合约，五条硬规则，成本 10 分钟，收益是整个课程。不然你会得到一堆能跑的代码和一个什么都没学会的自己。

2. **Python 太烂就先停下来补。** 别觉得"边做边学"能糊过去。我第 6 天才补，如果第 1 天补，前面 5 天的效率至少翻倍。补的时候只学和任务强相关的那一小撮（`list`/`dict`/`with open`/`try`），不要去啃整本教程。

3. **每天写复盘，写你不体面的地方。** 这篇文章里最有价值的段落，全是我当时觉得很丢人、但照实记下来的东西。"我被自动补全带着写错了而且看不出来"这种句子，三个月后是能救你的。

4. **一定要做一次盲写。** 关掉编辑器、关掉补全、关掉文档，从零写一遍。这是唯一能测出你真实水位的方式。跟着教程敲一遍代码然后觉得"我会了"，是这行最大的自欺。

5. **别追速度。** 我这个"7 天"实际跨了快两个月，中间还插了 3 天 Python 急救。门槛规则是：**上一周自检没全过，不许解锁下一周。进度慢不是问题，夹生才是问题。**

---

## 十一、下一步

Week 1 到此封版。接下来的路线：

- **Week 2**：实用工具 + 结构化输出深化（PDF 长文总结、邮件助手、严格 JSON schema 校验）
- **Week 3**：工具调用 Function Calling
- **Week 4**：RAG 入门
- **Week 5**：Agent + MCP
- **Week 6**：FastAPI 工程化 + 上线

现在我至少能稳定拿到 `usage` 了，Week 2 一开始就要用它做成本控制。

---

## 仓库

所有代码、7 天的复盘原文、那份教学合约 `CLAUDE.md`，都在这里：

**https://github.com/luyouse-luka/ai-learning**

里面包括：

- `week1/CLAUDE.md` —— 教学合约，可以直接抄去用
- `week1/day1~day6_*.py` —— 每天的脚本（保留了 TODO 注释和我填的实现）
- `week1/day7_blind.py` —— 盲写挑战的最终版
- `week1/README.md` —— 7 天完整复盘原文（比这篇文章更啰嗦、更真实）
- `week1/day7_review.md` —— 考核记录和自评

如果你也在转型路上，欢迎交流。有错的地方欢迎指出——我这个水平，错的地方大概率不少。
