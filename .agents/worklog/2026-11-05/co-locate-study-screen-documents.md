---
task_id: "2026-11-05-co-locate-study-screen-documents"
date: "2026-11-05"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Đưa tài liệu màn hình vào thư mục ảnh nguồn tương ứng

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; đã đọc đủ ba worklog được chọn trong 148 worklog `docs` khả dụng.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-05/check-study-screen-stitch-coverage.md`
    - carry_forward: Có 83 mã màn hình duy nhất trong 84 thư mục có ID; SH-01 có hai biến thể. Kiểm kê trước chỉ xác nhận `screen.png` và `code.html`, không xác nhận ảnh chú thích.
  - path: `.agents/worklog/2026-11-05/load-study2work-context.md`
    - carry_forward: `screen_stitch/` là tài liệu thiết kế; mã giao diện Study và ngữ cảnh con Study Web vắng mặt trong bản làm việc.
  - path: `.agents/worklog/2026-11-05/organize-study-screen-stitch.md`
    - carry_forward: Các thư mục màn hình đã được xếp theo nhóm trong danh mục; giữ nguyên nội dung ảnh và HTML nguồn.
- shortage: `none` (đã đọc đủ ba worklog được chọn)

## EXPECTED_BEHAVIOR

- Requirement: Theo chỉ đạo mới nhất, đặt tệp Markdown riêng của từng màn hình vào đúng thư mục đang chứa ảnh nguồn của màn hình đó. Giữ một phiên cho mỗi màn hình; trước mắt sửa quy ước và di chuyển các DD/kế hoạch SH-01 đến SH-04 hiện có.
- Canonical contract/approved DD: `apps/study-client/docs/screen_stitch/README.md`, `dd_screens/PLAN.md`, danh mục `apps/study-client/docs/list_screen.md` và yêu cầu mới nhất của người dùng. Giữ ảnh gốc `screen.png`; tài liệu và ảnh chú thích phải cùng nằm trong thư mục màn hình.

## CURRENT_BEHAVIOR

- Source/config: Trước khi cập nhật, `screen_stitch/README.md` chỉ yêu cầu `screen.png` và `code.html` trong thư mục màn hình. Bốn tệp DD SH-01–SH-04 nằm ở `dd_screens/`; bốn kế hoạch cùng ID và bốn bản đồ số nằm ở `dd_screens/plans/`. DD có liên kết tương đối tới ảnh, kế hoạch, bản đồ số và mã nguồn. Hiện có 83 thư mục chứa `screen.png`, trong đó 4 thư mục SH-01–SH-04 đã có `screen_annotated.png`. README cũ từng liệt kê biến thể SH-01 thứ hai nhưng cây hiện tại không có thư mục đó.
- Runnable tests: Không áp dụng; đây là điều chỉnh cấu trúc tài liệu. Sẽ kiểm tra liên kết và đối chiếu tĩnh sau khi di chuyển.
- Runtime wiring: Không đổi. Đây là bộ tài liệu thiết kế; không suy ra giao diện Study đã được nối khi chạy.

## SOURCE_TRACE

```text
dd_screens/<ID>.md + dd_screens/plans/<ID>_PLAN.md -> thư mục screen_stitch chứa screen.png cùng ID -> cập nhật liên kết tương đối, README và quy ước trong PLAN.md
```

## DISCREPANCIES_AND_STATUSES

| Hạng mục | Bằng chứng | Trạng thái | Tác động |
|---|---|---|---|
| Vị trí tài liệu màn hình | Tám tài liệu SH-01–SH-04 đang ở hai thư mục tổng hợp, tách khỏi các thư mục chứa ảnh màn hình. | SAI_KHÁC | Không đáp ứng quy ước mới của người dùng; cần chuyển tệp và sửa các liên kết/đường dẫn chuẩn. |
| Độ bao phủ ảnh chú thích | Cây hiện tại có 83 thư mục ảnh nguồn và chỉ 4 ảnh chú thích SH-01–SH-04; 79 màn hình chưa có ảnh chú thích. | CHƯA_ĐẠT | Chưa đáp ứng yêu cầu hai ảnh cho toàn bộ 83 màn hình; phải tiếp tục theo từng phiên màn hình. |
| Biến thể SH-01 thứ hai | README cũ và worklog trước liệt kê biến thể `__variant-2`, nhưng `find` hiện không thấy thư mục/tệp tương ứng; DD SH-01 cũng ghi nhận thiếu biến thể này. README hiện đã được sửa cho khớp cây nguồn. | SAI_KHÁC_TÀI_LIỆU | Không tạo lại tài sản thiếu; giữ lại ghi chú để chủ sở hữu xác nhận hoặc cung cấp nguồn. |

## CHANGES

- Files changed: Đã chuyển bốn DD, bốn kế hoạch và bốn bản đồ số SH-01…SH-04 vào các thư mục chứa ảnh nguồn tương ứng; cập nhật liên kết bên trong tài liệu. Cập nhật `README.md`, `dd_screens/PLAN.md`, hai tài liệu SH-01 về tình trạng biến thể thiếu, kế hoạch SH-02 về đường dẫn ảnh, nhật ký SH-04 về vị trí hiện tại và nhật ký này.
- CONTEXT_UPDATES: Không có.
- Context pages changed: Không có; chỉ sửa hướng dẫn và chỉ mục trong `screen_stitch` theo yêu cầu.
- Assumptions: Một DD và một kế hoạch cho mỗi mã màn hình. Nếu có nhiều thư mục biến thể nguồn, đặt DD/kế hoạch cạnh biến thể được mô tả; mỗi biến thể có thật cần ảnh chú thích và bản đồ số riêng. Không tự tạo lại biến thể SH-01 thứ hai đang thiếu.

## VERIFICATION

| Lệnh/đọc tài liệu | Kết quả | Trạng thái |
|---|---|---|
| `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/select-worklogs.mjs --type docs --limit 3` và đọc các kết quả | Đã chọn và đọc đủ ba worklog cùng loại. | ĐÃ_XÁC_MINH |
| `apps/study-client/docs/screen_stitch/README.md`, `dd_screens/PLAN.md`, danh sách Markdown trong `screen_stitch/` | Đã thấy DD và kế hoạch SH-01–SH-04 tách khỏi thư mục ảnh nguồn. | ĐÃ_XÁC_MINH_TĨNH |
| Chuyển tài liệu SH-01–SH-04 và rà soát đường dẫn Markdown | Bốn DD, bốn kế hoạch và bốn bản đồ số hiện nằm cùng ảnh nguồn; không còn DD/kế hoạch riêng trong `dd_screens/` hoặc `dd_screens/plans/`; 50 liên kết Markdown hiện có đều mở được. | ĐÃ_XÁC_MINH_TĨNH |
| Đối chiếu danh mục, thư mục ảnh và bộ tài liệu hiện có | 83 mã duy nhất trong `list_screen.md` khớp 83 thư mục có `screen.png`; SH-01–SH-04 có đủ ảnh gốc, ảnh chú thích, DD, kế hoạch và bản đồ số. SHA-256 ảnh/HTML nguồn của cả bốn màn hình giữ nguyên. | ĐÃ_XÁC_MINH_TĨNH |
| Kiểm kê ảnh chú thích toàn bộ màn hình | Hiện có 4/83 ảnh `screen_annotated.png`; 79 màn hình chưa có ảnh chú thích. Đây là phần việc còn lại của mục tiêu tổng thể. | ĐÃ_XÁC_MINH_TĨNH / CHƯA_HOÀN_TẤT |
| Kiểm thử dự án | Không chạy; phiên này chỉ sắp xếp tài liệu và đối chiếu tĩnh. | KHÔNG_CHẠY |

## HANDOFF

- Điều kiện còn chặn: 79/83 màn hình chưa có ảnh chú thích và DD/kế hoạch tương ứng. README cùng worklog cũ từng ghi nhận biến thể SH-01 thứ hai, nhưng cây hiện tại không có thư mục/tệp đó; không tái tạo khi chưa có nguồn.
- Bước tiếp theo: Tiếp tục theo thứ tự danh mục với SH-05 trong phiên màn hình kế tiếp; tạo kế hoạch trước, sau đó hoàn thiện ảnh chú thích và DD ngay trong thư mục SH-05.
