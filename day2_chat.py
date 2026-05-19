"""
Day 2 · messages 数组与多轮对话
==========================================

【今日目标】
做一个命令行多轮对话脚本，能记住"上下文"。
体感上像 mini 版的 ChatGPT。

【核心认知（必须先想清楚再写代码）】
LLM 本身是「无状态」的。它不记得你上一句说了什么。
"记忆"完全是你这边的责任——
你每次都要把整个对话历史塞进 messages 里发过去。

也就是说：
    第 1 轮：messages = [system, user1]
    第 2 轮：messages = [system, user1, assistant1, user2]
    第 3 轮：messages = [system, user1, assistant1, user2, assistant2, user3]
    ...

随着对话变长，每轮都要发更多 token，越来越贵。
这是后面要解决的问题（截断 / 总结 / RAG）。

【启动 Claude Code 后，对它说】

    开始 day 2

【需要实现的功能】
1. 一个 while 循环，反复读用户输入
2. 用户输入 "exit" 时退出
3. 用户输入 "clear" 时清空历史（保留 system）
4. 每轮把 user 输入和 assistant 回复都追加到 history
5. 把整个 history 发给 API

【加分项（做完基础再做）】
- 在每条消息前打印 token 数（用 tiktoken 或 response.usage）
- 退出时打印总花费的 token 数

【启动 Claude Code 时建议先问】

    "messages 数组中 role 有哪几种？assistant 这个 role 是谁写的？
     我自己用代码追加 assistant 消息时，content 应该填什么？"

==========================================
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def chat_loop():
    """
    TODO 1：初始化 client（同 day1）
    """
    client = None  # ← 你的代码

    """
    TODO 2：初始化 history 列表
    放一条 system 消息，定义 AI 的角色
    建议：'你是一个简洁的中文助手，回答控制在 50 字以内'
    """
    history = []  # ← 你的代码

    print("输入 exit 退出，clear 清空历史\n")

    while True:
        """
        TODO 3：读用户输入
        - 空输入跳过
        - "exit" 退出循环
        - "clear" 清空 history（但保留第一条 system 消息）
        """
        user_input = input("你: ").strip()
        # ← 你的代码（处理 exit / clear / 空输入）

        """
        TODO 4：把用户输入追加到 history
        格式：{"role": "user", "content": user_input}
        """
        # ← 你的代码

        """
        TODO 5：调用 API，model 用 "deepseek-chat"
        把整个 history 当 messages 传过去
        """
        response = None  # ← 你的代码

        """
        TODO 6：取出 assistant 回复
        打印出来
        【关键】把它也追加到 history（这就是"记忆"的本质）
        """
        # ← 你的代码


if __name__ == "__main__":
    chat_loop()


# ============================================
# 完成检验：
# 你问"我刚才说了什么？"，AI 应该能复述
# 如果 AI "忘了"，说明你没把 history 维护好
# ============================================
