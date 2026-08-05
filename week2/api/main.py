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

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from pydantic import BaseModel, Field
from pypdf import PdfReader
from pathlib import Path

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

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
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
    # TODO: 三条校验，各自 raise HTTPException
    #       外围提示（语法直接给，你只管想「哪一条配哪个码」）：
    #           raise HTTPException(status_code=400, detail="说人话的原因")
    #       ⚠️ 想清楚每一条到底是「调用方的错」还是「我的错」→ 决定 4xx 还是 5xx
    #       ⚠️ c) 的阈值先随便给一个你觉得合理的数，写上你的理由，跑完看数据再调
    #          （规则 7：先做后定，不要求你现在论证）

    # ---- 4.2 调模型 --------------------------------------------------
    # TODO: messages 构造 + client.chat.completions.create(...)
    #       和 day2 一模一样，别看 day2_summarize.py，先默写
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": text}
    ]
    response = client.chat.completions.create(model=MODEL, messages=messages, max_tokens=MAX_OUTPUT_TOKENS)
    result = response.choices[0].message.content.strip()
    # ---- 4.3 检查它是怎么停下来的 ------------------------------------
    # day2 的遗留：你只 print 了 finish_reason，没有「检查」。
    # 打印 ≠ 检查。在脚本里没人看见，在服务里 = 用户拿到半截总结当成品。
    #
    # TODO: finish_reason == "length" 时怎么办？
    #       想清楚：这是谁的错？该返回什么码？还是说……不该报错，而是照常返回但告诉调用方？
    #       （这题没有唯一答案，写下你的选择和理由，我批）
    finish_reason = response.choices[0].finish_reason
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
    
