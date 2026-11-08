# ME-06 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: 2. API #49 và ánh xạ dữ liệu

### Source trace hiện tại

```mermaid
sequenceDiagram
    participant M as Mentor
    participant W as Study Web route (UNWIRED)
    participant R as GET #49 route
    participant V as get_course_contents
    participant A as MENTOR auth guard
    participant DB as courses + contents
    M->>W: Mở /mentor/courses/:courseId/content
    W->>R: Bearer JWT + course_id
    R->>V: Chuyển raw path, DB session, trace ID
    V->>A: Validate token, numeric principal, role MENTOR
    A-->>V: Principal hoặc 401/403
    V->>V: Parse signed int64
    V->>DB: Q1 course id + mentor_id
    DB-->>V: Course row; owner mismatch → 403
    V->>DB: Q2 active contents theo course, parent/order/id
    DB-->>V: Flat rows, gồm mọi status
    V->>V: Validate row/payload/IDs/parents/cycle
    V-->>R: 200 Content[] hoặc 404/500
    R-->>W: ApiEnvelope; client dựng tree theo parent_id
```

Flow Web là expected/proposed. Các bước sau route đã được đọc trong current Study Server source:

1. `apps/study-server/app/api/v1.py` đăng ký GET `/mentor/courses/{course_id}/content`, response model `GetCourseContentsEnvelope`; route chuyển raw path và dependency DB vào `get_course_contents`.
2. Shared `validate_current_user_request(..., role="MENTOR")` chạy trước mọi truy vấn. Thiếu/sai auth hoặc role sai trả lỗi auth/authorization từ helper.
3. `parse_course_id` nhận signed int64. Sai định dạng hoặc ngoài miền int64 map về 404 `DESIGN_RESOURCE_NOT_FOUND` theo handler, không trả 422 cho path.
4. `FIND_MENTOR_COURSE` đọc `courses.id, mentor_id`. Không tồn tại trả 404; principal không bằng `courses.mentor_id` trả 403 `DESIGN_ACCESS_DENIED`. Source không kiểm tra assignment relation; AC-21/AC-22 có cách diễn đạt “course phụ trách” rộng hơn direct owner.
5. `LIST_COURSE_CONTENTS` lọc đúng `course_id` và `deleted_at IS NULL`, rồi order `parent_id NULLS FIRST, content_order ASC, id ASC`; `content_order` được trả thành `order`.
6. `_map_contents` kiểm tra từng row là mapping, `payload` là JSON object, `course_id` đúng, IDs duy nhất, parent có mặt trong response và không tạo cycle. Nếu không hợp lệ, handler trả safe 500 và rollback; không trả cây một phần.
7. Tree rỗng là thành công 200 `DESIGN_RESOURCE_RETRIEVED`, `message="No course content found."`, `data:[]`. Response thành công là một mảng `Content[]` phẳng, không có pagination.
8. Endpoint chỉ đọc; không INSERT/UPDATE/DELETE/commit business data. DB và mapping lỗi trả safe 500 `DESIGN_INTERNAL_ERROR` sau rollback.

### Response contract đang chạy trong source

