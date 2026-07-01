# Study2Work — Danh sách màn UI theo module

## Mục tiêu
Tài liệu này gom các màn UI theo đúng nhóm chức năng của hệ thống Study2Work, bám theo:
- kiến trúc monorepo và module nghiệp vụ của dự án,
- luồng người học / mentor / doanh nghiệp / quản trị,
- use case đã mô tả trong diagram.

## Done
1. Public
2. Xác thực & Onboarding

---

## 1) Module Public / Khách truy cập

### PUB-01. Trang chủ landing
- Giới thiệu sản phẩm, định vị EdTech + HRTech, CTA đăng ký.
- Khối nội dung: hero, giá trị cốt lõi, quy trình học, lộ trình, đối tác, testimonial.

### PUB-02. Giới thiệu nền tảng
- Mô tả hệ sinh thái học tập, thực chiến, đánh giá năng lực, kết nối tuyển dụng.
- Các mục: vì sao khác biệt, mô hình vận hành, đối tượng phù hợp.

### PUB-03. Lộ trình đào tạo công khai
- Hiển thị các giai đoạn Foundation, Core Skills, Team Project, Career Ready, Employer Connection.
- Có thể xem theo nhánh: Frontend / Backend / Mobile.

### PUB-04. Danh sách khóa học / chương trình
- Liệt kê chương trình học, bootcamp, mentoring, luyện phỏng vấn.
- Bộ lọc theo level, nhánh nghề, thời lượng, hình thức học.

### PUB-05. Chi tiết khóa học / chương trình
- Nội dung chương trình, mục tiêu đầu ra, yêu cầu đầu vào, mentor phụ trách, CTA đăng ký.

### PUB-06. Workshop / sự kiện / cộng đồng công khai
- Danh sách workshop, challenge, livestream, mock interview.
- Có lịch, mô tả, đăng ký tham gia.

### PUB-07. Blog / tin tức / tài nguyên
- Bài viết kiến thức, lộ trình học, review CV, chia sẻ kinh nghiệm đi làm.

### PUB-08. Câu hỏi thường gặp
- Giải đáp về học phí, đầu ra, cách học, mentor, tuyển dụng, chứng chỉ, portfolio.

### PUB-09. Liên hệ / hỗ trợ
- Form liên hệ, hotline, email, social links, thông tin hợp tác.

---

## 2) Module Xác thực & Onboarding

### AUTH-01. Đăng ký tài khoản
- Đăng ký bằng email / số điện thoại / social login nếu có.
- Chọn vai trò ban đầu: người học, mentor, doanh nghiệp.

### AUTH-02. Đăng nhập
- Đăng nhập thường, ghi nhớ phiên, chuyển hướng theo vai trò.

### AUTH-03. Quên mật khẩu
- Gửi mã xác thực / link đặt lại mật khẩu.

### AUTH-04. Đặt lại mật khẩu
- Nhập mật khẩu mới, xác nhận mật khẩu mới.

### AUTH-05. Xác thực email / OTP
- Xác minh tài khoản sau đăng ký hoặc khi đổi thông tin nhạy cảm.

### AUTH-06. Chọn vai trò / mục tiêu học tập
- Người học chọn mục tiêu: học lại nền tảng, đi thực tập, fresher, nâng cấp kỹ năng.

### AUTH-07. Hoàn thiện hồ sơ ban đầu
- Avatar, tên, trường, ngành, level, nhánh nghề, mục tiêu học.
- Dùng để cá nhân hóa lộ trình học.

---

## 3) Module Người học / Student

### 3.1 Dashboard & tổng quan

### STD-01. Dashboard người học
- Tổng quan tiến độ học, task đang làm, lịch học, thông báo, điểm số.
- Khối gợi ý: việc cần làm hôm nay, học gần nhất, mục tiêu tuần.

### STD-02. Hoạt động gần đây
- Lịch sử xem bài học, nộp bài, nhận feedback, tham gia project.

### STD-03. Lịch học cá nhân
- Xem timeline buổi học, deadline, workshop, live session.

### 3.2 Kiểm tra đầu vào & lộ trình

### STD-04. Màn kiểm tra đầu vào
- Bài test nền tảng để xác định điểm xuất phát.

### STD-05. Kết quả đầu vào
- Hiển thị mức độ hiện tại, điểm mạnh/yếu, đề xuất nhánh học.

### STD-06. Lộ trình học cá nhân hóa
- Hiển thị roadmap theo level và nhánh nghề.
- Có trạng thái đã học, đang học, sắp học.

