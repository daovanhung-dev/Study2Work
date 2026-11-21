---
title: "Verification Report — Study API #57 Lưu feedback"
order: 11
dd_id: "57"
api_name: "Lưu feedback bài nộp Mentor"
source_sheet: "Verification Report"
status: "Draft — Needs Confirmation"
---

# Báo cáo kiểm tra — Study API #57

## Kết quả

**VERIFIED_LOCAL_SOURCE_AND_TESTS_WITH_OPEN_QUESTIONS.** Route, request/response models, SQL/view flow, middleware mapping, focused HTTP tests and current OpenAPI were checked locally. This does not prove live schema, migration deployment, object storage, client compatibility or AC-23 end-to-end.

## Nguồn đã rà soát

| Nguồn | Kết quả |
|---|---|
| Catalog API và reusable schema | Đọc row #57, các row #54–#56, Submission, UploadAsset, ApiEnvelope; giữ nguyên descriptor và error set. |
| AC-23 index và diagram | Đọc actor, precondition, postcondition, toàn bộ node/edge; xác nhận #54 → #55 → #56 grade/status → #57 feedback → success. |
| DD #54–#56 | Rà response cardinality, files/rubric gaps, grade/status candidate, feedback ownership và open questions. |
| Legacy DB guide/DDL | assignment_submissions.feedback TEXT là nullable candidate; file_url là file bài nộp; quan hệ FK cho phép NULL trong DDL. |
| V1-PILOT DDL | assessment_reviews.feedback_markdown và rubric relations thuộc UUID assessment model; không có mapping được duyệt tới legacy BIGINT submissions. |
| Runtime source | API #57 route/module/view and middleware template are wired locally. Shared auth requires MENTOR; direct course owner, feedback overwrite and `feedback_text` wire key are DERIVED. |
| Templates/workflow | Tám template Markdown đã mở và hash; phụ lục được chép từ template; Study DD chỉ giao Markdown, không tạo ZIP. |
| Archive scan | Không có archive/workbook trong phạm vi docs Study và resource create_dd_api. |

## Kiểm tra hợp đồng

- Method/path giữ đúng: POST /api/v1/mentor/submissions/{submission_id}/feedback.
- Actor/auth giữ đúng: Bearer JWT; role Mentor.
- Path giữ đúng: submission_id:int64!.
- Body giữ nguyên hai descriptor: feedback text:string! và attachments:string!.
- Success giữ đúng: HTTP 200 DESIGN_RESOURCE_UPDATED.
- Response giữ đúng: ApiEnvelope<Submission>.
- Error set chính xác: 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 422 DESIGN_VALIDATION_ERROR; 500 DESIGN_INTERNAL_ERROR.
- Không thêm query, HTTP 400/409/503 hoặc business code khác.
- Runtime updates only candidate `assignment_submissions.feedback`; score/status remain unchanged. `attachments` is accepted as a required opaque string and is not persisted or returned because there is no supported target.

## Kiểm tra artifacts

| Kiểm tra | Kết quả |
|---|---|
| Manifest | Đủ 11 file: 8 sheets theo template, một mapping table candidate và ba report chuẩn. |
| Front matter | ĐẠT — metadata API #57 và trạng thái Draft — Needs Confirmation có ở cả 8 sheets. |
| Template appendix | ĐẠT — appendix mỗi sheet khớp byte-for-byte với template tương ứng. |
| Độ phủ request/response | ĐẠT — path, hai body descriptor, envelope và mọi field Submission/UploadAsset đều được liệt kê. |
| JSON | ĐẠT — request, success shape và error example parse được; placeholder được giải thích. |
| Liên kết | ĐẠT — relative link targets và anchors được kiểm tra. |
| Cấu trúc Markdown | ĐẠT — số cột bảng, code fence, Unicode và whitespace đã kiểm tra. |
| Source implementation | ĐẠT local source/import/OpenAPI — route and middleware template are present; no live service/deployment was exercised. |
| Focused API #57 tests | ĐẠT — 28 passed; tests use fake DB queries and one upstream Starlette/httpx deprecation warning. |
| Full Study Server suite | ĐẠT — 538 passed with the same upstream warning. |
| Ruff | ĐẠT — `uv run ruff check app tests`. |
| Diff whitespace | ĐẠT — `git diff --check`. |
| Context validator | BASELINE_INVALID — full validator reports missing DB Admin pages/source and broad dirty-source drift; `--skip-drift` leaves only DB Admin missing-source/context errors. No API #57 manifest path error was reported. |
| Live schema/migrations | CHƯA XÁC MINH — DDL candidate không chứng minh deployment. |

## Còn mở

- Contract approval for `feedback_text` wire key and the direct-owner identity mapping.
- Format/storage/response mapping of feedback attachments; current input is opaque and unused.
- Approval of overwrite behavior because diagram also says INSERT/UPDATE and no history relation is source-backed.
- Assigned-Mentor access and live null/orphan relation behavior.
- Response Submission.files resolver, rubric contract và result disclosure timing.
- Student result disclosure timing after #56 versus #57.

## Phạm vi kiểm chứng

- Wiring source API #57: VERIFIED locally by import/OpenAPI and TestClient route tests.
- API #57 focused tests: 28 passed; full Study tests: 538 passed.
- Flow client/runtime AC-23: NOT_RUN.
- Live schema/migration/deployment: NOT_VERIFIED.
- Trạng thái DD: Draft — Needs Confirmation.

## Rà soát vĩ mô AC-23 #54–#57

**Kết quả:** VERIFIED_WITH_OPEN_QUESTIONS.

| API | Vai trò trong flow | Kết luận liên kết |
|---|---|---|
| #54 | Đọc submissions để chọn một bài nộp | User asked the agent to decide the three ambiguities using recommendations; current `Page<Submission>`, default page 1/size 20, newest-first ordering and constrained UploadAsset match remain DERIVED. Tests use fake DB; live/client compatibility remain unverified. |
| #55 | Đọc submission, files và rubric | Reusable Submission chưa có rubric; files[] should reuse API #54's DERIVED lookup, with API #35 compatibility open. |
| #56 | Lưu score và status GRADED | Candidate chỉ ghi score/status; key, schema và nơi lưu rubric items chưa được xác nhận. |
| #57 | Lưu feedback sau bước chấm | Runtime updates feedback only under a DERIVED overwrite fallback; opaque attachments are not persisted. Contract approval and attachment storage remain open. |

- Không gộp mutation score/status với feedback; chưa có quy tắc về thời điểm Student nhìn thấy kết quả.
- Mentor identity/assignment access, nullable/orphan references và direct-owner predicate vẫn là câu hỏi chung.
- Error sets remain per API; `data:null` is current shared behavior and dynamic #57 error mapping is wired locally.
- API #57 route tests ran locally; AC-23 end-to-end and live database checks were not run.
