# AD-25 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-25-TC-001` | Planning ref / not run | `AC-38` | See source acceptance section | P2 |

## 2. Test planning references

### AD-25-TC-001 — Acceptance planning reference (AC-38)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-25](../../screen_stitch/05_admin/AD-25_xuat-bao-cao-va-theo-doi-tien-trinh/AD-25.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-38`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-25_xuat-bao-cao-va-theo-doi-tien-trinh/AD-25.md).

## 3. Source acceptance / test plan (not run; historical snapshot 2026-11-08)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và quyết định còn mở

### F.1. DD artifact acceptance checklist

- [x] AD-25 plan saved before marker JSON, annotation and DD.
- [x] Original `screen.png` and `code.html` retained; their recorded hashes are in this DD and plan.
- [x] Elements are indexed #1–#46; one element row maps to each `AD25-EL-01`…`AD25-EL-46` marker.
- [x] Expected flow, current static behavior, AC/API/runtime boundaries and source links are recorded separately.
- [x] EV-01…EV-09, current state, candidate API boundary, error/retry gaps and navigation gates are documented.
- [x] DD, implementation and runtime status are reported separately.
- [x] Static verification complete: marker geometry/IDs/coordinates, JSON/SVG parse, image dimensions/visual review, relative links, unchanged source hashes, inventory/index consistency and `git diff --check`.

### F.2. Blockers trước implementation

| ID | Decision required | Owner/evidence needed | Until resolved |
|---|---|---|---|
| B01 | Chốt #103 202 response: `ApiEnvelope<Report>` hay `Operation`; field chứa ID/type and error mapping. | API/product contract owner; reconcile catalog endpoint row, Operation tracking prose, API #103 DD and AC-38. | Không parse pollable operation or show accepted job details. |
| B02 | Chốt #103 GET side effect, idempotency, duplicate submit and retry/caching semantics. | API/security/product owners. | Không implement automatic retry or imply GET is safe/idempotent. |
| B03 | Chốt filter serialization and relationship to #102 `from/to/segment`, AD-24 URL state, checkbox scopes and period presets. | Reporting/product and API #102/#103 owners. | Không construct `filters` or claim exported report matches dashboard filters. |
| B04 | Chốt format default/case, MIME/extension and unsupported-format response. | T041 approves CSV/XLSX/PDF; catalog still declares `format?:string`. | Do not infer default, MIME/extension mapping or validation response. |
| B05 | Chốt report/analytics authorization policy, claims and consistency with Admin role. | Security/product/API owner; AC-38 precondition vs #103 row and current guard. | Do not treat Admin badge or generic ADMIN guard capability as authorization proof. |
| B06 | Chốt AC-38 edge and whether/how #18 is used by export. | AC/API owners; diagram has unconnected status node while inventory implies conditional handoff. | No SH-07 navigation/polling. |
| B07 | Implement the T041-approved export Operation policy and producer/result mapping. | T041 resolves export UUID, owner-only access and `PENDING|SUCCEEDED|FAILED`; current #18 route is notification-only and catalog row says int64. | No export poll or SH-07 handoff until #103/#18 map the approved UUID/result. |
| B08 | Implement artifact result/storage/download handling under the approved link lifetime. | T041 approves one-hour signed URLs; ExportAsset result field, storage service and download route are not implemented. | Keep Download disabled and do not claim mockup-only security controls. |
| B09 | Define AD-24 filter transfer and restoration across existing routes. | AD-24/AD-25 routes are source-wired; current back link passes no filters. | Do not serialize or restore filters until approved. |
| B10 | Apply the canonical Study Web visual guide. | `.agents/web-study/design.md` specifies Ocean tokens, system typography, responsive layout and visible focus. | Preserve the screenshot as a reference; do not use its cobalt palette or remote font. |

### F.3. Status

- **DD:** `BLOCKED` — unresolved response, filters, formats, authorization, operation/result, storage and AC handoff decisions prevent an implementation-ready behavioral contract.
- **Implementation:** `PARTIAL` — the AD-25 route/page and Admin session gate are source-wired; #103/export worker, report #18 mapping, artifact storage and download are absent.
- **Runtime:** `NOT VERIFIED` — no browser route or API was exercised. Static artifact checks do not establish deployment or live DB state.
- **Scope completed:** AD-25 only for this session; no subsequent Screen ID authored.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Completion and status criteria

- Create marker JSON/overlay/annotated PNG from the exact coordinates above, then visually inspect the final image and adjust the plan first if any marker obscures content.
- Write A–F DD with one row per marker, detailed EV-01…EV-09 behavior/API boundaries, state/navigation matrix, source register and explicit blockers.
- Do not mark #103 or an export-specific #18 flow as wired; do not claim export submission, polling, artifact delivery or runtime behavior is implemented.
- Current outcome: `DD BLOCKED`; `IMPLEMENTATION PARTIAL`; `RUNTIME NOT VERIFIED`. The route/page/session gate exist, while export submission, polling and artifact delivery remain unavailable until their contracts and source exist.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
