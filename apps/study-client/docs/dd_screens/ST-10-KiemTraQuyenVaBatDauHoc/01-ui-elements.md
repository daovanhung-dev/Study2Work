# ST-10 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-10_markers.json](../../screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/ST-10_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-10-EL-001` | `ST10-EL-01` | Study2Work LMS logo and school icon |
| #2 | `ST-10-EL-002` | `ST10-EL-02` | Trang chủ, Khóa học của tôi, Tiến độ, Thảo luận, Thông báo |
| #3 | `ST-10-EL-003` | `ST10-EL-03` | Static Nguyễn Văn A / Học viên identity and profile icon |
| #4 | `ST-10-EL-004` | `ST10-EL-04` | Khóa học / Kỹ sư Frontend Chuyên nghiệp / ST-10 transition label |
| #5 | `ST-10-EL-005` | `ST10-EL-05` | ENTITLEMENT GATE: ACTIVE |
| #6 | `ST-10-EL-006` | `ST10-EL-06` | Shield icon, Hand-off Transition Module label and waiting-for-access title |
| #7 | `ST-10-EL-007` | `ST10-EL-07` | SECURITY_GATE_ENFORCED |
| #8 | `ST-10-EL-008` | `ST10-EL-08` | Progress illustration, STATUS: 423_LOCKED and static access-check copy |
| #9 | `ST-10-EL-009` | `ST10-EL-09` | Disabled lesson/media surface, protected-content heading and explanatory text |
| #10 | `ST-10-EL-010` | `ST10-EL-10` | Chặn tự động stream / waiting for server Session Token copy |
| #11 | `ST-10-EL-011` | `ST10-EL-11` | Static policy copy naming APIs #22, #23 and #24 |
| #12 | `ST-10-EL-012` | `ST10-EL-12` | Quay lại tổng quan khóa học (ST-09) |
| #13 | `ST-10-EL-013` | `ST10-EL-13` | Bắt đầu học (ST-11) - Đang khóa vĩnh viễn |
| #14 | `ST-10-EL-014` | `ST10-EL-14` | Máy trạng thái Hand-off title, description and FSM badge |
| #15 | `ST-10-EL-015` | `ST10-EL-15` | checking / Active card and API #22 description |
| #16 | `ST-10-EL-016` | `ST10-EL-16` | denied / Fallback card and access-denied description |
| #17 | `ST-10-EL-017` | `ST10-EL-17` | started / Target ST-11 card and API #23 description |
| #18 | `ST-10-EL-018` | `ST10-EL-18` | DESIGN_ONLY status rows for GET #22, POST #23 and GET #24 |
| #19 | `ST-10-EL-019` | `ST10-EL-19` | Static note about no mock bypass and ST-10 contract |
| #20 | `ST-10-EL-020` | `ST10-EL-20` | © 2025 Study2Work and WCAG 2.1 AA badge |
| #21 | `ST-10-EL-021` | `ST10-EL-21` | Terms, privacy and help links |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Các marker 1–21 khớp [screen_annotated.png](../../screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/screen_annotated.png) và [ST-10_markers.json](../../screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/ST-10_markers.json). Các tên/người dùng/trạng thái trong ảnh là copy tĩnh, trừ native disabled attribute của nút Start.

