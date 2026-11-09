---
task_id: "2026-11-09-ai-server-ollama-client-and-error-handling"
date: "2026-11-09"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["server-ai"]
cross_scope_dependencies: ["AI Server -> Ollama HTTP API", "dev-superpowers output language across project scopes"]
status: "IN_PROGRESS"
---

# Worklog: AI Server Ollama client lifecycle and error handling

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-08/configure-local-ollama-ai-server.md`
    - carry_forward: Preserve the active chat route and raw success response; local checkout startup was verified previously, while live Ollama availability must be checked again.
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Trace exact current route and dependencies, expose source gaps, and preserve unrelated worktree entries.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: Keep developer decisions separate from derived behavior and verify contract and error changes explicitly.
- shortage: `none` (3 of 93 coding worklogs selected and read)

## EXPECTED_BEHAVIOR

- Requirement: Run the `dev-superpowers` workflow for the supplied developer description. Keep `POST /api/v1/chat_log_ai` non-streaming and its success JSON stable; use one shared `httpx.AsyncClient` per AI Server process with an explicit `max_connections=100`; reject blank and eventually overlong prompts; map Ollama errors to safe API responses.
- Canonical contract/approved DD: No DD or BD supplied. The current success JSON is `{response: string}`. The developer approved the proposed scope and defaults on 2026-11-09 with `approve nhé`: 8,000-character maximum, 5-second pool wait with HTTP 503, safe Ollama error JSON, and existing FastAPI 422 body.

## APPROVAL_RECORD

- Stage 1 intake: `APPROVED` by developer in this conversation on 2026-11-09 (`approve nhé`), covering the exact scope and options presented immediately before that message.
- Stage 2 SPEC: `APPROVED` by developer on 2026-11-09 via `tôi approve nhé làm bước tiếp theo đii` for Vietnamese SPEC SHA256 `FF2FC393212178F7E55641857E0DEF2628768191AAA72C5CB19141E0F441E635`. Approval metadata produced SHA256 `59BA3D2E0C4D70CB53DEB03E614E5901CE1D03B043BDC4DA66C080F31EF6E708`; an editorial decision/verification ledger produced SHA256 `3FE37AE80BFB37B4F1B4797DD4E49426C6784B00A4BE95A136C89C4B82D0C4AE`. Removing Markdown trailing spaces and separating metadata paragraphs produced current SHA256 `01F1A9133C3732A71A826AFDC42E1D0BB3CBB2DFFBD356AB94962454730B5AD9`. These edits changed only presentation, not requirements, scope or acceptance criteria, so approval carries forward. The previous pending English draft had SHA256 `9B51782822BAE9D54FE2B47527D3557EF29C3F117321DD9EC1E755C091599659`.
- Stage 3 PLAN: `APPROVED` on 2026-11-09. Developer selected `PLAN-D01` B (caller trực tiếp mở/đóng client tường minh), chose `PLAN-V01` A (đo trên host sau) and instructed “thực hiện tiếp đi”. The approved-choice PLAN SHA256 was `0DA0A745192D86D0844BDB38FF838B93DB7C5BE7C888E783320F18C4B1E85F3D`; removing Markdown trailing spaces and updating the SPEC formatting-only hash reference produced current SHA256 `EE99FAB7F91A965806E552B8D16B479CFCCE0B051EEB94DF242DB052FC4AF1A9`. The previous pending SHA256 was `486CB7E83A3E63B6A0C47477489FA38C0821786F70200ADC2BC7A1B629244987`. No requirement, choice, test case or scope changed; approval carries forward.
- Stage 4 code/tests: `APPROVED` by developer on 2026-11-09 via “ok nhưng ... commit rồi push ...”, in reply to the completed code/test summary. Eight focused mock tests passed; live Ollama throughput remains deferred per `PLAN-V01` A.
- Stage 5 delivery: Developer explicitly requests a commit and push to `ducna_dev/featrure_AI_sever` and selected `feat(ai-server): reuse Ollama client and handle chat errors`. The provided GitHub URL is a Compare page (`/compare/develop...ducna_dev/featrure_AI_sever?expand=1`), not a numbered PR. The GitHub connection shows the remote branch at `fc980cd3` but no open PR in `daovanhung-dev/Study2Work` before push.

## CURRENT_BEHAVIOR

- Source/config at intake: At HEAD `fc980cd3` on `ducna_dev/featrure_AI_sever`, `app/main.py` created `FastAPI()` and included `app/api/v1.py`. The route accepted `ChatLogRequest(prompt: str)`, called `chat_log_ai` and returned `{response: answer}`. `OllamaService.generate` sent `stream: false` to `/api/generate`. `_request` created and closed `httpx.AsyncClient(timeout=self.timeout)` per call. The default `OLLAMA_TIMEOUT` was 180 seconds.
- Runnable tests at intake: No AI Server test files were found in the focused source inventory.
- Runtime wiring: The route is reachable from `app/main.py`. Copied core exception, middleware and database files are `UNWIRED`. The worktree already contains unrelated modifications and untracked files; preserve them.

## SOURCE_TRACE

```text
uvicorn app.main:app -> POST /api/v1/chat_log_ai -> ChatLogRequest
-> chat_log_ai -> ai_service.generate -> _request -> Ollama POST /api/generate
-> result["answer"] -> {"response": answer}; no database write
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Client lifecycle | `_request` creates an `AsyncClient` for each call. | `DISCREPANCY` | Developer requested one lifespan client per process with max 100 connections. |
| Prompt validation | `ChatLogRequest` declares only `prompt: str`. | `DISCREPANCY / DECIDED` | Approved: reject blank and over 8,000 characters with existing FastAPI 422 shape. |
| Error mapping | Adapter raises custom exceptions; route and main app do not map them to API errors. | `DISCREPANCY / DECIDED` | Approved: 503/504/502 upstream mapping and safe `{error:{code,message}}` JSON. |
| Pool wait | `timeout=self.timeout` applies the same configured value to HTTPX timeout categories. | `DISCREPANCY / DECIDED` | Approved: separate 5-second pool wait; 503 if exhausted. |
| Streaming | `generate` sends `stream: false`; developer chose to keep one final response in this task. | `DEFERRED` | No FE or streaming contract change. |
| Frontend consumer | Focused search found no use of `chat_log_ai` in the examined client source roots. | `NOT_FOUND` | No verified FE consumer to update in this scope. |

