"""
Day 6 · 代码注释生成器（综合训练）
==========================================

【今日目标】
做一个工具：输入一个 .py 文件路径 → 输出加好注释 + docstring 的新文件。

【这一天为什么重要】
它把 day1-day5 的所有技能都集成进来：
- 文件 I/O（读 .py 文件）
- 长输入处理（一个文件可能上千行 → token 超限）
- 结构化输出（必须保持代码可执行）
- 实用价值（你以后真的会用它处理老项目）

【今日新挑战：长上下文处理】
一个 1000 行的 Python 文件可能有 5000+ tokens。
有些模型上下文不够。即使够，也要考虑：
- 一次发太多 → 输出可能不全（max_tokens 限制）
- 分块发 → 每块的"上下文"怎么保留？

【启动 Claude Code 后，对它说】

    开始 day 6

【启动后建议先问】

    "如果一个 .py 文件 3000 行怎么办？分块策略有哪些？
     按函数切？按行数切？两者各有什么权衡？先不写代码，讨论方案。"

【在 demo_code/ 目录下放几个"原料文件"做测试】
- demo_code/no_comment.py  → 一段你自己写的、没注释的代码
- demo_code/legacy.py      → 一段你抄来的、看不懂的代码

让 Claude Code 帮你造一个故意写得不清楚的代码作为测试样本。

【需要实现的功能】
1. read_file(path) → 读源文件
2. add_comments(code) → 调 LLM 加注释，返回新代码
3. save_file(orig_path, new_code) → 保存为 orig_xxx_documented.py
4. validate(new_code) → 用 ast.parse 检查新代码语法是否合法
   （如果 AI 改坏了代码，validate 会发现）

【关键 Prompt 设计点】
system prompt 必须明确：
- 只加注释和 docstring
- 绝对不能修改任何代码逻辑
- 输出必须是完整可运行的 .py 内容
- 不要加任何说明性文字（如"以下是修改后的代码:"）

【加分项】
- 加 --check 模式：先 dry-run 显示 diff，确认后再写文件
- 自动备份原文件（orig.py → orig.py.bak）
- 支持批量处理整个目录
==========================================
"""

import os
import sys
import ast
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


SYSTEM_PROMPT = """
# TODO 1：写一个非常严格的 system prompt
# 重点：禁止修改逻辑、必须输出可执行代码、不要 markdown 包裹
""".strip()


def read_file(path: str) -> str:
    """
    TODO 2：读文件
    """
    # ← 你的代码


def add_comments(client: OpenAI, code: str) -> str:
    """
    TODO 3：调 LLM 加注释
    注意 max_tokens 至少要和 code 长度一样长
    """
    # ← 你的代码


def validate(code: str) -> bool:
    """
    TODO 4：用 ast.parse 检查代码合法性
    parse 失败说明 AI 改坏了，应该拒绝保存
    """
    try:
        ast.parse(code)
        return True
    except SyntaxError as e:
        print(f"❌ AI 输出的代码语法错误: {e}")
        return False


def save_file(orig_path: str, new_code: str) -> str:
    """
    TODO 5：保存到新文件
    例如 foo.py → foo_documented.py
    返回新文件路径
    """
    # ← 你的代码


def main():
    if len(sys.argv) < 2:
        print("用法: python day6_code_doc.py <文件路径>")
        sys.exit(1)

    path = sys.argv[1]

    """
    TODO 6：组合上面所有步骤
    1) 读文件
    2) 调 LLM
    3) validate
    4) 保存
    5) 打印结果
    """
    # ← 你的代码


if __name__ == "__main__":
    main()


# ============================================
# 完成检验：
# 1. 自己写一段 50 行没注释的代码，跑这个工具，看注释加得好不好
# 2. 故意给它一段不合法的 Python（缺括号），看 validate 是否拦下
# 3. 让 Claude Code 给你"造 bug"：
#    "请你帮我在我的 day6_code_doc.py 里故意制造 2 个隐蔽 bug，
#     不要告诉我在哪，我自己找。"
#    （这是反向训练你 debug 的能力）
# ============================================
