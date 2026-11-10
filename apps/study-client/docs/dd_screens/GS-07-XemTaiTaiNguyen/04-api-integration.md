# GS-07 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `GS-07-API-001` | #12 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #12
- Orchestration/data notes: GET #12 tại thời điểm mở; không cache signed URL vô hạn hoặc lộ internal storage key.
- BE/source status và gate: **R (#12 source-backed locally; API DD Draft)**; **BLOCK:** current public/no-auth direct URL lacks AC-06 access check/signer; preview/MIME/URL policy, 403/404/expiry mapping, GS-06/ST-12 return context and Study Web route UNWIRED; live schema unknown; prototype differs from Study design guide and WCAG unmeasured
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Luồng dự kiến sau khi contract được chốt

1. GS-06 hoặc ST-12 điều hướng tới route đã được duyệt, truyền `resourceId`; nếu cần giữ ngữ cảnh, nguồn cũng phải xác định `courseId`/`lessonId` và destination khi quay lại.
2. Client kiểm tra path param theo contract `resource_id:int64`. Không có client parser/route hiện tại để xác minh invalid-ID UX.
3. Hiển thị loading state và gọi #12 `GET /api/v1/resources/{resource_id}` theo catalog. Catalog khai báo public/no Bearer; thay đổi auth semantics cần được cập nhật trong hợp đồng trước khi triển khai.
4. Backend hiện kiểm tra ID dương signed-int64, truy vấn resource và, nếu `lesson_id` có giá trị, kiểm tra lesson không `DELETED` cùng course `PUBLISHED`. Thiếu row hoặc parent không hợp lệ trả 404. `lesson_id=null` bỏ qua parent check.
5. Backend hiện trả `id`, `name`, `type`, `url`, `lesson_id`; không kiểm tra access, visibility hoặc signer. Trước khi mở file cần product/backend/storage chốt liệu URL public hay signed, ai được truy cập, expiry và lỗi tương ứng. Hiện chưa đạt.
6. Sau khi policy và renderer được xác nhận: mở preview cho type/MIME được allowlist; fallback download khi download được phép. Trạng thái URL null, unsupported type, expiry, network failure, retry và URL safety chưa có contract.
7. Khi back, khôi phục đúng source (GS-06 hay ST-12) và context được xác nhận. Không mặc định luôn quay GS-06 chỉ từ prototype.

### Trích từ DD nguồn: API #12 request/response và error mapping

| Chủ đề | Declared contract / expected | Current source evidence |
|---|---|---|
| Method/path | `GET /api/v1/resources/{resource_id}`; `resource_id:int64` required; no query/body; public/no Bearer. | Route compose trong `app/api/v1.py`, raw string path để custom validator ánh xạ invalid ID thành 404; không có Authorization dependency. |
| Success | `ApiEnvelope<Resource>`; catalog/API DD liệt kê `id/name/type/url/visibility/lesson_id`; 200 `DESIGN_RESOURCE_RETRIEVED`. | Current `ResourceDetail` trả `id/name/type/url/lesson_id`; `url` nullable trong model và lấy direct từ DB; query/response không có `visibility`. |
| Not found | Declared 404 `DESIGN_RESOURCE_NOT_FOUND`. | Invalid/non-positive/overflow ID, resource missing, hoặc parent check fail trả cùng 404/code. Parent check chỉ chạy nếu `lesson_id` khác null. |
| Internal failure | Declared 500 `DESIGN_INTERNAL_ERROR`. | SQLAlchemy query error rollback và trả safe 500; Pydantic mapping error trả safe 500. |
| Access and URL | AC-06 yêu cầu public-or-authorized, 403 khi không có quyền, và Object Storage signed URL cho private resource. | Current route không auth; không visibility/enrollment check, không signer; trả direct `resources.url`. Không có current 403/410/expiry contract. |
| API DD/runtime label | API DD #12 `Draft — Needs Confirmation`; có dòng `RUNTIME_STATUS: ... DECLARED_NOT_RUNNABLE`. | `v1.py` compose #12 và test source tồn tại; đây là documentation/source discrepancy về local composition. Test source không được chạy; production/deployment/browser runtime vẫn chưa xác minh. |

Catalog, API DD và current source không hoàn toàn cùng một mức bảo đảm. `resources.url`/`lesson_id` của legacy DDL khác nullable flags của model/contract; V1-PILOT DDL không có generic `resources` table. Live schema vẫn chưa xác minh.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/02_guest_discovery/GS-07_xem-tai-tai-nguyen/GS-07.md)
