# Kế hoạch màn hình — SH-01 Trang giới thiệu Study

> **Trạng thái:** KẾ_HOẠCH_ĐÃ_XONG / DD_ĐANG_SOẠN · **Phạm vi phiên:** chỉ SH-01 · **Đợt danh mục:** W0.

## 1. Hợp đồng và bằng chứng

- **Tác nhân / vai trò:** Khách; trang giới thiệu công khai.
- **Bề mặt / route đề xuất:** Trang, / (đề xuất từ list_screen.md, chưa phải route của client hiện tại).
- **AC / độ ưu tiên / nhãn phía máy chủ trong danh mục:** AC-03, P0, R cho bằng chứng API nguồn. Trạng thái UI là UNWIRED vì apps/study-client/src không có trong bản làm việc này.
- **Truy vết:** SH-01 → API #05 GET /api/v1/categories và API #06 GET /api/v1/courses; các liên kết khám phá tiếp tục tới GS-01/GS-02. F02 mô tả chọn course_id để tới GS-03/#08, nhưng #08 chỉ có trong thiết kế và ô màn hình kế tiếp của SH-01 không liệt kê GS-03. DD sẽ ghi đây là sai khác/luồng mục tiêu, không phải hành vi hiện tại.
- **Tài sản nguồn tìm thấy:** `screen.png` (559×1600) và `code.html` trong thư mục biến thể 1 hiện tại. Worklog cũ và phiên bản README trước đây từng liệt kê biến thể SH-01 thứ hai, nhưng cây hiện tại không có thư mục hoặc tệp tương ứng. Không phục hồi hay suy đoán nội dung.
- **Mã băm trước khi chú thích:** PNG 777f11eafd87807524c99ac6c21d402519311f3c9ff48f54c0781b543bc0d64f; HTML d22ed5ee5000b49f6c4b69297b460ed0d2841938b04887f5b3882b8582d3e5b8.
- **Sai khác ảnh / HTML:** ảnh chụp có phần mở đầu, chỉ số, dải danh mục, sáu thẻ khóa học, thẻ lợi ích, lời chứng thực, logo đối tác, thu thập email và chân trang. HTML có liên kết giữ chỗ, điều khiển tìm kiếm và hai thẻ khóa học mẫu viết cứng; không thể hiện toàn bộ ảnh. Giữ nguyên hai bản gốc và ghi nhận chúng không tương đương.

## 2. Mục tiêu và luồng đích

