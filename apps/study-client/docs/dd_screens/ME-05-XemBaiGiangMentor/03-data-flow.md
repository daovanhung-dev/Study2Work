# ME-05 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: 2. Luồng tổng thể và truy vết source

### Luồng đọc sau khi tạo

```mermaid
sequenceDiagram
    participant M as Mentor
    participant ME04 as ME-04
    participant Web as Study Web route (chưa có source)
    participant API as GET #48
    participant Auth as Shared MENTOR guard
    participant DB as lessons/courses + lesson_uploads/uploads
    M->>ME04: Tạo lecture (expected AC-21)
    ME04-->>Web: #47 201 data.id (expected; client redirect chưa wire)
    M->>Web: Mở /mentor/lectures/:lectureId
    Web->>API: Bearer JWT + path lecture_id
    API->>Auth: Validate token và role MENTOR
    Auth-->>API: Numeric principal hoặc 401/403
    API->>API: Parse signed int64; lỗi hiện map 404
    API->>DB: Q1 lecture + parent course; kiểm tra direct owner
    API->>DB: Q2 linked UploadAsset theo owner/purpose/course, order
    DB-->>API: Lecture row + asset metadata
    API-->>Web: 200 ApiEnvelope<Lecture> hoặc safe error
    Web-->>M: Map các field được API trả về; phần còn lại đang blocked
```

Flow Web trong sơ đồ là expected/proposed. Current Web runtime route, token client, state cache và redirect chưa được tìm thấy.

### API #48 current source trace

1. `app/api/v1.py` đăng ký `GET /api/v1/mentor/lectures/{lecture_id}` và gọi `get_lecture(...)` với raw path, Authorization, Session và trace ID.
2. `validate_current_user_request(..., role="MENTOR")` chạy trước path parse và DB. Token thiếu/sai trả 401; role khác trả 403.
3. `parse_lecture_id` nhận signed int64; giá trị malformed/overflow trả 404 theo implementation hiện tại (catalog không khai báo 422).
4. Q1 `FIND_MENTOR_LECTURE` đọc `lessons` `LEFT JOIN courses`, match `lessons.id`, loại `status='DELETED'`. Không có row trả 404; course_id/parent course thiếu trả 500 integrity error; `courses.mentor_id != JWT principal` trả 403.
5. Q2 đọc association `lesson_uploads` và `uploads` theo `asset_position ASC, upload_id ASC`, scoped theo owner, `purpose='LECTURE'`, `course_id`. Không có links trả `assets: []`; link/metadata không khớp hoặc query lỗi trả 500.
6. Handler map `name→title`, `sort_order→order`, giữ `content` nullable và `status` lưu trong DB. Response là 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Lecture>`.
7. API read-only, không INSERT/UPDATE/DELETE/commit. Khi có lỗi giữa chừng, handler rollback session và chỉ trả safe business code/message.

`lesson_uploads` migration 005 và legacy DB.sql là checked-in artifacts. API #48 DD ghi live DB chưa xác minh; V1-PILOT schema dùng model UUID/version khác. Không coi local tests, DDL hay route registration là runtime verification.

### API #48 response mapping

| Response field | Type/nullable | UI mapping | Current source rule |
|---|---|---|---|
| `success`, `businessCode`, `message`, `meta`, `traceId` | envelope | API status/message boundary | Success 200 `DESIGN_RESOURCE_RETRIEVED`; errors dùng helper chung. `error_response` source đặt `data:null`; API DD #48 có câu mô tả mâu thuẫn rằng helper trả `{}` — ghi nhận discrepancy, source hiện hành ưu tiên. |
| `data.id` | int64 | #9; ID lecture | `lessons.id`, direct. |
| `data.course_id` | int64, required | Course context for #7/ME-03/ME-06 handoff | `lessons.course_id`; NULL/missing parent là 500 theo local handler. Đây là numeric ID, không phải course code/tên. |
| `data.title` | string, required | #11 | `lessons.name → title`. |
| `data.content` | string or null | #18 candidate only | Giữ nguyên text/SQL NULL. #47 nhận `content:int64` và lưu chuỗi thập phân; không xác nhận đây là Markdown/HTML/code/documentation. |
| `data.assets[]` | array, required | #21; child fields underpin #22/#23 | Ordered UploadAsset rows; `[]` nếu không có association. |
| `assets[].id/name/url/content_type/size_bytes/status` | int64/string/uri/string/int64/string | file name/type/size/status metadata; `url` is not proof access is available | `uploads.id/file_name/url/content_type/size_bytes/status`; scoped owner/purpose/course. |
| `data.order` | int32 | optional position metadata only if product decides to show it | `lessons.sort_order → order`. No module/chapter/neighbor semantics. |
| `data.status` | string in runtime model; catalog enum unspecified | #8 | Return stored value except `DELETED` is filtered before mapping. No Mentor status update endpoint. |

### Expected/current discrepancies

| Item | Expected/design | Current evidence | Status / impact |
|---|---|---|---|
| Study Web route | `/mentor/lectures/:lectureId` | No editable client source/router/package; static anchors are `#`. | `UNWIRED`; cannot claim route/redirect. |
| AC-21 access | Mentor may own or be assigned course | #48 checks only `courses.mentor_id == numeric JWT principal`. | `DISCREPANCY`; assigned-course authorization is unsupported. |
| API status | Inventory/catalog snapshot labels #48 `D`; local server has route/module/focused test source. | Source registration is local, API DD remains Draft. | `DISCREPANCY`; do not equate declaration or local source with deployment. |
| Screenshot projection | Author, video, analytics, discussions, course tree and lesson neighbors | Not fields of #48 response. | `DISCREPANCY`; no fabricated response mapping. |
| Lecture content | Academic formatted notes/code | API #48 returns nullable string; #47 stores decimal string from int64 input. | `DISCREPANCY`; display/content serialization needs API/Product decision. |
| Status/actions | Published badge, status menu, edit action | #48 returns status, filters `DELETED`; it does not change status or lecture fields. #47 creates PUBLISHED. | `DISCREPANCY`; hide/disable actions until contract. |
| Resources | Download/open PDF and GitHub | #48 returns UploadAsset metadata URL. Public URL/provider reachability is not verified; GitHub destination is mock data. | `IMPLEMENTATION BLOCKED`; URL exposure/use policy and link source required. |
| Course outline | Current/previous/next lesson tree | #48 has only `course_id` and `order`; no list/detail projection. #49/ME-06 is a separate flow. | `DISCREPANCY`; define navigation and lesson source. |
| Discussion link | Mockup names ST-25 | Inventory links ME-03/ME-06, and ST-25 is a Student screen. | `DISCREPANCY`; cross-role target is not approved for Mentor. |
| API DD / schema | Finalized persistence and DTO contract | API #48 DD is Draft; migrations/live DB, identity, content/null, enum, path mapping remain open. | `IMPLEMENTATION BLOCKED`; confirm before relying on DB result. |

