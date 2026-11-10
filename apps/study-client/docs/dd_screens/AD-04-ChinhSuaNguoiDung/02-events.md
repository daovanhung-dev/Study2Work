# AD-04 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-04-EV-001` | `Source heading` / EV-01 — Mở AD-04 và tải UserProfile | See source event detail below |
| `AD-04-EV-002` | `Source heading` / EV-02 — Thay đổi trường form và tạo dirty state | See source event detail below |
| `AD-04-EV-003` | `Source heading` / EV-03 — Lưu thay đổi qua API #70 | See source event detail below |
| `AD-04-EV-004` | `Source heading` / EV-04 — Cancel hoặc quay lại AD-03 | See source event detail below |
| `AD-04-EV-005` | `Source heading` / EV-05 — API docs, gate và manual support request | See source event detail below |
| `AD-04-EV-006` | `Source heading` / EV-06 — Shell navigation, notifications, footer và status assertions | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết từng sự kiện

### EV-01 — Mở AD-04 và tải UserProfile

| Thuộc tính | Đặc tả |
|---|---|
| Trigger / loại | Route entry từ AD-03 hoặc direct route khi router được triển khai; `Load`. Marker liên quan #9, #10, #18, #20, #21, #22, #23, #25, #26. |
| Preconditions | Route và client tồn tại; nhận numeric `user_id` từ AD-03/#68; session/token còn hiệu lực; permission mapping được duyệt. Không coi `USR-*` là ID hợp lệ. |
| Input | Path `user_id` raw string; header `Authorization: Bearer <token>` theo catalog. Không query/body. `X-Trace-Id` chỉ khi client tuân theo middleware/API convention; optional header này không được catalog #69/#70 yêu cầu. |
| API | #69 `GET /api/v1/admin/users/{user_id}`. 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<UserProfile>`; 401/403/404/500 theo catalog. |

1. Nhận và parse path theo route; giữ ID dưới dạng chuỗi an toàn cho đến khi kiểm tra định dạng signed-int64 ở ranh giới API/client. Không đưa PII vào URL.
2. Kiểm tra auth/session theo auth shell đã được duyệt. Backend local #69 kiểm tra Bearer/claim `ADMIN` trước path/query; mapping claim sang quyền AC-31 vẫn là `DERIVED`.
3. Khởi tạo `loading`, giữ form controls/Save disabled và gọi #69 một lần. API catalog không có query/body.
4. Phân tích HTTP status, business code, envelope và `data`. Chỉ coi 200 + `DESIGN_RESOURCE_RETRIEVED` + `UserProfile` hợp lệ là success. Error envelope có `data:null`.
5. Map profile vào baseline: `id`, `full_name`, `email`, `role`, `status`, `phone`, `avatar_url`, timestamps. Field nào bị policy PII chặn thì không render. Organization, audit, SSO actor, sync và compliance không có trong response.
6. Khi dữ liệu hợp lệ, chuyển `ready`; controls vẫn read-only cho đến khi body/permission/policy được duyệt. Không map trạng thái rỗng thành dữ liệu mặc định.
7. 401 → `unauthenticated`; 403 → `forbidden`; 404 → `not-found`; 500/mạng/response không hợp lệ → `load-error`. Cho retry GET chỉ sau khi có UX/network policy; không tự động retry vô hạn.
8. Khi rời page, truyền cùng numeric ID sang route được duyệt; route hiện tại chưa có implementation.

### EV-02 — Thay đổi trường form và tạo dirty state

| Thuộc tính | Đặc tả |
|---|---|
| Trigger / loại | `input`/`change` trên các control được duyệt; hiện toàn bộ controls disabled. Marker #21, #25 và nếu được bổ sung trong thiết kế thì phone/avatar. |
| Preconditions | GET #69 đã thành công; actor có quyền; API #70 body/role mapping và field ownership được duyệt; gate/UI policy nếu tồn tại có contract. |
| Input | Baseline #69 `UserProfile`; field mới nhập. Candidate body runtime có 4 required keys `full_name:string`, `phone:string|null`, `avatar_url:string|null`, `role:STUDENT|MENTOR|ADMIN`; tất cả body/rules là `DERIVED`. |

1. Nhận giá trị control; giữ baseline response tách khỏi draft state.
2. Chuẩn hóa/validate theo schema đã được duyệt. Nếu implementation chọn đúng local candidate: trim full_name, yêu cầu nonblank/max 150; trim phone và blank→null/max20; trim avatar_url/blank→null, không có URL validation; role thuộc allowlist. Không chuyển alias `lecturer` nếu chưa có mapping.
3. Không cho sửa/gửi email, status hoặc adminNotes qua #70. Trường phone/avatar_url không hiển thị: nếu full-replacement body được duyệt, lấy từ baseline chính xác, gồm null; không tự để mất giá trị.
4. So sánh draft với baseline bằng field/normalization policy được duyệt để tính `dirty`. Chưa có quy tắc canonical casing/Unicode; cần owner quyết định nếu equality ảnh hưởng UX.
5. Khi có thay đổi hợp lệ, chuyển `dirty`; khi invalid, chuyển `validation-error` và gắn lỗi vào trường phù hợp. Nút Save chỉ enabled nếu mọi blocker được giải quyết và contract cho phép.
6. Không gọi API ở change event. Nếu user quay về/cancel, xử lý draft theo EV-04.

