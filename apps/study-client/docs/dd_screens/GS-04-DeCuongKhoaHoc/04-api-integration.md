# GS-04 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `GS-04-API-001` | #09 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #09
- Orchestration/data notes: Tái dùng #8 từ cache → GET #9; phân biệt empty curriculum và lỗi.
- BE/source status và gate: **R (#09 source-backed locally)**; **BLOCK:** `course_id:int64` chưa khớp route string/parser range; visibility `PUBLISHED` chưa được API DD duyệt; response có content/video_url nhưng không preview/access field; legacy vs V1-PILOT schema/live DB chưa xác minh; cache/#08 reuse, AC-05 eager vs F02 lazy/direct-entry chưa chốt; Study Web UNWIRED
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: F. API #09 — current source contract

| Thuộc tính | Current source evidence |
|---|---|
| Method/path | `GET /api/v1/courses/{course_id}/curriculum`; router `apps/study-server/app/api/v1.py` gắn prefix `/api/v1`. |
| Auth/input | Public; route hiện không yêu cầu Bearer, query hoặc body. Catalog khai báo `course_id:int64`; route nhận `str` và validator gọi shared `parse_integer` nhưng không enforce signed int64/positive range. |
| Source chain | `apps/study-server/app/api/v1.py` → `apps/study-server/app/modules/guest/api_09_courses_curriculum/{validate.py,view.py,query.py,models.py}`. |
| Q1 | Kiểm tra course row theo `id=:course_id AND status='PUBLISHED'`. |
| Q2 | Chọn `lessons.id, course_id, name AS title, content, video_url, sort_order AS "order", status`; lọc `course_id` và `status='PUBLISHED'`; order `sort_order ASC, id ASC`. Read-only. |
| 200 ready | Common envelope `success,businessCode,message,data,meta,traceId`; `businessCode=DESIGN_RESOURCE_RETRIEVED`. `data.items` lesson list; `pagination={page:1,size:total,total:total,total_pages:1}` khi có item. |
| Lesson model | `id:int`, `course_id:int`, `title:string`, `content:string|null`, `video_url:string|null`, `order:int`, `status:string`. Không có `is_preview`, access level, permission decision, chapter hierarchy hoặc signed media URL. |
| 200 empty | `items=[]`, `page=1,size=0,total=0,total_pages=0`; message `No published lessons.` |
| 404 | `DESIGN_RESOURCE_NOT_FOUND` cho parse error hoặc course missing/unpublished. Không có #09 403 trong current source contract. |
| 500 | `DESIGN_INTERNAL_ERROR` cho query/mapping error; current code rollback SQLAlchemy errors. Raw DB detail không phải UI contract. |
| Pagination/cache | Query không phân trang; page metadata singleton. Không tìm thấy retry, TTL, client-cache, invalidation hoặc idempotency behavior trong source. |

Test source `apps/study-server/tests/modules/guest/api_09_courses_curriculum/test_courses_curriculum.py` bao gồm ID bình thường/invalid, course missing, lỗi ở hai query, success mapping, empty success và TestClient route composition; không có boundary case chứng minh signed-int64 validation. Các test dùng fake session; đã đọc nhưng **không chạy**, nên không xác minh DB thật, migration compatibility, deployment hoặc access policy.

### Contract và schema discrepancy

- API #09 DD `apps/study-server/docs/dd/09_courses_curriculum/02_Overview.md` đang `Draft — Needs Confirmation`; tài liệu ghi rõ `lessons.status='PUBLISHED'` là design-only visibility assumption. Vì vậy current filter là implementation fact, chưa phải approved security policy.
- API catalog khai báo `course_id:int64`, nhưng route hiện nhận `str`; shared parser không áp dụng signed-int64/positive bound. Không suy đoán response cho ID vượt range; đây là discrepancy cần chốt cùng API owner.
- `infra/postgres/study-server/DB.sql` có legacy BIGINT lesson fields `name/content/video_url/sort_order/status` phù hợp tên cột trong query, nhưng không có preview field.
- `infra/postgres/02_study_db.sql` mô tả V1-PILOT UUID/versioned schema khác: `title/summary/position/estimated_minutes/is_preview` và quan hệ course/version/chapter khác. API #09 không query model này. Context nói DDL checked-in không xác nhận live schema.
- **DISCREPANCY:** API hiện trả raw `content`/`video_url` cho public caller, trong khi Guest visibility rule và Student permission flow chưa được nối bằng preview/access data. Không coi `PUBLISHED` hoặc DDL `is_preview` của model khác là quyền xem Guest.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/02_guest_discovery/GS-04_de-cuong-khoa-hoc/GS-04.md)
