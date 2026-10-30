# VERIFICATION_REPORT — Study API #59

## Kết quả

- DD status: `Draft — Needs Confirmation`; local schema, owner/access policy, message visibility and attachment projection remain `DERIVED`, not business-owner approval.
- Runtime API #59: `SOURCE_BACKED_LOCAL`; route, module and focused HTTP tests are wired. Tests use fake DB rows and do not establish live schema or deployment behavior.
- Scope: API #59 DD, read-only route/module/tests, exact middleware contract registration and affected `server-study` context/manifest/worklog. No new migration or live DB operation.
- Output remains Markdown-only; no ZIP is created under the Study workflow.

## Deliverable manifest

| Nhóm | File |
|---|---|
| Sheets | `00_Cover.md`, `01_Lich_su.md`, `02_Overview.md`, `03_Request.md`, `04_Response.md`, `05_Data_Mapping.md`, `06_Error.md`, `07_table.md` |
| Reports | `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md` |
| Tổng | 11 Markdown files; không tạo ZIP theo Study workflow. |

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Skill/template registry | `createDD-markdown` được wire cho `server-study`; bộ template Markdown được giữ trong các sheet. | PASS |
| Template appendix | Các appendix đối chiếu nguồn Excel được giữ nguyên qua cập nhật nội dung chính. | PASS |
| Front matter | Tám sheet giữ `dd_id: "59"` và `Draft — Needs Confirmation`. | PASS |
| API contract | GET path, Mentor Bearer, required int64 path, no body/query, singleton response, 200 success và đúng 4 error codes khớp catalog. | PASS |
| Response mapping | Response tái dùng SupportRequest/UserSummary/SupportMessage/UploadAsset của API #58; mọi fallback được đánh dấu DERIVED. | PASS |
| Focused HTTP tests | API #59: 13 passed; trace, owner checks, full thread/assets, empty thread, invalid/missing path, broken parent/link, safe DB failure và OpenAPI được kiểm tra bằng fake DB. | PASS |
| Full Study suite | 563 passed, 1 upstream Starlette/httpx deprecation warning. | PASS |
| Ruff | `uv run ruff check app tests`: all checks passed. | PASS |
| OpenAPI | 29 `/api/v1` path templates, 30 operations; `request_id` là integer/int64 và `data` là singleton object. | PASS |
| Diff whitespace | `git diff --check` không báo lỗi. | PASS |
| Live DB/deployment | Không truy cập live DB và không apply migration 008. | NOT VERIFIED |
| Context validator | Kết quả và lỗi baseline được ghi trong worklog; không sửa scope DB Admin ngoài task. | SEE WORKLOG |
| AC-24 macro-review | #58 list → #59 detail → #60 reply → #61 resolve; #59 chỉ đọc request/thread. | VERIFIED_STATIC |

## Local implementation decisions

- Reuse API #58 legacy BIGINT `support_requests`, `support_messages` and `support_message_uploads`; this is a checked-in local fallback only.
- Use numeric Mentor JWT `sub` and direct `courses.mentor_id` ownership in request and thread queries.
- Missing request and malformed/out-of-range signed-int64 path return 404; extant request owned by another Mentor returns 403.
- Return the full message thread in `created_at ASC, id ASC` order; empty thread is `[]`. The selected schema has no internal-message flag.
- Resolve linked UploadAsset rows by owner, course, role-purpose and `UPLOADED`, ordered by link position. A broken linked projection returns safe 500 rather than partial data.
- Keep API #58 response model and omit nullable avatar/resolved fields per current runtime convention.

## Remaining verification limits

- Migration 008 is a checked-in artifact; its application and the live database schema were not inspected.
- Fake DB HTTP tests verify local orchestration and response mapping only; they do not prove live support relations, migration state, deployed authorization or storage URL reachability.
- DERIVED choices, including full-thread visibility and the 403-versus-404 privacy policy, remain subject to business-owner review.

Xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) và [PLAN_RESULT.md](./PLAN_RESULT.md).
