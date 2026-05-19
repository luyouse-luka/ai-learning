# LLM API Week 1 学习日志

> 目标：7 天从零掌握 LLM API 调用全流程，每天产出可运行代码 + 复盘笔记。
> 配套：`/home/ly/project/screen-ai-deepdive.pdf` 第二章
> 教学合约：见 `CLAUDE.md`

---

## 准备工作（Day 0，建议 30 分钟内完成）

- [ ] 注册 DeepSeek 账号：https://platform.deepseek.com
- [ ] 充值 10 元（够用 1 个月以上）
- [ ] 获取 API Key
- [ ] 复制 `.env.example` 为 `.env`，填入真实 key
- [ ] 安装依赖：`pip install -r requirements.txt`
- [ ] 读完 `CLAUDE.md`（5 分钟）

```bash
cp .env.example .env
# 编辑 .env 填入真实 key
pip install -r requirements.txt
```

---

## 7 天进度表

| Day | 主题 | 文件 | 状态 | 耗时 |
|---|---|---|---|---|
| 1 | Hello World 第一次调用 | `day1_hello.py` | ☐ |  |
| 2 | messages 多轮对话 | `day2_chat.py` | ☐ |  |
| 3 | 流式输出 streaming | `day3_stream.py` | ☐ |  |
| 4 | 参数实验（temperature 等）| `day4_params.py` | ☐ |  |
| 5 | AI 翻译工具 | `day5_translate.py` | ☐ |  |
| 6 | 代码注释生成器 | `day6_code_doc.py` | ☐ |  |
| 7 | 复盘 + 综合考核 | `day7_review.md` | ☐ |  |

---

## 每日复盘模板（每天结束花 5 分钟写）

复制下面模板，填入每天的实际内容。

```markdown
### Day N · 2026-MM-DD

**今天学到的最关键 1 件事**：
（一句话）

**最难的点 / 卡了多久**：

**踩的坑**：
1. 
2. 

**Claude Code 帮到我的方式**（具体例子）：

**明天开始前要复习的 1 个概念**：

**今天的 Claude Code 出题得分**：__/3
```

---

## 每日复盘记录

> ⬇️ 每天结束后向下追加，不要修改之前的记录

### Day 1 · 待填

（开始 day 1 时把"### Day N"这行复制下来填）

---

## 关键概念笔记（用自己的话写）

> ⚠️ 不要直接复制 AI 的解释。必须用自己的话写一遍。

### messages 数组

（待填）

### token

（待填）

### temperature

（待填）

### streaming

（待填）

### system prompt 的作用

（待填）

---

## 收藏的好 prompt（积累自己的 prompt 库）

| 场景 | Prompt | 效果 |
|---|---|---|
| | | |

---

## Week 1 结束自检（Day 7 填）

- [ ] 能解释 messages / role / token / temperature 的作用
- [ ] 能不查文档写出一个流式对话脚本
- [ ] 理解为什么模型"没有记忆"（无状态）
- [ ] 能估算一次调用的 token 数与成本
- [ ] 至少做出 2 个自己真的会用的小工具

---

## 下一周的准备

完成 Week 1 后，转入 Week 2（综合实战）：
- PDF 总结器
- 邮件起草助手
- FastAPI 接口化
- 部署到云服务器

但**只有 Week 1 自检全部 ☑ 才能进入 Week 2**。
