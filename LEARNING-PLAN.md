# 学习总清单 · LEARNING-PLAN

> 全部条目逐项取自仓库根的三份路线 PDF，出处标在每节标题后。
> 出处代号：**`[总纲]`** = `screen.pdf`（15 页，根）／**`[FS]`** = `screen-fullstack-deepdive.pdf`（24 页）／**`[AI]`** = `screen-ai-deepdive.pdf`（17 页）
>
> 建立于 2026-08-05（Week 2 Day 4 进行中）。**这份文件是活的，边学边改。**

---

## 0. 怎么用这份清单

### 状态记号（改这一个字符就行）

| 记号 | 含义 | 要求 |
|---|---|---|
| `[ ]` | 未开始 | — |
| `[~]` | 进行中 | — |
| `[x]` | 完成 | **后面跟证据**：文件名 / commit / 一句话结论 |
| `[-]` | 跳过或作废 | **必须写原因**，不写原因的跳过=自欺 |
| `[!]` | 卡住 | 写卡了多久。**满 1 小时提醒、满 2 小时必停** `[FS §八]` |

### 调整规则（防止清单变成摆设）

1. **可以改，但要留痕** —— 任何顺序调整、砍项、加项，都在文末 §11 调整日志记一行。
2. **砍项要过一道判据**：这一项是「2026 年还要手写的」还是「已被库吃掉、只为理解原理」？后者跑通一次即可，不深挖。（教学合约规则 8）
3. **不许压缩周期** —— PDF 给 4-6 周的，不许排成 1 周。夹生过一次了（Week 2 Day 3 翻车根因）。
4. **每周至少一个能发出去的产出** `[总纲 §九]`；`[AI §一]` 说得更狠：**学了不输出 = 没学**。
5. 每个主题动手前问一句：**这东西怎么接进我手上真实的项目**。答不出就说明选题不够具体。
6. **外部建议不直接入清单**（2026-08-06 加）—— 别处看来的路线图、别的 AI 给的排序，
   先过 §11 末「外部建议的三道筛选判据」。**「随时代即时调整」只作用在工具选型，不作用在原理层。**

### 每次会话的入口

Claude Code 在本目录工作时读 `week1/CLAUDE.md`（教学合约）→ 再读本文件 §1 看当前位置。

---

## 1. 当前位置

> **每完成一天就改这一节。** 其余各节只打勾，不动结构。

| 轨道 | 位置 | 说明 |
|---|---|---|
| **主线**（总纲 9 个月） | 阶段一 · **已开工**（08-07 Day 6） | 工具链就位：nvm + Node **v24.19.0** + pnpm 11.20 + `week3/frontend/`（Vue 3.5 / Vite 8.2 / TS 6.0）。阶段二只碰了 FastAPI 皮毛，阶段三反而超前 |
| **AI 线**（可并行） | 阶段 1 · **收尾** | 14 天清单 Day 1-13 ☑（Day 14 部署暂缓）。「附·AI 工程化生产实践」的护栏 **08-07 已补齐**（超时 / 502·504 / 日调用上限 / 空 summary），之后进阶段 2 |

**已确认的路线偏差**：week1 + week2 直接做了阶段三，**跳过阶段一整个、阶段二大部分**。
内容一行没白学，**错的是顺序**。修正方案 C（08-05 拍板）：用 Vue 3 + TS 重写 week2 PDF 总结服务的前端，当阶段一的练手项目。

**本周（Week 2）剩余**：

- [x] Day 4 原生 HTML 前端（对照组）—— `week2/api/static/index.html` 5 块 TODO 全填完，端到端跑通（含 400/413/422 + truncated 截断实测）。**已 commit**（`904c04d` + `e43c7f2`）
- [x] Day 5 AI 线阶段 1 护栏 + 还 Day 3 的债 —— `main.py` 四块全落地（超时 60s / 502·504 映射 / 日调用上限 / 空 summary 返 502），教练四条验证实测全绿（08-07）。**已 commit**（08-08）
- [x] Day 6 Week 2 收尾 + 阶段一开工准备 —— 环境（教练装，属外围）：nvm / Node v24.19.0 / pnpm 11.20 / `week3/frontend/` 跑通，dev server 685ms 起在 **5174**（5173 被本机别人的服务占了）。
      **ly 两件动手均完成**：① 启动链路（答案断两环、位置答反，已订正；判据 = `grep HomeView src/App.vue` 搜不到 → `<RouterView/>` 是占位符不是引用）
      ② HMR 三条判据全中，中途撞上一次 **HMR 失败**，暴露出教练的判据表只有两列、漏了第三种状态。**已 commit**（08-08）
- [ ] Day 7 巩固日：不看答案重写本周核心 + Week 2 总复盘 + Week 3 计划 + 目录重构

**当前瓶颈（教练盯的三条）**：

1. **知道了没调用**（已第五次）—— 答案就在自己写过的文件里，不翻。判据：做决定时那个文件有没有被打开过
2. **静默 bug 意识**（本周重点）—— Day 5 有实测进展（空 summary 的 502 亲手堵上、亲眼见到它触发），
   但 Day 5 复盘 Q1 仍漏答「日志里会不会报错」那一问。**认得出形状 ≠ 想得起来查**
   → Day 6 换了个壳又出现一次：HMR「滚动没变 + 日志还在」两条全绿，实际热更新失败了。
   **统一表述：「没有 A」不等于「有 B」——负向判据证明不了正向结论，判据必须直接测你要证的那件事。**
   （这次是教练的判据表漏了第三列，不是 ly 观测错；但形状与瓶颈 2 完全一致，合并记在这）
3. **变量作用域**（已第四次）—— 同一条规则的四张脸：循环 → `if` 分支 → 函数边界（`+1` 写进 `check_` 里）
   → **`global` 声明的覆盖范围**（删了名字但 `if` 分支里还有 `= 0` → 全新进程首次调用 500 `UnboundLocalError`）。
   **判据：函数里对某个名字有任何赋值（`=` / `+=` / `for x in`）就必须 `global` 声明，不管那行会不会执行到**

**已过的关**：messages 结构、拼写、成本计算（连续两轮全对）。

---

## 2. 阶段一：现代前端工程化 `[总纲 §二]` + `[FS §二]`

> **周期 0-3 月** · 目标：能独立写出一个前端页面，组件化开发，TypeScript 无压力，会用 Git 协作。
> ly 的起点 = Week 3。**这是本次修正的重点，一项都不许跳。**

### 为什么必学（说服自己用）`[FS §二]`

> 2026 年所有前端岗都默认要求 Vue/React + TS + Vite。**即使你做 WordPress / 切图，懂工程化 = 工资上限直接翻倍。**
> 而总纲 §五岗位表第一行「AI 应用工程师 ｜ LLM API 集成 + **全栈** + Prompt 工程 ｜ 25-45 万」——**「全栈」写在岗位要求里**。

从「切图仔」到「前端工程师」的跨越 = 五化：组件化（复用 UI）／响应式（数据驱动 DOM）／模块化（一个文件一个职责）／类型化（编辑器和 CI 帮你抓 bug）／工具化（自动构建、热更新、Tree-shaking）。

### 第 1 个月：工程化基础 `[总纲 §二]`

- [ ] **Git & GitHub** —— 分支管理、PR、代码回滚。每天提交代码
  - [ ] 过一遍 Learn Git Branching（交互式，learngitbranching.js.org，1 小时掌握 90% 用法）
  - [ ] 个人开发必会 12 命令 `[FS §六]`：`status`/`log --oneline`、`diff`/`diff --staged`、`add -p`（分块提交）、`commit --amend`、`stash`/`stash pop`、`reset HEAD~1`、`rebase -i HEAD~5`、`cherry-pick`、`reflog`（后悔药）、`tag v1.0.0`、`remote -v`/`fetch`、`branch -d`/`-D`
  - [ ] 分支策略选一个：Trunk-Based / Git Flow / **GitHub Flow（团队 10 内最简洁，事实标准）** / GitLab Flow
  - [ ] Commit 规范 Conventional Commits：`<type>(<scope>): <subject>`，type = feat/fix/docs/refactor/test/chore
