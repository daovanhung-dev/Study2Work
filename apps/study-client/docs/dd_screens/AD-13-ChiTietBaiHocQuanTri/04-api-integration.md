# AD-13 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-13-API-001` | #83 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #83
- Orchestration/data notes: AD-12 numeric `Lesson.id` → GET #83 `ApiEnvelope<Lesson>`; local #83 trả 7 fields, loại `DELETED`, không đọc dependencies/metrics; API #86 tự kiểm tra progress/resources/uploads khi delete. Không gọi Student #24 thay API Admin.
- BE/source status và gate: **R** local #83 route/module/query/model/test source; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** AC dependencies chưa có output rule; course title/type/resource/progress/metrics/SSE fields thiếu; ADMIN vs lesson-management permission, legacy/V1-PILOT schema, nullable required fields/status enum và Study Web `UNWIRED` còn mở; **RUNTIME NOT VERIFIED**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API #83 contract và local behavior

| Thuộc tính | Catalog / AC | Current source |
|---|---|---|
| Method/path | `GET /api/v1/admin/lessons/{lesson_id}` | Route wired cùng path; raw `lesson_id` chuyển sang module |
| Authentication | Bearer JWT; role Admin | Shared guard `role="ADMIN"`; chạy trước path parse/DB |
| Permission | AC-34 yêu cầu lesson-management permission | Fine-grained permission chưa có source |
| Input | Required path `lesson_id:int64`; không body/query | Custom signed-int64 parser; malformed/overflow/overlength→404 locally (DERIVED) |
| Success | 200 `ApiEnvelope<Lesson>` | 200 direct `Lesson` object trong `data` |
| Error | 401, 403, 404, 500 | Cùng catalog error set; no 422 trong OpenAPI #83 |
| Data | Lesson theo reusable schema | Legacy BIGINT lookup candidate, loại `DELETED`; không join dependencies |
| Side effect | GET / read-only | Không mutate, không commit; rollback nhánh missing/error |

### Trích từ DD nguồn: API response field mapping

| `data` field | Type/nullability | UI use candidate | Limits |
|---|---|---|---|
| `id` | int64, required | Lesson identifier; route handoff key to AD-14 | Numeric ID only; no code/slug format. |
| `course_id` | int64, required | Parent course identifier | No course title/name; candidate DDL allows NULL, mapping then fails. |
| `title` | string, required | Lesson title | Maps legacy `name`; no title search/type semantics here. |
| `content` | nullable string | Lesson text content if product specifies a safe rendering surface | No content block schema, HTML trust/sanitization or preview rule in #83. |
| `video_url` | nullable string | Source metadata only pending media-access contract | No signer/expiry/player/DRM/authorization; do not auto-embed. |
| `order` | int32, required | Lesson order | Maps legacy `sort_order`; candidate DDL nullable. |
| `status` | string, required | Raw lifecycle value pending UI enum/casing approval | Query excludes `DELETED`; other values are not allow-listed. |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-13_chi-tiet-bai-hoc-quan-tri/AD-13.md)
