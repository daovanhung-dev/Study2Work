# ME-12 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ME-12_markers.json](../../screen_stitch/04_mentor/ME-12_trao-doi-va-dong-yeu-cau/ME-12_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ME-12-EL-001` | `not supplied in marker JSON` | Mentor logo/brand lockup |
| #2 | `ME-12-EL-002` | `not supplied in marker JSON` | Tổng quan navigation |
| #3 | `ME-12-EL-003` | `not supplied in marker JSON` | Khóa học phụ trách navigation |
| #4 | `ME-12-EL-004` | `not supplied in marker JSON` | Chấm bài navigation |
| #5 | `ME-12-EL-005` | `not supplied in marker JSON` | Hộp thư hỗ trợ active navigation |
| #6 | `ME-12-EL-006` | `not supplied in marker JSON` | Thông báo navigation |
| #7 | `ME-12-EL-007` | `not supplied in marker JSON` | Notification bell/badge |
| #8 | `ME-12-EL-008` | `not supplied in marker JSON` | Mentor name/role/profile |
| #9 | `ME-12-EL-009` | `not supplied in marker JSON` | Breadcrumb Hộp thư hỗ trợ |
| #10 | `ME-12-EL-010` | `not supplied in marker JSON` | Breadcrumb Chi tiết yêu cầu trao đổi |
| #11 | `ME-12-EL-011` | `not supplied in marker JSON` | Quay lại danh sách yêu cầu (ME-11) |
| #12 | `ME-12-EL-012` | `not supplied in marker JSON` | Mã tiến trình ME-12 badge |
| #13 | `ME-12-EL-013` | `not supplied in marker JSON` | Main title |
| #14 | `ME-12-EL-014` | `not supplied in marker JSON` | Description |
| #15 | `ME-12-EL-015` | `not supplied in marker JSON` | Mã yêu cầu value/loading |
| #16 | `ME-12-EL-016` | `not supplied in marker JSON` | Trạng thái request |
| #17 | `ME-12-EL-017` | `not supplied in marker JSON` | Luồng hội thoại hỗ trợ heading |
| #18 | `ME-12-EL-018` | `not supplied in marker JSON` | Socket synchronization claim |
| #19 | `ME-12-EL-019` | `not supplied in marker JSON` | Empty-state illustration |
| #20 | `ME-12-EL-020` | `not supplied in marker JSON` | Empty-state heading |
| #21 | `ME-12-EL-021` | `not supplied in marker JSON` | Empty-state explanatory copy |
| #22 | `ME-12-EL-022` | `not supplied in marker JSON` | Socket/TLS 1.3 status badge |
| #23 | `ME-12-EL-023` | `not supplied in marker JSON` | Reply composer heading |
| #24 | `ME-12-EL-024` | `not supplied in marker JSON` | Character count |
| #25 | `ME-12-EL-025` | `not supplied in marker JSON` | Reply textarea |
| #26 | `ME-12-EL-026` | `not supplied in marker JSON` | Locked reply warning |
| #27 | `ME-12-EL-027` | `not supplied in marker JSON` | Send reply button (disabled) |
| #28 | `ME-12-EL-028` | `not supplied in marker JSON` | Resolve card heading |
| #29 | `ME-12-EL-029` | `not supplied in marker JSON` | Resolve explanatory copy |
| #30 | `ME-12-EL-030` | `not supplied in marker JSON` | Auto-settlement row |
| #31 | `ME-12-EL-031` | `not supplied in marker JSON` | Satisfaction survey row |
| #32 | `ME-12-EL-032` | `not supplied in marker JSON` | Mark resolved button (disabled) |
| #33 | `ME-12-EL-033` | `not supplied in marker JSON` | Minimum-exchange gate note |
| #34 | `ME-12-EL-034` | `not supplied in marker JSON` | Mentor standards card heading |
| #35 | `ME-12-EL-035` | `not supplied in marker JSON` | Standard 1: 24-hour SLA |
| #36 | `ME-12-EL-036` | `not supplied in marker JSON` | Standard 2: sources/references |
| #37 | `ME-12-EL-037` | `not supplied in marker JSON` | Standard 3: privacy |
| #38 | `ME-12-EL-038` | `not supplied in marker JSON` | Help-guide link |
| #39 | `ME-12-EL-039` | `not supplied in marker JSON` | Footer logo icon |
| #40 | `ME-12-EL-040` | `not supplied in marker JSON` | Copyright/WCAG footer text |
| #41 | `ME-12-EL-041` | `not supplied in marker JSON` | Quy chế Giảng viên link |
| #42 | `ME-12-EL-042` | `not supplied in marker JSON` | Tiêu chuẩn đánh giá link |
| #43 | `ME-12-EL-043` | `not supplied in marker JSON` | Hỗ trợ kỹ thuật link |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Coordinates are approximate source-image pixel anchors, origin top-left. Marker labels are placed in nearby margins/whitespace where possible. Element ID equals the same numbered marker in ME-12_markers.json and screen_annotated.png.

