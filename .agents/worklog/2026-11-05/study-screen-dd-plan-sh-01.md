---
task_id: "2026-11-05-study-screen-dd-plan-sh-01"
date: "2026-11-05"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["SH-01 giao diện đề xuất -> Study API #05 danh mục và #06 khóa học"]
status: "PARTIAL"
---

# Nhật ký công việc: Đọc tham chiếu giao diện Study và lập tài liệu SH-01

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- Lệnh chọn worklog: /home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/select-worklogs.mjs --type docs --limit 3
- Các worklog đã đọc:
  - .agents/worklog/2026-11-05/check-study-screen-stitch-coverage.md
    - Ghi nhận: có 83 Screen ID duy nhất; ảnh/code nguồn là đầu vào thiết kế, không chứng minh hành vi khi chạy; trước đó chưa có ảnh chú thích/tài liệu chi tiết theo ID.
  - .agents/worklog/2026-11-05/load-study2work-context.md
    - Ghi nhận: thiếu mã nguồn Study Web và context triển khai theo phạm vi; giữ ranh giới này, không khẳng định route/khi chạy.
  - .agents/worklog/2026-11-05/organize-study-screen-stitch.md
    - Ghi nhận: tài sản hiện có được giữ nguyên khi sắp xếp; không gán thứ tự cho biến thể nếu thiếu bằng chứng.
- Thiếu worklog: không.

## EXPECTED_BEHAVIOR

- Yêu cầu: Đọc apps/study-client/docs/screen_stitch/90_reference/study2work-lms-design-system/DESIGN.md và apps/study-client/docs/list_screen.md; tiếp tục mục tiêu tạo kế hoạch DD chi tiết có căn cứ nguồn và một bộ tài liệu màn hình mỗi phiên.
- Hợp đồng chuẩn/DD được duyệt: list_screen.md định nghĩa 83 Screen ID ổn định, route đề xuất, API tham chiếu, điều hướng, trạng thái, luồng F01–F13, điều kiện chặn và cấu trúc DD 12 phần. .agents/web-study/design.md là chuẩn giao diện Study; DESIGN.md được yêu cầu chỉ là tham khảo.

## CURRENT_BEHAVIOR

- Mã nguồn/cấu hình: apps/study-client/src không tồn tại trong bản làm việc này. screen_stitch hiện có 83 PNG và 83 HTML. README mô tả hai biến thể SH-01, nhưng hệ thống tệp hiện chỉ có SH-01_trang-gioi-thieu-study__variant-1/.
- Kiểm thử có thể chạy: đã đọc mã nguồn kiểm thử API #05/#06 trong bước chuẩn bị; không chạy kiểm thử trong tác vụ tài liệu.
- Nối khi chạy: apps/study-server/app/api/v1.py nối GET /api/v1/categories và GET /api/v1/courses. Điều này chỉ chứng minh route/mã nguồn; không chứng minh DB trực tiếp hay triển khai. Mã nguồn hiện trả danh mục ACTIVE theo locale và khóa học PUBLISHED; bộ lọc category của #06 bị từ chối 422.

## SOURCE_TRACE

~~~text
route / đề xuất (thiếu triển khai Study Web)
  -> GET công khai #05 danh mục và #06 khóa học độc lập
  -> kiểm tra/truy vấn/ánh xạ trong apps/study-server/app/modules/guest/api_05_categories và api_06_courses
  -> các dòng danh mục ACTIVE / khóa học PUBLISHED có phần thông tin người hướng dẫn
  -> DTO phản hồi + mã kiểm thử nguồn (phiên này không chạy kiểm thử)
~~~

## DISCREPANCIES_AND_STATUSES

