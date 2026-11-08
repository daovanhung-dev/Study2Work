# AD-08 — Chỉnh sửa khóa học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-08` |
| Module | Admin |
| Route | `/admin/courses/:courseId/edit` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Detailed Design:** `DD BLOCKED` · **Implementation:** `IMPLEMENTATION BLOCKED` · **Study Web runtime:** `NOT VERIFIED` (`UNWIRED` in current checkout)<br> |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-08.md](../../screen_stitch/05_admin/AD-08_chinh-sua-khoa-hoc/AD-08.md), [AD-08_PLAN.md](../../screen_stitch/05_admin/AD-08_chinh-sua-khoa-hoc/AD-08_PLAN.md), [AD-08_markers.json](../../screen_stitch/05_admin/AD-08_chinh-sua-khoa-hoc/AD-08_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Sửa metadata khóa, ảnh/giá nếu contract xác nhận.
- In-scope: GET #74 → PUT #75 → revalidate #74; không có API create admin course ở V1. #75 locally returns an updated Course projection; whether the UI also re-fetches #74 is open.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-32 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Sửa metadata khóa, ảnh/giá nếu contract xác nhận. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #74, #75
- Liên kết màn hình dự kiến: [AD-07](../AD-07-ChiTietKhoaHocQuanTri/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/ready/dirty/saving/422/unauthorized/forbidden/not-found/service-error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-08 source screen.png](../../screen_stitch/05_admin/AD-08_chinh-sua-khoa-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-08_chinh-sua-khoa-hoc/screen_annotated.png))
- Luồng: GET #74 → PUT #75 → revalidate #74; không có API create admin course ở V1. #75 locally returns an updated Course projection; whether the UI also re-fetches #74 is open.
- Priority: P1; Gate/source status: **R**; #75 route/module/test source exists, API DD remains Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** catalog/AC omit PUT body; local four-field full-replacement body and rules are DERIVED; thumbnail upload contract absent; mentor edit mockup conflicts with #75; AC-32 permission vs `ADMIN`, legacy/live schema, response/revalidation and Study Web UNWIRED remain open; Back/Cancel currently point to AD-06; **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-08 — Chỉnh sửa khóa học quản trị

> **Detailed Design:** `DD BLOCKED` · **Implementation:** `IMPLEMENTATION BLOCKED` · **Study Web runtime:** `NOT VERIFIED` (`UNWIRED` in current checkout)<br>
> **Screen:** AD-08 · **Actor:** Admin có course-management permission theo AC-32 · **Route đề xuất:** `/admin/courses/:courseId/edit` · **AC:** AC-32 · **API:** #74, #75<br>
> **Assets:** [screen nguyên trạng](../../screen_stitch/05_admin/AD-08_chinh-sua-khoa-hoc/screen.png) · [screen đánh số](../../screen_stitch/05_admin/AD-08_chinh-sua-khoa-hoc/screen_annotated.png) · [marker map](../../screen_stitch/05_admin/AD-08_chinh-sua-khoa-hoc/AD-08_markers.json) · [kế hoạch](../../screen_stitch/05_admin/AD-08_chinh-sua-khoa-hoc/AD-08_PLAN.md)

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### Expected behavior

AD-08 là màn hình chỉnh sửa metadata Course được inventory đề xuất tại `/admin/courses/:courseId/edit`. AD-07 chuyển numeric `Course.id`; không dùng chuỗi “Mã học phần” trong mockup thay cho ID. Theo inventory/AC-32, màn hình cần lấy Course qua GET #74, cho phép sửa theo contract được duyệt, gửi PUT #75 và làm mới hoặc revalidate dữ liệu theo quyết định client/API. AD-07 là màn hình liên kết; AD-09 sở hữu nhánh status/delete #76/#77.

Catalog #75 khai báo `PUT /api/v1/admin/courses/{course_id}`, Bearer JWT/Admin, `course_id:int64`, response `ApiEnvelope<Page<Course>>`, success `DESIGN_RESOURCE_UPDATED` và lỗi 401/403/404/422/500. Catalog và AC-32 **không khai báo request body**. API #75 DD vẫn `Draft — Needs Confirmation`; body bốn trường trong DD/backend hiện tại là candidate `DERIVED`, không phải contract được duyệt.

### Current behavior và trạng thái bằng chứng

