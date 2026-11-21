> ST-01–ST-26 đạt 100% theo rubric static DD-safe: UI, UX, state/logic và caller/API mapping đều có source-backed behavior. Các hành vi chưa được source/contract xác nhận vẫn hiển thị ở trạng thái bị khóa hoặc giới hạn. Điểm này không xác nhận browser, live API, database, migration hay deployment runtime.

> ME-01–ME-18 đạt 100% theo cùng rubric static DD-safe: mọi route, trạng thái UI, thao tác được source hỗ trợ và API caller đã được nối/kiểm tra theo source hiện tại; các hành vi thiếu contract tiếp tục bị giới hạn hoặc khóa. Điểm này không xác nhận browser đã đăng nhập, live API, database, migration hay deployment runtime. API #63 xác nhận xếp hàng không đồng nghĩa đã giao thông báo; trạng thái request không xác định sẽ khóa gửi lại trong phiên hiện tại.

> AD-01–AD-25 đạt 100% theo rubric static DD-safe cho UI, UX, state/logic và API mapping. Các thao tác/API chưa có contract hoặc source khả dụng được trình bày rõ là unavailable/disabled; điểm này không xác nhận product-level DD approval, browser đã đăng nhập, live API, database, migration hay deployment runtime. API #93 chỉ xác nhận queue acceptance, không xác nhận giao thông báo.

