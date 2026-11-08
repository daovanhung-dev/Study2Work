# ST-01 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

1. **Đi vào route:** Inventory đề xuất `/student`; precondition theo AC là Student đã đăng nhập. Current Study Web router/source không có, nên không xác nhận direct-entry, page guard hoặc redirect.
2. **Khởi tạo:** Inventory muốn các widget độc lập, nạp #20/#21 khi vào trang, #38/#43 lazy hoặc parallel. AC-13 gọi #20 rồi #21; AC-18 đặt #21 → #37 → #38. Ghi nhận `DISCREPANCY`; không chọn một thứ tự làm contract.
3. **Nạp khóa học:** API #20 catalog có optional `status`/`page`, nhưng response `UserProfile` chưa thể map thành course list theo AC-13. Không gửi default/filter tự tạo.
4. **Nạp tiến độ:** API #21 query grammar và response chưa mô tả progress aggregate. Không ghép theo `course_id`, tính % hoặc tổng hợp lesson/quiz/assignment khi chưa có contract.
5. **Nạp achievements:** API #38 `Page<Achievement>` có contract design-only. Chỉ record được backend xác nhận mới có thể hiển thị sau khi award/projection/empty rules được chốt; không suy chứng nhận/proof từ copy.
6. **Nạp notification:** API #43 `Page<Notification>` design-only. “Latest” order, recipient, unread state và projection chưa rõ; không dùng URL prototype `/notifications/latest`.
7. **Trạng thái widget:** Mỗi widget cần giữ trạng thái loading/empty/partial/error độc lập theo inventory; hiện chỉ có gated static panel. Không đổi 401/403/500/network failure thành empty.
8. **Đi tiếp:** Course CTA tham chiếu ST-08, progress CTA ST-20, notification CTA ST-26. Các `href="#"` hiện tại không điều hướng; không truyền course ID, notification ID hoặc query chưa có nguồn.
9. **Rời trang:** Header, breadcrumb, profile và footer anchors vẫn là placeholder. Back-stack, target legal/help và route ngoài các liên kết inventory chưa được xác nhận.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

### E.1. State matrix

| State | Entry condition | UI/data rule | Current evidence / exit |
|---|---|---|---|
| `static-gated` | HTML hand-off initial render. | Chỉ hiện status/unavailable copy; không có synthetic data. | Đây là state duy nhất thấy trong source asset; không phải API state. |
| `loading` | Inventory target sau khi widget request được bắt đầu. | Widget-local loading; không blank-fill với dữ liệu giả. | Chưa có UI design/route/request source; exit chưa xác định. |
| `ready` | Approved success response và projection cho widget. | Chỉ render fields đã được contract duyệt. | Không có loaded-state design hoặc runtime response. |
| `empty` | Successful empty response theo từng API's approved wire shape. | Không đồng nhất với access/API/network error. | #20/#21/#38/#43 empty semantics chưa thống nhất; AC-13 empty edge đang lệch. |
| `partial-widget` | Một số widget thành công, một số lỗi/rỗng, theo policy được duyệt. | Giữ trạng thái riêng cho từng widget; không làm dashboard-wide success giả. | Inventory target; ordering/failure/retry policy chưa xác định. |
| `forbidden` / `error` | 403 hoặc API/transport error theo contract. | Giữ 401/403/500 và #20 422 distinct; không đổi thành empty. | Page-level copy, recovery/redirect chưa được Study Web source xác nhận. |

### E.2. Navigation và handoff

| From | Expected target | Data/guard | Current evidence |
|---|---|---|---|
| Course CTA | ST-08 `/student/courses` | Student; no extra param unless contract requires it. | Inventory link; HTML `href="#"`; no Study Web route. |
| Progress CTA | ST-20 `/student/progress` | Student; progress/course data contract open. | Inventory link; HTML `href="#"`; no route. |
| Notification CTA | ST-26 `/student/notifications` | Student; no notification ID/deep link supplied. | Inventory link; HTML `href="#"`; no route. |
| Learner profile/navigation | ST-02 `/student/profile` | Student session; profile source outside ST-01 inventory API set. | Inventory relationship; header nav/profile controls have placeholder links or static sample. |
| Header discussions/home/legal/help | Destination TBD | No route/data/query assumed. | All anchors are `#`; current Study router absent. |

API #44/#45 state changes belong to AC-20 notification-center flow; ST-01 does not mark notifications read. No IDs other than approved API inputs are carried between screens.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: Chỉ sau role STUDENT hợp lệ; load #20/#21; thành tích #38, thông báo #43 lazy/parallel.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [ST-01](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/ST-01.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
