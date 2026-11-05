# Kế hoạch tổng — tài liệu thiết kế chi tiết màn hình Study

> **Trạng thái:** ĐANG_TIẾN_HÀNH. Kế hoạch này đi trước việc soạn từng màn hình và bao quát đủ 83 mã trong list_screen.md. Mỗi phiên chỉ soạn một mã màn hình.

## 1. Mục đích và nguồn thẩm quyền

- Tạo một tài liệu thiết kế chi tiết (DD) dạng Markdown cho mỗi mã màn hình duy nhất, gồm tổng quan, luồng tổng quát, thuộc tính trường/phần tử, mô tả sự kiện và xử lý dữ liệu chi tiết, trạng thái, màn hình liên kết, tiêu chí nghiệm thu và các điều kiện còn chặn.
- Giữ nguyên từng screen.png nguồn hiện có và tạo riêng screen_annotated.png trong cùng thư mục màn hình. Mỗi marker đánh số phải ánh xạ tới đúng phần tử tương ứng trong DD.
- Dùng `apps/study-client/docs/list_screen.md` làm danh mục chuẩn 83 mã màn hình, luồng và API; dùng `.agents/web-study/design.md` làm đích giao diện Study chuẩn. Bản làm việc hiện không có `apps/study-client/src`; đường dẫn và hành vi màn hình đề xuất không phải bằng chứng về hoạt động khi chạy.
- Chỉ dùng `90_reference/study2work-lms-design-system/DESIGN.md` làm tài liệu tham khảo hình ảnh. Bảng màu YAML (`#004ac6`, `#006c49`, `#784b00`) khác bảng màu trong văn xuôi (`#2563EB`, `#10B981`, `#F59E0B`); nút 40px/ô nhập 42px và khung 1440px cũng khác hướng dẫn Study (điều khiển 44px, vùng nội dung khoảng 1120–1200px). Ghi nhận sai khác; không âm thầm sửa mã màu chuẩn của Study.
- HTML/ảnh bản mẫu chỉ là đầu vào thiết kế. Tên mẫu, KPI, giá, điểm đánh giá, người hướng dẫn, lời chứng thực và logo đối tác viết cứng không phải dữ kiện có API; phải bỏ, ghi rõ là nội dung biên tập hoặc chặn tới khi có dữ liệu được duyệt trước khi tuyên bố triển khai.

## 2. Quy ước tài liệu đầu ra

| Tài liệu | Đường dẫn / quy tắc |
|---|---|
| Kế hoạch tổng và bảng theo dõi | dd_screens/PLAN.md (tệp này) |
| Tài liệu thiết kế chi tiết cho một màn hình | Cùng thư mục chứa ảnh nguồn của màn hình, tên `<ID>.md` |
| Kế hoạch riêng từng màn hình | Cùng thư mục với ảnh nguồn và tài liệu thiết kế, tên `<ID>_PLAN.md`; hoàn tất trước tài liệu/ảnh chú thích |
| Ảnh có đánh số | Cùng thư mục, tên `screen_annotated.png`; không bao giờ ghi đè `screen.png` |
| Bản đồ số chú thích | Cùng thư mục, tên `<ID>_markers.json`; mỗi số khớp với một phần tử trong tài liệu thiết kế |
| Bản xem sạch phát sinh | Nếu screen.png được cấp trống/không dùng được nhưng code.html tương ứng dựng được, lưu ảnh sạch thành screen_rendered.png; chú thích ảnh này và giữ nguyên screen.png |
| HTML gốc | Giữ nguyên code.html; đối chiếu với ảnh và ghi lại sai khác |
| Worklog | .agents/worklog/YYYY-MM-DD/<task-id>.md; ghi đúng tài liệu/mã nguồn đã đọc và kiểm tra tĩnh |

Nếu một mã có nhiều biến thể nguồn hiện tại, chỉ tạo một tài liệu thiết kế và một kế hoạch cho mã đó; đặt hai tài liệu trong thư mục của biến thể được mô tả. Mỗi biến thể đang có phải có ảnh chú thích và bản đồ số riêng. Không tự đoán biến thể nào mới hơn. Nếu README/tài liệu nhắc tới tài sản không tồn tại trong hệ thống tệp hiện tại, ghi nhận sai khác; không tự tạo lại.

## 3. Quy trình một màn hình mỗi phiên

