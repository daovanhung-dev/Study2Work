# ME-13 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ME-13_markers.json](../../screen_stitch/04_mentor/ME-13_chon-nguoi-nhan-thong-bao/ME-13_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ME-13-EL-001` | `not supplied in marker JSON` | Study2Work Mentor brand lockup |
| #2 | `ME-13-EL-002` | `not supplied in marker JSON` | Tổng quan header navigation |
| #3 | `ME-13-EL-003` | `not supplied in marker JSON` | Khóa học phụ trách header navigation |
| #4 | `ME-13-EL-004` | `not supplied in marker JSON` | Chấm bài header navigation |
| #5 | `ME-13-EL-005` | `not supplied in marker JSON` | Hộp thư hỗ trợ header navigation |
| #6 | `ME-13-EL-006` | `not supplied in marker JSON` | Thông báo header navigation |
| #7 | `ME-13-EL-007` | `not supplied in marker JSON` | Notification bell and unread dot |
| #8 | `ME-13-EL-008` | `not supplied in marker JSON` | Mentor name, role and profile action |
| #9 | `ME-13-EL-009` | `not supplied in marker JSON` | Breadcrumb Thông báo |
| #10 | `ME-13-EL-010` | `not supplied in marker JSON` | Breadcrumb Soạn thông báo mới |
| #11 | `ME-13-EL-011` | `not supplied in marker JSON` | Current breadcrumb Bước 1: Chọn người nhận |
| #12 | `ME-13-EL-012` | `not supplied in marker JSON` | Hệ thống thông báo học vụ badge |
| #13 | `ME-13-EL-013` | `not supplied in marker JSON` | ME-13 process code |
| #14 | `ME-13-EL-014` | `not supplied in marker JSON` | Screen title |
| #15 | `ME-13-EL-015` | `not supplied in marker JSON` | Permission claim chip |
| #16 | `ME-13-EL-016` | `not supplied in marker JSON` | Current step number 1 |
| #17 | `ME-13-EL-017` | `not supplied in marker JSON` | Current step label and title |
| #18 | `ME-13-EL-018` | `not supplied in marker JSON` | Step progress indicator |
| #19 | `ME-13-EL-019` | `not supplied in marker JSON` | Next step number 2 |
| #20 | `ME-13-EL-020` | `not supplied in marker JSON` | Next step ME-14 label and title |
| #21 | `ME-13-EL-021` | `not supplied in marker JSON` | Thiết lập phạm vi gửi card heading |
| #22 | `ME-13-EL-022` | `not supplied in marker JSON` | Required indicator |
| #23 | `ME-13-EL-023` | `not supplied in marker JSON` | Course field label |
| #24 | `ME-13-EL-024` | `not supplied in marker JSON` | Học kỳ hiện tại copy |
| #25 | `ME-13-EL-025` | `not supplied in marker JSON` | Course select control |
| #26 | `ME-13-EL-026` | `not supplied in marker JSON` | Course helper copy |
| #27 | `ME-13-EL-027` | `not supplied in marker JSON` | Recipient scope field label |
| #28 | `ME-13-EL-028` | `not supplied in marker JSON` | All students radio card |
| #29 | `ME-13-EL-029` | `not supplied in marker JSON` | Support-needed radio card |
| #30 | `ME-13-EL-030` | `not supplied in marker JSON` | Specific students radio card |
| #31 | `ME-13-EL-031` | `not supplied in marker JSON` | Notification policy card |
| #32 | `ME-13-EL-032` | `not supplied in marker JSON` | Target student list card heading |
| #33 | `ME-13-EL-033` | `not supplied in marker JSON` | Selected recipient count badge |
| #34 | `ME-13-EL-034` | `not supplied in marker JSON` | Anonymity mode chip |
| #35 | `ME-13-EL-035` | `not supplied in marker JSON` | Empty-state illustration |
| #36 | `ME-13-EL-036` | `not supplied in marker JSON` | Empty-state title |
| #37 | `ME-13-EL-037` | `not supplied in marker JSON` | Empty-state explanatory copy |
| #38 | `ME-13-EL-038` | `not supplied in marker JSON` | Source-not-synced badge |
| #39 | `ME-13-EL-039` | `not supplied in marker JSON` | WCAG AA badge |
| #40 | `ME-13-EL-040` | `not supplied in marker JSON` | Estimated recipient count row |
| #41 | `ME-13-EL-041` | `not supplied in marker JSON` | Inactive status label |
| #42 | `ME-13-EL-042` | `not supplied in marker JSON` | Cancel action |
| #43 | `ME-13-EL-043` | `not supplied in marker JSON` | Course-required helper note |
| #44 | `ME-13-EL-044` | `not supplied in marker JSON` | Continue to ME-14 disabled action |
| #45 | `ME-13-EL-045` | `not supplied in marker JSON` | Footer brand icon |
| #46 | `ME-13-EL-046` | `not supplied in marker JSON` | Copyright and compliance text |
| #47 | `ME-13-EL-047` | `not supplied in marker JSON` | Footer Mentor rules link |
| #48 | `ME-13-EL-048` | `not supplied in marker JSON` | Footer assessment standards link |
| #49 | `ME-13-EL-049` | `not supplied in marker JSON` | Footer technical support link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Tọa độ marker nằm trong ME-13_markers.json trên ảnh gốc 1600×1546. “Visible” dưới đây mô tả prototype; dynamic visibility/enabled states là yêu cầu thiết kế, chưa phải runtime.

