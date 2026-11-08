# AD-05 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-05_markers.json](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/AD-05_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-05-EL-001` | `not supplied in marker JSON` | Study2Work / LMS / Admin Portal brand |
| #2 | `AD-05-EL-002` | `not supplied in marker JSON` | Primary Admin navigation group |
| #3 | `AD-05-EL-003` | `not supplied in marker JSON` | System Normal badge |
| #4 | `AD-05-EL-004` | `not supplied in marker JSON` | Notifications button |
| #5 | `AD-05-EL-005` | `not supplied in marker JSON` | Admin identity and avatar |
| #6 | `AD-05-EL-006` | `not supplied in marker JSON` | Global breadcrumb trail |
| #7 | `AD-05-EL-007` | `not supplied in marker JSON` | RBAC assurance badge |
| #8 | `AD-05-EL-008` | `not supplied in marker JSON` | User management/list/action breadcrumb |
| #9 | `AD-05-EL-009` | `not supplied in marker JSON` | Back to AD-02 link |
| #10 | `AD-05-EL-010` | `not supplied in marker JSON` | API #69/#71/#72 reference strip |
| #11 | `AD-05-EL-011` | `not supplied in marker JSON` | Page title |
| #12 | `AD-05-EL-012` | `not supplied in marker JSON` | Security shield hero icon |
| #13 | `AD-05-EL-013` | `not supplied in marker JSON` | Page subtitle |
| #14 | `AD-05-EL-014` | `not supplied in marker JSON` | Execution-context panel heading |
| #15 | `AD-05-EL-015` | `not supplied in marker JSON` | Read-Only protocol badge |
| #16 | `AD-05-EL-016` | `not supplied in marker JSON` | Target account ID card |
| #17 | `AD-05-EL-017` | `not supplied in marker JSON` | Current account status card |
| #18 | `AD-05-EL-018` | `not supplied in marker JSON` | Intervention permission card |
| #19 | `AD-05-EL-019` | `not supplied in marker JSON` | Predicted impact callout |
| #20 | `AD-05-EL-020` | `not supplied in marker JSON` | Action method label |
| #21 | `AD-05-EL-021` | `not supplied in marker JSON` | Lock-account tab |
| #22 | `AD-05-EL-022` | `not supplied in marker JSON` | Unlock-account tab |
| #23 | `AD-05-EL-023` | `not supplied in marker JSON` | Permanent-delete tab |
| #24 | `AD-05-EL-024` | `not supplied in marker JSON` | Admin reason label and required audit indicator |
| #25 | `AD-05-EL-025` | `not supplied in marker JSON` | Disabled audit-reason textarea |
| #26 | `AD-05-EL-026` | `not supplied in marker JSON` | Disabled/inactive badge |
| #27 | `AD-05-EL-027` | `not supplied in marker JSON` | System-policy warning icon |
| #28 | `AD-05-EL-028` | `not supplied in marker JSON` | Policy warning title and body |
| #29 | `AD-05-EL-029` | `not supplied in marker JSON` | Return-safe action |
| #30 | `AD-05-EL-030` | `not supplied in marker JSON` | Confirm action button |
| #31 | `AD-05-EL-031` | `not supplied in marker JSON` | API handlers and Enforced Gate footer claim |
| #32 | `AD-05-EL-032` | `not supplied in marker JSON` | Audit code and ISO compliance footer claim |
| #33 | `AD-05-EL-033` | `not supplied in marker JSON` | Copyright/system footer text |
| #34 | `AD-05-EL-034` | `not supplied in marker JSON` | Privacy/RBAC/support footer links |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

ID phải trùng marker trên [annotated screenshot](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/screen_annotated.png) và [marker map](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/AD-05_markers.json). Các vị trí là vùng tương đối trong prototype; nội dung “static” không đồng nghĩa dữ liệu runtime.

