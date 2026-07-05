# API Catalog

Tổng số: **105 API**.

| # | Code | Method | Endpoint | Tên API | Module | DD |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | CAT-HOME-001 | GET | `/api/v1/catalog/home` | Lấy dữ liệu trang giới thiệu Study | 01. Public Catalog | [DD](apis/catalog/CAT-HOME-001/README.md) |
| 2 | CAT-PATH-LIST-001 | GET | `/api/v1/catalog/learning-paths` | Tìm kiếm và lọc lộ trình công khai | 01. Public Catalog | [DD](apis/catalog/CAT-PATH-LIST-001/README.md) |
| 3 | CAT-PATH-DETAIL-001 | GET | `/api/v1/catalog/learning-paths/{slug}` | Xem chi tiết lộ trình công khai | 01. Public Catalog | [DD](apis/catalog/CAT-PATH-DETAIL-001/README.md) |
| 4 | CAT-COURSE-LIST-001 | GET | `/api/v1/catalog/courses` | Tìm kiếm và lọc khóa học công khai | 01. Public Catalog | [DD](apis/catalog/CAT-COURSE-LIST-001/README.md) |
| 5 | CAT-COURSE-DETAIL-001 | GET | `/api/v1/catalog/courses/{slug}` | Xem chi tiết khóa học công khai | 01. Public Catalog | [DD](apis/catalog/CAT-COURSE-DETAIL-001/README.md) |
| 6 | CAT-SAMPLE-001 | GET | `/api/v1/catalog/sample-lessons/{lessonId}` | Phát bài học mẫu | 01. Public Catalog | [DD](apis/catalog/CAT-SAMPLE-001/README.md) |
| 7 | CAT-SEARCH-001 | GET | `/api/v1/catalog/search` | Tìm kiếm đồng thời lộ trình và khóa học | 01. Public Catalog | [DD](apis/catalog/CAT-SEARCH-001/README.md) |
| 8 | AUTH-REGISTER-001 | POST | `/api/v1/auth/register` | Đăng ký tài khoản | 02. Tài khoản, xác thực và hồ sơ | [DD](apis/auth/AUTH-REGISTER-001/README.md) |
| 9 | AUTH-LOGIN-001 | POST | `/api/v1/auth/login` | Đăng nhập | 02. Tài khoản, xác thực và hồ sơ | [DD](apis/auth/AUTH-LOGIN-001/README.md) |
| 10 | AUTH-LOGOUT-001 | POST | `/api/v1/auth/logout` | Đăng xuất | 02. Tài khoản, xác thực và hồ sơ | [DD](apis/auth/AUTH-LOGOUT-001/README.md) |
| 11 | AUTH-REFRESH-001 | POST | `/api/v1/auth/refresh` | Làm mới access token | 02. Tài khoản, xác thực và hồ sơ | [DD](apis/auth/AUTH-REFRESH-001/README.md) |
| 12 | AUTH-VERIFY-001 | POST | `/api/v1/auth/verify-contact` | Xác thực email hoặc số điện thoại | 02. Tài khoản, xác thực và hồ sơ | [DD](apis/auth/AUTH-VERIFY-001/README.md) |
| 13 | AUTH-RESEND-001 | POST | `/api/v1/auth/resend-verification` | Gửi lại mã xác thực | 02. Tài khoản, xác thực và hồ sơ | [DD](apis/auth/AUTH-RESEND-001/README.md) |
| 14 | AUTH-ME-001 | GET | `/api/v1/users/me` | Lấy hồ sơ người dùng hiện tại | 02. Tài khoản, xác thực và hồ sơ | [DD](apis/auth/AUTH-ME-001/README.md) |
| 15 | AUTH-PROFILE-UPDATE-001 | PATCH | `/api/v1/users/me` | Cập nhật hồ sơ cá nhân | 02. Tài khoản, xác thực và hồ sơ | [DD](apis/auth/AUTH-PROFILE-UPDATE-001/README.md) |
| 16 | AUTH-PASSWORD-CHANGE-001 | POST | `/api/v1/auth/change-password` | Đổi mật khẩu | 02. Tài khoản, xác thực và hồ sơ | [DD](apis/auth/AUTH-PASSWORD-CHANGE-001/README.md) |
| 17 | AUTH-FORGOT-001 | POST | `/api/v1/auth/forgot-password` | Yêu cầu đặt lại mật khẩu | 02. Tài khoản, xác thực và hồ sơ | [DD](apis/auth/AUTH-FORGOT-001/README.md) |
| 18 | AUTH-RESET-001 | POST | `/api/v1/auth/reset-password` | Đặt lại mật khẩu | 02. Tài khoản, xác thực và hồ sơ | [DD](apis/auth/AUTH-RESET-001/README.md) |
| 19 | AUTH-DEACTIVATE-001 | POST | `/api/v1/users/me/deactivate` | Yêu cầu vô hiệu hóa tài khoản | 02. Tài khoản, xác thực và hồ sơ | [DD](apis/auth/AUTH-DEACTIVATE-001/README.md) |
| 20 | ONB-CURRENT-001 | GET | `/api/v1/onboarding/current` | Lấy phiên onboarding hiện tại | 03. Onboarding | [DD](apis/onboard/ONB-CURRENT-001/README.md) |
| 21 | ONB-DRAFT-001 | PATCH | `/api/v1/onboarding/draft` | Lưu nháp onboarding | 03. Onboarding | [DD](apis/onboard/ONB-DRAFT-001/README.md) |
| 22 | ONB-RECOMMEND-001 | GET | `/api/v1/onboarding/recommended-paths` | Lấy gợi ý lộ trình theo onboarding | 03. Onboarding | [DD](apis/onboard/ONB-RECOMMEND-001/README.md) |
| 23 | ONB-CONFIRM-001 | POST | `/api/v1/onboarding/confirm` | Xác nhận hoàn tất onboarding | 03. Onboarding | [DD](apis/onboard/ONB-CONFIRM-001/README.md) |
| 24 | ONB-STATUS-001 | GET | `/api/v1/onboarding/status` | Lấy trạng thái điều kiện trước khi học | 03. Onboarding | [DD](apis/onboard/ONB-STATUS-001/README.md) |
| 25 | LRN-MY-PATHS-001 | GET | `/api/v1/learning-paths/me` | Lấy lộ trình của learner | 04. Lộ trình học | [DD](apis/learn/LRN-MY-PATHS-001/README.md) |
| 26 | LRN-PATH-DETAIL-001 | GET | `/api/v1/learning-paths/{pathId}` | Lấy chi tiết lộ trình theo ngữ cảnh learner | 04. Lộ trình học | [DD](apis/learn/LRN-PATH-DETAIL-001/README.md) |
| 27 | LRN-ACTIVATE-001 | POST | `/api/v1/learning-paths/{pathId}/activate` | Kích hoạt lộ trình | 04. Lộ trình học | [DD](apis/learn/LRN-ACTIVATE-001/README.md) |
| 28 | LRN-PAUSE-001 | POST | `/api/v1/learning-paths/{pathId}/pause` | Tạm dừng lộ trình | 04. Lộ trình học | [DD](apis/learn/LRN-PAUSE-001/README.md) |
| 29 | LRN-RESUME-001 | POST | `/api/v1/learning-paths/{pathId}/resume` | Tiếp tục lộ trình | 04. Lộ trình học | [DD](apis/learn/LRN-RESUME-001/README.md) |
| 30 | LRN-COMPLETE-001 | POST | `/api/v1/learning-paths/{pathId}/complete` | Yêu cầu kiểm tra hoàn thành lộ trình | 04. Lộ trình học | [DD](apis/learn/LRN-COMPLETE-001/README.md) |
| 31 | LRN-ELIGIBILITY-001 | GET | `/api/v1/learning-paths/{pathId}/eligibility` | Kiểm tra khả năng kích hoạt lộ trình | 04. Lộ trình học | [DD](apis/learn/LRN-ELIGIBILITY-001/README.md) |
| 32 | CNT-COURSE-OUTLINE-001 | GET | `/api/v1/courses/{courseId}/outline` | Lấy outline khóa học theo learner | 05. Khóa học và nội dung học | [DD](apis/content/CNT-COURSE-OUTLINE-001/README.md) |
| 33 | CNT-LESSON-STUDY-001 | GET | `/api/v1/lessons/{lessonId}/study` | Mở phiên học bài học | 05. Khóa học và nội dung học | [DD](apis/content/CNT-LESSON-STUDY-001/README.md) |
| 34 | CNT-LESSON-RESOURCES-001 | GET | `/api/v1/lessons/{lessonId}/resources` | Lấy danh sách tài nguyên bài học | 05. Khóa học và nội dung học | [DD](apis/content/CNT-LESSON-RESOURCES-001/README.md) |
| 35 | CNT-RESOURCE-DOWNLOAD-001 | POST | `/api/v1/lesson-resources/{resourceId}/download-url` | Xin signed URL tải tài liệu | 05. Khóa học và nội dung học | [DD](apis/content/CNT-RESOURCE-DOWNLOAD-001/README.md) |
| 36 | CNT-BOOKMARK-001 | POST | `/api/v1/lessons/{lessonId}/bookmarks` | Tạo hoặc cập nhật bookmark bài học | 05. Khóa học và nội dung học | [DD](apis/content/CNT-BOOKMARK-001/README.md) |
| 37 | CNT-BOOKMARK-LIST-001 | GET | `/api/v1/bookmarks` | Lấy bookmark của learner | 05. Khóa học và nội dung học | [DD](apis/content/CNT-BOOKMARK-LIST-001/README.md) |
| 38 | EXE-DETAIL-001 | GET | `/api/v1/exercises/{exerciseId}` | Lấy đề bài theo quyền learner | 06. Bài tập và đánh giá | [DD](apis/exercise/EXE-DETAIL-001/README.md) |
| 39 | EXE-START-001 | POST | `/api/v1/exercises/{exerciseId}/attempts` | Bắt đầu lượt làm bài | 06. Bài tập và đánh giá | [DD](apis/exercise/EXE-START-001/README.md) |
| 40 | EXE-SUBMIT-001 | POST | `/api/v1/exercises/{exerciseId}/submissions` | Nộp bài | 06. Bài tập và đánh giá | [DD](apis/exercise/EXE-SUBMIT-001/README.md) |
| 41 | EXE-ATTEMPT-LIST-001 | GET | `/api/v1/exercises/{exerciseId}/attempts` | Lấy lịch sử lượt làm của learner | 06. Bài tập và đánh giá | [DD](apis/exercise/EXE-ATTEMPT-LIST-001/README.md) |
| 42 | EXE-ATTEMPT-DETAIL-001 | GET | `/api/v1/exercise-attempts/{attemptId}` | Lấy chi tiết lượt làm | 06. Bài tập và đánh giá | [DD](apis/exercise/EXE-ATTEMPT-DETAIL-001/README.md) |
| 43 | EXE-SUBMISSION-DETAIL-001 | GET | `/api/v1/exercise-submissions/{submissionId}` | Lấy chi tiết bài nộp | 06. Bài tập và đánh giá | [DD](apis/exercise/EXE-SUBMISSION-DETAIL-001/README.md) |
| 44 | EXE-RETAKE-001 | GET | `/api/v1/exercises/{exerciseId}/retake-eligibility` | Kiểm tra quyền nộp lại | 06. Bài tập và đánh giá | [DD](apis/exercise/EXE-RETAKE-001/README.md) |
| 45 | EXE-REVIEW-001 | PATCH | `/api/v1/admin/exercise-submissions/{submissionId}/review` | Chấm hoặc phản hồi thủ công | 06. Bài tập và đánh giá | [DD](apis/exercise/EXE-REVIEW-001/README.md) |
| 46 | PRG-SUMMARY-001 | GET | `/api/v1/progress/summary` | Lấy tổng quan tiến độ | 07. Tiến độ và hoàn thành | [DD](apis/progress/PRG-SUMMARY-001/README.md) |
| 47 | PRG-PATH-001 | GET | `/api/v1/progress/learning-paths/{pathId}` | Lấy tiến độ theo lộ trình | 07. Tiến độ và hoàn thành | [DD](apis/progress/PRG-PATH-001/README.md) |
| 48 | PRG-COURSE-001 | GET | `/api/v1/progress/courses/{courseId}` | Lấy tiến độ theo khóa học | 07. Tiến độ và hoàn thành | [DD](apis/progress/PRG-COURSE-001/README.md) |
| 49 | PRG-LESSON-UPDATE-001 | PATCH | `/api/v1/lessons/{lessonId}/progress` | Cập nhật sự kiện tiến độ bài học | 07. Tiến độ và hoàn thành | [DD](apis/progress/PRG-LESSON-UPDATE-001/README.md) |
| 50 | PRG-ACTIVITY-001 | GET | `/api/v1/progress/activity` | Lấy lịch sử hoạt động học | 07. Tiến độ và hoàn thành | [DD](apis/progress/PRG-ACTIVITY-001/README.md) |
| 51 | PRG-DASHBOARD-001 | GET | `/api/v1/learner/dashboard` | Lấy dữ liệu dashboard learner | 07. Tiến độ và hoàn thành | [DD](apis/progress/PRG-DASHBOARD-001/README.md) |
| 52 | PRG-RECALC-001 | POST | `/internal/progress/recalculate` | Tính lại tiến độ nội bộ | 07. Tiến độ và hoàn thành | [DD](apis/progress/PRG-RECALC-001/README.md) |
| 53 | COM-GROUP-LIST-001 | GET | `/api/v1/community-groups` | Lấy danh sách nhóm cộng đồng phù hợp learner | 08. Cộng đồng Zalo | [DD](apis/community/COM-GROUP-LIST-001/README.md) |
| 54 | COM-GROUP-DETAIL-001 | GET | `/api/v1/community-groups/{groupId}` | Lấy chi tiết nhóm cộng đồng | 08. Cộng đồng Zalo | [DD](apis/community/COM-GROUP-DETAIL-001/README.md) |
| 55 | COM-OPEN-LINK-001 | POST | `/api/v1/community-groups/{groupId}/open-link` | Tạo phiên mở link Zalo | 08. Cộng đồng Zalo | [DD](apis/community/COM-OPEN-LINK-001/README.md) |
| 56 | COM-REPORT-001 | POST | `/api/v1/community-groups/{groupId}/reports` | Báo cáo nhóm hoặc link cộng đồng | 08. Cộng đồng Zalo | [DD](apis/community/COM-REPORT-001/README.md) |
| 57 | COM-MY-ACCESS-001 | GET | `/api/v1/community-groups/my-access` | Lấy phạm vi nhóm learner được xem | 08. Cộng đồng Zalo | [DD](apis/community/COM-MY-ACCESS-001/README.md) |
| 58 | COM-ADMIN-LIST-001 | GET | `/api/v1/admin/community-groups` | Danh sách quản trị nhóm | 08. Cộng đồng Zalo | [DD](apis/community/COM-ADMIN-LIST-001/README.md) |
| 59 | COM-ADMIN-CREATE-001 | POST | `/api/v1/admin/community-groups` | Tạo nhóm cộng đồng | 08. Cộng đồng Zalo | [DD](apis/community/COM-ADMIN-CREATE-001/README.md) |
| 60 | COM-ADMIN-UPDATE-001 | PATCH | `/api/v1/admin/community-groups/{groupId}` | Cập nhật nhóm cộng đồng | 08. Cộng đồng Zalo | [DD](apis/community/COM-ADMIN-UPDATE-001/README.md) |
| 61 | COM-ADMIN-ARCHIVE-001 | POST | `/api/v1/admin/community-groups/{groupId}/archive` | Lưu trữ nhóm cộng đồng | 08. Cộng đồng Zalo | [DD](apis/community/COM-ADMIN-ARCHIVE-001/README.md) |
| 62 | NOTI-LIST-001 | GET | `/api/v1/notifications` | Lấy thông báo của người dùng | 09. Thông báo nghiệp vụ | [DD](apis/notification/NOTI-LIST-001/README.md) |
| 63 | NOTI-DETAIL-001 | GET | `/api/v1/notifications/{notificationId}` | Lấy chi tiết thông báo | 09. Thông báo nghiệp vụ | [DD](apis/notification/NOTI-DETAIL-001/README.md) |
| 64 | NOTI-MARK-READ-001 | PATCH | `/api/v1/notifications/{notificationId}/read` | Đánh dấu thông báo đã đọc | 09. Thông báo nghiệp vụ | [DD](apis/notification/NOTI-MARK-READ-001/README.md) |
| 65 | NOTI-MARK-ALL-001 | POST | `/api/v1/notifications/mark-all-read` | Đánh dấu tất cả đã đọc | 09. Thông báo nghiệp vụ | [DD](apis/notification/NOTI-MARK-ALL-001/README.md) |
| 66 | NOTI-SETTINGS-GET-001 | GET | `/api/v1/notification-settings/me` | Lấy thiết lập nhận thông báo | 09. Thông báo nghiệp vụ | [DD](apis/notification/NOTI-SETTINGS-GET-001/README.md) |
| 67 | NOTI-SETTINGS-PUT-001 | PUT | `/api/v1/notification-settings/me` | Cập nhật thiết lập nhận thông báo | 09. Thông báo nghiệp vụ | [DD](apis/notification/NOTI-SETTINGS-PUT-001/README.md) |
| 68 | NOTI-ADMIN-LIST-001 | GET | `/api/v1/admin/notifications` | Danh sách thông báo quản trị | 09. Thông báo nghiệp vụ | [DD](apis/notification/NOTI-ADMIN-LIST-001/README.md) |
| 69 | NOTI-ADMIN-CREATE-001 | POST | `/api/v1/admin/notifications` | Tạo thông báo nháp | 09. Thông báo nghiệp vụ | [DD](apis/notification/NOTI-ADMIN-CREATE-001/README.md) |
| 70 | NOTI-ADMIN-SEND-001 | POST | `/api/v1/admin/notifications/{notificationId}/send` | Gửi thông báo | 09. Thông báo nghiệp vụ | [DD](apis/notification/NOTI-ADMIN-SEND-001/README.md) |
| 71 | NOTI-ADMIN-ARCHIVE-001 | POST | `/api/v1/admin/notifications/{notificationId}/archive` | Lưu trữ thông báo | 09. Thông báo nghiệp vụ | [DD](apis/notification/NOTI-ADMIN-ARCHIVE-001/README.md) |
| 72 | ADM-CONTENT-LIST-001 | GET | `/api/v1/admin/content/{contentType}` | Danh sách nội dung quản trị | 10. Admin quản trị nội dung | [DD](apis/admincontent/ADM-CONTENT-LIST-001/README.md) |
| 73 | ADM-CONTENT-CREATE-001 | POST | `/api/v1/admin/content/{contentType}` | Tạo nội dung nháp | 10. Admin quản trị nội dung | [DD](apis/admincontent/ADM-CONTENT-CREATE-001/README.md) |
| 74 | ADM-CONTENT-DETAIL-001 | GET | `/api/v1/admin/content/{contentType}/{contentId}` | Lấy chi tiết nội dung quản trị | 10. Admin quản trị nội dung | [DD](apis/admincontent/ADM-CONTENT-DETAIL-001/README.md) |
| 75 | ADM-CONTENT-UPDATE-001 | PUT | `/api/v1/admin/content/{contentType}/{contentId}` | Cập nhật nội dung | 10. Admin quản trị nội dung | [DD](apis/admincontent/ADM-CONTENT-UPDATE-001/README.md) |
| 76 | ADM-CONTENT-ARCHIVE-001 | POST | `/api/v1/admin/content/{contentType}/{contentId}/archive` | Lưu trữ nội dung | 10. Admin quản trị nội dung | [DD](apis/admincontent/ADM-CONTENT-ARCHIVE-001/README.md) |
| 77 | ADM-CONTENT-CHECK-001 | POST | `/api/v1/admin/content/{contentType}/{contentId}/pre-publish-check` | Kiểm tra trước khi publish | 10. Admin quản trị nội dung | [DD](apis/admincontent/ADM-CONTENT-CHECK-001/README.md) |
| 78 | ADM-CONTENT-PUBLISH-001 | POST | `/api/v1/admin/content/{contentType}/{contentId}/publish` | Publish nội dung | 10. Admin quản trị nội dung | [DD](apis/admincontent/ADM-CONTENT-PUBLISH-001/README.md) |
| 79 | ADM-CONTENT-UNPUBLISH-001 | POST | `/api/v1/admin/content/{contentType}/{contentId}/unpublish` | Gỡ publish nội dung | 10. Admin quản trị nội dung | [DD](apis/admincontent/ADM-CONTENT-UNPUBLISH-001/README.md) |
| 80 | ADM-CONTENT-VERSIONS-001 | GET | `/api/v1/admin/content/{contentType}/{contentId}/versions` | Lấy lịch sử phiên bản nội dung | 10. Admin quản trị nội dung | [DD](apis/admincontent/ADM-CONTENT-VERSIONS-001/README.md) |
| 81 | ADM-CONTENT-RESTORE-001 | POST | `/api/v1/admin/content/{contentType}/{contentId}/restore-version` | Khôi phục phiên bản nội dung | 10. Admin quản trị nội dung | [DD](apis/admincontent/ADM-CONTENT-RESTORE-001/README.md) |
| 82 | ADM-CONTENT-REORDER-001 | PATCH | `/api/v1/admin/content/{contentType}/{contentId}/ordering` | Sắp xếp nội dung con | 10. Admin quản trị nội dung | [DD](apis/admincontent/ADM-CONTENT-REORDER-001/README.md) |
| 83 | SUP-MY-LIST-001 | GET | `/api/v1/support-requests` | Lấy yêu cầu hỗ trợ của learner | 11. Admin học viên, hỗ trợ và ngoại lệ | [DD](apis/support/SUP-MY-LIST-001/README.md) |
| 84 | SUP-CREATE-001 | POST | `/api/v1/support-requests` | Tạo yêu cầu hỗ trợ | 11. Admin học viên, hỗ trợ và ngoại lệ | [DD](apis/support/SUP-CREATE-001/README.md) |
| 85 | SUP-DETAIL-001 | GET | `/api/v1/support-requests/{requestId}` | Lấy chi tiết ticket hỗ trợ | 11. Admin học viên, hỗ trợ và ngoại lệ | [DD](apis/support/SUP-DETAIL-001/README.md) |
| 86 | SUP-COMMENT-001 | POST | `/api/v1/support-requests/{requestId}/comments` | Bổ sung trao đổi cho ticket | 11. Admin học viên, hỗ trợ và ngoại lệ | [DD](apis/support/SUP-COMMENT-001/README.md) |
| 87 | SUP-CLOSE-001 | POST | `/api/v1/support-requests/{requestId}/close` | Learner đóng ticket | 11. Admin học viên, hỗ trợ và ngoại lệ | [DD](apis/support/SUP-CLOSE-001/README.md) |
| 88 | SUP-ADMIN-LIST-001 | GET | `/api/v1/admin/support-requests` | Danh sách ticket cho staff | 11. Admin học viên, hỗ trợ và ngoại lệ | [DD](apis/support/SUP-ADMIN-LIST-001/README.md) |
| 89 | SUP-ADMIN-PROFILE-001 | GET | `/api/v1/admin/learners/{learnerId}/support-profile` | Lấy support profile học viên | 11. Admin học viên, hỗ trợ và ngoại lệ | [DD](apis/support/SUP-ADMIN-PROFILE-001/README.md) |
| 90 | SUP-ADMIN-NOTE-001 | POST | `/api/v1/admin/support-requests/{requestId}/notes` | Thêm ghi chú nội bộ | 11. Admin học viên, hỗ trợ và ngoại lệ | [DD](apis/support/SUP-ADMIN-NOTE-001/README.md) |
| 91 | SUP-ADMIN-RESOLVE-001 | POST | `/api/v1/admin/support-requests/{requestId}/resolve` | Giải quyết ticket | 11. Admin học viên, hỗ trợ và ngoại lệ | [DD](apis/support/SUP-ADMIN-RESOLVE-001/README.md) |
| 92 | SUP-EXCEPTION-DECIDE-001 | POST | `/api/v1/admin/learner-path-exceptions/{exceptionId}/decision` | Duyệt hoặc từ chối ngoại lệ lộ trình | 11. Admin học viên, hỗ trợ và ngoại lệ | [DD](apis/support/SUP-EXCEPTION-DECIDE-001/README.md) |
| 93 | SUP-EXCEPTION-CREATE-001 | POST | `/api/v1/admin/learner-path-exceptions` | Tạo yêu cầu ngoại lệ lộ trình | 11. Admin học viên, hỗ trợ và ngoại lệ | [DD](apis/support/SUP-EXCEPTION-CREATE-001/README.md) |
| 94 | RPT-OVERVIEW-001 | GET | `/api/v1/admin/reports/overview` | Lấy báo cáo vận hành tổng quan | 12. Báo cáo vận hành | [DD](apis/report/RPT-OVERVIEW-001/README.md) |
| 95 | RPT-ALERTS-001 | GET | `/api/v1/admin/reports/alerts` | Lấy cảnh báo vận hành | 12. Báo cáo vận hành | [DD](apis/report/RPT-ALERTS-001/README.md) |
| 96 | RPT-EXPORT-001 | POST | `/api/v1/admin/reports/exports` | Tạo job xuất báo cáo | 12. Báo cáo vận hành | [DD](apis/report/RPT-EXPORT-001/README.md) |
| 97 | RPT-EXPORT-STATUS-001 | GET | `/api/v1/admin/reports/exports/{jobId}` | Lấy trạng thái job xuất báo cáo | 12. Báo cáo vận hành | [DD](apis/report/RPT-EXPORT-STATUS-001/README.md) |
| 98 | RBA-ROLE-LIST-001 | GET | `/api/v1/admin/roles` | Lấy danh sách vai trò | 13. RBAC và Audit | [DD](apis/rbac/RBA-ROLE-LIST-001/README.md) |
| 99 | RBA-PERMISSION-LIST-001 | GET | `/api/v1/admin/permissions` | Lấy danh sách quyền | 13. RBAC và Audit | [DD](apis/rbac/RBA-PERMISSION-LIST-001/README.md) |
| 100 | RBA-USER-ROLES-001 | GET | `/api/v1/admin/users/{userId}/roles` | Lấy role của người dùng | 13. RBAC và Audit | [DD](apis/rbac/RBA-USER-ROLES-001/README.md) |
| 101 | RBA-ROLE-ASSIGN-001 | POST | `/api/v1/admin/users/{userId}/roles` | Gán role cho người dùng | 13. RBAC và Audit | [DD](apis/rbac/RBA-ROLE-ASSIGN-001/README.md) |
| 102 | RBA-ROLE-REVOKE-001 | DELETE | `/api/v1/admin/users/{userId}/roles/{roleId}` | Thu hồi role của người dùng | 13. RBAC và Audit | [DD](apis/rbac/RBA-ROLE-REVOKE-001/README.md) |
| 103 | RBA-ROLE-PERMISSIONS-001 | PUT | `/api/v1/admin/roles/{roleId}/permissions` | Cập nhật quyền của role | 13. RBAC và Audit | [DD](apis/rbac/RBA-ROLE-PERMISSIONS-001/README.md) |
| 104 | RBA-AUDIT-LIST-001 | GET | `/api/v1/admin/audit-logs` | Tra cứu audit log | 13. RBAC và Audit | [DD](apis/rbac/RBA-AUDIT-LIST-001/README.md) |
| 105 | RBA-AUDIT-DETAIL-001 | GET | `/api/v1/admin/audit-logs/{auditId}` | Lấy chi tiết audit log | 13. RBAC và Audit | [DD](apis/rbac/RBA-AUDIT-DETAIL-001/README.md) |