- [x] **Node.js 环境** —— nvm v0.40.3 + Node **v24.19.0**（`nvm alias default`）+ pnpm **11.20.0**（corepack）· 08-07 Day 6
  - ⚠️ 装的时候踩到：`~/.npmrc` 里 `prefix=` 与 nvm **互斥**，`nvm use` 会直接拒绝生效（已注释，备份 `~/.npmrc.bak-20260807`）
  - **npm vs pnpm 的两个差别**：① 硬链接共享全局 store（12.7s 装完 40+ 包）② **幽灵依赖** —— npm 扁平化让你能 `import` 没在 `package.json` 声明的包，换机器就炸；pnpm 声明了才 import 得到
- [~] **Vite** —— 比 webpack 快 10-100 倍（原生 ESM + 按需编译），Vue3/React 标配。**dev 不打包 / 生产用 Rollup 打包，是两套机制**
  - [~] 必须会的 5 件事 `[FS §二]`：① **`npm create vue@latest` 建项目 ✅ 08-07**（`week3/frontend/`，Vite 8.2.0 冷启动 685ms）② 配代理（`vite.config.ts` 的 `server.proxy` 解决跨域）← **Week 3 第一件会撞的事**，前端 5174 调后端 8000 ③ 环境变量（`.env.development` / `.env.production`）④ 别名（`@` → `src`）⑤ 生产打包 `npm run build` → `dist`
- [ ] **TypeScript 基础** —— 目标：能把现有 JS 代码加上类型，消除 `any`。配 TS Playground 在线练
  - [ ] TS 8 大核心 `[FS §二]`：① 基本类型注解（能省则省，TS 会推断）② `interface` vs `type`（描述对象形状用 interface）③ 联合类型 `|`（`type Status = "loading"|"ok"|"error"`，替代 enum）④ 可选 `?` 与默认值 ⑤ 泛型（Array、Promise 最常见）⑥ `as` 类型断言（避免滥用，杀手锏但杀的是自己）⑦ 内置工具类型 `Partial`/`Required`/`Pick`/`Omit`/`Record` ⑧ 严格模式 `strict: true`（一开始报错多，但避免 90% 运行时 bug）

### 第 2 个月：Vue 3 核心 `[总纲 §二]` + 推荐学习顺序 `[FS §二]`

> **按这个顺序学，避免乱学。** 每条后面是「新手最容易错的点」。

- [ ] 1. **响应式 ref vs reactive** —— `ref` 用于基本类型，`reactive` 用于对象。**混用是新手最大错误源**
- [ ] 2. **模板语法 v-if / v-for / v-model** —— `v-for` 必须加 `:key`（用 id 不要用 index）；**`v-if` 与 `v-for` 不要同级**
- [ ] 3. **组合式 API setup + computed + watch** —— computed 是缓存的，watch 是副作用。**能用 computed 就别用 watch**
- [ ] 4. **组件通信 props / emit / provide-inject** —— 父子用 props/emit，跨层用 provide/inject，全局状态用 Pinia
- [ ] 5. **生命周期钩子** —— `onMounted`（DOM 已挂载）和 `onBeforeUnmount`（清理）最常用
- [ ] 6. **路由 Vue Router 4** —— 懒加载组件 `(() => import)`、路由守卫、动态参数
- [ ] 7. **状态管理 Pinia** —— 比 Vuex 简单 10 倍。`defineStore` + state/getters/actions 三件套
- [ ] 8. **异步组件 + Suspense** —— 大组件懒加载，配骨架屏显著提升首屏体验
- [ ] **Axios HTTP 请求** `[总纲 §二]`

**本月实战** `[总纲 §二]`：做一个「待办事项」应用——组件拆分 / 路由跳转 / 状态持久化到 localStorage。
> ⚠️ **ly 的替代方案（08-05 拍板，方案 C）**：改用 **week2 的 PDF 总结服务前端**。
> 依据 `[FS §一]`「带用途感学，差距 3-5 倍」。总纲的待办事项是纯前端 demo 无真后端；
> 而 PDF 服务已有真接口、6 字段契约、4 类错误码、5.78s 异步等待、文件上传——**待办事项练不到这些**。
> 原生 HTML 版（Day 4 产物）留作对照组，不作废。

### 第 3 个月：CSS 进阶 + 工程实战 `[总纲 §二]`

- [ ] **Flex & Grid** —— 彻底掌握，能还原任何设计稿布局。推荐 Flexbox Froggy + Grid Garden 游戏练习
- [ ] **Tailwind CSS** —— 2026 前端标配，不写自定义 CSS，直接用工具类组合
  - [ ] 必背 30 个类 `[FS §二]`：`flex` / `items-center` / `justify-between` / `gap-4` / `p-4` / `m-4` / `w-full` / `h-screen` / `text-sm` / `text-gray-600` / `bg-white` / `rounded-lg` / `shadow` / `border` / `hover:` / `md:` / `lg:`
  - [ ] 响应式断点：**移动优先**，默认样式给手机，`md:`/`lg:` 加桌面覆盖（`class="w-full md:w-1/2"`）
  - [ ] 避坑三条：① 不要混用 Tailwind + 大量自定义 CSS ② 重复组合用 `@apply` 抽取或直接做组件 ③ `tailwind.config.js` 设计 token 一次，全项目复用
- [ ] **响应式设计** —— 移动端优先、媒体查询、rem/vw 单位
- [ ] **前端工程化必备 5 件套** `[FS §二]`
  - [ ] ESLint（配 vue 推荐规则 + ts 推荐规则，保存自动 fix）
  - [ ] Prettier（统一缩进、引号、分号）
  - [ ] Husky + lint-staged（commit 前自动跑 ESLint+Prettier，脏代码进不了仓库）
  - [ ] Commitizen（规范 commit message，便于自动生成 changelog）
  - [ ] VitePWA / Compression（gzip 压缩、PWA 离线支持，部署前打开）

### 🎯 阶段一结束检验（两份文档合并，全部打勾才算过）

`[总纲 §二]`：
- [ ] 能用 Vue 3 + TypeScript + Vite 从零搭起一个项目
- [ ] 能拆分组件，会用 Pinia 管理跨组件状态
- [ ] 能调用后端 API 并在页面展示数据
- [ ] 代码提交到 GitHub，有清晰的 commit 记录
- [ ] 页面在手机上显示正常（响应式）

`[FS §二]` 补充：
- [ ] 能用 Vue 3 Composition API 写出**可复用**的组件
- [ ] 会用 TypeScript 给组件 props / 函数参数加类型，**不写 any**
- [ ] 能用 Pinia 管理跨组件状态，**会处理异步 action**
- [ ] 配过 Vite 代理解决跨域，会配置环境变量
- [ ] 用 Tailwind 做出在手机和桌面都好看的页面（移动优先）
- [ ] 至少完整部署过 1 个项目（**有公网 URL**）

---

## 3. 阶段二：后端服务化 + 数据库进阶 `[总纲 §三]` + `[FS §三]`

> **周期 3-6 月** · 目标：能写出一套完整的 RESTful API，前后端联调跑通，数据存 MySQL，会用 Redis 缓存，代码能用 Docker 打包运行。
> ⚠️ **红线：JWT / Docker / 数据库补完之前，`/summarize` 服务不许真正公开到公网**（现在零鉴权，挂上去谁都能烧 API 额度）。

### PHP → Python/FastAPI：你的优势与转换点 `[FS §三]`

| 维度 | PHP（已有） | Python + FastAPI（要学） |
|---|---|---|
| 运行模型 | 每请求新进程（短生命周期） | **常驻进程**（长生命周期）→ 可以缓存、定时任务、长连接 |
| 类型系统 | 弱类型 + 运行时检查 | 静态类型 TypeHints + Pydantic 强校验，**Bug 少 70%** |
| 异步模型 | 同步阻塞 | `async/await` 原生异步，一个进程处理上千并发 |
| ORM | Laravel Eloquent / Doctrine | SQLAlchemy（更强大但学习曲线略陡） |
| 模板引擎 | Blade / Twig | **前后端分离，后端只输出 JSON，不再写模板** |
| 部署 | Apache/Nginx + PHP-FPM | Docker + Uvicorn/Gunicorn + Nginx 反代 |

