# ST-14 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-14_markers.json](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra/ST-14_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-14-EL-001` | `ST14-EL-01` | Thoát bài thi |
| #2 | `ST-14-EL-002` | `ST14-EL-02` | Thương hiệu Study2Work Exam |
| #3 | `ST-14-EL-003` | `ST14-EL-03` | Đồng hồ header còn lại |
| #4 | `ST-14-EL-004` | `ST14-EL-04` | Hồ sơ người học |
| #5 | `ST-14-EL-005` | `ST14-EL-05` | Nút quay lại |
| #6 | `ST-14-EL-006` | `ST14-EL-06` | Tiêu đề quiz |
| #7 | `ST-14-EL-007` | `ST14-EL-07` | Tên kỳ thi và khóa học |
| #8 | `ST-14-EL-008` | `ST14-EL-08` | Badge lần làm |
| #9 | `ST-14-EL-009` | `ST14-EL-09` | Đồng hồ thời gian trong bài |
| #10 | `ST-14-EL-010` | `ST14-EL-10` | Trạng thái tự động lưu API 30 |
| #11 | `ST-14-EL-011` | `ST14-EL-11` | Tiến độ câu hỏi |
| #12 | `ST-14-EL-012` | `ST14-EL-12` | Nút nộp bài kiểm tra |
| #13 | `ST-14-EL-013` | `ST14-EL-13` | Câu hiện tại và tổng câu |
| #14 | `ST-14-EL-014` | `ST14-EL-14` | Điểm câu hỏi |
| #15 | `ST-14-EL-015` | `ST14-EL-15` | Tag chủ đề câu hỏi |
| #16 | `ST-14-EL-016` | `ST14-EL-16` | Nội dung câu hỏi |
| #17 | `ST-14-EL-017` | `ST14-EL-17` | Code snippet |
| #18 | `ST-14-EL-018` | `ST14-EL-18` | Lựa chọn A đang chọn |
| #19 | `ST-14-EL-019` | `ST14-EL-19` | Lựa chọn B |
| #20 | `ST-14-EL-020` | `ST14-EL-20` | Lựa chọn C |
| #21 | `ST-14-EL-021` | `ST14-EL-21` | Lựa chọn D |
| #22 | `ST-14-EL-022` | `ST14-EL-22` | Câu trước |
| #23 | `ST-14-EL-023` | `ST14-EL-23` | Gắn cờ xem lại |
| #24 | `ST-14-EL-024` | `ST14-EL-24` | Câu tiếp theo |
| #25 | `ST-14-EL-025` | `ST14-EL-25` | Chú giải phím tắt |
| #26 | `ST-14-EL-026` | `ST14-EL-26` | Tiêu đề danh sách câu |
| #27 | `ST-14-EL-027` | `ST14-EL-27` | Nhãn phần Hooks |
| #28 | `ST-14-EL-028` | `ST14-EL-28` | Tổng hợp đã trả lời chưa làm và gắn cờ |
| #29 | `ST-14-EL-029` | `ST14-EL-29` | Lưới chọn câu 1 đến 20 |
| #30 | `ST-14-EL-030` | `ST14-EL-30` | Lọc câu chưa trả lời |
| #31 | `ST-14-EL-031` | `ST14-EL-31` | Trạng thái kết nối và autosave |
| #32 | `ST-14-EL-032` | `ST14-EL-32` | Thẻ giảng viên chấm |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả element

`Element ID` khớp marker và số trong [ST-14_markers.json](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra/ST-14_markers.json), [overlay SVG](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra/ST-14_markers_overlay.svg) và [ảnh chú thích](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra/screen_annotated.png). Giá trị trong PNG là ví dụ thiết kế, không phải default backend.

