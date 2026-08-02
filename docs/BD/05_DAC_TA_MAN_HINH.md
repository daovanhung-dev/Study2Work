# 05. Đặc tả màn hình canonical V1-PILOT

## 1. Phạm vi và nguyên tắc

Tài liệu này là nguồn định nghĩa duy nhất cho sitemap, route, guard, dữ liệu hiển thị, thao tác, validation, trạng thái UX, responsive, accessibility, analytics và audit của giao diện Study2Work V1-PILOT. Tên API và business code lấy nguyên trạng từ `04_DAC_TA_API.md`; màn hình không tự suy diễn trạng thái, phần trăm, quyền, giá, match score hoặc payment result.

Frontend mục tiêu:

- Study: Vue 3, TypeScript, Vite, Tailwind, Pinia cho session/UI state, TanStack Query cho server state, Axios và Zod cho contract biên.
- Work: React, TypeScript, Vite, Tailwind, Zustand cho session/UI state, TanStack Query, React Hook Form và Zod.
- Hosted Identity dùng cùng design token và redirect allowlist của Study/Work. Access token giữ trong memory; rotating refresh token dùng cookie `HttpOnly`, `Secure`, `SameSite=Lax/Strict` phù hợp origin. Không lưu token/PII/form CV vào `localStorage`.

Mỗi screen record dưới đây kế thừa toàn bộ quy tắc chung tại mục 3. Nếu một API trả quyền/trạng thái khác UI cache, server thắng; UI invalidate query và render state mới. Không dùng nút ẩn làm hàng rào bảo mật.

## 2. Sitemap và route ownership

```text
identity.study2work.vn
├── /register, /verify-email, /login, /recover, /mfa
└── /account/security

study.study2work.vn
├── /, /paths, /paths/:slug, /courses, /courses/:slug, /samples/:lessonId
├── /learn/dashboard, /learn/onboarding, /learn/recommendations
├── /learn/primary-path, /learn/courses, /learn/courses/:courseId
├── /learn/lessons/:lessonId, /learn/assessments/:assessmentId
├── /learn/progress, /notifications, /community, /support, /profile
└── /ops/study/*

work.study2work.vn
├── /jobs, /jobs/:slug, /companies/:slug
├── /candidate/*
├── /enterprise/:enterpriseId/*
├── /university/:universityId/*
└── /ops/*
```

Route guard chạy theo thứ tự: route tồn tại → session/token → email verified/account status → MFA freshness nếu privileged → product/local projection → tenant membership → permission → resource scope. `401` đưa về login kèm signed return URL nội bộ; `403` hiển thị trang thiếu quyền, không vòng lặp redirect; account suspended/deletion pending hiển thị state chuyên biệt và khóa mutation. Tenant switch luôn reset query cache chứa tenant data, socket subscription và form draft nhạy cảm.

## 3. Mẫu màn hình và hành vi dùng chung

### 3.1 Trạng thái bắt buộc

| Trạng thái | Hành vi chuẩn |
|---|---|
| Initial loading | Skeleton giữ đúng kích thước; `aria-busy=true`; không flash empty/403; request có timeout và nút thử lại sau lỗi. |
| Background refresh | Giữ dữ liệu cũ có nhãn “đang cập nhật”; mutation liên quan bị khóa nếu version đang stale. |
| Empty | Nêu lý do và CTA hợp lệ; không dùng empty thay cho lỗi quyền hay lỗi mạng. |
| Validation | Validate khi blur/submit; lỗi gắn field bằng `aria-describedby`, focus lỗi đầu; giữ dữ liệu không bí mật. Server `meta.fieldErrors` là nguồn cuối. |
| `401` | Single-flight refresh một lần; thất bại thì xóa session memory và redirect login với return URL đã ký. |
| `403` | Trang thiếu quyền/suspended đúng business code; không tiết lộ target tenant/resource. |
| `404` | Trang không tìm thấy dùng cùng nội dung cho resource khác tenant. |
| `409` | Modal/state theo business code: cooldown hiển thị thời điểm, duplicate dẫn tới resource hiện có, terminal chuyển read-only. |
| `412` | Không tự ghi đè; hiển thị “có thay đổi mới”, cho reload/so sánh safe diff; form chỉ merge field không xung đột do người dùng xác nhận. |
| `429` | Countdown theo `Retry-After`; không auto-loop. |
| `503` | Nêu dependency tạm thời; mutation có idempotency phải tra trạng thái/retry cùng key, không tạo key mới mù quáng. |
| Offline | Banner persistent; GET dùng cache có timestamp nếu không chứa PII nhạy cảm; form draft chỉ giữ memory/session-encrypted; mutation xếp hàng chỉ cho read-receipt/progress monotonic, các nghiệp vụ tiền/apply/publish/ATS phải người dùng retry. |
| Success | Toast ngắn + state inline; focus chuyển tới heading kết quả; không chỉ dựa màu. |

### 3.2 Responsive và accessibility

- Breakpoint hành vi: mobile `<640px`, tablet `640–1023px`, desktop `>=1024px`. Bảng dữ liệu chuyển thành card có nhãn field trên mobile; filter dùng drawer; CTA chính sticky nhưng không che nội dung. ATS board có list thay thế đầy đủ trên mobile, không bắt drag-and-drop.
- WCAG 2.2 AA: keyboard-only, focus visible, skip link, semantic landmarks/headings, contrast >=4.5:1, touch target >=44px, label thật cho input, alt text có ý nghĩa, caption/transcript cho media, không auto-play, hỗ trợ reduced motion và zoom 200%.
- Modal trap focus, Escape đóng nếu không mất dữ liệu; destructive confirmation nêu đúng đối tượng/hậu quả. Live region polite cho load/success, assertive cho session expiry/security error. Chart luôn có bảng dữ liệu tương đương.
- Ngày giờ hiển thị timezone người dùng và UTC tooltip; tiền định dạng `vi-VN`, VND nguyên; trạng thái có text+icon. Sponsored và AI luôn có nhãn bằng chữ, không chỉ màu.

### 3.3 Analytics và audit

Event UI dùng `{eventName, screenId, actorType, tenantId?, resourceType?, resourceId?, result, businessCode?, traceId, occurredAt}`; không gửi email, phone, CV text, chat body, evidence, câu trả lời assessment hay free-text support. Page view dedupe theo navigation. CTA mutation ghi `attempted/succeeded/failed`; backend audit mới là bằng chứng nghiệp vụ. Các event chuẩn: `screen_viewed`, `cta_clicked`, `form_validation_failed`, `filter_applied`, `empty_state_seen`, `api_error_seen`, `offline_state_seen`, `sponsored_impression`, `sponsored_clicked`, `ai_draft_reviewed`.

## 4. Public và Authentication

