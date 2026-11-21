# ST-19 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-19-EV-001` | `ST19-EV-01` / ST19-EV-01 — Khởi tạo và tải submission | See source event detail below |
| `ST-19-EV-002` | `ST19-EV-02` / ST19-EV-02 — Ánh xạ trạng thái và receipt metadata | See source event detail below |
| `ST-19-EV-003` | `ST19-EV-03` / ST19-EV-03 — Hiển thị điểm và rubric | See source event detail below |
| `ST-19-EV-004` | `ST19-EV-04` / ST19-EV-04 — Hiển thị mentor feedback | See source event detail below |
| `ST-19-EV-005` | `ST19-EV-05` / ST19-EV-05 — Hiển thị file đã nộp | See source event detail below |
| `ST-19-EV-006` | `ST19-EV-06` / ST19-EV-06 — Mở file hoặc preview | See source event detail below |
| `ST-19-EV-007` | `ST19-EV-07` / ST19-EV-07 — Dùng breadcrumb | See source event detail below |
| `ST-19-EV-008` | `ST19-EV-08` / ST19-EV-08 — Quay lại tiến độ học tập | See source event detail below |
| `ST-19-EV-009` | `ST19-EV-09` / ST19-EV-09 — Mở line comments | See source event detail below |
| `ST-19-EV-010` | `ST19-EV-10` / ST19-EV-10 — Đặt lịch 1-on-1 | See source event detail below |
| `ST-19-EV-011` | `ST19-EV-11` / ST19-EV-11 — Điều hướng header và footer | See source event detail below |
| `ST-19-EV-012` | `ST19-EV-12` / ST19-EV-12 — Mở assignment tiếp theo | See source event detail below |
| `ST-19-EV-013` | `ST19-EV-13` / ST19-EV-13 — Hiển thị skill index và nội dung footer tĩnh | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

### ST19-EV-01 — Khởi tạo và tải submission

