# ME-11 — Hộp thư hỗ trợ học viên · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-11` |
| Module | Mentor |
| Route | `/mentor/support` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `DD BLOCKED` — đã đặc tả đầy đủ empty-state nguồn và truy vết API #58; loaded inbox, mapping filter và một số contract sản phẩm còn thiếu nên chưa đủ cơ sở triển khai mọi trạng thái.; **Implementation status:** `IMPLEMENTATION BLOCKED` — Study Web chưa có source/router; các quyết định loaded-state/filter và UI claim chưa được xác nhận.; **Runtime status:** `RUNTIME NOT VERIFIED` — không có ME-11 app route/runtime trong checkout; phiên docs này không chạy test hoặc ứng dụng. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ME-11.md](../../screen_stitch/04_mentor/ME-11_hop-thu-ho-tro-hoc-vien/ME-11.md), [ME-11_PLAN.md](../../screen_stitch/04_mentor/ME-11_hop-thu-ho-tro-hoc-vien/ME-11_PLAN.md), [ME-11_markers.json](../../screen_stitch/04_mentor/ME-11_hop-thu-ho-tro-hoc-vien/ME-11_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Inbox request thuộc course Mentor phụ trách; status/course filters và empty/ready/error states.
- In-scope: GET #58; chuyển `data[].id` sang ME-12; không tự thêm contact fields.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-24 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Inbox request thuộc course Mentor phụ trách; status/course filters và empty/ready/error states. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #58
- Liên kết màn hình dự kiến: [ME-12](../ME-12-TraoDoiVaDongYeuCau/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/empty/ready/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-11 source screen.png](../../screen_stitch/04_mentor/ME-11_hop-thu-ho-tro-hoc-vien/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-11_hop-thu-ho-tro-hoc-vien/screen_annotated.png))
- Luồng: GET #58; chuyển `data[].id` sang ME-12; không tự thêm contact fields.
- Priority: P2; Gate/source status: **R**; **BLOCK:** #58 có route/view/query/model/test source và DDL/migration 008 local, nhưng projection/lifecycle là DERIVED, live schema chưa xác minh; loaded-row design, status grouping/counts, course slug→int64 mapping, full-thread không pagination, AC-24 precondition vs empty state, SLA/realtime/Meet claims và Study Web UNWIRED còn chặn

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ME-11 — Hộp thư hỗ trợ học viên

> **DD status:** `DD BLOCKED` — đã đặc tả đầy đủ empty-state nguồn và truy vết API #58; loaded inbox, mapping filter và một số contract sản phẩm còn thiếu nên chưa đủ cơ sở triển khai mọi trạng thái.
> **Implementation status:** `IMPLEMENTATION BLOCKED` — Study Web chưa có source/router; các quyết định loaded-state/filter và UI claim chưa được xác nhận.
> **Runtime status:** `RUNTIME NOT VERIFIED` — không có ME-11 app route/runtime trong checkout; phiên docs này không chạy test hoặc ứng dụng.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### A.1. Mục tiêu, role và ranh giới

| Thuộc tính | Mô tả |
|---|---|
| Screen ID | ME-11 |
| Tên | Hộp thư hỗ trợ học viên |
| Mục tiêu kỳ vọng | Mentor xem các yêu cầu thuộc phạm vi khóa học mình phụ trách, lọc danh sách, làm mới và mở yêu cầu để trao đổi ở ME-12. |
| Actor | Mentor; API #58 yêu cầu Bearer/JWT hợp lệ với role `MENTOR`. Danh tính hiển thị trong mockup là dữ liệu mẫu. |
| Route đề xuất | `/mentor/support`; đây là route trong inventory, Study Web chưa có router để xác minh. |
| API trong phạm vi màn hình | #58 `GET /api/v1/mentor/support/requests`. |
| API thuộc màn hình kế tiếp | ME-12 owns #59 detail, #60 reply and #61 resolve; ME-11 không gửi reply hoặc resolve. |
| Màn hình trước | ME-01 theo F09; header cũng thể hiện các mục điều hướng Mentor nhưng đích route chưa có trong HTML. |
| Màn hình kế tiếp | ME-12 theo yêu cầu chọn một request; truyền request ID từ `data[].id`. Route/parameter UI chưa được source frontend xác nhận. |
| Dữ liệu nhạy cảm | Tên/avatar học viên, nội dung trao đổi, attachment URL/metadata và course/request IDs. Chỉ render theo dữ liệu server đã scope; không ghi raw message/attachment vào log hoặc analytics. |
| Current frontend | `UNWIRED`: checkout không có source/package/router Study Web. `code.html` là prototype độc lập, không phải app runtime. |

### A.2. Điều kiện vào/ra và API boundary

