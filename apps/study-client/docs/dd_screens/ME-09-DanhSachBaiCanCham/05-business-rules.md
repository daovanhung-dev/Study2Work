# ME-09 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ME-09-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Lọc course/status, danh sách bài nộp có deadline/owner.
- Gate/status (giữ nguyên): **D**; **BLOCK:** Response cardinality #54 sai kiểu
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

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

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
