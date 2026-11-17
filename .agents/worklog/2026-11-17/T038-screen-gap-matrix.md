# T038 — Study screen source gap matrix

> Snapshot generated 2026-11-17 from the 83-ID screen index/inventory, current Angular feature folders/routes/callers and Study Server `app/api/v1.py` route comments. Server status `R` means numbered route plus focused test source was found, `P` means route/module source exists without a focused test package, `S` marks the #02 email-delivery stub, and `D` means no numbered route source was found. FE structure/caller columns are source inventories only; they do not prove screen acceptance, deployment or live runtime. A route metadata dependency is not an HTTP caller; the FE caller column records page-invoked feature request methods, not merely a service wrapper.

| ID | Screen | Surface | Current FE structure | Assigned API IDs | Server source | FE caller |
|---|---|---|---|---|---|---|
| SH-01 | Trang giới thiệu Study | Page | route+page | #5,#6 | #5 R,#6 R | #5,#6 |
| SH-02 | Đăng nhập | Page | route+page | #3,#4 | #3 R,#4 R | — |
| SH-03 | Đăng ký học viên | Page | route+page | #1 | #1 R | #1 |
| SH-04 | Handoff xác thực email | Page | route+page | #2 | #2 S | — |
| SH-05 | Không đủ quyền / session hết hạn | State view | page only | #4 | #4 R | — |
| SH-06 | Trang không tồn tại / tài nguyên không còn | State view | route+page | #8 | #8 R | — |
| SH-07 | Theo dõi tác vụ bất đồng bộ | Panel | route+page | #18 | #18 R | — |
| GS-01 | Danh sách khóa học | Page | route+page | #5,#6 | #5 R,#6 R | #5,#6 |
| GS-02 | Tìm kiếm khóa học | Page | route+page | #5,#7 | #5 R,#7 R | #7 |
| GS-03 | Chi tiết khóa học | Page | route+page | #8,#9,#10 | #8 R,#9 R,#10 R | #8,#9 |
| GS-04 | Đề cương khóa học | Tab | parent tab | #9 | #9 R | #9 |
| GS-05 | Đánh giá và thảo luận công khai | Tab | parent tab | #8,#10 | #8 R,#10 R | #10 |
| GS-06 | Tài nguyên khóa học | Tab | parent tab | #11,#12 | #11 R,#12 R | — |
| GS-07 | Xem/tải tài nguyên | Page | route+page | #12 | #12 R | — |
| ST-01 | Tổng quan học viên | Page | route+page (dashboard widgets) | #20,#21,#38,#43 | #20 P,#21 R (UserProfile mismatch),#38 P,#43 P/SOURCE_ONLY | #20 active courses + #38 awards; #21/#43 not called |
| ST-02 | Hồ sơ cá nhân | Page | route+page | #4 | #4 R | — |
| ST-03 | Chỉnh sửa hồ sơ/avatar | Page | route+page (gate-only) | #4,#13,#14 | #4 R,#13 R,#14 R | — |
| ST-04 | Kiểm tra ghi danh trước đăng ký | Page | route+page (partial; gate-only enrollment) | #8,#15 | #8 R,#15 R (unsafe optional-token fallback) | #8 |
| ST-05 | Kiểm tra đơn hàng / checkout | Page | route+page (partial; order gate) | #8,#16 | #8 R,#16 R (DDL missing; no focused tests) | #8 |
| ST-06 | Thực hiện thanh toán | Page | route+page (payment gate) | #17,#18 | #17 P (503 fail-closed),#18 R (notification-only) | — |
| ST-07 | Kết quả đăng ký khóa học | Page | route+page (result gate) | #18,#19,#20 | #18 R (notification-only),#19 P (orders DDL absent),#20 P (local CourseSummary projection) | — |
| ST-08 | Khóa học của tôi | Page | route+page (API-backed course list) | #20,#21 | #20 P (local CourseSummary projection),#21 R (UserProfile projection) | #20 paged course list; #21 not called |
| ST-09 | Tổng quan khóa đang học | Page | route+page (enrollment + progress gate) | #9,#20,#37 | #9 R (public curriculum),#20 P (CourseSummary),#37 P (CourseProgress) | #20 ACTIVE membership pagination → #37; #9 not called |
| ST-10 | Kiểm tra quyền và bắt đầu học | Transition | route+page (access/start handoff) | #22,#23,#24 | #22 R,#23 R,#24 R (focused tests present) | #22 access → explicit #23 if PUBLISHED; #24 is called by ST-11 |
| ST-11 | Trình học bài/lesson player | Page | route+page (source-wired) | #24,#25,#26,#27 | #24 R,#25 R,#26 R,#27 R | #24 |
| ST-12 | Tài liệu kèm bài học | Panel | route+page (source-wired) | #12,#26 | #12 R,#26 R | #26 |
| ST-13 | Giới thiệu bài kiểm tra | Page | route+page (partial/gated) | #28,#29 | #28 R,#29 R | #28,#29 |
| ST-14 | Làm bài kiểm tra | Page | route+page (partial/gated) | #28,#29,#30 | #28 R,#29 R,#30 R | #28,#30 |
| ST-15 | Xác nhận nộp bài kiểm tra | Dialog | route+page (partial/gated) | #30,#31 | #30 R,#31 P | #31 |
| ST-16 | Kết quả bài kiểm tra | Page | route+page (source-wired) | #32 | #32 R | #32 |
| ST-17 | Chi tiết bài tập | Page | route+page (source-wired) | #33 | #33 R | #33 |
| ST-18 | Soạn và nộp bài tập | Page | route+page (partial/gated) | #33,#34,#35 | #33 R,#34 R (Shared),#35 P | #33,#34,#35 |
| ST-19 | Bài đã nộp và phản hồi | Page | route+page (source-wired) | #36 | #36 P | #36 |
| ST-20 | Tổng quan tiến độ | Page | route+page (partial/gated) | #21,#38 | #21 R,#38 P | #38 |
| ST-21 | Tiến độ theo khóa học | Page | route+page (partial/gated) | #37 | #37 P | #37 |
| ST-22 | Thành tích và chứng nhận | Page | route+page (source-wired) | #38 | #38 P | #38 |
| ST-23 | Danh sách thảo luận | Page | route+page (source-wired) | #39 | #39 P | #39 |
| ST-24 | Tạo câu hỏi / chủ đề | Page | route+page (partial/gated) | #39,#40 | #20 P,#39 P,#40 P | #20,#39,#40 |
| ST-25 | Chi tiết thread và phản hồi | Page | route+page (source-wired) | #41,#42 | #41 P,#42 P | #41,#42 |
| ST-26 | Thông báo học viên | Page | route+page (partial/gated) | #43,#44,#45 | #43 P,#44 P,#45 P (DDL dependency absent) | — |
| ME-01 | Dashboard mentor | Page | route+page (partial/gated actions) | #46,#54,#58 | #46 R,#54 R,#58 R | #46,#54,#58 |
| ME-02 | Các khóa học phụ trách | Page | route+page (partial/gated actions) | #46 | #46 R | #46 |
| ME-03 | Workspace khóa học của mentor | Page | route+page (partial/gated actions) | #49,#65 | #46 R,#49 R,#65 R | #46,#49,#65 |
| ME-04 | Tải lên và tạo bài giảng | Page | route+page (partial/gated actions) | #34,#46,#47 | #34 R (Shared),#46 R,#47 R | #46 |
| ME-05 | Xem bài giảng mentor | Page | route+page (partial/gated actions) | #48 | #48 R | #48 |
| ME-06 | Cây nội dung khóa học | Page | route+page (partial/gated actions) | #49 | #49 R | #49 |
| ME-07 | Tạo/chỉnh sửa nội dung | Page | route+page (partial/gated actions) | #49,#50,#51 | #49 R,#50 R,#51 R | #49,#50,#51 |
| ME-08 | Xuất bản/xóa nội dung | Dialog | route+page (partial/gated actions) | #49,#52,#53 | #49 R,#52 R,#53 R | #49,#52,#53 |
| ME-09 | Danh sách bài cần chấm | Page | route+page (partial/gated actions) | #54 | #54 R | #54 |
| ME-10 | Chấm điểm và phản hồi | Page | route+page (partial/gated actions) | #55,#56,#57 | #55 R,#56 R,#57 R | #55,#56,#57 |
| ME-11 | Hộp thư hỗ trợ học viên | Page | route+page (partial/gated actions) | #58 | #58 R | #58 |
| ME-12 | Trao đổi và đóng yêu cầu | Page | route+page (partial/gated actions) | #59,#60,#61 | #59 R,#60 R,#61 R | #59,#60,#61 |
| ME-13 | Chọn người nhận thông báo | Step | route+page (partial/gated actions) | #46,#62 | #46 R,#62 R | #46,#62 |
| ME-14 | Soạn thông báo mentor | Page | route+page (partial/gated actions) | #62,#63 | #62 R,#63 R | — |
| ME-15 | Theo dõi gửi thông báo | Page | route+page (partial/gated actions) | #18,#64 | #64 R | #64 |
| ME-16 | Tiến độ toàn khóa học | Page | route+page (partial/gated actions) | #65 | #65 R | #65 |
| ME-17 | Tiến độ từng học viên | Page | route+page (partial/gated actions) | #67 | #67 R | #67 |
| ME-18 | Analytics khóa học | Page | route+page (partial/gated actions) | #66 | #66 R | #66 |
| AD-01 | Dashboard quản trị | Page | route+page | #101 | #101 D | — |
| AD-02 | Danh sách người dùng | Page | route+page | #68 | #68 R | #68 |
| AD-03 | Chi tiết người dùng | Page | route+page | #69 | #69 R | #69 |
| AD-04 | Chỉnh sửa người dùng | Page | route+page | #69,#70 | #69 R,#70 R | #69 |
| AD-05 | Khóa/mở khóa/xóa tài khoản | Dialog | route+page | #69,#71,#72 | #69 R,#71 R,#72 R | #69 |
| AD-06 | Danh sách khóa học quản trị | Page | route+page | #73 | #73 R | #73 |
| AD-07 | Chi tiết khóa học quản trị | Page | route+page | #74 | #74 R | #74 |
| AD-08 | Chỉnh sửa khóa học | Page | route+page | #74,#75 | #74 R,#75 R | #74 |
| AD-09 | Thay đổi trạng thái/xóa khóa | Dialog | route+page | #74,#76,#77 | #74 R,#76 R,#77 R | #74 |
| AD-10 | Hàng đợi kiểm duyệt nội dung | Page | route+page | #78 | #78 R | #78 |
| AD-11 | Duyệt/từ chối nội dung | Page | route+page | #79,#80,#81 | #79 R,#80 R,#81 R | #79 |
| AD-12 | Danh sách bài học quản trị | Page | route+page | #82 | #82 R | #82 |
| AD-13 | Chi tiết bài học quản trị | Page | route+page | #83 | #83 R | #83 |
| AD-14 | Sửa, đổi trạng thái, xóa bài học | Page | route+page | #83,#84,#85,#86 | #83 R,#84 R,#85 R,#86 R | #83 |
| AD-15 | Danh sách bài kiểm tra | Page | route+page | #87 | #87 R | #87 |
| AD-16 | Tạo/chỉnh sửa quiz | Page | route+page | #88,#89 | #88 R,#89 R | — |
| AD-17 | Thống kê bài kiểm tra | Page | route+page | #91 | #91 R | #91 |
| AD-18 | Xác nhận xóa bài kiểm tra | Dialog | route+page | #90 | #90 R | — |
| AD-19 | Danh sách thông báo quản trị | Page | route+page | #92 | #92 R | #92 |
| AD-20 | Soạn/gửi thông báo hệ thống | Page | route+page | #93 | #93 R | — |
| AD-21 | Sửa/kiểm soát/đo trạng thái thông báo | Page | route+page | #18,#94,#95,#96 | #18 R,#94 R,#95 R,#96 R | #96 |
| AD-22 | Danh sách thảo luận bị báo cáo | Page | route+page | #97 | #97 R | #97 |
| AD-23 | Điều tra/kiểm duyệt thảo luận | Page | route+page | #98,#99,#100 | #98 R,#99 D,#100 D | #98 |
| AD-24 | Báo cáo tác động cộng đồng | Page | route+page | #101,#102 | #101 D,#102 D | — |
| AD-25 | Xuất báo cáo và theo dõi tiến trình | Trang | route+page | #18,#103 | #18 R,#103 D | — |