| ID | Route và guard | Dữ liệu/API | Nội dung, field và CTA | Luồng, validation và trạng thái riêng | Responsive, accessibility, analytics/audit |
|---|---|---|---|---|---|
| **SCR-IAM-001** | `/register`; anonymous, account active redirect app | `API-IAM-001` | Email, password + strength requirements, agreement links/version checkboxes; CTA Tạo tài khoản | Normalize email visually but không đổi người dùng âm thầm; password 12–128; disable double submit; accepted chuyển verify screen. Duplicate dùng safe message; 429 countdown; offline không queue credential | Password reveal có accessible name; agreement mở tab an toàn; track submit result only, không log email/password |
| **SCR-IAM-002** | `/verify-email`; token optional; pending account | `API-IAM-002`, `API-IAM-003` | Trạng thái link, nhập/paste token fallback, email masked, CTA Xác thực/Gửi lại | Auto-verify một lần khi token có; used/expired cho resend; cooldown hiện exact timer; success redirect signed return URL; không phân biệt email lạ ở resend | Live region cho kết quả; token input hỗ trợ paste; track verified/resend result |
| **SCR-IAM-003** | `/login`; anonymous | `API-IAM-004`, sau login dùng `API-IAM-011` | Email, password, remember device label; CTA Đăng nhập/Quên mật khẩu | Single submit; `MFA_REQUIRED` sang `/mfa`; suspended/deletion pending ra state riêng; invalid credential generic; lock hiện retry time; return URL chỉ same-site allowlist | Autofill chuẩn `username/current-password`; không CAPTCHA inaccessible; audit backend login, analytics chỉ outcome |
| **SCR-IAM-004** | `/recover`, `/reset-password`; anonymous | `API-IAM-009`, `API-IAM-010` | Email hoặc reset token, password mới/confirm; CTA Gửi hướng dẫn/Đặt lại | Forgot luôn cùng success state; expired/used token cho request lại; reset success revoke sessions rồi login; offline không lưu token/password | Announce policy errors; clipboard-safe token; track generic outcome |
| **SCR-IAM-005** | `/mfa`, `/account/mfa`; challenge/active privileged user | `API-IAM-005`, `API-IAM-017`, `API-IAM-018` | TOTP/recovery code; enrollment QR/secret hiển thị một lần; download/print recovery codes confirmation | Challenge max attempt/cooldown; enroll chưa active đến confirm; secret biến mất khi rời màn; lost MFA dẫn support verified flow; no browser persistence | QR có secret text alternative; segmented code vẫn là một accessible input; security audit mọi enrollment/challenge |
| **SCR-IAM-006** | `/account/security`; authenticated | `API-IAM-006`, `API-IAM-007`, `API-IAM-008`, `API-IAM-011`–`API-IAM-020`, `API-IAM-025` system-assisted | Profile identity, change password/email, sessions, logout all, MFA, deletion request/cancel | Step-up trước change/delete; current session marked; revoke confirmation; email cũ giữ đến verify; deletion nêu grace 30 ngày/legal hold/PII effects; token exchange không có CTA trực tiếp | Session list thành cards mobile; destructive dialog requires typed confirm; security operations audited, analytics redacted |
| **SCR-STU-001** | `/`; public | `API-STU-001`, `API-STU-003` | Giá trị Study, featured paths/courses, CTA Khám phá/Bắt đầu | Catalog failure giữ hero và retry section; authenticated CTA tới dashboard; sponsored content không tồn tại ở Study | Logical heading, reduce motion; track CTA/source campaign không PII |
| **SCR-STU-002** | `/paths`; public | `API-STU-001`, `API-STU-006` | Search, skill/level filter, sort, path cards, pagination | URL là nguồn filter; invalid filter reset có thông báo; empty có CTA clear; auth card có progress | Filter drawer mobile; result count announced; track filter aggregate |
| **SCR-STU-003** | `/paths/:slug`; public; chọn primary cần auth+onboarding | `API-STU-002`, `API-STU-012`–`API-STU-015` | Version, pinned courses, prerequisites, recommendation reason, current progress; CTA Chọn/Đổi lộ trình | Anonymous login return; onboarding missing dẫn wizard; cooldown dialog exact `nextAllowedAt`; switch confirm nêu progress giữ lại và reuse chỉ cùng version; 412 reload | Ordered curriculum accessible; confirmation keyboard-safe; audit switch ở backend |
| **SCR-STU-004** | `/courses`; public | `API-STU-003`, `API-STU-006` | Search/filter/sort, course cards, standalone badge, pagination | Mọi published course độc lập; empty/error như common; no onboarding gate | Card/grid to list; announce count; track filters |
| **SCR-STU-005** | `/courses/:slug`; public; enroll cần active account | `API-STU-004`, `API-STU-016` | Current published version, outcomes, curriculum preview, learner pinned enrollment, CTA Enroll/Continue | Verified learner enroll không onboarding; duplicate returns existing; if already old version show exact version and continue, không migrate; archived no new enroll | Curriculum accordion keyboard; version/status text; track enroll outcome |
| **SCR-STU-006** | `/samples/:lessonId`; public | `API-STU-005` | Sanitized sample blocks/resources, CTA course | Signed media expiry triggers refresh; unavailable/removed returns catalog CTA; no unsafe embed | Transcript/caption, no autoplay; media controls keyboard |
| **SCR-WRK-001** | `/jobs`; public | `API-WRK-001`, `API-WRK-004`, `API-PAY-012`, `API-PAY-013` | Search/filter/sort, organic cards and separate sponsored slots with “Được tài trợ”, pagination | URL filter; terminal job excluded; impression only after >=50% visible 1s; click signed placement; organic order không đổi do payment | Filter drawer/mobile cards; sponsored label announced; track filter/impression/click without fingerprinting |
| **SCR-WRK-002** | `/jobs/:slug`; public; apply requires candidate | `API-WRK-002`, `API-WRK-019`, `API-WRK-022` | Immutable published JD, company, salary, expiry, sponsored label, Save/Apply | Closed between load/apply returns no longer available; apply always rechecks revision; save prompts login; revision changed prompts review | Sticky apply CTA mobile; semantic sections; track view/save/apply-start |
| **SCR-WRK-003** | `/companies/:slug`; public | `API-WRK-003` | Verified badge, public company profile, active jobs | No internal members/legal docs; empty jobs state; unverified badge absent, never implied verified | Jobs list accessible; track public view only |

## 5. Learner Study

