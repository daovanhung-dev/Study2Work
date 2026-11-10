# ST-09 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-09-EV-001` | `ST09-EV-01` / ST09-EV-01 — Mở route và khởi tạo course context | See source event detail below |
| `ST-09-EV-002` | `ST09-EV-02` / ST09-EV-02 — Xác nhận course membership/enrollment | See source event detail below |
| `ST-09-EV-003` | `ST09-EV-03` / ST09-EV-03 — Nạp aggregate progress | See source event detail below |
| `ST-09-EV-004` | `ST09-EV-04` / ST09-EV-04 — Nạp curriculum public qua API #09 | See source event detail below |
| `ST-09-EV-005` | `ST09-EV-05` / ST09-EV-05 — Quay lại ST-08 | See source event detail below |
| `ST-09-EV-006` | `ST09-EV-06` / ST09-EV-06 — CTA sang ST-10 để kiểm tra quyền học bài | See source event detail below |
| `ST-09-EV-007` | `ST09-EV-07` / ST09-EV-07 — Header navigation | See source event detail below |
| `ST-09-EV-008` | `ST09-EV-08` / ST09-EV-08 — Footer navigation và legal/help links | See source event detail below |
| `ST-09-EV-009` | `ST09-EV-09` / ST09-EV-09 — Sao chép route | See source event detail below |
| `ST-09-EV-010` | `ST09-EV-10` / ST09-EV-10 — Mở chi tiết tiến độ ST-21 | See source event detail below |
| `ST-09-EV-011` | `Source heading` / Sự kiện không phát sinh trong asset | See source event detail below |
| `ST-09-EV-012` | `Source heading` / D.1 API và bảo mật | See source event detail below |
| `ST-09-EV-013` | `Source heading` / Quy tắc bảo mật | See source event detail below |
| `ST-09-EV-014` | `Source heading` / Business rules và open decisions | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết từng sự kiện

> Với các sự kiện chưa có source hoặc contract, các bước dưới đây mô tả điều kiện và blocker. Chúng không phải logic đã chạy và không đưa ra retry/cache/redirect policy.

### ST09-EV-01 — Mở route và khởi tạo course context

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Page route entry / Load. |
| Element | Page-level; route dự kiến /student/courses/:courseId; không có control. |
| Input | URL path với courseId dự kiến int64; session/token/role từ auth context nếu có. ST-08 selection payload không được source/asset xác nhận. |
| Điều kiện | Student session theo AC-13; route guard, token store và path parser hiện UNWIRED. |
| Quy trình | 1) Nhận URL. 2) Parse courseId theo contract sẽ được duyệt; hiện chưa có quy tắc invalid/zero/negative/overflow. 3) Kiểm tra Student session theo auth design; source client vắng mặt. 4) Không gọi #09 trực tiếp trước membership/access decision. 5) Hiển thị gated/error/loading state chỉ sau khi state taxonomy được duyệt; hiện ảnh chỉ là static gated mockup. |
| API / output | Không có API source-backed cho bước auth. Không định nghĩa redirect, cache, timeout hoặc retry. Expected output là course context đã được xác nhận hoặc một lỗi có mapping rõ; hiện chưa thể triển khai. |

### ST09-EV-02 — Xác nhận course membership/enrollment

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Sau khi route/session hợp lệ; Load/API. |
| Element | Page-level; card #14 chỉ là explanatory copy, không trigger. |
| Input | Bearer JWT theo catalog; courseId từ route. API catalog #20 là GET /api/v1/users/me/courses với query status? string và page? int32; không path/body. |
| API khai báo | API #20, role Student; response ApiEnvelope<UserProfile>; catalog codes: 200 DESIGN_RESOURCE_RETRIEVED, 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 422 DESIGN_VALIDATION_ERROR, 500 DESIGN_INTERNAL_ERROR. Query status enum/default/paging semantics chưa rõ. |
| Quy trình | 1) Không gửi user_id riêng theo /me endpoint. 2) Gọi #20 chỉ khi JWT/role contract sẵn sàng. 3) Validate HTTP/business result theo schema được duyệt. 4) Hiện response type không có course collection/membership contract và API #20 không có route/module/query/test source, nên không thể match courseId hoặc phân loại enrolled/not-enrolled. 5) Không cho render nội dung riêng tư từ #09 chỉ vì GET thành công. |
| Output/ngoại lệ | 401/403/422/500 được liệt kê trong catalog nhưng payload và screen mapping chưa có. Không giả định 404 cho nonmember, redirect, retry hay empty list semantics. Current status: NOT_FOUND; event expected only. |

