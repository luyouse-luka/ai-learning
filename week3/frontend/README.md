# frontend

Vue + TypeScript frontend for the PDF summarizer.

## Windows local setup

Run these commands in this directory:

```powershell
pnpm install --frozen-lockfile
pnpm exec node --version
pnpm dev
```

The project pins pnpm 11.20.0 and Node 24.19.0. pnpm downloads the project
runtime during installation and uses it for scripts; the system Node version
does not need to be changed.

Open `http://localhost:5174/`. To verify the setup, run `pnpm build`.

The existing application configuration includes:

- Axios, imported by `src/components/FileUploader.vue`.
- Vue Router, registered in `src/main.ts`, with `/` and `/about` routes.
- Pinia, registered in `src/main.ts`.
- The `@` alias pointing to `src/` in Vite and TypeScript.
- `VITE_API_BASE=/api` in `.env.development`. Vite forwards `/api/*` to
  `http://127.0.0.1:8000/*`.

The frontend can start independently. Actual PDF uploads require the FastAPI
backend running on port 8000 and its model API credentials configured locally.
The Week 4 Day 3 `FilePicker.vue` exercise is implemented and verified. Day 4
will replace its callback prop with a component event and extract the result panel.

### Windows backend setup

Run these commands from the repository root, not the frontend directory:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Create a root `.env` using `.env.example` as the reference and set your own
`DEEPSEEK_API_KEY` locally. The backend initializes its model client at import
time, so configure the key before starting it. `.env` and `.venv/` are ignored
by Git. Do not reuse an imported Linux virtual environment on Windows.

```powershell
.\.venv\Scripts\python.exe -m uvicorn week2.api.main:app --host 127.0.0.1 --port 8000
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:5174/api/health
```

Both health requests should return `status: ok`; `api_key_configured` should
be true. Health checks do not call the model. A successful PDF summary also
requires the model provider to accept the configured key and model.

Verified locally on 2026-10-13: backend dependency checks passed; both health
routes returned HTTP 200; uploading the existing `week2/attention.pdf` through
`http://127.0.0.1:5174/api/summarize` returned HTTP 200, a nonempty summary,
and `truncated: false`. This verifies the API path, not browser interaction.

### Current verification limits

`pnpm build-only` verifies the Vite bundle. `pnpm build` also checks TypeScript.
The completed Day 3 exercise passed `pnpm build` on 2026-10-13. The learner
also confirmed the browser upload worked; other error paths were not rechecked.
At the pre-push recheck, the local key setting was empty and the backend could
not restart. Restore the local key before running the backend again; the
earlier successful upload does not establish current service availability.

### 顺带发现 / 未修

- `eslint-plugin-oxlint` 1.73.0 requests `oxlint` ~1.73.0, while the project
  installs oxlint 1.74.0. This existing lint peer mismatch is outside the local
  dependency restoration; the application dependency versions are preserved.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Vue (Official)](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Recommended Browser Setup

- Chromium-based browsers (Chrome, Edge, Brave, etc.):
  - [Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
  - [Turn on Custom Object Formatter in Chrome DevTools](http://bit.ly/object-formatters)
- Firefox:
  - [Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)
  - [Turn on Custom Object Formatter in Firefox DevTools](https://fxdx.dev/firefox-devtools-custom-object-formatters/)

## Type Support for `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so we replace the `tsc` CLI with `vue-tsc` for type checking. In editors, we need [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) to make the TypeScript language service aware of `.vue` types.

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
pnpm install
```

### Compile and Hot-Reload for Development

```sh
pnpm dev
```

### Type-Check, Compile and Minify for Production

```sh
pnpm build
```

### Lint with [ESLint](https://eslint.org/)

```sh
pnpm lint
```
