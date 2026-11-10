# ME-14 — Soạn thông báo mentor · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-14` |
| Module | Mentor |
| Route | `/mentor/notifications/new` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Tình trạng tài liệu:** `DD READY` — đã đặc tả đầy đủ source prototype, luồng API hiện có, phần chưa có handler và các quyết định đang chặn triển khai.; **Tình trạng triển khai:** `IMPLEMENTATION BLOCKED` — recipient/course handoff, nội dung `int64`, channel, upload và lưu nháp chưa có contract phù hợp.; **Tình trạng runtime:** `RUNTIME NOT VERIFIED` — Study Web chưa wired; không có kiểm tra trình duyệt hoặc môi trường triển khai. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ME-14.md](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/ME-14.md), [ME-14_PLAN.md](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/ME-14_PLAN.md), [ME-14_markers.json](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/ME-14_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Soạn title/content/channels và preview recipients đã chọn ở ME-13.
- In-scope: ME-13 → giữ course + unique Student int64 IDs (carrier chưa chốt); POST #63 chỉ sau khi chốt scope/body/channel. #62 thuộc roster ME-13, không refetch ở ME-14. #63 trả Operation UUID và `meta.notification_ids[]`; #64 là status theo từng notification ID. Không gọi #18: Study route chưa wired, ID/lifecycle unresolved và AC-25 không có edge #18.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

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
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-14 source screen.png](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/screen_annotated.png))
- Luồng: ME-13 → giữ course + unique Student int64 IDs (carrier chưa chốt); POST #63 chỉ sau khi chốt scope/body/channel. #62 thuộc roster ME-13, không refetch ở ME-14. #63 trả Operation UUID và `meta.notification_ids[]`; #64 là status theo từng notification ID. Không gọi #18: Study route chưa wired, ID/lifecycle unresolved và AC-25 không có edge #18.
- Priority: P2; Gate/source status: **R**; #63 route/module/model/query/test có local source; API DD Draft/DERIVED. **DD READY; IMPLEMENTATION BLOCKED:** ME-13 handoff/course binding, `content:int64` vs free text, title 120 vs 200, In-app↔PUSH/email-worker, attachment và draft persistence chưa có contract; Study Web UNWIRED; runtime chưa verified

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ME-14 — Soạn thông báo mentor

> **Tình trạng tài liệu:** `DD READY` — đã đặc tả đầy đủ source prototype, luồng API hiện có, phần chưa có handler và các quyết định đang chặn triển khai.
>
> **Tình trạng triển khai:** `IMPLEMENTATION BLOCKED` — recipient/course handoff, nội dung `int64`, channel, upload và lưu nháp chưa có contract phù hợp.
>
> **Tình trạng runtime:** `RUNTIME NOT VERIFIED` — Study Web chưa wired; không có kiểm tra trình duyệt hoặc môi trường triển khai.

Ảnh nguồn: [screen.png](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/screen.png) · Ảnh đánh số: [screen_annotated.png](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/screen_annotated.png) · Bản đồ marker: [ME-14_markers.json](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/ME-14_markers.json) · Kế hoạch: [ME-14_PLAN.md](../../screen_stitch/04_mentor/ME-14_soan-thong-bao-mentor/ME-14_PLAN.md)

## Trích đoạn tổng quan từ DD nguồn

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
| Phụ thuộc status | API #64 đọc trạng thái theo từng `notification_id:int64`; API #18 generic operation hiện `UNWIRED` và chưa nối vào luồng AC-25. |
| Phụ thuộc upload | API #34 có purpose `SUBMISSION`/`LECTURE`; chưa có purpose hoặc quan hệ attachment cho notification. |
| Study Web | `UNWIRED`. HTML nguồn chỉ là prototype tĩnh; không chứng minh route, session, API integration, lưu trữ hoặc trạng thái runtime. |
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