### ST09-EV-03 — Nạp aggregate progress

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Sau membership gate thành công; Load/API. |
| Element | Page-level; không có progress element trong asset. |
| Input | courseId int64 từ path; Bearer JWT; không query/body theo catalog. |
| API khai báo | API #37 GET /api/v1/users/me/progress/{course_id}, Student. Response ApiEnvelope<UserProfile>; catalog codes 200, 401, 403, 404, 500 với DESIGN_* labels. |
| Quy trình | 1) Chỉ bắt đầu sau khi membership decision và request ordering được xác nhận. 2) Gọi #37 với courseId. 3) Validate response khi schema được định nghĩa. 4) AC-18 yêu cầu aggregate lesson + quiz + assignment progress nhưng formula/fields chưa được định nghĩa. 5) Không tự tính percent, denominator, completion, rounding, attempt/submission selection hoặc default 0. 6) Không cập nhật UI cho đến khi response shape và partial/error semantics được duyệt. |
| Output/ngoại lệ | #37 Draft; không có route/module/query/test source. 401/403/404/500 mapping, zero activity, partial data, stale response, cache/retry chưa được chốt. |

### ST09-EV-04 — Nạp curriculum public qua API #09

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Expected load after course membership/access design permits outline; Load/API. |
| Element | Page-level; course/lesson list chưa có marker vì không hiện trong design. |
| Request | GET /api/v1/courses/{course_id}/curriculum; path course_id int64; không query/body/auth theo catalog. |
| Current response | `ApiEnvelope<Page<Lesson>>`. Success envelope fields from `success_response`: `success=true`, `businessCode`, `message`, `data={items,pagination}`, `meta={}`, `traceId`; lesson fields are `id`, `course_id`, `title`, nullable `content`, nullable `video_url`, `order`, `status`. Error helper returns `success=false`, `businessCode`, `message`, `data=null`, `meta={}`, `traceId` and `X-Trace-Id`. The API #09 Draft examples show error `data={}`, which differs from the current helper's `null`. |
| Current behavior | Invalid non-integer path/course missing/unpublished → 404 DESIGN_RESOURCE_NOT_FOUND. Published course with no published lessons → 200, empty page (`page=1`, `size=0`, `total=0`, `total_pages=0`) and message “No published lessons.” Success → 200 DESIGN_RESOURCE_RETRIEVED; the message is “Curriculum retrieved.” when non-empty. SQL/mapping failure → 500 DESIGN_INTERNAL_ERROR; SQL exception path rolls back. Current query checks course PUBLISHED and lists lessons PUBLISHED ordered `sort_order ASC`, `id ASC`. The declared path type is int64, but the source validator only parses an integer and does not explicitly enforce signed-int64 bounds; the out-of-range response is not defined by this source and is not runtime-verified. Test source exists; not run. No authentication/enrollment/access check found. |
| Quy trình / giới hạn | 1) Do not treat #09 success as membership proof. 2) Do not use public content/video_url as private media entitlement. 3) Do not mark a lesson accessible based on PUBLISHED status alone. 4) Backend projection and Student-only access contract must be resolved before using this data to render protected learning content. |
| Retry/cache/output | No retries/cache policy specified by source/catalog; do not invent. Current API is source-backed, but its public projection creates a security/design blocker for a protected Student learning tree. |

### ST09-EV-05 — Quay lại ST-08

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Click #11; navigation. |
| Input | Current HTML href=#; data-path=/student/courses. It does not carry filter, page, scroll or enrollment result. |
| Current processing | Static anchor only; no router. Browser behavior of # may update fragment/current position; app navigation is not wired. |
| Expected result | ST-08 route from inventory. Return-state restoration and auth guard require client route/state design; no API call is specified for this click. |
| Failure cases | No destination route in current Study Web source. Do not claim preserved selection or browser-history semantics. |

### ST09-EV-06 — CTA sang ST-10 để kiểm tra quyền học bài

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Click #12; expected navigation/access handoff. |
| Input | HTML provides no lessonId, selected lesson or access token. Inventory route ST-10 expects /student/lessons/:lessonId/start. |
| Required contract | APIs #22 access, #23 start, #24 lesson content have no current Study Server route/module/test source. Route/API sequence, method, schemas, authorization policy and error mapping are unresolved. |
| Quy trình | 1) Cannot normalize a lesson ID because no selected lesson is present. 2) Cannot run access check with #22. 3) Cannot start or load lesson via #23/#24. 4) Keep CTA as non-operational static prototype; do not navigate with placeholder or invent a lesson. |
| Kết quả | Expected destination ST-10 only after a lesson row/selection and access contracts are available. No current success/error output exists. |

### ST09-EV-07 — Header navigation

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Click brand or navigation item #1/#2. |
| Input | Static data-path hints indicate /student, /student/courses, /student/progress, /student/discussions, /student/notifications; actual href values are #. |
| Xử lý | No API call in HTML. No Study Web router exists in editable source inventory. Route role guards and active-page behavior are unverified. |
| Kết quả | Destinations are inventory hints for ST-01/ST-08/ST-20/ST-23/ST-26. Do not claim navigation works or that auth context is retained. |

