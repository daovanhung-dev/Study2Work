# ME-05 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ME-05-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Thông tin bài giảng vừa tạo, file, trạng thái và link về course.
- Gate/status (giữ nguyên): **D**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: 5. State, error and access matrix

| State | Entry condition | Required display/data | Current/API evidence |
|---|---|---|---|
| `loading` | Route ID starts #48 request or retry | Loading status; clear the previous lecture before applying the new ID. | Implemented; route changes cancel stale requests. |
| `ready` | #48 returns 200 and valid `data` | Source-backed lecture fields only; keep null content and empty assets explicit. | Current local API behavior, not deployed/browser verified. |
| `unauthenticated` | #48 returns 401 | Show the Mentor session message; the shared API client ends the local Mentor session on 401. | Source-backed; browser flow not verified. |
| `forbidden` | Wrong role or direct-owner mismatch | Access denied without revealing another Mentor's lecture details. | #48 guard and owner branch return 403. |
| `not-found` | Invalid/out-of-range path, absent row or `DELETED` row | Not-found state. Do not distinguish hidden/tombstoned rows. | #48 currently maps invalid ID and missing/deleted row to 404. |
| `error` | HTTP failure or invalid response envelope/payload | Show safe error copy and retry action; do not render stale or partial lecture data. | Implemented; #48 returns safe server errors. |
| `empty-assets` | #48 succeeds with `assets:[]` | Valid success; asset section may show approved empty state. | Test source verifies empty array; not run in this session. |
| `null-content` | #48 returns `content:null` | Valid response with explicit empty-content copy. | Implemented; T041 sets #47 writes to Markdown strings, while legacy rows may remain null. |

**Authorization/data rules:** API #48 authenticates server-side and does not accept mentor ID from request. Direct knowledge of a lecture ID does not grant access. Never place Bearer tokens in route/query. API #48 filters `DELETED` but does not require `PUBLISHED`; do not hide draft status by assumption. AC-21 assigned-course support is not implemented by this direct-owner source.

### Trích từ DD nguồn: 6. Accessibility and presentation constraints

- The intended Study Web guide calls for responsive reflow below 768px, keyboard-visible focus, accessible names for icon controls, contrast-safe status, and at least 44px hit areas. This mockup's top navigation is hidden at some widths, controls are smaller, and several icon-only controls lack accessible labels in the static markup.
- Player controls need keyboard operation, captions semantics, focus order and reduced-motion support if a media contract is approved. Chapter/timeline status must not rely on color alone.
- Use semantic headings/landmarks, actual buttons/links, descriptive filenames, `aria-live` for copy/download feedback and focus restoration after menus/dialogs; these are implementation requirements, not current HTML behavior.
- Do not ship hardcoded personal identity, comments, metrics, repository URLs or sample lecture/course values as real account data.

### Trích từ DD nguồn: 7. Blockers and acceptance

| ID | Blocker / required decision | Evidence / owner action |
|---|---|---|
| ME05-B01 | Local route, API caller and Mentor token integration are source-wired; deployed route/API behavior is unverified. | Do not claim browser/deployment verification without running it. |
| ME05-B02 | Assigned-course authorization and Mentor identity do not match current direct-owner numeric JWT-sub source. | Resolve AC-21 assignment relation/identity and align #46/#47/#48. |
| ME05-B03 | #48 provides numeric `course_id`, not course name/code. | Current links use the validated ID; a course-name lookup is outside #48 and is not added. |
| ME05-B04 | T041 approves Markdown text in #47 `content:string`; #48 may still return null for legacy rows. | Current UI displays escaped text and an explicit null state; formatted Markdown rendering remains out of scope. |
| ME05-B05 | Status enum and mutation lifecycle are open; #48 is read-only, #47 creates PUBLISHED. | Define allowed states and approved Mentor status API before exposing #14. |
| ME05-B06 | Edit button has no Mentor lecture update API/route. | Approve endpoint/body/validation or remove #15 from production UI. |
| ME05-B07 | Video player, transcript, chapter timing, duration and preview access have no #48 fields or media source. | Define media resource/playback/caption/preview contract; do not use mock player data. |
| ME05-B08 | Asset URL access/download/PDF preview not verified. | Confirm storage URL authorization, MIME/preview, expiry, file naming and error policy. |
| ME05-B09 | Analytics metrics/chart/realtime values have no source in ME-05 contract. | Assign API/data source, metric definitions and freshness or remove #25. |
| ME05-B10 | Discussion cards/reply and ST-25 target lack Mentor route/API; ST-25 is Student-facing. | Define Mentor discussion ownership, route, read/write API and count policy. |
| ME05-B11 | Course tree and previous/current/next lesson rows are not returned by #48. | Define #49/ME-06 relationship or approved lesson-curriculum navigation source. |
| ME05-B12 | API #48 DD remains Draft; legacy schema/migration 005 deployment/live DB, assignment access, status enum and malformed-path policy remain unverified. | Keep source behavior distinct from deployment; Q-48-04's prior #47 decimal-string question is superseded by T041. |
| ME05-B13 | Stitch-only identity, player, analytics, discussion, GitHub, chapter/tree and action values have no #48 source. | Keep these mockup elements out of the implemented detail flow until their contracts/routes are approved. |

### DD acceptance for ME-05

- All 33 markers resolve one-to-one to element rows; all visible interactive controls map to event entries or an explicit blocked/unwired status.
- API #48 field/error/auth/ordering/side-effect claims match source; current API DD and live schema status remain separately stated.
- Approved decisions resolve blockers before calling the UI DD implementable. Until then ME-05 is **not DD READY**.
- The source-backed detail slice is implemented; unsupported Stitch elements remain blocked. `RUNTIME VERIFIED` remains false because no browser route/API deployment was exercised.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
