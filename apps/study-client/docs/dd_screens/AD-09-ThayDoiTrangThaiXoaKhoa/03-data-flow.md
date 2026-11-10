# AD-09 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Mô tả luồng hoạt động tổng thể

### EV-01 — Mở action route và tải target Course (#74)

- **Trigger/type:** Route entry từ AD-06/AD-07 hoặc deep link; `Load`. Mục tiêu, chưa có Study Web handler.
- **Preconditions:** Router/client được wire, numeric `courseId` và Bearer token tồn tại; AC-32 permission mapping được xác nhận.
- **Inputs:** Path `:courseId` → API `course_id:int64`; không body/query. Candidate GET #74: `GET /api/v1/admin/courses/{course_id}`.
- **Processing:** Client lấy Course/current status từ #74 theo AD-07 policy. Current #74 local query đọc course + mentor, không status-filter; không có counters. Kiểm tra success envelope/identity theo API contract cuối đã phê duyệt.
- **Outcome/errors:** 200 → `ready` với target Course/current status; 401/403/404/500 → trạng thái tương ứng; lỗi mạng → client-side state chưa có policy. Không hiển thị placeholder như một Course đã được chọn.
- **Current behavior:** Target card rỗng; không có GET call. Study Web runtime `UNWIRED`.

### EV-02 — Chọn action radio

