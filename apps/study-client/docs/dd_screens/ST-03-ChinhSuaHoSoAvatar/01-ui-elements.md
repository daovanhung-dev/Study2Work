# ST-03 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-03_markers.json](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/ST-03_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-03-EL-001` | `ST03-EL-01` | Study2Work LMS brand in header |
| #2 | `ST-03-EL-002` | `ST03-EL-02` | Trang chủ, Khóa học của tôi, Tiến độ, Thảo luận, Thông báo |
| #3 | `ST-03-EL-003` | `ST03-EL-03` | Static sample identity Nguyễn Văn A / Học viên and user icon |
| #4 | `ST-03-EL-004` | `ST03-EL-04` | Hệ thống > Hồ sơ cá nhân (ST-02) > Chỉnh sửa hồ sơ (ST-03) |
| #5 | `ST-03-EL-005` | `ST03-EL-05` | Blocked (Schema Conflict) status pill |
| #6 | `ST-03-EL-006` | `ST03-EL-06` | Technical gate title and explanatory copy for APIs #13 and #14 |
| #7 | `ST-03-EL-007` | `ST03-EL-07` | Quay lại Hồ sơ cá nhân (ST-02) |
| #8 | `ST-03-EL-008` | `ST03-EL-08` | Avatar placeholder, lock icon and gated/upload unavailable overlay |
| #9 | `ST-03-EL-009` | `ST03-EL-09` | Tài khoản Sinh viên and API #04 data-source caption |
| #10 | `ST-03-EL-010` | `ST03-EL-10` | Static no-file-support and API #13 halted diagnostic card |
| #11 | `ST-03-EL-011` | `ST03-EL-11` | Tải ảnh lên (Vô hiệu hóa) |
| #12 | `ST-03-EL-012` | `ST03-EL-12` | Chế độ an toàn ST-03 card |
| #13 | `ST-03-EL-013` | `ST03-EL-13` | Thông tin hồ sơ học viên card, description and form container |
| #14 | `ST-03-EL-014` | `ST03-EL-14` | Required full-name input, help text and API #04 badge |
| #15 | `ST-03-EL-015` | `ST03-EL-15` | Read-only email field, lock icon and help text |
| #16 | `ST-03-EL-016` | `ST03-EL-16` | Disabled phone field, nullable-conflict badge and warning |
| #17 | `ST-03-EL-017` | `ST03-EL-17` | Disabled bio textarea, missing-schema badge and warning |
| #18 | `ST-03-EL-018` | `ST03-EL-18` | Quay lại Hồ sơ cá nhân (ST-02) below fields |
| #19 | `ST-03-EL-019` | `ST03-EL-19` | Lưu thay đổi (Disabled) |
| #20 | `ST-03-EL-020` | `ST03-EL-20` | Static note that API #14 body mapping is unresolved |
| #21 | `ST-03-EL-021` | `ST03-EL-21` | Developer Hand-off Diagnostic title and proposed route context |
| #22 | `ST-03-EL-022` | `ST03-EL-22` | Asset mismatch / multipart and DDL diagnostic text |
| #23 | `ST-03-EL-023` | `ST03-EL-23` | Missing bio / nullable phone diagnostic text |
| #24 | `ST-03-EL-024` | `ST03-EL-24` | Wait for DDL and API contract alignment before release |
| #25 | `ST-03-EL-025` | `ST03-EL-25` | Footer copyright and static WCAG 2.1 AA badge |
| #26 | `ST-03-EL-026` | `ST03-EL-26` | Terms, privacy policy and help anchors |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả element

Marker trên ảnh và hàng tương ứng trong bảng dùng chung số 1–26. Kích thước/vị trí được ghi tương đối theo ảnh nguồn. Các trạng thái “mong đợi” dưới đây không khẳng định đã được triển khai. CSS HTML có hover cho các link và focus style cho input fullname; phone/bio/upload/save là disabled, email readonly. Không có bằng chứng runtime về keyboard focus, loading hay error state.

