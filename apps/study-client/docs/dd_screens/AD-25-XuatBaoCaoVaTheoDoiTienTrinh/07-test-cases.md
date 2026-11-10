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

## 3. Source acceptance / test plan (not run)

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

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Completion and status criteria

- Create marker JSON/overlay/annotated PNG from the exact coordinates above, then visually inspect the final image and adjust the plan first if any marker obscures content.
- Write A–F DD with one row per marker, detailed EV-01…EV-09 behavior/API boundaries, state/navigation matrix, source register and explicit blockers.
- Do not upgrade #103 or #18 from D; do not claim Study Web, API, export, poll or runtime behavior is implemented.
- Planned outcome: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED` until response, ID, permission, filters, storage and flow contracts are approved and code exists.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
