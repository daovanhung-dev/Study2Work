# ME-06 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ME-06-API-001` | #49 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #49
- Orchestration/data notes: GET #49; preserve ids/version, tránh render draft như published.
- BE/source status và gate: **D**; **BLOCK:** Content không nằm trong 18 bảng DB.sql
- Contract sources and discrepancies are preserved in the source excerpts below.

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

### Trích từ DD nguồn: 9. Nguồn đã truy vết

- Inventory: [`list_screen.md` ME-06](../../list_screen.md#L166); workflow [F08](../../list_screen.md#L61).
- API route/source: `apps/study-server/app/api/v1.py` lines 862–1028.
- #49: `apps/study-server/app/modules/mentor/api_49_mentor_content_list/{models.py,query.py,view.py,validate.py}`; tests `apps/study-server/tests/modules/mentor/api_49_mentor_content_list/test_mentor_content_list.py`.
- #50–#53: `apps/study-server/app/modules/mentor/api_50_mentor_content_create/`, `api_51_mentor_content_update/`, `api_52_mentor_content_publish/`, `api_53_mentor_content_delete/`; corresponding focused test directories under `apps/study-server/tests/modules/mentor/`.
- Persistence artifacts: `infra/postgres/study-server/DB.sql`, `infra/postgres/study-server/migrations/006_contents.sql`, `007_content_versions.sql`.
- API DD #49: [`02_Overview.md`](../../../../study-server/docs/dd/49_mentor_content_list/02_Overview.md), [`OPEN_QUESTIONS.md`](../../../../study-server/docs/dd/49_mentor_content_list/OPEN_QUESTIONS.md).
- Current static UI source: [`code.html`](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/code.html); current route/client state: `UNWIRED` in `.agents/web-work/study/`.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/ME-06.md)
