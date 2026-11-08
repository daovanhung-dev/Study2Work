# ST-15 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-15-API-001` | #30 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-15-API-002` | #31 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #30, #31
- Orchestration/data notes: Flush PUT #30 pending trước đúng một POST #31 → ST-16; không gọi #31 sau flush lỗi/không rõ và không retry mù sau 409/timeout; chỉ chuyển tiếp sau accepted response.
- BE/source status và gate: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #30 body/queue/upsert/order/outcome/retry và #31 ownership/state/repeat/deadline/concurrency/grading/transaction/response còn mở; ST-14 summary/dirty-queue handoff/direct entry chưa có contract; legacy BIGINT và V1-PILOT UUID/payload/lifecycle khác; PNG/HTML, timer/count/saved/attempt/instant-grading claims không thống nhất; Student #30–#32 route/module/test NOT_FOUND; Study Web UNWIRED; live schema chưa xác minh
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: A.4. API contract liên quan

| API | Contract thiết kế đã thấy | Điều chưa được xác nhận |
|---|---|---|
| #30 flush answer | `PUT /api/v1/attempts/{attempt_id}/answers`; Student Bearer; path `attempt_id:int64!`; catalog ghi `question_id:int64!`, `answer(s):string!`; 200 `DESIGN_RESOURCE_UPDATED`; 401/403/404/422/500; response `ApiEnvelope<QuizAttempt>`. | Tên/encoding answer; queue ordering; upsert key; ownership/state checks; concurrency; version/idempotency; retry/timeout reconciliation; response projection. Catalog không khai báo 409. |
| #31 submit | `POST /api/v1/attempts/{attempt_id}/submit`; Student Bearer; path `attempt_id:int64!`; không query/body; response `ApiEnvelope<QuizAttempt>`; 200 `DESIGN_RESOURCE_UPDATED`; 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 409 conflict code theo catalog, 500 `DESIGN_INTERNAL_ERROR`. | Q-31-01…06: ownership/masking, allowed states/expiry/repeat/concurrency/idempotency/locking, grading formula/manual detection, transaction/rollback, timestamp/response fields/disclosure và error mapping. |
| #32 result | `GET` theo API catalog, được ST-16 dùng để đọc kết quả sau submit. | Việc đọc lại sau timeout hoặc 409 không được #31 DD chốt làm reconciliation; không tự gọi #32 từ ST-15. |

Các API trên là design contract, không phải bằng chứng endpoint đang chạy. Không thêm request body, query parameter, header ngoài Bearer đã nêu, retry policy hoặc cache mutation.

**DISCREPANCY — database candidates:** `infra/postgres/study-server/DB.sql` mô hình hóa legacy `quiz_attempts`/`quiz_answers` bằng BIGSERIAL/BIGINT, `status` mặc định `IN_PROGRESS`, một `choice_id` trên mỗi answer và `is_correct NOT NULL`. `infra/postgres/02_study_db.sql` là DDL V1-PILOT riêng, dùng UUID `assessment_attempts`, yêu cầu `submitted_payload_snapshot` ngay lúc tạo attempt và mô hình hóa `assessment_answers` là immutable với `selected_option_ids`/text fields. V1-PILOT còn mô tả nhánh QUIZ `SUBMITTED → PASSED|FAILED`, khác AC-16 `SUBMITTED → PENDING_GRADE|GRADED`. Chưa có mapping được duyệt từ autosave #30/submit #31 sang các schema này; cả hai chỉ là candidate DDL, không xác nhận live schema.

### Trích từ DD nguồn: D.1. Bảng response và state mapping

| Response/tình huống | Mapping thiết kế | Điều kiện/giới hạn |
|---|---|---|
| #30 200 `DESIGN_RESOURCE_UPDATED` | Một answer write được API design chấp nhận. | Không chứng minh toàn bộ queue đã flush; không có runtime source/response field xác nhận saved count. |
| #30 401/403/404/422/500 | `flush_error` với business code tương ứng được giữ lại. | Field-level mapping/re-auth/retry chưa chốt; không gọi #31. |
| #31 200 `DESIGN_RESOURCE_UPDATED` | `submitted`, sau đó ST-16; AC-16 branch `PENDING_GRADE` hoặc `GRADED`. | Response schema/state mapping cần chốt; không hứa điểm tức thì. |
| #31 401/403/404/422/409/500 | `submit_error`/`conflict`, giữ màn hình. | Không coi 409 là thành công; copy/reconciliation/retry chưa được định nghĩa. |
| timeout/lost response #30 | `flush_ambiguous`; chặn #31. | API #30 outcome reconciliation chưa chốt. |
| timeout/lost response #31 | `ambiguous_network`. | Không auto-replay, không tự coi success; idempotency/reconciliation chưa chốt. |

### Trích từ DD nguồn: F.3. Nguồn truy vết

- [Kế hoạch ST-15](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/ST-15_PLAN.md), [marker map](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/ST-15_markers.json), [ảnh nguồn](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/screen.png), [HTML nguồn](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/code.html), [ảnh chú thích](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/screen_annotated.png).
- [Inventory, F05 và G-09](../../list_screen.md); [ST-14 handoff](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra/ST-14.md).
- [API catalog #30–#32](../../../../../docs/lists/list_api.md); [API #30 open questions](../../../../study-server/docs/dd/30_attempts_answers/OPEN_QUESTIONS.md).
- API #31 DD: [overview](../../../../study-server/docs/dd/31_attempts_submit/02_Overview.md), [request](../../../../study-server/docs/dd/31_attempts_submit/03_Request.md), [response](../../../../study-server/docs/dd/31_attempts_submit/04_Response.md), [mapping](../../../../study-server/docs/dd/31_attempts_submit/05_Data_Mapping.md), [errors](../../../../study-server/docs/dd/31_attempts_submit/06_Error.md), [open questions](../../../../study-server/docs/dd/31_attempts_submit/OPEN_QUESTIONS.md).
- [AC-16 index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-16 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio), [route inventory](../../../../../.agents/server-study/apis/declared-routes.md), [Study Web status](../../../../../.agents/web-work/study/INDEX.md), [UI target](../../../../../.agents/web-study/design.md).
- Candidate DB references: [table design](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [legacy DDL](../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql); these do not establish live schema.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/ST-15.md)
