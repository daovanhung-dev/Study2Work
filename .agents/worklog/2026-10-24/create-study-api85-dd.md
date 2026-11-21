---
task_id: "2026-10-24-create-study-api85-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #85 — Đổi trạng thái lesson

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ contract direct, không nhầm source/schema candidate thành runtime; bảng response và error theo catalog.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Giữ Query/Mutation/Response matrices và đánh dấu body/schema gap `SOURCE_REQUIRED`; không đoán enum.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Tách `DIRECT` khỏi `DERIVED`; các status proposal phải liên kết AC evidence và ghi confirmation gate.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tiếp tục chuỗi một API DD mỗi phiên tại API #85; lập plan và matrices trước khi tạo folder; viết tiếng Việt theo template và kiểm tra tĩnh ngay sau authoring.
- Canonical contract/approved DD: Catalog #85 xác nhận `PATCH /api/v1/admin/lessons/{lesson_id}/status`, Bearer JWT/Admin, path `lesson_id:int64!`, `ApiEnvelope<Lesson>`, HTTP 200 `DESIGN_RESOURCE_UPDATED` và đúng 401/403/404/422/500 codes. AC-34 xác nhận actor Admin có lesson-management permission, nhánh “UPDATE status + audit” rồi reload danh sách. Catalog/diagram chưa khai báo request body, enum values hoặc transition policy. Reusable `Lesson` có `status:LessonStatus`; member values chưa được liệt kê. `createDD-markdown`/`docs-dd` làm chuẩn cấu trúc; Study giao Markdown, không tạo ZIP.

## CURRENT_BEHAVIOR

- Source/config: `app/api/v1.py` không có API #85/Admin lesson route; không có matching API #85 module/view/test. Shared auth hiện chỉ có Student guard; Admin policy/guard chưa có. Legacy `infra/postgres/study-server/DB.sql` có `lessons.status VARCHAR(20) DEFAULT 'DRAFT'` và `updated_at`, nhưng không có audit relation. V1-PILOT `infra/postgres/02_study_db.sql` có lesson UUID/versioned table nhưng không có status field; `audit_events` dùng UUID resource ID, không map trực tiếp với legacy BIGINT lesson. Live schema chưa xác minh.
- Runnable tests: Không chạy vì đây là task DD/documentation-only.
- Runtime wiring: `UNWIRED / NOT_FOUND`; source-level route/view pair chưa tồn tại. Đây không phải kết luận về deployment.

## SOURCE_TRACE

```text
Admin Bearer principal + lesson-management permission -> PATCH theo path lesson_id + DERIVED body.status proposal -> kiểm tra target status (enum/transition còn mở) -> legacy-schema candidate UPDATE status (+ updated_at candidate) -> logical audit intent theo AC-34 nhưng physical mapping SOURCE_REQUIRED -> trả ApiEnvelope<Lesson> từ candidate returned row -> AC-34 reload danh sách
```

## PREAUTHORING MATRICES

### Requirement Matrix

