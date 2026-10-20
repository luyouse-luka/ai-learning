# Application Directory Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move the Vue application to frontend/ and the FastAPI service to backend/ while preserving behavior and the learner's current edits.

**Architecture:** Move application directories intact, including ignored local runtime files. Keep week1–week4 learning records, samples, root .env and root .venv in place. Update only path-dependent code and active documentation; preserve historical references with a migration note.

**Tech Stack:** Existing Vue, TypeScript, Vite, Pinia, pnpm and Python/FastAPI dependencies; no dependency changes.

**Spec:** User's 2026-10-20 selection recorded in week4/README.md under Day 7 directory migration; teaching boundaries in week1/CLAUDE.md.

## Global Constraints

- Retain the learner's App.vue and CostPanel.vue edits and remaining teaching comments.
- Preserve .env, .venv, week1/venv, model settings, pricing, request handling and pnpm-lock.yaml.
- Keep services local; do not call the model, commit, push or deploy.
- Use verified absolute workspace paths and native PowerShell Move-Item.

## Review Focus

- Preserve every tracked frontend file byte-for-byte except its README and the backend source reference comment; compare SHA-256 hashes.
- Load the root .env after backend relocation; compare its hash and assert the resolved path.
- Preserve Prompt experiment sample and output locations; verify paths without running an experiment.
- Preserve FastAPI health, static page and missing-file validation routes without model requests.
- Keep Vite aliases and proxy working; run the full build and check a local dev-server proxy request.

## Task 1: Establish the baseline

- [x] Run `pnpm build` in week3/frontend; type checking and production build passed.
- [x] Call `/health` through FastAPI TestClient; HTTP 200 and status=ok.
- [x] Record hashes for 43 tracked application files and the root .env in session state.
- [x] Resolve and record the user's chosen frontend/ + backend/ structure.

## Task 2: Move applications and repair path dependencies

- [x] Verify both source/destination pairs are inside the repository and destinations do not exist, then move `week3/frontend` to `frontend` and `week2/api` to `backend`; see the Windows runtime ruling below.
- [x] Change backend/main.py root configuration lookup to `ENV_FILE = BASE_DIR.parent / ".env"` and `load_dotenv(ENV_FILE)`; update its launch example to `.venv/Scripts/python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000`.
- [x] In backend/prompts.py define `ROOT_DIR = Path(__file__).resolve().parent.parent`, load `ROOT_DIR / ".env"`, set `SAMPLE = ROOT_DIR / "week2" / "attention_extracted.txt"`, and set comparison output to `OUTPUT_DIR = ROOT_DIR / "week4"`.
- [x] Update the backend source reference in frontend/src/types/api.ts to backend/main.py; retain all business logic and component edits.
- [x] Add root README.md with directory mapping and current startup commands; update frontend/README.md, learning-entry migration notes, current status and the Day 7 ledger.

## Task 3: Verify and record the result

- [x] Add tools/verify_workspace_layout.py and run `.venv\Scripts\python.exe tools\verify_workspace_layout.py`; check retired application entries, .env lookup, experiment paths, health/static endpoints, missing-file validation and invalid-file rejection without calling a model.
- [x] Run `pnpm build` in frontend; type checking and production build exited zero.
- [x] Compare preserved-file hashes and root .env against the baseline; 39/43 application files were identical. Intentional differences: backend/main.py, backend/prompts.py, frontend/README.md, frontend/src/types/api.ts. Root .env and pnpm-lock.yaml unchanged.
- [x] Start temporary local backend/frontend processes on available loopback ports 8000/5179, check Vite `/api/health` (200), and stop only the tool-managed sessions started by this verification.
- [x] Run `git diff --check`; review the final file list and obtain a read-only review of migration-specific risks. One stale current startup reference in week1/CLAUDE.md was found and corrected to the root/frontend README.
- [x] Update this ledger and Day 7 progress with actual results and remaining Week 4 self-check work.

## Execution decisions

- Execute in the user's current checkout: it contains learner edits, local dependencies and configured credentials needed for the authorized migration. No new checkout or dependency installation is needed.
- Keep historical lesson text unchanged; dated mapping notes identify the new application locations.
- Directory work is peripheral coaching support; do not modify learner-owned summarization or state-management logic.
- Ruling: PowerShell Move-Item traversed a pnpm junction and stopped partway. Recovered the application tree without overwriting files, moved remaining ordinary branches with Directory.Move, and rebuilt pnpm dependencies offline from the unchanged lockfile. No model, library, runtime or pricing upgrade was made.
- Ruling: Old dependency backups had their junctions unlinked without following targets. Recursive deletion was rejected by automatic approval review with only `blocked by policy`; retain ignored ordinary files at frontend/.migration-node-modules/ and week3/frontend/node_modules/. The retired application entry files are absent, and new runtime links point to the new frontend or shared pnpm runtime store.
- Ruling: Keep root node_modules/ and .migration-node-modules/ ignore patterns to exclude that local cleanup residue. No cache files belong in the migration's source change list.
