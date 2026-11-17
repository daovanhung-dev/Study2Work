# ST-04 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

### Luồng dự kiến theo AC-12

1. Student is expected to be logged in, then enters `/student/enroll/:courseId`. The route exists, but Study Web still has no Student session guard; `courseId` is passed as a path string.
2. Sau khi có `course_id:int64` hợp lệ, gọi API #08 để đọc course công khai đã `PUBLISHED`. #08 không yêu cầu Bearer theo catalog.
3. Nếu #08 trả thành công, lấy `data.items[0]`. Response singleton vẫn có `pagination`; category không được trả. `price` là decimal string; không tự đổi thành tiền hiển thị nếu chưa có currency/format rule.
4. Do not call #15 yet. Current Study Server source resolves a valid Student Bearer token but silently falls back to any enrollment when the token is absent or invalid, which conflicts with the Public contract and Student-specific decision.
5. Khi backend xác định nhánh: enrollment đã tồn tại → điều hướng nhánh Khóa học của tôi; chưa có enrollment và rule miễn phí được xác nhận → POST #19; nhánh trả phí → ST-05 tạo Order qua #16, tiếp ST-06 tạo payment qua #17.
6. Kết quả giao dịch cần được xác minh bởi server. AC-12 có node #18 operation-status nhưng node này không nối trong diagram; chưa thể chốt thứ tự/gating #18 so với #19.
7. Only after server-side entitlement/payment confirmation may #19 create enrollment and #20 reload My Courses (ST-08). Study Server now has routes for #19/#20, but their current runtime responses and the approved flow are not yet established by ST-04.
8. Với lỗi #08/#15, trạng thái hiển thị và điều hướng lỗi phải theo contract sau khi được chốt. Copy lỗi đang có trong HTML là nội dung tĩnh, không được ánh xạ thành lỗi API. Không có retry, timeout, cache, chống gửi trùng ở client hoặc chính sách phiên hết hạn hiện hành.

### Hành vi hiện tại

1. Study Web reads `courseId` from the route and calls #08 through the existing Guest course-detail service.
2. A published-course response leads to the enrollment gate; #08 404 maps to not-found; other errors map to a generic error. The page never calls #15 or infers enrollment state.
3. Người dùng chỉ có các anchor trong shell/breadcrumb/footer và CTA quay lại `/courses`. Điều hướng client-side, giữ lại filter/course context, và route đích trong runtime chưa được xác minh.
4. Study Server has current #15 source, but its unauthenticated/invalid-token fallback can return another user's enrollment. The client does not call it. Session-expiry behavior, identity selection and enrollment outcomes remain unverified.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

| State | Điều kiện vào / nguồn | Hành vi và state kế tiếp | Tình trạng |
|---|---|---|---|
| `course-loading` | Route invokes #08 | Loading status while public course detail is requested | Current FE source |
| `prototype-static-error` | Mở trực tiếp `code.html` | Luôn hiện #9/#10 và CTA #11; không gọi API | Current HTML only |
| `route-input-pending` | `/student/enroll/:courseId` receives `courseId` | Raw string is passed to #08; Student guard is still missing | Current FE source |
| `course-unavailable` | #08 returns 404 | Course does not exist, ID is invalid, or it is not `PUBLISHED`; show not-found state | Current FE source |
| `course-error` | #08 returns another HTTP/envelope error | Show generic course-load error | Current FE source |
| `enrollment-check-blocked` | #08 succeeds but #15 identity contract is unsafe/unresolved | Do not call #15 or branch; show enrollment gate | Current FE source |
| `already-enrolled` | Backend xác định đúng enrollment thuộc Student | Nhánh Khóa học của tôi/ST-08 theo AC-12; payload/navigation chưa chốt | Expected only |
| `free-enrollment` | Server confirms no enrollment and free/eligible | #19; then #20 and ST-08 | Expected only; APIs #19/#20 routes exist but flow/contracts are not approved |
| `paid-checkout` | Server xác nhận nhánh trả phí | ST-05/#16 → ST-06/#17; payment proof server-side | Expected only; routes #16–#18 exist but the flow remains gated |
| `session-expired-or-forbidden` | AC-12 Student precondition không còn hợp lệ | Redirect/401/403 destination và return path cần contract | Unspecified; #08/#15 hiện public trong catalog |
| `back-to-courses` | Click #11 | `/courses`; không giữ query/context | Prototype link only |

### Ma trận điều hướng và dữ liệu

| Từ | Điều kiện | Đến | Dữ liệu chuyển |
|---|---|---|---|
| GS-03 | Người dùng chọn ghi danh; AC-12 precondition | ST-04 (route đề xuất) | `courseId` candidate; slug/numeric mapping chưa chốt |
| ST-04 | Enrollment đã được resolve đúng và đã tồn tại | Khóa học của tôi / ST-08 | Enrollment/course identity; schema route payload chưa có |
| ST-04 | Rule free/eligible được backend xác nhận | ST-07 hoặc flow result theo AC-12 | `course_id`; #19/#20 runtime absent |
| ST-04 | Rule paid được backend xác nhận | ST-05 | `course_id`; order/payment contract chưa hoàn tất |
| ST-04 | Click #11 | `/courses` | Không truyền dữ liệu |
| Header/footer | Click static anchor | Path ghi trong HTML | Không truyền course/auth/filter state |

AC-12 đặt các nhánh trước payment và sau payment trong cùng flow, nhưng chi tiết route handoff của ST-05–ST-08 và vai trò chính xác của #18 chưa được phê duyệt. Không coi bảng route là runtime.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #8 trước; #15 chỉ gọi khi BE chốt identity/selection; nếu miễn phí → #19, nếu trả phí → #16.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [ST-04](../../screen_stitch/03_student/ST-04_kiem-tra-ghi-danh-truoc-dang-ky/ST-04.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
