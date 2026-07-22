"""
Day 1 · Hello World：第一次成功调用 LLM API
==========================================

【今日目标】
跑通从「Python 代码」到「LLM 返回结果」的完整链路。
不要追求完美，能跑通就赢了。

【今日必须掌握的概念】
1. API Key = 你的"身份证 + 钱包"，泄漏 = 别人花你的钱
2. client = 与 API 服务的连接对象（轻量，可复用）
3. messages = 一个数组，每条带 role 和 content
4. model = 你要调用哪个具体的模型（不同模型价格能力不同）
5. response = 一个嵌套对象，回答藏在 response.choices[0].message.content

【启动 Claude Code 后，对它说】

    开始 day 1

    （它会按 CLAUDE.md 的规则先给你讲原理，不会直接写代码）

【完成标准】
- 终端能看到 LLM 的回复（哪怕只是一句"你好"）
- 你能解释这段代码每一行在干什么
- 你能不看代码、关掉编辑器、在白纸上重写一遍

【常见踩坑】
- ❌ API Key 写错（多空格 / 引号没去掉）→ 401 错误
- ❌ base_url 漏掉 https:// → 连接错误
- ❌ 没装 openai 包 → ImportError
- ❌ Python 版本太老（<3.8）→ 语法错误

【反模式（请不要做）】
- 不要让 Claude Code 直接写完整代码就跑通就完事
- 不要不看任何文档
- 不要不读报错就喊"修一下"

==========================================
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # 从 .env 读取环境变量


def hello_llm():
    """
    TODO 1：创建 OpenAI 客户端
    提示：用 OpenAI(api_key=..., base_url=...)
    从环境变量读取，不要硬编码
    """
    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url=os.getenv("DEEPSEEK_BASE_URL"))  # ← 你的代码

    """
    TODO 2：构造 messages 数组
    提示：至少要有一条 role=user 的消息
    试试加一条 role=system 的"系统提示"，看看输出有什么变化
    """ 
    messages = [{"role":"user","content":"who are you?"}]  # ← 你的代码

    """
    TODO 3：调用 client.chat.completions.create()
    必填参数：model、messages
    DeepSeek 的 model 用 "deepseek-chat"
    """
    response = client.chat.completions.create(model="deepseek-chat", messages=messages)  # ← 你的代码   

    """
    TODO 4：从 response 里取出文本内容
    提示：response.choices[0].message.content
    打印出来
    """
    # ← 你的代码
    print(response.choices[0].message.content)

if __name__ == "__main__":
    hello_llm()


# ============================================
# 完成后向 Claude Code 说："day 1 完成"
# 它会按 CLAUDE.md 出 3 道题考你
# 答完把得分填进 README.md
# ============================================
