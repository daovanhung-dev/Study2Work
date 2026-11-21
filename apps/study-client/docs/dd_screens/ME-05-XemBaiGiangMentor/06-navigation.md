# ME-05 — Navigation

## 1. Route definition
- Current route in source: `/mentor/lectures/:lectureId`
- Status: registered in `mentor.route.ts`; browser/runtime not verified.
- Route params/types: `lectureId` is a positive signed int64 string, validated before request; invalid values stop before #48.
- Query params/defaults: preserve the inventory route string; detailed parsing rules only from source DD.
- Route guards: see source DD/API contract; do not create role policy.

## 2. Điểm vào
| From screen/route | Trigger | Params | Guard / fallback |
|---|---|---|---|
| [ME-04](../ME-04-TaiLenVaTaoBaiGiang/00-overview.md) | #47 create succeeds | `data.id` from created lecture | ME-04 navigates to `/mentor/lectures/:lectureId`; ME-05 reloads through #48 |

## 3. Điểm ra
| Destination | Trigger | Params | Điều kiện |
|---|---|---|---|
| [ME-03](../ME-03-WorkspaceKhoaHocCuaMentor/00-overview.md) | Activate workspace link | Validated `data.course_id` | Available only after a valid #48 response |
| [ME-06](../ME-06-CayNoiDungKhoaHoc/00-overview.md) | Activate content-tree link | Validated `data.course_id` | Available only after a valid #48 response |

## 4. Back / refresh / deep link
- Back behavior: xem source DD; không mặc định browser history.
- Preserve filters/scroll/form state: chỉ nếu source có nêu, nếu không `CẦN_XÁC_NHẬN`.
- Refresh/direct URL: route param stream reloads the current lecture and cancels a stale request; browser refresh was not exercised.
- Invalid/missing ID: invalid/overflow ID is shown locally; API #48 maps malformed/out-of-range/missing/deleted IDs to 404.
- Not authenticated/authorized: theo source role guard; xem [Business Rules](05-business-rules.md).

## 5. Diagram
```mermaid
flowchart LR
  S0["ME-05 Xem bài giảng mentor"] --> S1["ME-03"]
  S0["ME-05 Xem bài giảng mentor"] --> S2["ME-06"]
```

## Source navigation and flow detail

### Trích từ DD nguồn: 2. Luồng tổng thể và truy vết source

### Luồng đọc sau khi tạo

```mermaid
sequenceDiagram
    participant M as Mentor
    participant ME04 as ME-04
    participant Web as Study Web ME-05 route
    participant API as GET #48
    participant Auth as Shared MENTOR guard
    participant DB as lessons/courses + lesson_uploads/uploads
    M->>ME04: Tạo lecture (expected AC-21)
    ME04-->>Web: Điều hướng tới /mentor/lectures/{data.id}
    M->>Web: Mở hoặc tải lại /mentor/lectures/:lectureId
    Web->>API: Bearer JWT + path lecture_id
    API->>Auth: Validate token và role MENTOR
    Auth-->>API: Numeric principal hoặc 401/403
    API->>API: Parse signed int64; lỗi hiện map 404
    API->>DB: Q1 lecture + parent course; kiểm tra direct owner
    API->>DB: Q2 linked UploadAsset theo owner/purpose/course, order
    DB-->>API: Lecture row + asset metadata
    API-->>Web: 200 ApiEnvelope<Lecture> hoặc safe error
    Web-->>M: Render các field #48 hỗ trợ; phần mockup còn thiếu dữ liệu vẫn blocked
```

Client route, #48 caller, retry và #47 → #48 handoff hiện có trong source. Browser/runtime/deployment vẫn chưa xác minh.

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
| `data.content` | string or null | Escaped plain text in `<pre>`; null state | T041: #47 accepts Markdown `string` and stores it unchanged; #48 keeps nullable response for legacy rows. No HTML/Markdown renderer is used. |
| `data.assets[]` | array, required | #21; child fields underpin #22/#23 | Ordered UploadAsset rows; `[]` nếu không có association. |
| `assets[].id/name/url/content_type/size_bytes/status` | int64/string/uri/string/int64/string | file name/type/size/status metadata; `url` is not proof access is available | `uploads.id/file_name/url/content_type/size_bytes/status`; scoped owner/purpose/course. |
| `data.order` | int32 | optional position metadata only if product decides to show it | `lessons.sort_order → order`. No module/chapter/neighbor semantics. |
| `data.status` | string in runtime model; catalog enum unspecified | #8 | Return stored value except `DELETED` is filtered before mapping. No Mentor status update endpoint. |

### Expected/current discrepancies

| Item | Expected/design | Current evidence | Status / impact |
|---|---|---|---|
| Study Web route | `/mentor/lectures/:lectureId` | Registered route, route-param reactive page, #48 service, retry and ME-04 handoff exist. | `SOURCE-WIRED`; browser/deployment not verified. |
| AC-21 access | Mentor may own or be assigned course | #48 checks only `courses.mentor_id == numeric JWT principal`. | `DISCREPANCY`; assigned-course authorization is unsupported. |
| API status | Current screen/API matrix marks #48 `R`; API DD remains Draft. | Local route/module/query/validation/test and ME-05 caller exist; deployment/live schema remain unverified. | Source-wired locally; do not equate it with deployment. |
| Screenshot projection | Author, video, analytics, discussions, course tree and lesson neighbors | Not fields of #48 response. | `DISCREPANCY`; no fabricated response mapping. |
| Lecture content | Academic formatted notes/code | T041 approves #47 Markdown string; ME-05 renders escaped text, not formatted Markdown. #48 may return null for older rows. | Content serialization is source-backed; rich Markdown rendering remains intentionally absent. |
| Status/actions | Published badge, status menu, edit action | #48 returns status, filters `DELETED`; it does not change status or lecture fields. #47 creates PUBLISHED. | `DISCREPANCY`; hide/disable actions until contract. |
| Resources | Download/open PDF and GitHub | #48 returns UploadAsset URL but access/provider reachability is not verified; page displays metadata only. GitHub destination is mock data. | Download/preview/GitHub actions remain blocked pending URL and destination policy. |
| Course outline | Current/previous/next lesson tree | #48 has only `course_id` and `order`; no list/detail projection. #49/ME-06 is a separate flow. | `DISCREPANCY`; define navigation and lesson source. |
| Discussion link | Mockup names ST-25 | Inventory links ME-03/ME-06, and ST-25 is a Student screen. | `DISCREPANCY`; cross-role target is not approved for Mentor. |
| API DD / schema | Finalized persistence and DTO contract | API #48 DD remains Draft; live schema/migration, assigned-course support, status enum and malformed-path policy remain open. | Local source is used; no claim is made about live DB/deployment. |
