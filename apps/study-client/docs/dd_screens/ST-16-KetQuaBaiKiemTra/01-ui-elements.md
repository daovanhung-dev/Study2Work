# ST-16 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-16_markers.json](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/ST-16_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-16-EL-001` | `ST16-EL-01` | Study2Work logo and portal brand |
| #2 | `ST-16-EL-002` | `ST16-EL-02` | Global search input |
| #3 | `ST-16-EL-003` | `ST16-EL-03` | Primary navigation links |
| #4 | `ST-16-EL-004` | `ST16-EL-04` | Notifications control |
| #5 | `ST-16-EL-005` | `ST16-EL-05` | Student profile control |
| #6 | `ST-16-EL-006` | `ST16-EL-06` | Breadcrumb trail |
| #7 | `ST-16-EL-007` | `ST16-EL-07` | Pass/result status badge |
| #8 | `ST-16-EL-008` | `ST16-EL-08` | Skill category eyebrow |
| #9 | `ST-16-EL-009` | `ST16-EL-09` | Quiz result title |
| #10 | `ST-16-EL-010` | `ST16-EL-10` | Duration, submission time and attempt ordinal |
| #11 | `ST-16-EL-011` | `ST16-EL-11` | Next-lesson unlock claim card |
| #12 | `ST-16-EL-012` | `ST16-EL-12` | Score gauge, percent and answered denominator |
| #13 | `ST-16-EL-013` | `ST16-EL-13` | Points score |
| #14 | `ST-16-EL-014` | `ST16-EL-14` | Grade/GPA label |
| #15 | `ST-16-EL-015` | `ST16-EL-15` | Skill analysis heading |
| #16 | `ST-16-EL-016` | `ST16-EL-16` | Skill framework/data note |
| #17 | `ST-16-EL-017` | `ST16-EL-17` | Hook Core skill card |
| #18 | `ST-16-EL-018` | `ST16-EL-18` | Performance and memory skill card |
| #19 | `ST-16-EL-019` | `ST16-EL-19` | Next-gen React skill card |
| #20 | `ST-16-EL-020` | `ST16-EL-20` | Answer review heading |
| #21 | `ST-16-EL-021` | `ST16-EL-21` | All questions filter |
| #22 | `ST-16-EL-022` | `ST16-EL-22` | Correct answers filter |
| #23 | `ST-16-EL-023` | `ST16-EL-23` | Needs review filter |
| #24 | `ST-16-EL-024` | `ST16-EL-24` | Question 14 status, topic and difficulty |
| #25 | `ST-16-EL-025` | `ST16-EL-25` | Question 14 prompt |
| #26 | `ST-16-EL-026` | `ST16-EL-26` | Question 14 answer options and selected/correct state |
| #27 | `ST-16-EL-027` | `ST16-EL-27` | Question 14 instructor explanation |
| #28 | `ST-16-EL-028` | `ST16-EL-28` | Question 19 status and topic |
| #29 | `ST-16-EL-029` | `ST16-EL-29` | Question 19 prompt |
| #30 | `ST-16-EL-030` | `ST16-EL-30` | Question 19 selected incorrect answer |
| #31 | `ST-16-EL-031` | `ST16-EL-31` | Question 19 correct answer and explanation |
| #32 | `ST-16-EL-032` | `ST16-EL-32` | Question 19 instructor feedback/video reference |
| #33 | `ST-16-EL-033` | `ST16-EL-33` | Next-module recommendation panel |
| #34 | `ST-16-EL-034` | `ST16-EL-34` | Download PDF action |
| #35 | `ST-16-EL-035` | `ST16-EL-35` | Review-course-outline action |
| #36 | `ST-16-EL-036` | `ST16-EL-36` | Continue to next lesson action |
| #37 | `ST-16-EL-037` | `ST16-EL-37` | Footer brand and certification badges |
| #38 | `ST-16-EL-038` | `ST16-EL-38` | Footer navigation and legal links |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả element

Marker badges được đặt trong gutter trắng của ảnh chú thích; `x/y` trong [marker map](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/ST-16_markers.json) là vị trí phần tử trên ảnh nguồn 846×1600. Giá trị nhìn thấy trong PNG là sample, trừ khi nguồn được chỉ rõ.

