# AD-12 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-12-API-001` | #82 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #82
- Orchestration/data notes: GET #82; catalog singleton `Lesson` khác local `Lesson[]`; course cần int64 nhưng mockup dùng slug, type trả 422, status exact raw string, không có pagination; CTA Add chưa có API.
- BE/source status và gate: **R** local route/module/query/model/test source; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** cardinality, filter mappings, page metadata, row projection/Add API, lesson-management permission, legacy nullability/live schema và Study Web `UNWIRED` còn mở; **RUNTIME NOT VERIFIED**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API và liên kết màn hình

| API | Catalog contract | Local source behavior | Tình trạng |
|---|---|---|---|
| #82 `GET /api/v1/admin/lessons` | Bearer/Admin; query `course?:int64`, `status?:string`, `type?:string`; `ApiEnvelope<Lesson>`; catalog 401/403/500 | Role `ADMIN`; `course` signed int64; `type` unsupported→422; `status` exact; trả `ApiEnvelope<Lesson[]>`; DB/projection failures safe 500 | `R` source-backed locally; contract discrepancy; tests not run |
| #83 `GET /api/v1/admin/lessons/{lesson_id}` | Handoff đến AD-13 theo AC-34; path ID là numeric int64 trong route hiện tại | Route được đăng ký; AD-13 source/response chưa được đặc tả trong phiên này | Handoff candidate; không suy diễn row action |

Liên kết thiết kế: AD-01/Admin shell → AD-12 → AD-13 → AD-14; AD-14 thành công thì AC-34 dự kiến reload AD-12. Route, client navigation, filter preservation và reload chưa được triển khai/xác minh.

### Trích từ DD nguồn: Data mapping khi owner chốt contract

| Local #82 field | Type/current nullability | Mapping UI có thể xác minh | Giới hạn |
|---|---|---|---|
| `id` | integer | lesson ID; candidate path ID cho AD-13/#83 | Không chứng minh lesson code. |
| `course_id` | integer theo response model | numeric course ID | Không phải slug/course title; DDL legacy column nullable. |
| `title` | string, từ `lessons.name` | title | Không có keyword search. |
| `content` | nullable string | Không có column trong mockup list rõ ràng | Không suy ra body preview. |
| `video_url` | nullable string | Không có format/streaming claim được hỗ trợ | Không suy ra HLS/DRM/SCORM. |
| `order` | integer từ `sort_order` | thứ tự | DDL legacy `sort_order` nullable. |
| `status` | string | raw status nếu owner duyệt mapping | Không có enum/alias; DDL legacy nullable. |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/AD-12.md)
