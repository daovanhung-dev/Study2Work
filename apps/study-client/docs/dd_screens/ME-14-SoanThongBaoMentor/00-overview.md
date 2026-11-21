# ME-14 — Soạn thông báo mentor · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-14` |
| Module | Mentor |
| Route | `/mentor/notifications/new` — hiện được đăng ký trong `mentor.route.ts`; browser/runtime chưa xác minh |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | The approved producer slice is source-wired: ME-14 posts text, selected recipients and PUSH/EMAIL channels to API #63 and routes an accepted UUID to SH-07. The wider design remains Draft (course binding, provider delivery and live runtime are not established). |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ME-14.md](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/ME-14.md), [ME-14_PLAN.md](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/ME-14_PLAN.md), [ME-14_markers.json](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/ME-14_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Soạn title/content/channels và preview recipients đã chọn ở ME-13.
- In-scope: ME-13 → giữ course + unique Student int64 IDs (`history.state`); title/body preview; explicit PUSH/EMAIL selection; POST #63; accepted UUID routes to notification-only SH-07/#18. #62 belongs to ME-13; ME-14 does not refetch it. Delivery/provider behavior remains outside this implementation.
- Out-of-scope: Xem gate bên dưới; không kết luận browser runtime đã chạy hoặc #63 send đã được tích hợp.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-25 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Soạn title/content/channels và preview recipients đã chọn ở ME-13. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #62, #63
- Liên kết màn hình dự kiến: [ME-15](../ME-15-TheoDoiGuiThongBao/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | draft/validating/sending/accepted/error |
| Current source/runtime | Current Study Client source | `SOURCE-WIRED` for #63 submit and SH-07 handoff; browser/live runtime not verified |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-14 source screen.png](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/screen_annotated.png))
- Luồng hiện tại: ME-13 hands course + selected Student recipients to ME-14 via router history state. ME-14 validates IDs and selection, sends trimmed text and explicit `PUSH`/`EMAIL` values to #63, accepts only the expected 202 Operation envelope with UUID, then routes to SH-07. #63 does not receive `course_id`, so its server-side common ACTIVE roster check cannot bind the request to the exact course chosen in ME-13. Queue acceptance does not prove provider delivery.
- Priority: P2; #63 source caller and SH-07 handoff are implemented and covered by focused tests. `content` is text per the accepted #63 contract update. Browser/live API, DB, worker/provider delivery and exact course binding remain unverified/out of scope.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

Current-source update 2026-11-21: `/mentor/notifications/new` is registered. ME14 validates ME13's in-memory course/recipient handoff and removes those identifiers from the current history entry after reading them, so reload/back cannot replay the same handoff. It sends trimmed title/text and explicit `PUSH`/`EMAIL` channels through #63, accepts only the expected 202 queued response with UUID, locks editing after acceptance and routes that UUID to SH-07. A malformed success or ambiguous network outcome blocks another submit in the current page because #63 has no idempotency key; a confirmed error remains distinguishable. The #63 request has no `course_id`, so the API cannot bind recipients to the exact selected course; accepted does not prove provider delivery. Focused Mentor tests pass; browser/live API/DB/provider runtime is unverified. Draft persistence is not implemented.

# ME-14 — Soạn thông báo mentor

> **Tình trạng tài liệu:** `DD READY` — đã đặc tả đầy đủ source prototype, luồng API hiện có, phần chưa có handler và các quyết định đang chặn triển khai.
>
> **Tình trạng triển khai tại lúc tạo DD (2026-11-08):** `IMPLEMENTATION BLOCKED` — recipient/course handoff, nội dung `int64`, channel, upload và lưu nháp chưa có contract phù hợp. Current source update 2026-11-21 is recorded below.
>
> **Tình trạng runtime:** `RUNTIME NOT VERIFIED` — Study Client route/component đã được wired theo source hiện tại; browser runtime và môi trường triển khai chưa được xác minh.

Ảnh nguồn: [screen.png](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/screen.png) · Ảnh đánh số: [screen_annotated.png](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/screen_annotated.png) · Bản đồ marker: [ME-14_markers.json](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/ME-14_markers.json) · Kế hoạch: [ME-14_PLAN.md](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/ME-14_PLAN.md)

## Trích đoạn tổng quan từ DD nguồn

> Nội dung bảng/rule bên dưới được ghi khi tạo DD ngày 2026-11-08. Các mô tả current/unwired và contract `content:int64` là snapshot lịch sử; phần trạng thái hiện tại ở trên là evidence mới hơn.

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID | ME-14 |
| Tên | Soạn và gửi thông báo tới học viên — Bước 2: Soạn thảo nội dung |
| Mục tiêu dự kiến | Soạn tiêu đề, nội dung, kênh gửi và xem trước cho tập người nhận đã chọn ở ME-13. |
| Actor/role dự kiến | Mentor. Đây là role trong prototype/API contract; route Study Web và kiểm tra quyền trên màn hình chưa được triển khai. |
| Route dự kiến | `/mentor/notifications/new` theo `apps/study-client/docs/list_screen.md`; chưa có route runtime. |
| Màn hình trước/sau | ME-13 Chọn người nhận → ME-14 Soạn nội dung → ME-15 Theo dõi gửi. ME-15 chưa phải scope của phiên này. |
| AC liên quan | AC-25, page trong `apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio`. |
| API được inventory gắn | #62, #63. #62 phục vụ roster ở bước chọn người nhận ME-13; chưa có bằng chứng ME-14 cần gọi lại #62. #63 là API gửi theo thiết kế AC-25, nhưng chưa được gọi từ HTML/Study Web. |
| Phụ thuộc status | API #64 đọc trạng thái theo từng `notification_id:int64`; SH-07 hiện dùng notification-only #18 theo Operation UUID. Generic operation kinds và status từng notification/batch remain outside AC-25. |
| Phụ thuộc upload | API #34 có purpose `SUBMISSION`/`LECTURE`; chưa có purpose hoặc quan hệ attachment cho notification. |
| Study Web at DD generation | `UNWIRED`. HTML nguồn chỉ là prototype tĩnh; current source route/component evidence is recorded in the 2026-11-21 implementation note above; it does not prove browser runtime. |
| Source assets | `screen.png` và `code.html` được giữ nguyên. Hash ban đầu và checklist được ghi trong [ME-14_PLAN.md](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/ME-14_PLAN.md). |

### Điều kiện truy cập và sau xử lý

- **Điều kiện dự kiến:** Mentor có phiên hợp lệ; ME-13 đã cung cấp danh sách Student ID int64 và course context đã được contract xác nhận; title/content/channel đã đáp ứng quy tắc sản phẩm. Những điều kiện dữ liệu này chưa được nối với Study Web.
- **Hiện trạng khi mở:** Prototype hiển thị trạng thái “chưa xác định nhóm người nhận”; title/body rỗng; In-app được chọn; Email bị khóa; gửi bị disable; lưu nháp nhìn thấy nhưng chưa có handler.
- **Sau khi soạn:** Không có trạng thái ứng dụng được ghi lại. JavaScript chỉ cập nhật preview/counter trong DOM.
- **Sau khi gửi theo API #63 (conditional, chưa tích hợp):** HTTP 202 có nghĩa request đã được lưu và queued. Response gồm Operation UUID riêng và `meta.notification_ids[]` chứa ID int64 từng notification. Không khẳng định message đã đến người nhận.
- **Sau lỗi:** API #63 khai báo 401/403/422/503/500. Hiện chưa có client handler để hiển thị hoặc giữ input theo từng lỗi.

### Quy tắc nghiệp vụ và bảo mật

1. Không gửi nếu tập người nhận chưa được xác thực. Đây là trạng thái/ý định của prototype; cách xác thực và giữ selection chưa có UI runtime.
2. ME-13 chọn Student ID int64 nhưng không có carrier/cách lưu state đã được chốt. Không tự đưa IDs vào query string, session/local storage hoặc route state.
3. API #63 request nhận `recipients:string` CSV, `title:string` tối đa 200 ký tự, `content:int64`, `channels:string` CSV. Prototype lại nhập body văn bản tự do, giới hạn title 120 và thể hiện In-app/Email. Không cast text thành integer và không coi `PUSH` là mapping đã duyệt cho In-app.
4. API #63 không nhận `course_id`; source kiểm tra recipients có cùng thuộc ít nhất một course ACTIVE do Mentor trực tiếp sở hữu. Đây là mapping local `DERIVED`, không ràng buộc chắc chắn tới course được chọn ở ME-13.
5. API #63 không nhận file hoặc idempotency key. Gửi lại sau timeout có thể tạo batch khác. Worker/provider gửi push/email chưa wired.
6. Tách `data.id` Operation UUID khỏi `meta.notification_ids[]` int64. API #64 dùng notification ID; không dùng Operation ID làm path.
7. Không lưu nội dung thông báo, thông tin người nhận hoặc token trong log/UI lỗi. Chính sách chi tiết cần theo common auth/response contract khi triển khai.

### Discrepancy chính

| Chủ đề | Expected/design source | Current source | Tác động |
|---|---|---|---|
| Body | Nội dung tự do, toolbar định dạng, preview | #63 yêu cầu `content:int64`; toolbar không có handler | **BLOCKER:** chưa thể tạo payload gửi hợp lệ. |
| Title | Prototype `maxlength=120` | #63 model cho phép tối đa 200; local DDL có title limit; API DD còn Draft | Giữ 120 là thuộc tính prototype; chủ contract cần chốt giới hạn. |
| Recipient/course | ME-13 đã chọn scope | #63 chỉ nhận CSV IDs, không có `course_id`, tự suy ra common owned course | **BLOCKER:** handoff và scope chưa bảo toàn course selection. |
| Channel | In-app checked; Email disabled | #63 token `PUSH`/`EMAIL`, không có worker/provider | **BLOCKER:** chưa duyệt channel mapping/khả năng giao. |
| Attachment | PDF/DOCX/ZIP, tối đa 25 MB | Không có input/handler; #34 không hỗ trợ notification purpose; #63 không có attachment field | **BLOCKER:** copy prototype không được hiểu là contract. |
| Save draft | Nút hiện và có vẻ enabled | Không có draft API hoặc persistence | **BLOCKER:** không thể lưu nháp. |
| Operation tracking | inventory có API #18 downstream | Study #18 không có route/module/query/test; AC-25 không có edge #18 | **UNWIRED:** không poll #18 từ ME-14. |