| ID | Tên / loại / vị trí / mục đích | Thuộc tính, nguồn dữ liệu, validation | Hiển thị / trạng thái / event |
|---:|---|---|---|
| #1 | Brand Study2Work / LMS / Admin Portal; brand block ở header trái. | Logo/text tĩnh; không thuộc #69/#71/#72. | Visible; static. Click destination không có handler; shell navigation thuộc EV-06. |
| #2 | Nhóm primary Admin navigation; links giữa header. | Năm label tĩnh; HTML anchors dùng `href="#"`; route destinations chưa có source. | Visible; link action chưa wired; EV-06. |
| #3 | “SYSTEM NORMAL” badge; health indicator header. | Static assertion; không có health endpoint/data trong flow AD-05. | Visible nhưng không verified; không dùng làm trạng thái API/runtime; EV-06. |
| #4 | Notifications icon/button; header phải. | Không có unread count, data source hoặc handler. | Visible; click effect chưa được xác định; EV-06. |
| #5 | Admin name/role/avatar; identity block header phải. | Hard-coded. #69 trả target user, không phải identity của Admin hiện tại. | Visible; Admin profile source ngoài flow này; EV-06. |
| #6 | Global breadcrumb trail; đầu vùng nội dung. | Label tĩnh, chưa có route-state binding. | Visible; destinations/click behavior chưa wired; EV-05/EV-06. |
| #7 | “Chuẩn xác thực RBAC” badge; phải breadcrumb. | Claim tĩnh, không phải output của #69/#71/#72 hoặc permission evaluation result. | Visible nhưng không verified; không dùng làm authorization gate; EV-06. |
| #8 | User management / account list / action breadcrumb; nội dung trên trái. | Static labels; không truyền numeric ID hay route state trong HTML. | Visible; navigation theo route cần duyệt; EV-05. |
| #9 | “Quay lại danh sách người dùng (AD-02)” link; trên phải của breadcrumb. | Hiện `href="/admin/users"`; không có selected-user query/state. | Visible; click không được router xác minh; EV-05. |
| #10 | API #69/#71/#72 reference strip; dưới breadcrumb. | Tên API tĩnh; không phải proof các API được gọi/wired. | Visible; no event/request state; EV-06. |
| #11 | Page title “Kiểm soát trạng thái và quyền truy cập tài khoản”; hero heading. | Static copy. | Visible; no API source field; presentation only. |
| #12 | Security shield hero icon; trái title. | Decorative icon, không biểu diễn policy evaluation hoặc permission result. | Visible; no event. |
| #13 | Subtitle mô tả session/revoke/delete impact; dưới title. | Static copy. “Dừng toàn bộ phiên” không được local #71/#72 hỗ trợ: suspend revoke eligible refresh rows; access JWT có thể còn hạn; delete không revoke token rows. | Visible; phải chỉnh khi policy được duyệt; EV-06. |
| #14 | Execution-context panel heading; đầu panel xanh. | Static title. | Visible; no event. |
| #15 | “Giao thức Read-Only” badge; góc phải panel. | Static state; không có server gate/config source. | Visible; không bảo đảm mutation guard; EV-06. |
| #16 | Target account ID card; cột trái trong panel. | Mockup cho biết chưa chọn user; ID bị rút gọn. Khi wired, candidate source `UserProfile.id` / route `userId`, `int64`; path validation theo API. | Visible; no-selection/loading/ready; EV-01. Không dùng giá trị hard-coded làm request. |
| #17 | Current account-status card; cột giữa panel. | Mockup “Không xác định”; map `UserProfile.status:string` từ #69 sau khi PII/status display policy được duyệt. Không có approved enum mapping ở đây. | Visible; loading/ready/error; EV-01. Không map alias `active/locked/pending` theo suy đoán. |
| #18 | Intervention-permission card; cột phải panel. | Mockup “Bị khóa bởi chính sách”. Không có permission-decision API/field trong #69/#71/#72. | Visible; permission pending/allowed/denied chỉ sau auth/permission contract; EV-01/EV-06. Không suy ra từ badge #7. |
| #19 | Predicted-impact callout; dưới ba account cards. | Static impact copy; phải phản ánh đúng approved session/delete policy trước khi bật action. | Visible; không phải API result; EV-06. |
| #20 | Action-method label; phía trên tabs. | Static label. | Visible; no event. |
| #21 | Lock-account tab; tab trái. | `role="tab"`, selected mặc định trong HTML. Candidate action có thể tương ứng #71 `{status:"SUSPENDED"}` chỉ sau khi body/state policy được duyệt. | Visible, selected only in static markup; click chỉ đổi draft action sau khi ready; EV-02. |
| #22 | Unlock-account tab; tab giữa. | `role="tab"`, unselected. Candidate action #71 `{status:"ACTIVE"}` chỉ sau approval. Local ACTIVE không phục hồi refresh tokens đã revoked. | Visible; no handler in prototype; EV-02. |
| #23 | Permanent-delete tab; tab phải. | `role="tab"`, unselected; label “Xóa tài khoản vĩnh viễn” lệch local #72 soft marker, không hard delete/anonymize. | Visible; action disabled until deletion/lifecycle policy approved; EV-02. |
| #24 | Admin-reason label + required audit indicator; đầu form. | Required marker là static; không có body field/audit persistence contract ở #71/#72. | Visible; mandatory status not approved; EV-06. |
| #25 | Audit-reason textarea; vùng nhập lớn. | Textarea disabled; no source-backed type/required/max-length/default. #71 local candidate chỉ nhận `status`; #72 không nhận body. | Disabled in prototype; no typing event. Keep disabled unless field/audit API and validation are approved; EV-06. |
| #26 | “Vô hiệu hóa” badge; trong góc dưới phải textarea. | Static label; không có relation tới permission API hoặc current session. | Visible; prototype state only; EV-06. |
| #27 | System-policy warning icon; trái warning panel. | Decorative shield icon; no policy API source. | Visible; no event. |
| #28 | Policy warning title/body; warning panel dưới textarea. | Claims active data-integrity policy, enrollment/result protection, and temporary disablement are static. #72 local source does not enforce these dependencies. | Visible; copy requires owner source/policy; EV-06. |
| #29 | “Quay lại an toàn” action; dưới panel trái. | Anchor `/admin/users`; does not retain selected user in current HTML. | Visible/enabled-looking, but router/handoff is unwired; EV-05. No mutation. |
| #30 | “Xác nhận thực hiện” button; dưới panel phải. | Disabled button; no form submit/handler/request. | Disabled; only enable after selection, user/session state, authorization and policy checks are approved; EV-03/EV-04. |
| #31 | API handlers / “Enforced Gate: Active” footer claim; right side of card footer. | Static labels; not API telemetry or actual enforced-gate state. #69/#71/#72 endpoints are local source-backed, but Study Web does not call them. | Visible, unverified; EV-06. |
| #32 | Audit code `AD-05` / ISO/IEC 27001 compliance footer claim; left card footer. | Static audit/compliance assertion; no audit record, auditor, control evidence or compliance API in this screen flow. | Visible, unverified; EV-06. |
| #33 | Copyright/system footer text; page bottom left. | Static text and year. | Visible; no action/data source. |
| #34 | Privacy/RBAC/support footer links; page bottom right. | Anchor placeholders `#`; destination/content not defined in current source. | Visible; no verified navigation; EV-06. |

## 4. Conditional UI & state variations
- States theo inventory: no-selection/loading/ready-read-only/mode-selected/submitting/unauthenticated/forbidden/not-found/validation-error/success/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/AD-05.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
