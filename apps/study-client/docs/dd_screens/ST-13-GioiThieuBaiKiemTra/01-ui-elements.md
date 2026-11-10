# ST-13 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-13_markers.json](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/ST-13_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-13-EL-001` | `ST13-EL-01` | Brand and header |
| #2 | `ST-13-EL-002` | `ST13-EL-02` | Global search |
| #3 | `ST-13-EL-003` | `ST13-EL-03` | Primary navigation |
| #4 | `ST-13-EL-004` | `ST13-EL-04` | Notifications and account |
| #5 | `ST-13-EL-005` | `ST13-EL-05` | Breadcrumb |
| #6 | `ST-13-EL-006` | `ST13-EL-06` | Quiz labels |
| #7 | `ST-13-EL-007` | `ST13-EL-07` | Quiz title |
| #8 | `ST-13-EL-008` | `ST13-EL-08` | Instructor card |
| #9 | `ST-13-EL-009` | `ST13-EL-09` | Quiz cover preview |
| #10 | `ST-13-EL-010` | `ST13-EL-10` | Quiz status and attempt badge |
| #11 | `ST-13-EL-011` | `ST13-EL-11` | Passing goal panel |
| #12 | `ST-13-EL-012` | `ST13-EL-12` | Question count metric |
| #13 | `ST-13-EL-013` | `ST13-EL-13` | Duration metric |
| #14 | `ST-13-EL-014` | `ST13-EL-14` | Passing score metric |
| #15 | `ST-13-EL-015` | `ST13-EL-15` | Available attempts metric |
| #16 | `ST-13-EL-016` | `ST13-EL-16` | Start attempt button |
| #17 | `ST-13-EL-017` | `ST13-EL-17` | Review lesson CTA |
| #18 | `ST-13-EL-018` | `ST13-EL-18` | Certification and validity note |
| #19 | `ST-13-EL-019` | `ST13-EL-19` | Academic support card |
| #20 | `ST-13-EL-020` | `ST13-EL-20` | Rules heading |
| #21 | `ST-13-EL-021` | `ST13-EL-21` | Proctoring and security notice |
| #22 | `ST-13-EL-022` | `ST13-EL-22` | Scoring rule card |
| #23 | `ST-13-EL-023` | `ST13-EL-23` | Automatic submission card |
| #24 | `ST-13-EL-024` | `ST13-EL-24` | Certificate card |
| #25 | `ST-13-EL-025` | `ST13-EL-25` | Attempt history heading and count |
| #26 | `ST-13-EL-026` | `ST13-EL-26` | Previous attempt summary row |
| #27 | `ST-13-EL-027` | `ST13-EL-27` | Review previous attempt button |
| #28 | `ST-13-EL-028` | `ST13-EL-28` | Footer brand, description and badges |
| #29 | `ST-13-EL-029` | `ST13-EL-29` | Footer navigation columns |
| #30 | `ST-13-EL-030` | `ST13-EL-30` | Footer copyright and tagline |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả element

Ảnh đánh số theo [marker map](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/ST-13_markers.json). Marker gom các text/icon thuộc cùng một component. Nội dung định lượng/trạng thái trong mockup là **visual sample**, không phải default/business rule.