## CHANGES

- Files changed: Worklog, SPEC, PLAN and Vietnamese `dev-superpowers` skill files; `apps/ai-server/app/main.py`, `app/module/chat/model.py`, `app/service/ai/ollama_service.py`, `app/service/ai/__init__.py`, two README files, `tests/test_ollama_service.py`, `tests/test_chat_api.py`, and directly affected `.agents/server-ai` pages.
- CONTEXT_UPDATES: The skill and skill index now default developer-facing scope, SPEC, PLAN, approval and handoff text to Vietnamese, preserving technical identifiers. The skill also requires stage-owned decision/verification records in SPEC or PLAN, concise chat summaries, multiple-choice options and a free-text alternative. For lifecycle choices it now requires exact creation, reuse, closure, error and caller effects.
- Context pages changed: `.agents/skills/INDEX.md`, `.agents/server-ai/AGENTS.md`, `architecture.md`, `apis/chat.md`, `modules/chat.md`, `services/ollama.md`, `tests.md`.
- Assumptions: The request begins the full staged workflow. HTTPX's 100 connection value is a pool cap, not Ollama inference capacity.

## IMPLEMENTATION_RESULT

- FastAPI lifespan calls `ai_service.start()` once per process and `close()` on shutdown. Direct callers use explicit `start()` and `close()` in `finally`; unstarted use raises a clear lifecycle error. Service uses one HTTPX client with `max_connections=100` and a distinct 5-second pool timeout.
- `ChatLogRequest` rejects non-string, blank and over-8,000-character prompts with FastAPI 422, forwarding accepted content unchanged. Success remains `{response: string}` and `stream: false`.
- Pool, connection, timeout and invalid Ollama response errors map to safe HTTP 503/503/504/502 JSON; logs contain error class or HTTP status, not prompt or raw Ollama body. Ollama capacity and latency remain unverified on the deployment host.
- Test coverage: TC-01 through TC-14 covered by 8 focused test methods using `httpx.MockTransport` and `TestClient`; this is functional verification, not a performance measurement.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | Three coding worklogs selected and read. | `PASS` |
| Focused AI Server source and context inspection | Current entry, route, model, view, adapter, config and test inventory inspected. | `SOURCE_VERIFIED` |
| `node scripts/validate-agent-context.mjs` | Exit 1 on existing missing DB Admin context/source; no output names this worklog. | `BASELINE_FAILURE` |
| `Get-FileHash .../SPEC.md -Algorithm SHA256` | `9B51782822BAE9D54FE2B47527D3557EF29C3F117321DD9EC1E755C091599659`. | `SPEC_REVISION_RECORDED` |
| Vietnamese SPEC translation SHA256 | `FF2FC393212178F7E55641857E0DEF2628768191AAA72C5CB19141E0F441E635`; previous revision was pending, so no approved SPEC revision was invalidated. | `PENDING_SPEC_APPROVAL` |
| SPEC approval metadata SHA256 | Developer approved the previous Vietnamese content revision; metadata-only stamping produced current SHA256 `59BA3D2E0C4D70CB53DEB03E614E5901CE1D03B043BDC4DA66C080F31EF6E708` without behavior changes. | `APPROVED_SPEC` |
| PLAN SHA256 | `CEE067765C05DCFB858D2826728A2C687B36E92766603B798EE4A75B2DDECBC6`; corrected the planned PowerShell test command before approval; no code or tests have run. | `PENDING_PLAN_APPROVAL` |
| Editorial SPEC ledger SHA256 | `3FE37AE80BFB37B4F1B4797DD4E49426C6784B00A4BE95A136C89C4B82D0C4AE`; records approved and unverified states without changing REQ or AC. | `APPROVAL_CARRIED_FORWARD` |
| Revised PLAN ledger SHA256 | `C304B621646A91B7B04E15DFF80C9F280EE149FB0C19F025A101B07469E75E22`; `PLAN-D01` must be chosen before approval. | `NEEDS_DECISION` |
| PLAN-D01 lifecycle explanation SHA256 | `486CB7E83A3E63B6A0C47477489FA38C0821786F70200ADC2BC7A1B629244987`; A/B now have explicit direct-call examples and closure responsibilities; no source code changed. | `NEEDS_DECISION` |
| `quick_validate.py` for `dev-superpowers` with `PYTHONUTF8=1` | `Skill is valid!` using the Study Server virtual environment. | `PASS` |
| `git diff --check -- .agents/skills/INDEX.md` | No whitespace errors in the tracked skill index change. | `PASS` |
| `& .venv/Scripts/python.exe -m unittest discover -s tests -v` from `apps/ai-server` | 8 tests passed; mock transport covers TC-01 through TC-14. Initial run found two test-only assumptions about private HTTPX `_limits`; corrected tests to inspect constructor arguments, then reran successfully. | `PASS` |
| `git diff --check` | No whitespace errors in tracked diff. | `PASS` |
| `node scripts/validate-agent-context.mjs` after context edits | Exit 1; baseline manifest/context problems include missing DB Admin source, orphan AI Server context pages and widespread stale entries. The validator does not provide a scoped pass result for this task. | `BASELINE_FAILURE` |

## HANDOFF

- Remaining blockers: Git push requires network access. Existing PR has not been located through the connected GitHub repository; the supplied URL is a Compare page. Live Ollama throughput and latency remain unverified and are scheduled for deployment-host measurement per `PLAN-V01` A.
- Next owner/action: Stage only this AI Server workflow's agreed files, create the commit with the selected message and push the exact branch. Verify remote branch and report the PR status accurately. Preserve unrelated `uv.lock` and other existing worktree changes.
