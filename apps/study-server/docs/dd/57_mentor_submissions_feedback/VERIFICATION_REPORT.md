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

**VERIFIED_STATIC_ONLY_WITH_OPEN_QUESTIONS.** Bộ tài liệu được đối chiếu tĩnh với catalog, diagram AC-23, DD liên quan, DDL candidate và source hiện tại. Kết quả không chứng minh API runtime, live schema, migration hay AC-23 end-to-end.

## Nguồn đã rà soát

| Nguồn | Kết quả |
|---|---|
| Catalog API và reusable schema | Đọc row #57, các row #54–#56, Submission, UploadAsset, ApiEnvelope; giữ nguyên descriptor và error set. |
| AC-23 index và diagram | Đọc actor, precondition, postcondition, toàn bộ node/edge; xác nhận #54 → #55 → #56 grade/status → #57 feedback → success. |
| DD #54–#56 | Rà response cardinality, files/rubric gaps, grade/status candidate, feedback ownership và open questions. |
| Legacy DB guide/DDL | assignment_submissions.feedback TEXT là nullable candidate; file_url là file bài nộp; quan hệ FK cho phép NULL trong DDL. |
| V1-PILOT DDL | assessment_reviews.feedback_markdown và rubric relations thuộc UUID assessment model; không có mapping được duyệt tới legacy BIGINT submissions. |
| Runtime source | Không có API #57 route/module/test. Shared auth hiện Student-only; error helper và middleware discrepancies được ghi là future wiring gaps. |
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
- Mutation candidate chỉ cập nhật assignment_submissions.feedback; chưa có persistence target cho attachments.

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
| Source implementation | ĐẠT ở mức static scan — không thấy route/module/test API #57; điều này không chứng minh runtime. |
| Application tests | CHƯA CHẠY — docs-only; API #57 chưa có test module. |
| Live schema/migrations | CHƯA XÁC MINH — DDL candidate không chứng minh deployment. |

## Còn mở

- Wire key của feedback text.
- Format, persistence, access policy và response mapping của attachments.
- Repeated-call overwrite/history semantics dù diagram ghi INSERT/UPDATE.
- Mentor claim/assignment mapping và null/orphan behavior.
- Response Submission.files resolver, rubric contract và result disclosure timing.
- Error data null/object mismatch và dynamic middleware path mapping.

## Phạm vi kiểm chứng

- Wiring source API #57: UNWIRED / NOT_FOUND.
- Application tests: NOT_RUN.
- Flow client/runtime AC-23: NOT_RUN.
- Trạng thái DD: Draft — Needs Confirmation.

## Rà soát vĩ mô AC-23 #54–#57

**Kết quả:** VERIFIED_WITH_OPEN_QUESTIONS.

| API | Vai trò trong flow | Kết luận liên kết |
|---|---|---|
| #54 | Đọc submissions để chọn một bài nộp | Response catalog vẫn là một Submission dù endpoint và flow mang nghĩa danh sách; giữ câu hỏi mở, không tự đổi sang Page. |
| #55 | Đọc submission, files và rubric | Reusable Submission chưa có rubric; files[] chưa có asset resolver. |
| #56 | Lưu score và status GRADED | Candidate chỉ ghi score/status; key, schema và nơi lưu rubric items chưa được xác nhận. |
| #57 | Lưu feedback sau bước chấm | Candidate cập nhật feedback riêng; format, persistence và mapping response của attachments chưa rõ. |

- Không gộp mutation score/status với feedback; chưa có quy tắc về thời điểm Student nhìn thấy kết quả.
- Mentor identity/assignment access, nullable/orphan references và direct-owner predicate vẫn là câu hỏi chung.
- Giữ riêng error set theo từng API; data null/object và dynamic route mapping là gap tích hợp tương lai.
- Không chạy runtime test hoặc AC-23 end-to-end; đây là rà soát tài liệu.