### 第 4 个月：Python 进阶 + FastAPI `[总纲 §三]`

- [ ] **Python 进阶** —— 装饰器、生成器、异步 `async/await`、类型提示 `typing`（这些是 FastAPI 的基础，也是 AI 工具链的必备）
- [ ] **FastAPI 核心** —— 官方文档是业内最好的，全英文读一遍值得
  - [ ] 8 大核心特性 `[FS §三]`：① 路径操作装饰器 `@app.get("/users/{id}")` ② Pydantic 数据校验（客户端瞎传立刻报 422）③ **依赖注入 Depends**（FastAPI 灵魂特性，把「获取当前用户/数据库连接」封装成依赖）④ 自动文档 OpenAPI（`/docs` Swagger UI，`/redoc` 更美观）⑤ 异步路由 `async def`（性能提升 3-10 倍）⑥ 中间件 Middleware（统一处理 CORS、日志、限流、错误）⑦ 后台任务 BackgroundTasks（简单场景代替 Celery）⑧ WebSocket 原生支持（流式 AI 输出、聊天室必备，Flask 没有）
- [ ] **JWT 认证** —— 用户注册登录、Token 生成与校验、权限中间件。「几乎所有项目都需要，做一次就会了」
  - [ ] 为什么不用 Session：Session 需服务端存储（依赖 Redis/DB），多机部署要共享；**JWT 是无状态 Token，分布式天然友好**
  - [ ] 完整流程 `[FS §三]`：① 登录验证账密 → 服务端生成 JWT（含 user_id + 过期时间，用 secret 签名）② 返回 token 给前端，前端存 localStorage/cookie ③ 后续请求加 Header `Authorization: Bearer {token}` ④ FastAPI 依赖注入解析 token → 拿 user_id → 查用户
  - [ ] 安全四要点：① `SECRET_KEY` 放 `.env` **不进 git** ② HTTPS 必备（HTTP 下 token 会被中间人窃听）③ Token 短期有效（15-60 分钟），用 refresh_token 续期 ④ **密码必须 bcrypt 哈希存储，永远不存明文**
  - [ ] 工具：`python-jose`（JWT 编解码）+ `passlib[bcrypt]`（密码哈希）
- [ ] **SQLAlchemy ORM** —— Model 定义、关联查询、数据库迁移 Alembic
  - [ ] 实战要点 `[FS §三]`：Model 定义用 `declarative_base` ／ 每请求开一个 session 用完关闭（FastAPI 用 `Depends` 包装最优雅）／ 2.0 版查询改用 `select()` 函数式 ／ 关联关系 `relationship()` + `ForeignKey`，`lazy="select"` 懒加载 vs `lazy="joined"` 即时加载
  - [ ] ⚠️ **N+1 陷阱**：循环里查关联数据 = 性能黑洞。用 `joinedload` 或 `selectinload` 提前 join
  - [ ] Alembic 迁移：`alembic revision --autogenerate` 自动生成迁移脚本

### 第 5 个月：数据库进阶 + 缓存 `[总纲 §三]`

- [ ] **MySQL 进阶**（已有基础，这里是补齐）
  - [ ] 索引原理 B+ 树 —— 主键索引 = 数据本身（聚簇索引）；**辅助索引存的是主键值，所以要回表**
  - [ ] 索引怎么建 —— WHERE/ORDER BY/JOIN 用到的列加索引。**最左前缀原则**：联合索引 (a,b,c) 能用上 a / a,b / a,b,c
  - [ ] EXPLAIN 分析慢查询 —— `type=ref` 是好的，`type=ALL` 全表扫描是灾难；`rows` 估算扫描行数
  - [ ] 事务隔离级别 —— MySQL 默认 RR（可重复读）。要知道脏读/不可重复读/幻读是什么
  - [ ] 连接池配置 —— SQLAlchemy 的 `pool_size` + `max_overflow` + `pool_recycle` 三参数
  - [ ] 分页优化 —— OFFSET 大了变慢，改用游标分页 `WHERE id > last_id ORDER BY id LIMIT 20`
- [ ] **Redis 基础** —— 6 大典型场景 `[FS §三]`
  - [ ] 缓存（String）：`SET key value EX 300`
  - [ ] 分布式锁（String + SETNX）：防止任务被多次执行
  - [ ] 计数器（INCR）：点赞数、访问数，原子递增不需要事务
  - [ ] 排行榜（ZSET）：`ZADD` + `ZREVRANGE`
  - [ ] 消息队列（List / Stream）：`LPUSH` + `BRPOP` 简单队列；Stream 更可靠
  - [ ] Session 存储（Hash）：多机共享登录状态
  - [ ] 缓存穿透 / 雪崩解决方案 `[总纲 §三]`
- [ ] **接口设计** —— RESTful 规范、状态码语义、分页设计、统一响应格式、错误处理。「做出让前端同事满意的 API」
- [ ] **Swagger 文档** —— FastAPI 自动生成，但要会写好注释。**API 文档先行是工程师和码农的分水岭**

### 第 6 个月：Docker + 部署 + 前后端联调 `[总纲 §三]`

- [ ] **Docker 基础** `[FS §三]`
  - [ ] Dockerfile：`FROM python:3.11-slim` → COPY → pip install → `CMD uvicorn ...`，**镜像大小控制在 200MB 内**
  - [ ] 多阶段构建：编译阶段 + 运行阶段分离（前端项目从 node → nginx 两阶段，镜像可缩小 5-10 倍）
  - [ ] `docker-compose.yml`：一个 yml 起多服务（前端 + 后端 + MySQL + Redis），开发环境一行 `docker compose up` 启动全栈
  - [ ] ⚠️ **数据卷 volumes 必须挂载**，否则容器删了数据没了——**新手最常踩的灾难**
  - [ ] 网络 networks：同 compose 内服务直接用服务名互访（如 `mysql:3306`），不需要 IP
  - [ ] 生产注意：① 不要在容器里直接改代码 ② 日志输出到 stdout 让 `docker logs` 收集 ③ 用 `.env` 管配置不要写死在 yml
- [ ] **前后端联调** —— 跨域 CORS 配置、环境变量 `.env`、生产与开发环境分离、Nginx 反向代理基础
- [ ] **Linux 基础命令** —— ssh 连服务器、文件操作、进程管理、日志查看
- [ ] **云服务器部署** —— 把项目跑起来，有公网 IP 能访问。「这一步的成就感很强」
  - > ly 备注：已有 Vultr VPS，这一项的门槛比 PDF 假设的低

### 🎯 阶段二结束检验（两份合并）

`[总纲 §三]`：
- [ ] 能独立完成一个用户系统：注册 / 登录 / JWT 鉴权 / 个人信息
- [ ] 数据库设计合理，有外键关联，常用字段有索引
- [ ] API 有自动文档，前端能通过 Swagger 测试所有接口
- [ ] 项目用 docker-compose 一条命令启动
- [ ] 部署到云服务器，有域名或公网 IP 可以访问

`[FS §三]` 补充：
- [ ] 能**不查文档**写出 FastAPI + SQLAlchemy 的 CRUD 接口
- [ ] 理解 `async/await` 在什么场景能提升性能，什么场景没用
- [ ] 会用 Pydantic 做数据校验，能定义**嵌套模型**
- [ ] 完整实现过 JWT 登录注册 + 密码哈希
- [ ] 在 Redis 至少使用过 **3 种**数据结构解决实际问题
- [ ] 能写 Dockerfile + docker-compose.yml 一键起多服务
- [ ] 会用 EXPLAIN 分析慢查询并加索引优化

---

## 4. 阶段三：AI 能力接入 + 完整项目 `[总纲 §四]`

