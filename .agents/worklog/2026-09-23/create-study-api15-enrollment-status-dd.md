---
task_id: "2026-09-23-create-study-api15-enrollment-status-dd"
date: "2026-09-23"
primary_task_type: "docs"
secondary_task_types: ["api-dd", "context-loading"]
project_scopes: ["server-study"]
cross_scope_dependencies: ["Study API design contract", "AC-12 enrollment flow", "courses/enrollments schema"]
status: "PARTIAL"
---

# Worklog: Tạo DD Study API #15 kiểm tra trạng thái enrollment

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-23/create-study-api14-dd.md`
    - carry_forward: Dùng `createDD-markdown`; giữ expected/current tách biệt; API design-only chưa wired phải ghi `UNWIRED / NOT_FOUND`.
  - path: `.agents/worklog/2026-09-22/load-project-context.md`
    - carry_forward: Ưu tiên current source; context drift là trạng thái hiện hữu; Deno là compatibility runner khi Node không có.
  - path: `.agents/worklog/2026-09-22/load-study-register-account-context.md`
    - carry_forward: Study query helper không commit; docs-only không được suy diễn runtime từ design contract.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD Markdown cho API #15 kiểm tra trạng thái enrollment.
- Contract: `GET /api/v1/courses/{course_id}`, Public, path `course_id:int64!`, `ApiEnvelope<Enrollment>`, success `200 DESIGN_RESOURCE_RETRIEVED`, errors `404 DESIGN_RESOURCE_NOT_FOUND` và `500 DESIGN_INTERNAL_ERROR`.
- Approved handling: Giữ Public; không thêm Bearer/user identity; ghi gap `SOURCE_REQUIRED / BLOCKING DISCREPANCY` khi không xác định được enrollment duy nhất.

## CURRENT_BEHAVIOR

- Current Study router chỉ có các route API #1–#7; không có API #15.
- Không có module/query/view/model/test runtime cho enrollment-status.
- Checked-in schema có `courses` và `enrollments`; `enrollments` có `id`, `user_id`, `course_id`, `status`, `enrolled_at`, `completed_at`.
- Contract Public không cung cấp user identity để chọn một enrollment trong quan hệ có thể có nhiều bản ghi theo `course_id`.

## SOURCE_TRACE

```text
list_api.md + AC-12
-> Public GET course enrollment-status + course_id path
-> AC-12: đọc course PUBLISHED, kiểm tra enrollment hiện có
-> DB.sql/ERD: courses + enrollments(user_id, course_id, status, timestamps)
-> response Enrollment source columns are known
-> enrollment selection predicate is SOURCE_REQUIRED
-> API #15 route/module/test: UNWIRED / NOT_FOUND
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Public endpoint vs user-scoped enrollment | Contract/diagram ghi Public; `enrollments` có `user_id` và không có user input | `SOURCE_REQUIRED / BLOCKING DISCREPANCY` | Không tự thêm JWT, query user_id hoặc chọn record ngẫu nhiên |
| Plan endpoint literal vs canonical endpoint | Một dòng plan ghi thiếu `/enrollment-status`; `list_api.md`, AC index và diagram ghi đầy đủ suffix | `DISCREPANCY` | DD dùng canonical source path và ghi Q-15-00 |
| HTTP 404 semantics | Contract chỉ ghi resource not found; chưa rõ course hay enrollment vắng | `SOURCE_REQUIRED` | Cần ghi Open Question, không thêm 422/409 |
| Course visibility predicate | AC-12 sequence có `Course PUBLISHED`; API row không ghi predicate | `DERIVED / NEEDS CONFIRMATION` | Ghi rõ source và không nâng thành runtime fact |
| Enrollment status enum/uniqueness | Schema có VARCHAR(20), không có enum/unique constraint đầy đủ | `SOURCE_REQUIRED` | Không invent enum hoặc duplicate handling |
| Runtime API #15 | `app/api/v1.py` và current module/test tree không có route | `UNWIRED / NOT_FOUND` | DD là design artifact, không phải implementation |

## CHANGES

- Planned files: DD pack API #15 và worklog này.
- CONTEXT_UPDATES: Không đổi runtime architecture, endpoint registry hoặc schema.
- Assumptions locked: giữ Public; read-only; mapping chỉ source-backed; `07_table.md` ghi N/A mutation.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` | Chọn 3/22 worklog cùng type và đã đọc đủ | `VERIFIED` |
| Đọc contract, AC-12, API index, diagram, schema và current route tree | Đã tách expected/current; xác nhận public/enrollment identity gap và API #15 chưa wired | `VERIFIED` |
| Authoring DD pack | Tạo đủ 8 sheet và 3 companion files tại `apps/study-server/docs/dd/15_courses_enrollment_status/` | `VERIFIED` |
| Static DD check | 8 sheets, front matter, relative links, Markdown tables, 3 JSON examples và template fingerprints | `VERIFIED` — `STATIC_VALIDATION_OK` |
| `git diff --check` | Không có whitespace error | `VERIFIED` |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | Context manifest hợp lệ khi bỏ qua drift | `VERIFIED` — `AGENT_CONTEXT_OK` |
| Full `validate-agent-context.mjs` | Báo `CONTEXT_STALE` repository-wide ở nhiều scope hiện hữu | `PARTIAL` — không thuộc phạm vi cập nhật context của DD docs-only |

## HANDOFF

- Remaining blockers: Contract chưa xác định user identity trong endpoint Public và semantics của 404.
- Next action: Review `OPEN_QUESTIONS.md`; sau khi chốt identity/404/visibility/selection policy mới có thể chuyển DD sang implementation-ready và triển khai runtime.