| ID | Route và guard | Dữ liệu/API | Nội dung, field và CTA | Luồng, validation và trạng thái riêng | Responsive, accessibility, analytics/audit |
|---|---|---|---|---|---|
| **SCR-STU-010** | `/learn/dashboard`; learner active | `API-STU-021`, `API-STU-034` | Primary path, standalone courses, continue lesson, pending review, recent notification | New learner empty có CTA browse course/onboarding riêng; stale snapshot shows calculated time; dependency error per widget, not whole page | Cards reorder mobile; accessible progress text; track CTA not percentages as PII |
| **SCR-STU-011** | `/learn/onboarding`; learner | `API-STU-009`–`API-STU-011`, `API-STU-006` | Multi-step goals, level, known skills, constraints, review/complete | Save partial with If-Match; back retains draft; required fields only at complete; 412 safe merge; completion immutable status though profile edits trigger new recommendation | Stepper not sole navigation; error summary; track step completion/category only |
| **SCR-STU-012** | `/learn/recommendations`; onboarding complete | `API-STU-012`, `API-STU-014` | Top 3 path cards with rule-based reason/score band and course versions; CTA chọn | Stale recommendation offers rerun/review; choosing invokes same primary-path confirmation; no Study AI claim | Reasons readable text; compare table stacks mobile; track selection ID |
| **SCR-STU-013** | `/learn/primary-path`; learner | `API-STU-013`–`API-STU-015`, `API-STU-049` admin-only not exposed | Active pinned version, steps/progress/history, switch eligibility and modal | Cooldown countdown server time; concurrent switch 412/409 reload; completed path can choose next without old period mutation; no active state offers choose | Timeline has ordered list fallback; modal states exact retained progress; track switch start/result |
| **SCR-STU-014** | `/learn/courses`; learner | `API-STU-017`, `API-STU-021` | Enrollment cards with source standalone/path, exact version, state/progress; Continue | Filters; no cancel/reset control; presentation hide is local preference only; superseded version still usable | Cards mobile; progress text and bar; track continue |
| **SCR-STU-015** | `/learn/courses/:courseId`; enrolled learner | `API-STU-018`, `API-STU-021` | Pinned curriculum, completion rules, lesson states, continue CTA | Access uses enrollment version; locked path step is advisory and does not block independent published course; content fetch failure no version substitution | Curriculum keyboard accordion; completion requirement list; track lesson open |
| **SCR-STU-016** | `/learn/lessons/:lessonId`; enrolled learner | `API-STU-019`, `API-STU-020`, `API-STU-033` | Content blocks/resources, exact block completion, Previous/Next/Assessment | Progress monotonic autosave with version; offline may queue monotonic facts with original idempotency and reconcile max; resource expired refresh URL; completion recalculated server-side | Reading width, transcript/caption, keyboard media; announce saved/offline; no raw learning content analytics |
| **SCR-STU-017** | `/learn/assessments/:assessmentId`; eligible learner | `API-STU-023`–`API-STU-027`, `API-STU-030`–`API-STU-032` | Variant QUIZ/TEXT/LINK/FILE; instructions/rubric/attempt count; Save draft/Submit | Quiz option validation without revealing correct answers; text <=20k; link HTTPS only/no preview fetch; file allowlist <=25MiB with upload→scan polling; Submit disabled until CLEAN; infected requires replace and consumes no attempt; submit confirmation seals immutable attempt | Fieldset/legend for quiz; upload progress/live scan state; timer never sole cue; analytics type/outcome only, no answers/files |
| **SCR-STU-018** | `/learn/assessments/:id/attempts` | `API-STU-028`, `API-STU-029`, `API-STU-033` | Attempt timeline, result, rubric feedback, clean attachment download, Resubmit when allowed | Pending review state; feedback release policy; revoked/expired file no download; NEEDS_REVISION/FAILED creates new attempt, never edits old | Rubric table mobile cards; status text/icon; track view/resubmit |
| **SCR-STU-019** | `/learn/progress`; learner | `API-STU-021`, `API-STU-022` | Summary, exact-version completion, activity timeline, date/type filters | Snapshot freshness shown; empty by filter vs no learning distinct; rebuild is not learner CTA; cursor/date errors recover | Charts have tables; timeline keyboard; analytics filter only |
| **SCR-STU-020** | `/notifications`; authenticated Study | `API-STU-034`–`API-STU-038` | Cursor feed, unread count, mark one/all, category/channel preferences | Optimistic read can rollback; mandatory security category locked with explanation; offline read receipt may queue; expired entries omitted | Feed uses list semantics/live count; preferences labels; no message body analytics |
| **SCR-STU-021** | `/community`; eligible learner | `API-STU-039`–`API-STU-042` | Eligible Zalo groups, current rules, Accept/Open/Report | No link until current rule accepted; changed rules require reaccept; eligibility rechecked on open; report duplicate/attachment scan states; external warning | Rules scroll not forced; external-link indication; report audited backend |
| **SCR-STU-022** | `/support`, `/support/:id`; learner | `API-STU-043`–`API-STU-046` | Ticket list/detail/events; category, subject, body, clean attachments; Create/Cancel | Duplicate open request points existing; terminal read-only; offline keeps draft only in memory; staff notes never shown | Conversation/timeline semantics; attachment accessibility; analytics category/outcome, not text |
| **SCR-STU-023** | `/profile`; learner | `API-STU-007`, `API-STU-008`, link to `SCR-IAM-006` | Display name, bio, skills, locale/timezone; account security deep link | If-Match save; taxonomy missing refresh; identity email/password not editable here; profile update does not revert onboarding | Autosuggest keyboard support; bio counter; audit PII update backend |

## 6. Candidate Work

| ID | Route và guard | Dữ liệu/API | Nội dung, field và CTA | Luồng, validation và trạng thái riêng | Responsive, accessibility, analytics/audit |
|---|---|---|---|---|---|
| **SCR-WRK-010** | `/candidate`; active candidate | `API-WRK-018`, `API-WRK-020`, `API-WRK-024`, `API-WRK-028` | Profile completeness, recommended jobs, active applications/interviews/invitations | Widget errors isolated; new user CTA profile/jobs; sponsored recommendations separated/labeled; terminal applications remain history | Cards mobile; accessible status summaries; no sensitive recommendation features in analytics |
| **SCR-WRK-011** | `/candidate/profile`; candidate | `API-WRK-005`, `API-WRK-006`, `API-WRK-004` | Basics, summary, skills, education, experience; Save/Preview | If-Match/nested stable IDs; date overlaps warning; sanitize; preview does not imply searchable; 412 compare | Repeatable sections keyboard reorder buttons; field errors; PII update audited |
| **SCR-WRK-012** | `/candidate/privacy`; candidate + step-up opt-in | `API-WRK-007`, `API-PAY-011` | Private default, searchable preview, allowed display fields, consent/policy/expiry, sponsored profile opt-in | Opt-in explicit unchecked default; contact/CV/evidence never selectable; opt-out immediate UI/API hide, shows deindex target <=5m and stops promotion; 412 reload | Plain-language consent, no dark pattern; privacy action audited, analytics only enabled/disabled |
| **SCR-WRK-013** | `/candidate/cvs`, `/candidate/cvs/:cvId`; owner | `API-WRK-008`–`API-WRK-013`, `API-AIX-001`, `API-AIX-005`, `API-AIX-006` | CV list/editor, typed sections, template/version, default, Publish/Export, AI draft panel | Draft autosave If-Match; publish immutable; premium entitlement gate before export; async export/AI polling; AI output untrusted, must accept/edit then separately save; failure refunds reservation | Editor single-column mobile; reorder keyboard; PDF accessible metadata; never log CV/AI input text |
| **SCR-WRK-014** | `/candidate/portfolio`; candidate | `API-WRK-014`–`API-WRK-017` | Link/file item, title/description/visibility, reorder/edit/delete | HTTPS syntax only and no server preview; file CLEAN; deletion does not alter application snapshot; 412 reload | File/link type announced; keyboard ordering; audit mutations |
| **SCR-WRK-015** | `/candidate/discover`; candidate | `API-WRK-018`, `API-WRK-019`, `API-PAY-012`, `API-PAY-013` | Explained recommendations, saved jobs, labeled sponsored slots | Explanation shows job criteria overlap, no sensitive features; stale/closed job retained in saved list with status; promotion tracking signed/deduped | Reason list not opaque score only; labels accessible; track save/click |
| **SCR-WRK-016** | `/candidate/invitations`; candidate | `API-WRK-020`, `API-WRK-021` | Invitation/job/tenant/message/expiry; Accept/Decline | Accept routes to apply wizard; explicitly states application/chat not yet created; expired/duplicate transition reload; decline optional reason | CTA order non-coercive; analytics response only, message excluded |
| **SCR-WRK-017** | `/jobs/:jobId/apply`; candidate | `API-WRK-022`, `API-IAM-025`, `API-STU-061`, `API-STU-062`, `API-WRK-023` | Multi-step job revision, published CV, profile/portfolio snapshot preview, answers, Study evidence chooser, consent, final review | Fetch Study evidence with 5m downscoped token; select each ID explicitly; no evidence still valid. Recheck revision before submit; one idempotency key through retry; Study outage shows evidence unavailable but allows submit with stored selections; duplicate opens existing application | Stepper accessible; snapshot/consent plain language; no evidence content analytics; application audit backend |
| **SCR-WRK-018** | `/candidate/applications`; candidate | `API-WRK-024` | Filtered application cards/status/date/job snapshot | Status comes server; empty/filter distinction; no delete; terminal retained | Cards/mobile; status text; track filter/open |
| **SCR-WRK-019** | `/candidate/applications/:id`; owner | `API-WRK-025`–`API-WRK-027`, `API-WRK-031` | Snapshot, ATS history safe subset, evidence PENDING/READY/UNAVAILABLE/REVOKED, withdraw/consent withdraw, links interview/chat | Evidence error explicitly not a rejection signal; consent withdraw confirms hide/retention; application withdraw terminal and chat read-only; recruiter internal notes hidden | Timeline accessible; destructive dialogs; privacy/application actions audited |
| **SCR-WRK-020** | `/candidate/interviews`, `/candidate/interviews/:id`; candidate participant | `API-WRK-028`–`API-WRK-030` | Current schedule/version/timezone/mode, Confirm/Decline/Request reschedule, ICS | Stale schedule conflict reloads; alternate slot validation; expired one-use ICS refresh; internal calendar only; cancel/no-show/completed states | Local+UTC accessible time, download label; response audited |
| **SCR-WRK-021** | `/candidate/applications/:id/chat`; participant | `API-WRK-031`–`API-WRK-034`, `API-INT-011` | REST history, plain-text composer, receipts, reconnect indicator; V1 không có file/HTML | REST first then socket subscribe; dedupe eventId/sequence; gap refetch REST; terminal read-only; send uses client message ID/idempotency; optimistic bubble marked pending/failed; tombstone retained | Focus does not jump on new messages; live region optional/mute; chat body excluded analytics, moderation audit backend |
| **SCR-WRK-022** | `/candidate/topcv-billing`; candidate | `API-PAY-001`–`API-PAY-006`, `API-PAY-011`, `API-AIX-001`, `API-WRK-012` | VND products/credits/entitlements/orders/refunds, premium templates, AI assistance, sponsored opt-in | Provider choice VNPAY/MoMo; amount server authoritative; no auto-renew/card storage; pending order poll; entitlement only settled; consumed benefit refund policy shown | Price read aloud; provider redirect warning; finance mutation audited, analytics product/provider only |
| **SCR-WRK-023** | `/billing/return/:provider`; authenticated owner + opaque return nonce | `API-PAY-003`, `API-PAY-016` | Pending/success/failure status from internal order, CTA return/refresh | Never trust URL success; poll bounded then manual refresh; duplicate tab consistent; no entitlement claim until SETTLED | Live status; no raw provider payload; track final known outcome |