| ID | Tên, loại, vị trí, mục đích | Thuộc tính/dữ liệu/điều kiện và trạng thái | Event |
|---:|---|---|---|
| 1 | Study2Work Mentor brand lockup, link/logo, header trái; nhận diện LMS. | Text/icon tĩnh; visible; href="#" trong HTML; destination chưa xác định. | E07 |
| 2 | Tổng quan, nav link, header. | Label tĩnh; href="#"; active=false trong ảnh. | E07 |
| 3 | Khóa học phụ trách, nav link, header. | Label tĩnh; href="#"; destination chưa xác định. | E07 |
| 4 | Chấm bài, nav link, header. | Label tĩnh; href="#"; destination chưa xác định. | E07 |
| 5 | Hộp thư hỗ trợ, nav link, header. | Label tĩnh; href="#"; destination chưa xác định. | E07 |
| 6 | Thông báo, active nav link, header. | Active visual state; href="#"; route list chưa xác định. | E07 |
| 7 | Notification bell/unread dot, action, header phải. | Badge dot không có count/state source; href="#". | E07 |
| 8 | Mentor name/role/profile action, header phải. | Tên TS. Vũ Thành Đạt và role là static mock data; avatar; link target "#". Không map user runtime từ file này. | E07 |
| 9 | Breadcrumb Thông báo, link. | href="#"; đích chưa có. | E07 |
| 10 | Breadcrumb Soạn thông báo mới, link. | href="#"; đích chưa có. | E07 |
| 11 | Breadcrumb hiện tại Bước 1: Chọn người nhận. | Text tĩnh/current location; không có route state trong HTML. | — |
| 12 | HỆ THỐNG THÔNG BÁO HỌC VỤ, badge. | Static category claim; không có data source/config. | — |
| 13 | Mã quy trình ME-13. | Static Screen ID; read-only. | — |
| 14 | Chọn nhóm người nhận thông báo, h1. | Static title; visible. | — |
| 15 | Quyền Điều phối viên & Mentor phụ trách, chip. | Static claim; backend chỉ xác nhận MENTOR role và direct owner trong dependencies này; claim coordinator/assigned Mentor chưa được xác nhận. | — |
| 16 | Số bước hiện tại 1, stepper. | Static current-step indicator; no interactive state source. | — |
| 17 | Chọn phạm vi người nhận, step label. | Static label; visible. | — |
| 18 | Thanh tiến độ, stepper. | Decorative progress only; no formula/state source. | — |
| 19 | Số bước tiếp theo 2. | Static next-step indicator; no click handler. | — |
| 20 | Soạn thảo nội dung thông báo (ME-14), next-step label. | Static destination label; actual route/handoff unresolved. | E05 (only after confirmed handoff) |
| 21 | Thiết lập phạm vi gửi, card heading. | Static section heading; visible. | — |
| 22 | * Bắt buộc, required indicator. | Static red text; references a required field but field validation/current failure state absent. | — |
| 23 | Khóa học phụ trách, select label. | Labels course selector; no bound value in prototype. | E02 |
| 24 | Học kỳ hiện tại, helper/status label. | Static term claim; #46 has no term field/filter. | — |
| 25 | Course dropdown, select#course-selector. | Placeholder plus four static options; option values cs101/fe202/ba301/qa401 conflict with #62 int64 course_id. Runtime options must use #46 IDs after decision; currently no loading/disabled/error binding. | E02 |
| 26 | Course helper copy. | Claims courses have enrolled students and assigned instructor; #46/#62 do not establish these list semantics. | — |
| 27 | Phân loại đối tượng nhận, field label. | Labels radio group recipient_scope. | E03 |
| 28 | All students radio card. | value=all; visibly checked in screenshot; caption promises full roster broadcast. IDs must come from #62; exact default/reset rule needs confirmation. | E03 |
| 29 | Support-needed radio card. | value=support_needed; criteria claim late submissions/checkpoint/absence, absent from #62; should be blocked until criteria/source API is approved. | E03 |
| 30 | Specific students radio card. | value=specific; says select individuals from attendance table; #62 returns roster summaries, not attendance table/checkboxes. | E03, E04 |
| 31 | Quy định gửi thông báo, policy card. | Static privacy/delivery text claims LMS + linked-school email/WCAG; no supporting #46/#62/#63 behavior. | — |
| 32 | Danh sách học viên mục tiêu, card heading. | Title for roster panel; no roster data displayed in source prototype. | E02 |
| 33 | 0 Đã chọn, selected count badge. | Static count 0; runtime should derive from unique selected IDs; current HTML has no state binding. | E03, E04 |
| 34 | Chế độ bảo mật danh tính, privacy chip. | Static anonymity claim; API has no anonymity field or visibility semantics. | — |
| 35 | Empty-state illustration. | Decorative SVG/icon; visible when no roster is loaded in screenshot. | E02 |
| 36 | Chưa có danh sách học viên khả dụng, empty-state title. | Static empty copy; screenshot explains choose a course; no dedicated empty-course/empty-roster variants. | E02 |
| 37 | Empty-state explanatory copy. | Claims list appears when official enrollment data exists; #62 returns active-enrollment students but no synchronization status. | E02 |
| 38 | Nguồn dữ liệu: Chưa đồng bộ badge. | Static sync claim; no synchronization metadata in #62. | — |
| 39 | Tuân thủ: WCAG AA badge. | Static compliance claim; not verification evidence. | — |
| 40 | Estimated recipient count row. | Static 0 học viên; runtime count formula would equal selected unique recipient IDs, subject to scope decision. | E03, E04 |
| 41 | CHƯA KÍCH HOẠT, status label. | Static disabled/inactive copy; reason is not dynamically mapped. | E05 |
| 42 | Hủy bỏ, anchor/button action. | Anchor href="#"; no cancel destination. | E06 |
| 43 | Yêu cầu xác định khóa học trước khi tiếp tục, helper. | Static validation copy; design checks course only, while #63 also rejects empty recipients. | E05 |
| 44 | Tiếp tục soạn nội dung (ME-14), disabled button. | button type=button, disabled and aria-disabled=true in HTML; no handler. Activation must require valid course and non-empty recipients per downstream #63, but handoff is unresolved. | E05 |
| 45 | Footer brand icon. | Static decorative icon; no separate handler identified. | — |
| 46 | Copyright and WCAG compliance footer text. | Static legal/compliance text; copyright says 2025; do not substitute current runtime metadata. | — |
| 47 | Quy chế Giảng viên footer link. | Anchor href="#"; destination unresolved. | E08 |
| 48 | Tiêu chuẩn đánh giá footer link. | Anchor href="#"; destination unresolved. | E08 |
| 49 | Hỗ trợ kỹ thuật footer link. | Anchor href="#"; destination unresolved. | E08 |

## 4. Conditional UI & state variations
- States theo inventory: loading/empty/selected/denied
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/04_mentor/ME-13_chon-nguoi-nhan-thong-bao/ME-13.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
