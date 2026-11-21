---
task_id: "2026-11-05-study-screen-dd-sh-05"
date: "2026-11-05"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies:
  - "SH-05 xử lý trạng thái 401/403 từ phiên Study và quy tắc làm mới token phía Study Server"
status: "IN_PROGRESS"
---

# Nhật ký công việc: Soạn tài liệu thiết kế chi tiết màn hình SH-05

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; đã đọc đủ ba worklog được chọn trong 149 worklog `docs` khả dụng.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-05/check-study-screen-stitch-coverage.md`
    - carry_forward: Mã nguồn giao diện Study không có trong bản làm việc; tài sản màn hình chỉ là thiết kế. Kiểm tra hiện tại thay vì dựa vào số lượng biến thể trong worklog cũ.
  - path: `.agents/worklog/2026-11-05/co-locate-study-screen-documents.md`
    - carry_forward: DD, kế hoạch và bản đồ số phải cùng thư mục chứa `screen.png`; hiện 4/83 màn hình có ảnh chú thích, SH-05 là bước tiếp theo.
  - path: `.agents/worklog/2026-11-05/load-study2work-context.md`
    - carry_forward: Đọc source hiện hành, giữ riêng thiết kế đích với hành vi chạy thật; Study Web subcontext có thể thiếu và phải kiểm tra lại.
- shortage: `none` (đã đọc đủ ba worklog được chọn)

## EXPECTED_BEHAVIOR

- Requirement: Hoàn thiện riêng SH-05 trong phiên này. Giữ nguyên ảnh gốc, lập kế hoạch chi tiết trước DD/chú thích, tạo ảnh có số đánh dấu, đặt DD và kế hoạch cạnh ảnh nguồn, viết hoàn toàn bằng tiếng Việt ngoại trừ tên định danh kỹ thuật cần giữ nguyên.
- Canonical contract/approved DD: Dòng SH-05, AC-02/AC-11 và luồng xác thực trong `apps/study-client/docs/list_screen.md`; hướng dẫn hình ảnh Study tại `.agents/web-study/design.md`; trạng thái 401/403 và API #04/R-X01 chỉ được mô tả theo source hiện hành.

## CURRENT_BEHAVIOR

- Source/config: `screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/` có `screen.png` (1600×1280, SHA-256 `f13f4da1e7717ccafbf93155af94e526e8a5f865d63e207c21165118c16cd23f`) và `code.html` (SHA-256 `cd0f2cb849d8a39aae842c08f5602fc24718b2d34e9f446d56041c1017b8ad7a`). Chưa có ảnh chú thích, DD hoặc kế hoạch.
- Runnable tests: Chưa đọc mã kiểm thử API liên quan; không chạy kiểm thử nếu người dùng không yêu cầu.
- Runtime wiring: Chưa xác minh màn hình SH-05 có trong router giao diện; sẽ kiểm tra source hiện hành và ghi trạng thái tĩnh.

## SOURCE_TRACE

```text
SH-05 dự kiến nhận trạng thái HTTP 401/403 từ luồng xác thực -> phân biệt hết hạn/thiếu phiên với không đủ quyền -> chỉ thử làm mới phiên theo bằng chứng runtime R-X01 -> giữ đường quay lại nội bộ an toàn -> điều hướng tới SH-02 hoặc trang trước phù hợp; chưa chốt cho đến khi đọc source/API/test
```

## DISCREPANCIES_AND_STATUSES

| Hạng mục | Bằng chứng | Trạng thái | Tác động |
|---|---|---|---|
| Giao diện Study khi chạy | Bản làm việc trước chỉ có tài liệu Study; phải kiểm tra lại cây hiện tại. | CHỜ_KIỂM_TRA | DD không được tuyên bố route hoặc xử lý giao diện đã nối. |
| Ảnh chú thích SH-05 | Thư mục hiện có PNG gốc và HTML, chưa có `screen_annotated.png`. | CHƯA_ĐẠT | Cần tạo ảnh riêng có đánh số, giữ nguyên PNG gốc. |

## CHANGES

- Files changed: Chưa tạo DD, kế hoạch hoặc ảnh chú thích.
- CONTEXT_UPDATES: Chưa có.
- Context pages changed: Chưa có.
- Assumptions: Xem các trạng thái lỗi trong HTML là tài sản thiết kế cho tới khi mã nguồn/API xác nhận. Không tự tạo điểm cuối, mã nghiệp vụ, chính sách vai trò hoặc URL điều hướng.

## VERIFICATION

| Lệnh/đọc tài liệu | Kết quả | Trạng thái |
|---|---|---|
| `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/select-worklogs.mjs --type docs --limit 3` và đọc đủ ba kết quả | Chọn đúng loại `docs`; đã đọc ba worklog đã chọn. | ĐÃ_XÁC_MINH |
| `apps/study-client/docs/list_screen.md` và bảng theo dõi màn hình | Dòng SH-05 là bước kế tiếp; API #04, AC-02/AC-11, trạng thái 401/403 và R-X01 được ghi trong thiết kế đích. | ĐÃ_XÁC_MINH_TĨNH |
| Ảnh/HTML SH-05 | Tệp nguồn tồn tại; chưa sửa. | ĐÃ_XÁC_MINH_TĨNH |

## HANDOFF

- Điều kiện còn chặn: Chưa đọc mã hiện hành của API #03/#04, R-X01 và mã kiểm thử liên quan; cần xác định điều hướng an toàn cùng trạng thái giao diện từ căn cứ hiện có.
- Bước tiếp theo: Nạp đúng ngữ cảnh web/server, truy vết hợp đồng 401/403 và làm mới phiên; sau đó hoàn thiện kế hoạch SH-05 trước DD và ảnh chú thích.
