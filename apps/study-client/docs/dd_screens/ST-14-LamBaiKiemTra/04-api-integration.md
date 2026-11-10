# ST-14 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-14-API-001` | #28 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-14-API-002` | #29 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-14-API-003` | #30 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #28, #29, #30
- Orchestration/data notes: AC-16: GET #28 → đọc Quiz/rules/questions → eligibility → POST #29 tạo attempt → PUT #30 khi đáp án đổi. Screen owner của #29 chưa thống nhất giữa ST-13 Start và ST-14; route ST-14 đã yêu cầu `attemptId`. Chốt handoff duy nhất, không POST lặp.
- BE/source status và gate: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #30 answer representation/storage/upsert/ownership/state/response/retry chưa chốt; không có GET attempt/answers để restore; time/progress source thiếu; legacy BIGINT và V1-PILOT UUID/lifecycle khác nhau; PNG/HTML và WebSocket/idempotency claims chưa được xác nhận; Study Web UNWIRED; Student APIs #28–#32 NOT_FOUND
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: A.4. API contract liên quan

| API | Contract catalog | Request/response và lỗi | Bằng chứng current runtime |
|---|---|---|---|
| #28 | `GET /api/v1/quizzes/{quiz_id}`; Student Bearer; `path{quiz_id:int64!}`; `ApiEnvelope<Quiz>`. | 200 `DESIGN_RESOURCE_RETRIEVED`; 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR`. | Không tìm thấy Student route/module/test trong source hiện tại; không có source UI gọi API. |
| #29 | `POST /api/v1/quizzes/{quiz_id}/attempts`; Student Bearer; `path{quiz_id:int64!}`; không body/query; `ApiEnvelope<QuizAttempt>`. AC-16 đặt sau GET #28 và eligibility decision. | 201 `DESIGN_RESOURCE_CREATED`; 401/403/404/422/409/500 với business code tương ứng. | Không có Student endpoint/module/test. ST-13 gắn #29 với Start; ST-14 cũng liệt kê #29 nhưng route đã yêu cầu `attemptId`. Screen owner/handoff chưa được chốt. |
| #30 | `PUT /api/v1/attempts/{attempt_id}/answers`; Student Bearer; `path{attempt_id:int64!}`; catalog ghi `body{question_id:int64!, answer(s):string!}`; `ApiEnvelope<QuizAttempt>`. | 200 `DESIGN_RESOURCE_UPDATED`; 401/403/404/422/500. Catalog không có 409. Exact JSON property, representation, limits và response answers chưa xác nhận. | Không có Student route/module/caller/test hoặc runtime DB write. API DD và DDL chỉ là design evidence. |
| #31/#32 | #31 POST submit, #32 GET result theo inventory/API catalog; nằm ở ST-15/ST-16. | #31 có 200/401/403/404/422/409/500; #32 có 200/401/403/404/500. Không gọi ở ST-14. | Student runtime source không có các endpoint này. |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra/ST-14.md)
