# GS-03 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `GS-03-API-001` | #08 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `GS-03-API-002` | #09 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `GS-03-API-003` | #10 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #08, #09, #10
- Orchestration/data notes: GET #8 để xác định published → lazy GET #9 và #10 theo tab; course ID thống nhất.
- BE/source status và gate: **R (#08/#09), D (#10)**; **BLOCK:** #08 trả singleton Page<Course>, source LEFT JOIN khác API DD INNER JOIN; int64 course_id chưa khớp validator raw-string không có signed int64 range; AC-05 eager khác F02 lazy; #10 thiếu route/title-rating source; G-01 enrollment handoff; Study Web UNWIRED
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: E. API contract và mapping

### API #08 — public course detail (`SOURCE_BACKED`)

| Thuộc tính | Giá trị |
|---|---|
| Method / endpoint | `GET /api/v1/courses/{course_id}` |
| Authentication | Public; không yêu cầu Bearer token. |
| Path | `course_id` raw route segment; catalog type `int64`. Current route annotation là `str`; validator chỉ parse integer syntax, không enforce signed int64/positive range. Không query/body theo current route. |
| Source | `apps/study-server/app/api/v1.py` → `app/modules/guest/api_08_courses_detail/view.py`, `validate.py`, `query.py`; shared `course_catalog.models/helpers.py`. |
| Query | `courses` tìm ID và status `PUBLISHED`; current source `LEFT JOIN users` qua mentor ID để lấy mentor summary. API #08 Draft DD lại ghi `INNER JOIN`. Mentor id/name là bắt buộc ở model/mapper; thiếu mentor row làm mapping thành HTTP 500. Read-only. |
| Response 200 | Common envelope `{success,businessCode,message,data,meta,traceId}`; `businessCode=DESIGN_RESOURCE_RETRIEVED`; `data={items:[Course],pagination:{page:1,size:1,total:1,total_pages:1}}`. |
| Course mapping | `id:int`, `title:string`, `description:string|null`, `thumbnail_url:string|null`, `price:string`, `status:string`, `mentor:{id:int,full_name:string,avatar_url:string|null}`. Response source dùng giá serialized decimal string; không khai báo currency. |
| Errors | 404 `DESIGN_RESOURCE_NOT_FOUND` cho ID parse failure hoặc không tìm thấy course PUBLISHED; 500 `DESIGN_INTERNAL_ERROR` cho DB/mapping failure, gồm thiếu mentor id/name sau `LEFT JOIN`. Current code rollback SQLAlchemy failure và không trả raw DB detail. Oversized int64 path chưa được source/test xác minh. AC-05 có 403 alternative; đây là discrepancy, không map 403 như current API. |
| Retry/cache | Không có retry/cache/idempotency policy được source xác nhận; GET read-only không tự tạo cache behavior cho UI. |

### API #09 — public curriculum (`SOURCE_BACKED`)

| Thuộc tính | Giá trị |
|---|---|
| Method / endpoint | `GET /api/v1/courses/{course_id}/curriculum` |
| Authentication | Public; không yêu cầu Bearer token. |
| Path/body | Catalog: `course_id:int64`; current route nhận `str`, validator gọi shared `parse_integer` nhưng không enforce signed int64/positive range. Không query/body theo current route. |
| Source | `apps/study-server/app/api/v1.py` → `app/modules/guest/api_09_courses_curriculum/{view.py,validate.py,query.py,models.py}`. Test source ở `apps/study-server/tests/modules/guest/api_09_courses_curriculum/test_courses_curriculum.py`, không chạy. |
| Query | Q1 kiểm tra course PUBLISHED; Q2 chỉ lấy lessons cùng course với status PUBLISHED, sắp xếp `sort_order ASC, id ASC`. Read-only. |
| Response 200 | Common envelope; `businessCode=DESIGN_RESOURCE_RETRIEVED`; `data={items:[Lesson],pagination:{page:1,size:total,total,total_pages:1 nếu total>0, nếu rỗng là 0}}`. Empty message hiện tại “No published lessons.” |
| Lesson mapping | `{id:int,course_id:int,title:string,content:string|null,video_url:string|null,order:int,status:string}`. Không có preview/access permission field trong current model. |
| Errors | 404 `DESIGN_RESOURCE_NOT_FOUND` cho parse failure/missing/unpublished course; 500 `DESIGN_INTERNAL_ERROR` cho query/mapping error; current code rollback SQLAlchemy error. Oversized int64 path chưa được source/test xác minh. |
| Retry/cache | Không có policy được source xác nhận. |

### API #10 — reviews (`DECLARED_NOT_RUNNABLE`)

- Catalog khai báo public `GET /api/v1/courses/{course_id}/reviews`, `page?:int32`, `rating filter?:string`, `ApiEnvelope<Page<Discussion>>`, 200 `DESIGN_RESOURCE_RETRIEVED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
- API DD `apps/study-server/docs/dd/10_courses_reviews/` ghi trạng thái `Draft — Needs Confirmation`; query key `rating` là cách chuẩn hóa minh họa, rating semantics/source chưa có; `Discussion.title` required trong contract nhưng không có cột ở checked-in `discussions` DDL; không có rating field/table để tính average.
- Không có executable route/module/test trong `apps/study-server/app` và `apps/study-server/tests`. Không được coi catalog/API DD là runtime source và không gọi endpoint cho tới khi wired/contract được xác nhận.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/GS-03.md)
