---
task_id: "2026-11-21-build-server-web-commands"
date: "2026-11-21"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work"]
cross_scope_dependencies:
  - "Study Web /api/v1 dev proxy -> Study API at 127.0.0.1:3003"
  - "Work Web /api, /uploads, /img dev proxies -> Work API at 127.0.0.1:3002"
status: "VERIFIED"
---

# Worklog: Bổ sung lệnh chạy hai dự án Web

## READ_PLAN

| Path | Needed section/range | Task-specific reason | Status |
|---|---|---|---|
| `AGENTS.md` | User-supplied router and read-set/worklog rules | Route this documentation task without reopening supplied content | `READ_FROM_CONTEXT` |
| `.agents/AGENTS.md` | Global page graph and task rules | Apply the canonical context flow | `READ_FROM_CONTEXT` |
| `.agents/context-map.md` | Canonical flow and `web-work` / Study Web page graph | Select the registered frontend context | `READ_FROM_CONTEXT` |
| `.agents/context-manifest.json` | `web-work` scope and Study Web subcontext | Confirm machine-readable context wiring | `READ_FROM_CONTEXT` |
| `.agents/project/agent-control.md` | Read-set, target, and worklog rules | Track this documentation operation | `READ_FROM_CONTEXT` |
| `.agents/target.md` | Active target table | Preserve sole progress tracker | `READ_FROM_CONTEXT` |
| `.agents/worklog/README.md` | Worklog and same-type preflight rules | Complete required docs-task preflight | `READ_FROM_CONTEXT` |
| `.agents/worklog/TEMPLATE.md` | Required worklog sections | Use the canonical audit structure | `READ_FROM_CONTEXT` |
| `scripts/select-worklogs.mjs` | Exact-type worklog selection | Select up to three prior docs tasks | `READ_FROM_CONTEXT` |
| `.agents/worklog/2026-11-21/2026-11-21-build-server-web-commands.md` | Current task worklog body selected by the exact-type selector | Confirm the preflight record and planned scope | `READ` |
| `.agents/worklog/2026-11-21/document-server-and-script-prompts.md` | Full selected worklog | Carry forward relevant prompt-document conventions | `READ` |
| `.agents/worklog/2026-11-21/reconcile-study-screen-completion-status.md` | Full selected worklog | Carry forward relevant docs-only scope and evidence conventions | `READ` |
| `.agents/project/INDEX.md` | Cross-scope context entry | Confirm where proxy/service boundary guidance lives | `READ` |
| `.agents/project/contracts.md` | Local service/client dependency status | Record proxy dependencies accurately | `READ` |
| `.agents/web-work/AGENTS.md` | Scope rules | Apply web-work context rules | `READ` |
| `.agents/web-work/INDEX.md` | Scope page graph | Route the two frontend projects | `READ` |
| `.agents/web-work/study/AGENTS.md` | Study Web subcontext rules | Confirm Study client boundary relevant to its launch row | `READ` |
| `.agents/web-work/study/INDEX.md` | Study Web current source/context summary | Confirm its dev server and API proxy status | `READ` |
| `docs/prompts/build_server.md` | Full table and notes | Refresh target before updating existing command reference | `READ` |
| `apps/study-client/package.json` | `scripts` | Reconfirm Study Web start command | `READ` |
| `apps/study-client/README.md` | Local run section | Reconfirm documented working directory and address | `READ` |
| `apps/study-client/angular.json` | `serve` options | Reconfirm Angular serve behavior and proxy configuration | `READ` |
| `apps/study-client/proxy.conf.json` | Proxy target | Reconfirm Study API dependency | `READ` |
| `apps/work-client/web/package.json` | `scripts` | Reconfirm Work Web dev command, host, and port | `READ` |
| `apps/work-client/web/README.md` | Development-server note | Recheck current documentation and discrepancy | `READ` |
| `apps/work-client/web/vite.config.ts` | `server` host/port/proxy | Reconfirm actual Work Web address and API dependency | `READ` |

## LEAF_TARGET_PLAN

