# ST-26 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-26_markers.json](../../screen_stitch/03_student/ST-26_thong-bao-hoc-vien/ST-26_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-26-EL-001` | `ST26-EL-01` | Study2Work brand/logo |
| #2 | `ST-26-EL-002` | `ST26-EL-02` | Global navigation |
| #3 | `ST-26-EL-003` | `ST26-EL-03` | Global search |
| #4 | `ST-26-EL-004` | `ST26-EL-04` | Notification bell |
| #5 | `ST-26-EL-005` | `ST26-EL-05` | Student profile menu |
| #6 | `ST-26-EL-006` | `ST26-EL-06` | Semester/status strip |
| #7 | `ST-26-EL-007` | `ST26-EL-07` | Breadcrumb |
| #8 | `ST-26-EL-008` | `ST26-EL-08` | Page title and new badge |
| #9 | `ST-26-EL-009` | `ST26-EL-09` | Page description |
| #10 | `ST-26-EL-010` | `ST26-EL-10` | Mark all read |
| #11 | `ST-26-EL-011` | `ST26-EL-11` | All notifications tab |
| #12 | `ST-26-EL-012` | `ST26-EL-12` | Unread tab/count |
| #13 | `ST-26-EL-013` | `ST26-EL-13` | Assignments/grading tab |
| #14 | `ST-26-EL-014` | `ST26-EL-14` | Mentor schedule tab |
| #15 | `ST-26-EL-015` | `ST26-EL-15` | Forum activity tab |
| #16 | `ST-26-EL-016` | `ST26-EL-16` | Notification list region |
| #17 | `ST-26-EL-017` | `ST26-EL-17` | Notification 1 card |
| #18 | `ST-26-EL-018` | `ST26-EL-18` | Notification 1 CTA |
| #19 | `ST-26-EL-019` | `ST26-EL-19` | Notification 2 card |
| #20 | `ST-26-EL-020` | `ST26-EL-20` | Notification 2 CTA |
| #21 | `ST-26-EL-021` | `ST26-EL-21` | Notification 3 card |
| #22 | `ST-26-EL-022` | `ST26-EL-22` | Notification 3 CTA |
| #23 | `ST-26-EL-023` | `ST26-EL-23` | Notification 4 card |
| #24 | `ST-26-EL-024` | `ST26-EL-24` | Notification 4 CTA |
| #25 | `ST-26-EL-025` | `ST26-EL-25` | Notification 5 card |
| #26 | `ST-26-EL-026` | `ST26-EL-26` | Notification 5 CTA |
| #27 | `ST-26-EL-027` | `ST26-EL-27` | Notification 6 card |
| #28 | `ST-26-EL-028` | `ST26-EL-28` | Notification channels panel |
| #29 | `ST-26-EL-029` | `ST26-EL-29` | Email toggle |
| #30 | `ST-26-EL-030` | `ST26-EL-30` | Web Push toggle |
| #31 | `ST-26-EL-031` | `ST26-EL-31` | SMS reminder toggle |
| #32 | `ST-26-EL-032` | `ST26-EL-32` | API #48 status strip |
| #33 | `ST-26-EL-033` | `ST26-EL-33` | Weekly statistics chart |
| #34 | `ST-26-EL-034` | `ST26-EL-34` | Weekly statistics legend |
| #35 | `ST-26-EL-035` | `ST26-EL-35` | Emergency support panel |
| #36 | `ST-26-EL-036` | `ST26-EL-36` | Coordinator contact CTA |
| #37 | `ST-26-EL-037` | `ST26-EL-37` | Footer brand/description |
| #38 | `ST-26-EL-038` | `ST26-EL-38` | Footer program links |
| #39 | `ST-26-EL-039` | `ST26-EL-39` | Footer community links |
| #40 | `ST-26-EL-040` | `ST26-EL-40` | Footer office/contact |
| #41 | `ST-26-EL-041` | `ST26-EL-41` | Footer legal strip |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Marker IDs `ST26-EL-01`…`ST26-EL-41` map to [`screen_annotated.png`](../../screen_stitch/03_student/ST-26_thong-bao-hoc-vien/screen_annotated.png) and [`ST-26_markers.json`](../../screen_stitch/03_student/ST-26_thong-bao-hoc-vien/ST-26_markers.json). Composite elements list their visible children; sample values remain illustrative.