| # / Element ID | Tên, loại, vị trí, mục đích | Thuộc tính, nguồn dữ liệu, điều kiện | Trạng thái / sự kiện |
|---|---|---|---|
| **#1 — ST10-EL-01** | Brand Study2Work LMS và biểu tượng học tập; anchor bên trái header. | Label/icon cố định; href=#, data-path=trang-chu. Không có route binding hoặc validation. | Static/default; click thuộc EV-09, hiện không đi tới route. |
| **#2 — ST10-EL-02** | Primary navigation: Trang chủ, Khóa học của tôi, Tiến độ, Thảo luận, Thông báo. | 5 label tĩnh; nav có hidden md:flex; anchors href=# và data-path slugs. Không có mobile menu trong asset. | Static/hover class; active route state không bind. EV-09. |
| **#3 — ST10-EL-03** | Student identity: Nguyễn Văn A, Học viên, person icon ở header. | Danh tính/role viết cứng trong HTML; không lấy session hoặc profile; icon không có menu handler. | Static/default; không xác minh auth/session. |
| **#4 — ST10-EL-04** | Breadcrumb gồm Khóa học, tên khóa Kỹ sư Frontend Chuyên nghiệp, nhãn ST-10. | Tên khóa và Screen ID tĩnh; hai anchors href=#; không có lessonId/courseId binding. | Static/default; click breadcrumb thuộc EV-09, destinations chưa wired. |
| **#5 — ST10-EL-05** | Pill ENTITLEMENT GATE: ACTIVE ở trên nội dung. | Text/icon đỏ tĩnh, không có API response/state source. | Luôn vẽ active trong mockup; không phải access decision thực. |
| **#6 — ST10-EL-06** | Shield icon, Hand-off Transition Module label và H1 Đang chờ xác minh quyền bài học. | Copy tĩnh; không có lesson title hoặc request state mapping. | Static/default; EV-01–EV-03 là flow kỳ vọng, không phải handler hiện có. |
| **#7 — ST10-EL-07** | Badge SECURITY_GATE_ENFORCED ở cạnh heading. | Badge/icon tĩnh; không phải policy enforcement hook. | Static/default; enforcement backend chưa source-backed. |
| **#8 — ST10-EL-08** | Tiến trình cổng bảo vệ: tiêu đề, STATUS: 423_LOCKED, thanh progress 2/5 và explanatory copy. | Status string/progress width/copy được ghi tĩnh. 423 không có trong #22–#24 catalog; 2/5 không map tới thuật toán hoặc response. | Visual pulse/static; không có loading timer hoặc API progress. EV-03. |
| **#9 — ST10-EL-09** | Vùng player 16:9 placeholder, icon và heading Nội dung bài học được bảo vệ tuyệt đối. | Không có video/audio/iframe/player source. Copy nói player/tài liệu bị disable đến khi #22 cấp quyền. | Chỉ là surface tĩnh; nội dung/media không được tải trong HTML hiện tại. EV-04/EV-06. |
| **#10 — ST10-EL-10** | Pill Chặn tự động stream – Đang chờ máy chủ cấp phát Session Token trong player placeholder. | Copy tĩnh; không có token field/API contract hoặc session storage binding. | Static/default; không khẳng định server token tồn tại. |
| **#11 — ST10-EL-11** | Technical Security Contract callout nêu #22/#23/#24 và cảnh báo không tự tải nội dung. | Text/code fragments viết cứng; references không tạo request/guard. | Static documentation content; EV-03–EV-06 mô tả expected API path/gaps. |
| **#12 — ST10-EL-12** | Anchor Quay lại tổng quan khóa học (ST-09). | href=#, data-path=tong-quan-khoa-hoc; không truyền lessonId/courseId hoặc navigation state. | Click EV-08; hiện placeholder. |
| **#13 — ST10-EL-13** | Button Bắt đầu học (ST-11) – Đang khóa vĩnh viễn. | type=button, disabled=true, aria-disabled=true, title chờ phản hồi #22. Không có handler, request hoặc enable rule. Copy “vĩnh viễn” không phải API state. | Disabled trong static HTML; không phát click event. Expected enabled state và việc click có kích hoạt #23 hay không chưa được quy định; xem trigger gap tại EV-05. |
| **#14 — ST10-EL-14** | Panel Máy trạng thái Hand-off, lifecycle description và FSM badge. | Tiêu đề/description/badge cố định; không bind FSM state store. | Static/default; không tự tạo state machine. |
| **#15 — ST10-EL-15** | FSM step 1 checking, Active badge và mô tả gọi #22. | “Active”/pulse tĩnh; không chứng minh request started/pending. | Static illustration; EV-03 là event thiết kế. |
| **#16 — ST10-EL-16** | FSM step 2 denied, Fallback badge và access/prerequisite copy. | Text tĩnh; không có reason field hoặc error mapping. | Static illustration; expected denied branch EV-04. |
| **#17 — ST10-EL-17** | FSM step 3 started, Target ST-11 badge và copy #23 giải phóng media. | Text tĩnh; không nhận response #23 hoặc token/media grant. | Static illustration; expected success handoff EV-05–EV-07. |
| **#18 — ST10-EL-18** | Trạng thái API Backend card, ba rows GET #22, POST #23, GET #24. | Ba nhãn DESIGN_ONLY viết cứng; #22/#23/#24 API DD Draft và không có route/module source. | Static labels, không có health/status polling. |
| **#19 — ST10-EL-19** | Integration/security notice về no mock bypass và contract ST-10. | Text/icon tĩnh; không kiểm tra route/API. | Static/default; không có event độc lập. |
| **#20 — ST10-EL-20** | Footer copyright và WCAG 2.1 AA badge. | Năm 2025 và compliance claim tĩnh; chưa có audit runtime. | Static/default; không event. |
| **#21 — ST10-EL-21** | Footer Điều khoản dịch vụ, Chính sách bảo mật, Trợ giúp. | Anchors href=# với slugs; destination/URL policy không có contract trong asset. | Click EV-10; hiện placeholder. |

### Elements/controls dự kiến nhưng không có

Không có lesson selector/list, course/lesson data binding, access-reason panel, retry control, real loading indicator, session-expired control, network error action hoặc explicit “Continue” state được điều khiển bởi API. API #22–#24 status card là nội dung mockup, không phải control. Không tạo marker cho controls chưa có hình.

## 4. Conditional UI & state variations
- States theo inventory: checking/denied/started/failure
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/ST-10.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
