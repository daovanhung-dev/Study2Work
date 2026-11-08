# AD-09 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-09-TC-001` | Planning ref / not run | `AC-32` | See source acceptance section | P2 |

## 2. Test planning references

### AD-09-TC-001 — Acceptance planning reference (AC-32)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-09](../../screen_stitch/05_admin/AD-09_thay-doi-trang-thai-xoa-khoa/AD-09.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-32`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-09_thay-doi-trang-thai-xoa-khoa/AD-09.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và blocker

### Checklist

- [x] Original screenshot and HTML preserved; hashes recorded.
- [x] 38 ordered markers and matching DD rows cover the visible screen elements/options/actions.
- [x] Native radio-only behavior, disabled textarea/Confirm, static claims and broken back/cancel destination are documented separately from runtime.
- [x] AC-32 and #74/#76/#77 catalog, DD/open questions, route/model/validator/view/query/test source and candidate DDL were reviewed.
- [x] Status and delete branches, auth/path/body/effects/response/errors and transaction boundaries traced.
- [x] API body/enum, archive mapping, hard-vs-soft delete, dependency coverage, audit reason, permission/schema, deleted visibility/restore and Study Web wiring remain explicit.
- [ ] Owner approves #76 enum/body/transitions/learner effects and AC-32 permission mapping.
- [ ] Owner approves #77 deletion marker/dependencies/repeat/audit/lifecycle policy and confirms live schema/deployment.
- [ ] Study Web route/client/navigation/error/loading/reload flow is implemented and runtime verified.

### Blockers

1. Catalog/AC omit #76 body and status enum; local values/transition behavior are `DERIVED`; mockup `archive` cannot map.
2. Local #77 soft-deletes while the mockup claims permanent irreversible deletion. Dependency set, repeat-delete 404, restore/visibility and delete audit remain open.
3. Mockup reason/ISO-27001 requirement is not in #76/#77 body or local audit data model.
4. AC-32 fine-grained course-management permission is not implemented by local shared `ADMIN` guard. Legacy BIGINT and V1-PILOT UUID/versioned schema differ; live DB/deployment unverified.
5. No Study Web route/client. Target-course loading, correct AD-07 return, post-mutation GET/revalidation and API error/session states are not implemented.
6. Mockup enrollment/RBAC/protection/lifetime-retention claims are static. #74 counters are absent; #77's dependency check does not define a complete owner-approved policy.

**Completion decision:** The screen DD records the evidence and open decisions, but cannot be `DD READY` while body/enum, delete policy, permission, persistence and navigation decisions remain unresolved. Final screen status: **DD BLOCKED** · **IMPLEMENTATION BLOCKED** · **RUNTIME NOT VERIFIED**. Local API #76/#77 source status can be `R`; their API DDs remain Draft.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Execution and verification order

1. [x] Docs preflight; read three exact-type worklogs and AD-08 cross-screen handoff; load project/scope/context and registry.
2. [x] Review AD-09 assets/DOM, inventory, AC-32, API catalog/DD/source/tests, #73/#74 handoff and schema candidates; record expected/current discrepancies in worklog.
3. [x] Write this plan before markers, annotation or screen DD.
4. [x] Create ordered marker JSON/SVG and 2× annotated PNG; visually inspect marker placement.
5. [x] Author A–F DD with one row per marker, event sequence, API/error matrix, state/navigation matrix and blockers.
6. [x] Update AD-09 inventory and reverse API source status for #76/#77; update global tracker/checkpoint.
7. [x] Static audit hashes/dimensions, JSON/XML, marker order/bounds and C-row bijection, links, screen ID/folder/core-artifact counts, whitespace and final image. Do not run application tests/runtime.
8. [x] Finalize worklog; stop after AD-09.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
