# AD-19 — Danh sách thông báo quản trị · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-19` |
| Module | Admin |
| Route | `/admin/notifications (candidate; Study Web route chưa wired)` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: Source status is described in the source DD. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-19.md](../../screen_stitch/05_admin/AD-19_danh-sach-thong-bao-quan-tri/AD-19.md), [AD-19_PLAN.md](../../screen_stitch/05_admin/AD-19_danh-sach-thong-bao-quan-tri/AD-19_PLAN.md), [AD-19_markers.json](../../screen_stitch/05_admin/AD-19_danh-sach-thong-bao-quan-tri/AD-19_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Admin xem notification list; inventory mockup search/status/channel và draft/scheduled/sent là expected nhưng cần contract mapping.
- In-scope: Catalog #92 chỉ có status/channel/page và direct ApiEnvelope<Notification>; local #92 trả derived Page<Notification>, delivery-backed rows. No search, recipient/send-time fields or metrics mapping. AD-20 CTA path is /admin/notifications/create in HTML vs inventory /admin/notifications/new; guideline link unresolved.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-36 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Admin xem notification list; inventory mockup search/status/channel và draft/scheduled/sent là expected nhưng cần contract mapping. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #92
- Liên kết màn hình dự kiến: [AD-20](../AD-20-SoanGuiThongBaoHeThong/00-overview.md), [AD-21](../AD-21-SuaKiemSoatDoTrangThaiThongBao/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | unwired/loading/empty/ready/unauthorized/forbidden/validation-error/dependency-error/server-error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-19 source screen.png](../../screen_stitch/05_admin/AD-19_danh-sach-thong-bao-quan-tri/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-19_danh-sach-thong-bao-quan-tri/screen_annotated.png))
- Luồng: Catalog #92 chỉ có status/channel/page và direct ApiEnvelope<Notification>; local #92 trả derived Page<Notification>, delivery-backed rows. No search, recipient/send-time fields or metrics mapping. AD-20 CTA path is /admin/notifications/create in HTML vs inventory /admin/notifications/new; guideline link unresolved.
- Priority: P1; Gate/source status: **R** local #92 route/validator/query/model/view/focused-test source; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** catalog singleton vs local Page; enum/search/metric and recipient/send-time mapping; AC-36 permission vs ADMIN; notification grain/live schema; CTA/guidelines destinations; Study Web UNWIRED; **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-19 — Danh sách thông báo quản trị

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | AD-19 — Danh sách thông báo quản trị |
| Mục tiêu | Cho Admin xem danh sách thông báo và chuyển sang soạn mới hoặc xử lý một thông báo đã chọn, theo inventory và AC-36. |
| Actor | Admin. AC-36 yêu cầu quyền notification-management; catalog #92 ghi role Admin. |
| Route | Candidate: /admin/notifications. Chưa có route Study Web được xác minh. |
| Màn hình liên quan | AD-20 soạn/gửi; AD-21 sửa/kiểm soát/trạng thái. SH-07 chỉ là operation monitor nếu contract #93 cung cấp operation_id. |
| API liên quan | GET #92 là API đọc của màn hình. Các #93–#96 thuộc luồng màn hình kế tiếp; không gọi ngầm từ AD-19. |
| Trạng thái tài liệu | DD BLOCKED bởi các contract chưa được duyệt bên dưới; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. |
| Tài sản | [Ảnh gốc](../../screen_stitch/05_admin/AD-19_danh-sach-thong-bao-quan-tri/screen.png), [ảnh đánh số](../../screen_stitch/05_admin/AD-19_danh-sach-thong-bao-quan-tri/screen_annotated.png), [marker JSON](../../screen_stitch/05_admin/AD-19_danh-sach-thong-bao-quan-tri/AD-19_markers.json), [SVG overlay](../../screen_stitch/05_admin/AD-19_danh-sach-thong-bao-quan-tri/AD-19_markers_overlay.svg), [kế hoạch](../../screen_stitch/05_admin/AD-19_danh-sach-thong-bao-quan-tri/AD-19_PLAN.md), [HTML nguồn](../../screen_stitch/05_admin/AD-19_danh-sach-thong-bao-quan-tri/code.html). |

### Nguồn và mức độ bằng chứng

