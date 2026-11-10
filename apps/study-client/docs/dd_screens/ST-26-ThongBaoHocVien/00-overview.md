# ST-26 — Thông báo học viên · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-26` |
| Module | Student |
| Route | `/student/notifications` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: Source status is described in the source DD. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-26.md](../../screen_stitch/03_student/ST-26_thong-bao-hoc-vien/ST-26.md), [ST-26_PLAN.md](../../screen_stitch/03_student/ST-26_thong-bao-hoc-vien/ST-26_PLAN.md), [ST-26_markers.json](../../screen_stitch/03_student/ST-26_thong-bao-hoc-vien/ST-26_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Lọc chưa đọc, mở deep link an toàn, mark-one/mark-all.
- In-scope: GET #43 → khi user mở POST? Không, PATCH #44; PATCH #45 khi user bấm tất cả → refresh #43.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-20 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Lọc chưa đọc, mở deep link an toàn, mark-one/mark-all. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #43, #44, #45
- Liên kết màn hình dự kiến: [ST-09](../ST-09-TongQuanKhoaDangHoc/00-overview.md), [ST-17](../ST-17-ChiTietBaiTap/00-overview.md), [ST-25](../ST-25-ChiTietThreadVaPhanHoi/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | unread/read/empty/marking/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-26 source screen.png](../../screen_stitch/03_student/ST-26_thong-bao-hoc-vien/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-26_thong-bao-hoc-vien/screen_annotated.png))
- Luồng: GET #43 → khi user mở POST? Không, PATCH #44; PATCH #45 khi user bấm tất cả → refresh #43.
- Priority: P2; Gate/source status: **D**; **BLOCK:** Payload deep-link thông báo chưa định nghĩa

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-26 — Thông báo học viên

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### A.1. Định danh và mục tiêu

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID | ST-26 |
| Tên | Thông báo học viên |
| Route dự kiến | `/student/notifications` theo [screen inventory](../../list_screen.md); current Study Web chưa có route. |
| Actor | Student đã đăng nhập theo precondition AC-20. |
| Mục tiêu expected | Tải thông báo của principal hiện tại, cho phép xem toàn bộ/chưa đọc theo contract, đánh dấu một hoặc tất cả đã đọc, đồng bộ lại danh sách. Điều hướng notification chỉ qua deep-link contract an toàn đã được duyệt. |
| Điều kiện trước | Student authenticated; API #43–#45 đều yêu cầu Bearer JWT/Student. Cụ thể session guard/redirect ở Study Web chưa có source. |
| Trạng thái | `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. |
| Screen handoff | Inventory liên kết [ST-09](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/ST-09.md), [ST-17](../../screen_stitch/03_student/ST-17_chi-tiet-bai-tap/ST-17.md), [ST-25](../../screen_stitch/03_student/ST-25_chi-tiet-thread-va-phan-hoi/ST-25.md). Screenshot CTA minh họa [ST-19](../../screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/ST-19.md), [ST-25](../../screen_stitch/03_student/ST-25_chi-tiet-thread-va-phan-hoi/ST-25.md), [ST-11](../../screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/ST-11.md), [ST-22](../../screen_stitch/03_student/ST-22_thanh-tich-va-chung-nhan/ST-22.md) và Google Meet; các destination này chưa phải route/payload contract. |

### A.2. Expected behavior — inventory và AC-20

- Inventory ST-26 khai báo notification list, filter chưa đọc, mở deep link an toàn, mark-one/mark-all. Flow expected: GET #43 → PATCH #44 hoặc PATCH #45 do action người dùng → GET #43 refresh để đồng bộ list/read state.
- AC-20: Actor Student; precondition đăng nhập; postcondition danh sách/read state được đồng bộ. Activity diagram yêu cầu đọc `NotificationRecipient` theo user, hiển thị unread badge/list, chọn nhánh one/all, cập nhật `read_at` hoặc bulk unread rows, rồi sync UI.
- API #43 catalog: `GET /api/v1/users/me/notifications`, Student Bearer; query `unread_only?:boolean`, `page?:int32`; response `ApiEnvelope<Page<Notification>>`; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`.
- API #44 catalog: `PATCH /api/v1/notifications/{notification_id}/read`, Student Bearer; path `notification_id:int64!`, no catalog query/body; response `ApiEnvelope<Page<Notification>>`; HTTP 200 `DESIGN_RESOURCE_UPDATED`, 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.
- API #45 catalog: `PATCH /api/v1/notifications/read-all`, Student Bearer; `body{}` không có property khai báo; response `ApiEnvelope<Page<Notification>>`; HTTP 200 `DESIGN_RESOURCE_UPDATED`, 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.
- Page size/order cho #43, read-state field, response Page cho #44/#45, body requiredness cho #45 và safe deep-link payload chưa được chốt. Không trình bày các proposal trong API DD như behavior đã duyệt.