> **周期 6-9 月** · 目标：能把 LLM 能力集成到自己的全栈项目中，独立交付一个有 AI 功能的完整产品。
> ⚠️ **ly 已超前约 5 个月做了这里的大部分**。下面已打勾的项有文件为证，未打勾的是真没做。

### 第 7 个月：LLM API 接入 + Prompt 工程 `[总纲 §四]`

- [x] **LLM API 基础** —— DeepSeek API 调用 · `week1/day1_hello.py`
  - [x] 流式输出 Streaming · `week1/day3_stream.py`
  - [x] 对话历史管理 · `week1/day7_blind.py`（多轮记忆 + clear/tokens/exit）
  - [x] Token 计费控制 · Week 2 实测校准（英文 0.256 token/字符、中文 0.55）
- [ ] **Prompt 工程** —— System prompt 设计 ✅（Week2 Day2 做过）／ Few-shot 示例 ／ Chain of Thought 引导 ／ 输出格式约束 JSON mode
  - > 完整展开在 §5 的 AI 线阶段 2，**这是 ly 的下一个 AI 主线**
- [~] **前端 AI 集成** —— 加载状态处理 ✅（Day 4 三态机）／ 错误分流 ✅（400/413/422/500/default）／ 流式文本渲染（打字机）❌ ／ 错误重试 ❌ ／ 对话历史展示 ❌
  - > Day 4 做完基础版：`api/static/index.html`。流式渲染与重试留到 Week 3 Vue 版
- [x] **API Key 安全** —— 永远不要把 Key 放前端、后端中转调用、环境变量、调用频率限制
  - [x] `.env` + python-dotenv，`.env` 进 `.gitignore` · 仓库根 `.env.example`
  - [ ] 调用频率限制（rate limit）—— Day 5 护栏要做

### 第 8 个月：RAG 系统入门 `[总纲 §四]`

> 完整 6 步链路 + 参数 + 调优在 §5 的 AI 线阶段 3。这里只列总纲的框。
> ⚠️ **红线：切块（Split）属 AI 线阶段 3（第 7-12 周），不许提前当算法题练**（07-31 就是在这翻的车）。

- [ ] **Embedding 原理** —— 文本向量化的直觉理解、语义相似度计算、为什么向量检索比关键词检索更智能
- [ ] **向量数据库** —— ChromaDB（本地开发）或 Qdrant（生产）。文档存入、相似检索、元数据过滤
- [ ] **RAG Pipeline** —— 文档解析(PDF/Word) → 分块 → Embedding → 存储 → 检索 → 提示词组装 → LLM 生成
- [ ] **LangChain 入门** —— Chain、Document Loader、Text Splitter、Retriever。**不需要全学，跑通 RAG 链路即可**

### 第 9 个月：完整项目打磨 + 上线 `[总纲 §四]`

- [ ] **项目选题** —— 做一个你自己真正想用的工具，不要做 tutorial demo。**真实需求驱动的项目才有完成动力**
  - > 备选见 §6 的 6 个练手项目；总纲 §八给了完整方案「AI 问答笔记本」
- [ ] **代码质量** —— 单元测试 pytest、API 测试 httpx、代码注释、README 文档
- [ ] **性能优化** —— 数据库查询优化、Redis 缓存热点数据、异步任务队列 Celery 处理耗时操作（如 Embedding 生成）
- [ ] **上线与监控** —— Sentry 错误监控、日志结构化输出、接口响应时间监控。**生产项目不能是无人值守的黑盒**

### 🎯 阶段三结束检验 `[总纲 §四]`

- [ ] 项目有完整的 AI 功能（对话 / RAG / 内容生成等）
- [ ] 有稳定的线上环境，真实用户可以访问
- [ ] GitHub 仓库代码整洁，README 详细
- [ ] 能向别人流畅介绍技术选型和架构决策
- [ ] 知道项目的瓶颈在哪里，下一步怎么优化

---

## 5. AI 线细则（`ai-deepdive` 四阶段，与主线并行）`[AI]`

> `[AI §首页]` 第 5 行：「与主路线阶段三同步推进，**可并行启动**」——
> 所以提前启动 AI 线本身不算错，错在**当成唯一主线且没补地基**。

### 先记住：5 大新手陷阱 `[AI §一]`

| 陷阱 | 正解 | ly 中过吗 |
|---|---|---|
| 1. **原理先行** | 先调通 API 做出能用的东西，原理按需补 | 教练犯过（Day 3） |
| 2. 囤课不动手 | 一门课配一个项目，看一节做一节 | — |
| 3. **框架先行** | 先用裸 Python + requests 调 API，理解链路后再上框架 | 没有（正在裸调） |
| 4. 追新焦虑 | 固定一个模型（DeepSeek/Claude）做完一个项目再换 | 没有（固定 DeepSeek） |
| 5. 怕过时 | 迁移成本极低，工程能力通用，模型/框架只是工具 | — |

**核心 3 原则**：**用中学**（学不动 = 项目还不够具体）／**窄而深**（同时学三件事 = 一件都学不会）／**公开输出**（学了不输出 = 没学）。

### 阶段 1：LLM API 实战（第 1-2 周）`[AI §二]` —— ly 在这里

**API 6 大核心概念**（自检能否解释）：

- [x] `messages` —— 对话数组，每条带 role。**关键：模型本身无记忆，多轮靠你把历史塞回去**
- [x] `role: system` —— 系统提示词，决定 80% 的输出质量
- [x] `role: user / assistant` —— 多轮对话交替追加
- [x] `token` —— AI 处理的最小单位。**⚠️ 指南写「1 中文字≈1.5 token」偏高一倍多，以 ly 实测 0.55 / 0.256 为准**
- [x] `temperature` —— 0=确定（适合代码/JSON），0.7=平衡（聊天），1.5=创意
- [x] `max_tokens` —— 常用 1000-4000。⚠️ DeepSeek 推理模型下它卡的是 `reasoning + 正式回答` 之和

**Week 1 · 跑通 + 理解**（每天 2 小时）：

- [x] Day 1 注册 DeepSeek、跑通 hello world · `week1/day1_hello.py`
- [x] Day 2 理解 messages 数组，做命令行多轮对话脚本 · `week1/day2_chat.py`
- [x] Day 3 加入流式输出，实现打字机效果 · `week1/day3_stream.py`
- [x] Day 4 玩 temperature / top_p / max_tokens 各种参数 · `week1/day4_params.py`
- [x] Day 5 做一个「AI 翻译」工具 · `week1/day5_translate.py`
- [x] Day 6 做一个「代码注释生成器」 · `week1/day6_code_doc.py`
- [x] Day 7 总结笔记：API 全流程、踩过的坑、token 计费认知 · `week1/day7_review.md`（考核 8/10，盲写 10/10）

**Week 2 · 综合实战**：

- [x] Day 8-9 「PDF 总结器」：读 PDF → 分段 → AI 总结 → 输出 · `week2/day1_pdf.py` + `day2_summarize.py`
- [-] Day 10-11 「邮件起草助手」 —— **已作废**（该选题从 WordPress/Shopify 场景反推而来，三份路线文档零支持）
- [x] Day 12-13 改造成 FastAPI 接口 + 简单 HTML 前端 —— `week2/api/main.py` + `api/static/index.html`，端到端跑通
- [-] Day 14 部署到云服务器做成可访问 URL —— **暂缓**（零鉴权，JWT/Docker 属总纲阶段二；现状只监听 127.0.0.1 + ssh 隧道）

**🎯 阶段 1 结束自检** `[AI §二]`：

- [x] 能解释 messages / role / token / temperature 的作用
- [x] 能不查文档写出一个流式对话脚本（Day 7 盲写通过）
- [x] 理解为什么模型「没有记忆」（无状态）
- [x] 能估算一次调用的 token 数与成本
- [x] 至少做出 2 个自己真的会用的小工具（翻译器 + PDF 总结器）

### 阶段 2：Prompt 工程深化（第 3-6 周）`[AI §三]` —— 下一站

> 目标：掌握工业级 Prompt 设计方法。**Prompt 质量决定 AI 产品质量的 70%。**
> ⚠️ **红线：指南给 4 周，不许压成 1 周。**

