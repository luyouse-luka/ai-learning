import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { createRequire } from 'node:module'

const require = createRequire(new URL('../frontend/package.json', import.meta.url))
const ts = require('typescript')
const { ref } = require('vue')
const { createPinia, setActivePinia, defineStore } = require('pinia')
const { parse } = require('vue/compiler-sfc')
const source = readFileSync(new URL('../frontend/src/components/FileUploader.vue', import.meta.url), 'utf8')
const { descriptor, errors } = parse(source)
assert.equal(errors.length, 0)
assert.ok(descriptor.scriptSetup && descriptor.template, 'Script and template must exist')
const ast = ts.createSourceFile('FileUploader.ts', descriptor.scriptSetup.content, ts.ScriptTarget.Latest, true)
const handler = ast.statements.find(node => ts.isFunctionDeclaration(node) && node.name?.text === 'handlePick')
assert.ok(handler?.body, 'handlePick must exist')
const template = descriptor.template.ast
assert.ok(template, 'Template AST must exist')
const picker = template.children.find(node => node.type === 1 && node.tag === 'FilePicker')
assert.ok(picker, 'FilePicker must exist')
const pick = picker.props.find(prop => prop.type === 7 && prop.name === 'on' && prop.arg?.content === 'pick')
assert.ok(pick?.exp, 'FilePicker must bind pick')
assert.match(pick.exp.content, /^(?:handlePick|\(file\)\s*=>\s*handlePick\(file\))$/)

const js = ts.transpileModule(handler.getText(ast), {
  compilerOptions: { target: ts.ScriptTarget.ES2022 },
}).outputText
const storeSource = readFileSync(new URL('../frontend/src/stores/summarize.ts', import.meta.url), 'utf8')
const storeAst = ts.createSourceFile('summarize.ts', storeSource, ts.ScriptTarget.Latest, true)
const storeDefinition = storeAst.statements
  .filter(ts.isVariableStatement)
  .flatMap(node => node.declarationList.declarations)
  .find(node => node.name.getText(storeAst) === 'useSummarizeStore')
assert.ok(storeDefinition?.initializer, 'Summarize store definition must exist')
const storeJs = ts.transpileModule(`const useSummarizeStore = ${storeDefinition.initializer.getText(storeAst)}`, {
  compilerOptions: { target: ts.ScriptTarget.ES2022 },
}).outputText
const useSummarizeStore = new Function('ref', 'defineStore', `${storeJs}\nreturn useSummarizeStore`)(ref, defineStore)
const cases = [
  ['error to PDF', 'error', '文件 map.php 不是 PDF，请换一个', { name: 'valid.pdf' }],
  ['null selection', 'error', 'No file selected', null],
  ['done to new file', 'done', '', { name: 'next.pdf' }],
]
for (const [name, initialStatus, initialError, nextFile] of cases) {
  const selectedFile = ref({ name: 'map.php' })
  const errorMsg = ref(initialError)
  const status = ref(initialStatus)
  setActivePinia(createPinia())
  const summarizeStore = useSummarizeStore()
  if (initialStatus === 'done') {
    summarizeStore.setResult({
      summary: 'Fixture A summary', truncated: false,
      input_tokens: 1, output_tokens: 1, cost: 0, model: 'fixture-model',
    })
    assert.ok(summarizeStore.result, 'A previous result must exist before switching files')
  }
  let requests = 0
  const axios = { post() { requests++; throw new Error('Picking a file must not upload it') } }
  const handlePick = new Function('selectedFile', 'errorMsg', 'status', 'axios', 'summarizeStore', `${js}\nreturn handlePick`)(
    selectedFile, errorMsg, status, axios, summarizeStore,
  )
  handlePick(nextFile)
  assert.equal(selectedFile.value?.name ?? null, nextFile?.name ?? null)
  assert.equal(errorMsg.value, '')
  assert.equal(status.value, 'idle')
  assert.equal(requests, 0)
  assert.equal(summarizeStore.result, null, 'Picking a new file must clear the previous result')
  console.log(`PASS ${name}`)
}
console.log(`Passed ${cases.length}/${cases.length}; handler state and template binding checked, no browser or HTTP`)
