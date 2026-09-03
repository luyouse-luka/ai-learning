"""
Day 3 · 把 day2_summarize.py 包成一个服务

任务：让「上传一个 PDF → 拿到总结 + token + 成本」这件事，
     变成任何人拿着 URL 就能调用的接口。

跑起来（教练来跑，你只写）：
    week1/venv/bin/python -m uvicorn week2.api.main:app --reload --port 8000
    然后浏览器开 http://127.0.0.1:8000/docs 点着测

今天的边界：
    ✅ 今天做：契约设计、状态码分类、finish_reason 检查、文件类型/空文本校验
    ⏭ Day 5 做：超时、429/5xx 指数退避、日调用上限、部署
"""

import os
import io
import time

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel, Field
from pypdf import PdfReader
from pathlib import Path
from openai import OpenAI,APITimeoutError,APIConnectionError,RateLimitError,APIStatusError
# ---------------------------------------------------------------
# 外围（教练直接给，和 day2 一样，不是今天的考点）
# ---------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent.parent / ".env")          # .env 在仓库根

MODEL = "deepseek-v4-flash"
PRICE_IN = 0.14                                       # $ / 1M token
PRICE_OUT = 0.28                                      # $ / 1M token
MAX_OUTPUT_TOKENS = 500
EST_RATIO = 0.3

MAX_FILE_BYTES = 10 * 1024 * 1024  # 10 MB
MAX_CHARS = 200_000 # 正文字符上限

# ---------------------------------------------------------------
# Day 5 · 护栏参数
# ---------------------------------------------------------------
# TODO【5.1】超时秒数：先写 60，跑完看数据再调（规则 7：先做后定）
#       出处：SDK 默认 read timeout = 600s，是你实测 5.78s 的 100 倍，太长
# REQUEST_TIMEOUT = ...
#
REQUEST_TIMEOUT = 60  # 超时秒数，先写 60

# TODO【5.3】日调用上限：这几个常量你定，每个写一行理由
#       a) 按「调用次数」还是按「累计美元」卡？—— 二选一
#       b) 阈值给多少？（先随便给一个，跑完看数据再调）
#       c) 周期怎么算？自然日 00:00 重置，还是进程启动后满 24h 重置？
# DAILY_LIMIT = ...
DAILY_LIMIT = 200 # 日调用上限次数 参考其他的ai调用的次数
TOKEN_LIMIT = 100_000 # 日调用上限 token 数量 
DAILY_RESET_WINDOW = 24 * 60 * 60 # 满 24h 重置



client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    # TODO【5.1】加两个参数：timeout= / max_retries=
    #       max_retries 的 SDK 默认值就是 2，已自带指数退避 + jitter，你不用写退避逻辑
    #       ⚠️ 这两个数是乘起来的：timeout=60 + max_retries=2 → 最坏 180s 才返回
    max_retries =2,
    timeout=REQUEST_TIMEOUT,
   
)

# TODO【5.3】日调用计数器（模块级 = 进程内，重启就清零，够用）
#       ⚠️ 你踩过两次的坑：累加变量放在哪一层
#       ⚠️ 光有计数不够，还要存「上次重置的时刻」，否则它只会一路涨到天荒地老
# _calls_today = ...
# _window_start = ...

_calls_today = 0
_window_start = time.time()

def check_daliy_limit ():
    """ 花钱之前问一句，今天还有额度吗，没有就退回去"""
    global _calls_today, _window_start #
    now = time.time()
 
    if now - _window_start >= DAILY_RESET_WINDOW: # 窗口过期 重开一天
        _calls_today = 0
        _window_start = now 
    if _calls_today >= DAILY_LIMIT:
        raise HTTPException(
            status_code = 429, #402是没付钱，503整个服务挂了，429你没错，只是现在不行，过会再来
            detail =f"今日调用已达上限 {DAILY_LIMIT}次，请稍后重试"
        )
        