1. Chọn một Screen ID trong bảng theo dõi; đọc đúng dòng trong list_screen.md, luồng liên quan, tác nhân/vai trò và mục chỉ mục API.
2. Kiểm tra PNG/HTML gốc (kể cả mọi biến thể hiện có). Ghi khác biệt giữa ảnh và HTML, không sửa hai tài sản nguồn. Nếu PNG trống nhưng HTML dựng được, tạo screen_rendered.png có tên rõ và chú thích trên bản dựng; giữ PNG trống làm bằng chứng nguồn.
3. Với mỗi API được tham chiếu, kiểm tra nối route, kiểm tra yêu cầu, tác động truy vấn/dịch vụ, ánh xạ phản hồi và mã kiểm thử liên quan. Không chạy kiểm thử nếu người dùng không yêu cầu. Gắn nhãn R, S, D, M, UX, UNWIRED, NOT_FOUND hoặc DECLARED_NOT_RUNNABLE theo bằng chứng.
4. Viết <ID>_PLAN.md trước: mục tiêu màn hình, tác nhân/điều kiện tiên quyết, sơ đồ khu vực, danh sách marker, phụ thuộc điều hướng/dữ liệu, các bước sự kiện, xử lý trạng thái/lỗi, điều kiện chặn và tiêu chí nghiệm thu.
5. Tạo ảnh đánh số và <ID>.md. DD cần có: tổng quan; luồng tổng quát; sơ đồ màn hình liên kết; thuộc tính phần tử/trường; từng sự kiện gồm thao tác kích hoạt, đầu vào, nguồn dữ liệu, API/phương thức, kiểm tra/thuật toán, thứ tự yêu cầu, ánh xạ phản hồi, lỗi/thử lại và màn hình tiếp; ma trận trạng thái; bảo mật/quyền riêng tư; thích ứng/tiếp cận; quyết định còn mở; tiêu chí nghiệm thu.
6. Kiểm tra tĩnh cho ID đó: PNG/HTML gốc còn tồn tại và giữ hash; bản dựng sạch có ghi nguồn gốc; ảnh đánh số đọc được và giữ đúng tỷ lệ khung hình; mỗi số marker ánh xạ đúng một phần tử DD, không thiếu/thừa marker; mọi yêu cầu khớp nguồn hiện tại hoặc có điều kiện chặn rõ; mọi liên kết tương đối mở được.
7. Cập nhật bảng theo dõi và worklog với đường dẫn tài liệu, lệnh/kết quả kiểm tra chính xác, phụ thuộc còn thiếu và màn hình đủ điều kiện tiếp theo. Không tuyên bố triển khai/chạy thật từ tài sản tĩnh.

## 4. Các đợt theo phụ thuộc và liên kết màn hình

Các đợt dưới đây giữ thứ tự phụ thuộc đề xuất tại §8.1 của list_screen.md. Chúng sắp xếp tài liệu, không cam kết triển khai. Cột màn hình liên kết trong bảng theo dõi sao chép liên kết điều hướng của danh mục.

| Luồng | Liên kết màn hình | Quy tắc xử lý / điều kiện |
|---|---|---|
| F01 — Xác thực | SH-03 → SH-04 → SH-02; SH-05 khi 401/403 | Đăng ký #01; gửi email #02 hiện chỉ là giả lập; đăng nhập #03; hồ sơ học viên #04. SH-04 không được tuyên bố email đã gửi/xác minh. |
| F02 — Khám phá | SH-01 → GS-01 / GS-02 → GS-03 → GS-04 / GS-05 / GS-06 → GS-07 | SH-01/GS-01 dùng #05/#06; GS-02 dùng #05/#07. Không gửi tham số category cho #06 trước khi giải quyết G-05. Chi tiết khóa học #08 trở đi chỉ có trong thiết kế. |
| F03 — Ghi danh/thanh toán | GS-03 → ST-04 → ST-05 → ST-06 → ST-07 → ST-08; SH-07 theo dõi tác vụ | Điều kiện danh tính, độ tin cậy thanh toán và quyền ghi danh G-01/G-04 chi phối mọi tuyên bố thành công. |
| F04 — Học khóa học | ST-08 → ST-09 → ST-10 → ST-11 → ST-12; ST-21 | Hợp đồng ghi danh khóa học và quyền truy cập/tiến độ bài học mới có trong thiết kế. |
| F05 — Bài kiểm tra | ST-13 → ST-14 → ST-15 → ST-16 | Chuyển trạng thái lượt làm, lưu câu trả lời, nộp bài, đồng hồ và kết quả phải chờ hợp đồng. |
| F06 — Bài tập | ST-17 → ST-18 → ST-19 | Tải tệp, chủ sở hữu bài nộp, thử lại và trạng thái chấm phải chờ hợp đồng. |
| F07 — Tiến độ/cộng đồng | ST-01/ST-20 → ST-21/ST-22; ST-23 → ST-24 → ST-25; ST-26 | API bảng điều khiển, tiến độ, thành tích, thảo luận và thông báo mới có trong thiết kế. |
| F08 — Nội dung người hướng dẫn | ME-01 → ME-02 → ME-03 → ME-04/ME-06 → ME-05/ME-07 → ME-08 | Quyền sở hữu và lược đồ lưu nội dung/API chưa được nối. |
| F09 — Chấm bài/hỗ trợ của người hướng dẫn | ME-01 → ME-09 → ME-10; ME-01 → ME-11 → ME-12 | API bài nộp và hỗ trợ mới có trong thiết kế. |
| F10 — Thông báo/phân tích người hướng dẫn | ME-13 → ME-14 → ME-15/SH-07; ME-16 → ME-17/ME-18 | Hợp đồng người nhận/ID tác vụ và chỉ số phân tích còn mở. |
| F11 — CRUD quản trị | AD-01 → AD-02..AD-09; AD-12..AD-18 | Hồ sơ vai trò quản trị và hợp đồng đọc/sửa chi tiết mới có trong thiết kế. |
| F12 — Kiểm duyệt quản trị | AD-10 → AD-11; AD-22 → AD-23 | Phê duyệt, lưu báo cáo và hợp đồng kiểm toán mới có trong thiết kế. |
| F13 — Thông báo/báo cáo quản trị | AD-19 → AD-20 → AD-21/SH-07; AD-01 → AD-24 → AD-25/SH-07 | HTTP 202 chỉ xác nhận đã tiếp nhận, không có nghĩa đã gửi/hoàn tất; tải báo cáo cần URL kết quả do máy chủ cấp. |