| ID | Tên/loại; vị trí/mục đích | Thuộc tính, nguồn dữ liệu, validation | Hiển thị/trạng thái | Event |
|---:|---|---|---|---|
| 1 | Mentor logo/brand lockup; header trái; nhận diện. | Static anchor href="#"; destination unresolved. | Always visible; focus treatment not specified. | E06 |
| 2 | Tổng quan navigation item; header. | Static label/anchor; destination unresolved. | Active/inactive appearance from prototype only. | E06 |
| 3 | Khóa học phụ trách navigation item; header. | Static label/anchor; destination unresolved. | Default/focus/active states not implemented. | E06 |
| 4 | Chấm bài navigation item; header. | Static label/anchor; destination unresolved. | Default/focus/active states not implemented. | E06 |
| 5 | Hộp thư hỗ trợ active navigation item; header. | Static active label; current destination implied as support inbox only. | Active visual state; no runtime route. | E06 |
| 6 | Thông báo navigation item; header. | Static label/anchor; destination unresolved. | Default/focus states not implemented. | E06 |
| 7 | Notification bell and red badge; header right. | Static icon/dot; no notification count or notification API on this screen. | Visible in prototype; count/empty state unknown. | E06 |
| 8 | Mentor name, role and profile icon; header right. | Static name/role. Current authenticated user source is not wired to this asset. | Visible in prototype; account menu behavior unknown. | E06 |
| 9 | Breadcrumb Hộp thư hỗ trợ; under header. | Static anchor href="#"; expected destination is ME-11. | Always visible in prototype. | E02 |
| 10 | Breadcrumb Chi tiết yêu cầu trao đổi; current page label. | Static text; no data binding. | Current-location label; noninteractive appearance. | None |
| 11 | Quay lại danh sách yêu cầu (ME-11); button at upper right. | Static href="#"; expected route /mentor/support. No query/filter state contract. | Enabled-looking in image; not wired. | E02 |
| 12 | Mã tiến trình ME-12 badge; hero. | Literal process/screen identifier, not API data. | Always visible. | None |
| 13 | Main title; hero. | Literal Vietnamese title. | Always visible. | None |
| 14 | Screen description; hero. | Literal explanatory text; does not define an API field. | Always visible. | None |
| 15 | Mã yêu cầu label/value; hero right. | Current value is literal “Đang nạp...”. Intended value is returned SupportRequest.id; expected route requestId must agree with response id or treat mismatch as invalid projection. | Loading then mapped ID; error state unresolved visually. | E01 |
| 16 | Trạng thái request chip; hero right. | Current literal “Đang mở”. Intended source is SupportRequest.status from #59/#60/#61; do not map unknown enum values by guess. | Loading then source status; colors/labels for all states need confirmation. | E01, E04, E05 |
| 17 | Luồng hội thoại hỗ trợ section heading/icon. | Static section title/icon. | Always visible in prototype. | None |
| 18 | “Kênh đồng bộ hóa bảo mật Study2Work” claim. | Static copy/icon; no socket code/API or transport evidence. | Visible claim only; do not show live connection state based on this text. | None |
| 19 | Empty-thread illustration. | Static illustration. It is displayed beside the empty message copy. | Prototype empty state only; hide when messages exist under a future approved layout. | E01 |
| 20 | Empty-thread heading. | Literal “Chưa có dữ liệu hội thoại hiển thị”; not a server error or proof of missing request. | Shown in prototype; future visibility only when a valid request has messages: []. | E01 |
| 21 | Empty-thread explanatory copy. | Literal wait/sync and sign-in text; no polling/socket implementation backs it. | Static empty-state copy. | E01 |
| 22 | Socket/TLS 1.3 status badge. | Literal transport claim; source provides no socket/TLS state. | Prototype only; runtime status must not be inferred. | None |
| 23 | Reply composer heading/icon. | Static section heading/icon. | Always visible in prototype; actual access depends on approved lifecycle and API availability. | None |
| 24 | Character counter. | Static “0 / 2000”. Intended draft length display; API #60 has no maximum. Counting rule (Unicode code points/graphemes/UTF-16 units) and hard limit are unapproved. | Static count in asset; dynamic count and validity are proposed, blocked. | E03 |
| 25 | Reply textarea, id instructor-response-textarea. | Text input, placeholder prompt, rows=5, empty by default in HTML; no maxlength. Input string is sent as message. #60 rejects message.strip()==empty and preserves original supplied value. | Current control visually enabled; source lock notice conflicts. Disable when no valid request, unresolved policy says replies are prohibited, or request in-flight. | E03 |
| 26 | Reply locked warning. | Literal warning that reply remains locked until support service contract is connected. This is prototype copy, not a response business code. | Visible static warning; actual enable rule not established. | None |
| 27 | Gửi câu trả lời button. | Static disabled button with aria-disabled=true. Intended trigger for POST #60; no form handler. | Disabled in source. Future enabled only with valid request/session, approved status policy and nonblank message; disable while sending. | E04 |
| 28 | Tùy chọn đóng yêu cầu heading/icon. | Static card title/icon. | Always visible. | None |
| 29 | Resolve explanation. | Literal learner-satisfaction/valid-conversation statement. AC-24 supplies the satisfaction decision; API does not collect it. | Static copy; confirmation method unresolved. | E05 |
| 30 | Auto-settlement row. | Static “Quy trình nghiệm thu / Tự động kết toán” claim; no #59–#61 data or settlement side effect. | Prototype claim only; do not render as verified state. | None |
| 31 | Satisfaction-survey row. | Static “Khảo sát hài lòng / Sẽ gửi sau khi đóng” claim; no survey contract/API. | Prototype claim only; delivery timing and ownership unresolved. | None |
| 32 | Đánh dấu đã giải quyết và đóng yêu cầu button. | Static disabled button with aria-disabled=true; intended trigger #61, but AC confirmation interaction is absent. | Disabled in source. Enablement gate/minimum exchange and confirmation interaction remain blocked. | E05 |
| 33 | Minimum-valid-exchange gate note. | Literal “Chỉ mở khóa sau khi phát sinh tối thiểu một lượt trao đổi hợp lệ”; #61 does not enforce it. | Static note only; cannot be treated as backend rule. | None |
| 34 | Mentor standards card heading/icon. | Static content card title. | Always visible. | None |
| 35 | Standard 1: 24-hour response SLA. | Static claim; no SLA timestamp/measurement field or API. | Prototype only; SLA definition/approval unresolved. | None |
| 36 | Standard 2: provide references. | Static claim; no source/reference field in #59–#61 request/response. | Prototype only; whether this is guidance or required validation is unresolved. | None |
| 37 | Standard 3: learner-data privacy. | Static privacy statement; real access boundary is API ownership/auth check. | Prototype only; do not treat as a complete privacy policy. | None |
| 38 | Xem hướng dẫn xử lý khúc mắc external-looking link. | Static href="#"; URL/destination not present. | Enabled-looking; target unresolved. | E06 |
| 39 | Footer brand icon. | Static logo; no screen-specific data. | Always visible; no verified interaction. | None |
| 40 | Copyright/WCAG footer text. | Static “© 2025”, Study2Work, WCAG 2.1 AA and ownership statement; no compliance test evidence in this task. | Always visible claim. | None |
| 41 | Quy chế Giảng viên footer link. | Static href="#"; destination unresolved. | Enabled-looking; no navigation implementation. | E06 |
| 42 | Tiêu chuẩn đánh giá footer link. | Static href="#"; destination unresolved. | Enabled-looking; no navigation implementation. | E06 |
| 43 | Hỗ trợ kỹ thuật footer link. | Static href="#"; destination unresolved. | Enabled-looking; no navigation implementation. | E06 |

## 4. Conditional UI & state variations
- States theo inventory: loading/ready-empty/ready-thread/replying/resolving/resolved/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/04_mentor/ME-12_trao-doi-va-dong-yeu-cau/ME-12.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
