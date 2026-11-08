# ME-07 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ME-07-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Editor theo content_type/payload, xác thực dirty state.
- Gate/status (giữ nguyên): **D**; **BLOCK:** PUT #51 chưa mô tả body rõ trong catalog
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: 3. Data mapping and field rules

### Form field mapping

| Field/UI | Create source | Edit source | Request/validation status |
|---|---|---|---|
| `courseId` route | From ME-06 route/context candidate | Same | #50 body requires `course_id`; #51 has no course field. Server derives content’s course for authorization. Route syntax/client parsing is not implemented. |
| `contentId` route | Absent → candidate create mode | Required for candidate edit mode | #49 collection must contain this exact ID and same route course before enabling edit. #51 path takes it; never submit it in body. |
| `title` | Blank form value | From `Content.title` | #50/#51 require a string. Blank/whitespace and max-length rules are not enforced by current model; screenshot indicates required but does not define normalization/limit. |
| `content_type` | Blank select | From `Content.content_type` | APIs require a string but leave it open. HTML option values `theory/reading/practice` are sample values without enum approval. |
| `payload` | No source UI value; must be a JSON object | Current `Content.payload` object from #49 | Required by #50/#51; subtype/schema/editor/asset URI rules are `OPEN`. Placeholder is not payload data. |
| `sort_order` UI / `order` response | #50 generates root order | #49 returns int32 `order`; #51 preserves current order | UI’s positive-number field cannot be written through #50/#51. Create starts at root order 0; reordering/update order needs contract/API. Disable or remove the editable field until approved. |
| `parent_id` | #50 always writes `NULL` | #51 preserves current value | Not in either mutation request. Cannot choose/change parent from this form. |
| `status` / “Lưu bản nháp” | #50 sets `PENDING_REVIEW` | #51 resets current row to `PENDING_REVIEW` | No status field in body. “Draft” label is not a current approved enum mapping. |
| `version` | No initial version returned | #51 writes a prior-state snapshot | No version number/current-version pointer in #49/#50/#51 response; no concurrency token. |

### Error and side-effect boundary

- Do not merge API #50 or #51 into one route. Select method using create/edit mode and `contentId`, then invalidate/reload #49 only after server success.
- Do not pass UI `sort_order`, `parent_id`, session progress, owner, status or version in either request; current Pydantic models forbid undeclared body fields.
- #50 success creates exactly one root Content with server-derived order/status. #51 success creates a version-history snapshot and changes current status/content. Both commit internally in current implementation and return one Content item.
- There is no idempotency key. If a POST times out after the server may have committed, automatic retry can create a duplicate root. A client must not blindly retry ambiguous create failures; the UI retry/resolution policy is open.
- #51’s row lock prevents simultaneous #51 transactions from updating at once but has no optimistic token/409. Do not show a server-backed `conflict` outcome as current behavior; any stale-form warning requires a version/concurrency contract.

### Trích từ DD nguồn: 6. State, security and accessibility matrix

| State | Entry condition | Required UI behavior / evidence |
|---|---|---|
| `create-ready` | No `contentId`; course context available | Blank fields. Save remains disabled until body contract exists; source API can only create a root PENDING_REVIEW Content. |
| `edit-loading` | `contentId` present, #49 in flight | Do not show fixture values as loaded form data. |
| `ready` | #49 contains matching Content | Map current fields; preserve raw status/order/parent/ID. Payload editor is unavailable until subtype contract. |
| `empty` | #49 returns `data:[]` in create context | Treat as valid collection; edit mode resolves to not-found. |
| `dirty` | Any editable field changes | Client state candidate only; current static HTML has no dirty tracking. Cancel/discard behavior is open. |
| `validating` | User attempts save | Validate only approved field/type/payload rules; current client/server do not define all rules. |
| `saving-create` | POST #50 pending | Prevent repeat submit; no automatic retry after ambiguous timeout. |
| `saving-update` | PUT #51 pending | No version precondition; no server 409 conflict semantics. |
| `saved-await-refresh` | #50/#51 success before #49 refresh | Keep response visible; invalidate/reload #49 per inventory. Exact route destination open. |
| `denied` | 401/403 | Distinguish authentication from course ownership; no protected form/save action. Source authorization is direct owner, not assignment. |
| `not-found` | #49 course missing/invalid or edit ID not in result; #51 Content missing | Do not populate sample form; `#51` malformed/missing ID maps 404. |
| `validation-error` | #50/#51 body 422 | Keep local input where safe; field-level error contract and copy not defined. |
| `error` | API 500/network error | Show retry/leave state without claiming save succeeded. Safe backend error has no internal SQL details. |
| `conflict` | Inventory state only | Not source-backed: #51 has no version token/409. Do not claim conflict detection exists until API contract changes. |
| `current-mock-disabled` | Existing code.html | Save has `disabled` and `aria-disabled=true`; this is current static state, not an authorization result. |

