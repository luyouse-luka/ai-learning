// Day 4 · /summarize 接口契约的 TS 镜像
// 后端出处：week2/api/main.py 的 SummarizeResponse（:113）+ 各处的 HTTPException
// ⚠️ 这份文件是契约的另一半：后端改字段名，这里必须跟着改（改一次两边都要动）

// ---------------------------------------------------------------
// TODO【4.1】6 字段契约 → interface
//   对着 main.py 的 SummarizeResponse 逐字抄字段名，类型映射：
//   str → string ／ bool → boolean ／ int → number ／ float → number（TS 不区分整数小数）
//   ⚠️ 6 个字段后端全必填 —— 这里一个 ? 都不许出现
// ---------------------------------------------------------------
export interface SummarizeResponse {
  // 在这里填 6 行字段（字段名必须与后端逐字一致）
  summary: string;
  truncated: boolean;
  input_tokens: number;
  output_tokens: number;
  cost: number;
  model: string;
}

// ---------------------------------------------------------------
// TODO【4.2】错误码 → 联合类型
//   判据：不是 README 里「4 类」这个旧说法，是后端现在实际会返回哪些码。
//   去 main.py 数 HTTPException（status_code=...），一共 7 种。
//   每个成员后面用注释标一行语义（比如 429 是什么时候抛的）
// ---------------------------------------------------------------
export type ApiErrorCode = 400 | 413 | 504 | 502 | 429 | 422 | 500;

// 400 	不是 PDF / 提取为空 
// 413 	文件过大（超过 10MB）
// 504 	后端超时
// 502 	连不上模型 / 上游非 2xx / 空 summary
// 429 	deepseek 限流（免费额度用完 / 付费额度用完 / deepseek 自身限流）
// 422 	参数校验失败
// 500 	后端报错（FastAPI 抛异常 / Gunicorn 抛异常 / Nginx 抛异常） 你的代码崩了 
// ---------------------------------------------------------------
// TODO【4.3】错误响应形状 → interface（今天「可选 ?」的落点）
//   FastAPI 的 HTTPException 响应体是 {"detail": ...}
//   网络断了（fetch reject）时连对象都没有 → detail 加 ?
//   ⚠️ 422 的 detail 是数组不是字符串 —— 这个形状留到 Day 6 真写
//      错误 UI 时再加（2026-09-08 调整：ValidationIssue 砍掉，
//      现阶段没有真实使用处，Day 6 用到时讲一次就懂）
// ---------------------------------------------------------------
export interface ApiError {
  detail?: string;
}