## 7. Enterprise và Publisher Work

| ID | Route và guard | Dữ liệu/API | Nội dung, field và CTA | Luồng, validation và trạng thái riêng | Responsive, accessibility, analytics/audit |
|---|---|---|---|---|---|
| **SCR-WRK-030** | `/enterprise/create`; authenticated, no conflicting setup | `API-WRK-035` | Legal/public name, tax ID/country, contact, terms; Create workspace | Duplicate routes safe claim/support; creator becomes owner but tenant `PENDING_VERIFICATION`; cannot verify self; offline không queue | Multi-step review; tax error linked; legal creation audited |
| **SCR-WRK-031** | `/enterprise/:enterpriseId`; active membership | `API-WRK-036`, `API-WRK-042`, `API-WRK-054`, `API-PAY-005` | Verification/plan, jobs, ATS counts, interviews, usage alerts | Per-widget permission filter; tenant suspended locks mutation; cache reset on switch; metrics show freshness | Dashboard cards/table alternative; track widget/CTA only |
| **SCR-WRK-032** | `/enterprise/:enterpriseId/settings`; `PERM-WRK-001` or member permissions | `API-WRK-037`–`API-WRK-041` | Public/legal profile, verification docs/state, member list/invite/roles | Legal change after verified starts reverification; docs require CLEAN; member role If-Match; cannot remove last owner/self-escalate; revoked member session/query invalidated | Tables to cards; role checkbox descriptions; all PII/role/doc access audited |
| **SCR-WRK-033** | `/enterprise/:enterpriseId/jobs`; `PERM-WRK-010` | `API-WRK-042`, `API-WRK-048`–`API-WRK-050` | Job list/filter/lifecycle, Pause/Resume/Close/Create | State-specific CTA; terminal no reopen; paused/closed hidden public synchronously; close does not erase applications; 412 reload | Mobile cards; no drag-only action; lifecycle changes audited |
| **SCR-WRK-034** | `/enterprise/:enterpriseId/jobs/:jobId/edit`; author or `PERM-WRK-011` | `API-WRK-043`–`API-WRK-045`, `API-WRK-004`, `API-AIX-002`, `API-AIX-005`, `API-AIX-006` | Structured JD, skills/salary/location/questions/expiry, revision history, AI JD draft | Published opens new DRAFT revision; autosave If-Match; salary/expiry/policy validation; AI output requires human accept/edit then explicit save; prompt content rendered as text | Editor mobile linear; counters/error summary; no JD raw analytics, revisions audited |
| **SCR-WRK-035** | `/enterprise/:enterpriseId/jobs/:jobId/publish`; `PERM-WRK-012/013`, MFA where required | `API-WRK-046`, `API-WRK-047` | Completeness/policy/rights/entitlement check, review state, trusted grant disclosure, Submit/Publish | Default submit review; trusted active grant enables publish but checks remain; stale/expired grant or version blocks; publish immutable and index async; UI public preview verifies DB state | Checklist semantic; error links editor field; publish actor/reason audited |
| **SCR-WRK-036** | `/enterprise/:enterpriseId/talent/search`; `PERM-WRK-020` + entitlement | `API-WRK-051`, `API-WRK-004`, `API-PAY-012`, `API-PAY-013` | Filters, redacted result cards, organic reason, separately labeled sponsored profiles | Only opted-in profiles; never contact/CV/evidence; API 404 after opt-out even cached; filter allowlist; entitlement empty/error distinct | Filters drawer; sponsored text label; every search query/result ID audited, analytics no candidate attributes |
| **SCR-WRK-037** | `/enterprise/:enterpriseId/talent/:candidatePublicId`; search permission | `API-WRK-052`, `API-WRK-053` | Redacted public profile/portfolio preview, matching reason, Invite CTA | Recheck consent each open/action; rotating ID; invite requires own published job/credit and creates no chat/application; candidate disappearance generic | Accessible reason list; no contact reveal; profile access/invite audited |
| **SCR-WRK-038** | `/enterprise/:enterpriseId/talent/invitations`; `PERM-WRK-021` | `API-WRK-053` plus invitation projection from workspace | Invitation list/status/expiry/job, Create invite | Duplicate/open/expired states; no “message” CTA; acceptance only prompts candidate apply; consumed entitlement visible | Table/card; track invitation outcome, not candidate text |
| **SCR-WRK-039** | `/enterprise/:enterpriseId/ats`; `PERM-WRK-030` | `API-WRK-054`, `API-WRK-058`, `API-AIX-004`, `API-AIX-005`, `API-AIX-006` | List/board by canonical stage, filter/assignee; human status dialog; AI shortlist suggestion panel | Board has accessible list; drag opens confirmation and uses exact version; reason/artifact requirements; 412 returns card current column; AI never moves card and acceptance only selects/filter-highlights | Keyboard move menu and list view; counts announced; status transition audited, AI label/decision tracked |
| **SCR-WRK-040** | `/enterprise/:enterpriseId/applications/:id`; assigned recruiter/scoped permission | `API-WRK-055`–`API-WRK-059`, `API-AIX-003`, `API-AIX-005`, `API-AIX-006` | Immutable job/CV/profile/portfolio snapshots, answers, evidence state, notes, assignees, offer/status, match explanation | Field-level contact; evidence PENDING/UNAVAILABLE cannot be negative signal and has no score; withdrawn/revoked hidden; note internal; transition requires human/reason/current version; AI uses excluded fields and separate review | Tabs retain heading/focus; snapshot download authorized; every PII/evidence/decision access audited |
| **SCR-WRK-041** | `/enterprise/:enterpriseId/interviews/:id`; assigned recruiter | `API-WRK-060`–`API-WRK-062`, `API-WRK-030` | Current schedule/version, participants, mode, candidate response, Reschedule/Cancel/No-show/Complete/ICS | Internal participant IDs only; timezone and overlap warning; reschedule immutable version resets confirmation; no-show after grace; ICS internal only | Calendar has list form/table; date input labeled timezone; actions audited |
| **SCR-WRK-042** | `/enterprise/:enterpriseId/applications/:id/chat`; assigned recruiter | `API-WRK-031`–`API-WRK-034`, `API-INT-011` | Same authoritative chat as candidate, recruiter assignment badge | Assignment checked every send/subscribe; removed recruiter loses access; terminal read-only; REST/socket recovery and tombstone behavior như candidate | Message focus/live rules; chat body excluded analytics; access/moderation audited |
| **SCR-WRK-043** | `/enterprise/:enterpriseId/billing-topjd`; billing permission | `API-PAY-001`–`API-PAY-013`, `API-WRK-043`, `API-WRK-047`, `API-UNI-013` | Products/orders/entitlements/invoices/refunds, TopJD credits, sponsored job, AI JD usage, university partnership requests | VND prepaid/no auto-renew; provider redirect; settlement authoritative; promotion requires published job and visible label, separate organic; partnership response needs its own permission, no implicit data share | Finance tables/cards and CSV async where permitted; all finance/partnership mutations audited |
| **SCR-WRK-044** | `/enterprise/:enterpriseId/billing/return/:provider`; billing member + nonce | `API-PAY-003`, `API-PAY-016` | Tenant order status and return CTA | Same authoritative pending/poll rules as candidate; tenant membership rechecked; URL never settles | Live status, no provider secret; track safe outcome |

