---
title: "Verification Report — Study API #56 Lưu điểm"
order: 11
dd_id: "56"
api_name: "Lưu điểm bài làm Mentor"
source_sheet: "Verification Report"
status: "Draft — Needs Confirmation"
---

# Verification Report — Study API #56

## Kết quả

**PARTIALLY COMPLETED — STATIC DOCUMENT CHECKS ONLY.**

DD artifacts were checked against current static files. This does not prove API #56 runtime, live database schema, migrations, or an AC-23 end-to-end flow.

## Evidence reviewed

| Source | Result |
|---|---|
| API catalog row #56 | Method/path, actor, request descriptor, response, success and exact error set retained |
| API Guidelines | Error envelope requires data=null; safe field errors use meta.fieldErrors |
| Reusable Submission schema | All top-level fields and nested UploadAsset fields listed in Response Source Matrix |
| AC-23 index and activity diagram | Nodes and edges reviewed; sequence #54 list → #55 detail → grade input → #56 update grade/status → #57 feedback → success retained |
| Legacy DB table guide and DB.sql | assignment_submissions score/status and nullable legacy relations identified as candidates |
| V1-PILOT DB.sql | UUID assessment rubric schema is distinct; no inferred join to legacy submission |
| Current Study Server source | No API #56 route, module view.py or test exists |
| Current response/middleware source | error_response(None) emits data={}; exact-path DESIGN_CONTRACT_PATHS excludes the dynamic API #56 route |
| Template and workflow | Eight registered template files used; template appendix suffixes checked; Study workflow requires Markdown-only delivery |
| Archive scan | No archive/workbook under scoped Study Server docs or registered API DD resource folder |

## Contract checks

- Method/path: POST /api/v1/mentor/submissions/{submission_id}/grade.
- Required path: submission_id:int64!.
- Required body descriptors: score:int32! and rubric items:string!.
- Success: HTTP 200 DESIGN_RESOURCE_UPDATED.
- Response: ApiEnvelope<Submission>.
- Error set: exactly 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 404 DESIGN_RESOURCE_NOT_FOUND, 422 DESIGN_VALIDATION_ERROR, 500 DESIGN_INTERNAL_ERROR.
- No 400, 409, 503 or additional business code was added.
- The error example follows API Guidelines, not current error_response(None) serialization; future route wiring must resolve the data null/object discrepancy and dynamic-route business-code fallback.

## Artifact checks

| Check | Result |
|---|---|
| Expected artifacts | 11: eight template sheets, one table mapping, PLAN_RESULT.md, OPEN_QUESTIONS.md, VERIFICATION_REPORT.md |
| Template tails | PASS — appendix region compared byte-for-byte with corresponding source in all eight sheets |
| Front matter | PASS — required metadata present in all eight template sheets |
| Request/response field coverage | PASS — all catalog inputs, envelope fields and Submission/UploadAsset fields listed or marked SOURCE_REQUIRED |
| JSON examples | PASS — request and success/error examples parse as JSON |
| Relative links | PASS — local targets and anchors resolve |
| Markdown tables/fences/whitespace | PASS — column widths consistent, fences closed, no trailing whitespace |
| git diff --check | PASS — no diagnostics for tracked changes; custom scan also covered untracked DD files |

## Output SHA-256

Hashes cover all DD artifacts except this report, whose final hash is recorded in the task worklog to avoid a self-referential value.

| File | SHA-256 |
|---|---|
| 00_Cover.md | 895b58c2160508f8f7a7b6d5e47e28dd30bf75393fdf3ad08242ee16821133ef |
| 01_Lich_su.md | 27335dc3e98b0d520b4edc99fbd92342464ce642023534090854012d90e3e989 |
| 02_Overview.md | d44a006127c51fac869d70fad986c16c3e2ad9b06ab91a03ac3800d60edfd481 |
| 03_Request.md | ce1661356f55d63e90078800b9cecb156a641e69287a27b6900cfe5da497ace6 |
| 04_Response.md | 6ad84fdd6a1ba42378413ec7eb1a47ef8b904f51dc7940d594e321eb1f894052 |
| 05_Data_Mapping.md | c1ba93b18fe9d4b6c7f443e65a082080683c53b2d107f6206d0ab4b60632f946 |
| 06_Error.md | da177ade7da2d0c3d252d8cb0759e769dd7c9a9c947aba5c50c0a9b3254a9b01 |
| 07_assignment_submissions_update.md | d5e7b503c51a270e70fa3bb1aa021776aebcd883b3b424dc4c2c2d9f2e07737c |
| OPEN_QUESTIONS.md | 170ec1c6bbaa3106d8312d4bdbe4c4511046926aa54fd0fa497546d29674ea42 |
| PLAN_RESULT.md | e7e419bd03eb7a4244011e29031999de6e1b44f8ebfb5c690a11441812a1408f |

## Known gaps preserved

- Rubric field key, item encoding, validation and physical persistence are unresolved.
- Score int32 request versus decimal-string response and NUMERIC(6,2) candidate storage has no approved conversion/range rule.
- Mentor guard, token subject mapping, assigned-course policy and access masking are unresolved.
- files[] requires an asset resolver beyond the legacy single file_url column.
- Status preconditions, repeat grading, transaction/concurrency and history are unresolved.
- API #54 cardinality discrepancy remains open; the #54–#57 macro-review is recorded below.
- Current error_response() outputs data={} for None where API Guidelines specifies null; current middleware exact-path allowlist excludes API #56 and can use generic fallback codes. This is conditional future wiring drift.

## Verification boundary

- API #56 source wiring: UNWIRED / NOT_FOUND.
- Application tests: NOT_RUN; this is docs-only.
- Live DB/schema/migration: NOT_VERIFIED.
- AC-23 browser/client end-to-end: NOT_RUN.

## Rà soát vĩ mô AC-23 #54–#57

**Kết quả:** VERIFIED_WITH_OPEN_QUESTIONS.

- Thứ tự diagram nhất quán: #54 list → #55 detail/files/rubric → #56 grade/status → #57 feedback → success.
- #54 giữ response catalog dạng Submission đơn dù flow yêu cầu danh sách. Rubric API #55 đọc chưa có trong reusable Submission.
- Candidate API #56 chỉ ghi score/status; nơi lưu rubric items vẫn SOURCE_REQUIRED. API #57 cập nhật feedback riêng; không gộp hai mutation.
- Submission.files vẫn cần resolver UploadAsset được duyệt. attachments API #57 là dữ liệu riêng và chưa được ánh xạ; không tạo bảng hoặc response field giả định.
- Mentor principal/assignment mapping, giới hạn của direct-owner candidate và xử lý quan hệ null/orphan vẫn là câu hỏi chung.
- Giữ error set riêng theo catalog. Error helper trả data {} khác Guidelines yêu cầu null; dynamic Mentor routes cần mapping business code tường minh khi được wire.
- Không chạy runtime test hoặc AC-23 end-to-end.
