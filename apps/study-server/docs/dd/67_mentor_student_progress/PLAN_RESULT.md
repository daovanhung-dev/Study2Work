# PLAN_RESULT — Study API #67

## Kết quả theo plan

| Plan item | Kết quả |
|---|---|
| Exact catalog contract | Giữ GET `/api/v1/mentor/courses/{course_id}/students/{student_id}/progress`, Bearer JWT/Mentor, hai path int64 bắt buộc, không query/body, `ApiEnvelope<Page<Course>>`, HTTP 200 và lỗi đúng 401/403/404/500. |
| AC-26 trace | Đã đọc AC-26 index và full diagram: #65 class progress → #66 learning events → chọn Student → #67 đọc Student progress. Không tạo API-to-API call. |
| Related DD review | Đã đọc #65/#66 và đối chiếu #21/#25/#37/#62; dùng #65 làm candidate consistency boundary, không lấy #37 làm direct contract cho #67. |
| Current source | #67 không có route/module/focused test; Mentor guard absent; path chưa allowlist. API #9 current source lọc course/lesson PUBLISHED và sort theo `sort_order,id`. |
| Database evidence | Legacy BIGINT progress rows là candidate, nullable và không có unique user/lesson; V1-PILOT dùng UUID facts/snapshot và không có per-lesson percent tương đương. Live schema chưa xác minh. |
| Direct vs derived | Giữ Course/PageMeta direct schema. `StudentCourseProgress`, per-lesson detail, eligibility, missing-row rule và formula đều đánh dấu DERIVED/SOURCE_REQUIRED. |
| AC-26 macro-review | #65 class summary, #66 event analytics, #67 one-Student detail; common lesson denominator/formula boundary documented. Contract mismatch/pagination/auth/schema questions remain open. |
| Deliverables | 8 template sheets + 3 reports trong folder Markdown; `07_table.md` N/A — READ-ONLY API; không tạo ZIP/runtime/schema/catalog/diagram/context changes. |
| Verification | Static checks ghi trong VERIFICATION_REPORT; không chạy application tests. |

## API Requirement Matrix

| API ID | Method/path | Auth/input | Success/response | Errors |
|---|---|---|---|---|
| #67 | `GET /api/v1/mentor/courses/{course_id}/students/{student_id}/progress` | Bearer JWT; Mentor; `course_id:int64!`, `student_id:int64!`; no query/body | 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Page<Course>>` | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR` |

## Ma trận và ranh giới logic

| Nhóm | Kết quả |
|---|---|
| Request Usage | Bearer Mentor scopes the course; `student_id` is not authorization by itself; no pagination/filter input. |
| Query | Q1 course scope; Q2 roster membership; Q3 published lessons; Q4 student lesson state; all physical mapping remains schema candidate, not approved SQL. |
| Mutation | N/A — READ-ONLY API. |
| Response Source | Direct contract Course/PageMeta is preserved but does not carry progress; candidate single `StudentCourseProgress` object is DERIVED. |
| Shared candidate formula | #65/#67 both use PUBLISHED lesson denominator, completed status, floor average and zero for empty denominator. Each rule still requires approval. |
| Separation | #66 reads a learning-event source not found; #67 reads current progress state and does not count events. |

## Fingerprints — registered template SHA-256

| Sheet | SHA-256 |
|---|---|
| `00_Cover.md` | `fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63` |
| `01_Lich_su.md` | `d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e` |
| `02_Overview.md` | `c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6` |
| `03_Request.md` | `37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa` |
| `04_Response.md` | `5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8` |
| `05_Data_Mapping.md` | `11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b` |
| `06_Error.md` | `e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b` |
| `07_table.md` | `4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356` |
