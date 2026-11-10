# AD-14 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

### EV-01 — Mở route và tải Lesson

1. Caller dự kiến là AD-13, mang selected numeric `Lesson.id`; đây là handoff candidate từ #83, không phải route đã được triển khai.
2. Khi Study Web được wire và quyền được chốt, route guard phải kiểm tra Admin policy. Current backend APIs chỉ xác thực Bearer/JWT role `ADMIN`; AC-34 yêu cầu thêm lesson-management permission chưa được hiện thực.
3. Request candidate: `GET /api/v1/admin/lessons/{lesson_id}` (#83), không body/query. #83 đọc raw path sau auth; local malformed/out-of-range ID thành 404, không query DB.
4. HTTP 200 trả trực tiếp `ApiEnvelope<Lesson>`. Chỉ map `id`, `course_id`, `title`, nullable `content`, nullable `video_url`, `order`, `status`; #83 không trả course title, content type, module/chapter, progress, resource counts, audit hay metrics.
5. Missing/tombstoned Lesson → 404; auth → 401/403; query/projection → safe 500. Dữ liệu lỗi theo helper hiện tại có `data:null`.
6. Hiện screenshot hiển thị “Chưa nạp bản ghi…”, mọi form input disabled; đây là prototype state, không phải request/loading result.

### EV-02 — Chỉnh local metadata fields

- **Input:** giá trị trong form sau khi #83 thành công; trong ảnh các input/select/textarea đều disabled.
- **Candidate field mapping:** title ↔ `data.title`; description ↔ nullable `data.content`; order ↔ `data.order`. `course_id` là read-only/preserve candidate vì #84 không nhận course reassignment.
- **Unmapped:** content type không có field ở Lesson #83/#84; `video_url` có trong #83/#84 nhưng không có control trong mockup. Current #84 body bắt buộc cả bốn key; bỏ key gây 422, còn tự chèn giá trị cũ hay null đều là quy tắc chưa được duyệt.
- **Local state:** `dirty`/field validation có thể được thiết kế sau khi contract chốt; prototype không có change event hoặc unsaved-change handling. Không thêm positive/unique order rule hay URL scheme validator từ mockup.

### EV-03 — Lưu thông tin bằng API #84

1. Trigger candidate: một trong hai nút “Lưu thay đổi thông tin” (nút form hoặc nút action-card); cả hai hiện disabled, không có handler. Hai nút là một action candidate nhưng cách đồng bộ dirty state chưa có contract.
2. Direct catalog/AC chỉ nêu `lesson_id:int64`; current local request model là DERIVED strict body `{title:string, content:string|null, video_url:string|null, order:int32}`. Tất cả key bắt buộc, extra field bị từ chối; title tối đa 200 ký tự nhưng chuỗi rỗng được chấp nhận, không trim; content/video_url có thể null; order không có positivity/uniqueness rule.
3. Form hiện không thể tạo body đầy đủ mà không tự quyết định `video_url`; `course_id` và `content_type` không được body hiện tại nhận. Giữ action disabled/unresolved cho tới khi owner chốt field mapping.
4. Current router parse body model trước khi gọi handler. Body sai/missing/extra/type lỗi → 422 trước auth và không truy vấn DB. Với body hợp lệ, shared `ADMIN` guard chạy trước raw path validation/query; invalid signed-int64 path → local 422.
5. View update `name/content/video_url/sort_order/updated_at`, chỉ khi row chưa `DELETED`; không đổi course/status, không query dependency. Map `UPDATE ... RETURNING` thành reusable Lesson rồi commit. No row → 404 + rollback; query/mapping/commit failure → safe 500 + rollback.
6. 200 trả Lesson direct với `DESIGN_RESOURCE_UPDATED`. AC-34 diagram yêu cầu quay lại/reload AD-12; query preservation, success message, retry và concurrency behavior chưa có contract.

### EV-04 — Đổi trạng thái bằng API #85

1. Trigger candidate là nút “Thay đổi trạng thái xuất bản”; hiện disabled. UI không có select/radio target status trong ảnh.
2. Direct catalog/AC không khai báo body hay enum. Current local body DERIVED là strict `{status}` với `DRAFT|PUBLISHED|SUSPENDED`; `ARCHIVED` không được nhận. Body malformed/unknown status → 422 trước handler/auth.
3. Với body hợp lệ, shared `ADMIN` guard chạy trước raw signed-int64 path check/query; path lỗi → 422.
4. Local view lock Lesson chưa `DELETED`. Không có row → 404. Nếu target bằng current status, trả Lesson hiện tại, không update/audit nhưng vẫn commit để giải phóng lock.
5. Nếu status khác, update `status` và `updated_at`, sau đó insert actor ID + previous/new status vào `lesson_status_audit_logs` cùng transaction; lỗi query/audit/mapping/commit rollback, trả safe 500.
6. 200 trả Lesson direct. Current code không kiểm tra progress, course readiness, moderation approval hay transition matrix. Migration 012 và enum là candidate local; không hiển thị audit history vì response không chứa nó.
7. Sau success, AC-34 mô tả reload AD-12. Quy tắc confirmation cho publish/suspend và điều hướng lỗi chưa được thống nhất.

### EV-05 — Xóa bài học bằng API #86

1. Trigger candidate là nút xóa; hiện disabled. Inventory kỳ vọng delete confirmation/dependency handling, nhưng screenshot không có dialog hoặc confirm input; text/bước xác nhận cần owner quyết định.
2. Request direct: `DELETE /api/v1/admin/lessons/{lesson_id}`, Bearer/JWT, path only, không body/query. Shared `ADMIN` guard chạy trước raw signed-int64 parser/query; malformed/out-of-range signed int64 → local 422.
3. Local view khóa row chưa có tombstone bằng `FOR UPDATE`. Missing/already `DELETED` → 404. Sau đó một `EXISTS` projection kiểm tra mọi `lesson_progress`, `resources`, `lesson_uploads` theo lesson ID.
4. Nếu bất kỳ cờ nào true, rollback, không mutate và trả 422 `DESIGN_VALIDATION_ERROR` với message tổng quát. Client không nhận biết loại/count dependency; #83 không cung cấp preflight dependency.
5. Nếu các cờ false, update `lessons.status='DELETED'`, `updated_at=CURRENT_TIMESTAMP`; không hard-delete/cascade child, không ghi audit #85. Response `data` gồm `id`, literal `status:"deleted"`, DB-returned `deleted_at`; commit sau khi result mapping hợp lệ.
6. Query/projection/commit error → rollback + safe 500. Lock + check + update trong cùng transaction là local implementation; live PostgreSQL/FK/lock behavior chưa xác minh.
7. Success theo AC-34 quay lại/reload AD-12/#82. Không tự xóa resources, uploads, progress hoặc quiz; không suy ra dependency set ngoài ba relation đang có.

### EV-06 — Hủy hoặc quay lại

- Nút “Quay lại danh sách bài học (AD-12)” nêu đích AD-12, nhưng `href="#"` không điều hướng. Breadcrumb “Quản lý bài học” cũng là `#`.
- Nút “Hủy bỏ và quay lại” không nêu màn hình đích; không đoán quay AD-13 hay AD-12. Không có evidence cho confirm unsaved changes.
- Hủy/back không gọi mutation API; việc giữ filter/query/history khi trở về cần contract của AD-12/Study router.

### EV-07 — Admin shell, badges, policy copy và footer

- Navigation, Notification, Admin identity, RBAC, `SYSTEM NORMAL`, policy/security copy và footer hiện là HTML tĩnh; anchor destinations là `#`, button Notification không có listener.
- Không gọi API để xác minh system health, identity, audit, permission, data retention hoặc support ticket từ màn hình này.
- UI target khi implementation: theo `.agents/web-study/design.md`; source guide là intended design, không phải runtime.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

| State | Entry condition | UI behavior / action | Status |
|---|---|---|---|
| `route-unresolved` | Study Web has no editable router and `lessonId` is only proposed. | Do not treat the screenshot as an implemented page. | Current `UNWIRED` |
| `loading` | Future route calls #83 with a valid selected ID. | Show loading feedback without exposing static “system normal” as request status. | Expected; not implemented |
| `ready` | #83 returns a Lesson and caller is authorized under approved policy. | Map only confirmed fields; disable unsupported course/type/dependency edits. | Expected; field/permission blockers remain |
| `dirty` | An enabled, approved form field differs locally. | Keep unsaved values; cancel behavior requires confirmation policy. | Target only |
| `saving` | #84 request in flight. | Prevent duplicate submission if that behavior is approved; no current client code. | Target only |
| `status-changing` | #85 request in flight. | Separate from #84; status gate and confirmation unresolved. | Target only |
| `deleting` | #86 request in flight after approved confirmation UX. | Keep server-side dependency recheck authoritative. | Target only |
| `dependency-blocked` | #86 returns 422 for a local progress/resource/upload dependency. | Show API error without fabricating type/count; retry only after dependency policy allows. | Current API local behavior; UI not wired |
| `validation-error` | #84/#85 body/path is rejected with 422. | Render only returned field errors; do not invent validation messages. | API local behavior, body semantics DERIVED |
| `not-found` | #83/#84/#85/#86 returns 404 for absent/tombstoned target. | Offer navigation only after destination is confirmed. | API local behavior |
| `unauthenticated` / `forbidden` | 401 / 403. | Respect approved session/permission handling; current AC-specific permission is missing. | API local role guard; UI behavior unverified |
| `error` | Network or 500 failure. | Keep or discard local changes only by approved policy; no retry policy in contract. | Target only |
| `success-return` | #84/#85/#86 succeeds. | AC-34 expects reload of AD-12/#82; retain filters only if AD-12 router contract specifies them. | Expected by AC; not wired |

| Navigation | Data handoff | Evidence / limitation |
|---|---|---|
| AD-13 → AD-14 | Candidate numeric `Lesson.id` → `lessonId`. | API #83 int64 response/path; proposed route only. |
| AD-14 header back → AD-12 | Label explicitly names AD-12. | Current anchor is `#`; no selection/filter/history preservation. |
| Cancel → prior screen | No route data. | Destination unspecified in mockup/AC; unresolved. |
| Successful #84/#85/#86 → AD-12 | Refetch lesson list using #82. | AC-34 diagram; no client cache/filter behavior specified. |
| #83 404 / 401 / 403 / 500 | No extra ID or dependency payload. | Handle with existing approved shell/session policy when defined. |

## 4. Luồng đọc (Read)
- Orchestration từ inventory: AD-13 numeric `Lesson.id` → GET #83 → riêng một nhánh PUT #84 / PATCH #85 / DELETE #86 → reload AD-12/#82 theo AC-34.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [AD-14](../../screen_stitch/05_admin/AD-14_sua-doi-trang-thai-xoa-bai-hoc/AD-14.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
