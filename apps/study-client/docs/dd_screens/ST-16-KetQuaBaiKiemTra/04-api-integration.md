# ST-16 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-16-API-001` | #32 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #32
- Orchestration/data notes: GET #32 sau accepted #31; pending hiển thị trạng thái, không suy ra score=0; `GRADED` không tự nghĩa là pass; chỉ render field được phép theo response/disclosure policy.
- BE/source status và gate: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** API #32 Draft Q-32-01…06 còn mở về ownership, pending score, answer/feedback disclosure, shape/order và path/error; Student #32 route/module/test NOT_FOUND; Study Web UNWIRED; legacy BIGINT và V1-PILOT UUID attempt/answer models lệch, adapter/live schema chưa xác minh; PNG loaded Student và HTML unavailable Guest khác nhau, cả hai chưa khớp design target; screenshot fields/CTAs thiếu nguồn
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: A.4. API #32 contract và giới hạn

| Thuộc tính | API catalog / DD hiện có | Giới hạn cần giữ |
|---|---|---|
| Method/endpoint | `GET /api/v1/attempts/{attempt_id}/result` | Contract design-only; current Student route/module/test không tồn tại. |
| Authentication | Bearer JWT, role Student | Không truyền `user_id`; backend owner predicate chưa chốt. |
| Path | `attempt_id:int64!` | Không có min/max/range/parse mapping cụ thể; catalog không có 400/422. |
| Query/body | Không khai báo | Không thêm query/body/Content-Type. |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<QuizAttempt>` | Response DD Draft. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR` | 403-vs-404 cho attempt của user khác chưa chốt; không thêm 409/422. |
| Logical fields | `id`, `quiz_id`, `status`, `started_at`, `submitted_at?`, `score?`, `answers[]`; `QuizAnswer` có `question_id`, `choice_ids?`, `text_answer?`, `correct?`, `score?` | Projection, ordering, nullable/omit rule và field disclosure còn mở. |

API #32 DD `Draft — Needs Confirmation` nêu Q-32-01…06: ownership/masking; availability và score khi `PENDING_GRADE`; tiết lộ correctness/điểm câu; feedback field; answer shape/order; path/error mapping. AC-16 có “feedback” nhưng response schema và candidate tables không có feedback. Không tự thêm field hoặc API khác để lấp khoảng trống.

### Trích từ DD nguồn: A.5. Database candidates and visual-system alignment

**Database contract discrepancy:** API #32 catalog uses an int64 `attempt_id` and the reusable logical `QuizAttempt`/`QuizAnswer` schema. The legacy Study Server DDL has BIGINT `quiz_attempts`/`quiz_answers`, nullable attempt score/submission time, and one selected `choice_id` per answer. The separate V1-PILOT design uses UUID `assessment_attempts`, a required submitted payload snapshot, and immutable `assessment_answers` with selected-option/text fields. These models differ in identifier, lifecycle, and answer shape. Neither DDL artifact establishes a live schema or an approved adapter from V1-PILOT to API #32. Do not choose one, cast IDs, or infer an answer projection in this screen DD; backend ownership must resolve the mapping.

**Design-system discrepancy:** the Study Web target in `.agents/web-study/design.md` calls for ocean tokens, Inter/system typography without remote font dependencies, restrained surfaces, approximately 1120px content width, responsive 768/1024px breakpoints, and controls at least 44px high. The ST-16 PNG instead uses a bright cobalt/green gradient treatment, dense navigation and small text; the companion HTML separately imports Google Plus Jakarta Sans and Material Symbols and Tailwind from CDNs and renders a different Guest/unavailable composition. Neither artifact matches the target consistently or proves a current app implementation. Preserve the supplied assets; resolve which result state is canonical and align a future frontend design before implementation.

### Trích từ DD nguồn: D.1. API response and state mapping

| Response | State target | UI/data rule |
|---|---|---|
| 200 `DESIGN_RESOURCE_RETRIEVED`, `status=PENDING_GRADE` | `pending` | Show “Đang chờ chấm” from approved status; no score zero; pending score/correctness remain subject to Q-32-02/03. |
| 200 `DESIGN_RESOURCE_RETRIEVED`, `status=GRADED` | `graded` | Render only approved response fields; not automatically PASSED; no answer key without policy. |
| 200 with other/missing status | `unsupported_status` | Do not invent mapping. |
| 401 `DESIGN_AUTHENTICATION_REQUIRED` | `error`/authentication-required | No reauth route is defined in ST-16 contract. |
| 403 `DESIGN_ACCESS_DENIED` | `access_denied` | Owner behavior remains Q-32-01. |
| 404 `DESIGN_RESOURCE_NOT_FOUND` | `unavailable`/`not_found` | Do not expose ownership/existence beyond approved message. |
| 500 `DESIGN_INTERNAL_ERROR` | `error` | Safe copy only; no internal details. |
| Timeout/network failure or malformed envelope | `error`/`unavailable` | No result claim, retry or stale sample fallback is defined. |

### Trích từ DD nguồn: F.3. Nguồn truy vết

- [ST-16 plan](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/ST-16_PLAN.md), [marker map](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/ST-16_markers.json), [annotated screen](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/screen_annotated.png), [source PNG](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/screen.png), [HTML companion](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/code.html).
- [Screen inventory, F05 and G-09](../../list_screen.md); [ST-15 handoff](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/ST-15.md).
- [API catalog #32 and QuizAttempt/QuizAnswer schema](../../../../../docs/lists/list_api.md).
- API #32 DD: [overview](../../../../study-server/docs/dd/32_attempts_result/02_Overview.md), [request](../../../../study-server/docs/dd/32_attempts_result/03_Request.md), [response](../../../../study-server/docs/dd/32_attempts_result/04_Response.md), [mapping](../../../../study-server/docs/dd/32_attempts_result/05_Data_Mapping.md), [errors](../../../../study-server/docs/dd/32_attempts_result/06_Error.md), [open questions](../../../../study-server/docs/dd/32_attempts_result/OPEN_QUESTIONS.md).
- [API #31 grading questions](../../../../study-server/docs/dd/31_attempts_submit/OPEN_QUESTIONS.md); [AC-16 index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md); [AC activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio).
- [Candidate table design](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md); [legacy candidate DDL](../../../../../infra/postgres/study-server/DB.sql); [V1-PILOT candidate schema](../../../../../infra/postgres/02_study_db.sql); [current route inventory](../../../../../.agents/server-study/apis/declared-routes.md).
- [Study Web design target](../../../../../.agents/web-study/design.md); [Study Web scope status](../../../../../.agents/web-work/study/INDEX.md).
- [Study Web source status](../../../../../.agents/web-work/study/INDEX.md); [Study Web design target](../../../../../.agents/web-study/design.md).

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/ST-16.md)