Security and accessibility notes:

- Do not rely on `courseId`, UI badge or session-progress panel as access control; #50/#51 perform server checks, currently direct owner. Do not transmit JWT in query strings.
- Treat `payload` as untrusted JSON. Define subtype validation and safe rendering before allowing rich HTML, Markdown, asset URLs or external links.
- The editor header currently has no associated form control; future editor needs a programmatic label, keyboard support, focus order and validation/error association. Input controls should retain visible labels and focus state.
- Current `img` uses `data-alt` rather than `alt`; progress is a plain `div` without progressbar semantics/value. The mockup imports remote Plus Jakarta Sans while the Study Web guide says not to add remote font imports and targets responsive layout/visible focus/44px controls. These are design-source gaps, not runtime claims.

### Trích từ DD nguồn: 7. Discrepancies and decisions required

| Topic | Expected/mockup | Current evidence | Impact/status |
|---|---|---|---|
| Create vs edit route | Optional `contentId` route, shared editor title | No client router; screenshot has empty fields and does not reveal mode | Define distinct entry mode and data precondition. |
| Read before create | Inventory says GET #49 then create/update | #49 can list tree; #50 rechecks ownership; create does not need tree for order because server allocates it | Confirm whether #49 is always loaded or only in edit mode. |
| PUT body | Catalog path only | Code expects strict `{content_type,title,payload}`; API DD #51 says DERIVED/open | Update catalog and approve body before implementation. |
| Title | Mockup required star | API requires string presence but has no nonempty, whitespace or max-length rule | Define trim/length and field error behavior. |
| Type | Three select values | API type open string; no subtype models | Approve enum and each payload schema. |
| Display order | Positive order input and tree-placement guidance | #50 autogenerates root order from 0; #51 preserves order | Remove/disable field or add approved order API; do not send it to current routes. |
| Parent/sections | Text says position within chapter | #50 hardcodes root; #51 preserves parent | Child create/move unsupported by current APIs. |
| Detail editor/media | Rich editor and media area implied | Placeholder only; no asset endpoint in ME-07 inventory; payload shape open | Editor/payload and media flow block the primary screen action. |
| Save status | “Lưu bản nháp” | #50/#51 set `PENDING_REVIEW`; label/status lifecycle not approved | Confirm create/update status and whether save means draft or review submission. |
| Version/conflict | Inventory says `conflict`; AC says Content + version | #51 archives old row; response lacks version; no 409 | Define current revision/version selector and optimistic concurrency, or remove conflict promise. |
| Authorization | AC-22 says Mentor with course-management access | #49–#51 check direct `courses.mentor_id` | Confirm assignment/co-owner authorization; current UI copy overstates domain reconciliation. |
| Session badge/progress | “Đang đối soát”, 2/3 progress | No route/API data source | Remove or map to approved auth/session contract. |
| Live DB/runtime | Content tables exist in repository | DDL/migrations 006/007 local; live migration not verified; Study Web `UNWIRED` | No runtime/deployment claim. |

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
