# ============================================================
# Week 0.5 结业考：读文件 → 调 API 总结 → 存 JSON
# ============================================================
# 目标：读 input.txt 的内容 → 让模型总结成一句话 → 把结果存进 summary.json
#
# 规则（结业考，从严）：
#   - 代码全部你自己写，我只给「步骤路标」，不给任何代码
#   - 构造 messages 那一步【没有任何提示】，这是对你的核心考核
#   - 不许翻 day1~day6 的文件，不许问 AI 要答案
#   - 卡在哪一步，告诉我卡在第几步、报什么错、你试了什么
#
# 跑法：
#   cd /home/ly/ai-learning/week1
#   source venv/bin/activate      # 激活虚拟环境（有 openai、dotenv）
#   python3 grad_summarize.py
#
# 你手上已有的零件（都练过）：
#   .env 变量名：DEEPSEEK_API_KEY / DEEPSEEK_BASE_URL
#   模型名：deepseek-chat
# ============================================================


# ---- 步骤 1：import 三样东西 ----
# 需要：os、json、load_dotenv、OpenAI
# TODO
import os 
import json

from dotenv import load_dotenv 
from openai import OpenAI


# ---- 步骤 2：把 .env 加载进环境变量 ----
# （想想为什么这句必须在 os.getenv 之前）
# TODO
load_dotenv()

# ---- 步骤 3：创建 client ----
# 用 OpenAI(...)，api_key 和 base_url 都从 os.getenv 取
# TODO
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url=os.getenv("DEEPSEEK_BASE_URL"))


# ---- 步骤 4：读 input.txt 的全部内容，存进变量 text ----
# 用 with open，'r' 模式，encoding="utf-8"
# TODO
text = None
with open('input.txt',"r",encoding="utf-8") as f :
    text = f.read()

# ---- 步骤 5：构造 messages 【无提示，自己写】----
# 要求：
#   - 一个 system 消息，告诉模型它是「中文总结助手，只用一句话总结」
#   - 一个 user 消息，把上面读到的 text 交给它去总结
#   - 想清楚每个消息 dict 有哪两个键
# TODO
messages = [
    {"role": "system", "content": "你是中文总结助手，只用一句话总结"},
    {"role": "user", "content": text}
]


# ---- 步骤 6：调用 API ----
# client.chat.completions.create(...)，传 model 和 messages
# TODO
response = client.chat.completions.create(model="deepseek-chat",messages=messages)


# ---- 步骤 7：从 response 里挖出模型说的那句话，存进 summary ----
# 回忆那条链：response.choices[0].message.content
# TODO
summary = response.choices[0].message.content

print("模型总结：", summary)


# ---- 步骤 8：把结果存进 summary.json ----
# 要求：存成一个字典 {"source": "input.txt", "summary": summary}
# 用 with open 以 'w' 模式打开 summary.json，用 json.dump 写进去
# 提示：json.dump(要写的字典, f, ensure_ascii=False, indent=2)
#       （ensure_ascii=False 让中文正常显示，不变成 \uXXXX）
# TODO
with open('summary.json', 'w', encoding='utf-8') as f:
    json.dump({"source": "input.txt", "summary": summary}, f, ensure_ascii=False, indent=2)

print("已存进 summary.json，去看看")
