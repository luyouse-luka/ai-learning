"""
Week 3 Day 1 · AI 线阶段 2 开头 —— JSON 解析
教学合约：../week1/CLAUDE.md   ｜ 本周计划：./README.md

目标（做完你要能答出来的三件事）：
  1. json.loads 的三种失败长什么样，各自的报错关键词是什么
  2. response_format={"type":"json_object"} 挡住了其中哪一种、挡不住哪两种
  3. 解析失败时，程序【不许崩】—— 调用方拿到的是什么

⚠️ 本周新硬要求（week3/README.md）：
   交给教练之前，自己先跑几条路径，并在下面这行写下你验了什么。
   我跑了 7 条路径 / 判据是 输出了不同的结果 / 结果是 
    demo_offline里的五条路径
    1. 解析成功 → validate 全通过 → []
    2. 解析失败（except）→ 跳过 validate
    3. 解析成功 → validate 报类型错
    4. 解析失败（except）→ 跳过 validate
    5. 解析成功但空 → validate 报两条 missing
    demo_api 2 条
    6. content 为空 → 解析失败 → ["Parsing failed"] 分支
    7. 解析成功 → validate 返回 []

⚠️ 护栏自查两问（每写一个防御就问一遍）：
   ① 谁调用它？   ② 它判断的那个状态，谁在维护、活多久？
"""

import os
import json
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = "deepseek-v4-flash"
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
)


# ============================================================
# 【素材】三种坏输入 —— 这三条是我给的，不用你造
# ============================================================

BAD_1_WRAPPED = '好的，这是您要的 JSON：\n```json\n{"title": "Transformer", "count": 42}\n```'
BAD_2_LEGAL_BUT_WRONG = '{"title": "Transformer", "count": "42"}'
BAD_3_TRUNCATED = '{"title": "Transformer", "summary": "本文提出自注意力机制'
GOOD = '{"title": "Transformer", "count": 42}'


# ============================================================
# 【1】写一个不会崩的解析函数
# ============================================================
def safe_parse(raw: str) -> dict | None:
    """把模型返回的字符串解析成 dict。解析不了就返回 None，【不许抛异常出去】。

    TODO 你来写：
      - 用 try / except 包住 json.loads
      - except 要精确到 json.JSONDecodeError，不要裸 except
      - 失败时把「报错原因」和「原始字符串的前 80 个字符」打出来，
        否则将来线上出问题你只知道"解析失败了"，不知道模型到底吐了什么
      - 失败返回 None

    ⚠️ 想一想再动手：为什么返回 None，而不是返回 {} ？
       （提示：调用方拿到 {} 之后会做什么？这跟本周主线「没有 A ≠ 有 B」是同一件事）
    """
    # TODO
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: {e} | raw[:80] : {raw[:80]!r}")
    return None 


# ============================================================
# 【2】写一个字段校验函数 —— 这是 safe_parse 挡不住的那一层
# ============================================================
def validate(data: dict, required: dict) -> list[str]:
    """检查 data 里该有的字段有没有、类型对不对。返回【问题清单】，没问题就返回空列表。

    required 的形状（我给定，照着用）：
        {"title": str, "count": int}
        key = 字段名，value = 期望的 Python 类型

    TODO 你来写：
      - 遍历 required，逐个检查
      - 字段不存在   → 往清单里加一条，说清是哪个字段
      - 字段类型不对 → 往清单里加一条，说清期望什么、实际是什么
        （拿到实际类型名用 type(x).__name__）
      - 全部通过 → 返回 []

    ⚠️ 陷阱一枚：Python 里 isinstance(True, int) 是 True。
       今天用不到 bool，但记住这件事，将来校验 bool 字段会栽。
    """
    # TODO
    issues = []
    for field, expected_type in required.items():
        if field not in data:
            issues.append(f"missing field: {field}")
        elif not isinstance(data[field], expected_type):
            issues.append(f"wrong type for field '{field}' (expected {expected_type.__name__}, got {type(data[field]).__name__})")
    return issues