app = FastAPI(title="PDF 总结服务", version="0.1.0")

# day2 的 system prompt，原样搬过来
SYSTEM_PROMPT = """
    1. 你的任务是对文本进行总结，不能只是摘抄原文，要提炼出核心思想
    2. 总结的文本最多不要超过400字,需要用中文进行回复，总结回复的文本需要符合中文语言逻辑，通顺无语病
    3. 总结文本根据逻辑语义进行分段，并首行缩进，方便阅读
"""


# ---------------------------------------------------------------
# 【1】出口的形状 —— 今天的核心之一
# ---------------------------------------------------------------
# 调用方（明天的前端）拿到这个 JSON 之后要显示什么？想清楚再写字段。
# 提示：day2 你已经往 day2_summary.json 里存过一份，那份的字段够不够用？
#      少了什么会让前端「不知道该不该信这段总结」？
class SummarizeResponse(BaseModel):
    # TODO: 定义字段名和类型（str / int / float）
    #       ⚠️ 字段一旦定下来就是契约，明天前端按它来写，改一次两边都要动
    #      ⚠️ 你觉得「总结文本」够不够？要不要加一个「是否被截断」的 bool？
    # 同day 2的json字段名差不多
    summary: str
    truncated: bool
    input_tokens: int 
    output_tokens: int = Field(description="计费口径的输出 token，含模型推理部分，非总结正文长度")
    cost: float
    model: str


# ---------------------------------------------------------------
# 【2】GET /health —— 最简单的门
# ---------------------------------------------------------------
# 用途：部署之后，你（或者监控）敲一下就知道服务活没活着。
# 铁律：不调 AI、不花钱、不读文件。它要在服务半死不活时也能回话。
@app.get("/health")
def health():
    # TODO: 返回一个 dict，里面放什么你定
    #       想一想：只回 {"ok": true} 够吗？你还想知道什么？
    return {
        "status": "ok", #进程活着能处理的请求
        "model": MODEL, #线上跑的模型名字
        "api_key_configured": bool(os.getenv("DEEPSEEK_API_KEY")), #key 有没有配上
        "version": app.version, #线上跑的是哪一版的代码
    }
# 存在以下几种的实际情况：
# 1. 页面打不开/一直转圈 ==》进程死了 防火墙问题--》登录服务器
# 2. 打开了 .env 没跟着部署上去——这是部署到新机器最常见的一类事故，本地跑得好好的，线上 os.getenv 返回 None，直到有人调 /summarize 才炸
# 3. model 显示不是你想要的模型——你改了代码，忘了重新部署
# 4. version 显示不是你想要的版本——你改了代码，忘了重新部署 服务没重启

# ---------------------------------------------------------------
# 【3】从上传的字节流读 PDF
# ---------------------------------------------------------------
def extract_pdf(data: bytes) -> str:
    """把上传上来的 PDF 字节流读成纯文本。

    和 day2 的 load_pdf 唯一的区别：输入不是路径，是一坨 bytes。
    外围提示（不是考点）：PdfReader 除了吃路径，也吃「像文件一样的对象」，
                        用 io.BytesIO(data) 把 bytes 包成这种对象即可。
    """
    # TODO: 循环 reader.pages 累加 extract_text()
    #       ⚠️ 累加变量在循环外（你踩过两次）
    #       ⚠️ extract_text() 可能返回 None
    #       ⚠️ 页尾要补 "\n"，否则页码和正文粘一起（day2 的 sequence/6length）
    

    reader = PdfReader(io.BytesIO(data))
    text = ""
    for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
            
    return text