### A.3. Current behavior và tài sản

- `screen.png` là ảnh populated 1081×1600, SHA-256 `e9078467e90538daffcdade2a8a80f9d2936aa99338c93071dd9eb417d93587d`. Ảnh có header Student, sáu notification mẫu, unread/category tabs, mark-all CTA, preferences/chart/help sidebars và footer.
- Screenshot tự mâu thuẫn về sample read state: bốn card đầu có chấm xanh nhưng đồng thời ghi “Đã đọc”; title/tab ghi “5 mới” trong khi chỉ bốn chấm xanh nhìn thấy. Không dùng các sample để xác lập read state/count rule.
- `code.html` SHA-256 `3c040253758a64bf2d3287ff22fcf491325773476c657b5d2ab4a680e5965922` là fallback empty-state với Guest login/register header, không có list, filter, form/button, fetch/API/auth hoặc data binding; link quay về `/student/courses`. PNG và HTML là `DISCREPANCY`; giữ nguyên cả hai, annotate PNG populated.
- HTML có Google Fonts imports và Tailwind CDN. Đây là prototype content, không phải runtime; nếu frontend được author sau này thì Study Web design target yêu cầu không thêm remote font import/package.
- Study Web hiện không có editable source/package/router/Student screen. Ignored compiled `dist` chỉ có root `/` và không xác minh serving/deployment. Không có current UI event, route, auth guard hay navigation nào được xác minh.
- Current Study Server router có notification endpoints của Mentor #63/#64 và Admin #92–#96; tìm kiếm source không thấy Student #43/#44/#45 route/module/query/test. Đây là `NOT_FOUND` trong current Study source; không lấy behavior API Mentor/Admin thay cho Student.
- Screenshot gắn status “Cập nhật tự động qua API #48”. Catalog #48 là Mentor lecture detail `GET /api/v1/mentor/lectures/{lecture_id}`; nhãn này là `DISCREPANCY`, không phải bằng chứng về notification preference API.

### A.4. API DD status, data contract và blockers

| API | Catalog request/result | API DD hiện hành | UI implication |
|---|---|---|---|
| #43 | GET; optional `unread_only:boolean`, `page:int32`; `Page<Notification>`; 200/401/403/500. | `Draft — Needs Confirmation`; 7 open questions. | Chỉ hai query fields được khai báo; category filters và explicit unread count không có trong contract. |
| #44 | PATCH; `notification_id:int64!`; no body/query; `Page<Notification>`; 200/401/403/404/422/500. | `Draft — Needs Confirmation`; 7 open questions. | Principal/recipient rule, whether repeated mark is idempotent, 404 concealment, response page and read timestamp are unresolved. |
| #45 | PATCH; catalog `body{}`; `Page<Notification>`; 200/401/403/422/500. | `Draft — Needs Confirmation`; 8 open questions. | Body requiredness/validation, bulk response rows/Page, empty result, recipient scope and state storage are unresolved. |

