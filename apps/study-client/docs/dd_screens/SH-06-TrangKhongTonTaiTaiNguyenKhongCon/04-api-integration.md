# SH-06 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `SH-06-API-001` | #08 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #08
- Orchestration/data notes: Router 404 hoặc resource 404 chuyển state; không chuyển 500 thành 404.
- BE/source status và gate: **D**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: 5. API #08 và nguồn dữ liệu

### 5.1 `GET /api/v1/courses/{course_id}`

| Thành phần | Current source behavior |
|---|---|
| API ID/status | API #08 trong API contract tổng thể đã duyệt; API DD #08 còn `Draft — Needs Confirmation`. Dòng SH-06 ghi BE `D`, API index §5 ghi #008 `R`; current route/module/test source tồn tại (`SOURCE_BACKED`; deployment chưa xác minh). |
| Method / endpoint | `GET /api/v1/courses/{course_id}`; public, không yêu cầu Authorization/Bearer. Path `course_id` design type int64 bắt buộc; route nhận raw string rồi `validate_course_id` dùng `parse_integer`. |
| Request | Path param `course_id`; không query/body. Invalid integer path hiện trả 404 `DESIGN_RESOURCE_NOT_FOUND`, không 422. |
| Query / side effect | `FIND_PUBLISHED_COURSE_DETAIL` đọc `courses` `LEFT JOIN users m ON m.id=c.mentor_id`, filter `c.id=:course_id AND c.status='PUBLISHED'`. Read-only; không commit. SQL error gọi rollback. |
| HTTP 200 | `DESIGN_RESOURCE_RETRIEVED`; `data.items` có một course và `data.pagination={page:1,size:1,total:1,total_pages:1}`. Course fields: `id:int`, `title:string`, `description:string|null`, `thumbnail_url:string|null`, `price:string` dạng decimal, `status:string`, `mentor:{id:int,full_name:string,avatar_url:string|null}`. |
| HTTP 404 | `DESIGN_RESOURCE_NOT_FOUND`, message hiện “Published course not found.”; dùng cho ID không parse được và không có published row. Missing và non-PUBLISHED giống nhau. |
| HTTP 500 | `DESIGN_INTERNAL_ERROR`, message an toàn “Courses could not be retrieved.”; SQLAlchemy error, projection/mapping error hoặc CoursePage validation failure. API #08 hiện không trả 403. |
| Envelope / trace | Shared response envelope: `success`, `businessCode`, `message`, `data`, `meta`, `traceId`; response header `X-Trace-Id`. Không render `data` khi 404 hoặc error body thô trên SH-06. |
| DB source | [`DB.sql`](../../../../../infra/postgres/study-server/DB.sql) có bảng `courses`/`users` và các cột query dùng; `courses.mentor_id` nullable trong DDL. `map_course` yêu cầu mentor id/name, nên thiếu mentor data thành 500, không thành 404. DDL không xác minh live schema. |

Source trace: [`API route`](../../../../study-server/app/api/v1.py) → [`view.py`](../../../../study-server/app/modules/guest/api_08_courses_detail/view.py) → [`validate.py`](../../../../study-server/app/modules/guest/api_08_courses_detail/validate.py) → [`query.py`](../../../../study-server/app/modules/guest/api_08_courses_detail/query.py) → [`CoursePage/models.py`](../../../../study-server/app/modules/guest/_shared/course_catalog/models.py) + [`helpers.py`](../../../../study-server/app/modules/guest/_shared/course_catalog/helpers.py). Test source: [`test_courses_detail.py`](../../../../study-server/tests/modules/guest/api_08_courses_detail/test_courses_detail.py); test được đọc, không chạy trong phiên docs.

### 5.2 Design contract và source discrepancy

- [`API contract`](../../../../../docs/lists/list_api.md) khai báo #08 `ApiEnvelope<Page<Course>>`, 200 `DESIGN_RESOURCE_RETRIEVED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`; file đánh dấu `APPROVED_DESIGN_CONTRACT` nhưng chưa runtime-verified. [`API DD #08`](../../../../study-server/docs/dd/08_courses_detail/02_Overview.md) vẫn ghi `Draft — Needs Confirmation`. Response Page singleton trong source khớp kiểu `data` của contract.
- [`AC-05 guest diagram`](../../../../study-server/docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) có nhánh “NO → 404/403” cho course existence/publication, trong khi [`API catalog`](../../../../../docs/lists/list_api.md) ghi 404/500. Current #08 query không trả private row; cả missing/unpublished cùng trả 404; internal query/mapping failure là 500; route không có 403 branch. Đây là discrepancy cần owner xử lý trước DD READY. Nếu guard khác trả 403, giữ access-denied state riêng; không gán 403 cho #08.
- [`list_screen.md`](../../list_screen.md) SH-06 liệt kê #08 là `D`; current source tồn tại nhưng live deployment/schema chưa được xác nhận. Không nâng trạng thái thành `RUNTIME VERIFIED`.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/SH-06.md)