## Structural counts

- `route+page`: 79 (including partial/gated Student and Mentor routes/pages)
- `parent tab`: 3
- `page only`: 1
- `not started`: 0

## Known sources of incompleteness

- SH-05 has a page component but no route; error-context and session recovery policy remain unresolved.
- StudentLayout now establishes a Student-only session through API #03 and keeps tokens in tab memory. ST-01 calls #20/#38 independently; #21 returns UserProfile and #43 is SOURCE_ONLY. ST-08 calls paged #20. ST-09 paginates #20 with `status=ACTIVE` before #37 and leaves public #09 unused because it cannot prove entitlement or provide the safe learning tree. ST-10 calls #22 at entry and explicit #23 only when the returned lesson is PUBLISHED; ST-11 calls #24 after navigation. `DISCREPANCY`: #22 does not filter lesson status and #23 lacks a publication predicate. ST-02/ST-03 remain gate-only. ST-04 calls public #08 then keeps unsafe #15 gated; ST-05 calls #08 then keeps #16 gated because `orders` is absent from checked-in DDL. ST-06 payment and ST-07 result remain gated.
- ST-11–ST-25 have source-local API request callers for bounded behaviors; ST-26 has route metadata but no request because #43–#45 are SOURCE_ONLY and depend on a missing checked-in notification_recipients relation. #31 and #35–#45 have route/module source without focused server test packages; do not treat local build or route metadata as API/runtime verification.
- ME-01–ME-18 now have Mentor routes/pages, API-ID metadata and screen-local callers for source-supported behavior. ME-04 upload/lecture creation and ME-14 notification dispatch remain gated; ME-07 uses current #50/#51 request fields and ME-08 actions are explicit and server-validated. Local focused server tests exist for #46–#67, but live schema/deployment and authenticated browser behavior remain unverified.
- Admin and Guest structures/callers vary. Existing read-only callers do not close unresolved mutation, permission, response projection, live schema or visual runtime gates.
- Screen-specific DD and Stitch assets remain present in their indexed packages; page/route counts do not prove implementation matches those artifacts.