## 8. University

| ID | Route và guard | Dữ liệu/API | Nội dung, field và CTA | Luồng, validation và trạng thái riêng | Responsive, accessibility, analytics/audit |
|---|---|---|---|---|---|
| **SCR-UNI-001** | `/university/create`; authenticated representative | `API-UNI-001` | Legal/public identity, institution code, contact, terms; Create | Duplicate claim/support; creator owner of tenant `PENDING_VERIFICATION`; cannot self-verify | Stepper/error summary; creation audited |
| **SCR-UNI-002** | `/university/:universityId/verification`; `PERM-UNI-001` | `API-UNI-002` | Legal snapshot, CLEAN documents, consent, status/checklist | Pending locks new submission; requested-info creates revision; sensitive docs signed and no preview cache | Accessible upload/scan; doc access and submit audited |
| **SCR-UNI-003** | `/university/:universityId/members`; membership admins | `API-UNI-003`, `API-UNI-004` | Member/status/role list, invite form | Seat/role/last-owner rules; invite expiry; tenant switch reset; same generic cross-tenant errors | Table/cards; role descriptions; actions audited |
| **SCR-UNI-004** | `/university/:universityId/affiliations`; `PERM-UNI-010/031` | `API-UNI-005`, `API-UNI-016` | Invitation batch/result, affiliation state; individual detail only with purpose-specific consent | Batch per-row result/download redacted; no active affiliation until learner accepts; detail denied on expired/withdrawn consent; never CV/chat/Study evidence | Large table virtualized with accessible nonvirtual export; every individual access privacy-audited |
| **SCR-UNI-005** | `/candidate/university-affiliations`; invitee/affiliated learner | `API-UNI-006`, `API-UNI-007` | University invitation, requested purposes/fields/expiry, Accept/Withdraw consent | Consent unchecked/default deny, max 12m; withdrawal immediate; explain aggregate anonymized history and no application creation | Plain-language purpose list, no bundled consent; privacy audit |
| **SCR-UNI-006** | `/university/:universityId/cohorts`; `PERM-UNI-011` | `API-UNI-008`, `API-UNI-009` | Cohort code/name/dates/criteria/member count, Add/Remove affiliation | Active affiliations only; If-Match on membership set; criteria stored snapshot; no raw Study data | Table/card and bulk accessible selection; mutation audited |
| **SCR-UNI-007** | `/university/:universityId/programs`; `PERM-UNI-020` | `API-UNI-010` | Internship program rules/dates/partner enterprises/status | Partner must active; DRAFT review before distribution policy; invalid date/scope linked fields | Structured rule builder keyboard-safe; audit |
| **SCR-UNI-008** | `/university/:universityId/campus-jobs`; `PERM-UNI-021` | `API-UNI-011`, `API-WRK-001`, `API-WRK-002` | Select public accepting jobs/cohorts/period/message; Distribution history | Recheck job at submit; distribution notification only, never apply/referral/chat; cohort empty warning | Search/select keyboard; message excluded analytics; audit recipient aggregate |
| **SCR-UNI-009** | `/university/:universityId/partnerships`; `PERM-UNI-022` | `API-UNI-012` | Enterprise, exact scopes/purposes/dates, pending/active history | Bilateral acceptance required; scope change creates new version; no data sharing before active; expiry ends access | Scope checklist plain language; partnership audited |
| **SCR-UNI-010** | `/university/:universityId/referrals`; `PERM-UNI-023` | `API-UNI-014` | Consented affiliation, public job, note/status | Recheck JOB_REFERRAL consent and job; referral invites candidate choice, never creates application/chat; consent withdrawal hides individual detail | Candidate selection requires purpose badge; note excluded analytics; privacy audit |
| **SCR-UNI-011** | `/university/:universityId/reports`; `PERM-UNI-030` | `API-UNI-015` | Date/cohort/program dimensions, outcome metrics, freshness, export | Default aggregate; every cell `<10` is “Đã ẩn để bảo vệ riêng tư”, not zero; dimension combinations also thresholded; individual drilldown absent | Chart + table/data download; suppressed cells announced; report query/export audited |

## 9. Publisher, Reviewer và Admin/Operations

Các route `/ops` dùng MFA bắt buộc, permission cụ thể và navigation sinh từ server authorization context. Search/read PII, download, export, decision, role, trusted grant, finance và break-glass đều audit. Admin không được sửa trực tiếp database; mọi correction là append-only API.