### Phạm vi các đợt

- **W0:** SH-01..03, SH-05..06, GS-01..02, ST-02. Tài liệu SH-04 ở nhánh bị chặn vì #02 chỉ là email giả lập; SH-07 thuộc W4 theo danh mục.
- **W1:** GS-03..07, ST-03, ST-08..12. Cần rà soát hợp đồng chi tiết/tài nguyên/hồ sơ và luồng học khóa.
- **W2:** ST-04..07 và ST-13..19. G-01/G-04 về ghi danh/thanh toán và G-09 về bài kiểm tra/bài tập quyết định mức sẵn sàng triển khai.
- **W3:** ST-20..26 và ME-01..18. Cần lược đồ tiến độ/cộng đồng và hợp đồng vai trò/nội dung/hỗ trợ người hướng dẫn.
- **W4:** AD-01..25 và SH-07. Cần RBAC quản trị, kiểm duyệt, thông báo/tác vụ và hợp đồng báo cáo/xuất tệp.
- **Mở rộng thứ tự:** ST-01 được xếp W3 cạnh API bảng điều khiển/tiến độ mà nó phụ thuộc; SH-04 có vị trí tài liệu W0 nhưng vẫn bị chặn triển khai. Đây là lựa chọn thứ tự viết tài liệu, không sửa thứ tự đợt trong nguồn.

## 5. Bảng theo dõi màn hình hiện tại

Các cột màn hình, route, AC, API tham chiếu, màn hình liên kết, độ ưu tiên và nhãn phía máy chủ/điều kiện bên dưới được chép từ list_screen.md §2; route vẫn là đề xuất. Chỉ đổi trạng thái sau khi đầu ra của từng ID đạt kiểm tra tĩnh tại §3.

