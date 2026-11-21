# AD-21 — Sửa/kiểm soát/đo trạng thái thông báo · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-21` |
| Module | Admin |
| Route | `/admin/notifications/:notificationId` — Angular route/page đã đăng ký trong Admin router; runtime chưa xác minh |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); **DD status:** `DD BLOCKED` — API detail/lifecycle/permission/operation mapping chưa đủ contract.; **Implementation status:** `IMPLEMENTATION PARTIAL SOURCE` — route/page và caller chỉ đọc #96 đã wired; #94/#95 và client handoff/poller #18 chưa wired.; **Runtime status:** `RUNTIME NOT VERIFIED`. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.2 / 2026-11-20 |
| Nguồn đối chiếu | [AD-21.md](../../screen_stitch/05_admin/AD-21_sua-kiem-soat-do-trang-thai-thong-bao/AD-21.md), [AD-21_PLAN.md](../../screen_stitch/05_admin/AD-21_sua-kiem-soat-do-trang-thai-thong-bao/AD-21_PLAN.md), [AD-21_markers.json](../../screen_stitch/05_admin/AD-21_sua-kiem-soat-do-trang-thai-thong-bao/AD-21_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Xem notification/status; sửa hoặc delete/cancel chỉ sau khi policy cho phép; SH-07 handoff có điều kiện.
- In-scope: #96 là GET status, không có GET detail riêng và không trả delivery counts/per-channel status; #94 catalog path-only nhưng local body `{title,content}`/QUEUED-only là DERIVED; #95 catalog DELETE trả `deleted`, local source hard-delete row và không dừng provider; chỉ gọi #18 sau khi Operation ID/type/owner/producer mapping được duyệt.
- Out-of-scope: Xem gate bên dưới; không kết luận live runtime/deployment hoặc approval chỉ từ source/tests.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-36 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Xem notification/status; sửa hoặc delete/cancel chỉ sau khi policy cho phép; SH-07 handoff có điều kiện. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #18, #94, #95, #96
- Liên kết màn hình dự kiến: [AD-19](../AD-19-DanhSachThongBaoQuanTri/00-overview.md), [SH-07](../SH-07-TheoDoiTacVuBatDongBo/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | expected: draft/scheduled/sending/delivered/failed; local fallback: QUEUED/SENT/FAILED |
| Current Study Web source | Angular route/page + GET #96 | `loading / loaded / error`; invalid/missing route IDs stop locally before GET; runtime/deployment chưa xác minh |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-21 source screen.png](../../screen_stitch/05_admin/AD-21_sua-kiem-soat-do-trang-thai-thong-bao/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-21_sua-kiem-soat-do-trang-thai-thong-bao/screen_annotated.png))
- Luồng: #96 là GET status, không có GET detail riêng và không trả delivery counts/per-channel status; #94 catalog path-only nhưng local body `{title,content}`/QUEUED-only là DERIVED; #95 catalog DELETE trả `deleted`, local source hard-delete row và không dừng provider; chỉ gọi #18 sau khi Operation ID/type/owner/producer mapping được duyệt.
- Priority: P1; Gate/source status: **R** local #94/#95/#96 routes/modules/query/validator/model/test source; API DDs Draft. **DD BLOCKED; IMPLEMENTATION PARTIAL SOURCE:** notification detail/projection, status/lifecycle mapping, AC-36 permission vs `ADMIN`, #94 body/edit gate, #95 cancel/delete/retention/worker coordination, delivery metrics/channel mapping, candidate legacy/live schema, #18 UUID/int64/owner/result mapping; AD-21 route/page/#96 read caller source-wired, #94/#95 actions and #18 client handoff/poller unavailable; **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.
- 2026-11-20 — AD21Page now validates raw `notificationId` against #96's positive signed-int64 parser before GET; invalid IDs stop locally and valid text remains unchanged.

## Trạng thái và ranh giới bằng chứng

# AD-21 — Kiểm soát và giám sát trạng thái thông báo

> **DD status:** `DD BLOCKED` — màn hình có kế hoạch, ảnh chú thích và đặc tả A–F; API detail/lifecycle/permission/operation mapping chưa đủ contract để lập trình an toàn.
> **Implementation status:** `IMPLEMENTATION BLOCKED` · **Runtime status:** `RUNTIME NOT VERIFIED`.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | AD-21 — Kiểm soát và giám sát trạng thái thông báo (Page theo inventory). |
| Mục tiêu | Cho Admin xem thông tin notification và trạng thái phân phối; chỉnh sửa hoặc hủy/xóa chỉ khi policy cho phép; có thể mở SH-07 nếu backend cấp Operation ID tương thích. |
| Actor / quyền dự kiến | Admin có `notification-management permission` theo AC-36. API catalog ghi role=Admin; local #94–#96 guard role `ADMIN`. Chưa có contract chứng minh guard `ADMIN` tương đương permission AC-36 hoặc xác định scope/tenant. |
| Route | `/admin/notifications/:notificationId` đã đăng ký trong Angular Admin router; current page validates raw `notificationId` as full-string positive signed-int64 before GET #96 and preserves valid text. Catalog #94–#96 khai báo `notification_id:int64`; browser runtime remains unverified. |
| Điều kiện trước | Khi triển khai: phiên xác thực hợp lệ và quyền đã được backend xác minh; notification ID do AD-19 hoặc nguồn server cấp, hợp lệ theo contract. Không có ID hợp lệ trong prototype hiện tại. |
| Kết quả sau | Đọc trạng thái nếu #96 được phép sử dụng; #94/#95 chỉ sau khi body, lifecycle và policy được duyệt. Không khẳng định gửi thành công hoặc provider đã hủy. Operation tracking chỉ qua SH-07/#18 sau khi producer, ID, ownership và route #18 thống nhất. |
| Màn hình liên kết | AD-19 là danh sách/điểm vào và đường quay lại; Angular page có RouterLink về `/admin/notifications`. Stitch HTML giữ anchor `#`/disabled như thiết kế tĩnh. SH-07 handoff vẫn có điều kiện. |
| API liên quan | #96 status read được page gọi; #94 update và #95 delete source tồn tại nhưng UI actions khóa; #18 có Study route/module/query/test nguồn cho notification-only lookup, nhưng AD-21 chưa có client handoff/poller. API DDs còn Draft. |
| Trạng thái tổng | Stitch prototype hiển thị placeholder tĩnh; Angular source hiện tải projection #96, render loading/loaded/error và giữ actions khóa. Runtime chưa xác minh. |

### Nguồn và trạng thái bằng chứng

| Nguồn | Bằng chứng / cách dùng |
|---|---|
| [Inventory row 79](../../list_screen.md) | Expected route, AC-36, API, liên kết và trạng thái dự kiến. Đây là design inventory, không phải route runtime. |
| [AC-36 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) và [macro-review](../../../../study-server/docs/dd/96_admin_notifications_status/AC-36_MACRO_REVIEW.md) | AC-36 precondition là notification-management permission; có nhánh PUT, DELETE/mark cancelled, status read và reload; review giữ open questions. |
| [API catalog](../../../../../docs/lists/list_api.md) | Contract trực tiếp cho #18/#94/#95/#96, response type và error set. Không thay bằng local fallback khi hai bên khác nhau. |
| [Study Server router](../../../../study-server/app/api/v1.py) | #18 và #94/#95/#96 routes hiện được đăng ký trong source; không chứng minh live deployment. |
| [API #94 view](../../../../study-server/app/modules/admin/api_94_admin_notifications_update/view.py), [API #95 view](../../../../study-server/app/modules/admin/api_95_admin_notifications_delete/view.py), [API #96 view/query](../../../../study-server/app/modules/admin/api_96_admin_notifications_status/view.py) | Current local auth, validation, DB effects, projection và errors; các fallback notification rules là DERIVED theo macro-review. |
| [Candidate Study DDL](../../../../../infra/postgres/study-server/DB.sql) | Legacy `notifications`/`notification_deliveries` schema trong Git; không chứng minh live DB/deployment. |
| [API #18 DD](../../../../study-server/docs/dd/18_operations/02_Overview.md) và [SH-07](../../screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07.md) | API #18 source-wired theo UUID và notification-only query; catalog int64, generic lifecycle/result và owner/Admin contract còn discrepancy. AD-21 client handoff/poller chưa wired. |
| AD-21 [`screen.png`](../../screen_stitch/05_admin/AD-21_sua-kiem-soat-do-trang-thai-thong-bao/screen.png), [`code.html`](../../screen_stitch/05_admin/AD-21_sua-kiem-soat-do-trang-thai-thong-bao/code.html) | Visual design inputs only. Source hashes are recorded in [plan](../../screen_stitch/05_admin/AD-21_sua-kiem-soat-do-trang-thai-thong-bao/AD-21_PLAN.md); original assets are unchanged. |
