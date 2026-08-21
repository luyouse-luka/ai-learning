"""
Week 3 Day 2 · AI 线阶段 2 —— Function Calling（工具调用）
教学合约：../week1/CLAUDE.md   ｜ 本周计划：./README.md   ｜ 昨天：./day1_json.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
今天唯一要带走的一句话：
    模型不会真的调用任何工具。它只会写一张纸条告诉你「我想调这个，参数是这些」，
    真正动手的是你的代码。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

目标（做完你要能答出来的四件事）：
  1. 四步流程分别是什么，模型被调用了几次
  2. tool_calls 是 None 的时候意味着什么，代码要怎么防
  3. arguments 是什么类型，为什么昨天的 safe_parse 必须搬过来
  4. schema 帮你锁住了昨天四层模型的哪几层，哪一层依然没人管

⚠️ 本周硬要求（week3/README.md）：交付前自己先跑几条路径，在下面写下你验了什么。
   ⚠️ 昨天这行被判「路径数是实的，判据不合格」——「输出了不同的结果」不是判据。
   今天的格式要求升级：每条路径必须写出【你期望看到的那个具体值】。
   反例：「跑通了 / 输出不同 / 没报错」
   正例：「期望 finish_reason == 'tool_calls' 且 m.content == ''」

   我跑了 __ 条路径：
     1.
     2.
     3.

⚠️ 护栏自查两问（每写一个防御就问一遍）：
   ① 谁调用它？   ② 它判断的那个状态，谁在维护、活多久？
"""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
)

MODEL = "deepseek-v4-flash"


# ============================================================
# 【素材】工具 1 的 schema —— 这一份我给你，逐行注释，照着改
# ============================================================
# 为什么给你：JSON Schema 这套写法你没见过，从零设计不是难度问题，是没素材。
# 你的活是【照着写第二个】，不是从零发明。
WEATHER_TOOL = {
    "type": "function",              # 目前只有 "function" 这一种，写死
    "function": {
        "name": "get_weather",       # ← 必须和你下面那个 Python 函数名一致，模型靠这个字符串指认
        "description": "查询某个城市当前天气",
                                     # ↑ 这句是【给模型看的】，不是注释。
                                     #   模型完全靠它决定「该不该用这个工具」。
                                     #   写得含糊 → 该用时不用 / 不该用时乱用。
        "parameters": {              # ↓ 从这里开始是 JSON Schema，描述「参数表单长什么样」
            "type": "object",        #   参数整体是一个对象（键值对），几乎永远是 object
            "properties": {          #   表单里有哪些格子
                "city": {
                    "type": "string",           # 这个格子填字符串
                    "description": "城市名，如 悉尼、Sydney",   # 也是给模型看的
                },
            },
            "required": ["city"],    # 哪些格子必填。没列进来的 = 可选
        },
    },
}


# ============================================================
# 【1】照着上面，写第二个工具的 schema
# ============================================================
# TODO 你来写：get_exchange_rate —— 查汇率
#   - 两个参数：from_currency / to_currency，都是 string，都必填
#   - description 两处都要写（函数一处、每个参数一处）
#
# ⚠️ 写完先别急着跑，回答一个问题：
#    required 里如果漏写了 to_currency，会发生什么？
#    （提示：schema 是「要求」还是「保证」？这跟昨天 response_format 挡不住哪两层是同一件事）
#   能正确运行但是不能返回想要的解结果， schema 只是要求，和response_format 挡不住空的字符串一样
EXCHANGE_TOOL = {
    # TODO
    "type": "function",
    "function": {
        "name": "get_exchange_rate",
        "description": "查询从一个国家到另一个国家的汇率",
        "parameters": {
            "from_currency": {
                "type": "string",
                "description": "国家名，比如 中国、China"
            },
            "to_currency": {
                "type": "string",
                "description": "国家名，比如美国、USA"
            }
        }
    }
}

