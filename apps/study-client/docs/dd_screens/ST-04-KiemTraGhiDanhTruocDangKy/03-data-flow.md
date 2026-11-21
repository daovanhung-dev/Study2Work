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

1. Student vào `/student/enroll/:courseId`. Route hiện có; Student session được kiểm tra khi gọi protected API, nhưng route guard và return-after-login chưa có.
2. Gọi API #08 bằng public `course_id` để xác nhận course `PUBLISHED`; giữ route input dạng chuỗi và yêu cầu ID là số nguyên an toàn trước khi chuyển sang body #19.
3. Gọi #15 qua `StudentApiService` với Bearer. API #15 source chỉ trả enrollment của JWT Student; catalog vẫn ghi Public/no-Bearer nên đó là contract discrepancy.
4. Enrollment `ACTIVE` mở ST-08. Khi không có row (#15 404), price `0` cho phép CTA ghi danh miễn phí; price dương chuyển ST-05/#16. Giá không hợp lệ dừng.
5. Chỉ thao tác bấm CTA miễn phí mới gọi #19. Sau success, #20 phải xác nhận course trong danh sách trước khi mở ST-08. Conflict #19 được kiểm tra lại bằng #20, không tự gửi lại mutation.
6. Với paid branch, ST-05/#16 tạo Order, ST-06/#17 khởi tạo VNPay; chỉ provider result đã được backend xác minh mới có thể xác lập payment/entitlement. ST-07/#18/#19 tiếp tục theo server operation outcome.
7. Nếu #19 thành công nhưng #20 lỗi, giữ riêng trạng thái refresh và chỉ retry #20. Không biến browser return, route, hoặc giá thành bằng chứng enrollment/payment.

### Hành vi hiện tại

1. Study Web đọc `courseId`, gọi #08, sau đó gọi Student-authenticated #15.
2. #08 404 → not-found; các envelope/network errors khác → error. #15 `ACTIVE` → already-enrolled; 404 sau khi #08 thành công → free/paid branch theo price; 401/403/session missing → login-required.
3. Free CTA gọi #19 một lần; #20 xác nhận course trước khi mở `/student/courses`. Nếu #20 lỗi, thao tác retry chỉ gọi #20. Paid course handoff sang ST-05.
4. API #15 backend đã xóa fallback theo toàn course; test source hiện còn kỳ vọng anonymous behavior và gate-only FE, nên test evidence stale. Không có test/browser/live DB verification trong task.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

| State | Điều kiện vào / nguồn | Hành vi và state kế tiếp | Tình trạng |
|---|---|---|---|
| `course-loading` | Route invokes #08 | Loading status while public course detail is requested | Current FE source |
| `prototype-static-error` | Mở trực tiếp `code.html` | Luôn hiện #9/#10 và CTA #11; không gọi API | Current HTML only |
| `route-input-pending` | `/student/enroll/:courseId` receives `courseId` | Raw string is passed to #08; Student guard is still missing | Current FE source |
| `course-unavailable` | #08 returns 404 | Course does not exist, ID is invalid, or it is not `PUBLISHED`; show not-found state | Current FE source |
| `course-error` | #08 returns another HTTP/envelope error | Show generic course-load error | Current FE source |
| `enrollment-check` | #08 succeeds and #15 uses Student Bearer | ACTIVE → already-enrolled; 404 → price branch; 401/403 → login-required | Current FE source; Public catalog discrepancy remains |
| `already-enrolled` | #15 returns current Student row with status ACTIVE | Open `/student/courses` | Current FE source |
| `free-enrollment` | #15 404 and #08 price is zero | Explicit #19, verify via #20, then open ST-08 | Current FE source; database runtime unverified |
| `paid-checkout` | #15 404 and #08 price is positive | Link to ST-05; provider success remains server-verified downstream | Current FE handoff; ST-05/#16–#18 pending |
| `session-expired-or-forbidden` | Student protected API reports LOGIN_REQUIRED/401/403 | Show login-required and link to `/login`; no return path preserved | Current FE; route guard/return path absent |
| `back-to-courses` | Click #11 | `/courses`; không giữ query/context | Prototype link only |

### Ma trận điều hướng và dữ liệu

| Từ | Điều kiện | Đến | Dữ liệu chuyển |
|---|---|---|---|
| GS-03 | Người dùng chọn ghi danh; AC-12 precondition | ST-04 (route đề xuất) | `courseId` candidate; slug/numeric mapping chưa chốt |
| ST-04 | #15 returns current Student ACTIVE row | `/student/courses` / ST-08 | Course ID stays in the fetched #20 list; no client entitlement token |
| ST-04 | #15 404 and #08 price is zero | #19 → #20 → ST-08 | Path/body `course_id`; #20 page 1 must contain course ID |
| ST-04 | #15 404 and #08 price is positive | ST-05 | `courseId` route segment |
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
