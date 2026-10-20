# AI Workstation

PDF 总结应用与全栈 / AI 学习记录。教学合约见 [week1/CLAUDE.md](week1/CLAUDE.md)，当前学习进度见 [LEARNING-PLAN.md](LEARNING-PLAN.md)。

## 当前目录

```text
frontend/       Vue + TypeScript + Pinia 应用
backend/        FastAPI 服务、Prompt 实验和原生 HTML 对照页
week1～week4/   按周保留的学习记录、练习及样本
tools/          可复跑验证脚本
.env            本地模型配置，Git 忽略
.venv/          本地 Python 环境，Git 忽略
```

2026-10-20 目录迁移：`week3/frontend/` → `frontend/`，`week2/api/` → `backend/`。旧学习日志里的路径对应当时目录，阅读时按此映射；课程周数与应用目录分开管理。

## 本地启动

前端：在仓库根打开 PowerShell，执行：

```powershell
cd frontend
pnpm install --frozen-lockfile
pnpm dev
```

默认地址为 `http://localhost:5174/`，以终端实际输出为准。项目沿用锁定的 Node / pnpm 配置，详见 [frontend/README.md](frontend/README.md)。

后端：在另一个位于仓库根的 PowerShell 中，使用已有本地环境：

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

新环境先执行 `python -m venv .venv` 和 `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`，再根据 `.env.example` 配置根目录 `.env`。前端 `/api/*` 继续代理至本地 8000 端口。

## 验证

在前端目录运行 `pnpm build`，执行类型检查和生产构建。

在仓库根运行：

```powershell
.\.venv\Scripts\python.exe tools\verify_workspace_layout.py
```

该检查覆盖新目录入口、根配置位置、Prompt 样本和输出路径，以及健康检查、静态页和两类无模型调用的上传校验。真实 PDF 总结和浏览器交互须另行验收。

## Prompt 对照实验

入口为 `backend/prompts.py`，样本仍在 `week2/attention_extracted.txt`，结果仍写入 `week4/`。执行 `.\.venv\Scripts\python.exe -m backend.prompts` 会调用模型，按当天学习任务运行。