| # / Element ID | Tên, loại, vị trí và mục đích | Thuộc tính, nguồn dữ liệu, validation | Điều kiện/trạng thái | Sự kiện |
|---|---|---|---|---|
| 1 `ST13-EL-01` | Brand “Study2Work LMS” và thanh header; logo/brand ở đầu trang. | Logo/tên là asset tĩnh. Không có API mapping. | Visible trong ảnh; link runtime chưa xác minh. | EV-05 nếu kích hoạt. |
| 2 `ST13-EL-02` | Ô tìm kiếm toàn cục; input trên header. | Placeholder là text mockup; query string, required, giới hạn, debounce và API search chưa được định nghĩa cho ST-13. Không tự gửi search. | Visible; focus/loading/result state chưa có trong source. | Hành vi chưa có contract; EV-05 ghi nhận. |
| 3 `ST13-EL-03` | Nhóm navigation chính; các link Trang chủ, Khóa học, Khóa học của tôi, Lộ trình học, Diễn đàn. | Screenshot không cung cấp route/href cho các link này; không có query/state contract. | Visible trên ảnh desktop; responsive/mobile menu chưa được thiết kế trong asset. | EV-05. |
| 4 `ST13-EL-04` | Notification bell và account/avatar. | Badge đỏ, tên “Nguyen Hanh”, role “Học viên” là dữ liệu hình ảnh; không có notification/profile API mapping trong ST-13 contract. | Visible/static; unread state, menu, auth expiry và click state chưa xác nhận. | EV-05; destination chưa xác nhận. |
| 5 `ST13-EL-05` | Breadcrumb từ Khóa học của tôi → course → chapter → quiz. | Các tên là copy trong PNG; `courseId`, `lessonId`, `quizId` nguồn và link/handoff không có đủ trong route/API contract. | Visible/static; không khẳng định các cấp breadcrumb điều hướng được. | EV-05. |
| 6 `ST13-EL-06` | Nhóm quiz badges: “QUIZ #02”, bắt buộc qua môn, GPA weight, Enterprise. | Các giá trị/copy chưa có field tương ứng trong Quiz catalog response; `#02` không phải `quiz_id` đã xác minh. | Visual sample; không dùng để authorize/enable Start. | Không có event nguồn. |
| 7 `ST13-EL-07` | Heading tên quiz. | Visual text mẫu. Field thiết kế có thể map là `Quiz.title` từ #28 khi response contract được duyệt; type/empty rule vẫn cần theo API schema. | Visible; loading/empty/error variant không có asset. | EV-01 tải dữ liệu. |
| 8 `ST13-EL-08` | Instructor card: avatar, tên, chức danh. | Không có instructor field trong logical Quiz #28 được rà soát; không tự gọi API khác hoặc lấy tên từ user session. | Visible/static trong PNG; không xác nhận người dạy thực tế. | Không có event nguồn. |
| 9 `ST13-EL-09` | Cover/preview hình quiz và caption. | Asset/caption tĩnh; không có `cover_url` trong logical Quiz #28 đã rà soát. URL nguồn, alt text và quyền tải chưa được cung cấp. | Visible trong PNG; không có loading/broken-image state. | Không có event nguồn. |
| 10 `ST13-EL-10` | Badge trạng thái “Sẵn sàng làm bài (Lần 2/3)”. | Trạng thái, current attempt ordinal và max attempts không có trong logical response #28; limit chưa có business rule. | Visual sample, không xác định `available/closed`. | EV-01; mapping còn blocked. |
| 11 `ST13-EL-11` | Goal panel, progress bar và “16/20 câu”, “80%”. | #28 có `passing_score` trong API DD, nhưng scale, display/rounding và công thức câu đạt chưa chốt. `16/20` không được tự tính. Không có attempt-progress source trong ST-13. | Visual sample; không hiển thị như số liệu đã tải. | EV-01; mapping còn blocked. |
| 12 `ST13-EL-12` | Metric số câu hỏi. | “20 câu” là sample. Chỉ được tính từ question collection nếu response shape và count semantics được chốt; không tự đếm phần tử từ schema hiện chưa hoàn chỉnh. | Visual sample; empty/loading/error state chưa có. | EV-01. |
| 13 `ST13-EL-13` | Metric thời lượng. | “30 phút” là sample. `duration_minutes` optional trong logical Quiz; null/omit và đơn vị/serialization cần theo API #28; không suy ra deadline hoặc countdown source. | Visual sample; timer semantics chưa được quyết định. | EV-01. |
| 14 `ST13-EL-14` | Metric điểm đạt tối thiểu. | “80%” là sample. Có thể tương ứng `passing_score`, nhưng scale/decimal formatting, rounding và relation với điểm câu hỏi còn mở. | Visual sample; không tự tính “≥16/20”. | EV-01. |
| 15 `ST13-EL-15` | Metric số lượt khả dụng. | “2/3” và “Còn lại 2 lần” là sample; API #28 logical schema không định nghĩa attempt summary/limit. | Visual sample; availability phụ thuộc policy chưa có. | EV-01. |
| 16 `ST13-EL-16` | Primary button “Bắt đầu làm bài ngay (Attempt 2)”. | “Attempt 2” không được lấy làm request field; API #29 chỉ có `quiz_id` path, không body/query. Disabled/loading/double-click/idempotency rules chưa chốt. | Button có vẻ enabled trong mockup; đó không phải runtime enablement. Chỉ request sau explicit click. | EV-02. |
| 17 `ST13-EL-17` | CTA “Ôn tập lại bài giảng trước khi thi”. | Không có lesson ID/handoff trong ST-13 route/inventory; không xác nhận ST-11 đích. | Destination và browser history behavior chưa xác định. | EV-03 (blocked). |
| 18 `ST13-EL-18` | Note về EdTech ISO, bảo mật và kết quả hợp lệ. | Claims/certification copy tĩnh; không có API/approval/evidence trong nguồn được rà soát. | Không trình bày như chứng nhận hệ thống đã đạt. | Không có event nguồn. |
| 19 `ST13-EL-19` | Academic support card và link “Hỏi trực tiếp Mentor trên Diễn đàn”. | Mentor/forum destination, course context và role access chưa được cung cấp. | Link có trong PNG; target/action chưa xác nhận. | EV-05. |
| 20 `ST13-EL-20` | Heading “Quy định & Hướng dẫn làm bài chi tiết”. | Text tĩnh, không có API mapping. | Visible; không xác nhận policy bên dưới đã duyệt. | Không có event nguồn. |
| 21 `ST13-EL-21` | Proctor/security notice, gồm cấm thu nhỏ/tab, “Auto-save API #30”, realtime webhook và phục hồi mất mạng. | Tất cả là visual copy. API #30 catalog là PUT answers, nhưng không có webhook/realtime spec, tab detection, reconnect protocol hay security policy trong contract được rà soát. | Không coi là guard, autosave hoặc bảo mật đang hoạt động. | Không phát sinh timer/listener theo copy; chưa có event được xác nhận. |
| 22 `ST13-EL-22` | Scoring rule card: điểm mỗi câu, chuyên đề, không trừ điểm. | Policy/formula chưa được AC-16/API #28 logical schema chốt; `quiz_questions.score` trong DDL chỉ là candidate column, không xác nhận grading rule. | Visual sample; không dùng làm phép tính. | Không có event nguồn. |
| 23 `ST13-EL-23` | Auto-submit card: tự nộp khi timer về 00:00 và lưu toàn bộ đáp án. | Auto-submit, timer source/timezone/clock authority, answer flush và expiry transition chưa có contract. | Static copy; không tạo timer ở ST-13. | Không tạo timer/API event theo copy. |
| 24 `ST13-EL-24` | Certificate/transcript card. | Transcript, certification generation và employer sharing không thuộc response #28/#29 được rà soát; không có opt-in/privacy contract. | Static claim; không xác nhận certificate. | Không có event nguồn. |
| 25 `ST13-EL-25` | Heading lịch sử attempt và count “1/3 lần đã thực hiện”. | History/count không được định nghĩa trong Quiz #28 logical schema; không có list endpoint trong ST-13 inventory. | Visual sample; no-history/empty state chưa được thiết kế. | EV-01 (data source absent). |
| 26 `ST13-EL-26` | Previous attempt row: lần 01, điểm, trạng thái, submitted timestamp, duration. | Các giá trị mẫu không có trong #28 response; status/score/history ownership chưa được nối với API #32. | Visual sample; không thể xác nhận trạng thái “Chưa đạt” hoặc elapsed time. | EV-04 context. |
| 27 `ST13-EL-27` | Button “Xem lại bài làm”. | Không có route/attempt ID/access rule từ ST-13. API #32 là result theo attempt ID trong AC-16, nhưng inventory gắn API #32 với ST-16; không suy ra button này gọi #32. | Destination và effect chưa xác nhận. | EV-04 (blocked). |
| 28 `ST13-EL-28` | Footer brand, mô tả nền tảng và badge chứng nhận. | Copy/logo tĩnh; không có API data source. Các chứng nhận không được xác nhận từ asset. | Visible; link/logo behavior chưa xác minh. | EV-05 nếu link kích hoạt. |
| 29 `ST13-EL-29` | Ba nhóm footer navigation: Học tập, Cộng đồng, Hỗ trợ & Pháp lý. | Screenshot không cho href/destination; danh sách link không phải route contract. | Visible/static; responsive behavior chưa được cung cấp. | EV-05. |
| 30 `ST13-EL-30` | Copyright và tagline cuối trang. | Text tĩnh, năm/copy trong ảnh; không có data/API. | Visible/static. | Không có event nguồn. |

### Quy tắc thiết kế UI dùng chung

[Study Web Design System](../../../../../.agents/web-study/design.md) là intended design target, không phải runtime proof: dùng ocean semantic tokens; điều khiển ≥44px; focus-visible và keyboard order; trạng thái không chỉ phân biệt bằng màu; reflow desktop/tablet/mobile tới 320px; alt text và reduced-motion. PNG hiện tại là desktop mockup, không xác nhận đã đạt các yêu cầu này.

## 4. Conditional UI & state variations
- States theo inventory: loading/closed/available/denied
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/ST-13.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
