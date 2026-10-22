import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { createRequire } from 'node:module'

const require = createRequire(new URL('../frontend/package.json', import.meta.url))
const ts = require('typescript')
const source = readFileSync(new URL('../frontend/src/components/FileUploader.vue', import.meta.url), 'utf8')
const script = source.match(/<script\b[^>]*>([\s\S]*?)<\/script>/)?.[1]
assert.ok(script, 'Vue script must exist')
const ast = ts.createSourceFile('FileUploader.ts', script, ts.ScriptTarget.Latest, true)
const names = ['getErrorMessage', 'toUserMessage']
const functions = names.map(name => {
  const node = ast.statements.find(item => ts.isFunctionDeclaration(item) && item.name?.text === name)
  assert.ok(node?.body, `${name} must exist`)
  return node.getText(ast)
})
const js = ts.transpileModule(functions.join('\n'), {
  compilerOptions: { target: ts.ScriptTarget.ES2022 },
}).outputText
// Execute the real functions with a synthetic Axios 422 response; no HTTP requests.
const toUserMessage = new Function('axios', 'selectedFile', 'console', `${js}\nreturn toUserMessage`)(
  { isAxiosError: () => true }, { value: null }, { error: () => {} },
)
const cases = [
  ['missing', undefined, '请求失败，请检查上传文件后重试'],
  ['string', '文件过大', '文件过大，请检查上传文件后重试'],
  ['multiple', [{ msg: '缺少文件' }, { msg: '格式错误' }], '缺少文件；格式错误，请检查上传文件后重试'],
  ['empty string', '', '，请检查上传文件后重试'],
  ['empty array', [], '，请检查上传文件后重试'],
]
let failures = 0
for (const [name, detail, expected] of cases) {
  const data = detail === undefined ? {} : { detail }
  const actual = toUserMessage({ response: { status: 422, data } })
  try {
    assert.equal(actual, expected)
    console.log(`PASS ${name}`)
  } catch {
    failures++
    console.error(`FAIL ${name}: ${JSON.stringify({ actual, expected })}`)
  }
}
console.log(`Passed ${cases.length - failures}/${cases.length}`)
process.exitCode = failures ? 1 : 0