- **Trigger/type:** Change trên radio group `course_action`; các giá trị HTML là `draft`, `archive`, `delete`.
- **Input/current behavior:** `draft` được `checked` ban đầu; cùng tên group làm lựa chọn độc quyền theo native radio. Một `change` listener tồn tại nhưng body chỉ là comment; CSS `peer-checked` đổi trạng thái nhìn thấy. Listener không cập nhật context/status/reason và không gọi API.
- **Target interpretation:** AC-32 tách status (#76) và delete (#77). Lowercase radio values không phải request values: `draft` chưa được contract map thành `DRAFT`; `archive` không nằm trong local #76 candidate enum; `delete` có thể chỉ ra nhánh #77 sau khi policy duyệt. Không tự map archive sang SUSPENDED/DELETED hoặc chọn trạng thái đích thay user.
- **Outcome:** Hiện chỉ selection visual trong prototype. Không có confirmation dialog, body generation hoặc side effect được wire.

### EV-03 — Xác nhận đổi status (#76)

- **Trigger/type:** Click Confirm với action đã được định nghĩa là status update; current Confirm #33 `disabled`, `type=button`, không handler.
- **Preconditions:** Course loaded; selection ánh xạ tới enum được owner duyệt; target state, transition/readiness/learner access, permission và response/reload policy đã chốt. Không có #76 transition matrix trong current source.
- **Direct request:** `PATCH /api/v1/admin/courses/{course_id}` status subpath `/status`; Bearer JWT; int64 path; catalog không khai báo body/query. Local candidate dùng JSON `{ "status": "DRAFT" | "PUBLISHED" | "SUSPENDED" }`, strict/extra-forbid. Không có `reason`, `course_action`, `archive`, course metadata hoặc `Idempotency-Key` trong approved direct contract.
- **Local processing order:**
  1. FastAPI giải mã/validate body model; invalid/missing/extra status có thể trả 422 trước view-level guard.
  2. View gọi shared auth guard role `ADMIN`; thiếu/sai token → 401; role không đạt → 403. AC-32 fine-grained course-management permission chưa được thực thi.
  3. Parse signed-int64 `course_id`; malformed/out-of-range → 422. No positive-only rule at parse stage.
  4. `SELECT status FROM courses WHERE id=:course_id FOR UPDATE`; SQL failure → rollback/safe 500; no row → rollback/404.
  5. Nếu stored status bằng target thì không update timestamp/audit; nếu khác, update status + `updated_at`, check returned id/status, rồi insert `course_status_audit_logs(course_id, actor_user_id, previous_status, new_status)` trong cùng transaction.
  6. Read Course/mentor projection qua query #74; kiểm tra identity và status khớp; tạo singleton `Page<Course>` (1/1/1/1). Projection/map/page errors rollback/500.
  7. Commit sau khi response projection hợp lệ; commit error rollback/500.
  8. Thành công trả 200 `DESIGN_RESOURCE_UPDATED`, message `Course status updated.`, Course Page, meta và trace ID. Local response Page cardinality là DERIVED.
- **Error/result:** Catalog/local statuses 401/403/404/422/500. Current source không trả 409 và không có transition gate. Target PUBLISHED có thể phù hợp public listing filter của API #06; enrollment access khi SUSPENDED và readiness khi publish chưa được #76 chốt. No enrollment/content mutation is performed by #76.
- **Current result:** Không thể submit từ prototype; reason control disabled. No audit reason is sent.

### EV-04 — Xác nhận delete (#77)

- **Trigger/type:** Click Confirm với action được duyệt là delete; current Confirm disabled and no handler.
- **Preconditions:** Course loaded; owner đã phê duyệt soft-delete marker, dependency coverage, repeat behavior, lifecycle/restore, permission và response/reload policy. Server dependency checks remain authoritative.
- **Direct request:** `DELETE /api/v1/admin/courses/{course_id}`, Bearer JWT; int64 path; catalog không body/query. Không gửi audit reason hoặc hard-delete flag.
- **Local processing order:**
  1. Shared `ADMIN` guard trước raw path parsing/DB; missing/invalid auth → 401, insufficient role → 403. Fine-grained AC-32 policy vẫn chưa có source.
  2. Parse signed int64; malformed/out-of-range → 422. Không có positive-only rule ở parser.
  3. Lock Course nếu `status IS DISTINCT FROM 'DELETED'`; query error → rollback/500; missing/already DELETED → rollback/404.
  4. Query candidate dependencies: any enrollment row; any generic Content with `deleted_at IS NULL`; any lesson, quiz or assignment row. Query/projection error → rollback/500.
  5. Nếu dependency tồn tại, rollback không mutation và trả 422 `DESIGN_VALIDATION_ERROR`, message `Course with enrollments or content cannot be deleted.` Dependency set/history coverage là DERIVED.
  6. Nếu không có candidate dependency, update `courses.status='DELETED'`, `updated_at=CURRENT_TIMESTAMP`; trả id và DB updated_at.
  7. Map `DeleteResult {id, status:"deleted", deleted_at}`; commit sau khi result hợp lệ; update/map/commit failure rollback/safe 500.
  8. Thành công trả 200 `DESIGN_RESOURCE_DELETED`, `Course deleted.`, DeleteResult, meta, trace ID. Không xóa child records, không cascade, không audit.
- **Error/result:** Catalog/local statuses 401/403/404/422/500. Repeated delete currently 404, not idempotent success. 422 is a validation-code fallback for dependencies, not 409. Catalog does not specify predicate/message.
- **Current result:** Radio selection alone never calls #77. Copy “xóa vĩnh viễn” is contradicted by local soft marker and must not be used as confirmed product behavior.

### EV-05 — Cancel/back và reload sau mutation

- **Trigger/type:** Click Back #14 or Cancel #32; click after successful mutation reloads or navigates per future client policy.
- **Current:** Both anchors have `href="/admin/courses"`; Back copy says AD-07, actual route is proposed AD-06 list. No unsaved-state guard. No mutation on cancel.
- **Expected candidate:** Return to AD-07 with same Course ID or AD-06 list according to approved navigation/history; inventory links both AD-06/AD-07. AC-32 says reload course management after a mutation. Exact GET #73/#74 order, list filter/page restore, whether to stay on route and status/delete success copy remain open.
- **Important current result:** Local #73/#74 list/detail query does not filter `DELETED`, so refresh does not necessarily remove a soft-deleted Course from Admin data. #76 also has no deleted-target filter and can overwrite DELETED with DRAFT/PUBLISHED/SUSPENDED; whether that is an allowed restore path is unresolved.

### EV-06 — Shell/footer/policy affordances

- **Trigger/type:** Click/hover/focus nav, notification, RBAC/policy links, footer links; static render.
- **Current:** Shell/footer anchors use `#`; notification is a no-handler button. System status, automatic RBAC comparison, safe gate, ISO reason, learner enrollment warning, policy/retention copy are static; no API or monitoring call exists.
- **Expected:** Only wire route, permission signal, retention, audit reason, support/resource or monitoring behavior if a source contract is approved. #74/#76/#77 do not establish those claims.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

| State | Entry condition | Display/data behavior | Exit/navigation | Evidence/status |
|---|---|---|---|---|
| `UNWIRED` | Current checkout | Static page; radio selection only; Confirm/reason disabled; no API client/router. | No feature route can run. | Current status. |
| `initial` | Proposed route before target load | No Course selected; do not imply a valid target. | Start EV-01 if route is wired. | Target state; prototype currently shows this. |
| `loading` | #74 request pending | Show pending state only while the request is active. | 200 → `ready`; API/network errors → matching state. | Not implemented. |
| `ready` | #74 returns target Course/current status | Show identity and status from response; no counters unless contract adds them. | Select action → `action_selected`; back/cancel via approved route. | Not implemented; #74 source-backed locally. |
| `action_selected` | User selects one approved branch | Current prototype has draft/archive/delete, default draft; values are not approved request mappings. | Status target → `confirm_status`; delete target → `confirm_delete`; cancel → EV-05. | Only native radio selection works; listener no-op. |
| `confirm_status` | User is about to send approved #76 target | Confirm target state and impact using owner-approved language. No current confirmation copy/state beyond page form. | Confirm → `status_working`; cancel → ready. | Confirmation semantics not implemented/approved. |
| `confirm_delete` | User is about to call #77 | State whether operation is a soft marker and disclose dependency blockers only after policy approval. Do not promise permanent delete. | Confirm → `delete_working`; cancel → ready. | Delete semantics/policy open. |
| `status_working` | PATCH #76 pending | Prevent unintended repeated action only under approved UI policy; network retry/idempotency open. | 200 → `done`; 422/401/403/404/500/network → error state. | Target state. |
| `delete_working` | DELETE #77 pending | Do not assume physical removal. | 200 → `done`; 422 dependency → `conflict`; 401/403/404/500/network → matching state. | Target state. |
| `conflict` | #77 local dependency candidate returns 422 | Present safe message; do not expose learner/content records. Catalog code is 422 validation; local predicate/message DERIVED. | Return to action context under approved UI flow. | Current backend candidate; UI not wired. |
| `validation_error` | #76 body/path or #77 path 422 | Map error only after field/error envelope policy is approved. | Correct supported input and resubmit. | API status exists; body policy open. |
| `unauthorized` | API 401 | Use shared session-expiry behavior; no redirect/refresh rule established here. | Shared auth flow. | Catalog status; UI open. |
| `forbidden` | API 403 | Do not use static RBAC badge as evidence of permission. | Shared forbidden behavior. | Catalog status; dedicated permission open. |
| `not_found` | #74/#76/#77 404 | Distinguish missing Course from already-DELETED #77 local result only if approved copy permits. | AD-06 or shared not-found flow; destination open. | Local source behavior. |
| `service_error` | API 500 | Safe message, no database detail. | Retry/navigation policy open. | Catalog status. |
| `network_error` | Request cannot reach server | Distinct from server 500; timeout/retry policy unspecified. | Recovery behavior open. | Client state only. |
| `done` | Valid 200 #76 or #77 response | Status branch returns Page<Course>; delete branch returns DeleteResult. Exact message/route and reload sequence need approval. | AC-32 reload management; choose #73/#74 route behavior. | Target state; client unwired. |

**Transition notes:** AC-32 says reload management after either mutation. Inventory suggests GET #73/#74. #76 current response already includes Course projection; #77 returns DeleteResult only. Do not assume a second GET, cache invalidation or dialog close behavior. Local #73/#74 expose DELETED status; #76 can replace it. Do not mark a course hidden, restored, or permanently removed without the lifecycle decision. No explicit 409 is cataloged; local #77 dependency uses 422. No client timeout, retry or duplicate-submit policy is specified.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: PATCH #76 hoặc DELETE #77 sau khi policy được duyệt → reload #73/#74 theo điều hướng được chốt.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [AD-09](../../screen_stitch/05_admin/AD-09_thay-doi-trang-thai-xoa-khoa/AD-09.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