| Element ID | Tên, loại, vị trí và mục đích | Thuộc tính, nguồn dữ liệu, hiển thị/trạng thái | Sự kiện |
|---|---|---|---|
| #1 ST03-EL-01 | Brand/logo Study2Work LMS; anchor ở đầu header. | Icon school và nhãn là nội dung tĩnh; href="#" và data-path="trang-chu"; không có route binding. Visible trong ảnh. | ST03-EV-08 |
| #2 ST03-EL-02 | Nhóm primary navigation; header giữa logo và account. | Năm anchor: Trang chủ, Khóa học của tôi, Tiến độ, Thảo luận, Thông báo; href="#"; không có selected-route state do router. Responsive class ẩn nav ở màn hẹp; hành vi menu thay thế không có. | ST03-EV-08 |
| #3 ST03-EL-03 | Account identity/avatar ở góc phải header. | Mẫu tĩnh “Nguyễn Văn A”, role “Học viên” và icon person; không lấy #04/session. Không hiển thị dữ liệu người dùng thật. | Không có event xác minh. |
| #4 ST03-EL-04 | Breadcrumb từ Hệ thống → ST-02 → ST-03. | Text tĩnh trong HTML; không có destination binding đáng tin cậy; không dùng breadcrumb làm route guard. | Không có handler. |
| #5 ST03-EL-05 | Pill Gate G-03 ở phía phải breadcrumb. | Text “Blocked (Schema Conflict)” và chấm đỏ là static copy. Không được gắn với HTTP code/feature flag. | Không có event. |
| #6 ST03-EL-06 | Warning banner G-03: icon khóa, title và mô tả. | Nêu chức năng avatar/lưu hồ sơ tạm dừng, upload/save bị vô hiệu hóa. Static design state, không phải lỗi từ server. | Không có event. |
| #7 ST03-EL-07 | Link quay về ST-02 ở trong banner. | Anchor href="#" và data-path="ho-so-ca-nhan"; không có navigation hoặc transfer state hiện tại. | ST03-EV-07 |
| #8 ST03-EL-08 | Avatar preview với lock overlay ở card trái. | Hình placeholder/lock và chữ GATED / UPLOAD UNAVAILABLE; không phải avatar URL từ #04. Không có file/preview state. | Hiển thị tĩnh; upload riêng ở #11. |
| #9 ST03-EL-09 | Nhãn “Tài khoản Sinh viên” và nguồn dữ liệu. | Caption nói API #04 GET /users/me (Runtime Only); chỉ là nhãn mockup. Không chứa giá trị response thật. | Không có event. |
| #10 ST03-EL-10 | Card Avatar Asset Pipeline diagnostic. | Copy “Không hỗ trợ chọn tệp”, “API #13 Halted”, mismatch binary/URL; là diagnostic tĩnh cũ. Backend #13 có source đăng ký, nhưng UI caller/storage live chưa xác minh. | Không có event. |
| #11 ST03-EL-11 | Button tải ảnh lên bên dưới preview. | Native button disabled, chữ “Tải ảnh lên (Vô hiệu hóa)”; không có input type=file, MIME/size UI validation hoặc file selection. Disabled means click không khởi chạy API. | ST03-EV-05 |
| #12 ST03-EL-12 | Card “Chế độ an toàn ST-03”. | Static copy nói dùng cấu trúc runtime/JWT Bearer, không tạo danh tính giả. Không chứng minh page đọc JWT hoặc có runtime safety behavior. | Không có event. |
| #13 ST03-EL-13 | Surface form hồ sơ; card phải gồm heading và mô tả. | Nội dung tĩnh “Thông tin hồ sơ học viên”; mô tả nói các trường xung đột schema đã khóa an toàn. Design không có loading/loaded/error variation. | Nhận nội dung khi ST03-EV-01; không có event riêng. |
| #14 ST03-EL-14 | Input họ và tên, help text và badge API #04. | input type=text, id/name fullname, label có dấu *, placeholder; không có HTML required/maxlength; không có giá trị prefill. API #14 server trim, yêu cầu không rỗng, tối đa 150 ký tự. Giá trị field/API mapping chưa được nối. | ST03-EV-02 |
| #15 ST03-EL-15 | Email field readonly, khóa và help text. | input type=email, readonly, placeholder mẫu name@student.study2work.edu.vn; dữ liệu dự kiến từ data.email API #04 nhưng chưa map. Read-only không được sửa từ UI này. | ST03-EV-03 |
| #16 ST03-EL-16 | Phone field và nullable-conflict warning. | input type=text, id/name phone, disabled, không có giá trị mặc định; nội dung báo quy tắc lưu chưa khóa. API #04 trả phone nullable; API #14 hiện yêu cầu field phone có mặt nhưng chấp nhận null, trim chuỗi và đổi blank thành null, tối đa 20 ký tự. | ST03-EV-04 |
| #17 ST03-EL-17 | Bio textarea và missing-schema warning. | textarea, id/name bio, rows=3, disabled; placeholder nói thiếu cột DB. API #04 response không có bio; API #14 request model extra-ignore nên hiện bỏ qua bio. Không có độ dài/validation/persistence contract. | ST03-EV-04 |
| #18 ST03-EL-18 | Link quay về ST-02 ở cuối form. | Anchor href="#" và data-path="ho-so-ca-nhan"; không lưu/chuyển dữ liệu form. Expected destination theo inventory là /student/profile. | ST03-EV-07 |
| #19 ST03-EL-19 | Button “Lưu thay đổi”. | Native type=button, disabled, aria-disabled=true; không submit form, không có handler, không gọi #14. Disabled appearance khớp Gate prototype. | ST03-EV-06 |
| #20 ST03-EL-20 | Note API #14 dưới action bar. | Static text nói chưa chốt body mapping và nút lưu bị khóa cứng. Đây là note thiết kế, không phải server validation/error response. | Không có event. |
| #21 ST03-EL-21 | Developer Hand-off Diagnostic heading và route context. | Static heading, Technical Gate G-03 badge và route text /student/profile/edit; route vẫn là đề xuất. | Không có event. |
| #22 ST03-EL-22 | Diagnostic card API #13. | Static copy tuyên bố frontend cần multipart/CDN và DDL không có metadata handler. Không khớp current source API #13 JSON Data URL → Object Storage → AvatarUploadResult; giữ nguyên như discrepancy của mockup. | Không có event. |
| #23 ST03-EL-23 | Diagnostic card API #14/DDL. | Static copy đề cập thiếu bio và phone nullable/thiếu validation. Thiếu bio đúng với DDL/source; phone nullable đúng DDL nhưng current API #14 có normalize/giới hạn max 20, dù chưa có phone format rule. | Không có event. |
| #24 ST03-EL-24 | Proposed next-step notice. | Static đề xuất chờ migration DDL v1.4 và chuẩn hóa API trước release. Đây là proposal trên mockup, không xác nhận migration đã phê duyệt hoặc tồn tại. | Không có event. |
| #25 ST03-EL-25 | Footer copyright và WCAG badge. | Copyright 2025 và “WCAG 2.1 AA Compliant” là text tĩnh. Badge không thay thế audit accessibility. | Không có event. |
| #26 ST03-EL-26 | Footer navigation: điều khoản, chính sách riêng tư, trợ giúp. | Ba anchor href="#"; tài liệu đích/route chưa map. | ST03-EV-09 |

## 4. Conditional UI & state variations
- States theo inventory: dirty/uploading/saving/422/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-03_chinh-sua-ho-so-avatar/ST-03.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
