# AD-25 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `AD-25-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Chọn format/phạm vi/kỳ, theo dõi export và chỉ tải artifact sau khi có kết quả được xác nhận.
- Gate/status (giữ nguyên): **D**; **DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #103/#18 catalog/Draft-only, no local route/query/model/test/worker/download source; response, GET retry, filter/format, permission, operation ID/access/status/result, AC-38 poll edge, storage/download and AD-24 filter handoff unresolved; Study Web UNWIRED
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

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
| B04 | Chốt allowed format enum, case/default, MIME/extension and unsupported-format response. | Reporting/API owner; catalog currently only `string`. | UI options are prototype-only; no client validation/API mapping. |
| B05 | Chốt report/analytics authorization policy, claims and consistency with Admin role. | Security/product/API owner; AC-38 precondition vs #103 row and current guard. | Do not treat Admin badge or generic ADMIN guard capability as authorization proof. |
| B06 | Chốt AC-38 edge and whether/how #18 is used by export. | AC/API owners; diagram has unconnected status node while inventory implies conditional handoff. | No SH-07 navigation/polling. |
| B07 | Chốt #18 ID type, ownership/access, status enum/lifecycle, terminal states, result/error schemas, persistence and retention. | API #18 owner; catalog row int64 vs UUID schema/AC; owner-only vs owner/Admin. | No operation ID coercion, poll loop or state mapping. |
| B08 | Chốt export artifact ownership/schema/storage/download endpoint, URL policy, expiry, cache, checksum, audit and cleanup. | API/storage/security owners; inventory says download only with result URL; generic pilot tables are candidates only. | Download remains unavailable; static claims remain unsupported. |
| B09 | Chốt actual Study Web route/shell, AD-24 return and filter-state continuity. | Web product/router owner; no current Study Web source. | Candidate route/link is not an implementation contract. |
| B10 | Chốt visual source-of-truth between screenshot and Study Web design guide. | Design owner. | Preserve screenshot; use canonical guide only after design decision. |

### F.3. Status

- **DD:** `BLOCKED` — unresolved response, filters, formats, authorization, operation/result, storage and AC handoff decisions prevent an implementation-ready behavioral contract.
- **Implementation:** `BLOCKED` — Study Web route/client and Study API #103/#18/export/download source are absent; worker/storage flow is not wired.
- **Runtime:** `NOT VERIFIED` — no browser route or API was exercised. Static artifact checks do not establish deployment or live DB state.
- **Scope completed:** AD-25 only for this session; no subsequent Screen ID authored.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
