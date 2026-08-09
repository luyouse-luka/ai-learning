#一个命令行脚本，输入一个长文本文件（.txt 就行，不用 PDF），输出一份总结。

import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI,APITimeoutError,APIConnectionError,RateLimitError,APIStatusError
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR.parent / ".env") 
MODEL = "deepseek-v4-flash"
PRICE_IN = 0.14                   # $ / 1M token（缓存未命中）
PRICE_OUT = 0.28                  # $ / 1M token

CHUNK_SIZE = 2000 # 每块的大小
CHUNK_OVERLAP = 200 # 块与块之间的重叠大小
DAILY_LIMIT = 200 # 日调用上限次数 参考其他的ai调用的次数
TOKEN_LIMIT = 100_000 # 日调用上限 token 数量 
DAILY_RESET_WINDOW = 24 * 60 * 60 # 满 24h 重置
_calls_today = 0
window_start_time = time.time()
def check_daily_limit():
    # 检查是否超过每日调用次数限制
    global _calls_today, window_start_time
    now= time.time()
    if now - window_start_time > DAILY_RESET_WINDOW:
        _calls_today = 0
        window_start_time = now
    if _calls_today >= DAILY_LIMIT:
        raise Exception("已达到每日调用次数上限，请稍后再试。")
client = OpenAI(api_key = os.getenv("DEEPSEEK_API_KEY"),base_url=os.getenv("DEEPSEEK_BASE_URL"))

def split_text(text: str, chunk_size: int, overlap: int): 
    """把成文本qie成若干块，每块 chunk_size 字符，块与块之间 overlap 字符重叠"""
    if overlap >= chunk_size: # 重叠部分不能超过块的大小，否则会出现死循环 step <=0
        raise ValueError("overlap 不能大于等于 chunk_size")
    step = chunk_size - overlap # 每块的步长
    chunks = [] # 存放切块后的文本
    start = 0
    while start < len(text): 
        end = start + chunk_size # 每块的结束位置
        chunk = text[start:end] # 切出一块文本
        chunks.append(chunk)
        if end >= len(text):
            break
        start += step
    return chunks

SYSTEM_PROMPT_TOTAL = """
    1. 你的任务是对文本进行总结，不能只是摘抄原文，要提炼出核心思想
    2. 总结的文本最多不要超过400字,需要用中文进行回复，总结回复的文本需要符合中文语言逻辑，通顺无语病
    3. 总结文本根据逻辑语义进行分段，并首行缩进，方便阅读
"""
SYSTEM_PROMPT_CHUNK = """ 你的任务是这块文本进行总结，不超过50字,需要用中文进行回复，总结回复的文本需要符合中文语言逻辑"""
 
def summarize_text(client,text:str,system_prompt:str):
    global _calls_today
    if not text or text.strip() == "":
       raise Exception("文本为空，请检查输入")
    check_daily_limit()
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ]
        )
    except APITimeoutError:
        raise Exception("上游模型超时，请稍后重试")
    #APITimeoutError 是 APIConnectionError 的子类，如果APIConnectionError在APITimeoutError前会被吞掉
    except APIConnectionError:
        raise Exception("连不上服务器模型")
    except RateLimitError:
        raise Exception("上游限流，请稍后再试") # 余额用尽的报错式  402（402 Insufficient Balance）
    #至于码， 502 说得过去，但 429 更可操作：502 暗示上游坏了（别重试），429 说的是过会儿再来（可以重试） —— 限流属于后者。
    except APIStatusError as e:
        raise Exception(f"上游返回 {e.status_code}")
    _calls_today += 1
   
    finish_reason = response.choices[0].finish_reason
    result = response.choices[0].message.content
    if not result or result.strip() == "":
        raise ValueError("AI 没有返回任何内容，可能是模型出错或文本过长")
    
    if finish_reason == "length":
        truncated = True
    else:
        truncated = False

    prompt_tokens = response.usage.prompt_tokens #输入的 token 数
    completion_tokens = response.usage.completion_tokens #输出的 token 数
    prompt_cost = prompt_tokens / 1000000 * PRICE_IN #输入的成本
    completion_cost = completion_tokens / 1000000 * PRICE_OUT #输出的成本
    return result,prompt_tokens,completion_tokens,truncated,prompt_cost,completion_cost

def summarize_chunks(client,chunks:list[str]):
    summaries = []
    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_prompt_cost = 0
    total_completion_cost = 0
    for chunk in chunks: 
        summary,prompt_tokens,completion_tokens,truncated,prompt_cost,completion_cost = summarize_text(client,chunk,SYSTEM_PROMPT_CHUNK)
        total_prompt_tokens += prompt_tokens
        total_completion_tokens += completion_tokens
        total_prompt_cost += prompt_cost
        total_completion_cost += completion_cost
        summaries.append(summary)
        print(len(summary), completion_tokens)
    return "\n".join(summaries),total_prompt_tokens,total_completion_tokens,total_prompt_cost,total_completion_cost

if __name__ == "__main__":
    # 用法: python day7_review.py <文本文件路径>
    # 路径写死 = 脚本，路径从命令行来 = 工具。分界线就在这三行。
    if len(sys.argv) < 2:
        print(f"用法: python {Path(__file__).name} <文本文件路径>")
        sys.exit(1)                      # 非 0 退出码 = 告诉调用方"我失败了"，管道/CI 才看得见

    input_path = Path(sys.argv[1])       # sys.argv[0] 是脚本自己，[1] 才是第一个参数
    if not input_path.is_file():         # 先验存在，否则下面 open 抛 FileNotFoundError 带一堆栈
        print(f"文件不存在或不是文件: {input_path}")
        sys.exit(1)

    with open(input_path,"r",encoding="utf-8") as f:
        content = f.read() # 读文件
    print(f"[输入] {input_path}  {len(content)} 字符")
    if len(content) < CHUNK_SIZE:
        total_summary,prompt_tokens,completion_tokens,truncated,prompt_cost,completion_cost = summarize_text(client,content,SYSTEM_PROMPT_TOTAL)
        print(total_summary)
        print(f"总共使用了 {prompt_tokens} 个输入 token, {completion_tokens} 个输出 token")
        print(f"总共花费了 ${prompt_cost:.6f} 的输入成本, ${completion_cost:.6f} 的输出成本")
        if truncated:
            print("注意：总结文本被截断，可能不完整")
    else:
        chunks = split_text(content,CHUNK_SIZE,CHUNK_OVERLAP) 
        total_chunk,total_prompt_tokens,total_completion_tokens,total_prompt_cost,total_completion_cost = summarize_chunks(client,  chunks)
        total_summary,prompt_tokens,completion_tokens,truncated,prompt_cost,completion_cost = summarize_text(client,total_chunk,    SYSTEM_PROMPT_TOTAL)
        print(total_summary)
        print(f"总共使用了 {total_prompt_tokens + prompt_tokens} 个输入 token, {total_completion_tokens + completion_tokens} 个输出     token")
        print(f"总共花费了 ${total_prompt_cost + prompt_cost:.6f} 的输入成本, ${total_completion_cost + completion_cost:.6f} 的输出成本 ")
        if truncated:
            print("注意：总结文本被截断，可能不完整")

