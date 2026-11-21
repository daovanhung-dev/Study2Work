# Bộ tài liệu ghép màn hình Study (`screen_stitch`)

Các thư mục được phân theo nhóm vai trò trong [`../list_screen.md`](../list_screen.md).
Tên mỗi màn hình dùng dạng `<ID>_<slug-ASCII>`; phần tên ngắn lấy từ tiêu đề trong
danh mục, viết thường, bỏ dấu tiếng Việt và thay dấu câu bằng dấu gạch ngang.
Ví dụ: `ST-13_gioi-thieu-bai-kiem-tra`. Mỗi thư mục màn hình chứa ảnh nguồn
`screen.png` và HTML nguồn `code.html`. Khi xử lý một màn hình, đặt ảnh có chú
thích `screen_annotated.png`, tài liệu `<ID>.md`, kế hoạch `<ID>_PLAN.md` và
bản đồ số `<ID>_markers.json` ngay trong cùng thư mục. Lập kế hoạch trước khi
soạn DD hoặc tạo ảnh chú thích.

Nếu một mã có nhiều biến thể thư mục, mỗi biến thể nguồn hiện có cần ảnh chú
thích và bản đồ số riêng. Chỉ giữ một DD và một kế hoạch cho mã đó, trong thư
mục của biến thể mà DD mô tả; không tự suy đoán biến thể nào mới hơn.

| Thư mục | Nhóm trong danh mục | Mã | Số mã |
|---|---|---|---:|
| `01_shared_auth_system/` | Chia sẻ / Xác thực / Hệ thống | SH-01–SH-07 | 7 |
| `02_guest_discovery/` | Khách / Khám phá | GS-01–GS-07 | 7 |
| `03_student/` | Học viên | ST-01–ST-26 | 26 |
| `04_mentor/` | Người hướng dẫn | ME-01–ME-18 | 18 |
| `05_admin/` | Quản trị | AD-01–AD-25 | 25 |
| `90_reference/` | Tài liệu tham chiếu, không phải mã màn hình | — | — |

`01_shared_auth_system/` hiện có thư mục
`SH-01_trang-gioi-thieu-study__variant-1/`. Các worklog cũ và phiên bản README
trước đây từng liệt kê biến thể thứ hai, nhưng kiểm tra cây hiện tại không tìm
thấy thư mục đó. Không tái tạo tài sản thiếu hoặc suy đoán nội dung của nó.

`90_reference/study2work-lms-design-system/DESIGN.md` là tài liệu tham khảo
hệ thống thiết kế, không nằm trong danh sách 83 mã màn hình.

Đây là các tài sản mẫu và tài liệu thiết kế; sự hiện diện ở đây không xác nhận
giao diện Study Web đã được triển khai hoặc hoạt động khi chạy.
