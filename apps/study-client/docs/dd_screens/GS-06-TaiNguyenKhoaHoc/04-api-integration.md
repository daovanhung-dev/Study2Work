# GS-06 — API Integration

> **T022 current-source update (2026-11-17):** The GS06 tab currently calls neither API. #11 has local route/module/query/model/test source but returns only the first row as a singleton; #12 is not used because its public direct-URL behavior lacks the AC-06 resource access policy. API #11/#12 DDs remain Draft.

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `GS-06-API-001` | #11 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `GS-06-API-002` | #12 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #11, #12
- Orchestration/data notes: GET #11 → người dùng chọn id → GET #12 trước khi mở URL; không suy diễn visibility.
- BE/source status và gate: **#11 route/module/query/test source-backed locally; API #11/#12 DD Draft; GS06 UI partial**; **BLOCK:** #11 query reads all rows but current view returns only `rows[0]`, while its DD disallows selecting a representative row; list/empty/order/pagination contract and `visibility` are unresolved. AC-06 public-or-authorized/403/private signed URL conflicts with #12 current public/no-auth/direct URL, conditional parent check only when `lesson_id` is non-null; no 410/TTL/signer. Legacy DDL has `resources`, V1-PILOT does not; live schema/deployment unknown. GS06 currently sends no resource request and offers no open/download action.
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Luồng dự kiến theo contract đã xác nhận được

1. GS-03 mở tab resource và chuyển cùng `courseId` vào route đề xuất. Current app không có route để kiểm chứng direct entry, query-state, back behavior hoặc auth/session.
2. Client cần xác nhận `courseId` có mặt trước khi tạo request. API #11 catalog yêu cầu `course_id:int64`, public/no Bearer, GET không body/query. Không có source implementation để xác định parser, validation response hay actual endpoint behavior.
3. Nếu gọi #11 theo design hiện có, response `data` được khai báo là một `Resource`. Do đó client không thể xác định collection rỗng, nhiều item, thứ tự hoặc tổng số. Không map response vào list; đánh dấu contract/config error và không hiển thị dữ liệu giả. Empty state chỉ hợp lệ khi API được sửa/duyệt trả một collection rỗng rõ ràng.
4. Khi collection contract được chốt và user chọn một item, lấy `resource.id` làm `resourceId`; không tự ghép URL từ ID hoặc đoán tên file.
5. Gọi #12 tại thời điểm user mở resource. API catalog là public GET không body/query; current backend đọc metadata và trả envelope. Current API không có visibility/access check hoặc storage signer, vì vậy không thể khẳng định 200 đồng nghĩa người dùng có quyền mở resource private.
6. Chỉ sau khi access policy, URL semantics và error contract được phê duyệt mới mở/tải `data.url`. Nếu thiếu URL, URL không hợp lệ, access bị từ chối hoặc mạng/API lỗi thì phải giữ nguyên state an toàn; exact copy/retry behavior cần product/API contract.
7. Khi được phép, điều hướng sang GS-07 với cùng `resourceId`; back trở lại GS-06 phải giữ `courseId` và tab. Cách lưu/restore state chưa được implement.

### Trích từ DD nguồn: API request/response và giới hạn

| API | Request | Current/design response | Auth/access | Status và giới hạn |
|---|---|---|---|---|
| #11 | `GET /api/v1/courses/{course_id}/resources`; `course_id:int64`; no body/query; public/no Bearer. | Draft declares singleton `Resource`; `visibility` has no source. Current route/module/query/model/tests exist. Query reads rows ordered by ID, but view serializes only `rows[0]`; no rows returns 404. | Catalog says public; AC-06 requires public-or-authorized. Unresolved. | Declared 200/404/500; collection cardinality, pagination/order and empty semantics unresolved. `SOURCE-BACKED LOCALLY; CONTRACT DISCREPANCY; API DD Draft`. |
| #12 | `GET /api/v1/resources/{resource_id}`; catalog type `int64`; no body/query; public/no Bearer. Current router nhận raw path `str` rồi validator chấp nhận positive signed-int64. | Current response `data={id:int,name:string,type:string,url:string|null,lesson_id:int|null}` trong envelope; bỏ `visibility`; URL là `resources.url` trực tiếp. API DD vẫn Draft và câu `DECLARED_NOT_RUNNABLE` đã stale so với source/test/report. | Route không có Bearer dependency; conditional parent gate chỉ khi `lesson_id` non-null. Không có visibility/enrollment check hoặc signer; null `lesson_id` không bị parent-gate. | Current source: 200 `DESIGN_RESOURCE_RETRIEVED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`; SQL error rollback; mapping error 500. Không có 403/410/TTL. |

Đối với cả hai GET, retry, timeout, cache invalidation, de-duplication khi click liên tiếp, CORS/storage headers và download disposition chưa có client contract. Không tự đặt giá trị mặc định. Legacy `DB.sql` có `resources` nhưng thiếu `visibility`; V1-PILOT schema không có `resources`; live schema/deployment chưa được xác minh.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/02_guest_discovery/GS-06_tai-nguyen-khoa-hoc/GS-06.md)
