# AD-14 — Sửa, đổi trạng thái, xóa bài học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-14` |
| Module | Admin |
| Route | `/admin/lessons/:lessonId/edit` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: # AD-14 — Sửa, đổi trạng thái, xóa bài học; **Trạng thái màn hình:** `DD BLOCKED` · `IMPLEMENTATION BLOCKED` · `RUNTIME NOT VERIFIED` · **API source:** #83–#86 local routes/modules/tests có source; DD API vẫn Draft và live DB chưa xác minh.<br> |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-14.md](../../screen_stitch/05_admin/AD-14_sua-doi-trang-thai-xoa-bai-hoc/AD-14.md), [AD-14_PLAN.md](../../screen_stitch/05_admin/AD-14_sua-doi-trang-thai-xoa-bai-hoc/AD-14_PLAN.md), [AD-14_markers.json](../../screen_stitch/05_admin/AD-14_sua-doi-trang-thai-xoa-bai-hoc/AD-14_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Sửa Lesson, đổi status hoặc xóa theo policy; xử lý lỗi dependency ở server.
- In-scope: AD-13 numeric `Lesson.id` → GET #83 → riêng một nhánh PUT #84 / PATCH #85 / DELETE #86 → reload AD-12/#82 theo AC-34.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-34 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Sửa Lesson, đổi status hoặc xóa theo policy; xử lý lỗi dependency ở server. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #83, #84, #85, #86
- Liên kết màn hình dự kiến: [AD-12](../AD-12-DanhSachBaiHocQuanTri/00-overview.md), [AD-13](../AD-13-ChiTietBaiHocQuanTri/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/ready/dirty/saving/status-changing/deleting/dependency-blocked/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-14 source screen.png](../../screen_stitch/05_admin/AD-14_sua-doi-trang-thai-xoa-bai-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-14_sua-doi-trang-thai-xoa-bai-hoc/screen_annotated.png))
- Luồng: AD-13 numeric `Lesson.id` → GET #83 → riêng một nhánh PUT #84 / PATCH #85 / DELETE #86 → reload AD-12/#82 theo AC-34.
- Priority: P1; Gate/source status: **R** local #83–#86 route/module/query/model/test source; API DDs Draft. #84 full-replacement body `{title,content,video_url,order}` và #85 `{status}`/enum/audit là DERIVED; #86 rechecks `lesson_progress`, `resources`, `lesson_uploads` and returns 422 on any reference. **DD BLOCKED; IMPLEMENTATION BLOCKED:** #84 form/body mismatch (no `video_url`, course/type unmapped), #85 `ARCHIVED` vs local `SUSPENDED`, dependency set/output, `ADMIN` vs lesson-management permission, legacy/V1-PILOT/live schema, Study Web `UNWIRED`; **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-14 — Sửa, đổi trạng thái, xóa bài học

> **Screen:** AD-14 · **Actor expected:** Admin có lesson-management permission theo AC-34 · **Route đề xuất:** `/admin/lessons/:lessonId/edit` · **APIs:** #83–#86 · **Trước:** AD-13/#83, từ danh sách AD-12/#82 · **Sau mutation:** AD-12/#82 reload theo AC-34<br>
> **Trạng thái màn hình:** `DD BLOCKED` · `IMPLEMENTATION BLOCKED` · `RUNTIME NOT VERIFIED` · **API source:** #83–#86 local routes/modules/tests có source; DD API vẫn Draft và live DB chưa xác minh.<br>
> **Assets:** [screen nguồn](../../screen_stitch/05_admin/AD-14_sua-doi-trang-thai-xoa-bai-hoc/screen.png) · [screen chú thích](../../screen_stitch/05_admin/AD-14_sua-doi-trang-thai-xoa-bai-hoc/screen_annotated.png) · [marker map](../../screen_stitch/05_admin/AD-14_sua-doi-trang-thai-xoa-bai-hoc/AD-14_markers.json) · [kế hoạch](../../screen_stitch/05_admin/AD-14_sua-doi-trang-thai-xoa-bai-hoc/AD-14_PLAN.md) · [inventory](../../list_screen.md)

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### Mục tiêu và expected behavior

AD-14 là trang Admin được inventory đề xuất để cập nhật metadata, đổi trạng thái hoặc xóa một Lesson đã chọn ở AD-13. AC-34 mô tả ba nhánh mutation riêng, sau đó reload danh sách qua API #82. Chỉ truyền `Lesson.id` dạng số khi client mapping được xác nhận; `lessonId` là tên route đề xuất, còn API nhận `lesson_id:int64`.