| Target | Single operation | Acceptance evidence |
|---|---|---|
| Cập nhật bảng lệnh local cho hai dự án Web | Bổ sung lệnh, thư mục chạy, địa chỉ và proxy của Study Web và Work Web vào bảng hiện có | Các giá trị khớp package/config; API rows còn nguyên; `git diff --check` sạch |

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-21/2026-11-21-build-server-web-commands.md`
    - carry_forward: current task worklog selected as newest docs entry; read to complete exact-type preflight.
  - path: `.agents/worklog/2026-11-21/document-server-and-script-prompts.md`
    - carry_forward: use commands from current package/readme/source and name each subproject working directory; this target is a docs-only reference; preserve unrelated changes.
  - path: `.agents/worklog/2026-11-21/reconcile-study-screen-completion-status.md`
    - carry_forward: keep source/runtime evidence distinct and preserve uncommitted files; docs-only work does not imply app tests.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Thêm lệnh chạy local cho hai dự án Web vào `docs/prompts/build_server.md`.
- Canonical contract/approved source: Current `package.json`, Angular serve config, and Vite config determine commands/addresses; proxy config determines API dependencies.

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| Cập nhật bảng lệnh local cho hai dự án Web | `0% → 0%` | Initial leaf target; acceptance is two source-backed Web rows with the existing server rows preserved. |
| Cập nhật bảng lệnh local cho hai dự án Web | `0% → 50%` | Rechecked the target table and current frontend package/config files; identified correct commands and addresses, plus the Work README's stale port/backend values. |
| Cập nhật bảng lệnh local cho hai dự án Web | `50% → 85%` | Added both Web rows, neutralized the mixed server/Web table labels, and documented the proxy dependencies; focused readback and diff check remain. |
| Cập nhật bảng lệnh local cho hai dự án Web | `85% → 100%` | Readback confirms five rows, source-backed commands/URLs/proxies, and all three API rows unchanged; scoped diff check exits 0. |

## CURRENT_BEHAVIOR

- Source/config: existing prompt table has three API rows only. Study Web declares `npm start` and README address `http://localhost:4200`; `angular.json` enables `proxy.conf.json`, which targets Study API `127.0.0.1:3003`. Work Web declares `npm run dev` at host `127.0.0.2`, port `3001`, strict port; its Vite config proxies `/api`, `/uploads`, `/img` to Work API `127.0.0.1:3002`. Work Web README currently says port `5174` and backend port `3000`, which conflict with current package/config.
- Runnable tests: docs-only task; no application tests planned.
- Runtime wiring: Study `/api/v1` and Work `/api`, `/uploads`, `/img` proxies are configured; the corresponding APIs must run separately for those proxied calls.

## SOURCE_TRACE

```text
Study Web Angular dev server -> /api/v1 proxy -> Study API :3003
Work Web Vite dev server -> /api,/uploads,/img proxies -> Work API :3002
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Work Web README launch details | `apps/work-client/web/README.md` says dev port 5174 / Work server 3000, while `package.json` and `vite.config.ts` specify port 3001 / proxy target 3002. | `DISCREPANCY` | The prompt reference will use current executable package/config values and leave the README out of scope. |

## CHANGES

- Files changed in final diff: `docs/prompts/build_server.md` and this worklog. `.agents/target.md` was temporarily updated and returned to its header-only baseline. `docs/prompts/script.md`, `apps/study-server/app/core/constants.py`, and the prior worklog are outside this task and untouched.
- CONTEXT_UPDATES: none planned.
- Context pages changed: none planned.
- Assumptions: the two Web projects are Study Web and Work Web; dependencies must already be installed.
- Target progress updates and completion evidence: see `TARGET_UPDATES`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `git status --short --branch` | `develop...origin/develop`; pre-existing `docs/prompts/script.md` modification and prior untracked Study Server worklog; target tracker now modified for this task | `CHECKED_BY_TOOL` |
| Final `git status --short --branch` | `docs/prompts/build_server.md` modified by this task; `docs/prompts/script.md`, `apps/study-server/app/core/constants.py`, and prior Study Server worklog remain outside-scope changes; target tracker is back to header-only | `CHECKED_BY_TOOL` |
| `git diff --check -- docs/prompts/build_server.md` | Exit 0, no whitespace errors | `VERIFIED` |
| Readback of `docs/prompts/build_server.md` | Five rows present; the existing three API rows are unchanged; both Web commands, addresses, and proxy dependencies match current package/config source | `VERIFIED` |

## HANDOFF

- Remaining blockers: Work Web README has stale dev port/backend values (5174/3000); this task records current package/config values (3001/3002) and leaves README out of scope.
- Next owner/action: none.
