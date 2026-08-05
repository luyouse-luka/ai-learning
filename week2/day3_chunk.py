"""
Day 3 · 切块策略：chunk size 与 overlap

╔══════════════════════════════════════════════════════════════════════╗
║  ⏸  2026-07-31 暂停，移交阶段 3（RAG · 第 7-12 周）                  ║
╠══════════════════════════════════════════════════════════════════════╣
║  原因：切块（Split）是《AI 学习深化指南》里 RAG 六步链路的第 2 步。  ║
║        在第 2 周做它，脱离了它唯一的用途——让检索召回精准片段。      ║
║        变成一个没有场景的纯算法练习，所以 ly 觉得「莫名其妙」。      ║
║                                                                      ║
║  已完成、保留：load_pdf() / split_text()  ← 写得对，阶段 3 直接复用   ║
║  verify_chunks()：ly 写了一半，有 2 个 bug（判断反转 + 恒等式漏项）， ║
║                   已在对话里批过，暂不修，阶段 3 重做                 ║
║  不再写：estimate_map_cost() / summarize_one_chunk()                  ║
║                                                                      ║
║  阶段 3 重做时的正确起点（指南直接给了，不用自己论证）：             ║
║      chunk_size = 500-1000 字，chunk_overlap = 10-20%                 ║
║      实际项目用 LangChain 的 RecursiveCharacterTextSplitter          ║
║      （指南原话：「性价比之王」）——手搓一遍只为理解它在干什么       ║
║                                                                      ║
║  完整复盘见 week2/README.md「教练自查（Day 3）」+「路线偏差修正」    ║
╚══════════════════════════════════════════════════════════════════════╝

⚠️ 下面【0】里那四条「约束」是教练倒着写出来的（先有 4000 再编依据），
   已在 README 里逐条拆过，**别当学习材料看**。保留是为了留个错误样本。

原任务：把 attention.pdf 切成带 overlap 的块，证明没丢内容，
       并算出「切块之后再逐块处理」要花多少钱 —— 和 Day 2 的 Stuff 对比。

ly 的预测（保留）：切块处理的总成本比 Day 2 的 Stuff（$0.00152）**更贵 20%**
                  ← 这个预测没验证，等阶段 3 重做时再算
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

# ---------------------------------------------------------------
# 外围（教练直接给，不是考点）
# ---------------------------------------------------------------
BASE_DIR = Path(__file__).parent
PDF_PATH = BASE_DIR / "attention.pdf"

load_dotenv(BASE_DIR.parent / ".env")

MODEL = "deepseek-v4-flash"       # ← 常量。今天默写你又写回硬编码了，注意
PRICE_IN = 0.14                   # $ / 1M token（缓存未命中）
PRICE_OUT = 0.28                  # $ / 1M token
EST_RATIO_EN = 0.3                # 英文字符 → token（官方；昨天实测 0.256，偏安全）
EST_RATIO_CN = 0.6                # 中文字符 → token（官方；昨天实测 0.55）

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)   


# ---------------------------------------------------------------
# 【0】今天你要定的两个数 —— 定完必须说得出依据
# ---------------------------------------------------------------
# CHUNK_SIZE（单位：字符）—— 四个约束夹出来的
#   上界·窗口              : 4000 字符 ≈ 1200 token，1M 窗口完全不是瓶颈 → 忽略
#   上界·lost-in-the-middle: 经验区间 1000-2000 token 一块 → 压到 ≈6000 字符
#   下界·语义完整          : attention.pdf 一个小节 2000-4000 字符，一块至少装得下一节 → ≈3000
#   下界·重复开销          : 块数 = 全文 ÷ step，size 越小块数越多，system prompt 重发越多次
# 3000-6000 取中：
CHUNK_SIZE = 4000

# CHUNK_OVERLAP（单位：字符）—— 按「要盖住什么」定
#   断句            : 几十字符够
#   跨块代词(it 指谁): 要看到那句话的主语，一两句话 → 200-300
#   上一段的论点前提 : 一个自然段的量级 → 300-500
# 记比例不记数字：overlap 取 chunk_size 的 10%-20%。
#   <10% 盖不住跨段线索；>20% 重复付费和重复要点都开始明显。
CHUNK_OVERLAP = 400          # = CHUNK_SIZE 的 10%，也就是输入费要多付 10%


# ---------------------------------------------------------------
# 【1】读 PDF —— Day 2 写过，直接沿用（不重复考）
# ---------------------------------------------------------------
def load_pdf(path):
    """读 PDF 全文，返回一个字符串。"""
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"
    return text


# ---------------------------------------------------------------
# 【2】切块 —— 今天的核心。三颗雷埋在里面，自己踩
# ---------------------------------------------------------------
def split_text(text, chunk_size, overlap):
    """把 text 切成带 overlap 的块，返回 list[str]。"""
    # 雷 1：overlap >= chunk_size 时 step <= 0，start 永不前进 → 死循环吃内存。
    #       它不抛异常，所以必须自己在门口拦：让它「早崩、响亮地崩」。
    if overlap >= chunk_size:
        raise ValueError(f"overlap({overlap}) 必须小于 chunk_size({chunk_size})，否则 start 不前进")

    step = chunk_size - overlap      # 每次窗口往前挪多少（不是 chunk_size！）
    chunks = []
    start = 0                        # 累加变量在循环外（你踩过三次的坑）

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])

        # 雷 2 + 雷 3 都靠这两行解决：
        #   已经切到文末了就立刻停，不要再挪 start。
        #   少了它 → 会多出一个只有 12 字符、且完全被上一块包含的冗余尾块，
        #            它会带着一份 system prompt 去调一次 API，花钱换回废话。
        if end >= len(text):
            break
        start += step

    return chunks


# ---------------------------------------------------------------
# 【3】证明切块没出错 —— 今天的新要求
# ---------------------------------------------------------------
def verify_chunks(text, chunks, chunk_size, overlap):
    """用【可计算的等式】证明切块正确。不许靠眼睛看。"""
    # TODO: 至少写出三个检查，每个都要能输出 True / False：
    #
    #   ① 没丢也没多：chunks 和原文之间存在一个精确的恒等关系。
    #      提示：overlap 部分被重复计入了 —— 把重复的那部分从每块开头
    #            扣掉再拼起来，应该精确等于原文。写成一个 == 表达式。
    #
    #   ② overlap 真的存在：相邻两块之间确实重叠了，而且长度正好是 overlap。
    #      提示：chunks[i] 的尾巴和 chunks[i+1] 的头，应该是同一段字符串。
    #      ⚠️ 最后一块是例外吗？想一下。
    #
    #   ③ 没有空块，且每块长度都 <= chunk_size。
    #
    # 检查不通过时要【明确打印哪一条挂了】。
    # 打印一句「验证通过」然后什么都没查，是今天最该避免的写法。
    sum=0
    for c in chunks:
        sum += (len(c) - overlap) 
        if c =="" and len(c)<= chunk_size:
            print("True")
        else: print("Flase")
    if sum==len(text): 
        print("True")
    else: print("False")        

    
    pass


# ---------------------------------------------------------------
# 【4】花钱之前先算钱 —— 你短板的第三次验收
# ---------------------------------------------------------------
def estimate_map_cost(chunks, system_prompt, out_chars_per_chunk):
    """估算「每块调一次 API」总共要花多少钱。"""
    # TODO: 算出并打印：
    #     - 总输入 token（⚠️ N 块 = N 次调用，system prompt 要重发 N 遍）
    #     - 总输出 token（每块都会吐一段总结，用中文比例算）
    #     - 总成本（输入输出分开、各乘各的单价）
    #
    # ⚠️ 昨天那颗雷今天引爆：Day 2 的估算漏算了 SYSTEM_PROMPT。
    #    正文 4 万字符时它 <1% 看不出来；一块 4000 字符时它就 2%，
    #    还要 × 块数。今天必须算进去。
    #
    # 算完回答两个问题（写在下面注释里）：
    #   Q1: 这个数和 Day 2 的 Stuff（$0.00152）比，是大还是小？
    #       和你在文件开头写的预测一致吗？
    #   Q2: 如果 overlap 翻倍，这个数怎么变？如果 CHUNK_SIZE 翻倍呢？
    #       两个方向为什么不一样？
    
    pass


# ---------------------------------------------------------------
# 【5】看一眼「块内视野」的代价 —— 只调 1 次 API，成本可忽略
# ---------------------------------------------------------------
SINGLE_CHUNK_PROMPT = """
TODO: 写一个「只总结这一块」的 system prompt。
      和 Day 2 那个全文总结的 prompt 有什么必须不一样的地方？
      提示：这一块的模型看不到前后文。你要不要告诉它这件事？
            要不要允许它说「这里提到的 it 我不知道指谁」？
"""


def summarize_one_chunk(chunk):
    """拿其中一块调一次 API，返回 (总结, response)。"""
    # TODO: 和 Day 2 的 summarize() 同构，自己写一遍（默写题）
    #
    # ⚠️ Day 2 你有、今天默写丢掉的那两样，补回来：
    #     - MODEL 用常量，不硬编码
    #     - finish_reason 要检查，别把残缺内容当成品
    pass


# ---------------------------------------------------------------
# main
# ---------------------------------------------------------------
if __name__ == "__main__":
    # TODO: 读 PDF，打印总字符数
    #
    # TODO: 切块，打印块数 + 每块长度
    #
    # TODO: 跑 verify_chunks —— 挂了就该在这里停住，别往下走
    #
    # TODO: 跑 estimate_map_cost，和 Day 2 的 $0.00152 摆在一起对比
    #
    # TODO（可选，只花 ~$0.0002）：挑中间的一块跑 summarize_one_chunk，
    #       把结果和 day2_summary.json 里的全文总结放一起读。
    #       重点看：这一块的总结里，有没有它其实不知道、但说得很肯定的东西？
    pass