### STD-07. Chi tiết một chặng học
- Mục tiêu, danh sách bài học, assignment, quiz, lab, project liên quan.

### 3.3 Học tập

### STD-08. Danh sách khóa học / module học
- Danh sách nội dung theo module, filter theo trạng thái học.

### STD-09. Chi tiết khóa học
- Nội dung, mục tiêu, bài học, tài liệu, live session, mentor.

### STD-10. Trình phát bài giảng video
- Video, tốc độ phát, bookmark, note, bài học tiếp theo.

### STD-11. Màn live session
- Tham gia lớp học trực tuyến, lịch sử buổi học, tài liệu đi kèm.

### STD-12. Thư viện tài liệu
- Slide, PDF, link, code sample, file tải về.

### STD-13. Ghi chú học tập
- Tạo note cá nhân trong lúc học.

### 3.4 Thực hành

### STD-14. Danh sách bài tập / quiz / lab
- Gom các bài thực hành theo module, mức độ, deadline.

### STD-15. Màn làm quiz
- Trắc nghiệm, câu hỏi ngắn, hiển thị điểm sau khi nộp.

### STD-16. Màn làm lab lập trình
- Môi trường thực hành / editor / hướng dẫn / kiểm tra kết quả.

### STD-17. Màn nộp bài
- Upload file, link repo, link demo, mô tả bài làm.

### STD-18. Màn trạng thái bài nộp
- Đang chờ chấm, đã chấm, bị trả về, cần chỉnh sửa.

### STD-19. Màn feedback bài tập
- Nhận nhận xét, điểm số, rubric, đề xuất cải thiện.

### 3.5 Dự án nhóm

### STD-20. Danh sách project cá nhân / nhóm
- Project đang tham gia, project đã hoàn thành, project được giao.

### STD-21. Chi tiết project
- Mô tả dự án, thành viên, vai trò, mốc tiến độ, file đính kèm.

### STD-22. Bảng nhiệm vụ sprint / Kanban
- To do / Doing / Review / Done, gán người phụ trách.

### STD-23. Màn pull request / code review
- Danh sách PR, trạng thái review, comment, lịch sử sửa.

### STD-24. Nhật ký đóng góp
- Ghi nhận commit, task đã hoàn thành, đóng góp trong team.

### 3.6 Đánh giá năng lực

### STD-25. Dashboard kỹ năng
- Skill matrix tổng quan, level từng kỹ năng, xu hướng tăng trưởng.

### STD-26. Chi tiết một kỹ năng
- Điểm, tiêu chí, lịch sử đánh giá, đề xuất học tiếp.

### STD-27. Lịch sử đánh giá
- Các lần test, assessment, nhận xét từ mentor, kết quả theo thời gian.

### STD-28. Báo cáo năng lực cá nhân
- Tổng hợp năng lực kỹ thuật, soft skill, kỷ luật, teamwork.

### 3.7 Portfolio / CV / Nghề nghiệp

### STD-29. Dashboard portfolio
- Tổng quan hồ sơ năng lực số, trạng thái công khai, lượt xem.

### STD-30. Trình tạo portfolio
- Chọn template, kéo thả nội dung, thêm project, bài viết, chứng chỉ.

### STD-31. Xem trước portfolio
- Preview bản public trước khi công khai.

### STD-32. Quản lý CV
- Danh sách CV, tạo mới, sao chép, phiên bản.

### STD-33. Trình tạo CV
- Chọn template, nhập thông tin, học vấn, kinh nghiệm, project, kỹ năng.

### STD-34. Xem trước và xuất CV
- Preview, export PDF, chia sẻ link.

### STD-35. Luyện phỏng vấn
- Danh sách bộ câu hỏi, mock interview, kỹ thuật / HR / hành vi.

### STD-36. Kết quả luyện phỏng vấn
- Nhận feedback, điểm mạnh/yếu, gợi ý cải thiện.

### 3.8 Cộng đồng

### STD-37. Trang cộng đồng
- Feed bài viết, hỏi đáp, chia sẻ kinh nghiệm, thảo luận nhóm.

### STD-38. Workshop / challenge / mock interview
- Lịch sự kiện, đăng ký tham gia, trạng thái tham dự.

### STD-39. Trang bài viết / thảo luận
- Xem nội dung, bình luận, like, lưu bài.

### 3.9 Tài khoản & hệ thống

### STD-40. Hồ sơ cá nhân
- Thông tin cá nhân, avatar, mục tiêu, nhánh học, liên kết xã hội.

### STD-41. Cài đặt tài khoản
- Đổi mật khẩu, ngôn ngữ, thông báo, quyền riêng tư.

