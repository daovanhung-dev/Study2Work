# Open Questions — API #50 Tạo nội dung mới

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** `POST /api/v1/mentor/content`

Các câu hỏi này phân biệt DDL artifact với production approval và các mapping/lifecycle chưa chốt. Không tự tạo enum member, payload field, business code hoặc HTTP status để lấp gap.

## Implementation decisions recorded 2026-10-25

Local runtime implements the following decisions using the user's diagram → infra → catalog → simplest-clear-option priority. These remain `DERIVED`, not product-approved rules:

| Topic | Current local behavior | Remaining question |
|---|---|---|
| Mentor/course authorization | Shared `MENTOR` JWT guard and direct `courses.mentor_id` ownership. | Is an assigned/co-managing Mentor also allowed? |
| Missing course | Same 403 `DESIGN_ACCESS_DENIED` as non-owner; API #50 has no 404. | Confirm desired product semantics; no new status/code is used. |
| Initial status | `PENDING_REVIEW` from AC-33 queue condition. | Confirm create → pending transition and complete status enum. |
| Parent/order | Root `parent_id=NULL`; next active root `content_order`, first value 0; course row lock during allocation. | Confirm initial placement/order convention and whether other writers need the same lock. |
| Payload/type | Open string `content_type`, JSON object payload only. | Define enum members, subtype fields and limits. |

These open confirmations do not block local API behavior. Local TestClient/fake DB checks do not verify live schema or deployment.

## Q-50-01 — Persistence and live availability of generic Content

**Bằng chứng**

- Catalog yêu cầu `ApiEnvelope<Content>` với BIGINT `id`, `course_id`, `parent_id?` và `order`.
- AC-22 diagram chỉ ghi logical `INSERT Content`.
- Legacy `DB.sql` and migration 006 now define `contents` with the catalog base fields and BIGINT course/parent relations. V1-PILOT `content_blocks` remains a separate UUID model.

**Cần xác nhận**

1. Is checked-in `contents` the approved production model, and has migration 006 been applied to the live schema?
2. Field/column mapping, foreign key tới course, ID strategy, transaction boundary và RETURNING projection là gì?
3. Có schema đã deploy nào tương ứng không? DDL hiện có không chứng minh live schema.

**Ảnh hưởng:** Local INSERT mapping is implemented against the checked-in artifact; production schema status, migration application and lifecycle rules remain open.

## Q-50-02 — Enum `ContentType`/`ContentStatus` và payload schema là gì?

**Bằng chứng**

- Catalog chỉ đặt type `ContentType`, `ContentStatus`, `payload:object`; không liệt kê enum members hoặc cấu trúc theo subtype.
- AC-33 dùng trạng thái `PENDING_REVIEW` trong moderation queue.

**Cần xác nhận**

1. Allowed `content_type` values và mapping sang payload schema?
2. Validation bắt buộc/optional trong payload, kích thước tối đa, URI/asset reference rules?
3. `PENDING_REVIEW` is implemented as the local initial state; confirm whether it is the approved create transition and list the full status enum.

**Ảnh hưởng:** Chặn validation 422 chi tiết và kiểm chứng nội dung response.

## Q-50-03 — Quy tắc quyền quản lý course và principal binding là gì?

**Bằng chứng**

- Catalog xác định Bearer JWT và role Mentor.
- AC-22 yêu cầu Mentor có quyền quản lý course.
- Current API #50 uses the shared guard's numeric JWT subject and direct `courses.mentor_id` comparison; no assignment relation/query is source-backed.

**Cần xác nhận**

1. JWT claim nào map tới Mentor/course owner?
2. Mentor được assign/co-manage course có quyền tạo không?
3. Course tồn tại nhưng không được phép có luôn trả 403 không?

**Ảnh hưởng:** Local direct-owner authorization is implemented using current Study source; product policy for assignment access and missing-course mapping remains open.

## Q-50-04 — Parent, order và ID được gán thế nào?

**Bằng chứng**

- Request chỉ nhận `course_id`, `content_type`, `title`, `payload`.
- Response Content có `parent_id?` và `order`.

**Đề xuất cần xác nhận**

- Implementation uses a root (`parent_id=NULL`) because the request has no parent field.
- Implementation allocates next order among active roots, starting at 0, under a course-row lock. Confirm whether this is the approved display order and whether other writers share the lock.
- Local legacy DDL uses BIGSERIAL; confirm the deployed key strategy/schema before deployment.

**Ảnh hưởng:** Local response defaults are implemented; product confirmation and live schema remain open.

## Q-50-05 — Course không tồn tại hoặc body có lỗi được map thế nào?

**Bằng chứng**

- Catalog API #50 có 401/403/422/500, không có 404.
- `course_id` là body field required; enum/payload schema chưa có.

**Cần xác nhận**

- Current implementation maps absent and non-owned courses to 403 `DESIGN_ACCESS_DENIED` to avoid course ID enumeration; confirm product semantics.
- Unknown enum members are not currently checked because no member list exists; when added, map invalid values through declared 422 `DESIGN_VALIDATION_ERROR`.
- Giá trị `title` rỗng/whitespace và int64 boundary được xác định ra sao?

**Ảnh hưởng:** Local branches use only catalog codes; enum/payload validation rules remain open.

## Q-50-06 — Middleware và cross-API lifecycle

**Bằng chứng**

- API #50 route is now in `DESIGN_CONTRACT_PATHS` and TestClient verifies the framework 422 code.
- AC-22 có #49–#53; AC-33 có approve/reject và audit behavior.

**Current status and remaining confirmation**

- Local middleware wiring is complete and TestClient verifies framework 422 mapping; future edits must keep the path registered.
- Confirm consistency between create→pending review, update #51, publish #52 and delete #53 after their runtime contracts are implemented.
- Xác định audit/review metadata ở schema/API nào; không tự thêm cột trong #50.

**Ảnh hưởng:** Contract business codes và lifecycle consistency sau khi API được nối.

## Q-50-07 — Content PENDING_REVIEW có thể bị Mentor xóa không?

API #50 đề xuất tạo Content ở PENDING_REVIEW. API #53 đề xuất soft-delete Content không PUBLISHED khi không còn direct child; điều này có thể rút Content khỏi AC-33 queue nhưng diagram không mô tả withdrawal/audit. Cần xác nhận quyền xóa pending item và cách queue giữ review history.