| ID | Màn hình / bề mặt | Route đề xuất | AC | API tham chiếu | Màn hình liên kết | Đợt | Ưu tiên | Nền tảng máy chủ / điều kiện chặn | Trạng thái DD |
|---|---|---|---|---|---|---|---|---|---|
| SH-01 | Trang giới thiệu Study (Trang) | `/` | AC-03 | #05, #06 | GS-01,SH-02,SH-03 | W0 | P0 | R | BẢN_NHÁP_ĐÃ_XONG |
| SH-02 | Đăng nhập (Trang) | `/login` | AC-02 | #03, #04 | ST-01 hoặc vỏ giao diện theo vai trò chờ xác nhận; SH-03 | W0 | P0 | R; CHẶN: Khởi tạo hồ sơ vai trò người hướng dẫn/quản trị viên chưa hoàn chỉnh | BẢN_NHÁP_ĐÃ_XONG |
| SH-03 | Đăng ký học viên (Trang) | `/register` | AC-01 | #01 | SH-04,SH-02 | W0 | P0 | R; CHẶN: Giao diện chưa có trong bản làm việc; API xác thực email còn giả lập | BẢN_NHÁP_ĐÃ_XONG |
| SH-04 | Bàn giao xác thực thư điện tử (Trang) | `/register/verification` | AC-01 | #02 | SH-02 | W0 (bị chặn: dịch vụ gửi thư mới ở mức giả lập) | P1 | S; CHẶN: Bộ gửi thư giả lập, chưa có điểm cuối xác nhận | BẢN_NHÁP_ĐÃ_XONG |
| SH-05 | Không đủ quyền / phiên hết hạn (Màn hình trạng thái) | `/forbidden` | AC-02,AC-11 | #04 | SH-02 hoặc route an toàn trước đó | W0 | P0 | R | CHƯA_BẮT_ĐẦU |
| SH-06 | Trang không tồn tại / tài nguyên không còn (Màn hình trạng thái) | `/not-found` | AC-05 | #08 | GS-01,SH-01 | W0 | P0 | D | CHƯA_BẮT_ĐẦU |
| SH-07 | Theo dõi tác vụ bất đồng bộ (Bảng) | `/operations/:operationId` | AC-12,AC-25,AC-36,AC-38 | #18 | ST-07,ME-15,AD-21,AD-25 | W4 | P2 | D; CHẶN: Enum trạng thái tác vụ/ánh xạ ID còn mâu thuẫn | CHƯA_BẮT_ĐẦU |
| GS-01 | Danh sách khóa học (Trang) | `/courses` | AC-03 | #05, #06 | GS-02,GS-03 | W0 | P0 | R; CHẶN: Danh mục chỉ hiển thị siêu dữ liệu; bộ lọc theo danh mục chưa hoạt động | CHƯA_BẮT_ĐẦU |
| GS-02 | Tìm kiếm khóa học (Trang) | `/courses/search?q=` | AC-04 | #05, #07 | GS-01,GS-03 | W0 | P0 | R; CHẶN: Chưa xác nhận bộ lọc theo danh mục có hoạt động | CHƯA_BẮT_ĐẦU |
| GS-03 | Chi tiết khóa học (Trang) | `/courses/:courseId` | AC-05 | #08, #09, #10 | GS-04,GS-05,GS-06,ST-04 | W1 | P1 | D; CHẶN: API #8–#10 chưa được nối; #8 trả kiểu Page<Course> | CHƯA_BẮT_ĐẦU |
| GS-04 | Đề cương khóa học (Thẻ) | `/courses/:courseId?tab=curriculum` | AC-05 | #09 | GS-03,ST-10 | W1 | P1 | D; CHẶN: Các quy tắc khả năng hiển thị bài học ở mức DD giả định | CHƯA_BẮT_ĐẦU |
| GS-05 | Đánh giá và thảo luận công khai (Thẻ) | `/courses/:courseId?tab=reviews` | AC-05 | #08, #10 | GS-03 | W1 | P2 | D; CHẶN: Lược đồ còn thiếu trường rating/title; nội dung đánh giá hiện được ánh xạ từ thảo luận | CHƯA_BẮT_ĐẦU |
| GS-06 | Tài nguyên khóa học (Thẻ) | `/courses/:courseId?tab=resources` | AC-06 | #11, #12 | GS-07,GS-03 | W1 | P2 | D; CHẶN: API #11 trả một Resource thay vì danh sách; chưa có quy tắc khả năng hiển thị | CHƯA_BẮT_ĐẦU |
| GS-07 | Xem/tải tài nguyên (Trang) | `/resources/:resourceId` | AC-06 | #12 | GS-06 | W1 | P2 | D; CHẶN: Quyền truy cập công khai hay riêng tư và dịch vụ ký URL chưa chốt | CHƯA_BẮT_ĐẦU |
| ST-01 | Tổng quan học viên (Trang) | `/student` | AC-13,AC-18,AC-20 | #20, #21, #38, #43 | ST-08,ST-20,ST-26,ST-02 | W3 (bị chặn bảng điều khiển APIs; mở rộng thứ tự) | P1 | D; CHẶN: API bảng điều khiển chưa được nối | CHƯA_BẮT_ĐẦU |
| ST-02 | Hồ sơ cá nhân (Trang) | `/student/profile` | AC-11 | #04 | ST-03 | W0 | P0 | R | CHƯA_BẮT_ĐẦU |
| ST-03 | Chỉnh sửa hồ sơ/ảnh đại diện (Trang) | `/student/profile/edit` | AC-11 | #04, #13, #14 | ST-02 | W1 | P1 | M; CHẶN: API #13/#14 chưa được nối; hợp đồng avatar, bio, phone còn xung đột | CHƯA_BẮT_ĐẦU |
| ST-04 | Kiểm tra ghi danh trước đăng ký (Trang) | `/student/enroll/:courseId` | AC-12 | #08, #15 | ST-05,ST-07,ST-08 | W2 | P1 | D; CHẶN: API #15 là công khai nhưng không xác định người dùng | CHƯA_BẮT_ĐẦU |
| ST-05 | Kiểm tra đơn hàng / thanh toán (Trang) | `/student/checkout/:courseId` | AC-12 | #08, #16 | ST-06,ST-04 | W2 | P2 | D; CHẶN: Bảng đơn hàng và chính sách thanh toán chưa có bằng chứng từ mã nguồn | CHƯA_BẮT_ĐẦU |
| ST-06 | Thực hiện thanh toán (Trang) | `/student/pay/:orderId` | AC-12 | #17, #18 | ST-07,SH-07 | W2 | P2 | D; CHẶN: Hợp đồng cổng thanh toán và tác vụ chưa triển khai | CHƯA_BẮT_ĐẦU |
| ST-07 | Kết quả đăng ký khóa học (Trang) | `/student/enroll/result/:courseId` | AC-12 | #18, #19, #20 | ST-08,ST-09 | W2 | P2 | D; CHẶN: Máy chủ phải xác minh thanh toán và bảo đảm ghi danh nguyên tử, không gây tác động lặp | CHƯA_BẮT_ĐẦU |
| ST-08 | Khóa học của tôi (Trang) | `/student/courses` | AC-13 | #20, #21 | ST-09,ST-20 | W1 | P1 | D; CHẶN: Cấu trúc phản hồi #20/#21 trong danh mục không khớp | CHƯA_BẮT_ĐẦU |
| ST-09 | Tổng quan khóa đang học (Trang) | `/student/courses/:courseId` | AC-13,AC-18 | #09, #20, #37 | ST-10,ST-21 | W1 | P1 | D; CHẶN: Chưa có hợp đồng đầy đủ cho cây học tập khóa học | CHƯA_BẮT_ĐẦU |
| ST-10 | Kiểm tra quyền và bắt đầu học (Chuyển tiếp) | `/student/lessons/:lessonId/start` | AC-14 | #22, #23, #24 | ST-11,ST-09 | W1 | P1 | D; CHẶN: Chưa có API quyền truy cập/bắt đầu bài học khi chạy | CHƯA_BẮT_ĐẦU |
| ST-11 | Trình phát bài học (Trang) | `/student/lessons/:lessonId` | AC-14,AC-15 | #24, #25, #26, #27 | ST-12,ST-09,ST-13,ST-17 | W1 | P1 | D; CHẶN: Cần chốt giới hạn tần suất cập nhật tiến độ và chính sách tự lưu | CHƯA_BẮT_ĐẦU |
| ST-12 | Tài liệu kèm bài học (Bảng) | `/student/lessons/:lessonId/resources` | AC-15 | #26, #12 | ST-11,GS-07 | W1 | P2 | D; CHẶN: Danh mục ghi kiểu phản hồi #26 là Lesson; cần làm rõ | CHƯA_BẮT_ĐẦU |
| ST-13 | Giới thiệu bài kiểm tra (Trang) | `/student/quizzes/:quizId` | AC-16 | #28 | ST-14 | W2 | P1 | D; CHẶN: Chưa quyết định quy tắc giới hạn thời gian và việc hiển thị đáp án | CHƯA_BẮT_ĐẦU |
| ST-14 | Làm bài kiểm tra (Trang) | `/student/quizzes/:quizId/attempts/:attemptId` | AC-16 | #28, #29, #30 | ST-15 | W2 | P1 | D; CHẶN: Còn thiếu quy tắc không lặp tác động của tự lưu, nguồn thời gian và lược đồ câu trả lời | CHƯA_BẮT_ĐẦU |
| ST-15 | Xác nhận nộp bài kiểm tra (Hộp thoại) | `/student/attempts/:attemptId/submit` | AC-16 | #30, #31 | ST-16,ST-14 | W2 | P1 | D; CHẶN: Chưa chốt máy trạng thái nộp bài | CHƯA_BẮT_ĐẦU |
| ST-16 | Kết quả bài kiểm tra (Trang) | `/student/attempts/:attemptId/result` | AC-16 | #32 | ST-09,ST-20 | W2 | P1 | D | CHƯA_BẮT_ĐẦU |
| ST-17 | Chi tiết bài tập (Trang) | `/student/assignments/:assignmentId` | AC-17 | #33 | ST-18,ST-09 | W2 | P1 | D | CHƯA_BẮT_ĐẦU |
| ST-18 | Soạn và nộp bài tập (Trang) | `/student/assignments/:assignmentId/submit` | AC-17 | #33, #34, #35 | ST-19,ST-17 | W2 | P1 | D; CHẶN: Chưa chốt giới hạn tải tệp, thử lại và dọn dữ liệu mồ côi | CHƯA_BẮT_ĐẦU |
| ST-19 | Bài đã nộp và phản hồi (Trang) | `/student/submissions/:submissionId` | AC-17 | #36 | ST-17,ST-20 | W2 | P1 | D | CHƯA_BẮT_ĐẦU |
| ST-20 | Tổng quan tiến độ (Trang) | `/student/progress` | AC-18 | #21, #38 | ST-21,ST-22 | W3 | P2 | D; CHẶN: Phản hồi tiến độ chưa có lược đồ miền dữ liệu chuẩn | CHƯA_BẮT_ĐẦU |
| ST-21 | Tiến độ theo khóa học (Trang) | `/student/progress/:courseId` | AC-18 | #37 | ST-11,ST-20 | W3 | P2 | D | CHƯA_BẮT_ĐẦU |
| ST-22 | Thành tích và chứng nhận (Trang) | `/student/achievements` | AC-18 | #38 | ST-20,ST-09 | W3 | P2 | D; CHẶN: Cơ chế lưu thành tích mới suy ra từ thiết kế | CHƯA_BẮT_ĐẦU |
| ST-23 | Danh sách thảo luận (Trang) | `/student/discussions` | AC-19 | #39 | ST-24,ST-25 | W3 | P2 | D | CHƯA_BẮT_ĐẦU |
| ST-24 | Tạo câu hỏi / chủ đề (Trang) | `/student/discussions/new` | AC-19 | #40, #39 | ST-23,ST-25 | W3 | P2 | D; CHẶN: Hợp đồng content:int64 không khớp ngữ nghĩa văn bản định dạng | CHƯA_BẮT_ĐẦU |
| ST-25 | Chi tiết chuỗi thảo luận và phản hồi (Trang) | `/student/discussions/:discussionId` | AC-19 | #42, #41 | ST-23 | W3 | P2 | D; CHẶN: Kiểu phản hồi thảo luận Page<Discussion> không nhất quán | CHƯA_BẮT_ĐẦU |
| ST-26 | Thông báo học viên (Trang) | `/student/notifications` | AC-20 | #43, #44, #45 | ST-09,ST-17,ST-25 | W3 | P2 | D; CHẶN: Chưa định nghĩa dữ liệu liên kết sâu trong thông báo | CHƯA_BẮT_ĐẦU |
| ME-01 | Bảng điều khiển người hướng dẫn (Trang) | `/mentor` | AC-21,AC-23,AC-24 | #46, #54, #58 | ME-02,ME-09,ME-11 | W3 | P1 | D; CHẶN: Chưa có API nhận diện vai trò người hướng dẫn | CHƯA_BẮT_ĐẦU |
| ME-02 | Các khóa học phụ trách (Trang) | `/mentor/courses` | AC-21 | #46 | ME-03,ME-04,ME-16 | W3 | P1 | D | CHƯA_BẮT_ĐẦU |
| ME-03 | Không gian làm việc khóa học của người hướng dẫn (Trang) | `/mentor/courses/:courseId` | AC-22,AC-26 | #49, #65 | ME-04,ME-06,ME-16 | W3 | P1 | D | CHƯA_BẮT_ĐẦU |
| ME-04 | Tải lên và tạo bài giảng (Trang) | `/mentor/courses/:courseId/lectures/new` | AC-21 | #46, #34, #47 | ME-05,ME-03 | W3 | P1 | D; CHẶN: Lược đồ lecture.content và tham chiếu tài sản còn chưa rõ | CHƯA_BẮT_ĐẦU |
| ME-05 | Xem bài giảng người hướng dẫn (Trang) | `/mentor/lectures/:lectureId` | AC-21 | #48 | ME-03,ME-06 | W3 | P1 | D | CHƯA_BẮT_ĐẦU |
| ME-06 | Cây nội dung khóa học (Trang) | `/mentor/courses/:courseId/content` | AC-22 | #49 | ME-07,ME-08 | W3 | P1 | D; CHẶN: Không có mô hình nội dung trong 18 bảng DB.sql | CHƯA_BẮT_ĐẦU |
| ME-07 | Tạo/chỉnh sửa nội dung (Trang) | `/mentor/courses/:courseId/content/:contentId?` | AC-22 | #49, #50, #51 | ME-06,ME-08 | W3 | P1 | D; CHẶN: Danh mục chưa mô tả rõ body của PUT #51 | CHƯA_BẮT_ĐẦU |
| ME-08 | Xuất bản/xóa nội dung (Hộp thoại) | `/mentor/content/:contentId/actions` | AC-22 | #52, #53, #49 | ME-06 | W3 | P2 | D; CHẶN: Cần chốt máy trạng thái xuất bản và phụ thuộc khi xóa | CHƯA_BẮT_ĐẦU |
| ME-09 | Danh sách bài cần chấm (Trang) | `/mentor/submissions` | AC-23 | #54 | ME-10 | W3 | P1 | D; CHẶN: Số lượng phần tử trong phản hồi #54 sai kiểu | CHƯA_BẮT_ĐẦU |
| ME-10 | Chấm điểm và phản hồi (Trang) | `/mentor/submissions/:submissionId` | AC-23 | #55, #56, #57 | ME-09 | W3 | P1 | D; CHẶN: Chưa khóa trường tiêu chí chấm, kiểu điểm và tính nguyên tử | CHƯA_BẮT_ĐẦU |
| ME-11 | Hộp thư hỗ trợ học viên (Trang) | `/mentor/support` | AC-24 | #58 | ME-12 | W3 | P2 | D; CHẶN: SupportRequest không có bảng trong DB.sql | CHƯA_BẮT_ĐẦU |
| ME-12 | Trao đổi và đóng yêu cầu (Trang) | `/mentor/support/:requestId` | AC-24 | #59, #60, #61 | ME-11 | W3 | P2 | D; CHẶN: Chưa có API tạo yêu cầu hỗ trợ cho học viên | CHƯA_BẮT_ĐẦU |
| ME-13 | Chọn người nhận thông báo (Bước) | `/mentor/notifications/new/recipients` | AC-25 | #46, #62 | ME-14 | W3 | P2 | D; CHẶN: Chưa chốt payload người nhận dưới dạng chuỗi | CHƯA_BẮT_ĐẦU |
| ME-14 | Soạn thông báo người hướng dẫn (Trang) | `/mentor/notifications/new` | AC-25 | #62, #63 | ME-15 | W3 | P2 | D; CHẶN: Tác vụ gửi chưa được nối | CHƯA_BẮT_ĐẦU |
| ME-15 | Theo dõi gửi thông báo (Trang) | `/mentor/notifications/:notificationId/status` | AC-25 | #18, #64 | ME-14,SH-07 | W3 | P2 | D; CHẶN: Chưa chốt ánh xạ operation_id và notification_id | CHƯA_BẮT_ĐẦU |
| ME-16 | Tiến độ toàn khóa học (Trang) | `/mentor/courses/:courseId/progress` | AC-26 | #65 | ME-17,ME-18 | W3 | P2 | D; CHẶN: Page<Course> của #65 chưa có cấu trúc dữ liệu phân tích phù hợp | CHƯA_BẮT_ĐẦU |
| ME-17 | Tiến độ từng học viên (Trang) | `/mentor/courses/:courseId/students/:studentId/progress` | AC-26 | #67 | ME-16 | W3 | P2 | D | CHƯA_BẮT_ĐẦU |
| ME-18 | Phân tích khóa học (Trang) | `/mentor/courses/:courseId/analytics` | AC-26 | #66 | ME-16 | W3 | P2 | D; CHẶN: Chưa xác lập lược đồ chỉ số | CHƯA_BẮT_ĐẦU |
| AD-01 | Bảng điều khiển quản trị (Trang) | `/admin` | AC-38 | #101 | AD-02,AD-06,AD-24 | W4 | P1 | D; CHẶN: Thiếu endpoint hồ sơ vai trò quản trị | CHƯA_BẮT_ĐẦU |
| AD-02 | Danh sách người dùng (Trang) | `/admin/users` | AC-31 | #68 | AD-03,AD-04 | W4 | P1 | D | CHƯA_BẮT_ĐẦU |
| AD-03 | Chi tiết người dùng (Trang) | `/admin/users/:userId` | AC-31 | #69 | AD-04,AD-05 | W4 | P1 | D | CHƯA_BẮT_ĐẦU |
| AD-04 | Chỉnh sửa người dùng (Trang) | `/admin/users/:userId/edit` | AC-31 | #69, #70 | AD-03 | W4 | P1 | D; CHẶN: Chưa đặc tả body PUT của API #70 | CHƯA_BẮT_ĐẦU |
| AD-05 | Khóa/mở khóa/xóa tài khoản (Hộp thoại) | `/admin/users/:userId/actions` | AC-31 | #69, #71, #72 | AD-02,AD-03 | W4 | P2 | D; CHẶN: Chưa khóa chính sách xóa và trạng thái vai trò | CHƯA_BẮT_ĐẦU |
| AD-06 | Danh sách khóa học quản trị (Trang) | `/admin/courses` | AC-32 | #73 | AD-07 | W4 | P1 | D; CHẶN: Chưa có quan hệ khóa học-danh mục | CHƯA_BẮT_ĐẦU |
| AD-07 | Chi tiết khóa học quản trị (Trang) | `/admin/courses/:courseId` | AC-32 | #74 | AD-08,AD-09,AD-12 | W4 | P1 | D | CHƯA_BẮT_ĐẦU |
| AD-08 | Chỉnh sửa khóa học (Trang) | `/admin/courses/:courseId/edit` | AC-32 | #74, #75 | AD-07 | W4 | P1 | D; CHẶN: Chưa xác nhận body PUT #75 và tải ảnh thu nhỏ lên | CHƯA_BẮT_ĐẦU |
| AD-09 | Thay đổi trạng thái/xóa khóa (Hộp thoại) | `/admin/courses/:courseId/actions` | AC-32 | #74, #76, #77 | AD-06,AD-07 | W4 | P2 | D; CHẶN: Chưa xác nhận chính sách xóa | CHƯA_BẮT_ĐẦU |
| AD-10 | Hàng đợi kiểm duyệt nội dung (Trang) | `/admin/content/pending` | AC-33 | #78 | AD-11 | W4 | P1 | D; CHẶN: Cơ chế lưu nội dung chưa có trong DDL | CHƯA_BẮT_ĐẦU |
| AD-11 | Duyệt/từ chối nội dung (Trang) | `/admin/content/:contentId/review` | AC-33 | #79, #80, #81 | AD-10 | W4 | P1 | D; CHẶN: Chưa khóa quy tắc duyệt và xuất bản | CHƯA_BẮT_ĐẦU |
| AD-12 | Danh sách bài học quản trị (Trang) | `/admin/lessons` | AC-34 | #82 | AD-13 | W4 | P1 | D | CHƯA_BẮT_ĐẦU |
| AD-13 | Chi tiết bài học quản trị (Trang) | `/admin/lessons/:lessonId` | AC-34 | #83 | AD-14 | W4 | P1 | D | CHƯA_BẮT_ĐẦU |
| AD-14 | Sửa, đổi trạng thái, xóa bài học (Trang) | `/admin/lessons/:lessonId/edit` | AC-34 | #83, #84, #85, #86 | AD-12,AD-13 | W4 | P1 | D; CHẶN: Cần chốt phụ thuộc giữa DELETE và tiến độ bài học | CHƯA_BẮT_ĐẦU |
| AD-15 | Danh sách bài kiểm tra (Trang) | `/admin/quizzes` | AC-35 | #87 | AD-16,AD-17,AD-18 | W4 | P1 | D | CHƯA_BẮT_ĐẦU |
| AD-16 | Tạo/chỉnh sửa bài kiểm tra (Trang) | `/admin/quizzes/new hoặc /admin/quizzes/:quizId/edit` | AC-35 | #88, #89 | AD-15,AD-17 | W4 | P1 | D; CHẶN: Thiếu GET chi tiết bài kiểm tra cho quản trị viên và lược đồ cấu hình/câu hỏi | CHƯA_BẮT_ĐẦU |
| AD-17 | Thống kê bài kiểm tra (Trang) | `/admin/quizzes/:quizId/statistics` | AC-35 | #91 | AD-15 | W4 | P2 | D; CHẶN: Kiểu Quiz trong phản hồi #91 không đủ dữ liệu thống kê | CHƯA_BẮT_ĐẦU |
| AD-18 | Xác nhận xóa bài kiểm tra (Hộp thoại) | `/admin/quizzes/:quizId/delete` | AC-35 | #90 | AD-15 | W4 | P2 | D; CHẶN: Chưa quyết định chính sách xóa khi đã có lượt làm bài | CHƯA_BẮT_ĐẦU |
| AD-19 | Danh sách thông báo quản trị (Trang) | `/admin/notifications` | AC-36 | #92 | AD-20,AD-21 | W4 | P1 | D | CHƯA_BẮT_ĐẦU |
| AD-20 | Soạn/gửi thông báo hệ thống (Trang) | `/admin/notifications/new` | AC-36 | #93 | AD-21,SH-07 | W4 | P1 | D; CHẶN: Chưa rõ lược đồ gửi theo người nhận/nhóm và ID tác vụ | CHƯA_BẮT_ĐẦU |
| AD-21 | Sửa/kiểm soát/đo trạng thái thông báo (Trang) | `/admin/notifications/:notificationId` | AC-36 | #18, #94, #95, #96 | AD-19,SH-07 | W4 | P1 | D; CHẶN: Chưa có GET riêng để đọc chi tiết thông báo | CHƯA_BẮT_ĐẦU |
| AD-22 | Danh sách thảo luận bị báo cáo (Trang) | `/admin/discussions/reported` | AC-37 | #97 | AD-23 | W4 | P1 | D; CHẶN: Chưa có POST báo cáo thảo luận từ học viên | CHƯA_BẮT_ĐẦU |
| AD-23 | Điều tra/kiểm duyệt thảo luận (Trang) | `/admin/discussions/:discussionId/moderate` | AC-37 | #98, #99, #100 | AD-22 | W4 | P1 | D; CHẶN: Lưu báo cáo/kiểm toán chưa có bằng chứng từ mã nguồn | CHƯA_BẮT_ĐẦU |
| AD-24 | Báo cáo tác động cộng đồng (Trang) | `/admin/reports/community-impact` | AC-38 | #101, #102 | AD-25 | W4 | P2 | D; CHẶN: Chưa xác nhận định nghĩa chỉ số báo cáo | CHƯA_BẮT_ĐẦU |
| AD-25 | Xuất báo cáo và theo dõi tiến trình (Trang) | `/admin/reports/export` | AC-38 | #103, #18 | AD-24,SH-07 | W4 | P2 | D; CHẶN: Chưa chốt URL xuất, lược đồ kết quả và danh sách định dạng được phép | CHƯA_BẮT_ĐẦU |

