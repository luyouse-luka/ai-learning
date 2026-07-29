"""
Day 2 · Stuff 策略：第一次真实的长文总结

任务：把 attention.pdf 整篇塞进一次 API 调用，让模型产出一份总结，
     并用真实 usage 校准昨天的估算。

规则：
    1. 你的任务是对文本进行总结，不能只是摘抄原文，要提炼出核心思想
    2. 总结的文本最多不要超过400字,需要用中文进行回复，总结回复的文本需要逻辑清晰，通顺无语病
    3. 总结的文本需要缩进两行，根据逻辑语义进行分段，方便阅读
"""

import os
import json
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

# ---------------------------------------------------------------
# 外围（教练直接给，不是考点）
# ---------------------------------------------------------------
BASE_DIR = Path(__file__).parent          # 脚本自己所在的目录，避开 cwd 相对路径的坑
PDF_PATH = BASE_DIR / "attention.pdf"
OUT_PATH = BASE_DIR / "day2_summary.json"

load_dotenv(BASE_DIR.parent / ".env")     # .env 在仓库根

MODEL = "deepseek-v4-flash"               # ← 常量，别再散在 8 个地方
PRICE_IN = 0.14                           # $ / 1M token（缓存未命中）
PRICE_OUT = 0.28                          # $ / 1M token
MAX_OUTPUT_TOKENS = 500                   # 目标 400 中文字 ≈ 240 token，×2 留余量给标点/换行/缩进
EST_RATIO = 0.3                           # 字符 → token 的估算系数（今天校准的就是它）

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)


# ---------------------------------------------------------------
# 【1】读 PDF —— 昨天写过，这次包成函数
# ---------------------------------------------------------------
def load_pdf(path):
    """读 PDF 全文，返回一个字符串。"""
    # TODO: 建 PdfReader，循环 reader.pages，累加 page.extract_text()
    # ⚠️ 累加变量定义在循环外面（你踩过两次的坑）
    # ⚠️ extract_text() 可能返回 None，想想要不要防
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"
        
    return text

# ---------------------------------------------------------------
# 【2】写 system prompt —— 今天的核心，四要素填满
# ---------------------------------------------------------------
# 四要素：角色 / 任务 / 约束（必须可判定！）/ 输出格式
SYSTEM_PROMPT = """
    1. 你的任务是对文本进行总结，不能只是摘抄原文，要提炼出核心思想
    2. 总结的文本最多不要超过400字,需要用中文进行回复，总结回复的文本需要符合中文语言逻辑，通顺无语病
    3. 总结文本根据逻辑语义进行分段，并首行缩进，方便阅读
"""


# ---------------------------------------------------------------
# 【3】调 API —— Stuff：全文一次塞进去
# ---------------------------------------------------------------
def summarize(text):
    """把全文塞进一次调用，返回 (总结文本, response 对象)。"""
    # TODO: 构造 messages —— system 放规矩，user 放正文
    #       想清楚 user 那条的 content 长什么样：光甩正文？还是加一句引导？
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text},
    ]
    # TODO: client.chat.completions.create(...)
    #       必填两个 + max_tokens（护栏，自己定值并说得出依据）
    #       今天不用 stream，理由你已经知道了
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=MAX_OUTPUT_TOKENS,
    )
     # TODO: 从 response 里挖出总结文本
    #       ⚠️ 路径从 response 写起，别从中间开始背
    result = response.choices[0].message.content.strip()
    print(f"{response.choices[0].finish_reason}")

    # TODO: return 总结文本 和 response（外面要用 response.usage）
    return result,response


# ---------------------------------------------------------------
# 【4】成本 & 估算校准 —— 今天必须亲眼看到的数字
# ---------------------------------------------------------------
def report(text, response):
    """打印真实 token、真实成本，以及昨天估算的误差率。"""
    # TODO: 从 response.usage 取真实的 输入 / 输出 token
    #       ⚠️ 字段名今天刚订正过，别再写错
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens

    # TODO: 算真实成本（输入输出分开，先 ÷1,000,000 再 × 单价）
    cost = input_tokens / 1_000_000 * PRICE_IN + output_tokens / 1_000_000 * PRICE_OUT

    # 估算 vs 真实：比【输入 token】。
    # 不比成本——估算里只有输入、cost 里含输出，口径对不上；
    # 而且单价是两边共有的常数，乘不乘都不改变误差率。
    est_tokens = len(text) * EST_RATIO
    diff = (est_tokens - input_tokens) / input_tokens * 100

    print(f"实际成本: ${cost:.6g}   （每 1000 次 ≈ ${cost * 1000:.2f}）")
    print(f"输入 tokens: 估算 {est_tokens:.1f}  /  真实 {input_tokens}")
    print(f"输出 tokens: {output_tokens}")
    print(f"误差率：{diff:+.2f}%   （正 = 估高了，安全；负 = 估低了，危险）")
    return input_tokens, output_tokens, cost, est_tokens, diff


# ---------------------------------------------------------------
# main
# ---------------------------------------------------------------
if __name__ == "__main__":
    
    
    # TODO: 读 PDF
    text=load_pdf(PDF_PATH)
    # TODO: 调用前先自检一句 —— 这坨东西大小合理吗？（想想我埋的那颗雷）
    #大小合理
    # TOOD: 总结
    summary, response = summarize(text)
    # TODO: 打印总结
    print(summary)
    # TODO: 打印总结 + report
    input_tokens, output_tokens, cost, est_tokens, diff = report(text, response)
    # TODO: 存 JSON 到 OUT_PATH（summary / 真实 token / 成本 / 误差率）
    data = {
        "summary" : summary,
        "input_tokens" : input_tokens,
        "output_tokens" : output_tokens,
        "cost": cost,
        "diff": diff
    }
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n已存到 {OUT_PATH}")
