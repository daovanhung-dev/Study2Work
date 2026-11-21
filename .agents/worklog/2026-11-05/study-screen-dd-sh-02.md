---
task_id: "2026-11-05-study-screen-dd-sh-02"
date: "2026-11-05"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["SH-02 giao diện đăng nhập -> Study API #03 đăng nhập, #04 hồ sơ học viên, R-X01 refresh"]
status: "PARTIAL"
---

# Nhật ký công việc: Tài liệu thiết kế chi tiết SH-02 — Đăng nhập

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- Lệnh chọn worklog: /home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/select-worklogs.mjs --type docs --limit 3
- Kết quả chọn: READY; đã chọn và đọc đủ 3 worklog loại tài liệu trong tổng số 145.
- Các worklog đã đọc:
  - .agents/worklog/2026-11-05/check-study-screen-stitch-coverage.md
    - Ghi nhận: screen_stitch là danh mục tài sản thiết kế; có 83 ID duy nhất; tài sản không chứng minh Study Web đang chạy.
  - .agents/worklog/2026-11-05/load-study2work-context.md
    - Ghi nhận: thiếu mã Study Web src và .agents/web-work/study/ dù manifest khai báo; cần kiểm tra trạng thái hiện tại và giữ ranh giới tài liệu.
  - .agents/worklog/2026-11-05/organize-study-screen-stitch.md
    - Ghi nhận: tài sản màn hình nguồn được giữ nguyên; không gán thứ tự mới/cũ cho biến thể nếu chưa có bằng chứng.
- Thiếu worklog: không.

## EXPECTED_BEHAVIOR

- Yêu cầu: Tiếp tục mục tiêu tài liệu 83 màn hình, mỗi phiên một màn hình. Với SH-02, tạo kế hoạch riêng soạn trước, một DD chi tiết đặt tên theo màn hình và một ảnh chú thích cho mỗi ảnh nguồn đang có; giữ nguyên screen.png và code.html.
- Hợp đồng chuẩn/DD được duyệt: dòng SH-02 và luồng F01 trong apps/study-client/docs/list_screen.md; API #03/#04 cùng mọi hợp đồng xác thực/refresh áp dụng. Route UI /login chỉ là đề xuất nếu mã Study Web hiện tại chưa chứng minh ngược lại.
- Yêu cầu mới nhất: toàn bộ tài liệu đầu ra phải viết bằng tiếng Việt; giữ nguyên các mã API/trường/route cần đối chiếu với mã nguồn.

## CURRENT_BEHAVIOR

- Mã nguồn/cấu hình: git status chỉ cho thấy .agents/worklog/2026-11-05/ và apps/study-client/docs/screen_stitch/ là chưa theo dõi. SHA-256 screen.png là 5c3cb8e59c1b645c4338ce527d5fd2c7a2288568fc04982481865d422ec4e323; SHA-256 code.html là 6e848c7bbab66b13f0486eb397b9da8a0e2059f3d9b169287b8359b8c1aad595. Thiếu tệp context và tệp chỉ mục Study Web được bản đồ context/manifest khai báo tại đường dẫn đã chỉ định; không có mã nguồn màn hình Study Web.
- Kiểm thử có thể chạy: đã đọc tên/mã nguồn kiểm thử liên quan; chưa chạy theo yêu cầu không chạy kiểm thử.
- Nối khi chạy: chưa có router/client Study Web. Mã nguồn Study Server hiện nối API #03 đăng nhập, #04 hồ sơ học viên và R-X01 refresh.

## SOURCE_TRACE

~~~text
route /login đề xuất, chưa có router Study Web
  -> API #03 POST /api/v1/auth/login
  -> nếu role STUDENT và chính sách phiên được duyệt: API #04 GET /api/v1/users/me
  -> #04 trả 401: R-X01 POST /api/v1/auth/refresh tối đa một lần rồi thử lại #04 một lần
  -> cập nhật trạng thái UI/đích điều hướng theo điều kiện role và phiên
~~~

## DISCREPANCIES_AND_STATUSES