| ID | Route và guard | Dữ liệu/API | Nội dung, field và CTA | Luồng, validation và trạng thái riêng | Responsive, accessibility, analytics/audit |
|---|---|---|---|---|---|
| **SCR-OPS-001** | `/ops/identity/users`; `PERM-IAM-001/002` + MFA | `API-IAM-021`, `API-IAM-022` | Filter/redacted users, account state/version, Suspend/Reactivate | Search exact/minimized; status reason required; cannot self-suspend; suspension revokes sessions and propagates; 412 reload | Table/cards; high-risk confirmation; search/read/change audited |
| **SCR-OPS-002** | `/ops/identity/roles`; `PERM-IAM-003` + recent MFA | `API-IAM-023` | User coarse global roles/current version, exact-set editor | Last platform admin protected; local tenant roles not shown/changed; step-up expiry prompt | Matrix has textual alternative; role diff/reason audited |
| **SCR-OPS-003** | `/ops/study/content`; `PERM-STU-001/004` | `API-STU-051`–`API-STU-053`, `API-STU-057` | Path/course stable entities, versions/status/owner, Create version/Archive | Published rows immutable; archive prevents new enroll but preserves pinned access; version lineage visible | Table/cards; version status text; all mutations audited |
| **SCR-OPS-004** | `/ops/study/paths/:id/edit`; author | `API-STU-052`–`API-STU-055` | Path metadata/version, ordered pinned course versions, rights/issues | DRAFT only; If-Match; exact courseVersion required; preview/publish check; no current course substitution | Keyboard reorder buttons; conflict compare; draft audit diff |
| **SCR-OPS-005** | `/ops/study/courses/:id/edit`; author | `API-STU-052`–`API-STU-055` | Course version/chapters/lessons/blocks/resources/completion rules | DRAFT only; content sanitize; resources must CLEAN; published copy creates new draft; structure checks | Tree has list/editor alternative; no drag-only; content audit |
| **SCR-OPS-006** | `/ops/study/assessments/:id/edit`; author/reviewer separation | `API-STU-054`, `API-STU-055`, `API-STU-030`–`API-STU-032` | Exactly one placement, type, quiz options/keys, rubric, attempts, file assets | Placement XOR enforced; QUIZ auto-grade config; TEXT/LINK/FILE rubric; answers never in preview learner payload; file scan states | Form sections/fieldset; option reorder keyboard; audit content, never log answer key analytics |
| **SCR-OPS-007** | `/ops/study/publish/:kind/:id`; `PERM-STU-003` + MFA | `API-STU-055`, `API-STU-056` | Immutable check report: rights, sanitize, assets, assessments, accessibility; Publish | Check hash/age/version; trusted publisher does not bypass; concurrent/stale check reload; success shows superseded/current IDs and impacted learners | Checklist links failures; typed confirmation; publish fully audited |
| **SCR-OPS-008** | `/ops/study/content-issues`; `PERM-STU-005` | `API-STU-058`, `API-STU-059` | Queue/filter/detail/events/status/resolution | Terminal reopen needs reason; affected published content can be taken down by separate authorized flow; attachment CLEAN only | Queue cards mobile; severity text; action audited |
| **SCR-OPS-009** | `/ops/work/job-reviews`; `PERM-OPS-002` | `API-OPS-003` | Review queue/status/risk/age, automated flags | No employer-private unrelated data; assignment/filter; empty vs dependency error | Table/card; priority accessible; read audited where PII |
| **SCR-OPS-010** | `/ops/work/job-reviews/:id`; reviewer | `API-OPS-004` | Immutable job revision, policy checklist, history; Approve/Reject/Request change | Maker/reviewer separation; reason/policy codes; approval does not auto publish; two reviewer conflict reload | Side-by-side stacks mobile; decision audit immutable |
| **SCR-OPS-011** | `/ops/trusted-publishers`; `PERM-OPS-003` + MFA | `API-OPS-005`, `API-OPS-006` | Eligibility evidence, domain/scope, validity, bootstrap flag/reason, grants/revocations | Default threshold 3 approved +90 clean days; pilot bootstrap explicit reason; self-grant prohibited; revoke immediate future use | High-risk review dialog; grant/revoke security audited/alerted |
| **SCR-OPS-012** | `/ops/study/reviews`; `PERM-STU-006` | `API-STU-047` | Manual assessment queue/type/age/assignee, CLEAN indicator | Pending/infected file absent; claim/filters; no answer export without permission | Accessible queue/table; access audit |
| **SCR-OPS-013** | `/ops/study/reviews/:attemptId`; assigned reviewer | `API-STU-029`, `API-STU-033`, `API-STU-048` | Immutable answer, rubric, history, score/feedback/decision | File URL short-lived and CLEAN; If-Match; second reviewer conflict; NEEDS_REVISION creates learner next-attempt option, no edit old | Rubric labels/error summary; answer/file access and decision audited |
| **SCR-OPS-014** | `/ops/study/support`; `PERM-STU-008` | `API-STU-045` | Ticket queue/detail/events/internal notes/SLA | Owner boundary; internal notes separated; resolve/reopen history append-only through event contract; attachment permission | Timeline accessible; PII read audited; no body analytics |
| **SCR-OPS-015** | `/ops/study/learners/:id`; `PERM-STU-009/010` + MFA for mutation | `API-STU-049`, `API-STU-050`, read projections from Study | Learner support summary, primary path periods/progress facts, Override/Adjustment | No password/account state direct edit; override reason and cooldown; adjustment appends fact correction/rebuild, never reset/delete; exact target/version | Diff/impact preview; high-risk typed confirm; every read/change audited |
| **SCR-OPS-016** | `/ops/study/rbac`; `PERM-STU-011` + MFA | `API-STU-060` | Local roles/scopes/expiry/assignment history | Exact-set roles; separation author/publisher/reviewer; global/tenant roles out of scope; last admin safeguard policy | Matrix text table; mutation security audit |
| **SCR-OPS-017** | `/ops/verifications`; `PERM-OPS-001` + MFA | `API-OPS-001` | Enterprise/university cases, type/status/age/risk | No raw doc prefetch; assignment and safe preview only | Queue table/cards; view audited |
| **SCR-OPS-018** | `/ops/verifications/:id`; reviewer not submitter | `API-OPS-002` | Legal snapshot, signed CLEAN docs, checklist/history, decision | Maker-checker; If-Match; request-info/reject reason; document URL expires; verified projection after commit | Sensitive banner; doc/decision audit; no download analytics payload |
| **SCR-OPS-019** | `/ops/payments/reconciliation`; `PERM-PAY-001/003` + MFA | `API-PAY-008`, `API-PAY-009` | Provider/date/state mismatch, order/attempt/webhook hashes, Requery/Mark reviewed | Cannot manually settle without verified provider evidence; out-of-order timeline; stale/provider unavailable pending; export scoped | Finance table; amount/status text; query/action/export audit |
| **SCR-OPS-020** | `/ops/payments/refunds`; `PERM-PAY-002` + recent MFA | `API-PAY-006`, `API-PAY-007` | Request/order/refundable/consumed benefit/reason; Approve/Reject | Maker-checker and no self-approve; amount limits/If-Match; provider processing async; refund/chargeback separate | VND accessible, confirmation; immutable finance audit |
| **SCR-OPS-021** | `/ops/reports`; report permission | `API-OPS-010` | Report selector/filter/freshness/SLO/queue metrics, export where allowed | Daily projection/no warehouse; freshness warning; aggregate privacy threshold; dependency-specific errors | Chart + data table; filter/export audited |
| **SCR-OPS-022** | `/ops/ai/runtime`; `PERM-AIX-001/002` + MFA | `API-AIX-007`, `API-AIX-008` | Provider/model config refs, health, queues, kill switch scope/reason | Secrets never displayed; validation probe then activate version; kill switch before/after provider and refunds reservations; manual paths stay available | Status text, confirmation; security audit/alert |
| **SCR-OPS-023** | `/ops/ai/policies`; `PERM-AIX-003` | `API-AIX-009`, `API-AIX-010` | Prompt/policy/model/eval versions, excluded fields, dataset results/threshold | Immutable version/maker-checker; required exclusions cannot remove; production PII prohibited in eval; activation only passing evaluation | Diff/table accessible; prompt text treated untrusted; version/action audited |
| **SCR-OPS-024** | `/ops/audit`; scoped audit permission + MFA | `API-OPS-007`, `API-OPS-008` | Cursor/filter/redacted audit, async encrypted export | Each service queried separately; date <=31d per interactive call; export reason/watermark/7d expiry; viewing/export itself audited | Virtual list with accessible pagination fallback; no raw sensitive value |
| **SCR-OPS-025** | `/ops/break-glass`; incident role + hardware/recent MFA | `API-OPS-009` | Ticket/scope/reason/duration/second approval/state | Max60m; second approval unless SEV-1 declaration; prominent countdown/stop; no permanent role mutation; expiry automatic | Persistent danger banner; every view/action immediate alert/audit |
| **SCR-OPS-026** | `/ops/moderation/chat`; moderator permission | `API-WRK-034` and moderation read projection | Report queue, minimal conversation context, policy reason, Tombstone | No unrestricted chat search; open only report/incident scope; author delete window distinct; content hidden but hash/event retained | Sensitive warning; body not analytics; read/decision audited |

