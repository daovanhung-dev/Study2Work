# AD-03 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [AD-03_markers.json](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/AD-03_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `AD-03-EL-001` | `not supplied in marker JSON` | Study2Work/LMS/Admin Portal brand |
| #2 | `AD-03-EL-002` | `not supplied in marker JSON` | Primary admin navigation group |
| #3 | `AD-03-EL-003` | `not supplied in marker JSON` | System Normal status pill |
| #4 | `AD-03-EL-004` | `not supplied in marker JSON` | Notifications icon |
| #5 | `AD-03-EL-005` | `not supplied in marker JSON` | Admin identity and avatar |
| #6 | `AD-03-EL-006` | `not supplied in marker JSON` | Global breadcrumb trail |
| #7 | `AD-03-EL-007` | `not supplied in marker JSON` | RBAC verification badge |
| #8 | `AD-03-EL-008` | `not supplied in marker JSON` | User management/detail breadcrumb |
| #9 | `AD-03-EL-009` | `not supplied in marker JSON` | API #69 data-sync badge |
| #10 | `AD-03-EL-010` | `not supplied in marker JSON` | Return to user list button (AD-02) |
| #11 | `AD-03-EL-011` | `not supplied in marker JSON` | Detail hero: icon, heading, subtitle and screen code |
| #12 | `AD-03-EL-012` | `not supplied in marker JSON` | Identity/contact card heading |
| #13 | `AD-03-EL-013` | `not supplied in marker JSON` | Not synchronized status badge |
| #14 | `AD-03-EL-014` | `not supplied in marker JSON` | Administrative actions card heading |
| #15 | `AD-03-EL-015` | `not supplied in marker JSON` | Edit user button (AD-04), disabled |
| #16 | `AD-03-EL-016` | `not supplied in marker JSON` | No-selected-user information panel |
| #17 | `AD-03-EL-017` | `not supplied in marker JSON` | Lock/status button (AD-05), disabled |
| #18 | `AD-03-EL-018` | `not supplied in marker JSON` | Account action advisory |
| #19 | `AD-03-EL-019` | `not supplied in marker JSON` | Full-name row |
| #20 | `AD-03-EL-020` | `not supplied in marker JSON` | Email row |
| #21 | `AD-03-EL-021` | `not supplied in marker JSON` | Login/role audit heading and record count |
| #22 | `AD-03-EL-022` | `not supplied in marker JSON` | User-ID row |
| #23 | `AD-03-EL-023` | `not supplied in marker JSON` | Audit empty-state panel |
| #24 | `AD-03-EL-024` | `not supplied in marker JSON` | Phone row |
| #25 | `AD-03-EL-025` | `not supplied in marker JSON` | System-role row |
| #26 | `AD-03-EL-026` | `not supplied in marker JSON` | Account-status row |
| #27 | `AD-03-EL-027` | `not supplied in marker JSON` | Security protocol and retention note |
| #28 | `AD-03-EL-028` | `not supplied in marker JSON` | API endpoint and response footnote |
| #29 | `AD-03-EL-029` | `not supplied in marker JSON` | Privacy/compliance banner |
| #30 | `AD-03-EL-030` | `not supplied in marker JSON` | RBAC Strict Audit Active badge |
| #31 | `AD-03-EL-031` | `not supplied in marker JSON` | Copyright and system footer text |
| #32 | `AD-03-EL-032` | `not supplied in marker JSON` | Privacy/RBAC/support footer links |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Marker ID phải trùng `AD-03_markers.json` và `screen_annotated.png`. Giá trị `--`, `TRỐNG`, `CHƯA GÁN` trong prototype là placeholder tĩnh, không phải default từ API.

