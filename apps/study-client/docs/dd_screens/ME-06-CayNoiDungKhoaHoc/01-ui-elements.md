# ME-06 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ME-06_markers.json](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/ME-06_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ME-06-EL-001` | `ME06-EL-01` | Logo Study2Work Mentor Portal |
| #2 | `ME-06-EL-002` | `ME06-EL-02` | Điều hướng Mentor toàn cục |
| #3 | `ME-06-EL-003` | `ME06-EL-03` | Ô tìm kiếm trên header |
| #4 | `ME-06-EL-004` | `ME06-EL-04` | Thông báo và số đếm mẫu |
| #5 | `ME-06-EL-005` | `ME06-EL-05` | Tài khoản Mentor |
| #6 | `ME-06-EL-006` | `ME06-EL-06` | Nhóm breadcrumb và đường dẫn course |
| #7 | `ME-06-EL-007` | `ME06-EL-07` | Trạng thái ghi danh và mã course |
| #8 | `ME-06-EL-008` | `ME06-EL-08` | Nhãn phiên bản builder và tự đồng bộ |
| #9 | `ME-06-EL-009` | `ME06-EL-09` | Tên và mô tả course |
| #10 | `ME-06-EL-010` | `ME06-EL-10` | Nút lưu thứ tự sắp xếp |
| #11 | `ME-06-EL-011` | `ME06-EL-11` | Nút thêm chương |
| #12 | `ME-06-EL-012` | `ME06-EL-12` | Nút thêm bài học liên kết ME-04 |
| #13 | `ME-06-EL-013` | `ME06-EL-13` | KPI số chương |
| #14 | `ME-06-EL-014` | `ME06-EL-14` | KPI số video |
| #15 | `ME-06-EL-015` | `ME06-EL-15` | KPI số lab và quiz |
| #16 | `ME-06-EL-016` | `ME06-EL-16` | KPI thời lượng tích lũy |
| #17 | `ME-06-EL-017` | `ME06-EL-17` | Các tab lọc trạng thái nội dung |
| #18 | `ME-06-EL-018` | `ME06-EL-18` | Ô tìm kiếm bài học |
| #19 | `ME-06-EL-019` | `ME06-EL-19` | Điều khiển mở và thu gọn cây |
| #20 | `ME-06-EL-020` | `ME06-EL-20` | Biểu đồ phân bố nội dung |
| #21 | `ME-06-EL-021` | `ME06-EL-21` | Hàng Chapter 01 và menu |
| #22 | `ME-06-EL-022` | `ME06-EL-22` | Hàng Chapter 02 và menu |
| #23 | `ME-06-EL-023` | `ME06-EL-23` | Nút thêm bài vào Chapter 02 |
| #24 | `ME-06-EL-024` | `ME06-EL-24` | Hàng bài 14 |
| #25 | `ME-06-EL-025` | `ME06-EL-25` | Xem ME-05, sửa và menu của bài 14 |
| #26 | `ME-06-EL-026` | `ME06-EL-26` | Hàng bài 15 |
| #27 | `ME-06-EL-027` | `ME06-EL-27` | Sửa và menu của bài 15 |
| #28 | `ME-06-EL-028` | `ME06-EL-28` | Hàng bài 16 |
| #29 | `ME-06-EL-029` | `ME06-EL-29` | Sửa và menu của bài 16 |
| #30 | `ME-06-EL-030` | `ME06-EL-30` | Hàng Lab 14 và trạng thái |
| #31 | `ME-06-EL-031` | `ME06-EL-31` | Rubric, cấu hình và menu Lab |
| #32 | `ME-06-EL-032` | `ME06-EL-32` | Hàng Quiz 02 |
| #33 | `ME-06-EL-033` | `ME06-EL-33` | Bộ đề và menu Quiz |
| #34 | `ME-06-EL-034` | `ME06-EL-34` | Hàng bài 17 nháp |
| #35 | `ME-06-EL-035` | `ME06-EL-35` | Nút xuất bản ngay liên kết ME-08 |
| #36 | `ME-06-EL-036` | `ME06-EL-36` | Hàng Chapter 03 và menu |
| #37 | `ME-06-EL-037` | `ME06-EL-37` | Hàng Chapter 04 và menu |
| #38 | `ME-06-EL-038` | `ME06-EL-38` | Nút thêm Chapter 05 |
| #39 | `ME-06-EL-039` | `ME06-EL-39` | Panel quy chuẩn LMS |
| #40 | `ME-06-EL-040` | `ME06-EL-40` | Link sổ tay kiểm duyệt EduTrust |
| #41 | `ME-06-EL-041` | `ME06-EL-41` | Timeline audit log gần đây |
| #42 | `ME-06-EL-042` | `ME06-EL-42` | Nút xem toàn bộ audit log |
| #43 | `ME-06-EL-043` | `ME06-EL-43` | Footer brand và nội dung giới thiệu |
| #44 | `ME-06-EL-044` | `ME06-EL-44` | Footer policy, liên kết và hỗ trợ |

