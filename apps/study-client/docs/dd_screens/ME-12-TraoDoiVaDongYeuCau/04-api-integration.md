# ME-12 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ME-12-API-001` | #59 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ME-12-API-002` | #60 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ME-12-API-003` | #61 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #59, #60, #61
- Orchestration/data notes: GET #59 → POST #60 reply → reload #59; PATCH #61 resolve sau xác nhận.
- BE/source status và gate: **R**; #59–#61 local route/module/query/model/test source-backed, migration 008 local; API DD Draft/DERIVED, live schema chưa verified. **BLOCK:** loaded thread/full-thread scale và attachment UI chưa có thiết kế; counter 2000 khác #60 không max; #61 không enforce tối thiểu một message, AC satisfaction/confirmation chưa chốt; #60 vẫn nhận reply sau RESOLVED/CANCELLED; POST retry không idempotent, GET refresh policy cần thống nhất; Socket/TLS, SLA, auto-settlement/survey là prototype claim; Student producer chưa có; Study Web UNWIRED
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: D.1. Shared API envelope and error handling

API success envelopes expose success, businessCode, message, data, meta and traceId. For #59–#61, success data is one SupportRequest object. Use the API-returned businessCode and HTTP status; do not infer success from HTTP status alone. Optional null fields may be omitted by response serialization.

| Response field | Type/meaning | UI mapping |
|---|---|---|
| success, businessCode, message, meta, traceId | Envelope fields; success is boolean, businessCode/message are strings, meta is an object, traceId is a string. | Check success and businessCode; retain traceId for diagnostics according to shared logging policy, without logging message content. |
| data.id | Positive int64 SupportRequest identifier in the response model. | Must equal route requestId; mismatch is a projection error. |
| data.course_id | Positive int64 course identifier. | No course title/slug is returned by #59–#61; do not derive a label. |
| data.student | User summary with id:int64, full_name:string and optional avatar_url:string. | Render only where the approved thread header needs student identity; privacy/display policy remains open. |
| data.status | String status. | Map only confirmed values; #61 local lifecycle includes OPEN, IN_PROGRESS, WAITING_LEARNER, RESOLVED, CANCELLED. |
| data.messages[] | Ordered message array; each item has id:int64, author summary, content:string, attachments array and created_at:datetime. | Render in server order; no pagination metadata is returned. |
| message.author | User summary with id, full_name and optional avatar_url. | Message author/time layout is not present in source mockup. |
| message.attachments[] | UploadAsset response items with id, name, url, content_type, size_bytes and status. | Render only returned metadata and link; attachment UI and file safety/download policy remain open. |
| data.created_at / data.resolved_at | Request creation datetime; optional resolution datetime (null fields can be omitted). | Display format/time zone is not defined by this screen source. |

Current catalog error sets are:

| API | HTTP/business outcomes in local source |
|---|---|
| #59 GET detail | 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 500 DESIGN_INTERNAL_ERROR |
| #60 POST reply | 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 422 DESIGN_VALIDATION_ERROR; 500 DESIGN_INTERNAL_ERROR |
| #61 PATCH resolve | 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 422 DESIGN_VALIDATION_ERROR, including STATE_NOT_RESOLVABLE; 500 DESIGN_INTERNAL_ERROR |

The exact safe message comes from the API response. Do not expose SQL/database details. No source contract declares 409, 503, a retry-after value, or a socket error code.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/04_mentor/ME-12_trao-doi-va-dong-yeu-cau/ME-12.md)
