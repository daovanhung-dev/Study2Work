# AD-15 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-15-EV-001` | `Source heading` / Response/error mapping cho EV-01, EV-05 và EV-08 | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện và xử lý dữ liệu

| Event | Trigger / loại | Tiền điều kiện | Input → xử lý → output | API / lỗi / cập nhật |
|---|---|---|---|---|
| EV-01 | Mở danh sách / Load | Route, auth và permission đã được owner duyệt; UI/client được wire. | Session + filter đã được duyệt → gọi GET → đọc envelope → chỉ map fields theo response contract đã chốt → chọn ready/empty/error. | Candidate #87. 200 local `Page<Quiz>` khác catalog `Quiz`; 401/403/500 catalog, local có thêm 422. Không retry/cache policy. |
| EV-02 | Nhập tìm kiếm / Input | Search contract và query parameter được bổ sung/phê duyệt. Hiện chưa đạt. | Chuỗi input → hiện không chuẩn hóa/gửi đi vì chưa có validation/query definition → không đổi data. | Không có search trong #87; không gọi API. |
| EV-03 | Đổi khóa học / Change | Có options source và slug→numeric ID mapping đã duyệt. Hiện chưa đạt. | Slug UI → không thể chuyển thành `course:int64` bằng chứng hiện có → không gửi request. | #87 không có course-list API dependency được xác nhận tại AD-15; không gọi với slug. |
| EV-04 | Đổi status / Change | Status vocabulary/casing được owner chốt. Hiện chưa đạt. | `draft/active/closed` → không có mapping → không gửi request. | Source #87 giữ exact raw status, không enum-check; không tự normalize. |
| EV-05 | Refresh / Click | Client wired; query được duyệt. | Filter/page state → candidate GET #87 → process response theo contract → cập nhật list state. | Hiện chỉ animation 800 ms. Retry, timeout, dedupe, cache policy chưa định nghĩa; không retry tự động. |
| EV-06 | Advanced filters / Click | Control hiện disabled; chưa có filter model/design. | Click không được thực hiện → state không đổi. | Không có handler/API/query. |
| EV-07 | Tạo quiz / Click + navigation | CTA được enable sau khi route, permission và AD-16 contract duyệt. | Không có request body ở AD-15 → điều hướng candidate AD-16. | #88 thuộc AD-16; không POST từ AD-15. Current CTA disabled. |
| EV-08 | Previous/next / Click | Paginator được wire và page contract được duyệt. | Current page + direction → tính candidate page; chỉ gửi page int32 >=1. Local fallback 1-based, size 20. | Candidate GET #87; empty late page là 200 với `items=[]`; chưa có quy tắc auto-correct. Current buttons disabled. |
| EV-09 | Edit row / Click + navigation | Row/quiz ID hợp lệ từ response contract và action được duyệt. | Quiz ID → chuyển candidate sang AD-16; không dựng update body ở list. | #89 thuộc AD-16. Ảnh empty không có action; GET detail/edit data contract còn thiếu. |
| EV-10 | Delete row / Click + navigation | Row/action và policy attempts được AD-18 phê duyệt. | Quiz ID → chuyển candidate AD-18; không mutation tại list. | #90 thuộc AD-18; không DELETE tại AD-15. Confirmation/conflict behavior chưa chốt. |
| EV-11 | Statistics row / Click + navigation | Quiz ID và #91 response được thống nhất với AD-17. | Quiz ID → mở candidate AD-17; không tính KPI từ Quiz list. | #91 thuộc AD-17; analytics fields chưa xác nhận. |
| EV-12 | Shell/breadcrumb/footer / Click | Destination/session shell contract có thật. | Click anchor/button → hiện không có route/handler; không làm thay đổi data. | Không có API. Current anchors `#`; notification không có listener; identity/RBAC/system copy tĩnh. |

### Response/error mapping cho EV-01, EV-05 và EV-08

| Kết quả | Bằng chứng local #87 | Xử lý target có thể ghi nhận | Giới hạn |
|---|---|---|---|
| 200 có items | `success=true`, `businessCode=DESIGN_RESOURCE_RETRIEVED`, local `data.items`, `data.pagination`; quiz item metadata-only. | Candidate ready state khi client được wire và response contract được thống nhất. | Catalog chỉ khai báo `ApiEnvelope<Quiz>`; không map bốn cột thiếu. |
| 200 rỗng | Message `No quizzes found.`; `items=[]`, `total=0`, `total_pages=0`. | Candidate empty state. | Không đồng nghĩa chưa đồng bộ hoặc API lỗi. |
| 401 | `DESIGN_AUTHENTICATION_REQUIRED` theo shared auth contract. | Giao cho auth/session flow đã được xác nhận. | Recovery route/session refresh chưa thuộc AD-15. |
| 403 | `DESIGN_ACCESS_DENIED`. | Hiển thị access-denied state theo shared shell khi có implementation. | Fine-grained permission mapping chưa có; local gate là role `ADMIN`. |
| 422 | Local derived parser cho course/page sai định dạng hoặc ngoài range. | Validation error state nếu contract sau này giữ 422. | Catalog #87 không liệt kê 422; response mapping chưa được owner duyệt. |
| 500 | `DESIGN_INTERNAL_ERROR`; local query/count/projection failure rollback và trả safe error. | Candidate service-error state, giữ dữ liệu chỉ theo policy app chung. | Không có retry rule; nullable legacy fields có thể làm projection fail. |
| Network/timeout | Không có UI client source/policy. | Chưa chốt. | Không tự đặt retry, stale fallback hay toast copy. |

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
