# ST-16 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-16-EV-001` | `ST16-EV-01` / ST16-EV-01 — Mở route và yêu cầu kết quả | See source event detail below |
| `ST-16-EV-002` | `ST16-EV-02` / ST16-EV-02 — Map grading status and permitted score | See source event detail below |
| `ST-16-EV-003` | `ST16-EV-03` / ST16-EV-03 — Lọc và xem lại đáp án | See source event detail below |
| `ST-16-EV-004` | `ST16-EV-04` / ST16-EV-04 — PDF, course outline and next-lesson controls | See source event detail below |
| `ST-16-EV-005` | `ST16-EV-05` / ST16-EV-05 — Authentication, access, error and unavailable response | See source event detail below |
| `ST-16-EV-006` | `ST16-EV-06` / ST16-EV-06 — Global navigation and accessible interaction | See source event detail below |
| `ST-16-EV-007` | `Source heading` / D.1. API response and state mapping | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

### ST16-EV-01 — Mở route và yêu cầu kết quả

- **Element/loại:** route load; no visible marker trigger.
- **Điều kiện:** Student context; `attemptId` from ST-15 route handoff. ST-15 should navigate after #31 accepted; direct-entry/refresh availability is still an API #32 question.
- **Input:** `attemptId:int64` path value; Bearer Student token from auth boundary. No query/body/user ID.
- **Xử lý:** (1) read and normalize the path value according to approved route parsing; (2) do not send a user ID or sample attempt ID; (3) require Student auth context; (4) GET #32 once on route load; (5) parse envelope only against approved schema; (6) bind approved fields and transition to `pending` or `graded`; (7) do not call #28/#27/#37 or derive pass/skills.
- **API:** #32 `GET /api/v1/attempts/{attempt_id}/result`; Authorization Bearer; no query/body; response `ApiEnvelope<QuizAttempt>`. Catalog errors: 401/403/404/500.
- **Output/exception:** loading → pending/graded only from supported status; otherwise unsupported/unavailable/error. No route/module/test exists to implement or verify this flow today.

### ST16-EV-02 — Map grading status and permitted score

- **Element/loại:** response mapping for #7, #10–#14.
- **Điều kiện:** #32 returns HTTP 200 `DESIGN_RESOURCE_RETRIEVED` with data matching the approved `QuizAttempt` schema.
- **Input:** candidate `status`, optional `submitted_at`, optional `score`, other response fields only if approved.
- **Xử lý:** (1) branch `PENDING_GRADE` → show pending status; omit score unless a policy explicitly allows a partial score; never fill `0`; (2) branch `GRADED` → display only supplied and permitted score fields; (3) do not equate GRADED with PASSED; passing threshold and `Quiz` data are not in ST-16/#32 contract; (4) do not compute percentage, GPA, duration, attempt ordinal or unlock from static values; (5) for unknown status, show unsupported/unavailable state and do not expose raw response details in user-facing copy or logs.
- **API:** no additional request. #32 DD leaves pending score `omit/null/partial` unresolved; AC-16 only names the two branches.
- **Output/exception:** render only permitted server-supplied fields. Missing optional score is not zero; malformed/incompatible envelope goes to error, not a fabricated result.

### ST16-EV-03 — Lọc và xem lại đáp án

- **Element/loại:** #20–#32; Click/tap/keyboard in screenshot.
- **Điều kiện:** only after API owner approves answer projection, question content/order and student disclosure.
- **Input:** `answers[]` may contain `question_id`, `choice_ids?`, `text_answer?`, `correct?`, `score?`; each detail remains optional and mapping open. Screenshot counts/questions are not input.
- **Xử lý:** (1) do not read answer key from quiz choices; (2) do not call #28 to fetch questions without approved ST-16 orchestration; (3) do not derive filter counts or reorder answers before order contract; (4) once approved, local filters may use only approved per-answer correctness/IDs and must preserve server order; (5) never show answer, correction or feedback while policy withholds it; (6) feedback currently has no response field/source.
- **API:** #32 only per inventory. No extra API currently authorized by ST-16 contract.
- **Output/exception:** current implementation state is design-only/disabled until response and disclosure contracts are approved. Empty answers vs missing collection semantics need owner decision.

