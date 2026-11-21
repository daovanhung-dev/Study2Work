# ME-10 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ME-10_markers.json](../../screen_stitch/04_mentor/ME-10_cham-diem-va-phan-hoi/ME-10_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ME-10-EL-001` | `ME10-EL-01` | Logo và thương hiệu Study2Work LMS Mentor |
| #2 | `ME-10-EL-002` | `ME10-EL-02` | Điều hướng Tổng quan |
| #3 | `ME-10-EL-003` | `ME10-EL-03` | Điều hướng Khóa học phụ trách |
| #4 | `ME-10-EL-004` | `ME10-EL-04` | Điều hướng Chấm bài đang chọn |
| #5 | `ME-10-EL-005` | `ME10-EL-05` | Điều hướng Hộp thư hỗ trợ |
| #6 | `ME-10-EL-006` | `ME10-EL-06` | Điều hướng Thông báo |
| #7 | `ME-10-EL-007` | `ME10-EL-07` | Chuông thông báo |
| #8 | `ME-10-EL-008` | `ME10-EL-08` | Danh tính và avatar Mentor mẫu |
| #9 | `ME-10-EL-009` | `ME10-EL-09` | Breadcrumb Chấm bài đến Chi tiết |
| #10 | `ME-10-EL-010` | `ME10-EL-10` | Badge mã phiên làm việc mẫu |
| #11 | `ME-10-EL-011` | `ME10-EL-11` | Eyebrow hệ thống điều phối chấm điểm |
| #12 | `ME-10-EL-012` | `ME10-EL-12` | Tiêu đề Đánh giá bài tập và phản hồi học viên |
| #13 | `ME-10-EL-013` | `ME10-EL-13` | Mô tả màn hình |
| #14 | `ME-10-EL-014` | `ME10-EL-14` | Nút quay lại danh sách bài nộp phía trên |
| #15 | `ME-10-EL-015` | `ME10-EL-15` | Tiêu đề panel Tập tin bài làm học viên |
| #16 | `ME-10-EL-016` | `ME10-EL-16` | Badge Đang đồng bộ |
| #17 | `ME-10-EL-017` | `ME10-EL-17` | Trạng thái đang chờ kết nối dữ liệu |
| #18 | `ME-10-EL-018` | `ME10-EL-18` | Mã nộp bài và tiến trình kiểm định mẫu |
| #19 | `ME-10-EL-019` | `ME10-EL-19` | Nút Làm mới kết nối |
| #20 | `ME-10-EL-020` | `ME10-EL-20` | Nút Báo cáo sự cố tải file |
| #21 | `ME-10-EL-021` | `ME10-EL-21` | Claim giao thức bảo mật AES-256 |
| #22 | `ME-10-EL-022` | `ME10-EL-22` | Claim khuôn khổ đánh giá WCAG 2.1 AA |
| #23 | `ME-10-EL-023` | `ME10-EL-23` | Dải lưu ý nghiệp vụ về file đính kèm |
| #24 | `ME-10-EL-024` | `ME10-EL-24` | Nhãn điểm đánh giá và khóa chỉnh sửa |
| #25 | `ME-10-EL-025` | `ME10-EL-25` | Input điểm disabled, thang /100 và gợi ý |
| #26 | `ME-10-EL-026` | `ME10-EL-26` | Tiêu đề rubric và bộ đếm tiêu chí 0/0 |
| #27 | `ME-10-EL-027` | `ME10-EL-27` | Empty state Chưa có rubric tự động |
| #28 | `ME-10-EL-028` | `ME10-EL-28` | Nhãn nhận xét và bộ đếm ký tự |
| #29 | `ME-10-EL-029` | `ME10-EL-29` | Textarea nhận xét của giảng viên |
| #30 | `ME-10-EL-030` | `ME10-EL-30` | Gợi ý Markdown hỗ trợ |
| #31 | `ME-10-EL-031` | `ME10-EL-31` | Cảnh báo an toàn dữ liệu |
| #32 | `ME-10-EL-032` | `ME10-EL-32` | Nút Lưu điểm số và gửi nhận xét disabled |
| #33 | `ME-10-EL-033` | `ME10-EL-33` | Nút quay lại danh sách bài nộp phía dưới |
| #34 | `ME-10-EL-034` | `ME10-EL-34` | Trạng thái chữ ký số PENDING_AUTH |
| #35 | `ME-10-EL-035` | `ME10-EL-35` | Version mẫu v2.4.1 |
| #36 | `ME-10-EL-036` | `ME10-EL-36` | Logo và copyright footer |
| #37 | `ME-10-EL-037` | `ME10-EL-37` | Link Quy chế Giảng viên |
| #38 | `ME-10-EL-038` | `ME10-EL-38` | Link Tiêu chuẩn đánh giá |
| #39 | `ME-10-EL-039` | `ME10-EL-39` | Link Hỗ trợ kỹ thuật |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết element