- **Element / event type:** Màn hình/route entry; `Load` khi mở hoặc refresh, không có marker control kích hoạt.
- **Trigger:** Route entry/refresh at `/student/submissions/:submissionId`.
- **Input:** `submissionId` from route path; Student Bearer token from auth/session layer. API #36 calls the path field `submission_id:int64!`.
- **Preconditions:** Student authenticated; route exists; ID parse policy and handoff key must be resolved. No route/current client implementation exists.
- **Processing:** (1) read path value; (2) validate only against the agreed int64 contract; do not invent positivity/error mapping; (3) send GET `/api/v1/submissions/{submission_id}` with Authorization header, no query/body; (4) await one response; retry, cache and timeout policy are unspecified; (5) accept success only for HTTP 200 and `DESIGN_RESOURCE_RETRIEVED`; (6) map `data` as Submission after schema validation is implemented; (7) render loaded state. API #36 is not currently wired.
- **Success output:** Receipt state backed by response data, with unresolved fields gated by approved projection policy.
- **Errors:** 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR`. Keep `data=null` for error envelope per API Guidelines. Exact login redirect/copy/retry UI is not defined. Network errors are client transport outcomes, not additional catalog business codes.
- **Side effects:** Read-only; no write or booking/comment mutation.

### ST19-EV-02 — Ánh xạ trạng thái và receipt metadata

- **Element / event type:** Data/UI state của màn hình; `API response handling` sau EV-01, không có marker control.
- **Trigger:** API #36 success response.
- **Precondition:** EV-01 nhận HTTP 200 với `DESIGN_RESOURCE_RETRIEVED`; response shape phải được xác thực theo contract được duyệt.
- **Input:** `id`, `assignment_id`, `user_id`, `content?`, `status`, `submitted_at`; other logical fields as contract allows.
- **Processing:** (1) map the server status without local promotion; (2) if status is `SUBMITTED`, do not display `GRADED`; (3) map submitted_at only under approved timezone/format rules; (4) show assignment/course/mentor fields only if a separate approved contract supplies them; (5) avoid inferring successful completion from screenshot text.
- **Output:** Status and receipt metadata that correspond to the approved API data only.
- **Open decisions:** full `SubmissionStatus` enum/transitions and timestamp timezone/precision/serialization.

### ST19-EV-03 — Hiển thị điểm và rubric

- **Element / event type:** EL-14–31; `API response handling / conditional render`, không phải user action.
- **Trigger:** Submission response has score/status and an approved policy permits disclosure.
- **Precondition:** API contract xác định scale/format và disclosure policy cho Student; thiếu quyết định nào thì không render phần phụ thuộc quyết định đó.
- **Input:** Optional `score?:decimal-string`; screenshot has total score and rubric breakdown but no breakdown fields are in logical schema.
- **Processing:** Do not convert decimal-string to a letter/percentage without a confirmed scale, max score and rounding rule. Do not infer rubric rows, cohort metrics or “on-chain” status. If score absent, don't show a fabricated value. If response includes it but release timing remains unresolved, this event stays blocked until owner confirms projection policy.
- **Output:** At most the confirmed score field/format; rubric visualization is design-only until a source contract exists.
- **Side effects:** None.

### ST19-EV-04 — Hiển thị mentor feedback

- **Element / event type:** EL-32–37; `API response handling / conditional render`, không phải user action.
- **Trigger:** Submission response has `feedback` and approved disclosure policy permits it.
- **Precondition:** API contract xác định Student được xem feedback và quy tắc null/omit; mentor identity/review time chỉ dùng khi có field source riêng.
- **Input:** Optional `feedback?:string`; screenshot adds mentor name, avatar, review date and biography which are absent from Submission schema.
- **Processing:** Preserve exact API text subject to approved rendering/sanitization rules; do not use mockup copy or infer grader identity. Score/feedback release timing, omit/null semantics and review timestamp are unresolved.
- **Output:** Feedback only when policy and field contract allow; otherwise loading/empty state presentation must be decided.

### ST19-EV-05 — Hiển thị file đã nộp

- **Element / event type:** EL-40–42, EL-44, EL-46; `API response handling / list render`, không phải user action.
- **Trigger:** Successful Submission response contains `files`.
- **Precondition:** `files[]` physical mapping, ordering and Student-safe projection have been approved; current candidate scalar `file_url` is insufficient.
- **Input:** `files:UploadAsset[]`; each logical asset has id, name, url, content_type, size_bytes and status per reusable schema.
- **Processing:** (1) retain array order only if API defines it; currently no sort rule; (2) render name/size/type/status only after schema confirmed; (3) do not reconstruct assets from scalar `assignment_submissions.file_url`; (4) do not assume multiple files, GitHub/Demo/report categories or thumbnail semantics; (5) expose open/download only with approved URL and access policy.
- **Output:** A file collection according to the resolved #34 association and #36 projection. Current physical mapping is blocked.

### ST19-EV-06 — Mở file hoặc preview

- **Element / event type:** EL-43, EL-45–47; `Click` hoặc keyboard activation khi action đã được duyệt.
- **Trigger:** User activates a confirmed asset link/action.
- **Precondition:** Asset is included in an approved #36 response and its URL/access/target behavior is authorized. This condition is not met by current source.
- **Input:** Asset URL and metadata from approved `UploadAsset` response; there is no confirmed #36 mapping today.
- **Processing:** No URL is created from the mockup or candidate `file_url`; access, signed/public URL, safe target and file-serving policy must be specified before enabling. Prototype `#` links are inert placeholders.
- **Output:** Only an approved secure file-open/download behavior. Current action remains design-only and disabled/unavailable until contract exists.

### ST19-EV-07 — Dùng breadcrumb

