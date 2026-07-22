"""
Day 3 · 流式输出 Streaming
==========================================

【今日目标】
让 AI 的回复像打字机一样一个字一个字蹦出来，而不是等几秒一次性出来。

【为什么要学这个】
所有用户面向的 AI 产品都必须做流式输出。
不做的话，用户面对 3-10 秒的空白等待会以为程序卡死。
ChatGPT / Claude 的"打字机效果"全是流式实现的。

【底层原理（先想清楚再写）】
- 不开 stream：HTTP 请求 → 服务器算完 → 一次返回完整 JSON
- 开 stream：HTTP 长连接 → 服务器每生成一个 token 就推一次（SSE）
- 总耗时和 token 数其实一样，但用户体感快 5-10 倍

【启动 Claude Code 后，对它说】

    开始 day 3

【启动后建议先问 Claude Code】

    "对比 stream=True 和 stream=False 在 HTTP 协议层面有什么不同？
     为什么流式让用户体感更快，但总耗时其实一样？
     先讲原理，不要写代码。"

【需要实现的功能】
基于 day2_chat.py 改造（或新写）：
1. 调用 API 时加 stream=True
2. 用 for 循环遍历 stream
3. 每收到一个 chunk，立刻 print 出来（不要等）
4. 把所有 chunk 拼起来，再追加到 history

【关键 3 个坑】
1. print 默认会换行 → 必须 end=""
2. print 默认有缓冲 → 必须 flush=True
3. chunk.choices[0].delta.content 可能为 None → 要判空

【伪代码（自己写，不要复制）】
    stream = client.chat.completions.create(..., stream=True)
    collected = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta is not None:
            print(delta, end="", flush=True)
            collected += delta
    print()  # 最后换行
    history.append({"role": "assistant", "content": collected})

【加分项】
- 加一个"打字速度"统计（chars per second）
- 加一个"中断"功能（按 Ctrl+C 停止当前回复但不退出程序）
==========================================
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def stream_chat():
    """
    TODO 1：初始化（同 day2）
    """
    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"),base_url=os.getenv("DEEPSEEK_BASE_URL"))  # ← 你的代码
    history = [{"role": "system","content": "you are a claudeCode chatbot"}]  # ← 你的代码

    while True:
        user_input = input("你: ").strip()
        if user_input == "exit":
            break
        elif user_input == "clear":
            history = [{"role": "system","content": "you are a claudeCode chatbot"}]  # ← 你的代码
            continue
        elif user_input == "":
            continue
        # ← 处理空输入 / clear
        """
        TODO 2：追加 user 消息
        """
        history.append({"role": "user", "content": user_input})  # ← 你的代码
        # ← 你的代码

        """
        TODO 3：调用 API with stream=True
        """
        stream = client.chat.completions.create(model="deepseek-chat", messages=history, stream=True)  # ← 你的代码
    
       
        
        """
        TODO 4：边收边打印 + 收集
        关键：end="" 和 flush=True
        判空：delta.content is not None
        """
        print("AI: ", end="", flush=True)
        collected = ""
        # ← 你的代码（for chunk in stream）
        try:
            for chunk in stream: # 遍历实时数据流 
                delta = chunk.choices[0].delta.content #  delta 流式输出专属取值语法
                if delta is not None: #AI 输出结束时，会返回一个空值，加这个判断 =不打印空内容、避免报错 
                                    #  不判空的后果:collected += None 会直接 TypeError(字符串不能和 None 相加),程序当场崩。
                                    
                    print(delta, end="", flush=True)  # ← 你的代码
                    collected += delta  # ← 你的代码
        except KeyboardInterrupt:
            print("\n【已中断当前回复】")
            continue  # 直接返回到主循环，等待下一轮输入
        print()  # 换行

        """
        TODO 5：把完整回复追加到 history
        """
        # ← 你的代码
        print("【本轮发出去的历史条数】", len(history))  # 检查历史条数是否增加
        
        history.append({"role":"assistant","content":collected})  # ← 你的代码
        

if __name__ == "__main__":
    stream_chat()


# ============================================
# 完成检验：
# 1. 字应该一个一个出现，不是一次性出现
# 2. 多轮对话 AI 仍能记住上下文
# 3. Ctrl+C 不应该让整个程序崩溃
# ============================================
