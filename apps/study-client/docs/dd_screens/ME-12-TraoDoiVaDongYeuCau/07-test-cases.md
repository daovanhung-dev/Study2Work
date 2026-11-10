# ME-12 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ME-12-TC-001` | Planning ref / not run | `AC-24` | See source acceptance section | P2 |

## 2. Test planning references

### ME-12-TC-001 — Acceptance planning reference (AC-24)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-12](../../screen_stitch/04_mentor/ME-12_trao-doi-va-dong-yeu-cau/ME-12.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-24`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-12_trao-doi-va-dong-yeu-cau/ME-12.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

### F.1. Static acceptance checklist

- [x] One plan exists before marker map, overlay, annotated image and DD.
- [x] Original screen.png and code.html are retained; source hashes are recorded for static recheck.
- [x] Annotated image has 43 sequential markers and a one-to-one element inventory.
- [x] Sections A–F cover purpose, full flow, element attributes, event input/processing/output/errors, states/navigation and acceptance checks.
- [x] #59, #60 and #61 endpoints, methods, auth, request shapes, response mapping, business codes, ordering and transaction effects are traced to local source/API DD.
- [x] Expected behavior, current code behavior, static prototype claims and unverified runtime/live DB are explicitly separated.
- [ ] Loaded-thread/attachment presentation and behavior are approved.
- [ ] Reply length and counter semantics are approved and consistent with server validation.
- [ ] Reply attachment picker/source/purpose and user-facing attachment policy are approved, or product explicitly confirms no attachments.
- [ ] Resolve confirmation and minimum-exchange gate are reconciled with AC-24 and #61.
- [ ] Post-resolve/cancelled reply behavior is approved and aligned across UI/API.
- [ ] Socket, SLA, auto-settlement, survey, guide destination and compliance claims are either verified or removed/rewritten by the owner.
- [ ] Study Web app route/auth/API wiring exists and is verified.
- [ ] Live schema/migration deployment and production API reachability are verified before runtime release.

### F.2. Traceability and evidence boundary

| Claim/requirement | Source of truth | Current evidence/status |
|---|---|---|
| ME-12 identity, route proposal, related screen, API sequence/states | apps/study-client/docs/list_screen.md row 52; F09 | Expected design; no app route source. |
| Mentor support decision | apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio AC-24 and UC24 | Expected AC: owned request; resolve if learner is satisfied, otherwise keep OPEN. AC does not specify modal, message minimum or full lifecycle. |
| ME-11 ID handoff | apps/study-client/docs/screen_stitch/04_mentor/ME-11_hop-thu-ho-tro-hoc-vien/ME-11.md and API #58 models | Expected data[].id handoff; static UI does not execute it. |
| Screen content and current controls | This folder's screen.png and code.html | Static prototype; no script, request, socket, form handler or route binding. |
| #59 detail request/response/ownership/thread order | apps/study-server/app/api/v1.py; app/modules/mentor/api_59_mentor_support_request_detail/{models,validate,query,view}.py; _shared/support_request_projection.py | Local route/source/test evidence; exact contract remains Draft and local data assumptions are DERIVED. |
| #60 reply body/validation/transaction | apps/study-server/app/api/v1.py; app/modules/mentor/api_60_mentor_support_reply/{models,validate,query,view}.py; tests/modules/mentor/api_60_mentor_support_reply/test_mentor_support_reply.py | Local implementation; no max length/idempotency; permits post-resolve/cancelled reply. Fake DB tests do not prove deployed database behavior. |
| #61 resolve state/transaction | apps/study-server/app/api/v1.py; app/modules/mentor/api_61_mentor_support_resolve/{models,validate,query,view}.py; tests/modules/mentor/api_61_mentor_support_resolve/test_mentor_support_resolve.py | Local implementation; lifecycle is DERIVED and differs from AC detail. |
| API contract decisions | apps/study-server/docs/dd/59_mentor_support_request_detail, 60_mentor_support_reply, 61_mentor_support_resolve and each OPEN_QUESTIONS.md | All Draft — Needs Confirmation. |
| Local database schema evidence | infra/postgres/study-server/migrations/008_support_requests.sql and Study Server DB DDL | Checked-in local schema only; live schema/deployment unverified. |
| Study Web runtime status | .agents/context-manifest.json scopes.web-work.subcontexts.study-web; apps/study-client tree | study-web is UNWIRED; no tracked app package/router/source. |

### F.3. Open decisions / blockers

| ID | Decision needed | Evidence/discrepancy | Owner to resolve | Effect |
|---|---|---|---|---|
| ME12-B01 | Define loaded thread, message metadata, attachments, responsive layout and behavior for large threads. | #59 returns the full thread without pagination; screenshot only shows an empty state. | Product/UX + frontend/API | DD and implementation blocked. |
| ME12-B02 | Approve reply maximum, Unicode counting rule, counter behavior and validation text. | Mockup says 2000; #60 has no max-length validation. | Product/BA + API owner | Do not hard-limit input based on mockup. |
| ME12-B03 | Decide whether replies support attachments and specify picker/upload contract. | #60 requires attachment_refs string; current composer has no picker; #60 expects LECTURE upload purpose. | Product/BA + API owner | Cannot design attachment reply UI. |
| ME12-B04 | Define satisfaction confirmation and minimum valid-exchange gate before resolve. | AC-24 says resolve when learner is satisfied; mockup requires one exchange; #61 has no minimum-message rule or confirmation payload. | Product/BA + API owner | Keep resolve unavailable until reconciled. |
| ME12-B05 | Decide replies on RESOLVED/CANCELLED requests. | #60 source accepts and preserves status; UI may be expected to lock after resolve. | Product/BA + API owner | Reply enablement cannot be finalized. |
| ME12-B06 | Confirm whether GET #59 must always follow successful POST #60. | Inventory requires reload; #60 already returns full updated SupportRequest. | Frontend/API owner | Impacts request count and stale-refresh handling. |
| ME12-B07 | Verify/remove static Socket/TLS, 24-hour SLA, automatic settlement, survey, privacy/reference and WCAG claims. | No supporting field/side effect in #59–#61; no UI runtime source. | Product/compliance/platform owners | Prototype copy cannot be treated as verified behavior. |
| ME12-B08 | Confirm guide/header/footer destinations and list-state restoration. | Static anchors use href="#"; route contract absent. | Product/frontend | Navigation cannot be implemented reliably. |
| ME12-B09 | Approve local fallback schema/lifecycle and confirm live migration/deployment. | API DD #59–#61 are Draft and identify DERIVED fields/status rules; tests use fake DB. | API/DB owner | API/local source does not prove deployed behavior. |

### F.4. Final status decision

DD BLOCKED because material presentation and business decisions remain open. IMPLEMENTATION BLOCKED because Study Web is UNWIRED and required lifecycle/attachment/UI contracts are unresolved. RUNTIME NOT VERIFIED because no runnable Study Web app or live API/database evidence exists in this scope.

#### Kế hoạch kiểm chứng từ source PLAN

> CẦN_XÁC_NHẬN: Plan nguồn không có section verification/test được nhận diện.


- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