- [ ] **Prompt 黄金 5 段结构** —— ① 角色 Role ② 任务 Task ③ 约束 Constraint ④ 示例 Example ⑤ 格式 Format
- [ ] **8 大核心技法**
  - [ ] Role Prompting —— 「你是资深刑事律师」vs「请帮我看合同」，前者输出深度高一个数量级
  - [ ] Few-shot —— **示例胜过描述**。要 AI 输出特定格式，给 2 个例子比写 500 字解释有效
  - [ ] Chain of Thought (CoT) —— 加一句「请逐步思考」，复杂推理准确率提升 20-50%
  - [ ] **JSON Mode / 结构化输出** —— Prompt 里加 schema + 「必须返回合法 JSON」；高级模型支持 `response_format={"type":"json_object"}` ⭐ **ly 的优先级最高项之一**
  - [ ] Prompt Chaining —— 复杂任务拆成 3-5 个简单 prompt 串联，每步输出作下步输入
  - [ ] Self-Reflection —— 「现在请检查上述回答有无错误并改进」，质量普遍提升
  - [ ] Meta Prompting —— 让 AI 写 Prompt：「请帮我设计一个用来 X 的 system prompt」
  - [ ] Negative Prompt —— 明确禁止：「不要使用 markdown / 不要说抱歉 / 不要超过 100 字」
- [ ] **Function Calling / Tool Use 实战** ⭐ **ly 的优先级最高项之一**（Agent 的基础）
  - [ ] 流程：定义工具（JSON schema）→ 模型决定调用哪个 → **你执行** → 把结果塞回去
  - [ ] **关键认知：模型不会真的调用工具，它只是「建议你调用」。执行权在你手里**
  - [ ] 设计原则：工具名 + 参数描述要写得像给 5 岁小孩看的说明书
  - [ ] 调试技巧：把 AI 的 `tool_calls` 输出打印出来看，**90% 的问题都是参数 schema 没写清楚**
  - [ ] 学源：Anthropic 官网 tool_use 文档（最权威）+ OpenAI function calling cookbook
- [ ] **防幻觉 5 招** —— ① 给资料不靠记忆（RAG 的核心动机）② 允许说「不知道」③ 引用原文 ④ 降低 temperature ⑤ 双模型互校
- [ ] **Prompt 测试与迭代方法论**
  - [ ] 建测试集：10-30 个典型输入 + 期望输出，改 prompt 后跑一遍看哪些 case 退化
  - [ ] 版本管理：Prompt 用 git 管，每次改动写 commit message 说明改了什么、为什么
  - [ ] A/B 对照：改 prompt 时保留旧版本，新旧各跑 10 次取平均，避免抽样偏差
  - [ ] 用工具：LangSmith / LangFuse / PromptLayer
  - [ ] 记录失败案例：建一个 `bad_cases.md`，每次发现 AI 翻车就记录

**🎯 阶段 2 结束自检**：
- [ ] 能用 5 段结构写出一个 200+ 字的 system prompt
- [ ] 至少使用过 5 种 prompt 技法（few-shot / CoT / JSON / self-reflection / negative）
- [ ] 会用 function calling 让 AI 调用一个真实 API（如天气）
- [ ] 有一个 10+ 用例的 prompt 测试集，能跑回归
- [ ] 能解释什么是幻觉，并用 3 种方法降低它

### 阶段 3：RAG 系统从 0 到 1（第 7-12 周）`[AI §四]`

> 目标：让 AI「读」你的私有数据。所有「AI 客服」「AI 知识库」「AI 笔记问答」本质都是 RAG。
> ⚠️ **红线：指南给 6 周。切块（Split）在这一阶段，不是现在。**

- [ ] **RAG 完整 6 步链路**（每步的关键决策）
  - [ ] 1. Load 加载源文档 —— 解析器选型（PyPDF / Unstructured / LlamaParse）
  - [ ] 2. Split 切块 —— **切块大小与重叠（影响极大）** ⏸ ly 有半成品 `week2/day3_chunk.py`（`load_pdf`/`split_text` 已写且正确）
  - [ ] 3. Embed —— 选哪个 embedding 模型
  - [ ] 4. Store 存向量库 —— ChromaDB / Qdrant / pgvector
  - [ ] 5. Retrieve 检索 —— top-k 数量、相似度阈值、重排
  - [ ] 6. Generate 生成 —— prompt 结构、上下文组织
- [ ] **Embedding 模型选型**（2026）—— `text-embedding-3-small`(1536, 英文/通用) ／ `-3-large`(3072, 高精度) ／ **`bge-large-zh-v1.5`(1024, 中文首选、开源可本地)** ／ DeepSeek embedding（国内项目）／ `voyage-3`(1024, Claude 生态)
- [ ] **文档切块 4 种策略** —— ① 固定长度（每 500 字切、重叠 50，最简单但可能切断句子）② 按结构切（标题/段落/章节，Markdown/HTML 友好）③ 按语义切（embedding 算相邻句相似度，效果最好成本最高）④ **递归切（LangChain `RecursiveCharacterTextSplitter`，先按段落超长再按句，性价比之王）**
  - [ ] **切块黄金参数**：`chunk_size=500-1000` 字，`chunk_overlap=10-20%`。小块召回精准但可能丢上下文；大块上下文全但检索准确率下降。**需按业务实测**
- [ ] **向量库选型** —— **ChromaDB**（本地单机，<100 万 chunk，入门首选）／ Qdrant（Docker/云，亿级，生产）／ pgvector（已有 PG 的项目）／ Milvus（K8s，十亿级）／ FAISS（纯内存最快无持久化）／ Pinecone（SaaS）
- [ ] **RAG 调优 5 大杠杆**（按收益排序）—— ① **Chunk 策略（优先调这个）** ② Top-K（常用 3-5）③ 混合检索（向量 + BM25 关键词，中文场景普遍提升 10-20%）④ Rerank（top-20 → reranker 重排 top-3，`bge-reranker-large`）⑤ Query 改写
- [ ] **RAG 评测 RAGAS 框架** —— Context Precision（检索质量）／ Context Recall（是否漏召）／ Faithfulness（幻觉）／ Answer Relevancy（生成质量）。工具 `pip install ragas`
- [ ] **RAG 翻车排查表**（贴墙上）

  | 症状 | 可能原因 | 解决方向 |
  |---|---|---|
  | 答非所问 | 检索召回错了 | 看 retrieved chunks，改切块/换 embedding |
  | 一本正经胡说 | 检索没找到，模型靠记忆编 | Prompt 加「信息不足必须说不知道」 |
  | 答案截断 | max_tokens 太小 / context 超限 | 加大 max_tokens / 减少 top-k |
  | 英文 query 失败 | 中文 embedding 模型只懂中文 | 换多语言 embedding（bge-m3） |
  | 速度慢 | 每次都重新 embed 全部文档 | 向量结果持久化、批量预计算 |
  | 同义词查不到 | 向量模型对术语不敏感 | 加同义词扩展、混合 BM25 检索 |

### 阶段 4：Agent 与工作流（第 13 周后）`[AI §五]`

> 目标：让 AI 不只回答问题，还能「做事」。**这是 2026-2028 最稀缺的能力。**
> ly 关心的「转型做 AI 应用开发」= 这里 + 深化路线 A。