TOOLS = [WEATHER_TOOL, EXCHANGE_TOOL]  # TODO 第二个工具写完后加进来


# ============================================================
# 【2】真正干活的本地函数 —— 后厨在这里
# ============================================================
# 今天不接真 API，返回写死的假数据就行（重点是流程，不是数据来源）
def get_weather(city: str) -> dict:
    """TODO 你来写：返回一个 dict，含 city / temp_c / condition 三个键，值写死"""
    # TODO
    weather_dict = {'city': "china","temp_c": 30,"condition": "阴天"}
    return weather_dict
    
def get_exchange_rate(from_currency: str, to_currency: str) -> dict:
    """TODO 你来写：返回一个 dict，含 from / to / rate 三个键，值写死"""
    # TODO
    exchange_rate_dict = {"from": "China","to": "USA","rate":"0.3"}

# 名字 → 函数对象的映射表。模型给你的是【字符串】"get_weather"，
# 你得把字符串变成能调用的东西 —— 这张表就是干这个的。
TOOL_REGISTRY = {
    "get_weather": get_weather,
    # TODO 第二个函数写完后加进来
    "get_exchange_rate": get_exchange_rate
}


# ============================================================
# 【3】把昨天的 safe_parse 搬过来
# ============================================================
# TODO 你来写：直接从 day1_json.py 复制过来即可，一个字不用改。
#   ⚠️ 这不是偷懒，是今天的重点之一：
#      模型返回的 arguments 是一串【模型现编的 JSON 文本】，
#      它可以被 max_tokens 截断、可以少字段、可以类型不对。
#      昨天那四层模型，今天原样再走一遍。
def safe_parse(raw: str) -> dict | None:
    # TODO
    try:
            return json.loads(raw)
    except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e} | raw[:80] : {raw[:80]!r}")
            return None 


# ============================================================
# 【4】四步流程 —— 今天的正题
# ============================================================
def run(user_question: str, max_tokens: int = 400):
    """走完 Function Calling 的一个完整回合。

    ┌─ 第 1 步：带着菜单去问模型 ────────────────────────────────
    TODO
      - client.chat.completions.create(model=MODEL, messages=messages,
                                       tools=TOOLS, max_tokens=max_tokens)
      - 打印 finish_reason —— 你会看到第三种值（以前只见过 stop / length）
      - 打印 repr(message.content) —— 猜猜是 None 还是 ''？先猜再跑
    
    ┌─ 第 2 步：检查模型到底想不想用工具 ──────────────────────────
    TODO
      - ⚠️ 必须先判断 if not message.tool_calls: —— 直接写 tool_calls[0] 会崩
        （问「1+1 等于几」时它就是 None，实验 2 你会亲眼看到）
      - 没有 tool_calls → 说明模型直接回答了，打印 content 后 return
      - 有 tool_calls → 把 message 本身 append 进 messages（原样回填，一个字不改）
        为什么要回填：第 2 次调用时模型得看见「我上一轮开过这张条子」，否则它不认账

    ┌─ 第 3 步：你来执行 ────────────────────────────────────────
    TODO 对每一个 tool_call：
      - 取 name 和 arguments
      - ⚠️ arguments 是 str，用【第 3 块】的 safe_parse 解析，不要直接 json.loads
      - 解析失败怎么办？—— 你自己决定，但必须【明确决定】，不许让它崩。
        想一想：这里返回 None，跟昨天 'null' 那个洞是不是同一个坑？
      - 从 TOOL_REGISTRY 查出函数对象，用 **args 调用
      - 把结果 append 进 messages，形状固定是这三个键：
            {"role": "tool", "tool_call_id": <那张条子的 id>, "content": <字符串>}
        ⚠️ content 必须是【字符串】，dict 要先 json.dumps(..., ensure_ascii=False)
        ⚠️ tool_call_id 必须对上号 —— 模型可能一次开三张条子，你得说清这是哪张的结果

    ┌─ 第 4 步：把结果交回去，让模型说人话 ────────────────────────
    TODO
      - 再调一次 create(...)，messages 现在比第 1 次多了两条
      - 打印最终 content
      - 打印这一次的 finish_reason，和第 1 次对比

    最后 return 什么由你定，但想一想：调用方拿到什么才够用？
    """
    messages = [{"role": "user", "content": user_question}]
    # TODO
    #1 带着问题去问模型
    resp1 = client.chat.completions.create(model=MODEL,messages= messages,max_tokens=max_tokens,tools=TOOLS)
    # tools 把菜单传过去
    message = resp1.choices[0].message
    print(f"[1] finish_reason = {resp1.choices[0].finish_reason !r}")
    print(f'[1] content       = {message.content !r}') 

    #2 模型需不需要用工具
    if not message.tool_calls:
        print(f"[2] 模型没开条子，直接回答了：{message.content}")
        return message.content
    
    print(f"[2] 模型开了条子 {len(message.tool_calls)} 张条子（用了多少工具）")
    messages.append(message) # 原样回填，一字不改
    
    #3 
    for tc in message.tool_calls:
        name = tc.function.name
        raw_args = tc.function.arguments
        print(f"[3] name={name!r} arguments={raw_args!r} type={type(raw_args).__name__}")
        args = safe_parse(raw_args)
        if not isinstance(args,dict):
            result = {"error": f"arguments 不是合法的参数对象: {raw_args !r}"}
        else: 
            fn =TOOL_REGISTRY.get(name)
            if fn is None:
                result ={"error": f"未注册的工具： {name}"}
            else:
                result =fn(**args)
        messages.append({
            "role":"tool",
            "tool_call_id":tc.id,
            "content": json.dumps(result,ensure_ascii=False)
        })
        
    #4 返回结果 让模型给出答复
    resp2 = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        max_tokens=max_tokens

    )
    final =resp2.choices[0].message.content
    print(f"[4] finish_reason ={resp2.choices[0].finish_reason !r}")
    print(f"[4] content       ={final}")
    return final
