# AD-14 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-14-API-001` | #83 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `AD-14-API-002` | #84 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `AD-14-API-003` | #85 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `AD-14-API-004` | #86 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #83, #84, #85, #86
- Orchestration/data notes: AD-13 numeric `Lesson.id` → GET #83 → riêng một nhánh PUT #84 / PATCH #85 / DELETE #86 → reload AD-12/#82 theo AC-34.
- BE/source status và gate: **R** local #83–#86 route/module/query/model/test source; API DDs Draft. #84 full-replacement body `{title,content,video_url,order}` và #85 `{status}`/enum/audit là DERIVED; #86 rechecks `lesson_progress`, `resources`, `lesson_uploads` and returns 422 on any reference. **DD BLOCKED; IMPLEMENTATION BLOCKED:** #84 form/body mismatch (no `video_url`, course/type unmapped), #85 `ARCHIVED` vs local `SUSPENDED`, dependency set/output, `ADMIN` vs lesson-management permission, legacy/V1-PILOT/live schema, Study Web `UNWIRED`; **RUNTIME NOT VERIFIED**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API boundary

| API | Direct design | Local source hiện tại | Kết quả chính |
|---|---|---|---|
| #83 GET `/api/v1/admin/lessons/{lesson_id}` | Path int64, Bearer/Admin, `ApiEnvelope<Lesson>`, 200; errors 401/403/404/500. | Shared `ADMIN`, raw signed-int64 validation, đọc một Lesson không `DELETED`, không đọc dependencies; lỗi path local 404. | `data: {id, course_id, title, content?, video_url?, order, status}`; field mapping kế thừa #09. |
| #84 PUT `/api/v1/admin/lessons/{lesson_id}` | Catalog/AC chỉ khai báo path; direct response Lesson; 200, errors 401/403/404/422/500. | Strict required full-replacement body `{title, content, video_url, order}` là DERIVED; update metadata, commit sau projection hợp lệ. Typed body validation chạy trước handler/auth. | Trả Lesson; giữ `course_id` và `status`; không ghi dependency/audit. |
| #85 PATCH `/api/v1/admin/lessons/{lesson_id}/status` | Direct path/auth/response/error set; catalog và AC không khai báo body/enum. | `{status}` và `DRAFT|PUBLISHED|SUSPENDED` là DERIVED; lock, đổi `status` + `updated_at`, ghi old/new/actor audit trong một transaction; same-status là no-op không audit. Typed body validation chạy trước handler/auth. | Trả Lesson; audit candidate table theo migration 012, chưa chứng minh live. |
| #86 DELETE `/api/v1/admin/lessons/{lesson_id}` | Path-only, `ApiEnvelope<DeleteResult>`, 200, errors 401/403/404/422/500; AC yêu cầu theo policy/dependency. | Shared `ADMIN`, lock, kiểm tra `lesson_progress`, `resources`, `lesson_uploads`; có reference trả 422, không có thì đặt `status='DELETED'`. Dependency/tombstone/timestamp rules là DERIVED. | `{id, status:"deleted", deleted_at}`; local `deleted_at` lấy DB `updated_at`. |

Tất cả API DD #84–#86 đang `Draft — Needs Confirmation`; #83 cũng Draft. Tài liệu và source local không xác minh schema/deployment đang chạy. Không có retry, timeout, optimistic version, idempotency token hoặc cache policy được contract khai báo.

### Trích từ DD nguồn: Response and validation mapping for implementation handoff

- #84 success is direct Lesson with `id`, `course_id`, `title`, nullable `content`, nullable `video_url`, `order`, `status`; `meta:{}` and trace ID follow current helper. Errors use catalog codes 401/403/404/422/500 and current `data:null` error envelope. The body fields and validator rules remain DERIVED.
- #85 success is direct Lesson; audit row is not in response. Current error set is 401/403/404/422/500. Local no-op and audit behavior are DERIVED.
- #86 success is direct DeleteResult `{id:int64, status:"deleted", deleted_at:datetime}`. Local dependency conflict uses 422 `DESIGN_VALIDATION_ERROR`; response intentionally carries no dependency counts/details. Current error set is 401/403/404/422/500.
- Do not add client retry, optimistic concurrency, idempotency, conflict code, toast wording or success persistence claims without an approved source.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-14_sua-doi-trang-thai-xoa-bai-hoc/AD-14.md)