## 10. Luồng màn hình trọng yếu

### 10.1 Standalone course và primary path

1. Từ `SCR-STU-005`, learner đã verify gọi `API-STU-016` trực tiếp; onboarding không được chèn vào guard.
2. `SCR-STU-011` hoàn tất onboarding rồi `SCR-STU-012` hiển thị top 3; chọn path qua `SCR-STU-013` và `API-STU-014`.
3. Switch modal luôn hiển thị path/version đích, dữ liệu giữ lại, cảnh báo completion chỉ reuse khi cùng `courseVersionId`, thời điểm cooldown tiếp theo. `409` giữ modal và hiển thị server time; `412` reload current period.
4. `SCR-STU-016` gửi fact monotonic; snapshot có thể stale/rebuild nhưng UI không cho nhập phần trăm.

### 10.2 Apply và evidence

1. `SCR-WRK-017` khóa job revision và lấy context Work. Token exchange chỉ cho `study-evidence` 5 phút; Study chooser chỉ thấy evidence của chính subject.
2. Candidate chọn từng evidence, đọc consent và review snapshot. Nếu Study mất kết nối, UI cho bỏ evidence hoặc vẫn submit selected IDs; không gọi lỗi này là “không đủ năng lực”.
3. Submit giữ cùng `Idempotency-Key` qua retry. Success đi `SCR-WRK-019`, hiển thị evidence PENDING. Worker READY/UNAVAILABLE cập nhật bằng polling/event; application status không đổi.
4. Candidate rút consent làm UI ẩn ngay. Recruiter `SCR-WRK-040` không còn download/content; revocation hiển thị neutral status và không tạo AI/match event.

### 10.3 Payment

1. Buyer chọn product/price version và provider; confirmation ghi rõ số VND, one-time/no auto-renew/no stored card.
2. Redirect ra VNPAY/MoMo. Quay về `SCR-WRK-023` hoặc `SCR-WRK-044` chỉ tra internal order; query success từ provider không được render là paid.
3. Webhook settled tạo entitlement; UI poll bounded và invalidate. Duplicate/out-of-order không tạo hai quyền. Mismatch hiện “Đang đối soát”, không “Thất bại” tùy tiện.
4. Refund hiển thị request→approved→provider processing→settled/failed; entitlement/reversal theo ledger, lịch sử không xóa.

### 10.4 ATS, interview, chat và AI

1. ATS transition bắt buộc human confirmation/reason/current version; AI panel chỉ suggestion. `412` trả card về trạng thái server và giữ note chưa submit trong memory.
2. Interview schedule/reschedule tạo version và ICS `SEQUENCE`; candidate response đúng version. Không có nút Connect Google/Microsoft V1.
3. Chat load REST trước, WebSocket sau; gap sequence refetch REST. Assignment/terminal state được recheck server ở mỗi send và subscription.
4. AI job async luôn hiển thị model/policy provenance, excluded-field policy, uncertainty và review. Accept AI output chưa save CV/JD và chưa đổi ATS; user phải thực hiện mutation riêng.

## 11. Ma trận coverage API → màn hình

Mọi API public có ít nhất một surface; API internal/webhook/realtime không có màn hình trực tiếp được ghi `N/A` cùng lý do. Đây là coverage triển khai, không thay thế định nghĩa API.

