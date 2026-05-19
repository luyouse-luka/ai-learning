"""
Day 5 · AI 翻译工具（第一次"做产品"）
==========================================

【今日目标】
不再是 demo，而是做一个你自己真的会用的小工具。
功能：输入一句中文 → 输出英文翻译 + 解释翻译难点。

【为什么这个项目重要】
你第一次面对的不是"代码问题"，而是"产品问题"：
- system prompt 怎么写才能让输出稳定？
- 输出怎么结构化，便于程序处理（不只是给人看）？
- 边界 case 怎么处理（输入英文怎么办？输入超长怎么办？）

【今日核心训练】
Prompt 工程，而不是 Python 代码。
代码本身很简单（几乎和 day1 一样），关键是 system prompt 怎么设计。

【启动 Claude Code 后，对它说】

    开始 day 5
    "我要做翻译工具，但要解释难点。
     请先帮我设计 system prompt（不要写 Python 代码），重点告诉我：
     1) 怎么让输出结构化（翻译 + 难点解释分开）
     2) 用什么手段让它真正"知道难点在哪"（few-shot? CoT?）
     讨论清楚后我自己写代码。"

【推荐的输出格式（JSON）】
{
    "translation": "...",
    "difficult_phrases": [
        {"chinese": "落地", "english": "implement", "why": "字面意 vs 商业用法"}
    ],
    "alternative_translations": ["...", "..."]
}

【启动 JSON Mode（DeepSeek 支持）】
传 response_format={"type": "json_object"} 给 API
但 system prompt 里必须出现 "json" 字样，否则报错

【边界 case 思考题（开工前先想 5 分钟）】
1. 用户输入英文怎么办？应该反向翻译还是报错？
2. 用户输入超长（5000 字）怎么办？
3. 用户输入纯数字 "12345" 怎么办？
4. 网络超时怎么办？
5. AI 返回非法 JSON 怎么办？

==========================================
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


# TODO 1：精心设计的 system prompt
# 这是今天最核心的产出。多迭代几次。
# 建议结构：角色 + 任务 + 输出格式 + few-shot 示例 + 约束
SYSTEM_PROMPT = """
你是一个 ...

# 你的代码（多写、多改）
""".strip()


def translate(client: OpenAI, text: str) -> dict:
    """
    TODO 2：调用 API，返回解析后的 dict
    要点：
    1) 用 response_format JSON Mode
    2) try/except 处理 JSON 解析失败
    3) 失败时打印原始返回，便于调试
    """
    # ← 你的代码


def pretty_print(result: dict):
    """
    TODO 3：把 dict 漂亮打印（不是 json.dumps，是人看的）
    例如：
        译文：...
        ---
        难点 1：xx → yy
            原因：...
        难点 2：...
    """
    # ← 你的代码


def main():
    """
    TODO 4：初始化 + 命令行循环
    支持用户连续输入，输入 exit 退出
    """
    client = None  # ← 你的代码

    while True:
        text = input("中文输入: ").strip()
        if text == "exit":
            break
        if not text:
            continue
        result = translate(client, text)
        if result:
            pretty_print(result)


if __name__ == "__main__":
    main()


# ============================================
# 完成检验：
# 1. 至少 5 句测试用例，包括：
#    - 普通日常句
#    - 专业术语（如"落地实施"）
#    - 文化梗（如"内卷"）
#    - 极短输入（一个字）
#    - 极长输入（200 字）
# 2. 让 Claude Code 扮演 PM 挑刺：
#    "你扮演产品经理，找出我这个翻译工具的 5 个 bug 或体验问题"
# ============================================