# ============================================================
# 【3】离线跑一遍四条输入，看清三种失败各自的形状
# ============================================================
def demo_offline():
    """不花钱，纯本地。四条输入各走一遍 safe_parse + validate，把结果打出来。

    TODO 你来写：
      - 依次处理 GOOD / BAD_1_WRAPPED / BAD_2_LEGAL_BUT_WRONG / BAD_3_TRUNCATED
      - 每条打印：这是第几条、safe_parse 的结果、validate 的问题清单
      - required 用 {"title": str, "count": int}

    ⚠️ 注意 BAD_2：safe_parse 会成功，validate 会失败。
       跑之前先自己预测一下 BAD_2 会打出什么，跑完对一下你猜得对不对。
    """
    # TODO
    test_cases= [
        ("GOOD", GOOD),
        ("BAD_1_WRAPPED", BAD_1_WRAPPED),
        ("BAD_2_LEGAL_BUT_WRONG", BAD_2_LEGAL_BUT_WRONG),
        ("BAD_3_TRUNCATED", BAD_3_TRUNCATED),
        ("BAD_4_EMPTY_DICT",'{}') 
    ]
    for i, (name, raw) in enumerate(test_cases, start=1):
        print(f"Test case {i} : {name}")
        parsed = safe_parse(raw)
        print(f"safe_parse result : {parsed}")
        if parsed is not None:
            issues = validate(parsed, {"title": str, "count": int})
            print(f"validate issues : {issues}")



# ============================================================
# 【4】真调一次 API —— 验证 response_format 到底挡住了哪一种
# ============================================================
def demo_api(max_tokens: int = 200):
    """让模型输出 JSON，然后走同一套 safe_parse + validate。

    TODO 你来写：
      - client.chat.completions.create(...)，带上 response_format={"type": "json_object"}
      - ⚠️ prompt 里必须出现 "json" 这个词，否则 API 直接报错（这是硬约束，不是建议）
      - 让它返回两个字段：title(str) / count(int)
      - 【顺序要求】先取 finish_reason 并打印，再 safe_parse。
        为什么是这个顺序？—— 见文件头的目标 3，你要能答出来
      - 打印 repr(raw)，不要 print(raw)。repr 才看得见有没有围栏、有没有换行

    ⚠️ 实验（这才是今天的重点，别跳过）：
       跑两次 —— max_tokens=200 和 max_tokens=15
       记录两次的 finish_reason 分别是什么、safe_parse 分别成不成功。
       这一组数据就是「response_format 挡不住失败 3」的证据。
    """
    # TODO
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Please provide a JSON object with fields 'title' (string) and 'count' (integer)."},
        ],
        response_format={"type": "json_object"},
        max_tokens=max_tokens
        )
    content = response.choices[0].message.content
    finish_reason = response.choices[0].finish_reason
    print(f"Finish reason: {finish_reason}") 
    print(f"Raw content: {repr(content)}")
    
    data = safe_parse(content)
    problems = validate(data, {"title": str, "count": int}) if data is not None else ["Parsing failed"]
    print(f"Safe parse result: {data}")
    print(f"Validation problems: {problems}")
    print(response.usage)
if __name__ == "__main__":
    # TODO 先只开 demo_offline()，跑通了再放开 demo_api()
    demo_offline()
    # demo_api(max_tokens=15)
    # CompletionUsage(completion_tokens=15, prompt_tokens=129, total_tokens=144, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=None, reasoning_tokens=15, rejected_prediction_tokens=None), prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cache_write_tokens=None, cached_tokens=128), prompt_cache_hit_tokens=128, prompt_cache_miss_tokens=1)
    # demo_api(max_tokens=200)

    # CompletionUsage(completion_tokens=134, prompt_tokens=129, total_tokens=263, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=None, reasoning_tokens=121, rejected_prediction_tokens=None), prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cache_write_tokens=None, cached_tokens=128), prompt_cache_hit_tokens=128, prompt_cache_miss_tokens=1)
    