| Chủ đề | Expected / contract | Current source hoặc prototype | Trạng thái |
|---|---|---|---|
| Route/ID | Proposed `/admin/courses/:courseId/edit`, numeric `Course.id` từ AD-07. | Không có Study Web package, route, entrypoint hay API client source trong checkout; HTML không khai báo router. | `UNWIRED`; route chưa chạy được. |
| Load/save | GET #74 → PUT #75 → revalidate #74 theo inventory. | HTML không gọi API. Local #75 tự đọc projection qua query #74 trong cùng transaction và trả projection đó trong response. | Client revalidation/cache policy `OPEN`; không kết luận phải gửi thêm GET. |
| Form | Chỉ field được owner/API duyệt mới thành editable. | Title, code, mentor, price, description, thumbnail và Save hiện disabled. Không có handler/fetch/API client. | Prototype read-only; chưa có UI behavior được triển khai. |
| Body #75 | Catalog/AC không nêu body. | Local strict model yêu cầu `title:string`, `description:string|null`, `thumbnail_url:string|null`, `price:string`; từ chối field thừa. | Body full replacement là `DERIVED`; API DD Draft. |
| Validation | Chưa có body policy được duyệt. | Local source kiểm tra title dài tối đa 200 (không trim/không nonblank), decimal string cho price (không exponent, tối đa 2 số thập phân, 10 số nguyên; số âm được chấp nhận), nullable description/thumbnail; thumbnail không được kiểm tra URI. | Chỉ là current/DERIVED candidate; không áp làm product rule khi chưa duyệt. |
| Thumbnail | Prototype gợi ý upload PNG/JPG và hiển thị `#75`. | Module #75 chỉ nhận `thumbnail_url`; không có multipart upload hay upload API trong route/module này. | Upload contract/constraints `NOT FOUND`; không được coi copy mockup là API behavior. |
| Mentor | Prototype nói cập nhật mentor và có select. | #75 body/SQL không nhận hoặc cập nhật mentor; response #74 chỉ trả owner hiện tại. | `DISCREPANCY`; mentor mutation phải được xác nhận/tách API. |
| Schema | Catalog dùng int64 Course ID. | Legacy candidate DDL có BIGINT và `name VARCHAR(200)`/`NUMERIC(12,2)`; V1-PILOT DDL mô tả Course UUID/versioned. Live schema không được chứng minh. | `OPEN`; không nâng candidate DDL thành live contract. |
| Quyền | AC-32 yêu cầu Admin có course-management permission. | Local #75 dùng shared JWT role `ADMIN`; không có check permission riêng. | `OPEN`; role ADMIN không chứng minh fine-grained permission. |
| Static preview/claims | Course data phải có nguồn từ API/config có contract. | Preview, Active, mã lô, mentor, 14 chương, 342 học viên, “Production Ready”, phiên bản, API paused/locked, RBAC, S3, audit/gateway/integrity đều là HTML tĩnh. | Không dùng làm dữ liệu hay trạng thái runtime. #74/#75 không xác nhận các chỉ số/claim này. |
| Links | Back/cancel phải theo approved route/history. | “Quay lại chi tiết (AD-07)” và “Hủy bỏ” đều có `href="/admin/courses"` (AD-06 list); các shell/footer links dùng `#`. | `DISCREPANCY`; destination và list-state restore chưa được quyết định. |

### Actor, điều kiện và liên kết

- **Actor dự kiến:** Admin có quyền course management theo precondition AC-32. Catalog ghi Bearer JWT/Admin; current API source chỉ xác minh role `ADMIN`, chưa chứng minh AC permission mapping.
- **Route parameter:** `courseId` dự kiến nhận numeric `Course.id` từ AD-07. Local #75 parse signed int64, chấp nhận giá trị âm nếu nằm trong miền; screen không tự áp positive-only rule khi chưa có contract.
- **Trước khi vào:** Cần route/client được wire, session token và ID. Khi load thành công từ #74, candidate Course fields gồm `id`, `title`, nullable `description`, nullable `thumbnail_url`, decimal-string `price`, `status`, `mentor`. Không có `course_code`, category hoặc counter trong local projection được AD-07 kiểm tra.
- **Sau khi lưu thành công:** Local #75 trả Course projection trong singleton `Page<Course>` và cập nhật metadata cùng `updated_at`. Cách client áp dụng response, gọi GET #74 lần nữa hoặc invalidate cache chưa được quy định. Quay về AD-07 hay giữ lại form cũng chưa được chốt.
- **Điều hướng liên quan:** AD-07 → AD-08 là handoff ID; AD-08 → AD-07 là return candidate; AD-06 là danh sách mà prototype hiện trỏ tới; AD-09 xử lý #76/#77. Không dùng API public #08 để thay GET #74.

### Nguồn truy vết

- [Screen inventory](../../list_screen.md) · [Global screen plan](../../screen_stitch/dd_screens/PLAN.md) · [AC-32 admin flow](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [API catalog](../../../../../docs/lists/list_api.md) · [API #75 route](../../../../study-server/app/api/v1.py) · [request model](../../../../study-server/app/modules/admin/api_75_admin_course_update/models.py) · [validator](../../../../study-server/app/modules/admin/api_75_admin_course_update/validate.py) · [view](../../../../study-server/app/modules/admin/api_75_admin_course_update/view.py) · [SQL](../../../../study-server/app/modules/admin/api_75_admin_course_update/query.py)
- [API #75 open questions](../../../../study-server/docs/dd/75_admin_course_update/OPEN_QUESTIONS.md) · [API #75 verification report](../../../../study-server/docs/dd/75_admin_course_update/VERIFICATION_REPORT.md) · [API #75 tests](../../../../study-server/tests/modules/admin/api_75_admin_course_update/test_admin_course_update.py)
- [API #74 detail source](../../../../study-server/app/modules/admin/api_74_admin_course_detail/query.py) · [Course response model](../../../../study-server/app/modules/guest/_shared/course_catalog/models.py) · [legacy schema candidate](../../../../../infra/postgres/study-server/DB.sql) · [V1-PILOT Course schema](../../../../../infra/postgres/02_study_db.sql)
- [Study Web design context](../../../../../.agents/web-study/design.md) · [Study Web scope index](../../../../../.agents/web-work/study/INDEX.md)
