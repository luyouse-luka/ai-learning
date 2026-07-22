"""
Day 4 · 参数实验
==========================================

【今日目标】
不再"调出一个像样的回复"，而是"故意调出 5 种不同风格"，
亲眼看见每个参数对输出的影响。

【今天主要参数清单】
- temperature  : 0-2，控制随机性。0=确定，1=平衡，2=极度发散
- top_p        : 0-1，核采样阈值。和 temperature 不要同时调
- max_tokens   : 限制单次回复最大长度
- frequency_penalty : -2 到 2，避免重复词
- presence_penalty  : -2 到 2，鼓励引入新话题

【今日不是"学功能"，是"做实验"】
按下面的实验设计跑一遍，记录结果。

【实验设计】
固定 prompt：'用 50 字写一段关于秋天的散文。'
固定 model：deepseek-chat

实验组：
1. temperature=0.0
2. temperature=0.5
3. temperature=1.0
4. temperature=1.5
5. temperature=2.0（极端值）

每个跑 3 次，看输出是否每次都不同。
然后做对照：
6. temperature=0.0 跑 3 次 → 应该非常相似甚至一样
7. temperature=2.0 跑 3 次 → 应该差异极大，甚至失控

【启动 Claude Code 后，对它说】

    开始 day 4

【启动后建议先问 Claude Code】

    "temperature 在底层是怎么影响 token 采样的？
     temperature=0 真的能保证每次输出一样吗？为什么？
     先讲原理，不要给代码。"

【需要实现的功能】
1. 一个函数 run_experiment(temp, prompt, runs=3) 返回 runs 次的输出列表
2. 一个主流程跑 5 组温度，把所有结果存入 results.json
3. 打印一个简洁的对比表格

【加分项】
- 把 5 组结果保存到 results/ 目录下，每组一个 markdown 文件
- 用 difflib 计算同组 3 次输出的相似度，可视化"随机性"
==========================================
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def run_experiment(client, temperature: float, prompt: str, runs: int = 3) -> list[str]:
    """
    TODO 1：跑 runs 次同样的 prompt，返回 runs 个回复
    每次调用都传同样的 temperature
    """ 
    results = []
    for _ in range(runs):
        response = client.chat.completions.create(model="deepseek-chat", messages=[{"role":"user","content":prompt}],temperature=temperature)
        result = response.choices[0].message.content.strip()
       
        results.append(result)
    # ← 你的代码
    return results


def main():
    """
    TODO 2：初始化 client
    """
    client = OpenAI(api_key= os.getenv("DEEPSEEK_API_KEY"),base_url=os.getenv("DEEPSEEK_BASE_URL"))  # ← 你的代码

    prompt = "用 50 字写一段关于秋天的散文。"
    temperatures = [0.0, 0.5, 1.0, 1.5, 2.0]

    """
    TODO 3：循环跑实验，把结果保存到字典
    格式：{"temp_0.0": [out1, out2, out3], "temp_0.5": [...], ...}
    """
    all_results = {}
    for temp in temperatures:
        all_results[f"temp_{temp}"] = run_experiment(client, temp, prompt)  # ← 你的代码
    # ← 你的代码

    """
    TODO 4：把 all_results 存到 results.json
    json.dump 时记得 ensure_ascii=False，indent=2
    """
    # ← 你的代码
    with open("results.json","w",encoding="utf-8") as f: #with 语句自动帮你 close / open 文件 w/r 读或写  encoding="utf-8"——你存的是中文散文，文件对象f
        json.dump(all_results,f,ensure_ascii=False,indent=2)   #json.dump：怎么把字典写成 JSON 
                                                               #ensure_ascii=False：不加的话中文会被转成 \u79cb\u5929 这种逃逸码，加了才是人能读的                 
                                                               #indent=2：缩进2个空格，便于阅读
    """
    TODO 5：打印对比表格（每组只打第一条，便于肉眼对比）
    """
    # ← 你的代码
    for temp, outs in all_results.items():
        print(f"{temp}: {outs[0]}\n")  # 打印每组的第一条结果，便于对比

if __name__ == "__main__":
    main()


# ============================================
# 完成后：
# 1. 把 results.json 贴给 Claude Code，让它帮你分析
# 2. 在 README.md "关键概念笔记 - temperature" 部分用自己的话写一段
# 3. 思考：哪些场景适合 temperature=0？哪些适合 1.5+？
# ============================================