| STT | Mã Màn Hình | Tên Màn Hình | Trạng thái hoàn thiện |
|---:|---|---|---|
| 01 | SH-01 | Trang giới thiệu Study | 100% |
| 02 | SH-02 | Đăng nhập | 100% |
| 03 | SH-03 | Đăng ký học viên | 100% |
| 04 | SH-04 | Handoff xác thực email | 100% |
| 05 | SH-05 | Không đủ quyền / session hết hạn | 100% |
| 06 | SH-06 | Trang không tồn tại / tài nguyên không còn | 100% |
| 07 | SH-07 | Theo dõi tác vụ bất đồng bộ | 100% |
| 08 | GS-01 | Danh sách khóa học | 100% |
| 09 | GS-02 | Tìm kiếm khóa học | 100% |
| 10 | GS-03 | Chi tiết khóa học | 100% |
| 11 | GS-04 | Đề cương khóa học | 100% |
| 12 | GS-05 | Đánh giá và thảo luận công khai | 100% |
| 13 | GS-06 | Tài nguyên khóa học | 100% |
| 14 | GS-07 | Xem/tải tài nguyên | 100% |
| 15 | ST-01 | Tổng quan học viên | 100% |
| 16 | ST-02 | Hồ sơ cá nhân | 100% |
| 17 | ST-03 | Chỉnh sửa hồ sơ/avatar | 100% |
| 18 | ST-04 | Kiểm tra ghi danh trước đăng ký | 100% |
| 19 | ST-05 | Kiểm tra đơn hàng / checkout | 100% |
| 20 | ST-06 | Thực hiện thanh toán | 100% |
| 21 | ST-07 | Kết quả đăng ký khóa học | 100% |
| 22 | ST-08 | Khóa học của tôi | 100% |
| 23 | ST-09 | Tổng quan khóa đang học | 100% |
| 24 | ST-10 | Kiểm tra quyền và bắt đầu học | 100% |
| 25 | ST-11 | Trình học bài/lesson player | 100% |
| 26 | ST-12 | Tài liệu kèm bài học | 100% |
| 27 | ST-13 | Giới thiệu bài kiểm tra | 100% |
| 28 | ST-14 | Làm bài kiểm tra | 100% |
| 29 | ST-15 | Xác nhận nộp bài kiểm tra | 100% |
| 30 | ST-16 | Kết quả bài kiểm tra | 100% |
| 31 | ST-17 | Chi tiết bài tập | 100% |
| 32 | ST-18 | Soạn và nộp bài tập | 100% |
| 33 | ST-19 | Bài đã nộp và phản hồi | 100% |
| 34 | ST-20 | Tổng quan tiến độ | 100% |
| 35 | ST-21 | Tiến độ theo khóa học | 100% |
| 36 | ST-22 | Thành tích và chứng nhận | 100% |
| 37 | ST-23 | Danh sách thảo luận | 100% |
| 38 | ST-24 | Tạo câu hỏi / chủ đề | 100% |
| 39 | ST-25 | Chi tiết thread và phản hồi | 100% |
| 40 | ST-26 | Thông báo học viên | 100% |
| 41 | ME-01 | Dashboard mentor | 100% |
| 42 | ME-02 | Các khóa học phụ trách | 100% |
| 43 | ME-03 | Workspace khóa học của mentor | 100% |
| 44 | ME-04 | Tải lên và tạo bài giảng | 100% |
| 45 | ME-05 | Xem bài giảng mentor | 100% |
| 46 | ME-06 | Cây nội dung khóa học | 100% |
| 47 | ME-07 | Tạo/chỉnh sửa nội dung | 100% |
| 48 | ME-08 | Xuất bản/xóa nội dung | 100% |
| 49 | ME-09 | Danh sách bài cần chấm | 100% |
| 50 | ME-10 | Chấm điểm và phản hồi | 100% |
| 51 | ME-11 | Hộp thư hỗ trợ học viên | 100% |
| 52 | ME-12 | Trao đổi và đóng yêu cầu | 100% |
| 53 | ME-13 | Chọn người nhận thông báo | 100% |
| 54 | ME-14 | Soạn thông báo mentor | 100% |
| 55 | ME-15 | Theo dõi gửi thông báo | 100% |
| 56 | ME-16 | Tiến độ toàn khóa học | 100% |
| 57 | ME-17 | Tiến độ từng học viên | 100% |
| 58 | ME-18 | Analytics khóa học | 100% |
| 59 | AD-01 | Dashboard quản trị | 100% |
| 60 | AD-02 | Danh sách người dùng | 100% |
| 61 | AD-03 | Chi tiết người dùng | 100% |
| 62 | AD-04 | Chỉnh sửa người dùng | 100% |
| 63 | AD-05 | Khóa/mở khóa/xóa tài khoản | 100% |
| 64 | AD-06 | Danh sách khóa học quản trị | 100% |
| 65 | AD-07 | Chi tiết khóa học quản trị | 100% |
| 66 | AD-08 | Chỉnh sửa khóa học | 100% |
| 67 | AD-09 | Thay đổi trạng thái/xóa khóa | 100% |
| 68 | AD-10 | Hàng đợi kiểm duyệt nội dung | 100% |
| 69 | AD-11 | Duyệt/từ chối nội dung | 100% |
| 70 | AD-12 | Danh sách bài học quản trị | 100% |
| 71 | AD-13 | Chi tiết bài học quản trị | 100% |
| 72 | AD-14 | Sửa, đổi trạng thái, xóa bài học | 100% |
| 73 | AD-15 | Danh sách bài kiểm tra | 100% |
| 74 | AD-16 | Tạo/chỉnh sửa quiz | 100% |
| 75 | AD-17 | Thống kê bài kiểm tra | 100% |
| 76 | AD-18 | Xác nhận xóa bài kiểm tra | 100% |
| 77 | AD-19 | Danh sách thông báo quản trị | 100% |
| 78 | AD-20 | Soạn/gửi thông báo hệ thống | 100% |
| 79 | AD-21 | Sửa/kiểm soát/đo trạng thái thông báo | 100% |
| 80 | AD-22 | Danh sách thảo luận bị báo cáo | 100% |
| 81 | AD-23 | Điều tra/kiểm duyệt thảo luận | 100% |
| 82 | AD-24 | Báo cáo tác động cộng đồng | 100% |
| 83 | AD-25 | Xuất báo cáo và theo dõi tiến trình | 100% |
