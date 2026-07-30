# Business Code Registry

| API | Success code | Meaning |
|---:|---|---|
| 001 | `CATALOG_OVERVIEW_RETRIEVED` | Lấy nội dung giới thiệu Study và điều hướng đến danh mục. thành công. |
| 002 | `CATALOG_LEARNING_PATHS_LISTED` | Tìm kiếm, lọc và phân trang lộ trình đã công khai. thành công. |
| 003 | `CATALOG_LEARNING_PATHS_SLUG_RETRIEVED` | Xem chi tiết lộ trình công khai và hành động phù hợp trạng thái người xem. thành công. |
| 004 | `CATALOG_COURSES_RETRIEVED` | Tìm kiếm, lọc danh sách khóa học công khai. thành công. |
| 005 | `CATALOG_COURSES_SLUG_RETRIEVED` | Xem thông tin khóa học, curriculum công khai và lộ trình sử dụng khóa học. thành công. |
| 006 | `CATALOG_SAMPLE_LESSON_LOADED` | Xem phần bài học mẫu được Admin cho phép công khai; không tạo tiến độ. thành công. |
| 007 | `ACCOUNT_REGISTERED_PENDING_VERIFICATION` | Tạo tài khoản học viên ở trạng thái chờ xác thực. thành công. |
| 008 | `ACCOUNT_LOGIN_SUCCEEDED` | Đăng nhập và trả ngữ cảnh điều hướng theo trạng thái tài khoản. thành công. |
| 009 | `AUTH_LOGOUT_COMPLETED` | Đăng xuất phiên hiện tại. thành công. |
| 010 | `AUTH_VERIFICATION_SEND_COMPLETED` | Gửi hoặc gửi lại link/OTP xác thực có giới hạn chống spam. thành công. |
| 011 | `ACCOUNT_CONTACT_VERIFIED` | Xác nhận email/điện thoại và chuyển tài khoản sang VERIFIED. thành công. |
| 012 | `AUTH_ACCOUNT_STATUS_RETRIEVED` | Lấy trạng thái tài khoản, xác thực, onboarding và quyền học hiện tại. thành công. |
| 013 | `AUTH_PASSWORD_FORGOT_COMPLETED` | Khởi tạo quy trình khôi phục mật khẩu mà không tiết lộ tài khoản có tồn tại. thành công. |
| 014 | `AUTH_PASSWORD_RESET_COMPLETED` | Đặt mật khẩu mới bằng token/OTP khôi phục. thành công. |
| 015 | `AUTH_PASSWORD_UPDATED` | Đổi mật khẩu khi đã đăng nhập. thành công. |
| 016 | `ME_PROFILE_RETRIEVED` | Lấy hồ sơ tài khoản, hồ sơ học tập và thiết lập cá nhân. thành công. |
| 017 | `ME_PROFILE_UPDATED` | Cập nhật các trường hồ sơ học viên được phép tự sửa. thành công. |
| 018 | `ME_CONTACT_CHANGE_CREATED` | Yêu cầu đổi email/số điện thoại và gửi xác thực kênh mới. thành công. |
| 019 | `ME_CONTACT_CHANGE_CONFIRM_COMPLETED` | Xác nhận kênh liên hệ mới trước khi áp dụng. thành công. |
| 020 | `ME_NAVIGATION_CONTEXT_RETRIEVED` | Xác định màn hình đích sau đăng nhập hoặc khi mở hành động bắt đầu học. thành công. |
| 021 | `ONBOARDING_CONFIG_RETRIEVED` | Lấy cấu hình bước onboarding, mục tiêu, công nghệ và lựa chọn nền tảng. thành công. |
| 022 | `ONBOARDING_CURRENT_RETRIEVED` | Lấy trạng thái onboarding, bản nháp và bước cần tiếp tục. thành công. |
| 023 | `ONBOARDING_DRAFT_SAVED` | Lưu hợp lệ dữ liệu từng bước và cho phép tiếp tục sau khi thoát. thành công. |
| 024 | `ONBOARDING_RECOMMENDED_PATHS_RETRIEVED` | Sinh danh sách lộ trình gợi ý từ hồ sơ onboarding. thành công. |
| 025 | `ONBOARDING_SELECTED_PATH_UPDATED` | Chọn duy nhất một lộ trình để xác nhận; chưa kích hoạt. thành công. |
| 026 | `ONBOARDING_REVIEW_RETRIEVED` | Lấy toàn bộ thông tin xác nhận trước khi hoàn tất onboarding. thành công. |
| 027 | `ONBOARDING_COMPLETED` | Xác nhận dữ liệu và chuyển tài khoản sang READY_TO_LEARN. thành công. |
| 028 | `LEARNING_PATHS_RETRIEVED` | Lấy danh sách lộ trình đã xuất bản kèm trạng thái cá nhân. thành công. |
| 029 | `LEARNING_PATHS_RETRIEVED` | Xem cấu trúc lộ trình, trạng thái từng khóa và điều kiện còn thiếu. thành công. |
| 030 | `LEARNING_PATHS_ACTIVATION_PREVIEW_CREATED` | Kiểm tra điều kiện và hiển thị xác nhận trước khi kích hoạt. thành công. |
| 031 | `LEARNING_PATH_ACTIVATED` | Kích hoạt lộ trình duy nhất và mở nội dung đầu tiên. thành công. |
| 032 | `ME_LEARNING_PATHS_ACTIVE_RETRIEVED` | Lấy lộ trình ACTIVE hiện tại và hành động tiếp theo. thành công. |
| 033 | `ME_LEARNING_PATHS_HISTORY_RETRIEVED` | Lấy lịch sử các lộ trình đã tham gia, kể cả hoàn thành/hủy/reset. thành công. |
| 034 | `ME_LEARNING_PATHS_ENROLLMENT_ID_SUMMARY_RETRIEVED` | Xem tổng kết lộ trình hoặc dữ liệu ôn tập lịch sử. thành công. |
| 035 | `ME_LEARNING_PATHS_NEXT_RECOMMENDATIONS_RETRIEVED` | Gợi ý lộ trình tiếp theo sau khi hoàn thành lộ trình hiện tại. thành công. |
| 036 | `SUPPORT_REQUEST_CREATED` | Gửi yêu cầu đổi/reset/hủy lộ trình theo quy trình ngoại lệ. thành công. |
| 037 | `SUPPORT_REQUESTS_RETRIEVED` | Xem danh sách yêu cầu hỗ trợ lộ trình của bản thân. thành công. |
| 038 | `SUPPORT_REQUESTS_RETRIEVED` | Xem chi tiết và kết quả xử lý yêu cầu lộ trình. thành công. |
| 039 | `COURSES_RETRIEVED` | Lấy chi tiết khóa học theo quyền truy cập của người xem. thành công. |
| 040 | `COURSES_CURRICULUM_RETRIEVED` | Lấy cây chương, bài học và bài tập cùng trạng thái khóa/hoàn thành. thành công. |
| 041 | `CHAPTERS_RETRIEVED` | Lấy chi tiết chương và các điều kiện mở khóa/hoàn thành. thành công. |
| 042 | `LESSON_STUDY_LOADED` | Mở bài học, tải nội dung, tài nguyên, tiến độ hiện tại và điều hướng. thành công. |
| 043 | `COURSES_CONTINUE_RETRIEVED` | Xác định bài đang học hoặc nội dung bắt buộc tiếp theo trong khóa. thành công. |
| 044 | `LESSONS_RESOURCES_RETRIEVED` | Lấy tài liệu đính kèm theo quyền và phân loại bắt buộc/tham khảo. thành công. |
| 045 | `RESOURCES_ACCESS_RETRIEVED` | Tạo/nhận quyền truy cập hoặc URL tải tài nguyên hợp lệ. thành công. |
| 046 | `CONTENT_ISSUES_CREATED` | Báo lỗi video, tài liệu, nội dung, link hoặc bản quyền ngay tại màn học. thành công. |
| 047 | `ME_CONTENT_ISSUES_RETRIEVED` | Theo dõi các báo lỗi nội dung đã gửi. thành công. |
| 048 | `EXERCISES_RETRIEVED` | Lấy danh sách bài tập theo khóa/chương/bài học và trạng thái cá nhân. thành công. |
| 049 | `EXERCISES_RETRIEVED` | Xem đề bài, tiêu chí, hint, tài liệu, hình thức nộp và trạng thái bài nộp. thành công. |
| 050 | `EXERCISES_DRAFT_RETRIEVED` | Lấy bản nháp bài làm hiện tại. thành công. |
| 051 | `EXERCISES_DRAFT_UPDATED` | Tạo/cập nhật bản nháp; chưa tính là đã nộp hoặc hoàn thành. thành công. |
| 052 | `EXERCISE_SUBMISSION_CREATED` | Nộp bài lần đầu và chuyển sang chấm tự động hoặc chờ review. thành công. |
| 053 | `EXERCISES_SUBMISSIONS_LATEST_RETRIEVED` | Lấy bài nộp và kết quả đánh giá mới nhất. thành công. |
| 054 | `EXERCISES_SUBMISSIONS_RETRIEVED` | Lấy lịch sử các lần nộp bài. thành công. |
| 055 | `SUBMISSIONS_RETRIEVED` | Lấy chi tiết một lần nộp và phản hồi tương ứng. thành công. |
| 056 | `EXERCISES_RESUBMISSIONS_CREATED` | Nộp lại khi NEEDS_REVISION hoặc được mở quyền. thành công. |
| 057 | `ADMIN_EXERCISE_SUBMISSIONS_RETRIEVED` | Lấy hàng đợi bài cần chấm và lọc theo trạng thái. thành công. |
| 058 | `ADMIN_EXERCISE_SUBMISSIONS_RETRIEVED` | Xem đầy đủ bài nộp, rubric và lịch sử chấm. thành công. |
| 059 | `EXERCISE_SUBMISSION_REVIEWED` | Chấm bài thủ công, ghi điểm, kết quả và phản hồi. thành công. |
| 060 | `ADMIN_EXERCISE_SUBMISSIONS_REOPEN_COMPLETED` | Mở lại quyền nộp bài trong trường hợp ngoại lệ. thành công. |
| 061 | `ME_DASHBOARD_RETRIEVED` | Lấy dashboard ưu tiên hành động học tiếp theo. thành công. |
| 062 | `ME_CONTINUE_LEARNING_RETRIEVED` | Xác định nội dung học tiếp theo trên toàn lộ trình. thành công. |
| 063 | `ME_PROGRESS_LEARNING_PATHS_RETRIEVED` | Lấy tiến độ chi tiết lộ trình và điều kiện còn thiếu. thành công. |
| 064 | `ME_PROGRESS_COURSES_RETRIEVED` | Lấy tiến độ khóa học theo chương, bài học và đánh giá. thành công. |
| 065 | `ME_PROGRESS_CHAPTERS_RETRIEVED` | Lấy tiến độ chương và trạng thái từng nội dung. thành công. |
| 066 | `ME_PROGRESS_LESSONS_RETRIEVED` | Lấy các điều kiện hoàn thành bài học và trạng thái từng điều kiện. thành công. |
| 067 | `LESSON_PROGRESS_UPDATED` | Ghi sự kiện xem video, đọc tài liệu hoặc xác nhận hoàn thành; tái tính tiến độ bài/chương/khóa/lộ trình. thành công. |
| 068 | `ME_LEARNING_HISTORY_RETRIEVED` | Lấy lịch sử lộ trình, khóa học, bài tập và nội dung gần đây. thành công. |
| 069 | `ME_COMPLETION_SUMMARIES_ENTITY_TYPE_RETRIEVED` | Lấy tổng kết khi hoàn thành khóa học hoặc lộ trình. thành công. |
| 070 | `COMMUNITY_GROUPS_RETRIEVED` | Lấy các nhóm cộng đồng phù hợp theo quyền, lộ trình, khóa học hoặc chủ đề. thành công. |
| 071 | `COMMUNITY_GROUPS_RETRIEVED` | Xem thông tin nhóm và quy tắc; link chỉ trả khi đủ quyền. thành công. |
| 072 | `COMMUNITY_LINK_OPENED` | Xác nhận đã đọc quy tắc, ghi nhận sự kiện mở link và trả liên kết Zalo. thành công. |
| 073 | `COMMUNITY_REPORT_CREATED` | Báo link hỏng, spam/lừa đảo, sai nội dung, moderator hoặc quy tắc. thành công. |
| 074 | `ME_COMMUNITY_REPORTS_RETRIEVED` | Theo dõi báo cáo cộng đồng đã gửi. thành công. |
| 075 | `ADMIN_COMMUNITY_GROUPS_RETRIEVED` | Tra cứu và quản lý danh sách nhóm cộng đồng. thành công. |
| 076 | `ADMIN_COMMUNITY_GROUPS_CREATED` | Tạo nhóm cộng đồng và gắn phạm vi áp dụng. thành công. |
| 077 | `ADMIN_COMMUNITY_GROUPS_RETRIEVED` | Lấy chi tiết quản trị nhóm, link, quy tắc, phạm vi và báo cáo. thành công. |
| 078 | `ADMIN_COMMUNITY_GROUPS_UPDATED` | Cập nhật tên, mô tả, link, quy tắc và điều kiện hiển thị. thành công. |
| 079 | `ADMIN_COMMUNITY_GROUPS_STATUS_UPDATED` | Chuyển trạng thái hoạt động, tạm dừng, đầy thành viên hoặc lưu trữ. thành công. |
| 080 | `ADMIN_COMMUNITY_GROUPS_MODERATORS_UPDATED` | Gán hoặc thay người phụ trách nhóm. thành công. |
| 081 | `ADMIN_COMMUNITY_REPORTS_RETRIEVED` | Lấy hàng đợi báo cáo cộng đồng. thành công. |
| 082 | `ADMIN_COMMUNITY_REPORTS_UPDATED` | Xử lý báo cáo cộng đồng và ghi kết quả. thành công. |
| 083 | `NOTIFICATIONS_LISTED` | Lấy trung tâm thông báo in-app có lọc và phân trang. thành công. |
| 084 | `NOTIFICATIONS_UNREAD_COUNT_RETRIEVED` | Lấy tổng số thông báo chưa đọc theo nhóm. thành công. |
| 085 | `NOTIFICATIONS_READ_UPDATED` | Đánh dấu một thông báo đã đọc. thành công. |
| 086 | `NOTIFICATIONS_READ_ALL_COMPLETED` | Đánh dấu đã đọc toàn bộ hoặc theo nhóm. thành công. |
| 087 | `NOTIFICATIONS_DELETED` | Ẩn/xóa thông báo khỏi trung tâm theo chính sách. thành công. |
| 088 | `NOTIFICATION_SETTINGS_ME_RETRIEVED` | Lấy thiết lập các kênh và loại thông báo có thể tùy chỉnh. thành công. |
| 089 | `NOTIFICATION_SETTINGS_ME_UPDATED` | Cập nhật thông báo không bắt buộc; không cho tắt sự kiện bảo mật/học tập bắt buộc. thành công. |
| 090 | `ADMIN_NOTIFICATIONS_RECIPIENT_PREVIEW_CREATED` | Xem trước nhóm người nhận trước khi gửi thông báo thủ công. thành công. |
| 091 | `ADMIN_NOTIFICATION_CREATED` | Gửi hoặc lên lịch thông báo tới nhóm học viên liên quan. thành công. |
| 092 | `ADMIN_NOTIFICATIONS_RETRIEVED` | Xem lịch sử thông báo thủ công và trạng thái gửi. thành công. |
| 093 | `ADMIN_NOTIFICATIONS_CANCEL_COMPLETED` | Hủy lô thông báo chưa gửi. thành công. |
| 094 | `ADMIN_LEARNING_PATHS_RETRIEVED` | Tra cứu lộ trình ở mọi trạng thái vòng đời. thành công. |
| 095 | `ADMIN_LEARNING_PATHS_CREATED` | Tạo lộ trình bản nháp. thành công. |
| 096 | `ADMIN_LEARNING_PATHS_RETRIEVED` | Lấy chi tiết quản trị lộ trình và cấu hình khóa học. thành công. |
| 097 | `ADMIN_LEARNING_PATHS_UPDATED` | Cập nhật thông tin và điều kiện lộ trình. thành công. |
| 098 | `ADMIN_LEARNING_PATHS_COURSES_UPDATED` | Gán và sắp xếp khóa học bắt buộc/tùy chọn trong lộ trình. thành công. |
| 099 | `ADMIN_LEARNING_PATHS_IMPACT_RETRIEVED` | Xem số học viên, khóa học và tiến độ bị ảnh hưởng trước thay đổi. thành công. |
| 100 | `ADMIN_LEARNING_PATHS_LIFECYCLE_COMPLETED` | Chuyển trạng thái DRAFT/IN_REVIEW/PUBLISHED/UPDATED/ARCHIVED. thành công. |
| 101 | `ADMIN_COURSES_RETRIEVED` | Tra cứu khóa học ở mọi trạng thái. thành công. |
| 102 | `ADMIN_COURSES_CREATED` | Tạo khóa học bản nháp. thành công. |
| 103 | `ADMIN_COURSES_RETRIEVED` | Lấy cấu hình đầy đủ khóa học, curriculum và tác động. thành công. |
| 104 | `ADMIN_COURSES_UPDATED` | Cập nhật thông tin, điều kiện hoàn thành và nhóm cộng đồng khóa học. thành công. |
| 105 | `ADMIN_COURSES_PATHS_UPDATED` | Gán khóa học vào một hoặc nhiều lộ trình. thành công. |
| 106 | `ADMIN_COURSES_CHAPTERS_ORDER_UPDATED` | Sắp xếp thứ tự chương trong khóa học. thành công. |
| 107 | `ADMIN_COURSES_IMPACT_RETRIEVED` | Xem học viên và lộ trình bị ảnh hưởng trước cập nhật khóa học. thành công. |
| 108 | `ADMIN_COURSES_LIFECYCLE_COMPLETED` | Chuyển trạng thái vòng đời khóa học. thành công. |
| 109 | `ADMIN_COURSES_CHAPTERS_CREATED` | Tạo chương trong khóa học. thành công. |
| 110 | `ADMIN_CHAPTERS_UPDATED` | Cập nhật tiêu đề, mục tiêu, điều kiện mở khóa/hoàn thành chương. thành công. |
| 111 | `ADMIN_CHAPTERS_DELETED` | Xóa chương khi được phép hoặc từ chối nếu ảnh hưởng nội dung đã xuất bản. thành công. |
| 112 | `ADMIN_CHAPTERS_ITEMS_ORDER_UPDATED` | Sắp xếp bài học/bài tập trong chương. thành công. |
| 113 | `ADMIN_CHAPTERS_LESSONS_CREATED` | Tạo bài học mới trong chương. thành công. |
| 114 | `ADMIN_LESSONS_UPDATED` | Cập nhật nội dung, video, ví dụ, điều kiện và tính bắt buộc của bài học. thành công. |
| 115 | `ADMIN_LESSONS_DELETED` | Xóa/ẩn bài học khi hợp lệ, bảo toàn lịch sử nếu đã có người học. thành công. |
| 116 | `ADMIN_LESSONS_PREVIEW_UPDATED` | Bật/tắt và cấu hình phạm vi bài học mẫu công khai. thành công. |
| 117 | `ADMIN_LESSONS_LIFECYCLE_COMPLETED` | Xuất bản, cập nhật, ẩn hoặc lưu trữ bài học. thành công. |
| 118 | `ADMIN_RESOURCES_CREATED` | Tạo tài liệu/tài nguyên và gắn nguồn, quyền sử dụng. thành công. |
| 119 | `ADMIN_RESOURCES_UPDATED` | Cập nhật mô tả, nguồn, quyền, liên kết và tính bắt buộc. thành công. |
| 120 | `ADMIN_RESOURCES_DELETED` | Ẩn/xóa tài nguyên không còn hợp lệ. thành công. |
| 121 | `ADMIN_EXERCISES_RETRIEVED` | Tra cứu cấu hình bài tập. thành công. |
| 122 | `ADMIN_EXERCISES_CREATED` | Tạo bài tập và cấu hình hình thức nộp/chấm. thành công. |
| 123 | `ADMIN_EXERCISES_RETRIEVED` | Lấy đầy đủ cấu hình bài tập, đáp án/rubric và thống kê ảnh hưởng. thành công. |
| 124 | `ADMIN_EXERCISES_UPDATED` | Cập nhật đề, hạn, đáp án, rubric, bắt buộc và quyền nộp lại. thành công. |
| 125 | `ADMIN_EXERCISES_DELETED` | Xóa/ẩn bài tập nếu hợp lệ, không phá lịch sử bài nộp. thành công. |
| 126 | `CONTENT_PRE_PUBLISH_CHECK_COMPLETED` | Chạy checklist trước xuất bản cho một nội dung được định danh trên URL. thành công. |
| 127 | `CONTENT_PUBLISHED` | Xuất bản, lưu trữ hoặc áp dụng cập nhật quan trọng cho nội dung sau khi kiểm tra điều kiện. thành công. |
| 128 | `ADMIN_LEARNERS_RETRIEVED` | Tra cứu học viên theo tên, liên hệ, mã, lộ trình và trạng thái. thành công. |
| 129 | `ADMIN_LEARNERS_SUPPORT_PROFILE_RETRIEVED` | Lấy hồ sơ hỗ trợ tổng hợp, không trả mật khẩu/OTP. thành công. |
| 130 | `ADMIN_LEARNERS_PROGRESS_RETRIEVED` | Xem tiến độ chi tiết phục vụ hỗ trợ nhưng không sửa trực tiếp. thành công. |
| 131 | `ADMIN_SUPPORT_REQUESTS_RETRIEVED` | Lấy hàng đợi yêu cầu đổi/reset/hủy lộ trình. thành công. |
| 132 | `ADMIN_SUPPORT_REQUESTS_RETRIEVED` | Xem yêu cầu, hồ sơ, tiến độ và lịch sử xử lý trước khi quyết định. thành công. |
| 133 | `SUPPORT_REQUEST_RESOLVED` | Chấp thuận/từ chối yêu cầu và chọn hành động ngoại lệ. thành công. |
| 134 | `ADMIN_LEARNERS_PROGRESS_RESET_COMPLETED` | Reset tiến độ theo phạm vi và lý do bắt buộc. thành công. |
| 135 | `ADMIN_LEARNERS_ACTIVE_PATH_CANCEL_COMPLETED` | Hủy lộ trình ACTIVE theo ngoại lệ. thành công. |
| 136 | `ADMIN_LEARNERS_ACTIVE_PATH_TRANSFER_COMPLETED` | Chuyển lộ trình bảo đảm không tạo hai lộ trình ACTIVE đồng thời. thành công. |
| 137 | `ADMIN_LEARNERS_SUSPEND_COMPLETED` | Tạm ngừng tài khoản vì vi phạm, bảo vệ tài khoản hoặc yêu cầu nội bộ. thành công. |
| 138 | `ADMIN_LEARNERS_UNSUSPEND_COMPLETED` | Mở lại tài khoản và ghi lý do. thành công. |
| 139 | `ADMIN_LEARNERS_SUPPORT_NOTES_RETRIEVED` | Lấy ghi chú nội bộ theo quyền. thành công. |
| 140 | `ADMIN_LEARNERS_SUPPORT_NOTES_CREATED` | Tạo ghi chú nội bộ hoặc phản hồi chính thức. thành công. |
| 141 | `ADMIN_LEARNERS_AUDIT_RETRIEVED` | Xem audit log liên quan riêng đến học viên. thành công. |
| 142 | `ADMIN_REPORT_OVERVIEW_LOADED` | Lấy dashboard tổng quan tài khoản, onboarding, học tập, bài tập và cộng đồng. thành công. |
| 143 | `ADMIN_REPORTS_REGISTRATIONS_RETRIEVED` | Báo cáo đăng ký và xác thực. thành công. |
| 144 | `ADMIN_REPORTS_ONBOARDING_RETRIEVED` | Báo cáo bắt đầu/hoàn thành onboarding và điểm rơi theo bước. thành công. |
| 145 | `ADMIN_REPORTS_LEARNING_PATHS_RETRIEVED` | Báo cáo kích hoạt, đang học, hoàn thành, thời gian và đổi/reset theo lộ trình. thành công. |
| 146 | `ADMIN_REPORTS_COURSES_RETRIEVED` | Báo cáo bắt đầu/hoàn thành khóa và điểm nghẽn bài học. thành công. |
| 147 | `ADMIN_REPORTS_ASSIGNMENTS_RETRIEVED` | Báo cáo nộp bài, kết quả, thời gian nộp và backlog review. thành công. |
| 148 | `ADMIN_REPORTS_COMMUNITY_RETRIEVED` | Báo cáo lượt mở link và vấn đề nhóm cộng đồng. thành công. |
| 149 | `ADMIN_OPERATION_ALERTS_LOADED` | Lấy cảnh báo vận hành theo ngưỡng đã cấu hình. thành công. |
| 150 | `ADMIN_RBAC_ROLES_RETRIEVED` | Lấy danh sách vai trò nghiệp vụ. thành công. |
| 151 | `ADMIN_RBAC_PERMISSIONS_RETRIEVED` | Lấy danh mục quyền chức năng. thành công. |
| 152 | `ADMIN_RBAC_MATRIX_RETRIEVED` | Lấy ma trận vai trò-quyền để kiểm thử và quản trị. thành công. |
| 153 | `ADMIN_USERS_ROLES_RETRIEVED` | Xem vai trò quản trị của một người dùng. thành công. |
| 154 | `ADMIN_USERS_ROLES_CREATED` | Cấp vai trò Admin/Support/Moderator/Content Admin. thành công. |
| 155 | `ADMIN_USERS_ROLES_ROLE_CODE_DELETED` | Thu hồi vai trò quản trị. thành công. |
| 156 | `AUDIT_LOGS_LISTED` | Tìm audit log theo đối tượng, người thực hiện, hành động và thời gian. thành công. |
| 157 | `ADMIN_AUDIT_LOGS_RETRIEVED` | Xem chi tiết một bản ghi audit. thành công. |