### EV-03 — Lưu thay đổi qua API #70

| Thuộc tính | Đặc tả |
|---|---|
| Trigger / loại | Click/submit Save (#36); hiện disabled và không có handler. |
| Preconditions | `ready/dirty`; required validation pass; actor và policy cho phép; numeric `user_id`; request body/schema và role mapping được owner duyệt; phone/avatar handling xác định. |
| API | #70 `PUT /api/v1/admin/users/{user_id}`; Bearer JWT/Admin; no query. Body catalog/AC `NOT SPECIFIED`. Local source candidate: strict JSON `{full_name:string, phone:string|null, avatar_url:string|null, role:"STUDENT"|"MENTOR"|"ADMIN"}`; 4 keys required, `extra=forbid`; status/body behavior DERIVED. |

1. Chặn double click/submit bằng client in-flight flag; build body từ field ownership đã duyệt. Không gửi email, status, `adminNotes`, ID, timestamps hay keys lạ.
2. Validate body trước request theo contract đã duyệt. Nếu contract chấp thuận current local candidate, dùng đúng normalization/range ở EV-02. Không giả định request partial: local model là full-replacement.
3. Chuyển `saving`; gửi đúng một PUT. Timeout/retry/idempotency behavior chưa có contract; không tự gửi lại khi kết quả commit chưa rõ.
4. Parse response. Chỉ HTTP 200 + `DESIGN_RESOURCE_UPDATED` + `ApiEnvelope<UserProfile>` hợp lệ là mutation success. Local view commit sau khi query row và response projection hợp lệ; zero-row 404; query/projection/commit lỗi rollback và 500. Đây là current local source behavior, chưa xác minh deployment/live schema.
5. Sau PUT success, dùng `data` làm evidence mutation đã thành công; theo inventory gọi GET #69 để revalidate profile. Nếu revalidation thành công, chuyển về AD-03 cùng `user_id`. Không gửi lại PUT chỉ vì GET sau save lỗi.
6. 422: hiển thị validation error và giữ draft. 401/403: giữ draft nếu auth shell cho phép, yêu cầu session/permission handling theo contract; không cho tiếp tục submit. 404: target user không còn tồn tại, hiển thị not-found và không refetch lặp. 500/network/timeout: giữ input; kết quả timeout có thể không xác định nên không tự retry.
7. Nếu GET sau successful PUT thất bại, trạng thái riêng `saved-refresh-error`: mutation đã được xác nhận bởi PUT, nhưng profile refresh/navigation chưa thành công. Cung cấp refresh GET theo policy; không coi thao tác như chưa lưu.

### EV-04 — Cancel hoặc quay lại AD-03

| Thuộc tính | Đặc tả |
|---|---|
| Trigger / loại | Click Back (#9) hoặc Cancel (#35); hiện hai đích khác nhau. |
| Preconditions | Có nguồn route/state để giữ numeric `user_id`. Unsaved-change confirmation policy cần được duyệt. |
| Input / xử lý | Nếu chưa dirty: navigate về AD-03 cùng ID theo route đã chốt. Nếu dirty: hiển thị confirm/discard chỉ khi product quyết định nội dung và draft preservation; không tự thêm modal. Không gửi API. |
| Kết quả | AD-03 tải hoặc giữ profile theo cache policy chưa được định nghĩa. Prototype hiện Back dùng string-code `/details`; Cancel mở `/admin/users`; cả hai cần sửa khi wire. |

### EV-05 — API docs, gate và manual support request

| Thuộc tính | Đặc tả |
|---|---|
| Trigger / loại | Click API docs (#16), gate/help callout (#37), send request (#38), hoặc thao tác liên quan gate (#11/#15/#34). |
| Preconditions | Destination/API/policy phải có contract và auth rules. Không có trong AD-04/#69/#70 hiện hành. |
| Input / xử lý | Không có request schema, ticket ID, API destination hoặc gate state source. Các nút hiện không handler. Giữ disabled/placeholder cho đến khi source được xác nhận; không tự tạo ticket/unlock endpoint. |
| Kết quả/lỗi | Không có chuyển trạng thái hay API response hiện tại. Static gate copy không được dùng để cho phép/chặn server mutation. |

### EV-06 — Shell navigation, notifications, footer và status assertions

| Thuộc tính | Đặc tả |
|---|---|
| Trigger / loại | Click header navigation, notifications, breadcrumbs, brand/footer links hoặc render các badge/copy #1–#8, #12–#14, #18, #22, #24, #27, #29–#33, #39–#40. |
| Preconditions | Route destinations và data source được định nghĩa. Hiện không có router/notification/health/audit/policy source trong Study Web hoặc API #69/#70. |
| Xử lý | Không coi `href="#"` là route. Không trình bày static `SYSTEM NORMAL`, verified API, 85% sync, audit/compliance/SSO/RBAC token, policy version là trạng thái runtime. Nếu UI được xây, render dữ liệu động chỉ từ source đã duyệt và kiểm soát PII. |
| Kết quả | Hiện tại prototype không xử lý event; không gọi API và không thay đổi state. |

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