- [ ] **Agent vs Chatbot 本质区别** —— Chatbot 一问一答，逻辑由人控制（**RAG 也属于这一类**）；Agent 模型自主决定下一步做什么，循环执行直到目标达成
- [ ] **ReAct 模式**（Reasoning + Acting）—— 每步输出 Thought（我现在应该做什么）→ Action（调哪个工具，参数是什么）→ Observation（工具返回了什么），循环直到完成。**这就是 LangGraph / AutoGen / Claude Agent SDK 的底层共同模型**
- [ ] **新手路径**（指南明确给的）：裸 Python 写一个 ReAct 循环（100 行）→ 上 LangGraph（理解图状态）→ 按需碰其他框架
- [ ] **框架对比** —— LangChain（老牌链式，生态全但抽象层重）／ **LangGraph（升级版，图状态机、可视化、调试好）** ／ CrewAI（多 Agent，Role-Based 直观）／ AutoGen（微软，文档跟不上）／ Claude Agent SDK（与 Claude 深度集成）／ 裸 Python（完全可控）
- [ ] **MCP 协议** —— Anthropic 2025 年发布的 AI 工具调用标准，「AI 界的 USB-C」。一次开发的 MCP Server 能被所有支持 MCP 的客户端调用
  - [ ] **学多深：能写一个简单的 MCP Server（连接你的数据库/笔记/日历给 AI 用）即可。半天足够**
  - [ ] 资源：modelcontextprotocol.io 官方文档，Python/TypeScript SDK 都有

### 附：AI 工程化生产实践 `[AI §七]` —— demo 到产品的 90% 工作量在这

> ⭐ **ly 的硬约束「商用护栏要成体系」对应的就是这一节。Day 5 要做的是其中前几条。**

- [ ] **API Key 安全** —— 永不放前端 ✅ ／ 环境变量 + `.env` 进 `.gitignore` ✅ ／ **密钥轮换（每项目独立 Key，30-90 天轮换）** ／ **调用频率限制（Redis rate limit，IP/用户级别）**
- [ ] **稳定性三件套**
  - [ ] **指数退避重试** —— 429/5xx → 1s/2s/4s/8s，最多 3-5 次。`tenacity` 库现成的 ← **Day 5**
  - [ ] **超时设置** —— API 调用必须设 timeout（推荐 60-120s），永远不要无限等。流式输出要做心跳检测 ← **Day 5**（实测端到端 5.78s，可据此定阈值）
  - [ ] 模型降级 —— 主模型挂了自动切备用（Claude → DeepSeek → 本地 Ollama）。多模型网关推荐 LiteLLM
  - [ ] 熔断 —— 某模型连续失败 10 次 → 拉黑 5 分钟
- [ ] **成本监控**
  - [ ] Token 统计 —— 每次调用记录 prompt_tokens + completion_tokens，日/周聚合到数据库
  - [ ] **成本告警** —— 日支出超阈值 → 告警。**否则一个死循环 bug 能烧掉一个月预算** ← **Day 5 日调用上限**
  - [ ] 缓存 —— 相同 prompt 直接返回缓存结果，可省 30-70%
  - [ ] 小模型分流 —— 简单任务用小模型，复杂任务才用大模型，成本下降 5-10 倍
- [ ] **可观测性** —— LangSmith（官方，免费额度够个人项目）／ LangFuse（开源可自部署，隐私敏感首选）／ **日志结构化**（至少记 input、output、tokens、latency、model、user_id、trace_id）／ Sentry 错误聚类

### 附：AI 踩坑 12 条速查 `[AI §八]`

| # | 坑 | 一句话解法 |
|---|---|---|
| 1 | Token 超限 | 定期总结历史对话、用 RAG 替代全量塞、改用长上下文模型 |
| 2 | **中文乱码** | 明确 `encoding=utf-8`；**PDF 优先 PyMuPDF / pdfplumber，不要 PyPDF2** ← ly 已中招（页码污染） |
| 3 | JSON 解析失败 | `response_format=json_object` + `json_repair` 容错 + 失败重试最多 3 次 |
| 4 | 流式输出中断 | 客户端心跳检测，3 秒无数据自动重连；前端 SSE 加 retry |
| 5 | 上下文遗忘 | lost-in-the-middle：关键约束放最后、定期总结历史、核心信息放 system |
| 6 | 速度太慢 | 流式立刻有反馈 / 拆并行子任务 / 缓存 / 换快模型 |
| 7 | RAG 答非所问 | 日志打印 retrieved_chunks，肉眼看对不对，再调切块/embedding/top-k |
| 8 | Prompt 改一处全崩 | 建 10+ 用例测试集，每次改完跑一遍 |
| 9 | Function Calling 参数错 | description 写得像说明书 + Pydantic 强校验 + few-shot 示例 |
| 10 | **账单爆炸** | 一个 bug 写循环调 API，一晚烧光 500 美元（真实案例）。**必设日额度上限 + rate limit** |
| 11 | Embedding 维度不匹配 | 换 embedding 必须重新 embed 全部文档，建库时记录用了什么模型 |
| 12 | 模型升级反而变差 | 升级前用测试集跑回归；**固化 model 版本号，不要用别名** ← ly 有 8 处硬编码 `deepseek-chat` 待处理 |

---

## 6. 深化路线（9 个月后按兴趣选一条）`[总纲 §五/六/七]`

> **现在不用选** —— 三条路的前 9 个月完全一样。走完阶段一二三，对「喜欢构建 AI 系统」还是「喜欢从 0 到 1 做产品」会有真实体感，那时选比现在准。
> ly 关心的「转型做 AI 应用开发」= **路线 A**，已在计划内。

### 路线 A：AI 工程化方向 `[总纲 §五]`

适合：喜欢构建 AI 系统、对 LLM 原理有好奇心、想做 AI 工具/平台类产品。**2026-2028 最稀缺的岗位。**

- Agent 框架（LangGraph / CrewAI / AutoGen）· MCP 协议（写 MCP Server）· 微调 LoRA/QLoRA（HuggingFace PEFT）· 推理优化（vLLM / 量化 GPTQ/AWQ/GGUF）· 评测体系（RAGAS / LLM-as-Judge）· MLOps（MLflow / DVC）
- 目标岗位与薪资（2026 参考）：**AI 应用工程师 `LLM API 集成 + 全栈 + Prompt 工程` 25-45 万** ／ AI 平台工程师 `Agent 框架 + MLOps + K8s` 35-60 万 ／ 大模型应用架构师 `系统设计 + RAG + 多模型调度` 50-80 万 ／ AI 产品工程师 `全栈 + AI 集成 + 产品感` 30-55 万

### 路线 B：高级全栈 / 架构师 `[总纲 §六]` + `[FS §四]`

适合：喜欢做产品、享受从 0 到 1、想成为技术全面的独立开发者或技术负责人。

- 系统设计 5 大支柱：可扩展性 / 可用性 / 一致性 / 性能（P50·P99·P999 长尾） / 可维护性
- 分布式核心 8 概念：负载均衡 · 服务发现 · 消息队列 · 分布式锁 · 分布式事务 Saga · 一致性哈希 · 限流熔断 · 链路追踪
- 云原生学习顺序：Docker 熟练 → K8s 基础（Pod/Deployment/Service/Ingress，minikube 本地玩）→ Helm Chart → GitHub Actions CI/CD → Terraform IaC → 可观测性（Prometheus + Grafana + ELK + Jaeger）
- 必读：《DDIA》(数据密集型应用系统设计) · system-design-primer · ByteByteGo · 《凤凰架构》

### 路线 C：鸿蒙生态 `[总纲 §七]` + `[FS §五]`

适合：有 TS/Vue/React 基础的人（ArkTS 是 TypeScript 超集，**阶段一学的 TS 就是最好的鸿蒙入门基础**）。

- 市场：原生鸿蒙开发者 <50 万，国内招聘需求每年 50 万+，同等经验比 Android 薪资高 30-50%
- ArkTS（TS 超集 + 装饰器 + 声明式 UI，禁用 any）· ArkUI（Column/Row/Stack，`@State`≈Vue ref、`@Link`≈v-model、`@Prop`≈props、`@Provide/@Consume`≈provide/inject）· 全场景适配 · 原子化服务 · 分布式能力 · DevEco Studio
- 12 周转型：1-2 周 ArkTS+环境 → 3-4 周 ArkUI+状态 → 5-6 周 路由+网络+存储 → 7-8 周 多设备适配+原子化服务 → 9-10 周 原生能力（相机/位置/通知）→ 11-12 周 AppGallery Connect 发布

---

## 7. 每周节奏模板 `[总纲 §九]` + `[FS §八]`

> 在职学习，每天 2-3 小时。全职可压缩到一半时间。