### ST16-EV-04 — PDF, course outline and next-lesson controls

- **Element/loại:** #33–#36; Click/tap/keyboard activation.
- **Điều kiện:** destination, file source, entitlement/progress rule and screen handoff explicitly approved.
- **Input:** currently only attempt/result context; no PDF reference, course/module/lesson ID or next-item contract is in #32 response/route inventory.
- **Xử lý:** (1) do not synthesize PDF or certificate; (2) do not infer “Xem lại đề cương” route from the copy, though ST-09 is a related inventory screen; (3) do not call progress/next APIs or set completion; (4) do not navigate to a named next lesson from mockup text; (5) keep controls unimplemented/disabled/omitted according to product decision until destinations and data source are defined.
- **API:** no PDF, course-outline, next-lesson or progress API in the ST-16 API list.
- **Output/exception:** all four actions are design-only. No route, file or DB side effect is verified.

### ST16-EV-05 — Authentication, access, error and unavailable response

- **Element/loại:** route/API response; error/unavailable state.
- **Điều kiện:** GET #32 returns non-success or an unsupported result state.
- **Input:** HTTP/business code and `attemptId`; no user-supplied owner ID.
- **Xử lý:** (1) 401 → authentication-required state; exact reauth destination not defined; (2) 403 → access-denied state; owner mismatch might instead be masked as 404; (3) 404 → result/attempt unavailable/not found per catalog, without revealing another user's existence; (4) 500 → safe internal-error state without SQL/stack trace; (5) path parse failure must not be mapped to unlisted 400/422 by this DD; (6) no retry/reconciliation behavior is defined; do not reuse prior screenshot data as stale success.
- **API:** only 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`. No 409 or 422.
- **Output/exception:** no successful result is shown unless response has approved success envelope. Exact user copy and retry control remain open.

### ST16-EV-06 — Global navigation and accessible interaction

- **Element/loại:** #2–#6, #34–#38 and keyboard/focus behaviors.
- **Điều kiện:** UI implementation exists and destinations are approved.
- **Input:** user interaction only; current HTML links are prototype markup, not route evidence.
- **Xử lý:** (1) do not infer search/profile/notification/footer destination from assets; (2) use semantic anchors/buttons and visible labels; (3) preserve keyboard/focus order and state announcements; (4) do not rely on color-only “passed/correct/incorrect” state; (5) support reduced-motion and responsive reflow per Study Web design target; (6) do not claim this behavior exists in current runtime.
- **API:** none.
- **Output/exception:** accessibility behavior is an implementation target; route/accessibility tests were not run.

### D.1. API response and state mapping

| Response | State target | UI/data rule |
|---|---|---|
| 200 `DESIGN_RESOURCE_RETRIEVED`, `status=PENDING_GRADE` | `pending` | Show “Đang chờ chấm” from approved status; no score zero; pending score/correctness remain subject to Q-32-02/03. |
| 200 `DESIGN_RESOURCE_RETRIEVED`, `status=GRADED` | `graded` | Render only approved response fields; not automatically PASSED; no answer key without policy. |
| 200 with other/missing status | `unsupported_status` | Do not invent mapping. |
| 401 `DESIGN_AUTHENTICATION_REQUIRED` | `error`/authentication-required | No reauth route is defined in ST-16 contract. |
| 403 `DESIGN_ACCESS_DENIED` | `access_denied` | Owner behavior remains Q-32-01. |
| 404 `DESIGN_RESOURCE_NOT_FOUND` | `unavailable`/`not_found` | Do not expose ownership/existence beyond approved message. |
| 500 `DESIGN_INTERNAL_ERROR` | `error` | Safe copy only; no internal details. |
| Timeout/network failure or malformed envelope | `error`/`unavailable` | No result claim, retry or stale sample fallback is defined. |

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