## Shared errors

| Code | HTTP | Meaning |
|---|---:|---|
| `REQUEST_REQUIRED` | 400 | Thiếu field bắt buộc. |
| `REQUEST_INVALID_FORMAT` | 400 | Sai kiểu/format/range/enum. |
| `METHOD_NOT_ALLOWED` | 405 | Sai HTTP method so với contract. |
| `AUTHENTICATION_REQUIRED` | 401 | Thiếu hoặc token không hợp lệ. |
| `ACCESS_DENIED` | 403 | Không đủ role/permission/scope. |
| `RESOURCE_NOT_FOUND` | 404 | Không tìm thấy hoặc ngoài scope. |
| `CONCURRENT_UPDATE_CONFLICT` | 409 | Optimistic lock/race conflict. |
| `IDEMPOTENCY_CONFLICT` | 409 | Cùng key, payload khác. |
| `BUSINESS_RULE_VIOLATION` | 422 | Không thỏa trạng thái/rule nghiệp vụ. |
| `RATE_LIMIT_EXCEEDED` | 429 | Vượt rate limit. |
| `DEPENDENCY_UNAVAILABLE` | 503 | Phụ thuộc ngoài tạm gián đoạn. |
| `INTERNAL_ERROR` | 500 | Lỗi hệ thống được che chi tiết. |