| 时段 | 内容 | 时长 | 原则 |
|---|---|---|---|
| 周一晚 | 看视频/读文档学新概念（**只看，不写代码**） | 1.5h | 低强度日 |
| 周二晚 | 敲代码实践昨天所学 | 2h | **关键：动手验证** |
| 周三晚 | 继续写 + 复盘周二卡点，用 AI 辅助理解 | 1.5h | 昨天卡哪儿今天解决 |
| 周四晚 | 推进项目功能或专项练习 | 2h | 聚焦一件事 |
| 周五晚 | 整理本周笔记，写学习总结（哪怕 100 字） | 1h | 哪怕 100 字也要写 |
| 周六上午 | 大块时间：项目 / 难题 / 读源码 | 3h | 需要深度专注的放这里 |
| 周日 | 休息或自由探索，不强制 | — | **必须留一天充电** |

### 防 burnout 5 原则 `[FS §八]`

1. **不要日更** —— 每天硬学 4 小时不如隔天学 6 小时，大脑需要消化时间
2. **留 buffer 周** —— 每 4 周留 1 周不学新东西，只巩固/做项目。规划外的事永远比想象的多
3. **卡 2 小时必须停** —— 立刻问 AI / 同行 / 社区 / 转任务。**硬扛是浪费生命**（这条压过教学合约规则 2）
4. **设置里程碑庆祝** —— 完成一个项目 = 吃顿好的 / 买个礼物
5. **找伙伴** —— 加 1-2 个学习群（不要超过 5 个）

### 「看似学了但其实没学」的 5 个信号 `[FS §八]`

| 信号 | 纠正 |
|---|---|
| 「我看懂了这个视频」但合上就写不出代码 | 暂停视频自己敲一遍 |
| 收藏夹一堆文章从没看过 | 清空收藏夹，只留近 1 周要看的 |
| 学了 X 个月还没有可展示的作品 | 暂停学习，2 周内必须做出一个 demo |
| 能复述概念但解释不了「为什么」 | 用费曼法 —— 假装给小白讲 |
| 换个相似场景就不会了 | 刻意变形练习，故意改条件 |

### 输出习惯：选一个就够 `[FS §八]`

- [ ] GitHub 提交（每天至少 1 个 commit）← **最低成本，ly 已在做**
- [ ] 技术博客（掘金/个人站，每周 1 篇 500 字以上）← ly 已有 `week1/article-7-days-llm-api.md`
- [ ] 社区回答（V2EX / Stack Overflow / 知乎）
- [ ] B 站视频（门槛高但效果最深刻）
- [ ] 给他人讲（现实生活中找听众）—— **能让外行听懂 = 你真懂**

---

## 8. 跨方向踩坑速查 15 条 `[FS §九]`

> 遇到症状先查这张表，比搜索快。（AI 方向的 12 条见 §5 末尾）

| # | 坑 | 解 |
|---|---|---|
| 1 | 前端：Vue 响应式失效 | 直接给 reactive 对象赋值整对象会失去响应式。用 `Object.assign(state, newObj)` 或 `ref + .value` |
| 2 | 前端：v-for + v-if 同级 | v-for 优先级高，每次遍历全部再过滤。用 computed 先过滤，或包一层 template |
| 3 | 前端：跨域 CORS | Vite 代理**只在开发生效**。生产必须后端开 CORS 或 Nginx 反代统一域名 |
| 4 | 前端：移动端 100vh 抖动 | iOS Safari 滚动时地址栏出现 → 100vh 跳变。用 `100dvh` 或 JS 监听 resize |
| 5 | 后端：FastAPI async 卡死 | async 函数里调同步阻塞库（如 requests）→ 整个事件循环卡住。用 httpx；或同步代码改用 `def` 而非 `async def` |
| 6 | 后端：SQLAlchemy N+1 | 循环里访问 `user.orders` → 每次发 SQL。查询时 `.options(selectinload(User.orders))` |
| 7 | 后端：MySQL 索引失效 | `LIKE "%xxx%"` / `WHERE YEAR(time)=2026` 用不上索引。改前缀匹配 / 范围查询 |
| 8 | 后端：JWT secret 泄漏 | SECRET_KEY 硬编码 push 到 GitHub。立即换 secret + 撤销所有 token，secret 只能在 `.env` |
| 9 | Docker：镜像越来越大 | 用 `python:3.11-slim` / alpine；多阶段构建；`.dockerignore` 排除 node_modules |
| 10 | Docker：数据库数据丢失 | volumes 必须挂载宿主机路径。生产用云厂商 RDS 不要自建 |
| 11 | Git：误 push 大文件/密钥 | `git filter-repo` 清除历史；BFG Repo-Cleaner 更简单 |
| 12 | Git：rebase 冲突 | 别慌别 abort。打开冲突文件找 `<<<<<<<` / `>>>>>>>`，手动选保留版本，`git add` 后 `git rebase --continue` |
| 13 | 部署：本地能跑生产报错 | 90% 是环境变量没配 / 版本不一致 / 缺系统依赖。用 Docker 统一环境根本解决 |
| 14 | 部署：HTTPS 证书过期 | Let's Encrypt 90 天。用 certbot 自动续期（cron 每月跑）或上 Cloudflare |
| 15 | 学习：跟不上技术更新 | 接受这是常态，没人能学完全部。深耕一个方向比啥都懂强，每周固定 1 小时扫「技术周刊」 |

---

## 9. AI 辅助编程的边界 `[FS §七]`

> ly 每天都在用 Claude Code，这一节是**约束自己**的。

| 好用场景 | 不好用场景 |
|---|---|
| 模板代码（CRUD、表单校验） | 业务逻辑（AI 不懂你的业务） |
| 翻译代码（Python → Go） | 架构决策（AI 没有全局上下文） |
| 单元测试生成 | 优化已有代码的可读性（AI 风格僵化） |
| 解读陌生代码 | 安全敏感代码（AI 偶尔会写出漏洞） |
| 错误诊断（贴报错给 AI） | |

**使用心法**：把 AI 当作「全栈但平庸的同事」。简单任务交给它批量处理，复杂任务自己上 + 让它审。**永远要 review 它的输出，不要直接 Tab 接受看都不看。**

⚠️ **反模式「AI 依赖症」**：所有问题问 AI 不查文档，几个月后基础概念全模糊。
**建议：AI 帮你写，但你必须能解释每一行。**（这正是本项目教学合约存在的原因）

---

## 10. 资源清单（少而精）`[总纲 §十]` + `[AI §十]` + `[FS §十]`

> 原则：**宁可看一份资源 3 遍，不要囤 30 份看 1 遍。**

### 必看视频（按顺序）`[AI §十]`

- [ ] Andrej Karpathy「Intro to LLMs」—— YouTube，1 小时。建立对 LLM 最重要的直觉，**看一遍胜过 10 本书**
- [ ] Andrej Karpathy「Let's build GPT」—— YouTube，4 小时。从 0 用 PyTorch 实现 mini-GPT
- [ ] fast.ai《Practical Deep Learning》Part 1 —— course.fast.ai，「自上而下」教学法

### 必读文档

| 方向 | 资源 |
|---|---|
| 前端 | cn.vuejs.org（中文极好）· typescriptlang.org/docs/handbook（短小精悍）· cn.vitejs.dev · tailwindcss.com · developer.mozilla.org |
| 后端 | fastapi.tiangolo.com（**Tutorial 全部章节必读**）· docs.sqlalchemy.org · realpython.com · use-the-index-luke.com（SQL 索引圣经，免费在线书）· 《Redis 设计与实现》黄健宏 |
| AI | docs.anthropic.com 的 prompt-engineering 章节（**工业界最系统**）· github.com/openai/openai-cookbook · python.langchain.com（不必通读）· api-docs.deepseek.com（中文最友好） |
| 工程化 | learngitbranching.js.org（1 小时掌握 90% Git）· linuxjourney.com · roadmap.sh · github.com/sindresorhus/awesome |

### GitHub 必关注 `[AI §十]`

