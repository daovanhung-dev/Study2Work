# AD-18 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-18-API-001` | #90 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #90
- Orchestration/data notes: Candidate DELETE #90 path-only; on success invalidate/refetch #87 theo inventory. `conflict` không được #90 catalog khai báo (không có 409); 422 local là invalid `quiz_id`, không phải conflict.
- BE/source status và gate: **R** local #90 route/module/query/model/validator/test source; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** AC-35 chỉ yêu cầu soft-delete khi có attempts, no-attempt branch không xác định; local hard-delete/no-history và soft-delete on linked answer are DERIVED; tombstone/timestamp/repeat, #29 race, permission, #87/#89/#91 visibility, target data/detail API, live schema and Study Web UNWIRED remain open; **RUNTIME NOT VERIFIED**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API #90 — direct contract và local source

| Thành phần | API catalog / AC-35 | Study Server hiện tại | Tác động lên UI |
|---|---|---|---|
| Method/path | `DELETE /api/v1/admin/quizzes/{quiz_id}`; path `quiz_id:int64!`; không body/query. | Route đã đăng ký cùng path template; chỉ truyền Authorization và raw path. | Không truyền audit reason hoặc UI-only fields. `quizId` route param phải được map sang numeric `quiz_id`; slug/UUID không tương thích với candidate int64. |
| Auth | Bearer JWT; role Admin. AC-35 nêu quiz-management permission. | Shared guard chỉ cho `ADMIN`, trước path validation và DB. | Cần owner quyết định permission mapping/route guard; không xem `ADMIN` tự động tương đương permission nghiệp vụ. |
| Success | HTTP 200 `DESIGN_RESOURCE_DELETED`; `ApiEnvelope<DeleteResult>`, gồm `id:int64`, `status:"deleted"`, `deleted_at:date-time`. | Envelope trả `success`, `businessCode`, `message`, `data`, `meta`, `traceId`. Local map nhánh soft/repeat từ `updated_at`; nhánh hard lấy `CURRENT_TIMESTAMP`. | Chỉ xử lý success khi HTTP 200 và envelope hợp lệ. Không suy ra data target hoặc audit log từ response. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR`. Không có 409. | Cùng status/business codes trên route. Local validator trả 422 với lỗi `quiz_id` không phải positive signed-int64; lỗi này là validation, không phải dependency conflict. | Không tạo state/API branch 409. Unauthorized/forbidden/not-found/invalid-id/service error phải được phân biệt. |
| Attempt/history policy | AC-35 node n10: soft-delete nếu Quiz đã có attempts; không xác định no-attempt branch. | Local code soft-deletes khi có attempt **hoặc linked answer**; nếu không có hai loại history này thì hard-delete children rồi Quiz. Đây là nhánh `DERIVED`, chưa được owner duyệt. | Không hứa hành vi từ mockup hoặc local implementation cho đến khi policy được chốt. |
| Retry/idempotency | Catalog không quy định timeout/retry/idempotency hoặc DELETE lặp. | Local tombstone DELETE lặp trả 200 với timestamp cũ; đây là local behavior, chưa phải contract được duyệt. | Không tự động retry request mơ hồ cho đến khi retry/idempotency/reconciliation policy được xác nhận. |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-18_xac-nhan-xoa-bai-kiem-tra/AD-18.md)