# 如果模型想要知道调没调用 tool ,需要再返回 tool_call_id


# ============================================================
# 【5】三条实验 —— 这才是今天的重点，别跳过
# ============================================================
def experiments():
    """三条路径，每条跑完先写下【你期望看到什么】，再看实际输出。

    实验 1（正常路径）：run("悉尼现在天气怎么样？")
        观察：finish_reason / content 是不是空 / arguments 的 type

    实验 2（模型不用工具）：run("1+1 等于几？")
        观察：tool_calls 是什么。
        ⚠️ 这条是【专门用来打你的】—— 如果第 2 步没写那个 if，这里必崩。
        崩了是好事，说明防御是必需的，不是我吓唬你。

    实验 3（arguments 被截断）：run("悉尼现在天气怎么样？", max_tokens=30)
        观察：finish_reason 是什么 / arguments 完不完整 / safe_parse 接没接住。
        ⚠️ 昨天实测：这个模型光推理就吃 ≈121 token，max_tokens 有效下限 ≈134。
           设 30 会发生什么，你先预测一个，再跑。

    实验 4（选做）：一句话里问两件事，看 tool_calls 是不是返回两条
    """
    # TODO
    print("=" * 60, "\n实验 1 · 正常路径")
    # 我期望看到：finish_reason stop，content 不为空  type dict
    run("悉尼现在天气怎么样？")

    print("=" * 60, "\n实验 2 · 模型不用工具")
    # 我期望看到：[2] 模型没开条子，直接回答了 2 
    run("1+1 等于几？")

    print("=" * 60, "\n实验 3 · arguments 被截断")
    # 我期望看到： JSONDecodeError: {e} | raw[:80] : 
    run("悉尼现在天气怎么样？", max_tokens=30)

if __name__ == "__main__":
    # TODO 先跑 experiments()，一条一条来，不要一次全放开
    ...
    experiments()