## 6. Nền tảng hiện tại và điều kiện nghiệm thu

- **Nguồn API hiện tại của SH-01:** list_screen phân loại #05/#06 là có mã nguồn. API #05 trả danh mục ACTIVE theo locale chính xác; API #06 trả khóa học PUBLISHED với tiêu đề/mô tả/ảnh thu nhỏ/giá/trạng thái và trường định danh người hướng dẫn. Mã nguồn #06 hiện từ chối category; không mô tả rằng bộ lọc danh mục đang hoạt động.
- **Nguồn UI hiện tại của SH-01:** không có mã nguồn/router Study Web. / và liên kết tới các ID khác chỉ là đề xuất. Mã nguồn/kiểm thử API không chứng minh dữ liệu DB trực tiếp hoặc môi trường đã triển khai.
- **Nền tảng trạng thái chung:** INITIAL, LOADING, READY, EMPTY, DIRTY, MUTATING, ACCEPTED (202), UNAUTHORIZED, FORBIDDEN, NOT_FOUND, CONFLICT, VALIDATION_ERROR, SERVICE_ERROR. Chỉ đưa trạng thái phù hợp với từng màn hình; các widget độc lập phải có thể khôi phục riêng.
- **Nền tảng giao diện chung:** token Study xanh biển, nhịp cách 4px, nội dung tối đa khoảng 1120px, bố cục thích ứng điện thoại/máy tính bảng/máy tính, điều khiển >=44px, tương phản có ngữ nghĩa và focus bàn phím rõ. Đây là hướng dẫn đích, không phải bằng chứng khi chạy.
- **Không tự tạo hành vi:** không thêm route, API, trường, bảng, kiểm tra, dịch vụ hoặc tuyên bố dữ liệu khi chưa có bằng chứng. Phụ thuộc D/S/UNWIRED có thể được ghi là điều kiện chặn, không được mô tả là đang hoạt động.
- **Hoàn tất:** đủ 83 ID có DD đặt tên theo màn hình, kế hoạch riêng soạn trước, ảnh chú thích cho mọi biến thể nguồn hiện có, bản đồ marker khớp, truy vết sự kiện tới nguồn, liên kết tương đối hoạt động, worklog được cập nhật và điều kiện còn mở được ghi rõ. Chưa hoàn tất nếu vẫn có dòng theo dõi chưa xong.