## 3. Đặc tả từng element

### Trích từ DD nguồn: 4. Element specification — 44 markers

Tọa độ nằm trong [ME-06_markers.json](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/ME-06_markers.json) theo source pixels, gốc trên trái. Mỗi ID xuất hiện một lần trong JSON, SVG và ảnh chú thích.

| # / ID | Phần tử | Data/state và event |
|---:|---|---|
| 1 `ME06-EL-01` | Logo Study2Work / Mentor Portal | Static brand; không có user/course field. Click có `href="#"`; EV-15. |
| 2 `ME06-EL-02` | Navigation Dashboard, khóa học, chấm bài, hỗ trợ, thông báo | Các link `href="#"`; route map chưa có. EV-15. |
| 3 `ME06-EL-03` | Search input trên header | Placeholder tìm học viên/bài tập; không có API, filter binding hay submit. EV-15. |
| 4 `ME06-EL-04` | Notification button và badge `3` | Badge hardcoded; không có unread count/API/read action. EV-15. |
| 5 `ME06-EL-05` | Avatar, tên và chức danh Mentor | Text mẫu; #49 chỉ kiểm tra token/principal, không trả profile. Không có menu/logout handler. EV-15. |
| 6 `ME06-EL-06` | Breadcrumb Portal → danh sách course → slug/course → ME-06 | Tên/code mẫu; mọi anchor là `#`. Route quay về và giữ filter chưa xác định. EV-16. |
| 7 `ME06-EL-07` | Trạng thái học kỳ/ghi danh và course ID | Không thuộc `Content[]`; #49 không trả course metadata. Không dùng status badge mẫu làm course state. |
| 8 `ME06-EL-08` | “Curriculum Builder v3.4” / “Tự động đồng bộ LMS Cloud” | Không có version/sync status/API trong #49. Không thể khẳng định đồng bộ đã chạy. |
| 9 `ME06-EL-09` | Course title và mô tả | Không có trong response #49. Cần source course summary riêng trước khi map. |
| 10 `ME06-EL-10` | “Lưu thứ tự sắp xếp” | HTML chỉ hiện toast và ghi nhầm `API #52 PUT /mentor/courses/reorder`. #52 hiện là PATCH publish; không có reorder route trong contract ME-06. EV-06 `BLOCKED`. |
| 11 `ME06-EL-11` | “Thêm Chương mới” | Candidate tạo root qua #50 chỉ khi type/payload được xác nhận; không có model `Chapter` riêng trong #49. EV-07 `BLOCKED`. |
| 12 `ME06-EL-12` | “Thêm Bài học mới (ME-04)” | Handoff ghi trên mockup; #47/#48 là Lecture, không có mapping giữa Lecture và Content child. #50 không nhận parent_id. EV-08 `BLOCKED`. |
| 13 `ME06-EL-13` | KPI “08 Chương học” | Sample value; #49 không tính tổng chapter hay course summary. |
| 14 `ME06-EL-14` | KPI “48 Video bài giảng Full-HD” | Sample value; không có content-type enum, asset/quality metric hoặc aggregation trong #49. |
| 15 `ME06-EL-15` | KPI “12 Lab GitHub & Quiz” | Sample value; payload subtype/aggregation chưa có nguồn trong #49. |
| 16 `ME06-EL-16` | KPI “140h Thời lượng tích lũy” | Sample value; #49 không trả duration. |
| 17 `ME06-EL-17` | Tabs Tất cả/Đã xuất bản/Bản nháp/Đang ẩn | HTML filter values là lowercase `all/published/draft/hidden`; row `data-status` cũng là lowercase. API #49 trả status mở và source mutation dùng giá trị uppercase. Chưa có mapping approved. EV-03. |
| 18 `ME06-EL-18` | Search theo tên bài học | Current JS chỉ tìm chuỗi trong `row.innerText`; không search server. Không có debounce/empty-result/clear contract. EV-04. |
| 19 `ME06-EL-19` | Mở rộng/thu gọn tất cả | Toggle class `.hidden` trên module bodies ở DOM hiện tại; không gọi API. EV-05. |
| 20 `ME06-EL-20` | Biểu đồ phân bố nội dung | Video/Lab/Quiz 70/18/12 và 91% hoàn thiện là sample; #49 không trả aggregation/completion. |
| 21 `ME06-EL-21` | Chapter 01 row, badge và menu | Tree node candidate nhưng type/status mapping chưa có. Số lesson/quiz/14h là fixture. Header toggle hiện đổi accordion; menu không có contract. EV-05/EV-17. |
| 22 `ME06-EL-22` | Chapter 02 row, badge, counts và menu | Các trường hiển thị là fixture; #49 trả node fields thô và `parent_id/order`, không count/duration. Toggle local; menu không wired. EV-05/EV-17. |
| 23 `ME06-EL-23` | “+ Bài học” trong Chapter 02 | Child create cần parent relation; #50 luôn insert `parent_id=NULL`. EV-08 `BLOCKED`. |
| 24 `ME06-EL-24` | Bài 14 row (published) | Candidate Content fields `id/title/status/order/parent_id`; title, lượt xem, duration và icon type là sample. Không xem ID là lecture ID. |
| 25 `ME06-EL-25` | Bài 14: Xem ME-05, Sửa, menu | “Xem ME-05” dùng `href="#"`; Content.id ↔ Lecture.id chưa có contract. Edit candidate ME-07/#51; menu actions chưa xác định. EV-09/EV-10/EV-17. |
| 26 `ME06-EL-26` | Bài 15 row | Content node candidate; title/status/duration mẫu, chưa có type mapping riêng. |
| 27 `ME06-EL-27` | Bài 15: Sửa và menu | Edit qua ME-07/#51 chỉ sau khi type/payload form được chốt; #51 reset status thành `PENDING_REVIEW`. Menu chưa rõ. EV-10/EV-17. |
| 28 `ME06-EL-28` | Bài 16 row | Content node candidate; “Mới thêm”, title, status và duration không phải dữ kiện #49 nếu chưa load response. |
| 29 `ME06-EL-29` | Bài 16: Sửa và menu | Cùng flow #51 như row 15; no menu actions contract. EV-10/EV-17. |
| 30 `ME06-EL-30` | Lab 14 row, badge score | #49 không định nghĩa Lab type/score rubric/score aggregate; không suy ra từ `payload` object chưa schema. |
| 31 `ME06-EL-31` | Auto-Grading Rubric, Cấu hình, menu Lab | Không có API/event mapping trong #49–#53; route `href`/handler không gắn. EV-11/EV-17 `BLOCKED`. |
| 32 `ME06-EL-32` | Quiz 02 row và số câu hỏi | Không có quiz type/payload schema/count trong #49. |
| 33 `ME06-EL-33` | Bộ đề và menu Quiz | Không có API/route trong ME-06 trace; block tới khi có source. EV-11/EV-17. |
| 34 `ME06-EL-34` | Bài 17 row trạng thái draft | API #49 trả raw `status`; `PENDING_REVIEW` là status được #50/#51 dùng, nhưng label “Draft” và draft/published distinction cần owner-approved mapping. EV-12. |
| 35 `ME06-EL-35` | “Xuất bản ngay (ME-08)” | JS mock đổi nhãn và row `data-status` tại browser. API #52 chỉ publish `APPROVED`; `PENDING_REVIEW→PUBLISHED` trả 422. EV-13 `BLOCKED` cho row draft hiện tại. |
| 36 `ME06-EL-36` | Chapter 03 row và menu | Tên/count/18h là fixture; raw Content type và status mapping chưa có. Toggle/menu như #21. EV-05/EV-17. |
| 37 `ME06-EL-37` | Chapter 04 row, capstone badge và menu | Tên/project/40h là fixture; không có project/chapter subtype trong #49. EV-05/EV-17. |
| 38 `ME06-EL-38` | “Thêm Chương học tiếp theo (Chương 05)” | Chưa có add-root/child UX contract; candidate #50 only root with approved type/payload, no local form. EV-14 `BLOCKED`. |
| 39 `ME06-EL-39` | LMS quality rules panel | Quy tắc title/video/lab là nội dung mẫu; không có validation contract trong #49/#50/#51. Không biến panel thành client-side validation spec. |
| 40 `ME06-EL-40` | Link sổ tay EduTrust | `href="#"`; destination/content ownership chưa xác minh. EV-16. |
| 41 `ME06-EL-41` | Audit timeline | Names, timestamps, actions là fixture; #49 không trả audit stream. Checked-in `content_review_audit_logs` là persistence artifact cho flow khác, không phải read endpoint ở ME-06. |
| 42 `ME06-EL-42` | “Xem toàn bộ 142 hoạt động sửa đổi” | Count/route/API không có trong ME-06 trace; button không wired. EV-17 `BLOCKED`. |
| 43 `ME06-EL-43` | Footer brand/mô tả LMS | Static copy, không phải response #49. |
| 44 `ME06-EL-44` | Footer policy, partner và hỗ trợ | Static link-like text; không có URL/event. Không tạo route từ nhãn hiển thị. |

## 4. Conditional UI & state variations
- States theo inventory: loading/empty/ready/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/ME-06.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