### ST09-EV-08 — Footer navigation và legal/help links

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Click footer group #20. |
| Input | Static data-path/slugs for app sections and terms/privacy/help; anchors use href=#. |
| Xử lý | No API. No route contract was found for legal/help slugs. |
| Kết quả | App section targets match inventory labels where available; actual routing, external URL and tab behavior are unresolved. |

### ST09-EV-09 — Sao chép route

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Click #18; clipboard action. |
| Input | Literal string /student/courses/:courseId from inline handler; not the current concrete URL or path parameter. |
| Current processing | HTML invokes navigator.clipboard.writeText with that literal. There is no success feedback, failure catch, permission check, or fallback in the markup. |
| Output | On supported/authorized clipboard implementations, the literal template may be copied; browser rejection behavior is unhandled in this mockup. This action does not load or navigate to a course. |
| Design decision | Keep as developer convenience only. If retained, decide whether copying template or concrete route is intended and provide observable success/failure behavior; no assumption is made here. |

### ST09-EV-10 — Mở chi tiết tiến độ ST-21

| Trường | Đặc tả |
|---|---|
| Trigger / loại | Expected navigation from progress summary; no control in PNG/HTML. |
| Input | courseId from route, if a progress control is later designed. |
| Inventory target | ST-21 route /student/progress/:courseId; API #37; linked from ST-09 inventory. |
| Xử lý / blocker | No ST-21 link/card/CTA appears in source asset and no current route exists. #37 is not source-backed and its response/formula remains open. No API call or navigation can be specified for this event yet. |
| Output | Mark as missing expected design. Add a visible trigger and approve courseId handoff before treating ST-21 as reachable. |

### Sự kiện không phát sinh trong asset

Không có form submit, search/filter, lesson selection, scrolling-triggered request, retry button, modal, tab change hoặc direct progress action. Chúng chỉ được ghi nhận như thiếu hụt so với expected inventory; không tạo event/control giả định.

### D.1 API và bảo mật

| API | Contract được khai báo | Current source | Dùng trong ST-09 |
|---|---|---|---|
| #09 | Public GET curriculum; course_id int64; response ApiEnvelope<Page<Lesson>>; 200/404/500. | SOURCE_BACKED_LOCAL: registered route/view/validator/query/model/test source; reverse API index corrected to R. API DD is still Draft. | Chỉ public outline projection; không chứng minh enrollment hoặc quyền phát nội dung/media. |
| #20 | Student GET /users/me/courses; optional status/page; Bearer JWT; response ApiEnvelope<UserProfile>; 200/401/403/422/500. | NOT_FOUND route/module/query/test. | Intended enrollment gate nhưng response schema không mô tả course membership. |
| #37 | Student GET /users/me/progress/{course_id}; Bearer JWT; response ApiEnvelope<UserProfile>; 200/401/403/404/500. | NOT_FOUND route/module/query/test; API DD Draft. | Intended aggregate progress; formula, payload, empty/error semantics chưa quyết định. |
| #22–#24 | Inventory uses lesson access/start/content flow. | NOT_FOUND route/module/test in current source. | Required before protected lesson access. |

### Quy tắc bảo mật

- Membership, course publication và lesson publication là các điều kiện khác nhau. Không thay authorization bằng trạng thái PUBLISHED.
- Current #09 public route does not check JWT/enrollment and returns lesson content/video_url. Student screen không được coi response này là permission grant; cần xác nhận backend projection/access policy với owner.
- API #09 contract declares signed int64 `course_id`, but its current validator has no explicit signed-int64 range check. Do not specify an out-of-range client response until the contract/source is aligned.
- #20/#37 path /me hàm ý identity từ auth, nhưng mapping claims → Student, ownership và revoked/expired session policy chưa có current contract.
- Không lưu hoặc đưa user/course entitlement vào URL ngoài courseId đã có trong route inventory. Không tự tạo access token/cache key.
- Không render dữ liệu riêng tư, video URL hoặc progress cho nonmember. UI gating đơn thuần không thay thế backend authorization.
- Error code/status body của #20/#37 chưa được xác minh ở runtime; không map 401/403/404 thành enrollment states khi contract chưa chốt.

### Business rules và open decisions

1. Membership source/status field, response collection shape và pagination của #20.
2. #37 numerator/denominator, lesson/quiz/assignment weights, completed semantics, rounding, selected attempt/submission, empty-course output và partial data.
3. #09 public vs authenticated projection; có được phép trả content/video_url công khai hay cần response/access split.
4. #22/#23/#24 ownership/access policy, request ordering, lesson access denial và media delivery.
5. Có thể gọi #09/#37 tuần tự hay song song sau gate; partial failure/reload/cache/stale response.
6. Loading, enrolled, not-enrolled, no-lessons, progress partial/error, course unavailable, session expired và retry UI.
7. CTA chọn lesson, ST-10 handoff và ST-21 progress-detail control.
8. Route guard/redirect/history semantics; concrete route generation từ ST-08.
9. Static mockup API badges/design tokens/accessibility claims cần sửa để phản ánh source và Study UI guide.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