- Reusable schema `Notification` yêu cầu `id:int64`, `title:string`, `content:string`, `channels:NotificationChannel[]`, `status:NotificationStatus`, `created_at:date-time`; `read_at` và `scheduled_at` optional. Schema không có `is_read`, `type/category`, sender, icon, unread count hay `action_url`.
- AC-20 gọi logical `NotificationRecipient.read_at`. Checked-in legacy Study DDL candidate có `notifications.id BIGSERIAL`, nullable `user_id`/`sender_id`, `title`, `content`, `type`, `is_read BOOLEAN DEFAULT FALSE`, `created_at TIMESTAMP`, `operation_id`; không có recipient table, `read_at`, `channels`, `status`, `scheduled_at` hoặc `action_url`. `is_read` không khai báo `NOT NULL`.
- V1-PILOT DDL khác: notification ID và `learner_id` là UUID; có `read_at`, `action_url`, expiry/payload và delivery model riêng. Nó không khớp int64 catalog/current numeric Student principal. Cả hai DDL chỉ là checked-in candidate; live schema/deployment chưa được xác minh.
- Không map `type` sang `channels`, `is_read` sang `status`, boolean thành `read_at`, hoặc `NotificationRecipient` sang `notifications.user_id` mà không có quyết định schema. Không coi `action_url` từ V1-PILOT là field của API catalog.
- API #43 response thiếu field để UI xác nhận unread/read từng row; unread filtering query có thể được yêu cầu nhưng count metadata semantics của Page là proposal trong API DD. Screenshot `5 mới` không được map từ sample count/Page total khi rule chưa duyệt.
- API #43 DD đề xuất page default 1, size 20, order `created_at DESC, id DESC`; các điểm này là `DERIVED`, không phải catalog. #44/#45 response Page cũng chưa có agreed projection/metadata semantics. #44 DD candidate dùng `is_read=TRUE` nhưng diagram yêu cầu `read_at`; #45 DD candidate bulk-updates only direct-recipient rows và trả all changed rows, đều chưa approved.
- API #44/#45 không khai báo `Idempotency-Key`; không tự thêm header. Error guideline `data:null` khác `error_response()` current fallback `data:{}`; Student endpoints chưa gọi helper này, nên đây là known shared discrepancy chứ không phải verified response của #43–#45.
- Safe deep-link requirement không có source field trong catalog Notification. Screenshot CTAs (ST-19, ST-25, ST-11, ST-22, Meet) không đủ để dựng URL, IDs hoặc trust policy. Không điều hướng dựa trên notification title/body hoặc raw URL.
- Sidebar preferences (Email/Web Push/SMS), weekly chart, help/contact và footer links không được #43–#45 cung cấp. Không gán API #48 hay thêm API/setting fields.

### A.5. Bảo mật và truy vết nguồn

- Principal phải đến từ Student Bearer/JWT theo catalog; không dùng user ID từ query/body, sample avatar/tên, notification payload không tin cậy hoặc URL token.
- Notification list/mutation phải được scope theo recipient hiện tại sau khi schema/access contract được duyệt. `user_id IS NULL` broadcast rows và per-Student read state chưa có physical model; không mở rộng tới broadcast bằng suy đoán.
- Destination chỉ được mở khi typed payload, allowed route list, parameter validation và external-link policy được source-backed. Nếu contract thiếu/sai, không route từ content text.
- Sources: [screen inventory](../../list_screen.md), [API catalog](../../../../../docs/lists/list_api.md), [AC-20 API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC-20 activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio), [API #43 overview/request/response/mapping/open questions](../../../../study-server/docs/dd/43_users_me_notifications/02_Overview.md), [API #44 overview/request/mapping/open questions](../../../../study-server/docs/dd/44_notifications_mark_read/02_Overview.md), [API #45 overview/request/mapping/open questions](../../../../study-server/docs/dd/45_notifications_read_all/02_Overview.md), [notification DB guide](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [legacy Study DDL candidate](../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql), [Study Web visual/accessibility target](../../../../../.agents/web-study/design.md), current [Study router](../../../../study-server/app/api/v1.py).