### STD-42. Trung tâm thông báo
- Thông báo học tập, deadline, feedback, phỏng vấn, system alert.

### STD-43. Lịch sử thanh toán
- Xem hóa đơn, gói học, gói mentoring, trạng thái thanh toán.

### STD-44. Trang thanh toán / checkout
- Chọn gói, xác nhận đơn, thanh toán, kết quả giao dịch.

---

## 4) Module Mentor

### MEN-01. Dashboard mentor
- Tổng quan lớp học, bài cần chấm, project cần review, lịch mentoring.

### MEN-02. Quản lý lớp / nhóm học
- Danh sách lớp, nhóm học, trạng thái học viên, phân nhóm.

### MEN-03. Chi tiết lớp học
- Danh sách học viên, tiến độ, điểm số, nguy cơ bỏ dở, ghi chú.

### MEN-04. Giao bài tập / assignment
- Tạo bài tập, đặt deadline, rubric, đính kèm tài liệu.

### MEN-05. Danh sách bài nộp
- Lọc theo lớp, bài, trạng thái, mức độ hoàn thành.

### MEN-06. Màn chấm bài
- Chấm điểm, comment, trả bài, yêu cầu sửa.

### MEN-07. Màn review code
- Xem diff, comment theo dòng, đề xuất refactor, checklist chất lượng.

### MEN-08. Màn đánh giá rubric
- Đánh giá theo tiêu chí: code quality, teamwork, deadline, problem solving.

### MEN-09. Màn đánh giá năng lực học viên
- Tổng hợp skill matrix, nhận xét, mức độ tiến bộ, đề xuất nhánh học.

### MEN-10. Màn mentoring / 1-1 session
- Lịch hẹn, nội dung buổi mentor, biên bản sau buổi học.

### MEN-11. Màn workshop
- Tạo workshop, quản lý đăng ký, điểm danh, tài liệu.

### MEN-12. Báo cáo lớp học
- Thống kê tiến độ, tỉ lệ hoàn thành, học viên cần hỗ trợ.

---

## 5) Module Doanh nghiệp / Employer

### EMP-01. Dashboard doanh nghiệp
- Tổng quan job post, candidate pool, shortlist, liên hệ.

### EMP-02. Hồ sơ công ty
- Thông tin công ty, mô tả, logo, website, lĩnh vực, quy mô.

### EMP-03. Danh sách tin tuyển dụng
- Quản lý các job post đang mở / đã đóng / nháp.

### EMP-04. Chi tiết tin tuyển dụng
- Mô tả công việc, yêu cầu kỹ năng, level, quyền lợi.

### EMP-05. Tạo / chỉnh sửa tin tuyển dụng
- Form đăng job, điều kiện lọc, thời hạn, gói tuyển dụng.

### EMP-06. Tìm kiếm ứng viên
- Tìm theo skill, level, project, trường, kinh nghiệm, vị trí mong muốn.

### EMP-07. Bộ lọc ứng viên
- Lọc theo skill matrix, portfolio, CV, project, điểm đánh giá.

### EMP-08. Hồ sơ ứng viên
- Xem thông tin, portfolio, CV, project, kỹ năng, feedback mentor.

### EMP-09. Shortlist ứng viên
- Danh sách ứng viên đã lưu, gắn trạng thái theo pipeline.

### EMP-10. Quy trình tuyển dụng
- Pipeline: mới xem -> liên hệ -> phỏng vấn -> offer -> tuyển.

### EMP-11. Màn liên hệ ứng viên
- Gửi message / email / mời phỏng vấn / trao đổi lịch.

### EMP-12. Thống kê tuyển dụng
- Số hồ sơ xem, số shortlist, số phỏng vấn, tỉ lệ chuyển đổi.

---

## 6) Module Quản trị hệ thống / Admin

### ADM-01. Dashboard quản trị
- Tổng quan người dùng, học viên, mentor, doanh nghiệp, nội dung, báo cáo.

### ADM-02. Quản lý người dùng
- Danh sách user, tìm kiếm, khóa/mở khóa, xem lịch sử hoạt động.

### ADM-03. Quản lý vai trò & phân quyền
- Role, permission, gán quyền theo module và tính năng.

### ADM-04. Quản lý nội dung
- Bài học, tài liệu, blog, workshop, cộng đồng, media.

### ADM-05. Quản lý mentor
- Duyệt mentor, hồ sơ, phân công lớp, trạng thái hoạt động.

### ADM-06. Quản lý doanh nghiệp
- Duyệt công ty, gói dịch vụ, trạng thái tài khoản, lịch sử đăng tin.