| Nguồn | Bằng chứng dùng trong DD |
|---|---|
| [Inventory](../../list_screen.md#L203), [global screen plan](../../screen_stitch/dd_screens/PLAN.md#L159) | Route candidate, AC/API, màn hình kế tiếp, state dự kiến và mức ưu tiên. |
| [AC-36 Admin management](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio#L768) | Admin mở màn hình, gọi #92, query notifications rồi chọn nhánh create/update/delete/status và reload màn hình quản lý. |
| [API catalog #92 và Notification schema](../../../../../docs/lists/list_api.md#L52) | Direct contract: GET #92, Bearer/Admin, status/channel/page tùy chọn, ApiEnvelope<Notification> và mã HTTP được công bố. |
| [API #92 Draft DD](../../../../study-server/docs/dd/92_admin_notifications_list/00_Cover.md), [open questions](../../../../study-server/docs/dd/92_admin_notifications_list/OPEN_QUESTIONS.md) | Catalog-vs-source split, enum/pagination/grain/permission/schema questions; trạng thái Draft — Needs Confirmation. |
| [Route](../../../../study-server/app/api/v1.py#L2692), [validator](../../../../study-server/app/modules/admin/api_92_admin_notifications_list/validate.py#L54), [query](../../../../study-server/app/modules/admin/api_92_admin_notifications_list/query.py#L3), [models](../../../../study-server/app/modules/admin/api_92_admin_notifications_list/models.py#L16), [view](../../../../study-server/app/modules/admin/api_92_admin_notifications_list/view.py#L186) | Current local implementation evidence. Đây không phải owner approval cho contract khác catalog. |
| [Focused test source](../../../../study-server/tests/modules/admin/api_92_admin_notifications_list/test_admin_notifications_list.py#L121), [test context](../../../../../.agents/server-study/tests.md#L208) | Test source uses fake DB projections; existing worklog records prior test counts. Tests were not run in this screen task. |
| [Legacy DDL](../../../../../infra/postgres/study-server/DB.sql#L298), [migration 009](../../../../../infra/postgres/study-server/migrations/009_notification_delivery_outbox.sql#L1) | Checked-in BIGINT notification/delivery schema candidate only; not proof of live schema or migration deployment. V1-PILOT UUID notification model is separate. |
| [Study Web design guide](../../../../../.agents/web-study/design.md#L30) | Design guidance for future implementation. The screenshot is a static visual source and does not establish runtime styling or behavior. |

### Hợp đồng dữ liệu: expected và current

| Nội dung | Expected — catalog / AC / inventory | Current — local source / HTML |
|---|---|---|
| Response #92 | Catalog khai báo ApiEnvelope<Notification>. AC-36 nói query notifications nhưng không định nghĩa Page, item grain, metadata hoặc empty response. | Local route trả ApiEnvelope<Page<Notification>> với data.items và data.pagination. Đây là DERIVED và là DISCREPANCY so với catalog. |
| Notification fields | id:int64, title:string, content:string, channels:NotificationChannel[], status:NotificationStatus, read_at?datetime, scheduled_at?datetime, created_at:datetime. Catalog không nêu enum values. | Local item: id, title, content, channels, status, created_at. read_at và scheduled_at bị omit. Không trả recipient, sender, operation_id, scheduled send time hoặc provider IDs. |
| Query | status?:string, channel?:string, page?:int32. Không có search, size, page origin/default hoặc ordering rule. | Guard ADMIN chạy trước query parse; page mặc định 1, phải là int32 dương; filter status/channel được giữ nguyên chuỗi; count/list dùng size 20, sort created_at DESC rồi id DESC. |
| Enum | Catalog chưa liệt kê NotificationStatus/NotificationChannel. | Local channel chỉ EMAIL/PUSH; status chỉ FAILED/QUEUED/SENT. Status aggregate: có QUEUED thì QUEUED; nếu không, có FAILED thì FAILED; nếu toàn bộ delivery SENT thì SENT. |
| Grain / inclusion | AC-36 không quyết định notification theo recipient hay campaign. | Local query dùng candidate legacy BIGINT notification + delivery aggregate; chỉ có row khi tồn tại ít nhất một delivery. Không group operation_id/campaign. |
| Search / metric / columns | Inventory/mockup yêu cầu title search, draft/scheduled/sent, card counts, recipient và send time. | Không có query search hoặc metric API; #92 projection không trả recipient/send time. Không suy metric từ page hiện tại. |
| Permission | AC-36: notification-management permission. | Shared local guard yêu cầu role ADMIN; không có fine-grained permission hay tenant/sender scope trong luồng #92. |

### Quy tắc nghiệp vụ và bảo mật

- Không hiển thị hoặc coi là đã gửi các giá trị metric, badge “System Normal”, bảo đảm RBAC, thời gian review 30 phút hoặc trạng thái draft/scheduled/published chỉ vì chúng xuất hiện trên mockup.
- Trước khi gọi #92, implementation cần một quyết định về AC-36 permission và mapping role/claim. Không tự thay notification-management permission bằng role ADMIN.
- Không hiển thị PII người nhận. Local #92 không trả user_id/sender_id và API list contract chưa chốt recipient grain.
- Không đổi chữ thường trong mockup thành enum viết hoa của backend bằng suy đoán; cũng không đổi QUEUED/FAILED/SENT thành draft/scheduled/published.
- #92 là GET chỉ đọc trong source hiện tại: hai query count/list; không commit hoặc gọi provider. Đây là bằng chứng về code local, không xác nhận DB/migration/worker deployed.
