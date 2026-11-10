# ME-12 — Trao đổi và đóng yêu cầu · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-12` |
| Module | Mentor |
| Route | `/mentor/support/:requestId` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: \| DD status \| DD BLOCKED \|; \| Implementation status \| IMPLEMENTATION BLOCKED \|; \| Runtime status \| RUNTIME NOT VERIFIED \| |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ME-12.md](../../screen_stitch/04_mentor/ME-12_trao-doi-va-dong-yeu-cau/ME-12.md), [ME-12_PLAN.md](../../screen_stitch/04_mentor/ME-12_trao-doi-va-dong-yeu-cau/ME-12_PLAN.md), [ME-12_markers.json](../../screen_stitch/04_mentor/ME-12_trao-doi-va-dong-yeu-cau/ME-12_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Thread message/attachment, reply composer, resolve sau khi đủ điều kiện.
- In-scope: GET #59 → POST #60 reply → reload #59; PATCH #61 resolve sau xác nhận.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-24 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Thread message/attachment, reply composer, resolve sau khi đủ điều kiện. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #59, #60, #61
- Liên kết màn hình dự kiến: [ME-11](../ME-11-HopThuHoTroHocVien/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/ready-empty/ready-thread/replying/resolving/resolved/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-12 source screen.png](../../screen_stitch/04_mentor/ME-12_trao-doi-va-dong-yeu-cau/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-12_trao-doi-va-dong-yeu-cau/screen_annotated.png))
- Luồng: GET #59 → POST #60 reply → reload #59; PATCH #61 resolve sau xác nhận.
- Priority: P2; Gate/source status: **R**; #59–#61 local route/module/query/model/test source-backed, migration 008 local; API DD Draft/DERIVED, live schema chưa verified. **BLOCK:** loaded thread/full-thread scale và attachment UI chưa có thiết kế; counter 2000 khác #60 không max; #61 không enforce tối thiểu một message, AC satisfaction/confirmation chưa chốt; #60 vẫn nhận reply sau RESOLVED/CANCELLED; POST retry không idempotent, GET refresh policy cần thống nhất; Socket/TLS, SLA, auto-settlement/survey là prototype claim; Student producer chưa có; Study Web UNWIRED

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ME-12 — Trao đổi và đóng yêu cầu

| Metadata | Value |
|---|---|
| DD status | DD BLOCKED |
| Implementation status | IMPLEMENTATION BLOCKED |
| Runtime status | RUNTIME NOT VERIFIED |
| Actor | Mentor |
| Screen type | Proposed page |
| Route proposal | /mentor/support/:requestId |
| Related screen | ME-11 Hộp thư hỗ trợ học viên |
| Business trace | AC-24, UC24, F09 |
| API dependencies | #59 detail, #60 reply, #61 resolve |

> Expected behavior comes from the screen inventory and AC-24. Current behavior comes from the checked-in static image/HTML and local Study Server source. Study Web has no app source/package/router and is registered UNWIRED. Local API source and fake-session tests do not prove live database deployment or a running UI.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### A.1. Mục tiêu và phạm vi

ME-12 is the Mentor detail page for one support request. The intended page reads a request thread, lets the Mentor send a reply, and lets the Mentor resolve the request after the learner is satisfied and the current lifecycle state permits resolution. The page is entered from ME-11 with the selected request ID.

The current PNG/HTML only shows the initial empty-thread composition. It contains a loading request-ID placeholder, a static OPEN-looking status, a blank reply box and disabled actions. It does not define how a loaded message thread, attachment preview, message author/time, success state, error state, confirmation prompt, or long thread is laid out. Those states remain design decisions.

### A.2. Actor, preconditions and postconditions

| Item | Specification |
|---|---|
| Actor | Authenticated Mentor whose identity owns the course linked to the request. API source checks Mentor role and direct course ownership against the JWT subject. |
| Preconditions | Expected route has requestId from ME-11 #58 data[].id. Request exists, is in the Mentor's course scope, and the Mentor session is valid. Exact route implementation and session integration do not exist in Study Web. |
| Read postcondition | Request metadata and full ordered message thread are available from #59, or a mapped error/empty-message state is shown. A valid request may have messages: []. |
| Reply postcondition | #60 inserts one message and any permitted attachment links atomically. The API returns the full updated request. Status is preserved by current source. |
| Resolve postcondition | #61 changes an allowed active state to RESOLVED and returns the full request. Repeating resolve on RESOLVED is idempotent in current source. |
| Screen exit | Back action is intended to return to ME-11. Other menu/footer destinations have no confirmed route in the prototype. |

### A.3. Route and screen relationships

- Expected inbound flow: ME-11 calls #58 and passes numeric SupportRequest id from data[].id to /mentor/support/:requestId.
- Expected current-screen flow: route requestId → GET #59 → render detail/thread → POST #60 when reply is permitted → refresh #59 per inventory → PATCH #61 when resolve is permitted.
- Expected return: back button → /mentor/support (ME-11). List-filter restoration is unspecified.
- No Student create-request route/API is present in this flow. Do not add a create-request action from ME-12 or a Student CTA based on this page.
- The static code.html uses href="#" for header, breadcrumb, back, help and footer anchors. It contains no app router binding or API client.

### A.4. Business rules and security

1. The Mentor must have an authenticated Mentor role. Each API checks ownership through the linked course and Mentor identity; UI state is not an authorization boundary.
2. Never trust a request ID or displayed status from the browser. Load from #59 and use server response for state and owner-scoped data.
3. #59 returns the complete thread, ordered by message created_at ascending with id as a tie-break; attachments are ordered by asset_position. The response is unpaginated.
4. #60 requires both message and attachment_refs. attachment_refs is a string containing a JSON array of unique signed int64 upload IDs; the string "[]" means no attachments. Existing UI has no attachment picker.
5. #60 rejects whitespace-only messages but has no source-level maximum length. The screenshot's 2000-character value is not an API rule.
6. #60 currently accepts replies for RESOLVED or CANCELLED requests and preserves their status. Whether the product should allow that remains unapproved.
7. #61 currently resolves OPEN, IN_PROGRESS and WAITING_LEARNER; a RESOLVED retry succeeds without another update; CANCELLED and other unsupported statuses return 422. #61 does not enforce a minimum message count or learner satisfaction.
8. Do not treat Socket/TLS 1.3, 24-hour SLA, automatic settlement, post-resolution satisfaction survey, privacy/source standards or WCAG footer copy as verified product behavior. The APIs do not return or enforce these claims.

### A.5. Current implementation status

| Area | Current evidence | Status |
|---|---|---|
| Screen assets | Original screen.png and code.html exist. HTML is static and has no scripts, API calls, socket, submit handler or route binding. | Static prototype only |
| Study Web application | No Study Web package/source/router is tracked; .agents/context-manifest.json registers study-web as UNWIRED. | UNWIRED |
| API #59–#61 | Routes, module code, tests and API DD packages exist in Study Server. API DDs remain Draft — Needs Confirmation; key local schema/lifecycle choices are DERIVED. | Local source-backed; contract approval/live deployment unverified |
| Database | Migration 008 and local support tables are checked in. Historical tests use fake DB sessions. | Live schema/deployment NOT VERIFIED |
| Screen DD | Plan, marker JSON/SVG, annotated image and this A–F document are present. | DD BLOCKED by open UI/business decisions below |
