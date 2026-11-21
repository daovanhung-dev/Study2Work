# ME-10 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ME-10-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Đọc bài làm + file, form điểm, rubric, nhận xét; tách 2 thao tác nếu API tách.
- Gate/status (giữ nguyên): **D**; **BLOCK:** Rubric fields, score type, atomicity chưa khóa
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Bảo mật, thích ứng, tiếp cận và nghiệm thu

### F.1. Bảo mật và riêng tư

- Treat submission content, file URLs, `user_id`, score and feedback as student data. Backend role/access checks remain authoritative; never infer permission from sample Mentor label.
- API source guard requires MENTOR role; direct owner is DERIVED and assigned Mentor scope is unresolved. Do not bypass 403 or expose existence/content through local cached data.
- Do not put token, content, feedback or file URL in logs, browser query strings or error messages. Use `traceId` for support correlation.
- Current “AES-256”, “PENDING_AUTH”, scan and signed-confirmation strings are not security evidence. Confirm storage/transport scanning and release rules before product claims.
- #57 attachments are not stored; do not tell the user they were uploaded. Do not conflate student-submitted file `files[]` with Mentor feedback attachments.

### F.2. Responsive và accessibility

- Treat `.agents/web-study/design.md` as intended target, not implemented evidence: keyboard operability, visible focus, reduced-motion support, semantic labels and target hit-area conventions must be checked in the eventual Study Web source.
- Current HTML associates labels with score/comment controls; score is disabled and has `aria-describedby`; text counter has no `aria-live`; textarea has no `maxlength`; anchors point to `#`. Verify screen reader announcement, validation/error focus, keyboard navigation, zoom/reflow, contrast and accessible status announcements when UI is implemented.
- The mockup is a fixed desktop 2-column layout at 1600×1556. Mobile/tablet stacking, long filenames/content, textarea growth, error banners and 200% zoom are not specified by the asset; implement responsively under the approved Study Web design and add screenshots/verification before claiming support.
- The visible WCAG 2.1 AA claim is not proof of conformance. Use meaningful text for loading/saved/error states, announce independent grade/feedback results, and preserve focus after submission as part of implementation review.

### F.3. Quyết định còn mở

| ID | Cần xác nhận | Nguồn chi tiết |
|---|---|---|
| Q-ME10-01 | Rubric source, response field/schema, relation to Assignment, item IDs/order/score, persistence target | [#55 questions](../../../../study-server/docs/dd/55_mentor_submissions_detail/OPEN_QUESTIONS.md), [#56 questions](../../../../study-server/docs/dd/56_mentor_submissions_grade/OPEN_QUESTIONS.md) |
| Q-ME10-02 | Score scale, integer/decimal/precision, `max_score` source, range, zero/empty meaning | #56 Q-56-03; #55 Q-55-06 |
| Q-ME10-03 | Whether `rubric_items` must persist; schema/transaction/history | #56 Q-56-01/02 |
| Q-ME10-04 | Feedback request wire keys, length/empty rules, attachment encoding/storage/response | [#57 questions](../../../../study-server/docs/dd/57_mentor_submissions_feedback/OPEN_QUESTIONS.md) |
| Q-ME10-05 | Combined visual button vs separate actions; order; independent success; retry/idempotency/audit | F09, #56 Q-56-05/07, #57 Q-57-03/06 |
| Q-ME10-06 | Grade eligibility/regrade and status lifecycle; when Student may see score/feedback | #55 Q-55-06, #56 Q-56-05/07, #57 Q-57-06 |
| Q-ME10-07 | Mentor numeric JWT claim, direct owner vs assigned Mentor, 403 vs 404, orphan rows | #55 Q-55-04/05; #56 Q-56-04; #57 Q-57-05 |
| Q-ME10-08 | API #35 file reference producer vs API #34 metadata URL and file privacy/status behavior | #55 Q-55-02/09; Study DB context |
| Q-ME10-09 | Live schema, migration deployment, nullable FK and legacy/V1-PILOT rubric model boundary | [Study Server DB context](../../../../../.agents/server-study/database.md), checked-in [candidate DDL](../../../../../infra/postgres/study-server/DB.sql) |
| Q-ME10-10 | Study Web auth/session/router/client cache, ME-09 return-state policy and navigation destinations | [Study Web context](../../../../../.agents/web-work/study/AGENTS.md) |
| Q-ME10-11 | #56/#57 precedence between Pydantic body-validation 422 and view-level auth 401/403 for missing, malformed, or extra body fields | [API route signatures](../../../../study-server/app/api/v1.py), [validation exception handler](../../../../study-server/app/core/middleware.py), API catalog #56/#57 |

### F.4. Acceptance checklist

- [x] Plan precedes marker map, annotated image and DD.
- [x] Original `screen.png` and `code.html` preserved; source hashes recorded in plan/worklog.
- [x] Every visible design element has a sequential marker and matching DD row (`#1–#39`).
- [x] API #55–#57 route → guard/view → query/mutation → response/error/transaction are distinguished from expected AC-23.
- [x] #56/#57 body-validation-before-view-auth behavior is source-traced and its precedence remains an explicit API contract question.
- [x] #56 grade and #57 feedback are separate, independently saved operations; partial success and revalidation are documented.
- [x] Rubric, score, feedback attachments, access and live schema gaps are explicit; no invented fields or behavior are represented as verified.
- [x] States, navigation, session/access, privacy and accessibility requirements are documented.
- [x] Relative links and marker bounds/uniqueness/1:1 mapping are statically checked; annotated image was visually inspected and marker positions adjusted to avoid important text.
- [x] `DD READY` is separate from `IMPLEMENTATION BLOCKED` and `RUNTIME NOT VERIFIED`.
- [ ] Product/API/schema owners close listed decisions before implementation.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