# ---------------------------------------------------------------
# 【4】POST /summarize —— 主接口
# ---------------------------------------------------------------
@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(file: UploadFile = File(...)):
    """收一个 PDF，返回总结 + 真实 token + 成本。"""

    data = await file.read()          # 外围：读上传的字节流，固定写法

    # ---- 4.1 把门守住 ------------------------------------------------
    # 门开了，进来的不一定是 attention.pdf。至少挡住三样东西：
    #   a) 根本不是 PDF（.jpg / .exe 改个后缀就进来了）
    #   b) 提取出来是空的（扫描件图片 PDF，一个字都提不出）
    #   c) 大到会烧钱的（day2 那颗雷：「这坨东西大小合理吗」，今天必须真写出来）
    #

    # TODO: 三条校验，各自 raise HTTPException
    #       外围提示（语法直接给，你只管想「哪一条配哪个码」）：
    #           raise HTTPException(status_code=400, detail="说人话的原因")
    #       ⚠️ 想清楚每一条到底是「调用方的错」还是「我的错」→ 决定 4xx 还是 5xx
    #       ⚠️ c) 的阈值先随便给一个你觉得合理的数，写上你的理由，跑完看数据再调
    #          （规则 7：先做后定，不要求你现在论证）
    # a) 检查文件类型：file.content_type
    if not data.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="上传的文件不是 PDF")
    # b) 文件本身太大，提取要吃CPU，在提取前拦截
    if len(data) > MAX_FILE_BYTES:
        raise HTTPException(status_code=413, detail="文件超过 10 MB")
    text= extract_pdf(data)
    # c) 提取出来是空的 
    if not text.strip():
        raise HTTPException(status_code=400,detail="PDF 提取出来是空的，可能是扫描件或图片 ")
    # d) 正文太长 （防烧钱）
    if len(text) > MAX_CHARS:
        raise HTTPException(status_code=413, detail=f"正文 {len(text)} 字符，上限 {MAX_CHARS} ")
    # ---- 4.15 日调用上限（Day 5) --------------------------------------
    # TODO【5.3】在这里检查「今天还有没有额度」
    #       为什么放这个位置：4.1 的门禁问的是「这一次值不值得做」，
    #                        额度问的是「今天还做不做」—— 两个都必须在花钱之前
    #       ⚠️ 计数在哪一行 +1？调用失败了算不算用掉一次额度？想清楚再写
    #       触顶了返回哪个码 —— 429 / 503 / 402 三选一，写上理由
    check_daliy_limit()
    #402是没付钱，503整个服务挂了，429你没错，只是现在不行，过会再来
    # ---- 4.2 调模型 --------------------------------------------------
    # TODO: messages 构造 + client.chat.completions.create(...)
    #       和 day2 一模一样，别看 day2_summarize.py，先默写
    #
    # TODO【5.2】Day 5：把下面这次 create() 用 try / except 包起来，映射成 502 / 504
    #       继承链（我在服务器上打出来的，不是凭印象）：
    #           APITimeoutError  ←  APIConnectionError  ←  APIError
    #           RateLimitError / InternalServerError  ←  APIStatusError  ←  APIError
    #       ⚠️ APITimeoutError 是 APIConnectionError 的子类。except 从上往下匹配，
    #          父类写在前面 → 超时被它整个吞掉 → 504 永远不出现，
    #          而且不报错、日志正常、测试也过（本周主线「静默 bug」的又一张脸）
    #       ⚠️ 你自己 raise 的 HTTPException 会不会被这个 except 误伤？
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text}
    ]
    try: 
        response = client.chat.completions.create(model=MODEL, messages=messages, max_tokens=MAX_OUTPUT_TOKENS)
    except APITimeoutError:
        raise HTTPException(status_code=504, detail="上游模型超时，请稍后重试")
    #APITimeoutError 是 APIConnectionError 的子类，如果APIConnectionError在APITimeoutError前会被吞掉
    except APIConnectionError:
        raise HTTPException(status_code=502, detail="连不上服务器模型")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="上游限流，请稍后再试") # 余额用尽的报错式  402（402 Insufficient Balance）
    #至于码，你填的 502 说得过去，但 429 更可操作：502 暗示上游坏了（别重试），429 说的是过会儿再来（可以重试） —— 限流属于后者。改不改都行。
    except APIStatusError as e:
        raise HTTPException(status_code=502, detail=f"上游返回 {e.status_code}")
    
    # ---- 4.3 检查它是怎么停下来的 ------------------------------------
    # day2 的遗留：你只 print 了 finish_reason，没有「检查」。
    # 打印 ≠ 检查。在脚本里没人看见，在服务里 = 用户拿到半截总结当成品。
    #
    # TODO: finish_reason == "length" 时怎么办？
    #       想清楚：这是谁的错？该返回什么码？还是说……不该报错，而是照常返回但告诉调用方？
    #       （这题没有唯一答案，写下你的选择和理由，我批）
    #
    # TODO【5.4】Day 5 · 还 Day 3 的债：现在是「先取值、后验值」，要倒过来
    #       走一遍现在的代码：content='' → .strip() → summary="" + truncated=True + HTTP 200
    #                        钱花了、内容是空的、没有一处报错、前端渲染出一片空白
    #       镜像那一半：content=None → .strip() 直接 AttributeError → 500，同样是钱花完才崩
    #       ⚠️ 「or "" 防不住 ''」的镜像是「.strip() 防不住 None」
    #       要你决定：「一个字都没有」和「被截断」是同一类还是两类？二选一 + 理由
    
    
    finish_reason = response.choices[0].finish_reason
    content = response.choices[0].message.content 
    
    if not content or not content.strip():
        raise HTTPException(status_code=502,detail="上游返回了空内容")
    result = content.strip()
    #- 截断 → 拿到半截，还有阅读价值 → 200 + truncated=True
    #- 空 → 什么都没有 → 502
    if finish_reason == "length":
        # 选择：不报错，照常返回，但告诉调用方
        # 理由：这是模型的限制，调用方没做错什么，报错不合理。调用方可以根据 truncated 字段决定是否要提示用户。
        truncated = True
    else:
        truncated = False
    # ---- 4.4 算钱 ----------------------------------------------------
    # TODO: 真实 token / 成本 / 误差率，和 day2 的 report() 一样
    #       区别：不 print 了，print 到服务器日志里前端看不见，要放进返回值
    input_tokens = response.usage.prompt_tokens
    output_tokens = response.usage.completion_tokens
    cost =(input_tokens * PRICE_IN + output_tokens * PRICE_OUT) / 1_000_000
    
    global _calls_today
    _calls_today += 1  
    # ---- 4.5 按契约返回 ----------------------------------------------
    # TODO: return SummarizeResponse(...)
    return SummarizeResponse(
        summary=result,
        truncated=truncated,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cost=cost,
        model=MODEL
    )


# ---------------------------------------------------------------
# 【5】把前端挂进来（Day 4 · 外围，教练直接给）
# ---------------------------------------------------------------
# html=True → 访问 / 时自动返回 static/index.html
#
# ⚠️ 这三行必须写在文件最末尾，在所有 @app.get / @app.post 之后。
#    路由是**从上往下**匹配的，mount("/") 是一张通吃所有路径的网。
#    如果把它写在 /health 上面，请求 /health 会先被这张网捞走，
#    然后去 static/ 里找一个叫 health 的文件，找不到 → 404。
#    你的接口会「凭空消失」，而代码看起来一点毛病没有。
app.mount("/", StaticFiles(directory=BASE_DIR / "static", html=True), name="static") 
# FastAPI 把 static/ 文件夹(里面就是 index.html)挂在 8000 端口上。你在浏览器访问 http://127.0.0.1:8000 时,拿到的那张 HTML 页面,是 FastAPI 亲手递出来的。
    
#完整的流程 浏览器访问http://127.0.0.1:8000 → FastAPI 发出 index.html(页面住在 8000) → 页面里 fetch('/summarize')  → 浏览器补全成 http://127.0.0.1:8000/summarize → 请求又回到 8000 —— 页面和接口同源,浏览器不拦