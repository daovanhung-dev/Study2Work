---
task_id: "2026-10-24-create-study-api50-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD API #50 — Tạo nội dung Mentor

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ cấu trúc 8 sheet chính + 3 report theo template; chỉ mô tả nguồn đã truy vết và ghi rõ phần schema chưa có.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: AC-22 Content là miền riêng với Lecture; schema Content, enum, payload, principal binding và tree rules chưa được runtime xác nhận.
  - path: `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`
    - carry_forward: Catalog có 103 ID; #50 là API tiếp theo chưa có DD; số route/view pair là bằng chứng source, không phải runtime proof.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: API catalog #50 `POST /api/v1/mentor/content`, Bearer JWT, role Mentor; body bắt buộc `{course_id:int64!, content_type:ContentType!, title:string!, payload:object!}`; trả HTTP 201 `DESIGN_RESOURCE_CREATED`, `ApiEnvelope<Content>`; lỗi đúng tập 401/403/422/500 theo catalog.
- Canonical contract/approved DD: `docs/lists/list_api.md` row #50; AC-22 flow POST → `INSERT Content` → reload content tree. AC-33 xác định moderation queue đọc content `PENDING_REVIEW`; suy ra create vào trạng thái này là đề xuất `DERIVED`, không xác định bảng/column lưu Content.
- Response `Content`: `id:int64`, `course_id:int64`, `content_type:ContentType`, `title:string`, `payload:object`, `status:ContentStatus`, `parent_id?:int64`, `order:int32`.

## CURRENT_BEHAVIOR

- Source/config: Không có route `/api/v1/mentor/content`, module `api_50_*`, hoặc test tương ứng trong `apps/study-server`; hiện endpoint `UNWIRED`/`NOT_FOUND`.
- DB artifacts: Legacy `DB.sql` có `courses`/`lessons` nhưng không có generic Content table. V1-PILOT có UUID `content_blocks` nhưng chỉ gắn `lesson_id`, không khớp Content contract BIGINT. Live schema chưa xác minh.
- Runnable tests: Không có test API #50 do route/module không tồn tại; task này chỉ thay đổi tài liệu.
- Runtime wiring: API #50 chưa được router đăng ký. Nếu route được nối mà chưa cập nhật middleware allowlist, contract error fallback hiện hành có thể phát `VALIDATION_ERROR`/`INTERNAL_SERVER_ERROR`, lệch `DESIGN_*`; ghi là discrepancy tích hợp có điều kiện.

## SOURCE_TRACE

```text
Catalog #50 + AC-22 POST -> absent route/module -> intended Mentor/course authorization -> logical INSERT Content (physical mapping SOURCE_REQUIRED) -> response ApiEnvelope<Content> -> AC-22 reload tree
AC-33 moderation queue reads status=PENDING_REVIEW; this supports the initial status value, but not its persistence schema.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Route/service/test | Current Study Server source scan | `UNWIRED` / `NOT_FOUND` | DD is design-only; no runtime claim. |
| Content persistence | Legacy and V1-PILOT DDL mismatch generic BIGINT Content contract | `SOURCE_REQUIRED` | Do not fabricate an INSERT or physical target. |
| Initial review state | AC-33 queue reads `status=PENDING_REVIEW`; AC-22 POST inserts Content | `DERIVED` transition proposal | Propose `PENDING_REVIEW` as initial state; confirm transition and persistence mapping. |
| Root placement and ordering | Request omits `parent_id` and `order`, response includes both | `DERIVED` proposal + confirmation required | Propose root (`parent_id=null`) and next sibling order; keep policy open pending approval. |
| Mentor identity/course assignment | Catalog gives role; AC-22 requires managed course; Study guard/principal mapping absent | `SOURCE_REQUIRED`; legacy `courses.mentor_id` only `DERIVED` candidate | Avoid an executable access query until identity and assignments are confirmed. |
| Validation branches | Contract allows 422 but omits 404 | `DERIVED` for request-shape validation; missing-course mapping open | Keep exact listed HTTP/business codes and flag unresolved invalid-course semantics. |

## CHANGES

- Files changed: `apps/study-server/docs/dd/50_mentor_content_create/` (8 sheets + 3 reports) and this task worklog.
- CONTEXT_UPDATES: None planned; no server convention or runtime contract changes.
- Context pages changed: None.
- Assumptions: Propose initial content state `PENDING_REVIEW` by combining AC-22 create with AC-33 pending-queue precondition (`DERIVED`, needs confirmation); propose root placement and append order as `DERIVED`, subject to confirmation. Keep physical Content schema, enums, payload schema, ID allocation, missing-course/access mapping and audit/timestamp fields `SOURCE_REQUIRED`/open. Exact catalog success/error set remains authoritative.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `git status --short` | Existing user changes/untracked DDs observed; preserve all outside API #50 scope. | COMPLETE |
| Worklog selector + read of 3 selected docs worklogs | #48, #49, inventory review complete. | COMPLETE |
| Diagram/source/DDL scan | AC-22, AC-33, catalog, runtime absence and DDL mismatch inspected. | COMPLETE |
| Custom static DD integrity/contract check | Exact 11-file manifest, all 8 front matters/template appendix tails, request/response coverage, catalog code set, JSON syntax, Markdown fences and whitespace passed. | VERIFIED |
| `git diff --check` + targeted whitespace review | No diagnostics; custom check also covered untracked DD files. | VERIFIED |

## HANDOFF

- Remaining blockers: Physical Content schema/persistence, payload/enums, Mentor identity/assignment, and missing-course semantics remain open; this DD is not implementation-ready.
- Next owner/action: API #50 DD was statically verified and is now macro-reviewed with #49–#53; its pending-review/root/order proposals remain open. Continue at API #54.

## GROUP_MACRO_REVIEW

- Status: VERIFIED_WITH_OPEN_QUESTIONS after API #53 was created.
- Cross-API findings: #49 tree cardinality/visibility remains unresolved; #50/#51 PENDING_REVIEW and tree placement are DERIVED; #52 publication transitions remain DERIVED and AC-33 APPROVED/PUBLISHED is ambiguous; #53 proposes direct-child blocking, no cascade, unpublish-first for PUBLISHED, and history-preserving soft delete.
- Shared blockers: generic Content/version schema, payload/enums/readiness, Mentor principal/assignment, dependency coverage, soft-delete/audit storage, and filtering deleted items from active tree/review queue.
- Application tests were not run; this records document-level macro-review only.