| Element ID / marker | Tên, loại, vị trí và mục đích | Thuộc tính, nguồn, visibility/state/validation | Event |
|---|---|---|---|
| ST26-EL-01 | Study2Work brand/logo ở đầu global header. | Static screenshot brand; destination is not verified. | EV-13 |
| ST26-EL-02 | Global nav group: Trang chủ, Khóa học, Khóa học của tôi, Lộ trình học, Diễn đàn. | Screenshot labels/links; HTML fallback uses `#`; no Study Web handlers/routes. | EV-13 |
| ST26-EL-03 | Course/search field in header. | Placeholder sample; query contract and search destination are outside #43–#45. | EV-13 |
| ST26-EL-04 | Notification bell and red badge. | Current-page icon/count sample; no badge-count field or link behavior confirmed. | EV-13 |
| ST26-EL-05 | Student avatar, name, role and menu chevron. | Identity values are samples; session/profile menu source is not available in this screen. | EV-13 |
| ST26-EL-06 | Semester/status strip “Học kỳ Fall 2024 • Đang theo học”. | Literal screenshot text; not Notification API data or Student enrollment proof. | — |
| ST26-EL-07 | Breadcrumb home → Học viên → Thông báo. | Visual hierarchy; route IDs/history behavior unavailable; “Học viên” is not proof of auth state. | EV-13 |
| ST26-EL-08 | Page title plus blue “5 mới” badge. | Title is static; count is sample and conflicts with four visible blue dots. API schema has no unread-count field. | EV-02 |
| ST26-EL-09 | Supporting description. | Static copy; no API/source mapping. | — |
| ST26-EL-10 | “Đánh dấu tất cả đã đọc” button. | Expected API #45; click only when enabled by an approved Student/read-state contract. Pending/success state is not wired. | EV-09 |
| ST26-EL-11 | “Tất cả thông báo” tab. | Visual filter option. API #43 `unread_only` is optional; whether all is omitted or `false`, query sync and page reset need approval. | EV-04 |
| ST26-EL-12 | “Chưa đọc” tab and `(5)` count. | Query candidate `unread_only=true`; unread state/count field is not in Notification response; count is sample. | EV-05 |
| ST26-EL-13 | “Bài tập & Chấm điểm” category tab. | Sample category; API #43 has no category/type query or approved enum. | EV-06 |
| ST26-EL-14 | “Lịch hẹn Mentor” category tab. | Sample category; no Student preference/notification category endpoint. | EV-06 |
| ST26-EL-15 | “Hoạt động diễn đàn” category tab. | Sample category; no category field/enum in reusable Notification schema. | EV-06 |
| ST26-EL-16 | Notification list region and vertical collection. | API #43 expected Page; response page/order/size are Draft/derived; screenshot supplies six rows but no pagination control. | EV-01, EV-02, EV-03 |
| ST26-EL-17 | Sample card 1: category “Đánh giá Đồ án”, time, title/body, unread dot and “Đã đọc”. | All content, grade/name/time/read marker illustrative; dot conflicts with “Đã đọc”; no Notification read/category field mapping. | EV-07, EV-08 |
| ST26-EL-18 | Card 1 CTA “Xem kết quả chấm (ST-19)”. | Proposed navigation target only; action payload/submission ID/route mapping absent. | EV-08 |
| ST26-EL-19 | Sample card 2: forum category, time, title/body, unread dot and “Đã đọc”. | Screenshot sample; category/state/content not proven by API. | EV-07, EV-08 |
| ST26-EL-20 | Card 2 CTA “Xem thảo luận (ST-25)”. | Proposed target only; discussion ID/action payload not present in Notification contract. | EV-08 |
| ST26-EL-21 | Sample card 3: mentor reminder, time, title/body, unread dot and “Đã đọc”. | Screenshot sample; no schedule field mapping; optional `scheduled_at` lacks physical source and semantics. | EV-07, EV-08 |
| ST26-EL-22 | Card 3 CTA “Vào phòng Meet”. | External target sample; no URL, trust/allowlist or new-tab policy in contract. | EV-08 |
| ST26-EL-23 | Sample card 4: new-course category, time, title/body, unread dot and “Đã đọc”. | Screenshot sample; course/category/read state do not map from Notification schema. | EV-07, EV-08 |
| ST26-EL-24 | Card 4 CTA “Vào học ngay (ST-11)”. | Proposed target only; lesson/course IDs and access check payload absent. | EV-08 |
| ST26-EL-25 | Sample card 5: achievement category, time, title/body and “Đã xem”. | Screenshot sample; no category field in Notification; no evidence of award from this message. | EV-07, EV-08 |
| ST26-EL-26 | Card 5 CTA “Xem chứng nhận (ST-22)”. | Proposed target only; course/achievement ID payload absent. ST-22 is a separate screen. | EV-08 |
| ST26-EL-27 | Sample card 6: system-maintenance category, time, title/body and “Đã xem”. | Screenshot sample; no type/status mapping or operational maintenance source. | EV-07 |
| ST26-EL-28 | “Kênh nhận tin” preferences panel heading and explanation. | Static sidebar; no #43–#45 preference contract. | — |
| ST26-EL-29 | Email notification toggle. | Visual state only; no Student preferences API, request field, default, persistence or consent semantics. | EV-10 |
| ST26-EL-30 | Web Push toggle. | Visual state only; no permission/device token/preferences contract. | EV-10 |
| ST26-EL-31 | SMS mentor-reminder toggle. | Visual state only; no phone/SMS consent/preferences contract. | EV-10 |
| ST26-EL-32 | Green “Cập nhật tự động qua API #48” strip. | Screenshot text is incorrect for current API catalog #48 (Mentor lecture detail); no preference update contract. | EV-10 |
| ST26-EL-33 | Weekly-statistics heading, total `42`, bar chart and day labels. | Sample aggregate; no stats endpoint in ST-26 catalog; do not derive from notification list. | EV-11 |
| ST26-EL-34 | Weekly-statistics legend/counts: grading 14, mentoring 8, forum 16, system 4. | Sample values/categories; no approved aggregate definitions or source. | EV-11 |
| ST26-EL-35 | Emergency-help card heading and supporting copy. | Static screenshot panel; no service-level/urgency contract. | — |
| ST26-EL-36 | “Liên hệ điều phối viên” CTA with external-link icon. | Destination/contact channel not defined; do not infer route or service. | EV-12 |
| ST26-EL-37 | Footer brand, purpose description and certification badges. | Static sample copy/assets; certification claims are not API data. | — |
| ST26-EL-38 | Footer “Chương trình” links. | Static labels/targets; no verified destination routes. | EV-14 |
| ST26-EL-39 | Footer community/support links. | Static labels/targets; no verified destination routes/services. | EV-14 |
| ST26-EL-40 | Footer office address, hotline and email. | Screenshot contact literals; not verified support contact details. | — |
| ST26-EL-41 | Copyright strip and terms/privacy/academic-policy links. | Static sample; policy destinations are not verified. | EV-14 |

## 4. Conditional UI & state variations
- States theo inventory: unread/read/empty/marking/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-26_thong-bao-hoc-vien/ST-26.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