| Element ID | Tên / loại / vị trí | Thuộc tính, nguồn dữ liệu và validation | Hiển thị / trạng thái | Sự kiện |
|---:|---|---|---|---|
| #1 | Brand Study2Work/LMS/Admin Portal; brand block, header trái. | Text/logo tĩnh từ prototype; không có API field. | Visible; shell hiện tại chỉ trong ảnh. | Không có handler/route xác nhận. |
| #2 | Primary admin navigation; nhóm 5 nav links. | Label tĩnh; `href="#"`, `data-path` không tạo router. | Visible ở kích thước desktop trong ảnh; responsive behavior chưa có implementation. | EV-06; đích mỗi route chưa được xác nhận. |
| #3 | “SYSTEM NORMAL”; status pill header. | Static copy; không có health API/source trong #69. | Visible trong prototype; không được coi là health state. | Không có. |
| #4 | Notifications; icon/button header. | Không có notification count, link hoặc API mapping. | Visible; trạng thái tĩnh. | EV-06; handler chưa có. |
| #5 | Admin identity/avatar; account block header phải. | Tên/role/avatar hard-coded trong prototype; không lấy từ #69 vì `data` là user được xem. | Visible; session/self-profile source ngoài phạm vi và chưa được xác nhận. | EV-06 nếu route profile được định nghĩa. |
| #6 | Breadcrumb hệ thống; navigation trail. | Các nhãn tĩnh; HTML không có route mapping. | Visible. | EV-06; destination chưa được định nghĩa. |
| #7 | “Chuẩn xác thực RBAC”; assurance badge. | Static assertion; API #69 chỉ chứng minh guard local đang kiểm tra claim `ADMIN`, không chứng minh chính sách toàn hệ thống. | Visible nhưng chưa được chứng thực. | Không có; không gắn với API response. |
| #8 | Breadcrumb quản lý user/danh sách/detail. | “Danh sách tài khoản” dùng fragment; “Chi tiết tài khoản” là label. | Visible; không thay route param. | EV-02 cho phần về AD-02; cần route thật. |
| #9 | “API #69 • Chế độ đồng bộ dữ liệu”; data status badge. | Text tĩnh; #69 là GET detail, không khai báo sync operation. | Visible nhưng không phải response state. | Không có API/event được xác nhận. |
| #10 | “Quay lại danh sách người dùng (AD-02)”; back button. | Anchor fragment `#danh-sach-nguoi-dung-ad-02`; không có query-state handoff hiện hữu. | Visible/enabled trong screenshot; chưa có navigation behavior. | EV-02; đích đề xuất `/admin/users`. |
| #11 | Detail hero: icon, title, subtitle, code AD-03. | Title/subtitle/code tĩnh; subtitle nhắc lịch sử hoạt động nhưng #69 không trả history. | Visible. | Không có riêng; EV-01 khởi tạo page data, subtitle không phải data source. |
| #12 | Card “Thông tin định danh và liên hệ”; section heading. | Static label/icon. | Visible. | Không có. |
| #13 | “CHƯA ĐỒNG BỘ”; identity card badge. | Static state không thuộc #69. | Prototype empty state; không thay cho `loading`, 404 hoặc error. | Không có. |
| #14 | Card “Hành động quản trị”; section heading. | Static label/icon. | Visible. | Không có. |
| #15 | “Chỉnh sửa thông tin (AD-04)”; disabled button. | `type=button`, `disabled`, `aria-disabled=true`; không gọi #70. | Disabled; phải giữ disabled đến khi quyền/route/API #70/body AD-04 được chốt. | EV-03; hiện không thể kích hoạt. |
| #16 | No-selected-user information panel; empty/info alert. | Copy nói chưa chọn user hoặc đang chờ server xác thực. Không có field/API biểu diễn “đồng bộ đang chờ”; #69 success không trả null profile. | Static visible. Chỉ placeholder trong prototype; không dùng làm 204/empty response handling. | EV-01 quyết định state thật; panel copy cần sửa khi wire. |
| #17 | “Khóa hoặc thay đổi trạng thái (AD-05)”; disabled button. | `type=button`, `disabled`, `aria-disabled=true`; không gọi #71/#72. | Disabled cho tới khi policy/route/API contract AD-05 được duyệt. | EV-04; hiện không thể kích hoạt. |
| #18 | Account action advisory; notice card. | Static rule “chỉ kích hoạt khi định danh chính xác”; exact business precondition chưa có contract. | Visible; không phải validation result. | EV-03/EV-04 chỉ tham chiếu sau khi owner xác nhận. |
| #19 | Họ và tên; profile field row. | `data.full_name:string`, bắt buộc trên success. `--` và “TRỐNG” hiện là prototype placeholder. | Ready: text value; loading/error/null behavior ngoài API model chưa thiết kế ở frontend. | EV-01 mapping. |
| #20 | Địa chỉ Email; profile field row. | `data.email:string`, bắt buộc; PII. Không tự mask/hiện đầy đủ trước policy owner decision. | Prototype placeholder `--`/“TRỐNG”; visibility phụ thuộc permission/PII policy. | EV-01 mapping; policy blocker. |
| #21 | “Nhật ký đăng nhập & phân quyền” + record count; audit card heading. | Không có `audit_count` trong `UserProfile`; không có audit API/event source trong #69. `0 bản ghi` là static. | Không thể hiển thị như số liệu live; panel chưa có data contract. | EV-05; render dữ liệu bị chặn. |
| #22 | Mã định danh người dùng; profile field row. | `data.id:int`; route/API candidate signed-int64. Dùng ID đã chọn từ #68; không tự đổi sang UUID hoặc email. | Ready: hiển thị id theo format được duyệt; placeholder `--`/“KHÔNG CÓ ID” không phản ánh 200 response. | EV-01 mapping; EV-02/03/04 handoff. |
| #23 | Audit empty-state panel; illustration, title, body. | Copy “Không có lịch sử phiên” không thể suy ra từ profile API; cần audit query và empty semantics. | Static prototype state; không khẳng định user không có phiên. | EV-05; hiện không có request/source. |
| #24 | Số điện thoại; profile field row. | `data.phone:string|null`; PII. Nếu null, UI null copy chưa được chốt; không coi `--` là API default. | Prototype placeholder; visibility/masking phụ thuộc policy. | EV-01 mapping. |
| #25 | Vai trò hệ thống; profile field row. | `data.role:string`; enum members và label mapping chưa có. Không tự map alias hoặc viết hoa/thường. | Prototype hiển thị `--`/“CHƯA GÁN”; API không quy định default cho thành công. | EV-01 mapping. |
| #26 | Trạng thái tài khoản; profile field row. | `data.status:string`; enum/lifecycle và behavior khi suspended/deleted/anonymized chưa xác nhận. | Prototype placeholder `--`/“CHƯA XÁC ĐỊNH”; không phải response value. | EV-01 mapping; downstream lifecycle decision. |
| #27 | “Giao thức ghi vết bảo mật” và “Lưu trữ 180 ngày”; policy footnote. | Static text; API #69 không ghi audit event hoặc trả retention. | Không được trình bày là policy hiện hành khi chưa có owner/source. | EV-05; không có API được wire. |
| #28 | Endpoint/response footnote. | Prototype ghi `GET /api/v1/admin/users/:userId` và `204 / NULL_PAYLOAD`. Endpoint param naming khác API catalog; 204 conflicts with catalog/source. | Static developer-facing note; không dùng làm runtime telemetry. | EV-01 source is #69; sửa copy khi frontend được wire. |
| #29 | Privacy/compliance banner: icon, title, policy copy. | Static reference Nghị định 13/2023/NĐ-CP và tự động giám sát; API #69 không xác nhận tuân thủ hoặc monitoring. | Visible; legal/security copy needs owner approval. | Không có event/API. |
| #30 | “RBAC Strict Audit Active”; assurance badge footer banner. | Static claim; no audit event/health field in #69. | Visible nhưng chưa được chứng minh. | Không có event/API. |
| #31 | Copyright/system footer text. | Tĩnh: `© 2025 Study2Work LMS`, hệ thống quản trị. | Visible. | Không có. |
| #32 | Footer privacy/RBAC/support links; link group. | Ba `href="#"` placeholders; target pages không được định nghĩa trong AD-03. | Visible; không xác nhận destination hoặc quyền. | EV-06; không có handler/router hiện tại. |

## 4. Conditional UI & state variations
- States theo inventory: loading/ready/unauthenticated/forbidden/not-found/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/AD-03.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