| API | Screen hoặc N/A có lý do |
|---|---|
| `API-IAM-001`, `API-IAM-002`, `API-IAM-003`, `API-IAM-004`, `API-IAM-005` | `SCR-IAM-001`, `SCR-IAM-002`, `SCR-IAM-003`, `SCR-IAM-005` |
| `API-IAM-006`, `API-IAM-007`, `API-IAM-008`, `API-IAM-009`, `API-IAM-010`, `API-IAM-011`, `API-IAM-012`, `API-IAM-013`, `API-IAM-014`, `API-IAM-015`, `API-IAM-016`, `API-IAM-017`, `API-IAM-018`, `API-IAM-019`, `API-IAM-020`, `API-IAM-025` | `SCR-IAM-004`, `SCR-IAM-005`, `SCR-IAM-006`; token exchange chạy nền trong `SCR-WRK-017` |
| `API-IAM-021`, `API-IAM-022`, `API-IAM-023` | `SCR-OPS-001`, `SCR-OPS-002` |
| `API-IAM-024` | N/A — JWKS được gateway/service đọc, không có UI |
| `API-STU-001`, `API-STU-002`, `API-STU-003`, `API-STU-004`, `API-STU-005`, `API-STU-006` | `SCR-STU-001`–`SCR-STU-006` |
| `API-STU-007`, `API-STU-008`, `API-STU-009`, `API-STU-010`, `API-STU-011`, `API-STU-012`, `API-STU-013`, `API-STU-014`, `API-STU-015` | `SCR-STU-011`, `SCR-STU-012`, `SCR-STU-013`, `SCR-STU-023` |
| `API-STU-016`, `API-STU-017`, `API-STU-018`, `API-STU-019`, `API-STU-020`, `API-STU-021`, `API-STU-022` | `SCR-STU-005`, `SCR-STU-010`, `SCR-STU-014`–`SCR-STU-016`, `SCR-STU-019` |
| `API-STU-023`, `API-STU-024`, `API-STU-025`, `API-STU-026`, `API-STU-027`, `API-STU-028`, `API-STU-029`, `API-STU-030`, `API-STU-031`, `API-STU-032`, `API-STU-033` | `SCR-STU-017`, `SCR-STU-018`, `SCR-OPS-006`, `SCR-OPS-013` |
| `API-STU-034`, `API-STU-035`, `API-STU-036`, `API-STU-037`, `API-STU-038`, `API-STU-039`, `API-STU-040`, `API-STU-041`, `API-STU-042`, `API-STU-043`, `API-STU-044`, `API-STU-045`, `API-STU-046` | `SCR-STU-020`, `SCR-STU-021`, `SCR-STU-022`, `SCR-OPS-014` |
| `API-STU-047`, `API-STU-048`, `API-STU-049`, `API-STU-050`, `API-STU-051`, `API-STU-052`, `API-STU-053`, `API-STU-054`, `API-STU-055`, `API-STU-056`, `API-STU-057`, `API-STU-058`, `API-STU-059`, `API-STU-060` | `SCR-OPS-003`–`SCR-OPS-008`, `SCR-OPS-012`, `SCR-OPS-013`, `SCR-OPS-015`, `SCR-OPS-016` |
| `API-STU-061`, `API-STU-062` | `SCR-WRK-017` qua audience token; Study không có evidence-export picker riêng |
| `API-WRK-001`, `API-WRK-002`, `API-WRK-003`, `API-WRK-004` | `SCR-WRK-001`, `SCR-WRK-002`, `SCR-WRK-003` và form metadata |
| `API-WRK-005`, `API-WRK-006`, `API-WRK-007`, `API-WRK-008`, `API-WRK-009`, `API-WRK-010`, `API-WRK-011`, `API-WRK-012`, `API-WRK-013` | `SCR-WRK-011`, `SCR-WRK-012`, `SCR-WRK-013` |
| `API-WRK-014`, `API-WRK-015`, `API-WRK-016`, `API-WRK-017`, `API-WRK-018`, `API-WRK-019`, `API-WRK-020`, `API-WRK-021` | `SCR-WRK-014`, `SCR-WRK-015`, `SCR-WRK-016` |
| `API-WRK-022`, `API-WRK-023`, `API-WRK-024`, `API-WRK-025`, `API-WRK-026`, `API-WRK-027`, `API-WRK-028`, `API-WRK-029`, `API-WRK-030` | `SCR-WRK-017`, `SCR-WRK-018`, `SCR-WRK-019`, `SCR-WRK-020` |
| `API-WRK-031`, `API-WRK-032`, `API-WRK-033`, `API-WRK-034` | `SCR-WRK-021`, `SCR-WRK-042`, `SCR-OPS-026` |
| `API-WRK-035`, `API-WRK-036`, `API-WRK-037`, `API-WRK-038`, `API-WRK-039`, `API-WRK-040`, `API-WRK-041` | `SCR-WRK-030`, `SCR-WRK-031`, `SCR-WRK-032` |
| `API-WRK-042`, `API-WRK-043`, `API-WRK-044`, `API-WRK-045`, `API-WRK-046`, `API-WRK-047`, `API-WRK-048`, `API-WRK-049`, `API-WRK-050` | `SCR-WRK-033`, `SCR-WRK-034`, `SCR-WRK-035` |
| `API-WRK-051`, `API-WRK-052`, `API-WRK-053`, `API-WRK-054`, `API-WRK-055`, `API-WRK-056`, `API-WRK-057`, `API-WRK-058`, `API-WRK-059` | `SCR-WRK-036`–`SCR-WRK-040` |
| `API-WRK-060`, `API-WRK-061`, `API-WRK-062` | `SCR-WRK-041` |
| `API-UNI-001`, `API-UNI-002`, `API-UNI-003`, `API-UNI-004`, `API-UNI-005`, `API-UNI-006`, `API-UNI-007`, `API-UNI-008`, `API-UNI-009`, `API-UNI-010`, `API-UNI-011`, `API-UNI-012`, `API-UNI-013`, `API-UNI-014`, `API-UNI-015`, `API-UNI-016` | `SCR-UNI-001`–`SCR-UNI-011`, `SCR-WRK-043` |
| `API-PAY-001`, `API-PAY-002`, `API-PAY-003`, `API-PAY-004`, `API-PAY-005`, `API-PAY-006`, `API-PAY-007`, `API-PAY-008`, `API-PAY-009`, `API-PAY-010`, `API-PAY-011`, `API-PAY-012`, `API-PAY-013`, `API-PAY-016` | `SCR-WRK-001`, `SCR-WRK-015`, `SCR-WRK-022`, `SCR-WRK-023`, `SCR-WRK-043`, `SCR-WRK-044`, `SCR-OPS-019`, `SCR-OPS-020` |
| `API-PAY-014`, `API-PAY-015` | N/A — provider gọi webhook/IPN; trạng thái được quan sát ở billing/reconciliation screens |
| `API-AIX-001`, `API-AIX-002`, `API-AIX-003`, `API-AIX-004`, `API-AIX-005`, `API-AIX-006`, `API-AIX-007`, `API-AIX-008`, `API-AIX-009`, `API-AIX-010` | `SCR-WRK-013`, `SCR-WRK-034`, `SCR-WRK-039`, `SCR-WRK-040`, `SCR-OPS-022`, `SCR-OPS-023` |
| `API-OPS-001`, `API-OPS-002`, `API-OPS-003`, `API-OPS-004`, `API-OPS-005`, `API-OPS-006`, `API-OPS-007`, `API-OPS-008`, `API-OPS-009`, `API-OPS-010` | `SCR-OPS-009`–`SCR-OPS-011`, `SCR-OPS-017`–`SCR-OPS-025` |
| `API-INT-001` | N/A — Study/Work worker reconcile Identity projection |
| `API-INT-002`, `API-INT-003`, `API-INT-004`, `API-INT-005` | N/A — signed asynchronous evidence saga; user sees projection ở `SCR-WRK-019`, recruiter ở `SCR-WRK-040` |
| `API-INT-006`, `API-INT-007` | N/A — signed Identity event consumers |
| `API-INT-008` | N/A — optional provider callback; Ollama pilot dùng worker polling |
| `API-INT-009` | N/A — audited Study repair job, không phải learner CTA |
| `API-INT-010` | N/A — privacy worker deindex; candidate sees state at `SCR-WRK-012` |
| `API-INT-011` | `SCR-WRK-021`, `SCR-WRK-042`; WebSocket chỉ phân phối, REST là nguồn dữ liệu |

## 12. Screen acceptance checklist

Mỗi screen chỉ đạt khi có test desktop/mobile và keyboard cho loading, background refresh, empty, success, validation, `401`, `403`, `404`, `409`, `412`, `429`, `503`, offline/reconnect và retry idempotent tương ứng. Các walkthrough bắt buộc:

1. Auth/session/MFA: register→verify→login; expired/duplicate/resend; lock/suspend; refresh reuse; session revoke; account deletion grace.
2. Study: standalone không onboarding; onboarding→recommendation→primary path; two-switch conflict/cooldown; exact-version course; progress rebuild; quiz/manual assessment; scan pending/infected; two reviewers; trusted publish.
3. Work: private-by-default/opt-in/opt-out <=5 phút; invitation không chat; apply duplicate/revision conflict/Study outage; evidence consent/revocation; ATS conflict/human decision; interview reschedule/no-show; chat reconnect/terminal/assignment revoke.
4. University: affiliation accept/withdraw; consent-expired detail; cohort/program/distribution/referral; report group dưới 10.
5. Payment/promotion: VNPAY và MoMo redirect, pending return, duplicate/out-of-order webhook, mismatch/reconcile/refund/chargeback; entitlement only settled; sponsored label mọi viewport.
6. AI: async success/timeout/DLQ, prompt injection/output blocked, excluded fields, kill switch, human edit/reject; không mutation ATS tự động.
7. Security/privacy: cross-tenant URL, role denial, signed URL expired, MIME spoof/malware, PII analytics redaction, break-glass expiry, legal hold/deletion state.
