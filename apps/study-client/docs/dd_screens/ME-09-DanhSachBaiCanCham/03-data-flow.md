# ME-09 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

### B.1. Luồng tải màn hình dự kiến

1. Người dùng vào route đề xuất `/mentor/submissions`. Study Web route chưa tồn tại; guard, token source và fallback phiên hết hạn chưa được triển khai.
2. Client cần gửi Bearer token cho #54. Server kiểm tra chữ ký/subject/role MENTOR trước mọi DB access. Client role label không thay thế authorization của server.
3. Khi contract đã duyệt, client gọi #54 với filter defaults được xác nhận. API hiện chấp nhận query `course_id`, `status`, `page`; không gửi `size`, `q` hoặc sort.
4. Server count/list giới hạn dữ liệu đến course có `mentor_id` bằng authenticated JWT subject; response được sắp mới nhất trước theo `submitted_at`, sau đó `id` giảm dần.
5. Client phải phân biệt `items=[]` (empty success) với HTTP/network error. API #54 không trả partial result.
6. Khi có `items`, client cần render theo row layout đã được phê duyệt. Hiện không có screenshot/HTML loaded state để quyết định trường hiển thị, deadline, owner/course label hay link file.
7. Khi chọn row, chuyển `data.items[].id` sang ME-10 path `submission_id`; #55 mới tải chi tiết. Chấm điểm #56 và feedback #57 chỉ diễn ra ở ME-10.

### B.2. Handoff ME-09 → ME-10

```mermaid
flowchart LR
  ME09[ME-09 danh sách] -->|GET #54: Page<Submission>, current source| LIST[(data.items)]
  LIST -->|chọn data.items[].id| ME10[ME-10 chi tiết]
  ME10 -->|GET #55| DETAIL[(Submission detail)]
  ME10 -->|POST #56 grade; độc lập| GRADE[(Score/status)]
  ME10 -->|POST #57 feedback; độc lập| FEEDBACK[(Feedback)]
```

Sơ đồ trên nối expected screen flow với current API source. Nó không chứng minh frontend navigation hoặc cache đã được wired. API #55 source hiện đọc submission trực tiếp theo ID và áp dụng direct-owner Mentor policy; nó không trả rubric trong current response. Không suy luận dữ liệu hoặc thao tác #55–#57 trên ME-09.

### Trích từ DD nguồn: E. Trạng thái, bảo mật và khả năng truy cập

### E.1. Ma trận trạng thái

| State | Điều kiện chuyển vào | UI/behavior | Mức bằng chứng |
|---|---|---|---|
| `loading` | Route entry hoặc request #54 đang pending. | Không hiển thị empty copy như kết quả cuối trước response. | Required design; chưa có trong asset/source. |
| `empty` | HTTP 200, `data.items=[]` (bao gồm no match/missing course trong source). | Có thể dùng empty visual hiện tại sau khi sửa copy về direct-owner/no match và bỏ auto-sync claim chưa được chứng minh. | Asset hiện có; runtime mapping chưa wired. |
| `ready` | HTTP 200, `data.items.length>0`. | Cần row/card, field list, paging và row action được duyệt; không có mock loaded asset. | API source-backed; UI design gap. |
| `refreshing` | Người dùng bấm reload và #54 request đang chạy. | Prototype hiện chỉ animate cục bộ; chưa có network state. | UNWIRED. |
| `error` | Network error hoặc server 500. | Hiển thị lỗi; retry/keep-old-data policy cần chốt. | Current API error source; UI chưa wire. |
| `auth-required` | #54 trả 401. | Theo auth flow đã duyệt; screen không tự xử lý/refresh token theo giả định. | Server source-backed; client flow UNWIRED. |
| `access-denied` | #54 trả 403. | Báo không đủ quyền; không render sample data. | Server source-backed. |
| `filter-validation-error` | #54 trả 422 do numeric range/request constraints. | Gắn lỗi vào query/control hợp lệ; status unknown hiện có thể empty 200. | Server source-backed; UI chưa wire. |
| `navigating-detail` | User activate một row đã tải. | Dùng item `id` làm #55 path; tránh gửi nhầm assignment ID. | Handoff expected; row/route chưa tồn tại. |

```mermaid
stateDiagram-v2
  [*] --> loading
  loading --> empty: 200 + items=[]
  loading --> ready: 200 + items>0
  loading --> auth-required: 401
  loading --> access-denied: 403
  loading --> filter-validation-error: 422
  loading --> error: network/500
  ready --> refreshing: click reload (future request)
  empty --> refreshing: click reload (future request)
  refreshing --> ready: 200 + items>0
  refreshing --> empty: 200 + items=[]
  refreshing --> error: network/500
  ready --> navigating-detail: select item.id
```

### E.2. Bảo mật và data handling

- API #54 là boundary bảo mật: shared guard yêu cầu role `MENTOR` trước DB; mọi count/list query lọc theo direct `courses.mentor_id`. Không coi hidden UI hoặc role label từ HTML là authorization.
- Theo fallback hiện hành, assigned Mentor không có access relation. Không cho UI giả định assignment/course membership tương đương direct owner. Nếu #54 trả 403, không thử gọi #55 bằng cùng ID để vượt scope.
- API list có thể trả `content`, `files`, `user_id`, `score`, `feedback`. Chỉ render các field khi row layout và disclosure policy được duyệt; không suy tên Student, deadline hoặc rubric từ ID/copy. Secure URL/download semantics của file chưa được xác minh.
- API #54 chỉ đọc. UI không được báo mutation, “đã chấm” hay “đã đồng bộ” do riêng việc mở danh sách.

### E.3. Accessibility/design checks

- Study Web design target yêu cầu keyboard operation, focus-visible rõ, label gắn với input, accessible name cho icon-only control, state không phụ thuộc màu, control cao tối thiểu 44px, reflow đến 320 CSS px và reduced motion.
- HTML hiện gắn `label for` cho course/status/search; controls khoảng 44px. Avatar/bell và content status cần accessible name/semantics rõ; empty/loading/error announcements và row keyboard interaction chưa có.
- Footer ghi “Chuẩn kiểm định WCAG 2.1 AA” là copy, không phải kết quả audit. Không gọi màn hình đạt WCAG hoặc responsive/runtime verified trong phiên này.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #54; click submission_id → ME-10; không khẳng định response Page khi contract chỉ Submission.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [ME-09](../../screen_stitch/04_mentor/ME-09_danh-sach-bai-can-cham/ME-09.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
