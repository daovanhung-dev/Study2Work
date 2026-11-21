# GS-06 — API Integration

> **T041/current-source update (2026-11-20):** GS-06 calls #11 after #08 published-course success. #11 returns PUBLIC `Resource[]`, ordered by `id ASC`; a valid course with no public rows returns `200 []`. GS-07 calls #12. PUBLIC returns a validated direct HTTP(S) URL; PRIVATE requires Student Bearer + published parent course + ACTIVE enrollment and returns a signed URL with TTL 300 seconds. Source is local evidence; live DB/runtime remains unverified. T041 approves these behaviors and supersedes the historical T022 statements below.

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `GS-06-API-001` | #11 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `GS-06-API-002` | #12 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #11, #12
- Orchestration/data notes: #11 public collection → user selects ID → #12 metadata and access decision → open validated URL.
- BE/source status and gate: **#11/#12 current source-backed locally; T041 contract approved; UI partial; runtime not verified.** `resources` table has no current Study writer found (#47 stores `lesson_uploads`); legacy/V1-PILOT schema compatibility and live database remain open. MIME-specific preview/expiry UI is not implemented.
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
| #11 | `GET /api/v1/courses/{course_id}/resources`; path `course_id`; no body/query; public. | Current data: `id/name/type/url/visibility/lesson_id`; only PUBLIC rows from PUBLISHED lessons/courses; `Resource[]`, ID ascending. | Public/no Bearer. | 200 `DESIGN_RESOURCE_RETRIEVED`, including `[]`; 404 unpublished/missing course; 500 query/mapping error. Current route uses Python `int` and positive check; no live DB claim. |
| #12 | `GET /api/v1/resources/{resource_id}`; catalog path int64; no body/query. | `data={id:int,name:string,type:string,url:string,visibility,lesson_id:int|null}`. PUBLIC URL comes from `resources.url`; PRIVATE URL is signed for 300 seconds. | PUBLIC: no Bearer. PRIVATE: Student Bearer, published parent and ACTIVE enrollment required. | 200 `DESIGN_RESOURCE_RETRIEVED`; 401 unauthenticated/invalid Student token, 403 no ACTIVE enrollment, 404 missing/invalid/unpublished parent or missing storage key, 500 lookup/mapping error, 503 signing dependency unavailable. |

Đối với cả hai GET, retry, timeout, cache invalidation, de-duplication khi click liên tiếp, CORS/storage headers và download disposition chưa có client contract. Không tự đặt giá trị mặc định. Legacy `DB.sql` có `resources` nhưng thiếu `visibility`; V1-PILOT schema không có `resources`; live schema/deployment chưa được xác minh.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/02_guest_discovery/GS-06_tai-nguyen-khoa-hoc/GS-06.md)