## 7. Phiên đầu tiên

- **Màn hình:** SH-01 — Trang giới thiệu Study.
- **Rà soát tài sản hiện tại:** có 83 PNG + 83 HTML; README liệt kê biến thể SH-01 thứ hai nhưng hệ thống tệp hiện tại không có. screen.png và code.html của variant-1 khác đáng kể: ảnh có thêm danh mục, sáu thẻ, lợi ích/lời chứng thực/logo/email; HTML có hai ví dụ khóa học viết cứng và liên kết neo giữ chỗ.
- **Điều kiện cần ghi nhận:** chỉ lập tài liệu cho một biến thể đang có, không suy đoán biến thể thiếu; đánh dấu chỉ số/thẻ/bằng chứng xã hội mẫu là chưa được hỗ trợ cho tới khi có nội dung/dữ liệu duyệt.

## Tài liệu tham chiếu

- apps/study-client/docs/list_screen.md §§0–9; trọng tâm là danh mục màn hình, F01–F13, chỉ mục API, ma trận trạng thái UI, điều kiện chặn và kế hoạch đợt.
- apps/study-client/docs/screen_stitch/90_reference/study2work-lms-design-system/DESIGN.md (chỉ là tham khảo hình ảnh).
- .agents/web-study/design.md (đích giao diện Study chuẩn; không phải bằng chứng khi chạy).
- Mã nguồn API hiện tại: apps/study-server/app/api/v1.py, apps/study-server/app/modules/guest/api_05_categories/, apps/study-server/app/modules/guest/api_06_courses/ và thư mục kiểm thử tương ứng.
