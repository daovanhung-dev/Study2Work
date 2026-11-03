---
task_id: "2026-11-01-fix-study-api-null-bind-parameters"
date: "2026-11-01"
primary_task_type: "fix"
secondary_task_types: ["coding", "test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "COMPLETE"
---

# Worklog: Sửa lỗi nullable PostgreSQL bind của Study Server

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `fix`
- selector_command: `node scripts/select-worklogs.mjs --type fix --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/remove-unicode-encode-catch-access-token.md`
    - carry_forward: Bảo toàn HTTP mapping/trace; ghi rõ validator global nếu baseline ngoài Study vẫn lỗi.
  - path: `.agents/worklog/2026-10-25/remove-valueerror-study-server.md`
    - carry_forward: Giữ error mapping qua `error_response(...)`; bảo toàn các file dirty ngoài task.
  - path: `.agents/worklog/2026-10-25/restore-errordetail-study-server.md`
    - carry_forward: Giữ nguyên wire response và error envelope; context validator có baseline thiếu DB Admin.
- shortage: `none` (3 matching fix worklogs đã được đọc)

## EXPECTED_BEHAVIOR

- Requirement: Sửa 10 truy vấn PostgreSQL làm API #7, #54, #58, #68, #73, #78, #82, #87, #92 và #97 trả HTTP 500; không đổi route, filter, auth hoặc response contract.
- Canonical contract: Giữ nguyên API/DD semantics, bao gồm predicate tùy chọn; chỉ định kiểu cho nullable binds tại SQL boundary.
- User scope decision: Chỉ sửa 10 lỗi API; lỗi global `validate-agent-context` thuộc phạm vi riêng. API #98 và discrepancy DD/source không thuộc task này.

## CURRENT_BEHAVIOR

- Source/runtime: Baseline trước sửa dùng pattern `:field IS NULL OR ...`; branch-backed HTTP run tái hiện PostgreSQL `AmbiguousParameter` và trả 500. Sau sửa, query constants cast explicit nullable binds và cả 10 route chạy HTTP với filter rỗng/giá trị trên branch tạm.
- Schema evidence: Checked-in Study legacy DDL mô tả BIGINT cho các ID và VARCHAR/TEXT cho filter strings; production branch không được ghi.
- Tests: Fake-session tests pass nhưng không xác minh suy luận kiểu bind của PostgreSQL. Neon's branch skill cho phép realistic branch; Neon CLI không có trong PATH nên dùng Neon MCP.
- Existing worktree: Context, API #98 test/report và OpenAPI assertion changes từ lượt test trước đang dirty; giữ nguyên, không ghi đè.

## SOURCE_TRACE

```text
route -> API view validates/authenticates and binds optional filters -> query constant -> SQLAlchemy text()/psycopg -> PostgreSQL parse/type inference -> safe error_response or page response -> API tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Nullable bind SQL types | Ten list/search operations failed on baseline PostgreSQL; post-fix filtered/unfiltered HTTP and SQL tests pass. | `FIXED_AND_LIVE_VERIFIED` | Explicit casts type each nullable bind in both `IS NULL` and comparison expressions without changing predicate logic. |
| Global context validator | Prior run exits nonzero for missing web-work/study-web and db-admin context/source plus broad source drift. | `OUT_OF_SCOPE` | Run as required after context edits and record existing baseline failures; do not repair other scopes. |

## CHANGES

- Thêm cast kiểu rõ trong SQL constants của 10 API: #7 q pattern TEXT; #54/#58 course ID BIGINT và status VARCHAR; #68 role/status VARCHAR, keyword TEXT; #73 status VARCHAR, mentor ID BIGINT; #78 content type TEXT, course ID BIGINT; #82/#87 course ID BIGINT, status VARCHAR; #92 status TEXT, channel VARCHAR; #97 reason/severity VARCHAR.
- Cập nhật test expression assertions, thêm assert cho nullable filters và count/list cast consistency. Giữ nguyên route, authorization, filter semantics và response.
- Cập nhật report sau sửa, giữ nguyên baseline HTTP 59/69 và danh sách 10 lỗi làm lịch sử; kết quả follow-up riêng cho nhóm sửa là 20/20 HTTP requests pass.
- Context pages cập nhật: `.agents/server-study/AGENTS.md`, `architecture.md`, `apis/declared-routes.md`, `core/runtime.md`, `tests.md`, `workflows/README.md`. API #98 discrepancy giữ nguyên.
- Assumptions: temporary normal Neon branch từ snapshot production chỉ dùng cho migration/fixture test; email/object storage stub; branch đã bị xóa sau verification.

## VERIFICATION

| Command / action | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type fix --limit 3` | Three matching worklogs selected and read. | VERIFIED_PREFLIGHT |
| Neon CLI availability | `neon` CLI unavailable; use Neon MCP branch tools per skill fallback. | VERIFIED |
| Focused 10-module suite | `uv run pytest -q tests/modules/guest/api_07_courses_search tests/modules/mentor/api_54_mentor_submissions_list tests/modules/mentor/api_58_mentor_support_requests tests/modules/admin/api_68_admin_users_list tests/modules/admin/api_73_admin_courses_list tests/modules/admin/api_78_admin_content_pending tests/modules/admin/api_82_admin_lessons_list tests/modules/admin/api_87_admin_quizzes_list tests/modules/admin/api_92_admin_notifications_list tests/modules/admin/api_97_admin_discussions_reported` → 178 passed. | VERIFIED |
| Full Study suite | `uv run pytest -q` → 1326 passed, 0 failed, one upstream Starlette/httpx deprecation warning. | VERIFIED |
| Ruff and diff | `uv run ruff check app tests`; `git diff --check` → pass. | VERIFIED |
| Branch-backed HTTP | Migrated temporary Neon branch, Student register + login, Mentor/Admin fixture login; Uvicorn loopback; ten operations called with empty and matching filters → 20/20 HTTP 200; no external email/object storage. | VERIFIED |
| Neon cleanup | Deleted `br-flat-dew-b3ongn2c`; searched by temporary branch name and confirmed `[]`. | VERIFIED |
| Context validator | Exit 1 `AGENT_CONTEXT_INVALID`: missing `web-work/study-web` and `db-admin` context/source, broken links for those scopes and `CONTEXT_STALE` across repo including Study. Recorded as existing cross-scope/context baseline; left out of scope per user choice. | VERIFIED_WITH_OUT_OF_SCOPE_FAILURES |

## HANDOFF

- Remaining blockers: None for the ten PostgreSQL nullable-bind failures. Global validator remains failing outside the approved scope; API #98 contract discrepancy remains unchanged.
- Next owner/action: Review and merge the ten SQL cast fixes, test updates, report and Study context changes.
