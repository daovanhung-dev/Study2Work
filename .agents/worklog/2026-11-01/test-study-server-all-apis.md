---
task_id: "2026-11-01-test-study-server-all-apis"
date: "2026-11-01"
primary_task_type: "test"
secondary_task_types: ["docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Kiểm thử toàn bộ Study Server API đã code

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `test`
- selector_command: `node scripts/select-worklogs.mjs --type test --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-11/test-study-api13-avatar-quick.md`
    - carry_forward: API #13 tests use injected storage/S3 stubs; do not infer remote storage verification.
  - path: `.agents/worklog/2026-09-21/build-work-projects.md`
    - carry_forward: isolate verification to the requested target and report actual command availability.
  - path: `.agents/worklog/2026-09-18/work-server-api-tests.md`
    - carry_forward: fake-backed HTTP tests do not connect to live Neon; distinguish them from DB-backed checks.
- shortage: `none` (3 matching worklogs available; all selected logs were read)

## EXPECTED_BEHAVIOR

- Requirement: đọc DD trước khi test; tạo báo cáo Markdown có một trạng thái cho từng operation; kiểm tra mọi API module đã code qua local HTTP; dùng branch Neon riêng; tạo dữ liệu/token cần thiết; stub email/storage; xóa branch sau khi lưu báo cáo.
- Phạm vi DD: 66 API module hiện có gồm 67 operation module (API #3 có login và refresh), cộng 2 utility operation trong 69 `/api/v1` operation. Kiểm tra riêng `/`, `/health/live`, `/health/ready`.
- Canonical contract: DD/status được giữ theo từng file; phần `Draft`, `DERIVED`, `UNWIRED` và open question không được xem là quyết định đã duyệt. API #99–#103 chỉ có DD, không kiểm tra runtime.

## CURRENT_BEHAVIOR

- Source hiện khai báo 58 path template / 69 operation dưới `/api/v1`; có 66 API module source, trong đó API #3 có login và refresh. API #98 có source/route nhưng DD còn ghi Draft/UNWIRED.
- DD cho tất cả 66 module được rà trước khi tạo fixture và gọi HTTP; status DD và endpoint được lập trong báo cáo.
- Neon branch tạm `codex-study-api-test-2026-11-01` kế thừa snapshot production. Đã đối chiếu schema `dao_van_hung`; branch có 16 bảng trước migrations và 30 bảng sau khi áp dụng checked-in migrations 002–014. Mọi fixture/migration chỉ ở branch.
- Full test suite sau thêm 9 characterization tests cho API #98 và sửa bốn OpenAPI assertions stale: **1324 passed, 0 failed**, một Starlette/httpx deprecation warning.
- Local Uvicorn HTTP run: 69/69 `/api/v1` operations được gọi; 59 PASS / 10 FAIL. Mười list/search query operation lỗi HTTP 500 do PostgreSQL không suy luận được kiểu của nullable bind parameter. API #99–#103 không có route/module nên NOT_RUN.
- Email và object storage được stub. Không xác minh provider, production schema/data hoặc deployment Ubuntu.

## SOURCE_TRACE

```text
DD review -> route/module/test inventory -> temporary Neon branch/schema -> seeded role/data -> local Uvicorn with injected Settings -> HTTP matrix -> report -> branch deletion
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #98 | DD `Draft — Needs Confirmation`/`UNWIRED`; source có GET detail, tự dựng title từ content và không đọc report relation. Thêm characterization tests. | `DISCREPANCY` | Report chỉ mô tả source hiện tại; title/report/status chưa được coi là contract đã duyệt. |
| API #14 | Source schema không có cột `bio`; PUT trả 200 nhưng field không được lưu/trả như DD. | `DISCREPANCY` | Giữ kết quả HTTP pass kèm sai lệch source/DD trong report. |
| API #3 refresh | Route test pass, DD #3 chỉ mô tả login; Q-03-04 còn mở. | `DD_GAP` | Có dòng riêng trong ma trận; không tuyên bố DD refresh đã được phê duyệt. |
| APIs #7, #54, #58, #68, #73, #78, #82, #87, #92, #97 | HTTP 500 `DESIGN_INTERNAL_ERROR`; PostgreSQL `AmbiguousParameter` với nullable bind dạng `:field IS NULL OR ...`; tái hiện trên branch test. | `FAIL` | Đã báo cáo; không sửa source trong task test. |
| `create_app(Settings)` harness | Lần thử đầu tạo DB dependency override trả generator như object và API #1 trả 500; harness đổi sang app composition mặc định với Settings test được inject trước khởi tạo. | `TEST_SETUP_ISSUE / WORKAROUND` | Kết quả cuối chạy route + DB dependency thật trên branch test; không chỉnh source runtime. |
| APIs #99–#103 | Chỉ có DD; không có module/route trong Study Server. | `NOT_RUN` | Không tuyên bố đã xác minh runtime. |
| Provider/schema boundary | Email/storage dùng stub; Neon branch tạm bị xóa sau báo cáo. | `STUBBED / ISOLATED` | Không có ghi production; không xác minh tích hợp thật hoặc deployment. |

## CHANGES

- Tạo `apps/study-server/docs/testing/api-test-report-2026-11-01.md` với 69 dòng matrix, ba system route, DD status, kết quả negative/auth, flow phụ thuộc và mười lỗi DB-backed.
- Thêm `tests/modules/admin/api_98_admin_discussions_detail/test_admin_discussion_detail.py` với 9 characterization tests.
- Sửa OpenAPI count assertions lỗi thời trong API #92–#95 test modules: 57/68 → 58/69.
- Cập nhật context hiện hành: `.agents/server-study/AGENTS.md`, `tests.md`, `apis/declared-routes.md`, `core/runtime.md`, `architecture.md`, `modules/README.md`, `workflows/README.md`.
- CONTEXT_UPDATES: ghi nhận API #98 route/source mismatch, 58 path templates / 69 operations, 1324 tests, kết quả HTTP PostgreSQL-backed.
- Assumptions/boundary: app chạy trên loopback; branch test kế thừa snapshot production nhưng chỉ branch đó nhận migrations/fixtures; sau khi báo cáo hoàn tất đã xóa branch Neon và xác nhận không tìm thấy branch theo tên. Không ghi production.

## VERIFICATION

| Command / action | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type test --limit 3` | Đã đọc đủ ba worklog `test` được chọn ở preflight. | VERIFIED_PREFLIGHT |
| DD review trước test | Rà cover/overview/request/response/error/open-questions của 66 API DD; API #99–#103 xác nhận chỉ có DD. | VERIFIED |
| Neon branch + migrations | Tạo branch cô lập; áp dụng migrations checked-in 002–014 trên branch; không ghi production. | VERIFIED |
| Local Uvicorn HTTP matrix | Đủ 69 `/api/v1` operations: 59 PASS / 10 FAIL; system routes 3/3 PASS; 57/57 protected missing-Bearer probes 401; role 403, validation 422, conflict 409, not-found 404 probes đúng. | VERIFIED_WITH_API_FAILURES |
| Focused regression | API #98 + #92–#95: `96 passed`. | VERIFIED |
| Full suite | `uv run pytest -q`: `1324 passed, 1 warning` trong 164.34s. | VERIFIED |
| Ruff | `ruff check` và `ruff format --check` trên test files đã đổi đều pass. | VERIFIED |
| `node scripts/validate-agent-context.mjs` | Exit 1: phát hiện missing context/source roots cho `web-work/study-web` và `db-admin`, cùng nhiều `CONTEXT_STALE` entry hiện hành (bao gồm Study source inventory). Không phát hiện riêng broken link của các Study pages vừa cập nhật. Không sửa scope ngoài task. | BLOCKED_BY_EXISTING_GLOBAL_CONTEXT_DRIFT |
| Neon branch cleanup | Xóa branch tạm; `list_branches` search theo tên trả danh sách rỗng. | VERIFIED |

Chi tiết từng API: [`api-test-report-2026-11-01.md`](../../../apps/study-server/docs/testing/api-test-report-2026-11-01.md).

## HANDOFF

- Follow-up: mười lỗi nullable PostgreSQL bind đã được sửa và xác minh lại bằng HTTP (20/20 request pass); xem `.agents/worklog/2026-11-01/fix-study-api-null-bind-parameters.md`.
- API #98 cần quyết định DD/contract riêng về report relation, title và thread shape trước khi reconcile source.
- Task test/report và follow-up fix đã hoàn tất; không còn branch/data thử tồn tại trên Neon.