| ID / marker | Tên, loại, vị trí và mục đích | Thuộc tính, nguồn dữ liệu, hiển thị/trạng thái và event |
|---|---|---|
| ST14-EL-01 / #1 | Link/button “Thoát bài thi”; góc header trên trái; rời phiên làm. | Text/icon tĩnh trong PNG. Destination, confirm khi có answer chưa lưu, history/back và giữ state chưa có contract. Visible trên mockup; event ST14-EV-08. |
| ST14-EL-02 / #2 | Brand/logo “Study2Work Exam”; header. | Asset/copy tĩnh; không có data/API. Không suy ra logo link destination hoặc route. Static; không có event đã xác nhận. |
| ST14-EL-03 / #3 | Pill countdown “45:20 còn lại”; header phải. | Giá trị mẫu; không có `deadline_at`, duration source hoặc clock protocol xác nhận. Chỉ visible nếu time contract được duyệt; nếu không, ẩn/không hiển thị. ST14-EV-06. |
| ST14-EL-04 / #4 | Avatar/tên “Nguyen Hanh”; góc phải header. | Profile source chưa xác định trong Quiz/Attempt contract; tên/avatar trong ảnh là sample. Display-only cho tới khi source/auth profile mapping chốt; click destination chưa xác nhận. |
| ST14-EL-05 / #5 | Icon back ở toolbar thứ hai; quay khỏi header row. | Destination và khác biệt so với EL-01 chưa xác định. Không tự áp browser history nếu dirty state; event ST14-EV-08. |
| ST14-EL-06 / #6 | Quiz title “Quiz 02: React Hooks & Re-render …”. | Candidate source `Quiz.title` từ #28; string limit/truncation/a11y label chưa ghi trong contract. Loading/error state theo #28; display-only. |
| ST14-EL-07 / #7 | Course/exam subtitle và status dot. | Quiz logical schema chỉ có `course_id`, chưa có course title/exam session/status color mapping. Copy sample không phải contract. State/source blocked; không xác định dot nghĩa là “đang mở”. |
| ST14-EL-08 / #8 | Badge `Attempt 2/3`. | Không có attempt ordinal/limit trong route hoặc `QuizAttempt` schema; giá trị sample. Chỉ render khi response contract có source được duyệt; hiện không thể bind. |
| ST14-EL-09 / #9 | Khối timer `18:39 thời gian` trong toolbar. | Đồng hồ mẫu thứ hai, khác EL-03; không có nguồn/server timestamp. Không quyết định elapsed vs remaining, pause behavior hoặc hết hạn. ST14-EV-06. |
| ST14-EL-10 / #10 | Autosave indicator “API #30: Đã đồng bộ 2 giây trước”. | Candidate state dựa trên request lifecycle #30, nhưng #30 chưa runnable; response không có `saved_at` đã chốt. Không hiển thị success/time trước khi API 200 thực sự được xác minh. ST14-EV-03. |
| ST14-EL-11 / #11 | Tiến độ `14/20 (70%)` và progress bar. | Total có thể lấy từ `Quiz.questions.length` sau schema xác nhận; numerator/formula, question answered semantics và stale count chưa chốt. PNG mâu thuẫn với summary bên phải. ST14-EV-04. |
| ST14-EL-12 / #12 | Button “Nộp bài kiểm tra”. | Trigger tới ST-15 theo inventory; không gọi #31 trong ST-14. Disabled/loading behavior khi save pending chưa được owner chốt. Event ST14-EV-07. |
| ST14-EL-13 / #13 | Current question label “Câu hỏi 14 / 20”. | `currentQuestionId/index` là screen state; total từ Quiz response nếu được xác nhận. `14` chỉ là screenshot sample. ST14-EV-04. |
| ST14-EL-14 / #14 | Badge điểm câu `1.0 điểm`. | Không có point field trong logical `QuizQuestion` được trích từ catalog; không suy ra grading/weight. Chỉ render sau contract bổ sung. |
| ST14-EL-15 / #15 | Tag “Phân tích Code Snippet React 19”. | Không có category/tag field trong QuizQuestion schema hiện có; copy sample. Không tạo filter/data rule từ tag. |
| ST14-EL-16 / #16 | Text prompt câu hỏi. | Candidate `QuizQuestion.text` từ #28. Markdown/HTML/code rendering, length và sanitization contract chưa mô tả; không thực thi embedded markup theo suy đoán. Visible khi question data hợp lệ; loading/error theo #28. |
| ST14-EL-17 / #17 | Code snippet block, tên file/line labels. | Có trong PNG; QuizQuestion schema chỉ nêu `text`, chưa có code field/format/syntax language. Cách tách code khỏi text và preserve formatting cần chốt. |
| ST14-EL-18 / #18 | Choice A, selected trong ảnh. | Candidate từ `QuizQuestion.choices`; `QuizChoice` schema/type/order chưa hoàn chỉnh. Selected state cần server answer hoặc state cục bộ mới; `A`/selected là sample. Event ST14-EV-03/09. |
| ST14-EL-19 / #19 | Choice B. | Cùng schema/state rules với A; text `B` là sample. Selection cardinality (single/multi/text) chưa được xác nhận. ST14-EV-03/09. |
| ST14-EL-20 / #20 | Choice C. | Cùng schema/state rules; không hiển thị correctness/score. ST14-EV-03/09. |
| ST14-EL-21 / #21 | Choice D. | Cùng schema/state rules; không giả định luôn có đúng bốn lựa chọn. ST14-EV-03/09. |
| ST14-EL-22 / #22 | Button “Câu trước”. | Local navigation trong câu hỏi đã tải; disabled condition khi đầu danh sách cần xác nhận. Không tự gọi API. ST14-EV-04/09. |
| ST14-EL-23 / #23 | Button “Đánh dấu xem lại sau (Flag)”. | Toggle flag state mẫu; không có field/API # nào trong inventory để persist flag. Reload persistence, visual state, filter interplay chưa chốt. ST14-EV-05/09. |
| ST14-EL-24 / #24 | Button “Câu tiếp theo”. | Local navigation; behavior ở câu cuối phải chờ quyết định, không tự biến thành submit. ST14-EV-04/09. |
| ST14-EL-25 / #25 | Help bar keyboard shortcuts `1–4`, `→`, `P`. | Static instructions trong PNG; mapping choice/order và key focus policy chưa có source. Chỉ công bố phím được triển khai; event ST14-EV-09. |
| ST14-EL-26 / #26 | Heading “Danh sách 20 câu hỏi”. | Candidate total từ Quiz.questions khi response/order được chốt. 20 là sample; visible với panel; không chứng minh có đủ 20 API records. |
| ST14-EL-27 / #27 | Section chip “Phần 1: Hooks”. | Không có section/part field trong logical QuizQuestion/Quiz schema đã xác nhận. Static sample; không tạo grouping logic. |
| ST14-EL-28 / #28 | Summary counters: đã trả lời, chưa làm, gắn cờ. | `13`, `6`, `1` là sample; chưa có projection answers/flag. Các category có thể overlap; tổng/denominator và khi nào cập nhật chưa chốt. ST14-EV-04/05. |
| ST14-EL-29 / #29 | Question grid 1–20, current/answered/unanswered/flagged styles. | Candidate IDs/order từ #28 questions; state từ attempt answers/flags chưa có restore source. Click chọn câu là local navigation; visual state hiện tại mẫu. ST14-EV-04. |
| ST14-EL-30 / #30 | Filter “Lọc câu chưa trả lời (6 câu)”. | Input là collection of unanswered questions, phụ thuộc câu trả lời đã lưu/dirty và công thức chưa chốt. Không thay đổi dữ liệu; behavior khi filter rỗng/chọn câu chưa trả lời cần xác định. ST14-EV-04. |
| ST14-EL-31 / #31 | Card online/WebSocket ping/autosave. | PNG claim “Trực tuyến”, `18ms`, idempotent autosave; không có WebSocket/ping protocol, telemetry API hay runtime. Không hiển thị như fact nếu chưa có contract. ST14-EV-10. |
| ST14-EL-32 / #32 | Instructor grading card/avatar/name/title. | Không có instructor/profile relationship trong Quiz/Attempt response contract được kiểm tra. Sample content; không hiển thị dynamic card nếu thiếu source/permission policy. |

## 4. Conditional UI & state variations
- States theo inventory: unsaved/saving/saved/retrying/expired
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-14_lam-bai-kiem-tra/ST-14.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
