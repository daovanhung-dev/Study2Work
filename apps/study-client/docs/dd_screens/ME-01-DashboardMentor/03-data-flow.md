# ME-01 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: 3. Luồng màn hình tổng quát

1. Browser yêu cầu route đề xuất `/mentor`. Study Web hiện không có route source, nên bước mount/guard chưa được xác minh.
2. Tiền điều kiện nghiệp vụ là Mentor đã đăng nhập. Khi request tới server, #46/#54/#58 tự kiểm Bearer JWT, claims số và role `MENTOR`. Không dùng API #04 để xác minh Mentor vì API #04 yêu cầu `STUDENT`; chưa có current Mentor `/me` endpoint trong client contract này.
3. Theo inventory, dashboard cần lấy dữ liệu từ #46/#54/#58. Các request là read-only, không phụ thuộc response lẫn nhau ở backend; thứ tự/concurrency, cache và retry của client chưa được xác nhận. Không tuyên bố đã có parallel fetch.
4. Từng response phải được phân tích theo envelope thật và map riêng cho widget. `200` với empty collection là trạng thái rỗng hợp lệ. Lỗi một API không được che thành lỗi toàn màn hình nếu giữ yêu cầu widget độc lập, nhưng cách hiển thị/retry cụ thể cần thiết kế.
5. Dữ liệu #46 có thể hỗ trợ course title/description/thumbnail/price/status/mentor và tổng pagination. #54/#58 hiện không đủ projection để tái tạo nguyên các hàng mẫu. Các widget rating/lịch/thông báo/shift/profile chưa có contract và phải được giải quyết trước khi mô tả như dữ liệu động.
6. Người dùng có thể chọn điều hướng đến course, submission hoặc support. Các đích là route đề xuất; link trong HTML không hoạt động. Direct CTA tới ME-10/ME-12 chưa thống nhất với AC list-first.
7. Khi rời dashboard, không có side effect được xác nhận. Mọi GET hiện tại là read-only; không ghi cache/session/analytics theo bằng chứng trong client checkout.

### Trích từ DD nguồn: 7. State matrix

States dưới đây phân biệt response của từng widget với state toàn trang; chúng không tuyên bố đã có trong client.

| State | Điều kiện | UI/data behavior cần giữ | Bằng chứng / quyết định còn thiếu |
|---|---|---|---|
| `loading` per widget | Request tương ứng đang xử lý. | Một widget đang tải không được làm biến mất kết quả thành công của widget khác theo inventory. Skeleton/placeholder detail chưa có thiết kế xác nhận. | Expected từ list_screen; no runtime. |
| `ready` | API trả 200 `DESIGN_RESOURCE_RETRIEVED` và items có dữ liệu. | Chỉ map field có trong response model; không hiển thị fake counts/title/rating/SLA. | #46/#54/#58 source-backed; field mismatch còn mở. |
| `empty` | #46 page items rỗng; #54 page items rỗng; #58 `data=[]`. | Empty là success, không phải 404. Copy/CTA empty-state cần thiết kế. | Current API source. |
| `partial` | Tối thiểu một widget thành công trong khi widget khác lỗi/tải. | Giữ widget độc lập; không biến lỗi một API thành nội dung giả. | Inventory yêu cầu partial; exact shell presentation chưa có. |
| `unauthenticated` | 401 `DESIGN_AUTHENTICATION_REQUIRED`. | Handoff login/refresh/session clear chưa được quy định cho Mentor Web. | Server behavior source-backed; client behavior UNWIRED. |
| `forbidden` | 403 `DESIGN_ACCESS_DENIED` do role/course scope. | Không retry cùng token như lỗi mạng; access-denied destination/copy chưa có app router. | Server source-backed. |
| `validation-error` | 422 `DESIGN_VALIDATION_ERROR` từ query/input. | Lỗi input không được map thành empty. Dashboard không nên gửi filter không xác nhận. | #46 validator; #54/#58 route field validation. |
| `request-error` | 500 hoặc network failure. | Hiển thị lỗi độc lập với trace ID nếu có; automatic retry/timeout/stale display chưa được thiết kế. | API 500 source-backed; network UI not wired. |
| `unsupported-widget` | Rating, schedule, notices, unread/profile data chưa có source. | Không render sample numbers như dữ liệu; hide/placeholder/error treatment cần Product chốt. | `NOT_FOUND` trong API được screen tham chiếu. |

### Trích từ DD nguồn: 8. Điều hướng, quyền và dữ liệu truyền

| Từ | Đích dự kiến | Dữ liệu truyền | Điều kiện / trạng thái |
|---|---|---|---|
| Header/course “Tất cả lớp học” | ME-02 `/mentor/courses` | Không cần ID | Inventory link; route runtime `UNWIRED`. |
| Course “Workspace” | ME-03 `/mentor/courses/:courseId` | `Course.id` từ API #46 | Screenshot CTA; direct route cần được xác nhận; server vẫn phải kiểm ownership. |
| Course content-tree icon | ME-06 `/mentor/courses/:courseId/content` | `Course.id` từ #46 | Label “Xem cây nội dung”; target/flow chưa được link ở dòng ME-01 inventory. |
| Header/grading “Xem tất cả” | ME-09 `/mentor/submissions` | Không cần ID | Inventory link; route runtime `UNWIRED`. |
| Submission preview action | ME-10 `/mentor/submissions/:submissionId` hoặc ME-09 trước | `Submission.id` nếu direct | Asset cho ME-10; AC-23/list flow qua ME-09; `DISCREPANCY`, Product quyết định. |
| Header/support “Mở Workspace” | ME-11 `/mentor/support` | Không cần ID | Inventory link; route runtime `UNWIRED`. |
| Support preview action | ME-12 `/mentor/support/:requestId` hoặc ME-11 trước | `SupportRequest.id` nếu direct | Asset cho ME-12; AC-24/list flow qua ME-11; `DISCREPANCY`, Product quyết định. |
| Notifications, schedule, announcement, footer | Chưa xác định | Không truyền data từ sample | Không tạo route hoặc external link. |

Các API list kiểm soát owner/role ở server. Không xem ẩn menu hoặc parse role ở client là authorization. Không có xác nhận refresh/logout/return-to-route policy cho dashboard.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #46/#54/#58 theo quyền; mỗi widget có trạng thái lỗi độc lập.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [ME-01](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
