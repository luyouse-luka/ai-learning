"""
Week 4 Day 2 —— Prompt 技法实战（Role / Few-shot / Negative）

这个文件只放 prompt 和对照实验，不碰 FastAPI。
改完并验过之后，main.py 里的 SYSTEM_PROMPT 才换成从这里 import。
（先验后接线 —— 没验就接，出了问题分不清是 prompt 的锅还是接线的锅）
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = "deepseek-v4-flash"
MAX_OUTPUT_TOKENS = 1500          # ⚠️ 小了会被 reasoning token 吃光，返回空字符串（Week 3 Day 6 栽过两小时）
SAMPLE = Path(__file__).parent.parent / "attention_extracted.txt"   # 固定输入 = 控制变量


# ===================================================================
# V1 —— 你现在线上跑的这版，原样搬过来当基线，一个字都别改
# ===================================================================
SYSTEM_PROMPT_V1 = """
    1. 你的任务是对文本进行总结，不能只是摘抄原文，要提炼出核心思想
    2. 总结的文本最多不要超过400字,需要用中文进行回复，总结回复的文本需要符合中文语言逻辑，通顺无语病
    3. 总结文本根据逻辑语义进行分段，并首行缩进，方便阅读
"""


# ===================================================================
# V2 —— 今天你要写的。五段结构，三个技法各用一次
# ===================================================================
# TODO【1】Role —— 补上 V1 完全没有的那一段
#     判据：读完这句，模型知道"我是谁、我平时怎么干活"吗？
#     ⚠️ 选职业，别选头衔（"资深科技编辑" ✅ / "诺贝尔奖得主" ❌ —— 后者只会让它更爱下断言）
#
# TODO【2】Task —— 把 V1 第 1 条劈开：哪半句是"做什么"，哪半句是"不许怎么做"
#     劈完之后 Task 这段应该只剩一件事
#
# TODO【3】Constraint —— 收走 V1 第 1 条劈出来的那半句 + 第 2 条
#     ⚠️ 能改正向的一律改正向（"不要超过 400 字" → 给个区间）
#     ⚠️ 留下来当负向的，你要能说出"它的正向版写不出来"这个理由
#
# TODO【4】Example —— V1 完全没有的第二段。给 1-2 个 输入→输出 的样例
#     ⚠️ 最该给示例的是 V1 第 3 条那个要求 —— 昨天你自己指出它有歧义，
#        歧义就是"描述"要过理解那一关时出的错，示例把那一关删掉
#     ⚠️ 示例的长度/段数会被一起学走。你只给一个三段的例子，它就倾向永远输出三段
#
# TODO【5】Format —— 输出长什么样。和 Constraint 的分界：
#     Constraint 管"内容边界"，Format 管"排版形状"
SYSTEM_PROMPT_V2 = """
role: 你是资深语言模型训练师，专门训练模型如何总结文本。请严格按照以下要求进行总结：
task: 对文本进行总结，提炼核心思想
constraint: 总结文本字数需控制在400字以内，需要用中文进行回复，需要概括归纳， 而不是只摘抄原文。
format: 按逻辑语义分段，段与段之间空一行；每一个段落（包括第一段）都以两个全角空格「　　」开始；篇幅与段数以上方 constraint 为准，不参照示例的长度。
<example>
输入：随着人工智能技术的快速发展，越来越多的企业开始将 AI 应用到日常工作中。从最初的简单文本生成，到现在的代码编写、数据分析、客服服务以及内容创作，AI 正在逐渐改变传统的工作方式。对于个人而言，AI 可以帮助提高效率，例如程序员可以利用 AI 快速生成代码框架，市场人员可以让 AI 分析用户数据，设计人员也可以利用 AI 快速产生不同的设计方案。

不过，AI 带来便利的同时，也产生了一些新的问题。首先，AI 生成的内容并不一定完全正确，如果使用者缺乏判断能力，就可能把错误的信息当成事实。其次，一些重复性较强的工作可能会被 AI 自动化，从而导致部分岗位的工作内容发生变化。除此之外，企业在使用 AI 时还需要考虑数据隐私、安全以及知识产权等问题。

因此，未来真正重要的并不只是“会不会使用 AI”，而是能否正确地与 AI 协作。个人需要学习如何提出清晰的问题、判断 AI 输出的质量，并结合自己的专业知识进行修改和决策。企业则需要建立相应的管理制度，在提高效率的同时控制数据、安全和合规风险。可以预见，AI 更可能成为人的工作伙伴，而不是简单地完全取代人类。未来的竞争力，也可能越来越取决于一个人利用 AI 解决实际问题的能力。
输出：
　　AI 正在改变工作方式，在代码编写、数据分析与内容创作等环节显著提升个人与企业的效率。

　　与此同时，输出准确性、岗位结构变化与数据隐私等风险同步出现，因此关键不在于是否使用 AI，而在于能否判断其输出质量并建立相应的管理机制。
</example>
"""


def summarize(system_prompt: str, text: str) -> str:
    """同一段文本 + 不同 system prompt，其它参数全一样。"""
    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    # TODO【6】照 week1 的写法调一次，返回正式回答的字符串
    #     ⚠️ 只改 system_prompt 这一个变量，temperature / max_tokens 两版必须一致，
    #        否则跑出差异你说不清是 prompt 的功劳还是参数的功劳
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        
    )
    return response.choices[0].message.content.strip()


def measure(label: str, s: str) -> None:
    """把能机械判定的量打出来 —— 这是判据的【实得值】，不靠肉眼看。"""
    paras = [p for p in s.split("\n") if p.strip()]
    print(f"\n--- {label} ---")
    print(f"字数      {len(s)}")
    print(f"段数      {len(paras)}")
    print(f"首段开头  {paras[0][:4]!r}" if paras else "首段开头  (空)")   # repr 才看得见空格是全角还是半角
    print(f"术语保留  {'multi-head attention' in s.lower()}")


def compare() -> None:
    """跑 V1 / V2 各一次，落盘，然后按判据逐条比。"""
    text = SAMPLE.read_text(encoding="utf-8")
    out = Path(__file__).parent.parent.parent / "week4"

    # 【7】落盘 —— 不是为了好看，是为了明天还能翻出来，以及被质疑时有原件
    #     每花一次钱就立刻落一次盘：攒到最后一起写，后面任何一步崩掉，前面的钱全白花
    summary_v1 = summarize(SYSTEM_PROMPT_V1, text)
    (out / "day2_v1.txt").write_text(summary_v1, encoding="utf-8")

    summary_v2 = summarize(SYSTEM_PROMPT_V2, text)
    (out / "day2_v2.txt").write_text(summary_v2, encoding="utf-8")

    measure("V1", summary_v1)
    measure("V2", summary_v2)

    # TODO【8】判据表 —— 【实得值】measure() 已经替你量出来了，
    #     但【期望值】必须你自己填，而且要在**跑之前**填。
    #     跑完再填期望 = 照着结果编期望，判据恒绿，等于没判（你栽过的那种自洽）。
    #
    #     ⚠️ 每格必须是能当场判对错的具体值。"读起来更顺了" 不算。
    #
    #     | 判据         | V1 期望 | V2 期望 |
    #     |--------------|---------|---------|
    #     | 字数         |小于四百|四百以内|
    #     | 段数         |分段|分段|
    #     | 首段开头     |缩进|缩进|   ← 你昨天选的是路 A 还是路 B，这格的期望就不同
    #     | 术语保留     |         |         |
    #     | (你自己加一条)|         |         |
    #
    #     填完把这张表连同终端实得值抄进 week4/README.md 的 Day 2 节。


if __name__ == "__main__":
    compare()