| Thuộc tính | Expected behavior | Current evidence |
|---|---|---|
| Mục tiêu | Sửa nội dung Lesson; thay đổi trạng thái qua action riêng; xóa theo policy dependency. | `code.html` là prototype tĩnh, chưa có binding/event/API. |
| Actor/quyền | Admin có lesson-management permission theo AC-34. | #84–#86 guard role `ADMIN`; chưa có policy permission riêng. |
| Route | `/admin/lessons/:lessonId/edit` theo inventory và mockup. | Study Web router/source không có trong checkout; route chưa tồn tại được xác minh. |
| Handoff | Từ AD-13 bằng selected Lesson ID; AD-13 #83 trả candidate numeric `id`. | API #83 trực tiếp trả Lesson; #83 không trả dependency list/count. |
| Mutation | Chỉ chọn một nhánh PUT #84, PATCH #85 hoặc DELETE #86. | Cả ba route có local source; request/body và policy còn các phần DERIVED. |
| Sau mutation | AC-34 reload danh sách lesson qua #82. | Không có client navigation/cache behavior để xác minh; filter/history carry-over chưa được contract. |

### API boundary

| API | Direct design | Local source hiện tại | Kết quả chính |
|---|---|---|---|
| #83 GET `/api/v1/admin/lessons/{lesson_id}` | Path int64, Bearer/Admin, `ApiEnvelope<Lesson>`, 200; errors 401/403/404/500. | Shared `ADMIN`, raw signed-int64 validation, đọc một Lesson không `DELETED`, không đọc dependencies; lỗi path local 404. | `data: {id, course_id, title, content?, video_url?, order, status}`; field mapping kế thừa #09. |
| #84 PUT `/api/v1/admin/lessons/{lesson_id}` | Catalog/AC chỉ khai báo path; direct response Lesson; 200, errors 401/403/404/422/500. | Strict required full-replacement body `{title, content, video_url, order}` là DERIVED; update metadata, commit sau projection hợp lệ. Typed body validation chạy trước handler/auth. | Trả Lesson; giữ `course_id` và `status`; không ghi dependency/audit. |
| #85 PATCH `/api/v1/admin/lessons/{lesson_id}/status` | Direct path/auth/response/error set; catalog và AC không khai báo body/enum. | `{status}` và `DRAFT|PUBLISHED|SUSPENDED` là DERIVED; lock, đổi `status` + `updated_at`, ghi old/new/actor audit trong một transaction; same-status là no-op không audit. Typed body validation chạy trước handler/auth. | Trả Lesson; audit candidate table theo migration 012, chưa chứng minh live. |
| #86 DELETE `/api/v1/admin/lessons/{lesson_id}` | Path-only, `ApiEnvelope<DeleteResult>`, 200, errors 401/403/404/422/500; AC yêu cầu theo policy/dependency. | Shared `ADMIN`, lock, kiểm tra `lesson_progress`, `resources`, `lesson_uploads`; có reference trả 422, không có thì đặt `status='DELETED'`. Dependency/tombstone/timestamp rules là DERIVED. | `{id, status:"deleted", deleted_at}`; local `deleted_at` lấy DB `updated_at`. |

Tất cả API DD #84–#86 đang `Draft — Needs Confirmation`; #83 cũng Draft. Tài liệu và source local không xác minh schema/deployment đang chạy. Không có retry, timeout, optimistic version, idempotency token hoặc cache policy được contract khai báo.

### Current prototype và giới hạn

`screen.png` 1510×1600 và `code.html` được giữ nguyên. Prototype có 5 form controls đều disabled, 4 nút mutation disabled, các anchor dùng `href="#"`, status/identity/RBAC/SYSTEM NORMAL là copy tĩnh. Không có route param, fetch/XHR, API URL, data binding, listener, timer, SSE hay WebSocket. Study Web hiện chỉ có docs/assets, ignored `dist` và `node_modules`; editable source, package manifest, router và API client không có. Trạng thái `UNWIRED`.

### Blocker / discrepancy

1. **#84 body:** catalog/AC không khai báo body; source dùng full replacement DERIVED. Form có `course_id` selector và content-type selector nhưng #84 không nhận các field đó; #84 yêu cầu `video_url` nhưng form không có control. Không tự đoán giữ/clear giá trị ẩn.
2. **#85 status:** mockup hiển thị Draft/Published/Archived; source fallback nhận `DRAFT`, `PUBLISHED`, `SUSPENDED`. Không tự map Archived sang Suspended; không có transition/readiness/progress gate.
3. **#86 dependencies:** #83 không trả dependencies; #86 chỉ recheck tại mutation-time với ba relation cục bộ. Danh sách dependency đầy đủ, cách diễn giải progress và UX xác nhận xóa cần owner/schema review.
4. **Authorization:** AC-34 fine-grained lesson-management permission chưa có source policy; `ADMIN` role không chứng minh quyền riêng.
5. **Schema:** legacy `lessons` BIGINT có `course_id`, `sort_order`, `status` nullable; reusable Lesson yêu cầu `course_id`, `order`, `status`. V1-PILOT là UUID/versioned Lesson khác. Migration 012 là checked-in candidate, không chứng minh live deployment.
6. **UI/runtime:** controls hiện disabled và không có frontend source; Study Web design target khác palette/font/width mockup. Không claim frontend behavior hoặc runtime.