| Hạng mục | Bằng chứng | Trạng thái | Ảnh hưởng |
|---|---|---|---|
| Đường dẫn context Study Web | Bản đồ context/manifest khai báo .agents/web-work/study/*; thao tác đọc báo thiếu tệp chỉ mục | NOT_FOUND / SOURCE_REQUIRED | Không suy đoán hành vi client; SH-02 vẫn là đề xuất thiết kế. |
| Ranh giới UI/API | Hành trình đăng nhập Study đi qua Study Web và Study Server | CROSS_SCOPE | Đã kiểm tra cả hai phạm vi; giữ kỳ vọng phía giao diện tách khỏi hành vi phía máy chủ. |
| API #03 | DD/danh mục chuẩn mô tả 201 và chỉ hồ sơ; nguồn hiện trả 200 cùng token, có nhánh 401/403/500 | DISCREPANCY | Giữ riêng hợp đồng kỳ vọng và hành vi nguồn; không tự hòa giải. |
| PNG SH-02 | screen.png 1280×1024 nhìn thấy trống; HTML dựng được giao diện | DISCREPANCY | Giữ ảnh gốc; dùng screen_rendered.png và screen_annotated.png làm tài sản phát sinh, có ghi nguồn. |
| Khởi tạo vai trò | #04 chỉ chấp nhận STUDENT; chưa có route hồ sơ phù hợp người hướng dẫn/quản trị viên | BLOCKED | Không gọi #04 cho các vai trò khác, không đưa về /student. |

## CHANGES

- Tệp đã tạo/cập nhật: worklog này; kế hoạch tổng; DD và kế hoạch riêng SH-01/SH-02; hai bản đồ marker JSON; công cụ dựng ảnh; hai ảnh chú thích; bản xem sạch SH-02. Đã Việt hóa toàn bộ văn xuôi, tiêu đề và nhãn trong bộ tài liệu đầu ra.
- CONTEXT_UPDATES: không có; không sửa trang context chuẩn.
- Trang context đã sửa: không.
- Giả định: dùng danh mục/nguồn API hiện tại; giữ mọi thay đổi không liên quan; không chạy kiểm thử nếu người dùng không yêu cầu.

## VERIFICATION

| Lệnh/đọc | Kết quả | Trạng thái |
|---|---|---|
| Công cụ chọn worklog | Đã đọc đủ 3 worklog loại tài liệu được chọn | VERIFIED |
| Nguồn SH-02 và hợp đồng liên quan | Đã kiểm tra mã HTML/ảnh, API #03/#04/R-X01 và cấu hình liên quan | VERIFIED |
| Kiểm tra tĩnh sau Việt hóa | 83 ID duy nhất, 0 route lệch, marker SH-01 1–13 và SH-02 1–8 khớp DD, 22 liên kết cục bộ đã kiểm tra và không có liên kết hỏng | VERIFIED |
| Kích thước ảnh | SH-01 gốc 559×1600, chú thích 1118×3200; SH-02 gốc 1280×1024, bản dựng 1280×1024, chú thích 2560×2048 | VERIFIED |
| Cú pháp công cụ chú thích | Đã phân tích cú pháp Python bằng ast.parse; hợp lệ | VERIFIED |
| Hash tài sản nguồn | screen.png và code.html khớp hash đã ghi ở trên; ảnh gốc SH-01 cũng khớp hash trong kế hoạch | VERIFIED |
| Chạy kiểm thử | Không được yêu cầu; không chạy | NOT_RUN |

## HANDOFF

- Điều kiện còn mở: sai khác hợp đồng #03; chính sách lưu/refresh token; khởi tạo vai trò người hướng dẫn/quản trị viên; PNG nguồn trống; bộ xử lý mẫu chưa định nghĩa; context Study Web bị thiếu.
- Hành động tiếp: tiếp tục mục tiêu 83 ID, mỗi phiên một màn hình; màn hình kế tiếp là SH-03. SH-02 là bản nháp có bằng chứng nguồn, chưa sẵn sàng triển khai.
