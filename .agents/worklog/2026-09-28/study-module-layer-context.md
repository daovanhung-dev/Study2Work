---
task_id: "2026-09-28-study-module-layer-context"
date: "2026-09-28"
primary_task_type: "docs"
secondary_task_types: ["context-maintenance"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "PARTIAL"
---

# Worklog: Làm rõ context layer cho module Study

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run -A scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-26/document-study-api3-view-comments.md`
    - carry_forward: Tách expected/current; comment phải bám luồng runtime và không dùng để sửa discrepancy trong DD.
  - path: `.agents/worklog/2026-09-26/update-agents-context-api3-rules.md`
    - carry_forward: Cập nhật page hiện hữu, giữ page graph/manifest khi không thêm context page; comment API header ngay trước handler.
  - path: `.agents/worklog/2026-09-23/create-study-api14-dd.md`
    - carry_forward: Ưu tiên current source, ghi rõ discrepancy và không suy diễn implementation từ context/design.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Làm rõ ranh giới `models.py`, `validate.py`, `query.py`, `view.py` cho Study API dựa trên source hiện tại; validators chỉ trả lỗi qua `error_response(...)`; mọi thao tác có ý nghĩa trong view có comment tiếng Việt.
- Canonical contract/approved DD: Kế hoạch được người dùng duyệt ngày 2026-09-28; chỉ cập nhật context/worklog, không đổi runtime source.

## CURRENT_BEHAVIOR

- Source/config: Context có ranh giới layer cơ bản nhưng còn mô tả model validation và comment view theo event chính. `architecture.md` vẫn ghi validator API #1 rỗng/unwired và validation nằm trong model, trái source hiện tại. API #5 `models.py` còn khai báo `DEFAULT_LOCALE`; API #2 không có `query.py` vì không truy vấn DB.
- Runnable tests: Study context ghi 163 tests; task chỉ cập nhật tài liệu nên không cần chạy runtime tests.
- Runtime wiring: API #1–#7 có `validate.py`; API #1, #3–#7 có SQL constants trong `query.py`; API #2 dispatch qua provider không truy cập DB. `error_response` trả `JSONResponse`.

## SOURCE_TRACE

```text
current API #1–#7 models/validate/query/view + app/core/responses.py
-> .agents/server-study layer and comment guidance
-> future Study coding agents
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #1 validation ownership | Current source has `validate_register_request`; architecture context says empty/unwired and model validation | DISCREPANCY | Correct context to source-backed validation boundary. |
| API #5 model contents | `api_05_categories/models.py` declares `DEFAULT_LOCALE` outside a model class | DISCREPANCY | State desired model-only rule and record this existing source exception without moving runtime code. |
| API #2 query layer | API #2 delegates to an email provider and has no `query.py` | VERIFIED | Explain that `query.py` is conditional on SQL queries; do not require an empty file. |
| View comment granularity | Existing context asks for event comments; approved plan selects comments for each meaningful operation, with cohesive operations allowed to share one comment | RESOLVED | Update Study instructions and preserve API header convention. |

## CHANGES

- Files changed: `.agents/server-study/AGENTS.md`, `architecture.md`, `modules/README.md`, `workflows/README.md` and this worklog.
- CONTEXT_UPDATES: Clarified layer ownership, error-return rule, optional SQL constants file, meaningful-operation comments in views, and corrected stale API #1 ownership; documented API #5's current `DEFAULT_LOCALE` placement discrepancy.
- Context pages changed: `.agents/server-study/AGENTS.md`, `.agents/server-study/architecture.md`, `.agents/server-study/modules/README.md`, `.agents/server-study/workflows/README.md`; no manifest/page graph change.
- Assumptions: Context-only task; no source constants moved and no runtime behavior changed.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run -A scripts/select-worklogs.mjs --type docs --limit 3` | Selected and read 3 matching docs worklogs; no shortage | VERIFIED |
| Read current API #1–#7 models/validators/queries/views, response factory and affected Study context; scan for superseded layer/comment wording | Confirmed API #1 validator is active; API #2 has no SQL/query file; API #5 `models.py` contains `DEFAULT_LOCALE`; no superseded wording remains in Study context | VERIFIED |
| `git diff --check` | No whitespace errors | VERIFIED |
| `deno run -A scripts/validate-agent-context.mjs` | `AGENT_CONTEXT_INVALID`: pre-existing missing DB Admin context/source paths and stale tracked source snapshots across scopes, including Study | CONTEXT_BASELINE |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_INVALID` due to missing DB Admin context/source paths and broken DB Admin links; no Study-specific page-graph errors reported | CONTEXT_BASELINE |
| Study runtime tests | Not run; approved scope changes context/worklog only | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: Repository-wide context validation remains red due to missing DB Admin context/source paths and stale source snapshots recorded in earlier worklogs.
- Next owner/action: Study context updates are complete; refresh repository-wide DB Admin paths/source snapshots in a separate maintenance task if a green global validator is required.