| Hạng mục | Bằng chứng | Trạng thái | Ảnh hưởng |
|---|---|---|---|
| Runtime Study Web | Có .agents/web-study/design.md nhưng thiếu apps/study-client/src | UNWIRED | Route và tương tác UI vẫn là đề xuất thiết kế. |
| Danh mục biến thể SH-01 | screen_stitch/README.md ghi biến thể 1 và biến thể 2; find chỉ thấy biến thể 1 | DISCREPANCY | Không tạo/khôi phục bản gốc không có; chỉ chú thích tài sản đang có và ghi thiếu biến thể. |
| Ảnh SH-01 so với HTML | Ảnh có danh mục, sáu thẻ khóa học, lợi ích/lời chứng thực/logo/email/chân trang; HTML nhỏ hơn, có hai thẻ khóa học mẫu viết cứng và liên kết neo | DISCREPANCY | Coi là hai bản mẫu không tương đương; nội dung mẫu/liên kết không phải bằng chứng khi chạy/API. |
| Thẩm quyền tham chiếu giao diện | Màu YAML DESIGN.md khác văn xuôi; hướng dẫn Study/list_screen dùng màu biển và điều khiển >=44px | DISCREPANCY | Giữ nguyên ảnh làm bằng chứng; ghi khoảng cách giao diện, không âm thầm đổi token. |
| API #05/#06 | Có route/module/mã kiểm thử nguồn; tham số category gửi tới #06 bị từ chối | RUNTIME_SOURCE | SH-01 có thể hiện danh mục dạng thông tin không lọc; không tuyên bố lọc hoặc dữ liệu khóa học giả. |

## CHANGES

- Tệp đã tạo/cập nhật:
  - .agents/worklog/2026-11-05/study-screen-dd-plan-sh-01.md
  - apps/study-client/docs/screen_stitch/dd_screens/PLAN.md (kế hoạch luồng và bảng theo dõi 83 ID)
  - apps/study-client/docs/screen_stitch/dd_screens/SH-01.md
  - apps/study-client/docs/screen_stitch/dd_screens/plans/SH-01_PLAN.md
  - apps/study-client/docs/screen_stitch/dd_screens/plans/SH-01_markers.json
  - apps/study-client/docs/screen_stitch/dd_screens/tools/render_annotation.py
  - apps/study-client/docs/screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/screen_annotated.png
- CONTEXT_UPDATES: không có; không sửa trang context chuẩn.
- Trang context đã sửa: không.
- Giả định: phiên một màn hình hiện tại bao quát SH-01; kế hoạch tổng theo dõi cả 83 ID, các phiên sau xử lý một ID mỗi phiên.

## VERIFICATION

| Lệnh/đọc | Kết quả | Trạng thái |
|---|---|---|
| Đọc DESIGN.md và list_screen.md theo yêu cầu | Đã đọc từ bản làm việc hiện tại | VERIFIED |
| Kiểm tra tệp/count SH-01 hiện tại | 83 PNG + 83 HTML; chỉ tìm thấy variant-1 | VERIFIED |
| Dựng ảnh chú thích SH-01 | render_annotation.py; PNG gốc 559×1600, ảnh 1118×3200 với 13 marker; đã xem ảnh | VERIFIED |
| Kiểm tra tĩnh sau Việt hóa | 83 ID duy nhất; SH-01/SH-02 có bản nháp hoàn tất, 81 ID còn lại chưa bắt đầu; 22 liên kết cục bộ đã kiểm tra và không có liên kết hỏng | VERIFIED |
| Khớp marker | SH-01 có 13 marker khớp bảng DD; SH-02 có 8 marker khớp bảng DD | VERIFIED |
| Tính toàn vẹn tài sản gốc | SHA-256 PNG/HTML khớp hash trước khi chú thích | VERIFIED |
| Kiểm thử API #05/#06 | Không chạy; task không yêu cầu chạy | NOT_RUN |

## HANDOFF

- Điều kiện còn mở: thiếu variant-2, thiếu khi chạy Study Web, chưa xác minh nguồn nội dung mẫu, còn quyết định về route thẻ khóa học/bộ lọc danh mục và sai khác giao diện.
- Hành động tiếp: tiếp tục mục tiêu 83 ID, mỗi phiên một màn hình theo thứ tự phụ thuộc; màn hình tiếp theo SH-03 vì SH-02 đã hoàn tất bản nháp. Tài liệu SH-01 là bản nháp có căn cứ nguồn, chưa sẵn sàng triển khai.
