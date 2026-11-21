# SH-06 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [SH-06_markers.json](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/SH-06_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `SH-06-EL-001` | `SH06-EL-01` | Header brand link |
| #2 | `SH-06-EL-002` | `SH06-EL-02` | Primary navigation group |
| #3 | `SH-06-EL-003` | `SH06-EL-03` | Login link |
| #4 | `SH-06-EL-004` | `SH06-EL-04` | Register CTA |
| #5 | `SH-06-EL-005` | `SH06-EL-05` | Decorative account icon placeholder |
| #6 | `SH-06-EL-006` | `SH06-EL-06` | HTTP 404 status badge |
| #7 | `SH-06-EL-007` | `SH06-EL-07` | 404 status illustration |
| #8 | `SH-06-EL-008` | `SH06-EL-08` | Error heading |
| #9 | `SH-06-EL-009` | `SH06-EL-09` | Error description |
| #10 | `SH-06-EL-010` | `SH06-EL-10` | Primary return-to-catalog CTA |
| #11 | `SH-06-EL-011` | `SH06-EL-11` | Secondary home CTA |
| #12 | `SH-06-EL-012` | `SH06-EL-12` | Safe Scope notice card |
| #13 | `SH-06-EL-013` | `SH06-EL-13` | Recommended-courses heading |
| #14 | `SH-06-EL-014` | `SH06-EL-14` | See all courses link |
| #15 | `SH-06-EL-015` | `SH06-EL-15` | Course card 1 |
| #16 | `SH-06-EL-016` | `SH06-EL-16` | Course card 2 |
| #17 | `SH-06-EL-017` | `SH06-EL-17` | Course card 3 |
| #18 | `SH-06-EL-018` | `SH06-EL-18` | Help prompt strip |
| #19 | `SH-06-EL-019` | `SH06-EL-19` | Contact support link |
| #20 | `SH-06-EL-020` | `SH06-EL-20` | Footer brand and platform descriptor |
| #21 | `SH-06-EL-021` | `SH06-EL-21` | Footer navigation group |
| #22 | `SH-06-EL-022` | `SH06-EL-22` | Copyright text |

## 3. Đặc tả từng element

### Trích từ DD nguồn: 3. Ảnh và marker

- [Ảnh nguồn không chú thích](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/screen.png) là ảnh 1600×1425; được giữ nguyên.
- [Ảnh chú thích](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/screen_annotated.png) đánh số 22 element nhìn thấy theo thứ tự #1–#22; card gợi ý mock cũng được đánh dấu để không bị hiểu là dữ liệu thật.
- [JSON marker](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/SH-06_markers.json) lưu target/center theo pixel gốc góc trái trên.
- [HTML prototype](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/code.html) là nguồn bố cục/copy mẫu, không phải Study Web runtime.

### Trích từ DD nguồn: 4. Đặc tả element

Kích thước/vị trí mô tả ảnh nguồn. Target implementation tuân thủ [Study Web design guide](../../../../../.agents/web-study/design.md): font Inter nếu có sẵn hoặc system, không tải remote font, content width khoảng 1120px, responsive reflow, focus-visible và control cao tối thiểu 44px. Element dưới đây có mặt trong ảnh mặc định; trạng thái hover/focus/loading/error chỉ áp dụng khi tương tác hoặc khi state đổi.