- **Element / event type:** EL-06; `Click` hoặc keyboard activation.
- **Trigger:** User activates one breadcrumb link.
- **Precondition:** Destination route and required course/assignment identifiers are known and allowed for the current Student session.
- **Input:** Submission/assignment/course context and destination route.
- **Processing:** Determine destination from approved route graph; inventory associates ST-17 and ST-20 but doesn't define full IDs/return stack. Preserve intended Student context if route contract is available; auth guard behavior is not implemented.
- **Output:** Navigation only to a known authorized route. Screenshot sample labels/IDs must not be used as route data.

### ST19-EV-08 — Quay lại tiến độ học tập

- **Element / event type:** EL-53; `Click` hoặc keyboard activation.
- **Trigger:** User clicks “Quay lại Bài giảng/tiến độ học tập (ST-20)” CTA in the mockup.
- **Precondition:** Approved ST-20 destination and required course/progress context exist; no such current Study Web route is wired.
- **Input:** Destination ST-20 and a course/progress context, if required by approved route.
- **Processing:** The exact ST-20 route is not in current frontend source; route ID and state transfer are unconfirmed. Do not fabricate a course ID from sample content.
- **Output:** Navigation can be enabled once destination/context contract is agreed; otherwise no current action is wired.

### ST19-EV-09 — Mở line comments

- **Element / event type:** EL-38; `Click` hoặc keyboard activation.
- **Trigger:** “Xem 3 Line Comments (PR)” action.
- **Precondition:** Product/API owner approves the comments source, identifier, destination and access rule; none is present in #36.
- **Input:** Mockup label/count only; #36 has no PR URL/comment count field.
- **Processing / output:** No API, route, authorization or external destination exists in this contract. Do not call a guessed service or present sample count as live. Keep action blocked/design-only.

### ST19-EV-10 — Đặt lịch 1-on-1

- **Element / event type:** EL-39; `Click` hoặc keyboard activation.
- **Trigger:** “Đặt lịch 1-on-1” action.
- **Precondition:** Booking contract supplies an authorized mentor, available time selection, destination and side-effect policy; none is present in #36.
- **Input:** No mentor ID, calendar slot, booking endpoint, consent or schedule policy is supplied by #36.
- **Processing / output:** Do not create calendar/booking side effects. This CTA needs a separate approved contract and destination; current implementation is absent.

### ST19-EV-11 — Điều hướng header và footer

- **Element / event type:** EL-01–05, EL-57; link/button `Click` hoặc keyboard activation; EL-02 input `Input/Change` chỉ khi search behavior có contract.
- **Trigger:** Brand, search, nav, notifications, profile or footer links (EL-01–05, EL-57).
- **Precondition:** A destination or action contract and Student/session behavior are defined; the current HTML anchors do not establish those routes.
- **Input:** Static prototype anchors and labels.
- **Processing / output:** These destinations are not wired in Study Web source. Notification/profile/search behavior is outside #36; do not treat HTML `#` as route contract.

### ST19-EV-12 — Mở assignment tiếp theo

- **Element / event type:** EL-54; `Click` hoặc keyboard activation.
- **Trigger:** “Xem đồ án tiếp theo (Capstone 02)” CTA.
- **Precondition:** A source provides the next assignment ID, ordering rule and Student access; API #36 supplies none of them.
- **Input:** Mockup text only; #36 does not return a next assignment identifier/order/access status.
- **Processing / output:** No path can be built without an approved next-item source and route. Keep disabled/omit pending product contract; don't infer sequential assignment IDs.

### ST19-EV-13 — Hiển thị skill index và nội dung footer tĩnh

- **Element / event type:** EL-48–50, EL-55–56, EL-58; `Page render`, không phải user action.
- **Trigger:** Loaded static page presentation.
- **Precondition:** Static footer content is approved; skill-index metrics require a separately approved source and calculation contract before display as real data.
- **Input:** Static skill-index and footer copy/icons/charts in PNG; no API fields. Footer link navigation is covered by EV-11.
- **Processing / output:** Treat noninteractive footer content as presentation pending content approval. Skill-index metric/chart has no source, aggregation or period contract; do not calculate it from submission score. No mutation/event is defined.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