| Requirement | Evidence | Status/decision |
|---|---|---|
| `PATCH /api/v1/admin/lessons/{lesson_id}/status`; Bearer JWT; Admin; path `lesson_id:int64!` | `docs/lists/list_api.md`, API #85 | DIRECT |
| `ApiEnvelope<Lesson>`; 200 `DESIGN_RESOURCE_UPDATED`; exact errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR` | API #85 catalog row | DIRECT; preserve exact set |
| Admin lesson-management permission; update status plus audit; reload list | AC-34 index and diagram nodes n9/n10/n13 | DIRECT intent; no invented physical audit fields |
| JSON body `{status: LessonStatus}` | Catalog/diagram expose only path; UPDATE needs target to be specified | DERIVED proposal; field requiredness and content type need confirmation |
| Enum members, casing, allowed transitions, same-status/retry behavior | Not specified by catalog/diagram/reusable schema | SOURCE_REQUIRED; do not invent |

### Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Bearer JWT | Authenticate Admin; AC-34 lesson permission; audit actor candidate | DIRECT requirement; claim/policy/actor mapping SOURCE_REQUIRED |
| `lesson_id` | Required path int64 | Candidate `lessons.id` predicate and returned Lesson identity | DIRECT type; legacy BIGINT physical mapping candidate |
| Body `status` | Proposed JSON field | Candidate target for status mutation and returned `data.status` | DERIVED; enum/transition validation SOURCE_REQUIRED |
| Query parameters | None declared | None | DIRECT absence in catalog/diagram |
| `X-Trace-Id` | Current middleware convention | Envelope/audit correlation candidate | Current-source convention; audit column mapping unresolved |

### Query Matrix

| Step | Type | Source/target | Conditions/effect | Status |
|---|---|---|---|---|
| Q1/M1 | `UPDATE ... RETURNING` candidate | Legacy `lessons` | `id=:lesson_id`; set only `status=:status`; `updated_at=CURRENT_TIMESTAMP` candidate | Status effect DIRECT; table/columns DERIVED from legacy DDL; live schema unknown |
| M2 | Logical audit append | No approved compatible physical relation | Record Admin status change per AC-34 | Audit intent DIRECT; physical table/keys/payload/transaction mapping SOURCE_REQUIRED; no INSERT SQL invented |
| Other reads/writes | None proposed | Courses, dependencies, progress, metadata | No extra predicates or bulk side effects | Not required by AC-34 status branch |

### Mutation Matrix

| Mutation | Target | Fields/effect | Status |
|---|---|---|---|
| M1 UPDATE | Legacy `lessons` candidate | Change `status`; preserve id, course, content, video, order and created_at | DIRECT logical effect; DERIVED physical candidate |
| M1 timestamp | Legacy `lessons.updated_at` | Set server timestamp if this legacy mapping is selected | DERIVED; timestamp owner/live schema need confirmation |
| M2 audit | Logical audit event | Record status operation by Admin | AC-34 DIRECT; physical persistence SOURCE_REQUIRED |
| No mutation | Lesson metadata/dependencies/progress | No changes or bulk propagation proposed | Scope boundary |

### Response Source Matrix

| Response item | Candidate source/transform | Status/gap |
|---|---|---|
| Envelope/business codes | Catalog #85 + reusable `ApiEnvelope<T>` | DIRECT contract; current error helper emits `{}` absent `data`, while API guideline says `null` |
| `data.id`, `course_id` | Legacy `lessons.id`, `course_id` | Candidate; `course_id` nullable in DDL but required int64 in Lesson |
| `data.title` | Legacy `name -> title` | Candidate alias; API #09 precedent |
| `data.content`, `video_url` | Legacy same-named columns | Candidate nullable values; omit-vs-null unresolved |
| `data.order` | Legacy `sort_order -> order` | Candidate alias; API #09 precedent |
| `data.status` | Returned updated status | Direct response field; legacy table candidate; enum members/casing unresolved; V1-PILOT lesson has no status |
| `meta`, `traceId` | Envelope/current trace middleware | Empty meta candidate; trace propagate/generate per current convention |

## PRIOR SOURCE REVIEW

- `apps/study-server/docs/dd/82_admin_lessons_list/` and `83_admin_lesson_detail/`: preserve reusable Lesson projection and Admin/AC-34 boundary; keep route/schema gaps explicit.
- `apps/study-server/docs/dd/84_admin_lesson_update/`: status is excluded from metadata update and explicitly owned by API #85.
- `apps/study-server/docs/dd/71_admin_user_status/` and `76_admin_course_status/`: precedent for status body as DERIVED, no invented enum/transition matrix, and logical audit intent separated from physical audit schema.
- `apps/study-server/app/api/v1.py`, `app/utils/auth.py`, `app/core/middleware.py`, `app/core/responses.py`: no Admin lesson route/guard or API #85-specific error integration in current source.
- `infra/postgres/study-server/DB.sql` and `infra/postgres/02_study_db.sql`: legacy BIGINT status column conflicts with V1-PILOT UUID/versioned lesson model; audit schema does not directly pair with the legacy lesson ID.

## PLAN BEFORE DD AUTHORING

1. Xác nhận catalog #85 và AC-34 node/edges, gồm status input, transition/audit intent, success/error set.
2. Đọc DD #82–#84 và status mutation precedents #71/#76; giữ status operation tách khỏi lesson metadata update #84.
3. Kiểm tra source router/auth/middleware, reusable Lesson, legacy/pilot schema, audit/status columns/tables và live-schema boundary.
4. Lập Requirement, Request Usage, Query, Mutation và Response Source matrices trước khi tạo DD folder.
5. Nếu catalog/diagram thiếu body, status enum hoặc transition table, đưa phương án status field tối thiểu thành `DERIVED` theo chỉ dẫn người dùng; giữ các giá trị/transition chưa có nguồn thành open questions, không phát minh bảng audit/cột.
6. Tạo 8 template sheets và 3 reports trong `85_admin_lesson_status`; giữ exact contract/error codes, Draft status, Markdown-only.
7. Kiểm tra package/appendices, status/error transitions, JSON, links, tables, fences, whitespace; cập nhật inventory/worklog.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Body/schema | Catalog and diagram are path-only; legacy status column exists but V1-PILOT Lesson has no status | `DERIVED / DISCREPANCY` | Propose one `status` field; enum and selected schema remain open |
| Audit persistence | AC-34 requires audit; legacy schema lacks audit relation; V1 `audit_events` resource ID is UUID while legacy lesson ID is BIGINT | `SOURCE_REQUIRED` | Keep logical audit effect, omit guessed INSERT/table mapping |
| Runtime/Admin access | No API #85 route/view/test; Student-only guard | `UNWIRED / NOT_FOUND` | DD describes expected contract/proposal, not current behavior |
| Live schema | Checked-in legacy and V1-PILOT DDL differ; live metadata unavailable | `NOT_VERIFIED` | Physical query is candidate only |

## CHANGES

- Files changed: `apps/study-server/docs/dd/85_admin_lesson_status/` (8 template sheets + 3 reports), this worklog, and the current-count section in `inventory-study-api-dd-counts.md`.
- CONTEXT_UPDATES: None; context pages and registry remain unchanged.
- Context pages changed: None planned.
- Assumptions: Preserve all pre-existing worktree modifications; documentation-only scope. The proposed body has one status field; allowed values/transitions and physical audit persistence remain unapproved.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector and review | Deno selector returned #48/#49/#50; all three read in full; no shortage. | `VERIFIED` |
| Contract/source/template/diagram inspection | Catalog row, AC-34 nodes, reusable Lesson, DD #82–#84 and status precedents #71/#76, current route/auth/middleware/response, legacy/V1 schema pages reviewed; preauthoring matrices recorded. | `VERIFIED_STATIC_ONLY` |
| DD package | Exact 11-file folder; 8/8 appendix suffixes byte-match registered template; exact catalog success/error set; 4 JSON examples parse; 39 tables / 410 data rows; 14 balanced fences; 28 local links and 13 anchors resolve; no trailing whitespace. | `PASS — STATIC` |
| `git diff --check` | No diagnostics. | `PASS` |
| Application tests | Not run; docs-only and API #85 has no route/module. | `NOT_RUN` |
| Context validator | No `.agents/<scope>` page or registry changed. | `NOT_APPLICABLE` |

## HANDOFF

- Remaining blockers: Owner confirmation for body, LessonStatus enum/transitions, Admin policy, selected schema, compatible audit persistence, transaction and error integration.
- Next owner/action: API #86 DD and the AC-34 #82–#86 document-level macro-review are complete; continue at API #87 in the next API-DD session.

## GROUP_MACRO_REVIEW — AC-34 #82–#86

- Status: `VERIFIED_WITH_OPEN_QUESTIONS`; see `apps/study-server/docs/dd/86_admin_lesson_delete/VERIFICATION_REPORT.md`.
- Findings carried into #85: status plus audit belongs only to the #85 branch. Physical audit mapping, status body/enum/transitions and selected schema remain open; #86 does not inherit an audit write by analogy.
- No API approval, route implementation, live schema check or application test is implied by this review.