`mlabonne/llm-course`（40k star，结构化路线图 + Colab 实战）· `langchain-ai/langchain`（examples 目录是活教材）· `Unsloth-ai/unsloth`（微调最快）· `Anthropic/claude-cookbooks`（Tool Use / RAG / Agent 规范示例）· `ggerganov/llama.cpp`

### 必读论文（只 3 篇）`[AI §十]`

- [ ] Attention Is All You Need (2017) —— 即使不读全文，也要看图 1 那张架构图 · **仓库里已有 `week2/attention.pdf`**
- [ ] Retrieval-Augmented Generation (2020) —— 理解为什么要做 RAG
- [ ] ReAct: Synergizing Reasoning and Acting (2022) —— 所有 Agent 框架的理论基础

### 中文社区

宝玉的微博（中文 AI 信息最快源头之一，每天 5 分钟）· 十字路口 Crossing（播客）· 掘金 · V2EX · 阮一峰周刊（每周五更新）· 魔搭社区 ModelScope

### 开发工具 `[总纲 §十]`

编辑器 Cursor / VS Code + Copilot · API 测试 **Apifox**（国产，比 Postman 好用）或 FastAPI 自带 Swagger · 数据库 TablePlus / DBeaver · 终端 WSL2 + oh-my-zsh + zsh-autosuggestions + fzf · HTTP `curl`/`httpie` · JSON `jq`

---

## 11. 调整日志

> 任何偏离本清单的决定都记在这里。**格式：日期 · 改了什么 · 为什么。**

| 日期 | 调整 | 原因 |
|---|---|---|
| 2026-07-31 | 作废「WordPress/Shopify 接 AI」目标 | 教练从现状反推的，三份文档零支持（逐字复核：Shopify 出现 0 次，WordPress 唯一 1 次语义相反） |
| 2026-08-05 | 路线改以总纲 `screen.pdf` 为根 | 此前只读了 ai-deepdive 一份，它第 2 行就写着「配套《个人定制学习路线》」，没顺着找总纲 |
| 2026-08-05 | **方案 C**：Week 3 起补阶段一，用 Vue3+TS 重写 week2 前端 | 内容没白学，错的是顺序。带真后端的项目比总纲的纯前端「待办事项」练得到更多 |
| 2026-08-05 | AI 线 Day 10-11「邮件起草助手」作废 | 选题从 WP/Shopify 场景反推 |
| 2026-08-05 | AI 线 Day 14「部署到公网」暂缓 | 零鉴权，JWT/Docker 属总纲阶段二 |
| 2026-08-05 | `day3_chunk.py` 切块暂停，移交 AI 线阶段 3 | 切块属第 7-12 周，提前当算法题练是排期红线 |
| 2026-08-05 | 目录 `ai-learning/` → `AI_Workstation/` | ly 指定 |
| 2026-08-06 | Day 4 完成，AI 线阶段 1 收尾 | `api/static/index.html` 端到端跑通 |
| 2026-08-06 | 外部 AI 的路线建议（AI Coding / Agent / MCP / 自动化工作流）**评估后不调整主线** | 与本清单重合度高；唯一缺口 Agent/MCP 已在 §5 阶段 4 + §6 路线 A。判据见下 |
|  |  |  |

### 外部建议的三道筛选判据（2026-08-06 定）

> 起因：ly 拿另一个 AI 给的路线建议来比对本清单，并问「学习路线是否需要随前沿变化即时调整」。

**那份建议**：一梯队 AI Coding / Agent / MCP / AI 工作流自动化；二梯队 多模态 / AI 产品 / RAG；
三梯队 World Model / Robotics / AI for Science。
结论「未来一年 = Vue + Python + FastAPI + Agent + AI Coding + 自动化工作流」。

**评估结论：不冲突，不调整。** 它答的是「学什么」，本清单答的是「按什么顺序学、怎么验收」——两个正交的维度。

| 它列的 | 本清单里的位置 |
|---|---|
| Python + FastAPI | §3 阶段二第 4 个月（week2 已提前碰） |
| Vue 3 | §2 阶段一第 2 个月（Week 3 开工） |
| AI Coding | §9「AI 辅助编程的边界」—— ly 每天在用 |
| **Agent / MCP** | §5 AI 线阶段 4（第 13 周后）+ §6 深化路线 A |
| RAG | §5 AI 线阶段 3（第 7-12 周） |
| 多模态 / World Model / Robotics / AI for Science | **三份路线文档里都没有**，不加 |

**两处它给不了、本清单有的**：工程护栏（§5 附「AI 工程化生产实践」）和契约设计（Week 2 Day 3）。
原因不是它不懂，是**它的输入里没有 ly 的错误历史**——它不知道「知道了没调用」已经第五次、
不知道 `finish_reason` 打印了却没检查。**通用路线图对任何 29 岁前端都给同一张。**

**一处排序不同意**：RAG 不该排「未来 2-5 年」。它的前置技能就是 week2 正在做的
（读 PDF → 提文本 → 算 token → 控成本 → 判断截断），对 ly 是「阶段 1 之后紧接着」。
反倒是 **MCP 可以早于 §5 阶段 4 碰一下**——它跟 ly 的主业接得上（给 Claude Code 加个自用工具），
反馈闭环最短，而且本质就是「定义一份工具契约 + 处理调用失败」，和 Day 3 的 `SummarizeResponse` 同一件事。
（`[AI §五]` 原话：**能写一个简单的 MCP Server 即可，半天足够**。）

---

**三道判据 —— 一条新东西值不值得插进清单：**

1. 它解决的问题，现在的方案是**真的解决不了**，还是只是「更好」？只是更好 → 不插。
2. 它下面那层原理我会不会？不会 → **先补原理**。学封装 = 背 API。
3. 半年后它被替换，我手里剩什么？**剩原理 = 值得；剩 API 记忆 = 不值。**

**为什么不该「即时调整」：**

| | 变化速度 | 例子 |
|---|---|---|
| **上层封装** | 半年一换 | LangChain → LangGraph → 下一个；手搓 fetch → Axios → TanStack Query |
| **下层原理** | 十年没怎么变 | HTTP 状态码语义、超时与重试、幂等、token 计费、上下文窗口、鉴权、流式 |

Week 1-2 学的全在下层。**追新的代价是真实的**：Day 4 一项在 6 天内改过两次排期
（map-reduce → HTML 前端 → 对照组），每改一次后面所有天的依赖都要重排。
这条和 §5「5 大新手陷阱」第 4/5 条（追新焦虑、怕过时）是同一件事，
也和 §8 第 15 条「跟不上技术更新 = 接受这是常态，深耕一个方向比啥都懂强」对上。

### 待办的结构性调整

- [ ] **目录重构**（Day 7 做）—— 现在 `week1/week2` 装不下前端项目。候选：`stage1-frontend/` + `stage3-ai/{week1,week2}`。改目录要连带改 `week1/CLAUDE.md` / README / memory 全部路径引用
- [ ] **`deepseek-chat` 硬编码 8 处**（week1 各脚本）—— 该模型 2026-07-24 已弃用，映射到 `deepseek-v4-flash`。对应 AI 踩坑第 12 条「固化 model 版本号」
- [ ] **PDF 解析换 PyMuPDF / pdfplumber** —— AI 踩坑第 2 条，`pypdf` 已暴露页码污染（`sequence\n6length`）
- [ ] **venv 不能跨机器同步** —— `~/.unison/sync.prf` 尚未加 `ignore = Path */venv`（本地 3.12 建的，服务器解析成 3.10）

---

### 两句收尾（原文照抄）

> **`[总纲]`**：你现在的基础组合（HTML/CSS/JS/PHP + Python + MySQL）在市场上比你想象的有价值。9 个月后，你将有一个完整的全栈 AI 项目、真实的线上经历、扎实的 TypeScript 基础。
>
> **`[FS §十]`**：技术学习最大的浪费不是学错方向，是**「反复开始又放弃」**。你的基础已经把 60% 的全栈技能解锁。剩下的 40% 不是新世界，是同一个世界的不同视角。