1. Mở route đề xuất /; hiển thị phần giới thiệu tĩnh đã được duyệt ngay.
2. Tải danh mục (#05) và một trang khóa học đã xuất bản (#06) độc lập. Lỗi ở một khu vực không được làm trống khu vực còn lại.
3. Gửi nội dung tìm kiếm đã loại khoảng trắng đầu/cuối tới GS-02 (/courses/search?q=); #07 thuộc GS-02, không thuộc SH-01.
4. “Khám phá khóa học” / “Xem tất cả” chuyển tới GS-01 (/courses).
5. Thao tác đăng nhập / đăng ký chuyển tới SH-02 / SH-03.
6. Chọn khóa học có thể dẫn tới GS-03 theo F02 bằng course_id trả về, nhưng đây là ĐÍCH / SAI KHÁC: #08 ở trạng thái D và danh sách màn hình kế tiếp của SH-01 tại §2 không có GS-03. Giữ thao tác thẻ ở trạng thái chặn hoặc dùng GS-01 cho tới khi được duyệt.
7. Thẻ danh mục, nhãn sắp xếp, biểu mẫu email, chỉ số marketing chưa được hỗ trợ, lời chứng thực và logo đối tác không được gọi API chưa có căn cứ hoặc tự nhận là dữ liệu thật.

## 3. API và ánh xạ phản hồi

### API #05 — danh mục

- **Route / nguồn:** apps/study-server/app/api/v1.py → api_05_categories.view.get_categories → find_active_categories → SQL ACTIVE_CATEGORIES → ánh xạ phản hồi Category / CategoryPage.
- **Yêu cầu:** GET /api/v1/categories; bỏ locale để dùng mặc định hiện tại vi-VN. Truy vấn khớp chính xác locale và status=ACTIVE, sắp theo id ASC.
- **Ánh xạ thành công:** data.items[] gồm id, name, slug, description tùy chọn; data.pagination có page=1, size=tổng số, total, total_pages=1 (kể cả khi không có mục nào).
- **Hiển thị:** Có thể lấy tên danh mục để điền dải thông tin danh mục. slug không phải bộ lọc khóa học trong hành vi #06 hiện tại. Không tự tạo nội dung bản địa hóa ngoài dữ liệu của dòng danh mục.
- **Lỗi:** Đầu vào truy vấn sai có thể trả 422; lỗi truy vấn/ánh xạ trả 500 an toàn DESIGN_INTERNAL_ERROR kèm trace ID. Danh sách rỗng vẫn là 200, không phải lỗi.

### API #06 — khóa học đã xuất bản

- **Route / nguồn:** apps/study-server/app/api/v1.py → api_06_courses.view.get_courses → kiểm tra đầu vào → SQL đếm và phân trang trên courses kết hợp users (mentor) → map_course → CoursePage.
- **Yêu cầu đề xuất cho trang giới thiệu:** GET /api/v1/courses?page=1&size=6. size=6 nằm trong khoảng hiện chấp nhận 1..100; nếu bỏ sort, thứ tự mặc định là created_at DESC, id ASC. Kích thước mặc định của endpoint là 20. Không gửi category từ dải danh mục; endpoint trả 422 cho tới khi xử lý xong điều kiện quan hệ/bộ lọc.
- **Ánh xạ thành công:** data.items[] gồm id, title, description tùy chọn, thumbnail_url tùy chọn, price dạng chuỗi thập phân, status (PUBLISHED với các dòng này), mentor{id,full_name,avatar_url?}; data.pagination gồm page,size,total,total_pages.
- **DTO hiện không có:** tiền tệ, giá cũ/giảm giá, điểm đánh giá/số lượt đánh giá, thời lượng, số bài học, lượt ghi danh, danh mục, thứ hạng nổi bật/phổ biến. Không hiển thị chúng như dữ liệu API; không suy luận ký hiệu tiền tệ chỉ từ price.
- **Lỗi:** page<1, size ngoài 1..100, sort không hỗ trợ hoặc có bộ lọc category đều trả 422; lỗi SQL/ánh xạ/người hướng dẫn không còn bản ghi trả 500 an toàn; trang rỗng/ngoài phạm vi trả thành công với items rỗng và siêu dữ liệu phân trang. Chỉ hiển thị lỗi trong khu vực tương ứng và đưa trace ID nếu có.

## 4. Kế hoạch chú thích đánh số

Tọa độ tính bằng pixel CSS trên PNG gốc 559×1600. `SH-01_markers.json` là dữ liệu đầu vào cho bộ dựng. Các số 1–13 phải xuất hiện đúng một lần và khớp bảng phần tử trong DD.

| # | Khu vực đích | Chi tiết / nội dung được phép | Thao tác |
|---:|---|---|---|
| 1 | Đầu trang | Thương hiệu, điều hướng chính, tìm kiếm, đăng nhập/đăng ký; không giả định chuông/ảnh đại diện có chức năng | Chuyển tới SH-01, GS-01, GS-02, SH-02, SH-03 khi đích đã xác định |
| 2 | Nội dung mở đầu | Tiêu đề, mô tả ngắn, nhãn chỉ dùng khi ngày tháng/lời khẳng định đã được xác minh | Nội dung tĩnh; không gọi API |
| 3 | Tìm kiếm | Ô nhập và nút gửi | Loại khoảng trắng hai đầu của q; chuyển tới GS-02; không gọi #07 tại đây |
| 4 | Nút hành động mở đầu | Khám phá khóa học / lời kêu gọi đăng ký | GS-01 / SH-03 |
| 5 | Dải chỉ số | Ảnh có 10.000+, 120+, 94% | Chưa có căn cứ; ẩn cho tới khi có nguồn được duyệt |
| 6 | Dải danh mục | Chỉ lấy tên từ #05; thẻ không lọc | Không gửi category cho #06; tắt tương tác cho tới khi điều kiện G-05 được giải quyết |
| 7 | Tiêu đề / điều khiển khóa học nổi bật | Tiêu đề, “xem tất cả”, điều khiển trông như sắp xếp/bộ lọc | “Xem tất cả” → GS-01; ẩn điều khiển chưa được hỗ trợ |
| 8 | Thẻ khóa học | Chỉ dùng DTO #06 | Thao tác mở chi tiết còn bị chặn; xem bước 6 §2 |
| 9 | Thẻ lợi ích | Nội dung và biểu tượng tĩnh | Chỉ dùng nội dung biên tập đã duyệt; không gọi API |
| 10 | Lời chứng thực | Ảnh có điểm sao, tên và tuyên bố nơi làm việc | SH-01 không có API lời chứng thực/đánh giá tổng quát; ẩn tới khi có nguồn được duyệt |
| 11 | Logo nhà tuyển dụng | Dải đối tác/nhà tuyển dụng | Không có API; cần tài sản và tuyên bố sử dụng được duyệt |
| 12 | Kêu gọi để lại email | Ô email và nút gửi | Chưa có endpoint; không thu thập/gửi; bỏ hoặc tắt cho tới khi có API được duyệt |
| 13 | Chân trang | Nhóm liên kết, liên kết pháp lý, huy hiệu | Chỉ dùng liên kết Study đã biết; URL ngoài/pháp lý cần được duyệt |

## 5. Thuật toán sự kiện chi tiết cần ghi trong DD

| Sự kiện | Đầu vào / nguồn | Xử lý | Kết quả / trạng thái tiếp |
|---|---|---|---|
| E01 vào trang | Route đề xuất /; locale #05 mặc định vi-VN | Hiển thị khung tĩnh; gọi độc lập #05 và #06 (song song); danh mục không phụ thuộc yêu cầu khóa học | Mỗi khu vực ở LOADING rồi tự chuyển READY, EMPTY hoặc lỗi riêng |
| E02 nhận phản hồi danh mục | Phản hồi #05 | Đọc data.items đã kiểm tra; hiển thị tên; không dùng slug làm bộ lọc | Dải danh mục rỗng hoặc có dữ liệu; bấm thẻ không gọi #06 |
| E03 nhận phản hồi khóa học | Phản hồi #06 | Chỉ đọc trường DTO; giữ thứ tự máy chủ; dùng id làm khóa; ảnh null dùng chỗ giữ trung tính; giá thập phân không tự thêm tiền tệ | Danh sách hoặc trạng thái rỗng; chỉ hiển thị pagination.total nếu thật sự cần |
| E04 gửi tìm kiếm | Chuỗi người dùng nhập | Loại khoảng trắng hai đầu; ô rỗng không gọi API (câu chữ báo lỗi là quyết định sản phẩm); chuyển tới GS-02 kèm q đã mã hóa | GS-02 sở hữu yêu cầu #07 và trạng thái tìm kiếm/lỗi |
| E05 xem tất cả | Bấm nút xem danh mục khóa học | Chuyển tới GS-01; không quy định gọi API lặp tại đây | GS-01 sở hữu trạng thái trang/bộ lọc |
| E06 chuyển tới xác thực | Bấm đăng nhập/đăng ký | Chuyển tới SH-02/SH-03 | API xác thực thuộc các màn hình đó |
| E07 chọn danh mục | id/slug từ #05 | Không gửi category cho #06 khi G-05 chưa xử lý; giữ thẻ chỉ để xem hoặc vô hiệu hóa | Không gọi yêu cầu / không đổi trạng thái |
| E08 chọn khóa học | course.id từ #06 | Luồng đích F02 tới GS-03 với courseId ổn định; chặn vì #08 ở trạng thái D và ô điều hướng của danh mục bỏ qua GS-03 | Chưa được duyệt thì không cho thao tác hoặc dẫn về GS-01; không tuyên bố đã tải chi tiết |
| E09 thử lại khu vực | Người dùng bấm thử lại ở khu vực lỗi | Chỉ gọi lại GET của khu vực đó; không thử lại 422 do tham số không hỗ trợ | Khu vực về LOADING rồi tự nhận trạng thái thành công/rỗng/lỗi |
| E10 gửi email | Email người dùng nhập | Không có API hay hợp đồng lưu trữ được duyệt; không gửi/lưu | Ẩn/tắt có ghi rõ điều kiện |
| E11 điều hướng chân trang | Bấm liên kết nội bộ đã biết | Chỉ dùng đích tương đối đã duyệt; liên kết neo chưa rõ/ngoài miền tắt cho tới khi có đích | Route an toàn hoặc không thao tác với trạng thái vô hiệu hóa rõ ràng |

## 6. Trạng thái và tiêu chí nghiệm thu

- Phần mở đầu tĩnh hiển thị mà không đợi API.
- Danh mục và khóa học nổi bật tải độc lập; lỗi một yêu cầu không làm mất phần còn lại.
- #05 có items rỗng là trạng thái rỗng bình thường; #06 có trang rỗng là trạng thái chưa có khóa học xuất bản.
- Chỉ thử lại GET an toàn. Không đổi lỗi 500/mạng thành thành công rỗng. Không tự chuyển lỗi API công khai sang màn hình đăng nhập.
- Bộ lọc danh mục, chỉ số giả, nhãn điểm/thời lượng/giảm giá, dữ liệu khóa học mẫu, lời chứng thực, tuyên bố logo đối tác và thu thập email tiếp tục ẩn/tắt cho tới khi có nguồn được duyệt.
- Tìm kiếm loại khoảng trắng hai đầu và chuyển tới GS-02; SH-01 không gọi #07.
- Liên kết đăng nhập/đăng ký trỏ tới SH-02/SH-03. Mọi route vẫn là đề xuất cho tới khi Study Web có khi chạy.
- Sai khác điều hướng chi tiết khóa học được giải quyết hoặc tiếp tục bị chặn rõ ràng.
- Đích giao diện theo .agents/web-study/design.md: màu biển, điều khiển cao 44px, nhịp 4px và bố cục thích ứng. Ảnh mẫu rộng 559px không chứng minh bố cục thích ứng.
- Hash PNG/HTML gốc không đổi; có ảnh đánh số; bản đồ marker khớp bảng phần tử DD.

## 7. Quyết định còn mở

1. Cung cấp hoặc chính thức loại bỏ biến thể SH-01 thứ hai đang thiếu; chủ sở hữu: quản lý tài sản `screen_stitch`.
2. Xác nhận ảnh hay HTML là phiên bản giao diện được chọn; chủ sở hữu: Sản phẩm/Thiết kế.
3. Xác nhận thẻ khóa học SH-01 có mở trực tiếp GS-03 không, vì F02 có nhưng ô điều hướng SH-01 không liệt kê, còn API #08 ở trạng thái D; chủ sở hữu: BA/Sản phẩm.
4. Duyệt hoặc bỏ các phần chỉ số, lời chứng thực, logo doanh nghiệp và thu thập email; chủ sở hữu: Sản phẩm/Marketing.
5. Xác nhận cách ghi giá khóa học vì API #06 trả chuỗi giá thập phân không kèm tiền tệ; chủ sở hữu: Sản phẩm/máy chủ.
6. Giải quyết G-05 trước khi biến thẻ danh mục thành bộ lọc; chủ sở hữu: máy chủ/DB.
7. Xác nhận .agents/web-study/design.md tiếp tục là nguồn chuẩn giao diện hay có ngoại lệ riêng được duyệt; chủ sở hữu: Thiết kế Study.
