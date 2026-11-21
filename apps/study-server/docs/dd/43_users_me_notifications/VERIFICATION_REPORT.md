# VERIFICATION_REPORT — Study API #43

## Trạng thái

- DD pack: PASS — đủ 8 sheet theo template và 3 report Markdown.
- DD `status`: Draft — Needs Confirmation.
- Runtime `status`: UNWIRED / NOT_FOUND.
- Runtime tests: NOT_RUN — tài liệu-only task; không có source route để test.
- Macro review AC-20 #43–#45: Pending đến khi DD #44 và #45 tồn tại.

## Template fingerprint

Template folder: `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/`.

| File | SHA-256 |
|---|---|
| 00_Cover.md | fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63 |
| 01_Lich_su.md | d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e |
| 02_Overview.md | c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6 |
| 03_Request.md | 37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa |
| 04_Response.md | 5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8 |
| 05_Data_Mapping.md | 11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b |
| 06_Error.md | e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b |
| 07_table.md | 4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356 |

Study workflow yêu cầu Markdown-only; không tạo ZIP.

## Checks

| Check | Result | Status |
|---|---|---|
| Required files | 11/11 expected files: 8 template sheets + `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`. | PASS |
| Front matter and API ID/`status` | 8/8 sheet có front matter, `dd_id: "43"`, đúng API name và `Draft — Needs Confirmation`. | PASS |
| Catalog contract | Đối chiếu API #43: GET path, Student Bearer JWT, `unread_only`/`page`, ApiEnvelope<Page<Notification>>, HTTP 200 và chỉ các lỗi 401/403/500 đúng code. | PASS |
| AC-20 traceability | Theo flow mở notification center, đọc danh sách theo user, hiển thị, và phân nhánh thao tác API #44/#45; điểm chưa có `NotificationRecipient` được ghi là discrepancy. | PASS |
| Request/response field coverage | Hai query field và các field envelope, Page, Notification được thể hiện riêng; response source matrix ghi source/status từng field. | PASS |
| JSON examples | Hai fenced JSON example parse hợp lệ. Marker `SOURCE_REQUIRED_*` được ghi rõ là placeholder, không phải enum đã xác nhận. | PASS |
| Relative links and anchors | Tất cả link file và anchor nội bộ trong pack resolve. | PASS |
| Markdown tables/code fences/whitespace | Kiểm tra độ rộng hàng bảng, cặp fence, inline backtick và trailing whitespace; không phát hiện lỗi. | PASS |
| One field/condition/error per row | Request/query/response-source/error matrices đã rà soát; từng trường, điều kiện query, và error case nằm riêng một hàng. | PASS |
| Source gaps and derived rules | `channels`, `status`, `read_at`, `scheduled_at`, recipient/broadcast và timezone được giữ `SOURCE_REQUIRED`/open; page default/size/order/count được đánh dấu `DERIVED`. | PASS |
| Output core fingerprint | SHA-256 gộp các file DD/report trừ báo cáo này: `0f273d2fda836c8297a7c78044d3a9a2ad7d2b398a62cd1e4c13e1264ef340b4`. | PASS |
| Runtime tests | Không chạy do task chỉ tạo tài liệu và API #43 hiện `UNWIRED / NOT_FOUND`. | NOT_RUN |

## Template comparison

- Tám sheet giữ đúng tên/thứ tự và có đúng một phụ lục đối chiếu template mỗi sheet.
- `07_table.md` là read-only: update/insert/delete đặt N/A, candidate read projection và schema gaps được liệt kê riêng.
- Ba report Markdown đi kèm đủ; không sửa file template nguồn.
