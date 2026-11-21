# ME-08 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ME-08-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Review cảnh báo dependency, xác nhận publish/unpublish hoặc xóa.
- Gate/status (giữ nguyên): **D**; **BLOCK:** Publish state machine và delete dependency cần chốt
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: 6. State, security, responsive and accessibility matrix

| State | Entry condition | Required handling/evidence |
|---|---|---|
| `route-loading` | ME-08 opened with Content ID | Resolve course context and request lifecycle; no selected Content is present in current asset. |
| `hydrating` | #49 request in flight | Do not display sample DRAFT/status as loaded content. |
| `ready` | Exact active Content appears in #49 for same course | Display raw current fields; no permission or allowed-transition field is available. Actions remain blocked until policy/body and UX are approved. |
| `not-found` | Course #49 returns 404, list is empty for target, or target is absent/soft-deleted | Do not hydrate from screenshot; distinguish course API 404 from locally absent Content. |
| `denied` | 401/403 | No action; source checks role and direct owner. AC-22 assigned-course policy may differ. |
| `confirm-publish` | Publish intent selected | Confirmation control/copy is not in source asset. No request before an explicit confirmed target. |
| `confirm-unpublish` | Unpublish intent selected | No current control; state transition is DERIVED. |
| `confirm-delete` | Delete intent selected | Confirmation dialog is a candidate; dependency effect list is incomplete. |
| `publishing` / `unpublishing` | #52 pending | Prevent repeated clicks. Current `#52` same-target is idempotent, but body contract remains unapproved. |
| `deleting` | #53 pending | Prevent repeated clicks; no blind retry after ambiguous timeout. |
| `blocked` | #52/#53 returns 422 | Show specific approved status/dependency explanation; current backend text can say unsupported transition, PUBLISHED must be unpublished, or active child blocks deletion. Client copy/policy is open. |
| `success-await-refresh` | Mutation is 200 but #49 refresh has not succeeded | Mutation success remains distinct from refresh failure. Keep `courseId` for refresh. |
| `success` | Mutation + refresh succeed | Return to ME-06 using its course route/context; no runtime implementation exists. |
| `error` | Network or 500 | No success claim. Reconcile ambiguous mutations through #49 when `courseId` is available; retry policy is not cataloged. |

**Security:** Do not trust the static security badges or `courseId` supplied by the client. #49/#52/#53 each authenticate the Mentor and perform current server-side direct-owner checks. Do not expose JWT in route/query. Do not infer assignment/co-owner rights from the copy “quyền quản lý khóa học”. The backend must remain the final authorization boundary.

**Data safety:** Treat `payload` as opaque JSON at this screen; ME-08 must not parse or use it to calculate impact without a schema. #53 does not validate external references. Do not claim retention of learner progress or certificate recalculation unless a source-backed contract covers those records.

**Responsive/accessibility:** Current HTML marks buttons disabled and includes `aria-disabled`; no action dialog, focus trap, live-region response, confirmation focus management, error association or loading state is wired. For a future approved confirmation flow, label the exact target/action, announce processing/results, preserve keyboard focus, make destructive intent explicit and provide visible focus/44px controls. Current mockup uses a 1440px content maximum and imports remote Plus Jakarta Sans/Material Symbols; Study Web design guide targets about 1120px responsive content, system/available Inter fonts, reflow below 768px and no remote font imports. The WCAG badges in the image are not accessibility evidence.

### Trích từ DD nguồn: 7. Discrepancies and decisions required

| Topic | Expected/mockup | Current evidence | Impact/status |
|---|---|---|---|
| Page vs dialog | Inventory classifies Dialog; source is a full page with header/footer. | No modal overlay. | Product/design must confirm presentation. |
| Target selection/hydration | Route has `contentId`; mockup says choose from tree but has no picker/selected item. | #49 is course collection only; ME-08 route omits `courseId`. | Define ME-06 → ME-08 state handoff and no-detail lookup. |
| #52 request body | Catalog/AC path only; action text includes publish/unpublish. | Strict source `{published:boolean}`; body is DERIVED. | Approve request or change canonical source/catalog; do not send undocumented body as finalized. |
| Lifecycle/readiness | Mockup says draft/publish; inventory says publish/unpublish. | Local code only supports APPROVED↔PUBLISHED; APPROVED is only gate. #50/#51 use PENDING_REVIEW. AC-33 approval semantics overlap. | Resolve state machine, Admin approval relation, readiness and public-reader behavior. |
| Unpublish control | Inventory requires publish/unpublish. | Screenshot has only disabled publish button. | Add/confirm the affordance and separate explicit target from toggle. |
| #53 delete policy | “If permitted”, dependency warning; copy claims online submissions block deletion. | Source checks exact PUBLISHED and active direct Content child only; other non-PUBLISHED statuses pass; no learner/dependency queries. | Approve eligible statuses, dependency inventory, child and transitive-tree policy, audit/retention/queue effect. |
| Publish then delete | Mockup may suggest one lifecycle flow. | Current source needs a separate unpublish commit before DELETE on PUBLISHED; later delete can still fail. | Do not auto-chain; define partial-success/confirmation behavior. |
| Refresh context | F08 requires #49 reload after mutation. | #49 requires course ID; #53 result omits it and proposed route carries only content ID. | Preserve courseId via an approved ME-06 navigation contract. |
| Claims and audit | Student impact, certificate update, attendance/submission retention, audit row, production/region/Safe Mode. | No corresponding data/effects in #49/#52/#53. | Remove or source/approve before implementation; do not treat as current. |
| Direct owner vs course permission | AC-22 says Mentor may manage course. | #49/#52/#53 compare numeric JWT subject to `courses.mentor_id`. | Confirm assigned-Mentor identity/access policy. |
| Live schema/runtime | Local source and migrations exist. | No Study Web route, deployed API or live DB verification. | Runtime remains NOT VERIFIED. |

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
