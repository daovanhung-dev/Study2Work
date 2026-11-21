# AD-25 — Business Rules

> **T041 approved-policy update (2026-11-19):** CSV/XLSX/PDF, owner-only UUID Operation with `PENDING|SUCCEEDED|FAILED`, and a one-hour signed artifact URL are approved. This supersedes blocker wording below for those choices only; response field mapping, filter serialization, generic operation persistence/producer and exact artifact/download contract remain open.

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-25-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Chọn format/phạm vi/kỳ, theo dõi export và chỉ tải artifact sau khi có kết quả được xác nhận.
- Current gate/status: **D**; **DD BLOCKED; IMPLEMENTATION PARTIAL; RUNTIME NOT VERIFIED:** AD-25 route/page and Admin session gate are source-wired; #103 has no local route/worker; current #18 source is notification-only and has no export mapping. T041 approves formats and target Operation/artifact policy, but response mapping, filters, producer, artifact/storage/download and AD-24 handoff remain unresolved.
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và quyết định còn mở — historical status snapshot (2026-11-08)

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
| B07 | Implement the T041-approved export Operation policy and its producer/result mapping. | T041 resolves export UUID, owner-only access and `PENDING|SUCCEEDED|FAILED`; current #18 route is notification-only and the catalog row still says int64. | No export poll or SH-07 handoff until #103 and #18 are mapped to the approved UUID/result contract. |
| B08 | Implement artifact result/storage/download handling under the approved link lifetime. | T041 approves one-hour signed URLs; ExportAsset result field, storage service, endpoint, authorization and cleanup are not implemented. | Keep Download disabled; do not claim the mockup's checksum/audit/cache/24-hour cleanup. |
| B09 | Define AD-24 filter transfer and restoration across the existing routes. | AD-24 and AD-25 routes are source-wired; current back link does not pass filters. | No filter query or restoration until its serialization is approved. |
| B10 | Apply the canonical Study Web visual guide. | `.agents/web-study/design.md` is the intended design target; it requires Ocean semantic tokens, system typography, responsive layout and visible focus. | Preserve screenshot as reference; do not carry its cobalt palette or remote font into the implementation. |

### F.3. Status — historical source snapshot (2026-11-08)

- **DD:** `BLOCKED` — unresolved response, filters, formats, authorization, operation/result, storage and AC handoff decisions prevent an implementation-ready behavioral contract.
- **Implementation:** `PARTIAL` — Study Client route/page/Admin session gate are source-wired; #103/export worker, export-specific #18 mapping, artifact storage and download are absent.
- **Runtime:** `NOT VERIFIED` — no browser route or API was exercised. Static artifact checks do not establish deployment or live DB state.
- **Scope completed:** AD-25 only for this session; no subsequent Screen ID authored.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