| # / Element ID | Tên, loại, vùng và mục đích | Data/thuộc tính, điều kiện và trạng thái | Sự kiện |
|---|---|---|---|
| 1 / `ST16-EL-01` | Brand/logo Study2Work ở header trái. | Static brand trong PNG; không có app shell runtime hiện tại. | — |
| 2 / `ST16-EL-02` | Global search input. | Không thuộc API #32; placeholder là sample. Search submit/navigation không được screen contract định nghĩa. | `EV-06` |
| 3 / `ST16-EL-03` | Nhóm link điều hướng header: Trang chủ, Khóa học, Khóa học của tôi, Tiến độ, Lộ trình, Diễn đàn. | Destinations chỉ là HTML/mockup links; auth gating và route behavior chưa được verify. | `EV-06` |
| 4 / `ST16-EL-04` | Notification icon/badge. | Notification count/destination không có source trong #32; design-only. | `EV-06` |
| 5 / `ST16-EL-05` | Student profile/avatar/name. | “Nguyen Hanh / Học viên” là sample. Identity phải đến từ auth/profile source khác khi được nối; không dùng làm owner proof. | `EV-06` |
| 6 / `ST16-EL-06` | Breadcrumb: Khóa học của tôi → Chuyên gia Frontend React & TypeScript → Kết quả Quiz #02. | Course/quiz labels không có trong #32 response (chỉ có `quiz_id`); các crumb links chưa có contract. | `EV-06` |
| 7 / `ST16-EL-07` | Pass badge “Chúc mừng bạn đã đạt chuẩn đầu ra (PASSED)”. | Pass state/threshold không được #32 định nghĩa. Không render PASSED từ `GRADED` hoặc sample score. | `EV-02` |
| 8 / `ST16-EL-08` | Eyebrow “ĐÁNH GIÁ KỸ NĂNG CHUYÊN SÂU”. | Copy mẫu; không có skill-assessment field trong `QuizAttempt`. | — |
| 9 / `ST16-EL-09` | Heading kết quả và quiz title. | “React Hooks & Re-render Benchmark” là sample; #32 response không có title. | — |
| 10 / `ST16-EL-10` | Metadata thời lượng hoàn thành, ngày nộp và số lần làm. | `submitted_at?` là field logical optional; duration/attempt ordinal không có trong #32. Timestamp timezone/format và derived duration chưa chốt. PNG values are sample. | `EV-02` |
| 11 / `ST16-EL-11` | “Đã mở khóa bài học tiếp theo” banner và ngưỡng 80%. | Không có pass threshold/progress/unlock field/API trong ST-16 contract. Không mở khóa hoặc điều hướng dựa trên copy. | — |
| 12 / `ST16-EL-12` | Score gauge 90% và `18/20 câu đúng`. | Gauge/formula/denominator không có trong response schema. Không suy ra từ `score` nếu scale và total chưa chốt. | `EV-02` |
| 13 / `ST16-EL-13` | Điểm quy đổi `9.0/10`. | `QuizAttempt.score?` là candidate raw aggregate; scale, rounding, max score và permission chưa chốt. Value is sample. | `EV-02` |
| 14 / `ST16-EL-14` | Xếp loại `GPA A+`. | Không có GPA mapping/field/threshold trong #32 hoặc AC-16; không tính phía client. | `EV-02` |
| 15 / `ST16-EL-15` | Heading báo cáo mức độ thành thạo kỹ năng. | Tĩnh trong mockup; no skill analytics source. | — |
| 16 / `ST16-EL-16` | Badge dữ liệu theo “Khung năng lực Frontend 2026”. | Framework/version claim không có contract hoặc API #32 field. | — |
| 17 / `ST16-EL-17` | Skill card “Module Hook Core”: level, description, correct count and bar. | Mọi metric/copy là sample; không có skill mapping/aggregation source trong #32. | — |
| 18 / `ST16-EL-18` | Skill card “Hiệu năng & Bộ nhớ”. | Mọi metric/copy là sample; không có skill mapping/aggregation source trong #32. | — |
| 19 / `ST16-EL-19` | Skill card “Next-gen React 19”. | Mọi metric/copy là sample; không có skill mapping/aggregation source trong #32. | — |
| 20 / `ST16-EL-20` | Heading “Chi tiết bài làm và giải thích từ Giảng viên”. | AC-16 nhắc feedback, nhưng feedback field/source chưa có; heading không chứng minh nội dung có thể đọc. | `EV-03` |
| 21 / `ST16-EL-21` | Filter “Tất cả câu hỏi (20)”. | Count sample; client filter chỉ khả thi khi questions/answer collection và ordering được chốt. | `EV-03` |
| 22 / `ST16-EL-22` | Filter “Câu trả lời đúng (18)”. | Correctness và disclosure policy là Q-32-03; không filter/đếm cho tới khi được duyệt. | `EV-03` |
| 23 / `ST16-EL-23` | Filter “Cần rút kinh nghiệm (2)”. | Definition của “cần rút kinh nghiệm” và count không có trong contract. Không đồng nhất với incorrect khi chưa có rule. | `EV-03` |
| 24 / `ST16-EL-24` | Question 14 header: topic, difficulty, đúng/+1.0 điểm. | `QuizAnswer.question_id` có thể tồn tại; topic/difficulty/correctness/point không được #32 projection chốt. Values are sample. | `EV-03` |
| 25 / `ST16-EL-25` | Question 14 prompt. | Question text không thuộc `QuizAttempt`; không gọi #28 ngầm để hydrate. | `EV-03` |
| 26 / `ST16-EL-26` | Question 14 option group A–D, selected/correct highlight. | `choice_ids?` logical optional; text/order/selected mapping và disclosure không chốt. Không lấy answer key từ `quiz_choices.is_correct`. | `EV-03` |
| 27 / `ST16-EL-27` | Instructor explanation cho Question 14. | Không có feedback field ở reusable schema/candidate tables; source/permission chưa có. | `EV-03` |
| 28 / `ST16-EL-28` | Question 19 header: topic và “Cần ôn tập kỹ lại”. | Status/category/rating are sample; no per-question remediation field in #32. | `EV-03` |
| 29 / `ST16-EL-29` | Question 19 prompt. | Question text absent from #32 response; source for result review is not defined. | `EV-03` |
| 30 / `ST16-EL-30` | Answer B được chọn và bị đánh sai. | `choice_ids?` may identify a selected choice after schema resolution; `correct?` policy is unresolved. Do not expose before approval. | `EV-03` |
| 31 / `ST16-EL-31` | Correct answer C and explanation. | Answer key is not in #32 logical response and must not be inferred from `quiz_choices.is_correct`; disclosure is open even after GRADED. | `EV-03` |
| 32 / `ST16-EL-32` | Mentor feedback, video reference and duration for Question 19. | No feedback/video field or access contract in #32; design-only. | `EV-03` |
| 33 / `ST16-EL-33` | Next-module journey recommendation card/title. | Module/course progression, completion percentage and next-lesson state have no source in #32. | `EV-04` |
| 34 / `ST16-EL-34` | “Tải chứng nhận PDF” action. | No certificate or report API/file contract in ST-16; do not generate/download a file by implication. | `EV-04` |
| 35 / `ST16-EL-35` | “Xem lại đề cương” action. | Possible relation to ST-09 is not an approved route mapping. Destination/return context unresolved. | `EV-04` |
| 36 / `ST16-EL-36` | “Tiếp tục bài học tiếp theo” action. | Next lesson/access and progress APIs are outside ST-16 row; eligibility/destination not specified. Do not mark lesson complete or navigate automatically. | `EV-04` |
| 37 / `ST16-EL-37` | Footer Study2Work identity and certification badges. | Static marketing/certification claims; no result-data source. | — |
| 38 / `ST16-EL-38` | Footer navigation/legal link groups. | Static HTML/mockup links include `#` placeholders; destination/content policy not verified. | `EV-06` |

## 4. Conditional UI & state variations
- States theo inventory: pending/graded/unavailable/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/ST-16.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
