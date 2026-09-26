---
task_id: "2026-09-26-update-agents-context-api3-rules"
date: "2026-09-26"
primary_task_type: "docs"
secondary_task_types: ["context-maintenance"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["repository conventions", "server-study context graph"]
status: "VERIFIED"
---

# Worklog: Cập nhật Agents Context từ phiên Study API #3

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-26/document-study-api3-view-comments.md`
    - carry_forward: Comment API #3 phải ngắn, bám event/DD step, mô tả current runtime và không dùng comment để reconcile discrepancy.
  - path: `.agents/worklog/2026-09-23/create-study-api14-dd.md`
    - carry_forward: Tách expected/current behavior; giữ `DISCREPANCY`, `SOURCE_REQUIRED`, `UNWIRED` thay vì suy diễn từ DD.
  - path: `.agents/worklog/2026-09-23/create-study-api15-enrollment-status-dd.md`
    - carry_forward: Docs/context update không được biến design-only evidence thành runtime fact.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Ghi các rule bền vững từ phiên API #3 vào Agents Context: comment style, API header convention, DD/current discrepancy handling, Study module boundaries và verification workflow.
- Scope: Cập nhật `.agents/project/conventions.md`, `.agents/server-study/AGENTS.md`, `.agents/server-study/workflows/README.md`, `.agents/server-study/modules/README.md`; không đổi application source.

## CURRENT_BEHAVIOR

- Các page đã có transaction/validation/source-priority rules nhưng chưa ghi rõ API handler header comments, short event comments và comment-only verification.
- API #3 hiện có `# API #03 auth_login`/`# API #03 auth_refresh` trước handler, shared validators trong `app/utils/validate.py`, và local `validate.py` đã được loại bỏ.
- Context page graph/manifest đã tồn tại; không cần thêm page hoặc registry entry mới.

## SOURCE_TRACE

```text
current Study source + API #3 DD
-> worklog evidence
-> project conventions / server-study entry / workflow / module context
-> future coding/docs agents
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| DD vs current API #3 runtime | DD và source khác về status/response/token persistence | DISCREPANCY | Context phải yêu cầu mô tả current source và không tự reconcile |
| API #3 refresh DD coverage | DD tập trung login; current source có refresh rotation | CURRENT_SOURCE_EXTENSION | Ghi comment/header convention cho cả handler nhưng không gán refresh sai DD step |
| Context registry | Các page đích đã nằm trong manifest/page graph | VERIFIED | Chỉ sửa nội dung page, không sửa manifest |

## CHANGES

- Files changed: Added concise API header/comment conventions, DD/current discrepancy handling and API #3 validation/module boundary guidance to existing context pages.
- CONTEXT_UPDATES: Updated repository conventions plus Study Server entry, workflow and module pages; no new page or manifest entry was needed.
- Context pages changed: `.agents/project/conventions.md`, `.agents/server-study/AGENTS.md`, `.agents/server-study/workflows/README.md`, `.agents/server-study/modules/README.md`.
- Assumptions: Giữ rule hiện có, thêm nội dung ngắn không trùng; không cập nhật `architecture.md` vì ownership đã đủ và không thay đổi.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` | Selected and read 3 matching docs worklogs | VERIFIED |
| Read target context pages, manifest and API #3 source/worklogs | Confirmed insertion points and no new page required | VERIFIED |
| `git diff --check` | No whitespace errors after removing an existing trailing space in the patched context block | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | VERIFIED |

## HANDOFF

- Remaining blockers: Full repository context drift remains a known baseline; drift was intentionally skipped per task scope.
- Next owner/action: Future Study/API tasks should follow the newly recorded concise comment and source/contract alignment rules.