### ADM-07. Quản lý đánh giá
- Assessment, rubric, skill matrix mẫu, cấu hình tiêu chí.

### ADM-08. Báo cáo & phân tích
- Dashboard KPI, tỉ lệ học, tỉ lệ hoàn thành, tỉ lệ tuyển dụng.

### ADM-09. Cài đặt hệ thống
- Cấu hình email, thông báo, thanh toán, banner, cấu hình chung.

### ADM-10. Nhật ký hệ thống
- Audit log, log hoạt động, lỗi, cảnh báo bảo mật.

---

## 7) Module AI hỗ trợ

### AI-01. Trợ lý AI tổng quát
- Chat hỏi đáp trong hệ thống.
- Gợi ý theo ngữ cảnh màn đang mở.

### AI-02. AI gợi ý lộ trình học
- Sinh roadmap theo đầu vào, mục tiêu nghề nghiệp, level hiện tại.

### AI-03. AI giải thích code
- Phân tích đoạn code, giải thích luồng xử lý, khái niệm liên quan.

### AI-04. AI gợi ý sửa lỗi
- Gợi ý nguyên nhân lỗi, cách fix, checklist debug.

### AI-05. AI review CV
- Phân tích CV, chấm sơ bộ, góp ý về bố cục, nội dung, từ khóa.

### AI-06. AI review portfolio
- Gợi ý cải thiện portfolio, cách trình bày project, case study.

### AI-07. AI luyện phỏng vấn
- Bộ câu hỏi theo role, chấm câu trả lời, gợi ý cải thiện.

### AI-08. Lịch sử trao đổi AI
- Lưu lại session chat, prompt đã dùng, kết quả đã sinh ra.

---

## 8) Module Thông báo

### NOTI-01. Trung tâm thông báo
- Gộp thông báo học tập, dự án, mentor, tuyển dụng, admin.

### NOTI-02. Chi tiết thông báo
- Nội dung, nguồn, thời gian, link điều hướng.

### NOTI-03. Cài đặt thông báo
- Email / in-app / push, bật tắt theo loại thông báo.

### NOTI-04. Thông báo lịch học
- Nhắc buổi học, deadline, workshop, phỏng vấn.

---

## 9) Module Thanh toán

### PAY-01. Trang bảng giá / gói dịch vụ
- So sánh gói học, mentoring, bootcamp, tuyển dụng.

### PAY-02. Chọn gói / đặt mua
- Chọn dịch vụ, số lượng, thời hạn, ưu đãi.

### PAY-03. Checkout
- Xác nhận thông tin, phương thức thanh toán, mã giảm giá.

### PAY-04. Kết quả thanh toán
- Thành công / thất bại / chờ xử lý.

### PAY-05. Lịch sử giao dịch
- Danh sách hóa đơn, trạng thái thanh toán, tải hóa đơn.

---

## 10) Module Màn dùng chung / hệ thống

### SYS-01. Sidebar / topbar / shell ứng dụng
- Khung điều hướng dùng chung cho từng vai trò.

### SYS-02. Tìm kiếm toàn cục
- Tìm course, project, bài viết, candidate, user, report.

### SYS-03. Upload / quản lý file
- Avatar, CV, portfolio, project files, certificate.

### SYS-04. Trang lỗi
- 401, 403, 404, 500, empty state, no permission.

### SYS-05. Cài đặt ngôn ngữ / giao diện
- Chọn ngôn ngữ, dark/light mode, kích thước hiển thị.

---

## 11) Gợi ý map module theo app

### Web public
- PUB-01 → PUB-09

### Web / mobile cho người học
- AUTH-01 → AUTH-07
- STD-01 → STD-44
- NOTI-01 → NOTI-04
- PAY-01 → PAY-05
- AI-01 → AI-08
- SYS-01 → SYS-05

### Web mentor
- MEN-01 → MEN-12
- NOTI-01 → NOTI-04
- SYS-01 → SYS-05

### Web employer
- EMP-01 → EMP-12
- NOTI-01 → NOTI-04
- SYS-01 → SYS-05

### Web admin
- ADM-01 → ADM-10
- SYS-01 → SYS-05

---

## 12) Kết luận
Danh sách này ưu tiên đúng theo các nhóm chức năng cốt lõi của Study2Work: học tập, thực hành, đánh giá năng lực, portfolio/CV, cộng đồng, mentor, tuyển dụng, AI và quản trị. Đây là bộ màn đủ sát để làm checklist UI, chia task thiết kế, hoặc dùng làm prompt cho AI tạo giao diện.