### Trích từ DD nguồn: 5. State, error and access matrix

| State | Entry condition | Required display/data | Current/API evidence |
|---|---|---|---|
| `loading` | Proposed route starts #48 request | Loading treatment that preserves page context; avoid rendering fixture data. | Expected by inventory; Study Web implementation absent. |
| `ready` | #48 returns 200 and valid `data` | Source-backed lecture fields only; keep null content and empty assets explicit. | Current local API behavior, not deployed/browser verified. |
| `unauthenticated` | #48 returns 401 | Safe auth-required state; redirect/refresh behavior requires existing auth contract. | API source status; client auth policy absent. |
| `forbidden` | Wrong role or direct-owner mismatch | Access denied without revealing another Mentor's lecture details. | #48 guard and owner branch return 403. |
| `not-found` | Invalid/out-of-range path, absent row or `DELETED` row | Not-found state. Do not distinguish hidden/tombstoned rows. | #48 currently maps invalid ID and missing/deleted row to 404. |
| `error` | DB failure, missing parent, broken upload association or response projection | Safe generic error; preserve trace ID for support; retry policy still needs UI decision. | Source returns 500 `DESIGN_INTERNAL_ERROR`; no raw DB details. |
| `empty-assets` | #48 succeeds with `assets:[]` | Valid success; asset section may show approved empty state. | Test source verifies empty array; not run in this session. |
| `null-content` | #48 returns `content:null` | Valid response; fallback copy/section behavior needs product approval. | Response model nullable; current #47 content semantics unresolved. |

**Authorization/data rules:** API #48 authenticates server-side and does not accept mentor ID from request. Direct knowledge of a lecture ID does not grant access. Never place Bearer tokens in route/query. API #48 filters `DELETED` but does not require `PUBLISHED`; do not hide draft status by assumption. AC-21 assigned-course support is not implemented by this direct-owner source.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #48; không tự bổ sung edit lecture endpoint nếu không có contract.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [ME-05](../../screen_stitch/04_mentor/ME-05_xem-bai-giang-mentor/ME-05.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