Các marker `#1–#39` trong [ảnh chú thích](../../screen_stitch/04_mentor/ME-10_cham-diem-va-phan-hoi/screen_annotated.png) có cùng số/ID trong [marker map](../../screen_stitch/04_mentor/ME-10_cham-diem-va-phan-hoi/ME-10_markers.json) và [SVG overlay](../../screen_stitch/04_mentor/ME-10_cham-diem-va-phan-hoi/ME-10_markers_overlay.svg). “Static” là bằng chứng mockup, không phải runtime behavior.

| # / Element ID | Tên, loại, vị trí và thuộc tính hiện biết | Nguồn; hiển thị / trạng thái | Event |
|---|---|---|---|
| 1 / ME10-EL-01 | Logo/brand link ở header trái. | HTML `data-path="tong-quan"`, `href="#"`; route chưa wire. | E10 |
| 2 / ME10-EL-02 | Nav link “Tổng quan”. | `href="#"`; destination chưa xác nhận. | E10 |
| 3 / ME10-EL-03 | Nav link “Khóa học phụ trách”. | `href="#"`; không truyền course context theo source. | E10 |
| 4 / ME10-EL-04 | Nav “Chấm bài”, active page. | `aria-current="page"`; `href="#"`. | Không có route event được wire; E10 chỉ ghi placeholder. |
| 5 / ME10-EL-05 | Nav link “Hộp thư hỗ trợ”. | `href="#"`; support flow thuộc ME-11/12. | E10 |
| 6 / ME10-EL-06 | Nav link “Thông báo”. | `href="#"`; chưa có route trong asset. | E10 |
| 7 / ME10-EL-07 | Notification bell link/icon, có dot đỏ. | `href="#"`; unread state/API #43 không được gọi từ HTML. | E10 |
| 8 / ME10-EL-08 | Tên/avatar Mentor mẫu. | “TS. Vũ Thành Đạt / MENTOR / GIẢNG VIÊN”; tĩnh, không lấy từ token hay current-user API. | Không có event. |
| 9 / ME10-EL-09 | Breadcrumb Chấm bài → Chi tiết. | Link cha dùng `href="#"`; phần chi tiết là text. | E08/E10; chưa wired. |
| 10 / ME10-EL-10 | Badge mã phiên `SES-ME10-SYNC`. | Giá trị ví dụ; không phải API traceId hoặc session từ server. | Không có event. |
| 11 / ME10-EL-11 | Eyebrow “Hệ thống điều phối chấm điểm LMS”. | Nhãn tĩnh, không phải status API. | Không có event. |
| 12 / ME10-EL-12 | H1 “Đánh giá bài tập và phản hồi học viên”. | Heading page. | E01 load context. |
| 13 / ME10-EL-13 | Mô tả màn hình. | Copy tĩnh về chuẩn đánh giá; không định nghĩa score/rubric policy. | Không có event. |
| 14 / ME10-EL-14 | Nút quay lại ME-09 phía trên. | Anchor `href="#"`, text chỉ rõ ME-09; no history/filter retention logic. | E08 |
| 15 / ME10-EL-15 | Panel title “Tập tin bài làm học viên” và phụ đề kho lưu trữ. | Không có nội dung file thật trong ảnh; #55 response `files[]` là source tương lai, file lookup DERIVED. | E01 |
| 16 / ME10-EL-16 | Badge “Đang đồng bộ”. | Visual badge có biểu tượng refresh; không có timer/polling/event trong HTML. | E02 (placeholder only) |
| 17 / ME10-EL-17 | Minh họa và thông báo “Đang chờ kết nối dữ liệu”. | Design empty/wait state; không đồng nghĩa server job thật. | E01/E02 |
| 18 / ME10-EL-18 | Progress widget: “Phân giải định danh đối tượng”, mã `SUB-VERIFYING`, “Cổng kiểm định: Tự động”. | Mã và scan status là sample; không có endpoint/progress event. | E01; data mapping blocked |
| 19 / ME10-EL-19 | Button “Làm mới kết nối”. | `<button type=button>`; không có click handler, disable/retry logic. | E02 |
| 20 / ME10-EL-20 | Button “Báo cáo sự cố tải file”. | `<button type=button>`; không có handler, API hay route. | E09 |
| 21 / ME10-EL-21 | Claim “Giao thức bảo mật AES-256”. | Static text; không chứng minh transport/storage encryption. | Không có event; claim cần xác minh. |
| 22 / ME10-EL-22 | Claim “Khuôn khổ đánh giá: WCAG 2.1 AA”. | Static text; không phải kết quả accessibility audit. | Không có event; xem A11y target ở mục E. |
| 23 / ME10-EL-23 | Advisory strip về malware scan và liên kết danh tính tài khoản học viên. | Copy tĩnh; #55 trả một upload match nhưng không có scan/identity proof flag trong response. | E01; mapping claim blocked |
| 24 / ME10-EL-24 | Score label và “Khóa chỉnh sửa”. | Label gắn `for="grade-input"`; hiển thị thang `0–100`, source #56 là int32/range DERIVED. | E03 |
| 25 / ME10-EL-25 | Number input `id=grade-input`, placeholder `--`, `/100`; disabled; `aria-describedby=grade-input-hint`. | Không có `min`, `max`, `step` hoặc giá trị mặc định; hint nói thang điểm đang thiết lập nhưng #55 không trả `max_score`. | E03; hiện không tương tác được |
| 26 / ME10-EL-26 | Rubric heading và `0 / 0 Tiêu chí`. | Static count; không source từ #55; #56 `rubric_items` không persisted. | Không có rubric event; E05 bị block |
| 27 / ME10-EL-27 | Rubric empty card, “Chưa có rubric tự động”. | Mockup copy; #55 không trả rubric, nên không đủ bằng chứng rằng đây là true empty state. | E01; rubric load blocked |
| 28 / ME10-EL-28 | Label “Nhận xét của giảng viên” và `0 ký tự`. | Label `for="mentor-comments"`; counter local. Không có max/required rule trong HTML. | E04 |
| 29 / ME10-EL-29 | Textarea `id=mentor-comments`, `rows=6`, placeholder tiếng Việt; no maxlength. | Editable trong HTML. Không có sanitize/save/network logic. | E04 |
| 30 / ME10-EL-30 | Hint khuyến khích dẫn chứng và “Markdown hỗ trợ”. | Copy tĩnh; không có Markdown renderer/library trong asset. | Không có event |
| 31 / ME10-EL-31 | Security warning “tạm khóa cho tới khi phiên… xác thực hợp lệ”. | Static warning; route/auth session UI không được wire. Backend guard vẫn là authority. | E01/E05/E06 |
| 32 / ME10-EL-32 | Nút “Lưu điểm số và gửi nhận xét”. | Disabled; `aria-disabled=true`, `type=button`; kết hợp hai API tách. | E05/E06 only after split/contract approval; hiện không có click event. |
| 33 / ME10-EL-33 | Link quay lại ME-09 phía dưới form. | Anchor focus style; `href="#"`; không xác định history/cache behavior. | E08 |
| 34 / ME10-EL-34 | Status “Chữ ký số xác nhận: PENDING_AUTH”. | Giá trị mẫu, không được xác minh bởi #55–#57. | Không có event |
| 35 / ME10-EL-35 | Version `v2.4.1`. | Static build/version text; không chứng minh version ứng dụng đang chạy. | Không có event |
| 36 / ME10-EL-36 | Footer logo/copyright/WCAG copy. | Static; ngày, ownership và compliance chưa xác minh. | Không có event |
| 37 / ME10-EL-37 | Link “Quy chế Giảng viên”. | `href="#"`; destination/document chưa biết. | E10 |
| 38 / ME10-EL-38 | Link “Tiêu chuẩn đánh giá”. | `href="#"`; không phải nguồn rubric đã wire. | E10 |
| 39 / ME10-EL-39 | Link “Hỗ trợ kỹ thuật”. | `href="#"`; contact destination chưa biết. | E10 |

## 4. Conditional UI & state variations
- States theo inventory: loading/dirty/grading/feedback-sent/conflict
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/04_mentor/ME-10_cham-diem-va-phan-hoi/ME-10.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