| # / Element ID | Tên, loại, vị trí | Thuộc tính, dữ liệu, validation | Hiển thị / trạng thái | Sự kiện |
|---|---|---|---|---|
| **#1 `SH06-EL-01`** | Brand/logo header, `a`; góc trên trái. | Icon `school` và chữ “Study2Work LMS”; `data-path="trang-chu"`, `href="#"`; không có payload. | Default visible; hover color trong prototype. Target route `/` chưa được router xác nhận. | `SH06-EV-04`. |
| **#2 `SH06-EL-02`** | Primary nav group, `nav`; header giữa-trái. | Ba anchors “Trang chủ”, “Khóa học”, “Tìm kiếm”; data-path lần lượt `trang-chu`, `khoa-hoc`, `tim-kiem`; href đều `#`. Route proposals tương ứng `/`, `/courses`, `/courses/search?q=` theo inventory; query mặc định chưa xác nhận. | Group hiện ở desktop (`hidden md:flex`); ở viewport nhỏ source ẩn nav mà không có menu thay thế. Cần xác nhận responsive navigation. | `SH06-EV-05`. |
| **#3 `SH06-EL-03`** | Link “Đăng nhập”, `a`; header phải. | data-path `dang-nhap`, href `#`; route proposal `/login`; không truyền 404 resource ID. | Default visible; hover style có, focus-visible style chưa được nêu rõ trong HTML. | `SH06-EV-05`. |
| **#4 `SH06-EL-04`** | CTA “Đăng ký”, `a`; cạnh link đăng nhập. | data-path `dang-ky`, href `#`; route proposal `/register`; không gửi form/API. | Default/hover; CTA cao theo padding nhưng target layout phải đo lại ở mọi breakpoint. | `SH06-EV-05`. |
| **#5 `SH06-EL-05`** | Icon account/person, `div` + icon; header góc phải. | Vòng tròn 32×32px, không `button`, `a`, `role`, accessible name hoặc click handler. Không có user data. | Trang trí hiện tại; không mô tả là profile action. Nếu muốn interactive cần Product/UI requirement, semantics và route riêng. | Không có event trong source. |
| **#6 `SH06-EL-06`** | HTTP status pill, `div`; trên hero. | Copy “Mã lỗi hệ thống · HTTP 404 • Resource Not Found”; chấm màu primary. Source cố định, không bind status/API body. | Prototype luôn visible. Target text có thể dùng status chung cho route/resource 404; không gọi là “business code”. | State đổi theo `SH06-EV-01` / `SH06-EV-02`. |
| **#7 `SH06-EL-07`** | Số 404 + divider, `h1` và trang trí; trung tâm hero. | H1 số `404`; số 0 màu primary; divider 96×4px. Không có data input. | Route/resource 404; divider decorative. Screen reader đọc H1 một lần; divider ẩn khỏi accessibility tree. | State đổi theo EV-01/02. |
| **#8 `SH06-EL-08`** | Heading, `h2`; dưới số 404. | Copy hiện tại “Không tìm thấy trang hoặc tài nguyên yêu cầu”. Nguồn tĩnh; không nhúng URL/ID. | Visible trong hai 404 states; không dùng cho 403/500. | EV-01/02. |
| **#9 `SH06-EL-09`** | Description, `p`; dưới heading. | Copy hiện tại cho biết resource không tồn tại/đã dời, đề nghị kiểm tra đường dẫn hoặc về danh sách khóa học. “Đã dời” chưa có backend evidence; target copy nên chỉ nói “không khả dụng” nếu không có nguyên nhân được xác nhận. | Visible route/resource 404; wrap theo viewport, không cắt text. | EV-01/02. |
| **#10 `SH06-EL-10`** | Primary CTA, `a`; dưới description. | Label “Về danh sách khóa học (GS-01)”; `data-path="khoa-hoc"`, href `#`; target proposal `/courses`. No path/query/body. | Default/hover/focus; min-height 44px trong HTML; target focus-visible rõ. | `SH06-EV-03`. |
| **#11 `SH06-EL-11`** | Secondary CTA, `a`; cạnh primary CTA. | Label “Về trang chủ (SH-01)”; `data-path="trang-chu"`, href `#`; target proposal `/`. | Default/hover/focus; min-height 44px trong HTML. | `SH06-EV-04`. |
| **#12 `SH06-EL-12`** | Safe Scope notice, `card/notice`; dưới CTA. | Icon verified_user; title “Quy chuẩn dữ liệu an toàn • Safe Scope”; badge “Standard Spec”; paragraph nói tài nguyên nội bộ/draft/course không hoạt động bị ẩn. API #08 xác minh riêng việc chỉ query PUBLISHED và cùng 404 cho missing/unpublished; nhãn Standard Spec chưa có nguồn. | Visible trong prototype; target chỉ giữ thông điệp chung đã duyệt. Không tuyên bố các resource khác cũng có policy nếu chưa source-backed. | Không có click event; content theo EV-01/02. |
| **#13 `SH06-EL-13`** | Header section gợi ý, `section heading + p`; nửa dưới trang. | Title “Khám phá các khóa học khả dụng”; subtitle có tuyên bố doanh nghiệp đối tác. Không có API/metric source trong SH-06 inventory. | Prototype visible. `BLOCKED`: Product/UX phải xác nhận giữ/bỏ, copy và data source; không chọn ẩn/bỏ thay họ. | `SH06-EV-08`. |
| **#14 `SH06-EL-14`** | “Xem tất cả” link, `a`; phải heading gợi ý. | `data-path="khoa-hoc"`, href `#`; proposal `/courses`. Ẩn ở viewport nhỏ (`hidden sm:inline-flex`); primary CTA #10 vẫn có. | Visible từ breakpoint `sm`; hover underline. Cần focus-visible và route xác nhận. | `SH06-EV-06`. |
| **#15 `SH06-EL-15`** | Course card 1, linked card `a`; cột trái. | Mock values: Công nghệ phần mềm; 12 tuần; “Fullstack Web Developer”; description Node.js/React/Cloud/Agile; “1.420 học viên”; Chi tiết. Không có course ID, API field hoặc formatter source. | Prototype visible. `BLOCKED`: không render/click mock; Product/UX phải chốt section/data contract trước implementation. | `SH06-EV-07` / EV-08. |
| **#16 `SH06-EL-16`** | Course card 2, linked card `a`; cột giữa. | Mock values: Phân tích dữ liệu; 8 tuần; “Data Analyst Foundation”; description SQL/PowerBI/visualization; “980 học viên”; Chi tiết. Không có ID/API field. | Như #15; card text bị giới hạn dòng trong prototype. | `SH06-EV-07` / EV-08. |
| **#17 `SH06-EL-17`** | Course card 3, linked card `a`; cột phải. | Mock values: Quản trị dự án; 6 tuần; “Product Owner & Scrum”; description acceptance criteria/backlog; “750 học viên”; Chi tiết. Không có ID/API field. | Như #15; không coi số học viên hay duration là thật. | `SH06-EV-07` / EV-08. |
| **#18 `SH06-EL-18`** | Help strip icon + prompt, `aside/group`; dưới grid. | Icon `help_outline`; text hỏi người dùng cần trợ giúp tài khoản/môn học đã đăng ký. Không có API, role hoặc email trong source. | Prototype visible; icon trang trí với accessible label từ text cạnh. Target copy không khẳng định có help workflow nếu chưa có channel. | Không có action riêng; liên quan EV-09. |
| **#19 `SH06-EL-19`** | Contact link, `a`; phải help strip. | Label “Liên hệ ban giáo vụ Study2Work”, icon support_agent; href `#`, data-path `trang-chu`. Không có address/contact ID/channel. | Prototype visible. `BLOCKED`: Product phải xác nhận giữ/bỏ và route/channel; không biến anchor placeholder thành action. | `SH06-EV-09`. |
| **#20 `SH06-EL-20`** | Footer identity/descriptor, `div`; trái footer. | Icon menu_book, “Study2Work LMS”, descriptor “Nền tảng học tập & Định hướng nghề nghiệp”. Static; icon decorative. | Visible ở mọi viewport; footer reflow cần giữ thứ tự đọc. | Không có handler. |
| **#21 `SH06-EL-21`** | Footer nav group, `nav`; footer giữa. | Bốn anchors: Chương trình đào tạo (`data-path=khoa-hoc`), Tra cứu chứng chỉ (`tim-kiem`), Quy chế học vụ (`trang-chu`), Hỗ trợ học viên (`trang-chu`); toàn bộ href `#`. Chỉ route courses có thể đối chiếu inventory; chứng chỉ/quy chế/hỗ trợ chưa có route tương ứng. | Prototype visible, flex-wrap. `BLOCKED`: Product phải xác nhận giữ/bỏ và đích của từng link; không suy route từ `data-path`. | `SH06-EV-10`. |
| **#22 `SH06-EL-22`** | Copyright, `div`; phải footer. | Text `© 2025 Study2Work. All rights reserved.`; năm/source legal wording static. Không tự đổi năm thành current date nếu chưa có rule/template. | Visible; text wrap nếu cần ở mobile. | Không có handler. |

## 4. Conditional UI & state variations
- States theo inventory: route-404/resource-404
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/01_shared_auth_system/SH-06_trang-khong-ton-tai-tai-nguyen-khong-con/SH-06.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
