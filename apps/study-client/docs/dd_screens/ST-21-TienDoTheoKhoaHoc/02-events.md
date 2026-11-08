# ST-21 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-21-EV-001` | `ST21-EV-01` / ST21-EV-01 — Vào trang và kiểm tra Student session | See source event detail below |
| `ST-21-EV-002` | `ST21-EV-02` / ST21-EV-02 — Chuẩn hóa `courseId` | See source event detail below |
| `ST-21-EV-003` | `ST21-EV-03` / ST21-EV-03 — Tải course progress qua API #37 | See source event detail below |
| `ST-21-EV-004` | `ST21-EV-04` / ST21-EV-04 — Xử lý response và map dữ liệu | See source event detail below |
| `ST-21-EV-005` | `ST21-EV-05` / ST21-EV-05 — Tổng hợp và render course state | See source event detail below |
| `ST-21-EV-006` | `ST21-EV-06` / ST21-EV-06 — Chọn lesson và tiếp tục học | See source event detail below |
| `ST-21-EV-007` | `ST21-EV-07` / ST21-EV-07 — Quay về ST-20 | See source event detail below |
| `ST-21-EV-008` | `ST21-EV-08` / ST21-EV-08 — Header và footer navigation | See source event detail below |
| `ST-21-EV-009` | `ST21-EV-09` / ST21-EV-09 — Xử lý lỗi API/session/network | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết sự kiện

### ST21-EV-01 — Vào trang và kiểm tra Student session

- **Trigger / điều kiện:** điều hướng tới route đề xuất `/student/progress/:courseId`; precondition expected là Student đăng nhập theo AC-18/API #37.
- **Input:** route segment `courseId`, app session/Bearer token. Hiện không có router, auth guard hoặc caller source trong Study Web.
- **Xử lý:** (1) xác nhận route target sau khi app router được tạo; (2) xác định session theo auth contract chung đã duyệt; (3) không coi prototype render là authenticated route; (4) server phải kiểm tra JWT/role ở API boundary.
- **Output:** expected screen entry; current result là `UNWIRED`, không có navigation/runtime được xác minh.
- **Ngoại lệ:** session thiếu/hết hạn và redirect/recovery chưa được screen/API #37 đặc tả ngoài status 401.

### ST21-EV-02 — Chuẩn hóa `courseId`

- **Trigger / điều kiện:** route entry có path segment.
- **Input:** UI `courseId` từ ST-20 expected link; API path `course_id:int64!`.
- **Xử lý:** (1) giữ nguyên nguồn course ID từ selected course; (2) chuẩn hóa representation sang path param chỉ theo parser/range rule đã duyệt; (3) không lấy ID từ title/copy; (4) API catalog không định nghĩa min/max hoặc malformed-path response.
- **Output:** path value chỉ đủ điều kiện gửi request khi int64 handling được xác nhận; hiện không có client behavior.
- **Ngoại lệ:** empty/non-numeric/overflow/negative ID đều là `SOURCE_REQUIRED`; không tự gán 400/404/422 ở client.

### ST21-EV-03 — Tải course progress qua API #37

