---
task_id: "2026-11-05-study-screen-dd-sh-03"
date: "2026-11-05"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Màn hình Study Web SH-03 -> API #01 đăng ký của Study Server; chỉ bàn giao API #02 ở SH-04 theo danh mục và mã nguồn hiện tại"]
status: "PARTIAL"
---

# Worklog: Tài liệu thiết kế màn hình SH-03

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; đã đọc đủ 3 worklog được chọn trong 146 worklog `docs` khả dụng.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-05/check-study-screen-stitch-coverage.md`
    - carry_forward: Danh mục có 83 mã màn hình duy nhất; mọi mã đều có tài sản. Đây là nền thiết kế, không phải bằng chứng Study Web đã triển khai.
  - path: `.agents/worklog/2026-11-05/load-study2work-context.md`
    - carry_forward: `apps/study-client/src` và trang ngữ cảnh con Study Web không có trong bản làm việc gần nhất được ghi nhận; kiểm tra lại mã nguồn hiện tại, không suy ra giao diện đang chạy từ tài sản thiết kế.
  - path: `.agents/worklog/2026-11-05/organize-study-screen-stitch.md`
    - carry_forward: Thư mục SH-03 đã được xếp vào nhóm theo inventory; giữ nguyên artifact gốc và tách reference dưới `90_reference/`.
- shortage: `none` (146 worklog docs khả dụng; đã đọc đủ 3 worklog được chọn)

## EXPECTED_BEHAVIOR

- Requirement: Hoàn thiện một màn hình trong phiên làm việc này: SH-03. Tài liệu đầu ra phải viết hoàn toàn bằng tiếng Việt, có kế hoạch chi tiết trước tài liệu màn hình, ảnh gốc kèm chú giải đánh số, cùng luồng thành phần/sự kiện/API dựa trên bằng chứng.
- Canonical contract/approved DD: `apps/study-client/docs/list_screen.md`, `apps/study-client/docs/screen_stitch/90_reference/study2work-lms-design-system/DESIGN.md` và yêu cầu mới nhất của người dùng. Cần đọc lại các tài liệu và đối chiếu với mã nguồn hiện tại trước khi ghi hành vi.

## CURRENT_BEHAVIOR

- Source/config: Ảnh SH-03 có biểu mẫu tên/email/mật khẩu, nút tạo tài khoản và liên kết đăng nhập. `code.html` chặn gửi biểu mẫu mặc định và không gọi API; mã nguồn/bộ định tuyến Study Web không có trong bản làm việc. API #01 có đường dẫn `POST /api/v1/auth/register`, kiểm tra rồi chuẩn hóa `email` và `full_name`, băm mật khẩu Argon2id, ghi tài khoản vai trò `STUDENT`, `commit`, trả hồ sơ công khai với HTTP 201. API #02 là đường dẫn tách biệt; bộ gửi thư mặc định chỉ trả `accepted`.
- Runnable tests: Có mã kiểm thử API #01 cho chuẩn hóa, 422, 409, 201, `rollback` và phản hồi an toàn; có mã kiểm thử API #02 cho HTTP 202, bộ giả lập, không phụ thuộc cơ sở dữ liệu và lỗi bộ gửi thư. Không chạy kiểm thử theo phạm vi task.
- Runtime wiring: Đường dẫn máy chủ được khai báo trong `apps/study-server/app/api/v1.py`; đây là bằng chứng mã nguồn, không chứng minh API đã triển khai hoặc cơ sở dữ liệu đang chạy thực tế. Đường dẫn giao diện `/register` và điều hướng chưa được xác minh.

## SOURCE_TRACE

```text
Mẫu SH-03 (onsubmit chỉ preventDefault; không gọi API; giao diện khi chạy NOT_FOUND)
-> mục tiêu POST /api/v1/auth/register
-> RegisterRequest -> validate_register_request -> create_user
-> CHECK_DUPLICATE -> băm Argon2id -> INSERT_USER (role='STUDENT') -> commit
-> HTTP 201 DESIGN_RESOURCE_CREATED + data hồ sơ công khai
-> điều hướng đích sang SH-04, ánh xạ data.id thành user_id và dùng data.email
-> chỉ gọi API #02 riêng ở SH-04; bộ gửi thư mặc định trả accepted, không gửi email thật.
Đã đọc mã kiểm thử API #01/#02, không chạy kiểm thử.
```

## DISCREPANCIES_AND_STATUSES

| Hạng mục | Bằng chứng | Trạng thái | Tác động |
|---|---|---|---|
| Trang ngữ cảnh Study Web | Bộ định tuyến tham chiếu `.agents/web-work/study/`, nhưng đường dẫn không tồn tại trong bản làm việc hiện tại. | `NOT_FOUND` | Dùng mã nguồn/tài liệu hiện có; ghi rõ khi không thể xác nhận giao diện lúc chạy. |
| Giao diện khi chạy | `apps/study-client` hiện chỉ có tài liệu; `code.html` gọi `preventDefault()` và không có lời gọi API. | `UNWIRED / SOURCE_REQUIRED` | SH-03 chỉ là thiết kế; không mô tả `/register` như đường dẫn đang hoạt động. |
| Quy tắc mật khẩu | Bản HTML ẩn ghi tối thiểu 8 ký tự; API #01 chỉ từ chối chuỗi rỗng/toàn khoảng trắng, không đặt ngưỡng 8. | `DISCREPANCY` | Không đưa ngưỡng 8 vào hợp đồng kiểm tra; cần sửa nội dung lỗi mẫu hoặc chốt quy tắc riêng cho máy chủ. |
| Bàn giao xác minh | API #01 ghi nhật ký rằng bước gửi bị trì hoãn; API #02 là đường dẫn riêng với bộ gửi thư giả lập mặc định. | `DISCREPANCY` | Tạo tài khoản không tự chứng minh email được gửi/xác minh; SH-04 phải nêu rõ trạng thái `accepted`. |
| Phản hồi và cơ sở dữ liệu | API #01 trả `data.id`, còn API #02 nhận `user_id`; tệp DDL trong kho khai báo mặc định `status`, không xác nhận lược đồ đang chạy thực tế. | `DISCREPANCY` | Nếu tiếp tục sang SH-04, ánh xạ `data.id` → `user_id`; không khẳng định trạng thái cơ sở dữ liệu đang chạy. |

## CHANGES

- Files changed: Tạo kế hoạch `SH-03_PLAN.md`, tài liệu `SH-03.md`, `SH-03_markers.json`, ảnh `screen_annotated.png`; cập nhật bảng theo dõi `PLAN.md` và worklog này. Không sửa `screen.png` hoặc `code.html`.
- CONTEXT_UPDATES: Không đổi kiến trúc, API, hợp đồng hoặc mã nguồn.
- Context pages changed: Không có.
- Assumptions: Chỉ xử lý SH-03 trong phiên này; giữ nguyên nội dung gốc của `screen.png` và `code.html`.

## VERIFICATION

| Lệnh/nguồn đọc | Kết quả | Trạng thái |
|---|---|---|
| Bộ chọn worklog `docs` | Chọn 3 worklog; đã đọc cả ba. | `VERIFIED` |
| Study Web subcontext | `.agents/web-work/study/AGENTS.md` không tồn tại trong checkout. | `NOT_FOUND` |
| `list_screen.md`, `DESIGN.md`, HTML/PNG SH-03 | Đọc danh mục SH-03, luồng F01, hướng dẫn thiết kế và ảnh/HTML nguồn. | `VERIFIED_STATIC_ONLY` |
| API #01/#02 và mã kiểm thử liên quan | Đọc đường dẫn, mô hình, bộ kiểm tra, lớp điều phối, câu truy vấn, bộ gửi thư và mã kiểm thử; không chạy kiểm thử. | `VERIFIED_STATIC_ONLY` |
| Tạo ảnh chú thích | Chạy `tools/render_annotation.py` với Chrome; tạo ảnh 2560×2112 từ ảnh gốc 1280×1056, gồm 7 điểm đánh dấu. | `VERIFIED_STATIC_ONLY` |
| Kiểm tra tĩnh SH-03 | Liên kết Markdown cục bộ hợp lệ; JSON có marker 1–7; bảng DD có đúng 7 hàng; danh mục có 83 mã duy nhất, 3 bản nháp đã xong và 80 chưa bắt đầu. | `VERIFIED_STATIC_ONLY` |
| Giữ nguyên tài sản gốc | SHA-256 PNG `67eef666cf7ebf48db44b2b721b13a40632237a165ff11ca6b5a2040a32d079e` và HTML `bd0123dee4571caff1920804b4ce8508d2f20f53ce8e113afcb766874c8334a3` khớp trước/sau. | `VERIFIED` |
| Kiểm thử dự án | Không chạy theo phạm vi tài liệu; chỉ đọc mã kiểm thử API. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: Giao diện khi chạy không có trong bản làm việc; bộ gửi email xác minh đang giả lập; cần chốt giới hạn mật khẩu 8 ký tự và vòng đời `status` trước khi phát hành.
- Next owner/action: SH-03 hoàn tất ở mức bản nháp; phiên tài liệu tiếp theo đủ điều kiện xử lý SH-04.
