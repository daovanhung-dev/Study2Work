# ST-05 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-05-API-001` | #08 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-05-API-002` | #16 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #08, #16
- Orchestration/data notes: Revalidate #8; POST #16 một lần theo action người dùng; lưu order_id từ response.
- BE/source status và gate: **#08 R; #16 D; DD BLOCKED**; **BLOCK:** Order schema, provider/amount/currency policy và idempotency chưa source-backed; inventory revalidation lần hai chưa được AC-12 đặt thứ tự; Study Web UNWIRED; HTML chưa có confirm UI
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API boundary

| API | Request / quyền | Success | Error/current boundary | Tác động |
|---|---|---|---|---|
| #08 | `GET /api/v1/courses/{course_id}`; Public; `course_id:int64` | 200 `DESIGN_RESOURCE_RETRIEVED`; current envelope `Page<Course>` singleton | Catalog/current source: 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`; current code maps invalid ID or missing/unpublished course to 404; query/mapping error to 500 | Read-only; không sửa enrollment/order. Current SQL dùng `LEFT JOIN users`; Draft API #08 mô tả `INNER JOIN`, cần giữ discrepancy. |
| #16 | `POST /api/v1/orders`; Bearer JWT; role Student; body `{course_id:int64!, payment_provider:PaymentProvider!}` | Contract: 201 `DESIGN_RESOURCE_CREATED`, `ApiEnvelope<Order>` | Catalog: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`; #16 chưa có runtime response | AC-12 chỉ yêu cầu tạo logical Order `PENDING` ở paid branch; physical write/transaction/idempotency chưa có nguồn. |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-05_kiem-tra-don-hang-checkout/ST-05.md)