- **Expected entry:** Mentor mở ME-11 từ ME-01 hoặc điều hướng được duyệt. AC-24 bắt đầu bằng GET #58; inventory cho phép `loading/empty/ready/error` và yêu cầu danh sách theo khóa học Mentor phụ trách.
- **Current API #58:** route nhận `course_id` tùy chọn kiểu positive signed-int64, `status` tùy chọn string; Bearer header; response `ApiEnvelope<SupportRequest[]>`. API DD #58 vẫn `Draft — Needs Confirmation`; collection shape, BIGINT schema, lifecycle và attachment mapping là fallback được chọn cho local implementation, chưa phải contract-owner approval.
- **Expected exit:** khi chọn request đã hiển thị, chuyển `data[].id` sang ME-12. F09 định tuyến tiếp #59 → #60 → #61 trong ME-12. Không gọi #59 từ ME-11 theo inventory hiện hành.
- **Không có Student producer xác nhận:** source route hiện có các Mentor support APIs #58–#61, nhưng không tìm thấy endpoint Student tạo support request. Không suy ra CTA/tạo mới cho Student từ empty-state copy.
- **Dữ liệu trả về:** #58 gồm toàn bộ `messages[]` cho từng request, dù #59 cũng đọc thread. Không phân trang/giới hạn; trước khi triển khai inbox cần chốt payload grain và cách dùng thread từ list.

### A.3. Expected behavior và current behavior

**Expected behavior** lấy từ [inventory ME-11 và F09](../../list_screen.md), [UC24](../../../../../docs/diagrams/UC_UNICA.drawio), [AC-24](../../../../study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio): Mentor vào inbox hỗ trợ, xem/filte requests có quyền, chuyển request đã chọn tới ME-12. Inventory nêu status filter, course filter và empty/ready/error states. AC-24 bắt đầu #58 nhưng precondition của activity nói Mentor đã có một request trong scope.

**Current behavior** lấy từ screenshot/HTML và Study Server source: ảnh và HTML chỉ có empty state cùng controls tĩnh; tab click chỉ đổi selected styling/ARIA, select không có handler, refresh chỉ chạy animation cục bộ 650 ms rồi thay dòng đồng hồ. HTML không gọi API. Study Web chưa có app source. API #58 đã có route/module/query/model và test source; test history dùng fake session, không chứng minh schema live hoặc migration đã deploy.

### A.4. Discrepancy và blocker

| ID | Bằng chứng / chênh lệch | Ảnh hưởng và quyết định cần có |
|---|---|---|
| ME11-B01 — Empty state vs AC precondition | Screenshot/inventory cần empty state; AC-24 precondition nói đã có request trong scope. | Xác nhận empty state thuộc ME-11 hay chỉ ngoài luồng AC-24; không xóa một trong hai bằng suy luận. |
| ME11-B02 — Loaded list design | PNG/HTML không có request row/card, paging, sorting hoặc loaded state. | Cần duyệt cấu trúc row, field hiển thị, thứ tự, attachment preview và cách mở ME-12. DD blocked cho ready state. |
| ME11-B03 — Status tabs/counts | UI có All/Open/Resolved và số 0 mẫu. API status là exact optional string, không trả facets/counts; DDL fallback liệt kê `OPEN`, `IN_PROGRESS`, `WAITING_LEARNER`, `RESOLVED`, `CANCELLED`. | Chốt grouping của Open, nơi hiển thị CANCELLED và nguồn/count semantics; không suy ra status filter từ nhãn. |
| ME11-B04 — Course options | Prototype values `all`, `fe-adv`, `be-node`, `fullstack-capstone`; #58 cần positive int64. API #58 chỉ trả `course_id`, không có title. #46 course list là nguồn ứng viên nhưng chưa được nối vào ME-11. | Chốt API/field map cho option labels và IDs, all sentinel, loading/error state; không gửi slug làm `course_id`. |
| ME11-B05 — Thread grain/pagination | #58 tải toàn bộ messages + attachments cho mọi row, không pagination; #59 đọc lại thread. | Chốt projection/paging và giới hạn vận hành/riêng tư trước khi dùng dữ liệu này trong danh sách lớn. |
| ME11-B06 — Claims không có source | Mockup ghi SLA `<4 giờ`, cập nhật tức thì/auto notification, kho câu trả lời chuẩn, Google Meet. #58 và HTML không chứng minh SLA, push, template hoặc meeting integration. | Product cần xác nhận hoặc sửa các claim/đích link trước triển khai. |
| ME11-B07 — Student request producer | Không thấy route tạo support request phía Student trong current scoped source. | Chưa thể mô tả nguồn tạo dữ liệu hoặc CTA gửi hỗ trợ phía Student. |
| ME11-B08 — Schema/deployment | `DB.sql` và migration 008 có support tables BIGINT; live schema/deployment chưa được truy cập. V1-PILOT UUID model là thiết kế khác. | Dùng trạng thái `SOURCE_BACKED_WITH_DERIVED_PROJECTIONS`; không đánh dấu migration/runtime DB verified. |
| ME11-B09 — Query/auth precedence | FastAPI validate `course_id` trước khi gọi route/view auth; malformed/out-of-range có thể trả 422 trước 401/403. Catalog không mô tả precedence. | Contract cần xác nhận hành vi request vừa thiếu auth vừa invalid query; không dùng 422 làm bằng chứng đã xác thực. |
| ME11-B10 — Runtime/design system | HTML dùng bright-blue palette, CDN Tailwind và Google Fonts; intended Study design page khác palette; app source không có. | Chốt việc dùng visual reference, font/CDN và responsive behavior trong Study Web implementation. |