- **Trigger / điều kiện:** Student session và course path value hợp lệ theo rule được phê duyệt.
- **Input:** `GET /api/v1/users/me/progress/{course_id}`; Authorization Bearer JWT; no query, no body.
- **Xử lý:** (1) map route param tới required int64 path; (2) không truyền user ID; (3) gửi GET; (4) chỉ HTTP 200 + `DESIGN_RESOURCE_RETRIEVED` là catalog success; (5) không thêm retry, timeout, cache hoặc dedupe policy khi chưa có contract.
- **Output:** catalog response `ApiEnvelope<UserProfile>`; API #37 hiện `DECLARED_NOT_RUNNABLE`, không có request runtime.
- **Errors:** catalog giữ nguyên 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`; không thêm 400/422.

### ST21-EV-04 — Xử lý response và map dữ liệu

- **Trigger / điều kiện:** API #37 trả success envelope.
- **Input:** `ApiEnvelope<UserProfile>` theo catalog/API #37 DD. UserProfile fields gồm identity/profile data, không có course/lesson/quiz/assignment progress.
- **Xử lý:** (1) xác minh `success/businessCode`; (2) không xem `data.id/full_name/email/role/status` là progress DTO; (3) không lấy user profile làm nguồn course title hoặc completion; (4) khi response schema được đổi/chốt, map fields đúng contract rồi mới render.
- **Output:** hiện chưa thể tạo loaded progress state từ response catalog; phải giữ DD/implementation blocker cho đến khi contract cập nhật.
- **Ngoại lệ:** malformed envelope, missing fields, unexpected type/nullability chưa có API #37 recovery policy.

### ST21-EV-05 — Tổng hợp và render course state

- **Trigger / điều kiện:** chỉ sau khi API response DTO, nguồn dữ liệu và aggregate rule được duyệt.
- **Input:** AC-18 đặt tên lesson, quiz và assignment progress; candidate tables/fields trong API DD/DB design chưa phải query/contract.
- **Xử lý:** (1) xác định tập lesson/quiz/assignment đủ điều kiện; (2) xác định attempt/submission được chọn và status; (3) chốt denominator, weighting, completion threshold, rounding và timestamp; (4) map unit status; (5) render `loading/empty/in-progress/completed` theo điều kiện có thẩm quyền; (6) không gán zero/empty khi request lỗi hoặc course chưa có progress nếu chưa có rule.
- **Output:** hiện không có công thức hoặc loaded-state design có thể triển khai. Static HTML chỉ minh họa empty fallback.
- **Ngoại lệ:** course chưa enroll/không có unit, hidden lesson, quiz/assignment chưa chấm, attempt đang làm, duplicate submissions và stale aggregate đều cần business rules.

### ST21-EV-06 — Chọn lesson và tiếp tục học

- **Trigger / điều kiện:** Student chọn lesson row khi loaded-state UI tồn tại; HTML hiện không có row/link nên event chưa có element.
- **Input:** `lesson_id` từ API progress contract được duyệt; user/session và course context.
- **Xử lý:** (1) kiểm tra lesson ID đến từ response đã xác nhận; (2) không truyền progress row như quyền truy cập; (3) chuyển qua ST-10/access gate trước khi ST-11 theo inventory; (4) không mở trực tiếp video/content hoặc bỏ qua entitlement check.
- **Output:** expected navigation ST-10/ST-11 only after gate; route/data handoff chưa có Study Web runtime.
- **Ngoại lệ:** lesson không còn tồn tại/không thuộc course/không được truy cập phải theo #22–#24/AC-14 contract; không tự gán lỗi của #37.

### ST21-EV-07 — Quay về ST-20

- **Trigger / điều kiện:** bấm breadcrumb “Tiến độ” hoặc CTA “Quay lại tổng quan tiến độ”.
- **Input:** static href `/student/progress`; browser navigation context. Không có course ID trong body/query.
- **Xử lý:** (1) dùng target route inventory của ST-20; (2) không tạo filter/state ngoài course ID; (3) giữ browser-back semantics theo router chung nếu được triển khai.
- **Output:** ST-20 overview là expected target; current route transition chưa wire.
- **Ngoại lệ:** route unavailable/session expiry handling chưa thuộc HTML/API #37 contract.

### ST21-EV-08 — Header và footer navigation

- **Trigger / điều kiện:** kích hoạt brand, header nav, breadcrumb home, footer terms/privacy/academic/support link.
- **Input:** prototype labels và href (`#`, hoặc ST-20 path cho Tiến độ).
- **Xử lý:** (1) chỉ mô tả links đang nhìn thấy; (2) không tạo search/notification/profile/support behavior; (3) không suy route thật từ `data-path`; (4) active nav Tiến độ chỉ là static styling.
- **Output:** destinations ngoài ST-20 không được xác minh bởi current Study Web source.
- **Ngoại lệ:** placeholder `#`, route/access guard, legal documents và focus/browser-back policy chưa được wiring.

### ST21-EV-09 — Xử lý lỗi API/session/network

- **Trigger / điều kiện:** API #37 trả error code hoặc client không nhận/không parse được response.
- **Input:** 401/403/404/500 trong catalog; transport/parse failures không có business code riêng.
- **Xử lý:** (1) giữ đúng `DESIGN_AUTHENTICATION_REQUIRED`, `DESIGN_ACCESS_DENIED`, `DESIGN_RESOURCE_NOT_FOUND`, `DESIGN_INTERNAL_ERROR`; (2) không hiển thị data protected sau 403; (3) không diễn giải 404 tự động thành empty progress; (4) không thêm retry/redirect/query validation code; (5) network/parse presentation cần app-level policy.
- **Output:** state lỗi expected theo API, nhưng UI copy/action/retry chưa có contract; runtime chưa xác minh.
- **Ngoại lệ:** 400/422 không thuộc catalog #37; malformed path/error mapping là open question Q-07.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
