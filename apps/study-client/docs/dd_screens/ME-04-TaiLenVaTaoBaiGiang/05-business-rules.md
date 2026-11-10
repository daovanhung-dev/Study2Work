# ME-04 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ME-04-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Form lecture metadata, sắp xếp thứ tự, đính kèm media.
- Gate/status (giữ nguyên): **D**; **BLOCK:** Schema lecture.content và asset refs còn ambiguity
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: 6. Điều hướng, bảo mật và dữ liệu

- **Route input:** `courseId` is expected to be a signed-int64 numeric DB/API ID. The screenshot's alphanumeric code is unsupported in current #46/#47 schemas.
- **Authorization:** rely on server MENTOR guard. Client-only role or course selection cannot authorize access. Current #46/#34/#47 use direct owner; AC assignment path is not supported by those predicates.
- **Asset isolation:** never accept `owner_id`, URL, `content_type`, `size_bytes` or `status` from the client as authoritative #47 asset metadata. Upload via #34 and submit returned IDs only; server re-resolves owner/purpose/course.
- **Side effects:** #34 object+metadata persist before #47. #47 atomically writes lesson and relation rows locally. These are not one cross-request transaction.
- **Sensitive files:** API #34 currently returns a URL from configured public base; link access semantics/expiry and actual storage policy were not verified. Do not claim private/signed playback from screenshot text.
- **No synthetic values:** do not save sample module/order, duration, rating/QA, course code, encoding status, preview/prerequisite or Draft status until their source/contract exists.

### Trích từ DD nguồn: 7. UI/accessibility target

Use [`Study Web design guide`](../../../../../.agents/web-study/design.md) as intended UI target, not runtime evidence. Apply Ocean semantic tokens, Inter if already available or system sans-serif, responsive gutters/content width, visible focus, semantic controls, reduced-motion support and clear inline errors. The supplied mockup loads remote Plus Jakarta Sans/Tailwind and several toolbar/icon controls are 28–42 px, below the guide's 44 px minimum. The dense two-column form also needs mobile reflow, keyboard accessible file selection/drop fallback, announced upload progress/errors, and status copy that does not rely on color or a percent badge. These are implementation/design gaps; no frontend code was changed.

### Trích từ DD nguồn: 8. Blockers và quyết định còn mở

| ID | Blocker | Evidence / quyết định cần có |
|---|---|---|
| ME04-B01 | Ownership/assignment | AC-21 allows assigned Mentor; #46/#34/#47 require direct owner. Product/API owner resolves allowed relation and permission. |
| ME04-B02 | Course context | #46 pagination and no detail-by-ID; define direct-entry lookup and how to map numeric ID vs displayed code and module structure. |
| ME04-B03 | Content editor contract | #47 `content:int64` is stored as decimal text; define rich-text/code serialization or a new approved API/data model. |
| ME04-B04 | Lifecycle | UI Draft/review/Publish vs #47 immediate PUBLISHED. Define states, review gate and preview behavior. |
| ME04-B05 | Module/order | Define module hierarchy, order source, uniqueness/range/next-order behavior. |
| ME04-B06 | Unsupported metadata | Define persistence for duration, lesson type, stream URL, guest preview, prerequisites and QA checks/results. |
| ME04-B07 | Upload type/size | Reconcile mockup 2 GB/media allowlist with #34 arbitrary bytes/MIME and no app cap; define UI/storage limits and feedback. |
| ME04-B08 | Asset lifecycle/idempotency | Define delete/cleanup of uploads, cancel/remove semantics, ambiguous #34/#47 retry and orphan retention. No delete route currently found. |
| ME04-B09 | Study Web app | Editable source, route/auth/API client, responsive UI and runtime state wiring are absent. |
| ME04-B10 | Live database/storage | Verify target legacy schema and migrations 004/005, Object Storage configuration/access, and actual endpoint deployment. |
| ME04-B11 | Visual/accessibility | Reconcile mockup font/control size and dense responsive form with Study design target; approve implementation layout. |

### Status gate

| Status | Kết quả | Lý do |
|---|---|---|
| `DD READY` | **NO — `DD BLOCKED`** | Main content mapping, lifecycle, access, course structure and supported fields unresolved. Source-backed API behavior and blockers are recorded, but implementation decisions are still required. |
| `IMPLEMENTATION BLOCKED` | **YES** | UI source absent and screen requirements cannot map to current #47 body/state semantics. |
| `RUNTIME VERIFIED` | **NO — `RUNTIME NOT VERIFIED`** | No Study Web route/serving/runtime was available or run; API test source and prior local reports do not prove deployment. |

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
