# Báo cáo kiểm chứng — API #91 Thống kê quiz

## Phạm vi

- Tài liệu: `apps/study-server/docs/dd/91_admin_quizzes_statistics/`.
- Trạng thái DD: `Draft — Needs Confirmation`.
- Runtime, route, module và test của API #91: `SOURCE_BACKED` locally.
- API #91 focused HTTP tests: 19 passed; linked #87–#91 regression: 104 passed; full Study suite: 1197 passed. Đây là verification local với fake DB, không phải live database verification.
- Live DB: `NOT_VERIFIED`; DDL legacy và V1-PILOT là hai mô hình riêng.

## Truy vết nguồn

- Catalog #91: `GET /api/v1/admin/quizzes/{quiz_id}/statistics`, Admin Bearer JWT, `quiz_id:int64!`, response trực tiếp `ApiEnvelope<Quiz>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, đúng lỗi 401/403/404/500.
- AC-35 diagram: nhánh STATISTICS gọi #91, aggregate attempt statistics rồi hiển thị; diagram không định nghĩa metric hoặc response fields.
- AC-16 diagram: #29 tạo attempt `IN_PROGRESS`; #30 lưu answer; #31 nộp và chuyển nhánh `PENDING_GRADE`/`GRADED`; #32 đọc kết quả. Các nhãn này không tạo thành enum đầy đủ.
- Legacy DDL là nguồn candidate cho `quizzes` 1:N `quiz_attempts`; `submitted_at` và `score` nullable. V1-PILOT dùng UUID `assessments`/`assessment_attempts`/`assessment_answers`, không được gộp vào model BIGINT của API.
- Đã đối chiếu DD #87–#90 và #29–#32 cho list visibility, update/delete, attempt history và result.

## Template

- Dùng đủ tám file trong `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/`.
- Manifest SHA-256: `541b6ea0c36c5781c1b62574e1aba4e2fab5fde2f949a54129a123c63b78b9c2` (SHA-256 của các dòng `filename:file_sha256`, sắp xếp theo filename).
- Study workflow giao thư mục Markdown, không tạo ZIP.

## Kiểm tra tĩnh

| Hạng mục | Kết quả | Trạng thái |
|---|---|---|
| Package | 11 file: 8 sheet và 3 report | PASS — 11/11 |
| Template appendix | Tám appendix so khớp byte-for-byte với template | PASS — 8/8 |
| Catalog contract | GET/path/auth/response/status và đúng bốn error code được giữ nguyên | PASS |
| Response/query mapping | Tách contract `ApiEnvelope<Quiz>` khỏi `QuizStatistics` proposal; các metric và nguồn candidate được đánh dấu DERIVED/SOURCE_REQUIRED | PASS — static |
| JSON examples | Parse ví dụ contract và các proposal | PASS — 5/5 |
| Markdown tables/fences | 33 bảng, 450 dòng bảng nhất quán; code fences cân bằng | PASS |
| Relative links/anchors | 28 relative link target tồn tại; bốn anchor của data mapping có target | PASS |
| Whitespace/newline | Không có trailing whitespace; mọi file có final newline | PASS |
| AC-35 macro-review | Rà soát #87–#91 cùng ranh giới attempt AC-16 #29–#32 | VERIFIED_WITH_OPEN_QUESTIONS |
| API #91 HTTP tests | 19 passed; ADMIN-before-path/DB, bounds, aggregate/null branches, errors, trace, read-only behavior and OpenAPI | PASS — local fake DB |
| Linked quiz regression | #87–#91: 104 passed | PASS — local fake DB |
| Full Study suite | `.venv/bin/pytest -q`: 1197 passed; one upstream Starlette/httpx TestClient deprecation warning | PASS — local |
| Ruff | `.venv/bin/ruff check app tests` | PASS |
| Scoped formatting | Changed API #91 source/test, router and middleware pass `ruff format --check` | PASS |
| OpenAPI | 53 `/api/v1` path templates / 62 operations; #91 has exact 200/401/403/404/500, int64 path and aggregate IDs/counts, Authorization, no body/query | PASS — local schema |

## Kết quả và giới hạn

- Mục tiêu statistics trong AC-35 xung đột với response `ApiEnvelope<Quiz>` trong diagram/catalog. Runtime local dùng `ApiEnvelope<QuizStatistics>` là fallback DERIVED riêng; không nhập metrics vào reusable `Quiz`, không sửa catalog/diagram, DD vẫn Draft.
- `attempt_count`, `submitted_attempt_count`, `graded_attempt_count`, `average_score`, `passed_attempt_count` và `pass_rate` là các định nghĩa đề xuất; ngưỡng điểm nullable, scale/rounding và cách xử lý dữ liệu bất thường cần xác nhận.
- Shared ADMIN guard và route-template allowlist chạy trước truy vấn; fine-grained quiz-management policy vẫn chưa có source.
- Invalid/malformed/overflow path được map về catalog 404 theo fallback DERIVED; error helper trả `data:null`.
- SQL aggregate chạy trên checked-in legacy BIGINT candidate; tests dùng fake DB và không xác minh live schema, PostgreSQL execution, deployment hoặc owner approval.

## AC-35 macro-review #87–#91 — document-level

- Trạng thái: `VERIFIED_WITH_OPEN_QUESTIONS`; đây là review nhất quán tài liệu, không phải quyết định được duyệt hoặc runtime verification.
- Đề xuất chung đều `DERIVED`: #90 soft-delete quiz có attempt và giữ questions/choices/attempts/answers; chỉ đề xuất hard-delete khi không có attempt; #87 ẩn tombstone mặc định; #89 không cập nhật quiz tombstone và đề xuất chặn thay đổi có history; #29 không tạo attempt mới sau tombstone; #30–#31 có thể tiếp tục attempt đã tạo; #32 vẫn đọc kết quả đã giữ; #91 aggregate history nếu quiz row còn tồn tại.
- Nếu quiz bị hard-delete hoặc không tồn tại, #91 dùng 404 trực tiếp từ catalog. Lock/race, enum/timestamp tombstone, in-flight policy, access, response, metrics và schema vẫn cần xác nhận.
- Coding pass đã thêm runtime và HTTP tests; không sửa schema, catalog hoặc diagram. Application verification được ghi ở phần trên.
