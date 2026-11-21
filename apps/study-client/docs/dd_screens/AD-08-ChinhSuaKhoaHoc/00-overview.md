# AD-08 — Chỉnh sửa khóa học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-08` |
| Module | Admin |
| Route | `/admin/courses/:courseId/edit` — declared trong Angular Admin router; browser/deployment runtime chưa xác minh |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Detailed Design:** `DD BLOCKED` · **Implementation:** `PARTIAL SOURCE` · **Study Web runtime:** `NOT VERIFIED`<br> |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.3 / 2026-11-20 (signed-int64 route guard) |
| Nguồn đối chiếu | [AD-08.md](../../screen_stitch/05_admin/AD-08_chinh-sua-khoa-hoc/AD-08.md), [AD-08_PLAN.md](../../screen_stitch/05_admin/AD-08_chinh-sua-khoa-hoc/AD-08_PLAN.md), [AD-08_markers.json](../../screen_stitch/05_admin/AD-08_chinh-sua-khoa-hoc/AD-08_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Sửa metadata khóa, ảnh/giá nếu contract xác nhận.
- In-scope target: GET #74 → approved PUT #75 → response/revalidation policy; không có API create admin course ở V1. Current Angular source calls GET #74 only and keeps edits in a local draft; #75 locally returns an updated Course projection, but whether UI also refetches #74 is open.
- Out-of-scope: Xem gate bên dưới; không kết luận browser/deployment runtime đã chạy.

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
| Inventory states | `list_screen.md` | Target: loading/ready/dirty/saving/422/unauthorized/forbidden/not-found/service-error |
| Current source | Angular Admin router / `AD08Page` | Route/page and GET #74 caller present; component state is `loading`/`loaded`/`error`; runtime not verified. |
| Current draft/write | `AD08Page` / `AD08ApiService` | Title/description/price draft is local component memory; no dirty state or PUT #75 caller; Save/upload disabled. |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-08 source screen.png](../../screen_stitch/05_admin/AD-08_chinh-sua-khoa-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-08_chinh-sua-khoa-hoc/screen_annotated.png))
- Current Angular source: GET #74 → map fields/local draft; there is no PUT #75 caller. Target flow and response/revalidation choice remain open.
- Priority: P1; Gate/source status: **R**; #75 route/module/test source exists, API DD remains Draft. **DD BLOCKED; IMPLEMENTATION PARTIAL SOURCE; WRITE FLOW BLOCKED:** catalog/AC omit PUT body; local four-field full-replacement body and rules are DERIVED; thumbnail upload contract absent; mentor edit mockup conflicts with #75; AC-32 permission vs `ADMIN`, legacy/live schema, and response/revalidation remain open. Angular Back/Cancel point to AD-07 with route ID; Stitch prototype links point to AD-06; **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template.
- 2026-11-16 — Re-audit Angular route/page/GET #74 and local draft; corrected Course ID label; write flow and runtime remain blocked/unverified.

## Trạng thái và ranh giới bằng chứng

# AD-08 — Chỉnh sửa khóa học quản trị

> **Detailed Design:** `DD BLOCKED` · **Implementation:** `PARTIAL SOURCE` · **Study Web runtime:** `NOT VERIFIED`<br>
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
| Route/ID | `/admin/courses/:courseId/edit`, numeric `Course.id` từ AD-07. | Angular Admin router declares the route; `AD08Page` validates the complete raw route ID against signed-int64 bounds before GET #74 and preserves valid IDs unchanged. Invalid-route toolbar navigation returns to AD-06. Stitch HTML remains static. | Route/page/GET caller present; malformed/missing/out-of-range IDs skip GET; runtime unverified. |
| Load/save | GET #74 → approved PUT #75 → response/revalidation per client/API decision. | Angular page calls GET #74 only; local #75 reads its projection in the same transaction and returns it. | Read/draft present; no PUT caller; response/revalidation policy `OPEN`. |
| Form | Chỉ field được owner/API duyệt mới persist. | Angular title/description/price inputs update a local component-memory draft; ID and mentor are read-only, thumbnail selection and Save are disabled. | Draft source present; no dirty state, persistence, or PUT caller. |
| Body #75 | Catalog/AC không nêu body. | Local strict model yêu cầu `title:string`, `description:string|null`, `thumbnail_url:string|null`, `price:string`; từ chối field thừa. | Body full replacement là `DERIVED`; API DD Draft. |
| Validation | Chưa có body policy được duyệt. | Local source kiểm tra title dài tối đa 200 (không trim/không nonblank), decimal string cho price (không exponent, tối đa 2 số thập phân, 10 số nguyên; số âm được chấp nhận), nullable description/thumbnail; thumbnail không được kiểm tra URI. | Chỉ là current/DERIVED candidate; không áp làm product rule khi chưa duyệt. |
| Thumbnail | Prototype gợi ý upload PNG/JPG và hiển thị `#75`. | Module #75 chỉ nhận `thumbnail_url`; không có multipart upload hay upload API trong route/module này. | Upload contract/constraints `NOT FOUND`; không được coi copy mockup là API behavior. |
| Mentor | Prototype nói cập nhật mentor và có select. | #75 body/SQL không nhận hoặc cập nhật mentor; response #74 chỉ trả owner hiện tại. | `DISCREPANCY`; mentor mutation phải được xác nhận/tách API. |
| Schema | Catalog dùng int64 Course ID. | Legacy candidate DDL có BIGINT và `name VARCHAR(200)`/`NUMERIC(12,2)`; V1-PILOT DDL mô tả Course UUID/versioned. Live schema không được chứng minh. | `OPEN`; không nâng candidate DDL thành live contract. |
| Quyền | AC-32 yêu cầu Admin có course-management permission. | Local #75 dùng shared JWT role `ADMIN`; không có check permission riêng. | `OPEN`; role ADMIN không chứng minh fine-grained permission. |
| Preview/claims | Course data phải có nguồn từ API/config có contract. | Angular preview binds the local title/description/price draft and #74 mentor/status; it does not load a thumbnail or show metrics. Stitch prototype claims/metrics remain static and unsupported by #74/#75. | Use only source-backed fields; prototype claims are not runtime evidence. |
| Links | Back/cancel phải theo approved route/history. | Stitch prototype links target `/admin/courses`; Angular Back/Cancel RouterLinks target `/admin/courses/:courseId` with the raw route ID. | Prototype/source differ; Angular destination is present in source, runtime unverified. |

### Current Study Web source re-audit — 2026-11-20

- AD08Page validates the complete raw `courseId` against API #74's optional-sign signed-int64 path parser before requesting; it does not use JavaScript `Number`. Missing, malformed, or out-of-range IDs show a local error and skip GET #74. Valid IDs are passed unchanged.
- The toolbar back link returns invalid IDs to AD-06 and keeps valid IDs contextual to AD-07. The cancel link is only rendered after a successful #74 response, so its route ID has passed validation. #75 save and thumbnail upload remain unavailable; write contract, permission mapping and Stitch route discrepancy remain open. Runtime and tests were not checked in this continuation.

### Current #74 response audit (2026-11-21)

- Before creating the local draft, AD-08 requires `DESIGN_RESOURCE_RETRIEVED` and the exact locally implemented #74 singleton `Page<Course>` shape: one valid Course/mentor item and pagination `1/1/1/1`. A missing, multi-item, malformed or empty success response goes to the safe error state.
- The route ID stays a raw string for the request/navigation; the response Course ID is not compared through JavaScript number conversion. #75 Save and thumbnail upload remain unavailable, and runtime is unverified.

### Actor, điều kiện và liên kết

- **Actor dự kiến:** Admin có quyền course management theo precondition AC-32. Catalog ghi Bearer JWT/Admin; current API source chỉ xác minh role `ADMIN`, chưa chứng minh AC permission mapping.
- **Route parameter:** `courseId` route string được giữ nguyên để gọi #74 và hiển thị; local #75 parse signed int64, chấp nhận giá trị âm nếu nằm trong miền. Screen không tự áp positive-only rule khi chưa có contract.
- **Trước khi vào:** Angular route/page/GET caller có trong source; browser/deployment runtime chưa xác minh. Page cần Admin session và ID. Khi load thành công từ #74, Course fields gồm `id`, `title`, nullable `description`, nullable `thumbnail_url`, decimal-string `price`, `status`, `mentor`. Không có `course_code`, category hoặc counter trong local projection được AD-07 kiểm tra.
- **Sau khi lưu thành công:** Local #75 trả Course projection trong singleton `Page<Course>` và cập nhật metadata cùng `updated_at`. Cách client áp dụng response, gọi GET #74 lần nữa hoặc invalidate cache chưa được quy định. Quay về AD-07 hay giữ lại form cũng chưa được chốt.
- **Điều hướng liên quan:** AD-07 → AD-08 handoff ID có trong source; Angular Back/Cancel về AD-07 với raw route ID; Stitch prototype links vẫn trỏ tới AD-06. AD-09 xử lý #76/#77. Không dùng API public #08 để thay GET #74.

### Nguồn truy vết

- [Screen inventory](../../list_screen.md) · [Global screen plan](../../screen_stitch/dd_screens/PLAN.md) · [AC-32 admin flow](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [API catalog](../../../../../docs/lists/list_api.md) · [API #75 route](../../../../study-server/app/api/v1.py) · [request model](../../../../study-server/app/modules/admin/api_75_admin_course_update/models.py) · [validator](../../../../study-server/app/modules/admin/api_75_admin_course_update/validate.py) · [view](../../../../study-server/app/modules/admin/api_75_admin_course_update/view.py) · [SQL](../../../../study-server/app/modules/admin/api_75_admin_course_update/query.py)
- [API #75 open questions](../../../../study-server/docs/dd/75_admin_course_update/OPEN_QUESTIONS.md) · [API #75 verification report](../../../../study-server/docs/dd/75_admin_course_update/VERIFICATION_REPORT.md) · [API #75 tests](../../../../study-server/tests/modules/admin/api_75_admin_course_update/test_admin_course_update.py)
- [API #74 detail source](../../../../study-server/app/modules/admin/api_74_admin_course_detail/query.py) · [Course response model](../../../../study-server/app/modules/shared/course_catalog/models.py) · [legacy schema candidate](../../../../../infra/postgres/study-server/DB.sql) · [V1-PILOT Course schema](../../../../../infra/postgres/02_study_db.sql)
- [Study Web design context](../../../../../.agents/web-study/design.md) · [Study Web scope index](../../../../../.agents/web-work/study/INDEX.md)