| Field | Type | Ánh xạ/giới hạn |
|---|---|---|
| `success`, `businessCode`, `message`, `meta`, `traceId` | envelope | Thành công 200 `DESIGN_RESOURCE_RETRIEVED`; helper chung định dạng lỗi. |
| `data` | `Content[]` | Mảng phẳng. Không có `children[]`, pagination hay version selector. UI chỉ được dựng quan hệ bằng `parent_id`. |
| `data[].id` | int64 | ID node Content; dùng làm định danh ổn định trong response. Không mặc định đây cũng là `lecture_id` của #48. |
| `data[].course_id` | int64 | Course sở hữu node; route đầu vào/current query đã scope theo course này. |
| `data[].content_type` | string mở | Không có enum member được enforce bởi #49; chưa đủ bằng chứng phân loại chapter/video/lab/quiz. |
| `data[].title` | string | Tiêu đề node. |
| `data[].payload` | JSON object | Schema bên trong chưa được xác định; không suy diễn duration, asset, rubric, quiz questions hoặc metadata từ mockup. |
| `data[].status` | string mở | API trả nguyên status của mọi node active; không chuẩn hóa nhãn/label/color cho `published/draft/hidden` nếu chưa chốt enum mapping. |
| `data[].parent_id` | int64 hoặc null | Null biểu thị root trong projection; giá trị khác dùng nối tới `data[].id`. Source bảo đảm parent hiện diện trong cây trả về. |
| `data[].order` | int32 | Map từ `contents.content_order`; đây là thứ tự hiện có, không phải endpoint ghi thứ tự. |
| `version` | Không có | Inventory yêu cầu giữ ID/version nhưng #49 response không có version. `content_versions` chỉ được ghi bởi #51; API #49 hiện không chọn/trả version. Không tự thêm field. |

### DB và trạng thái API

- Legacy checked-in `infra/postgres/study-server/DB.sql` có `contents` và `content_versions`; migration `006_contents.sql` tạo `contents`, migration `007_content_versions.sql` tạo `content_versions`. Đây là artifacts trong checkout, không chứng minh migration đã áp dụng trên live DB.
- Pilot UUID schema (`chapters`, `lessons`, `content_blocks`) khác model BIGINT mà #49 query; không trộn hai schema.
- API #49 route/module/query/test source đã được wire cục bộ; API DD [#49](../../../../study-server/docs/dd/49_mentor_content_list/02_Overview.md) vẫn `Draft — Needs Confirmation`. Local test source dùng fake DB; test không chạy trong phiên này.

### Trích từ DD nguồn: 6. Ma trận trạng thái, lỗi và bảo mật

| State | Trigger/evidence | UI rule |
|---|---|---|
| `loading` | Request #49 đang chờ | Skeleton/progress và cancel/retry behavior cần design; không có current client implementation. |
| `empty` | 200 `data:[]` | Hiển thị empty course state. Không phải lỗi; CTA create chỉ bật sau khi #50/type/parent rules được duyệt. |
| `ready` | 200 có cây đã validate | Dựng từ flat Content[] và giữ `id/status/order`; không gán mock values hoặc version không có. |
| `denied` | 401 hoặc 403 | Phân biệt sign-in/role/owner theo auth UX đã duyệt; không lộ course/node data. Current owner check direct. |
| `not-found` | 404 malformed/out-of-range path hoặc missing course | Không render mock course. Path error hiện cùng business code resource not found. |
| `error` | 500 DB/projection/tree integrity; network error ở client tương lai | Safe message, retry theo policy; không render partial tree. Network mapping chưa có source. |
| `saving/blocked` | Mutation handoff | Chỉ bật theo allowed server transition. #51/#52/#53 có 422 path; không optimistic-commit status/order. |
| `filter-empty` | Local search/filter không có row | Copy/ancestor behavior chưa có design; combine search and filter state thay vì để JS handlers ghi đè. |

- Server source yêu cầu role MENTOR và so khớp numeric principal với `courses.mentor_id`; assigned Mentor chưa được hỗ trợ ở các API này. UI không tự quyết định quyền bằng status badge.
- Mọi ID/status từ API phải được giữ an toàn; không đặt token/secret trong route. `payload` là object bất kỳ theo API model nên cần schema-specific sanitization/rendering trước khi render HTML hoặc URL.
- Không coi asset, GitHub, handbook, audit row hoặc external link trong fixture là trusted URL. Link policy/allowlist hiện chưa có contract cho ME-06.
- Keyboard/ARIA/focus, responsive behavior, loading/retry copy và destructive confirmation cần được chốt cho implementation; HTML hiện không chứng minh khả năng tiếp cận hay runtime layout ngoài snapshot desktop.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #49; preserve ids/version, tránh render draft như published.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [ME-06](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/ME-06.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
