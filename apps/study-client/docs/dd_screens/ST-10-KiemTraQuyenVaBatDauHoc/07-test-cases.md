# ST-10 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-10-TC-001` | Planning ref / not run | `AC-14` | See source acceptance section | P1 |

## 2. Test planning references

### ST-10-TC-001 — Acceptance planning reference (AC-14)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-10](../../screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/ST-10.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-14`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-10_kiem-tra-quyen-va-bat-dau-hoc/ST-10.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

### Blockers

| ID | Blocker | Owner/decision |
|---|---|---|
| ST10-B01 | ST-09 has no lesson row/selection/lessonId handoff in current assets. | Product/design/frontend |
| ST10-B02 | API #22 has no current source; access predicate, identity binding, allow/reason schema and 404 semantics unresolved. | API/backend/security |
| ST10-B03 | API #23 has no current source; BIGINT and V1-PILOT UUID progress schemas differ, so UPSERT identity/key, repeated start, field preservation, idempotency, response and transaction are unresolved. | API/backend/database |
| ST10-B04 | API #24 has no current source; direct-call authorization, lesson/course publish policy, 403/404, query/projection and null behavior unresolved. Current public #09 also returns lesson `content`/`video_url` without enrollment/auth context. | API/backend/security/product |
| ST10-B05 | Catalog #22/#23/#24 generic Lesson payloads may not match access/start/content responsibilities; #23 could expose content before #24. | API/product/security |
| ST10-B06 | Study Web editable source/router absent; route/auth/navigation/runtime cannot be verified. | Frontend/build owner |
| ST10-B07 | Static 423_LOCKED, Session Token, permanent-lock, release-media and WCAG-compliant claims are not source-backed. | Product/design/security/accessibility |
| ST10-B08 | Inventory orders #23 after allowed access but does not say whether it is automatic or triggered by the Start button; current button is disabled. | Product/design/frontend |

### Acceptance checklist

- [x] Source PNG and HTML preserved; hashes recorded.
- [x] All 21 visible marker IDs have one matching element description.
- [x] Expected and current routes/API behavior are separated.
- [x] All identified route/API/navigation events describe trigger, inputs, order, outputs and current gaps.
- [x] #22–#24 status, auth, path, response and business-code declarations compared with current Study Server source.
- [x] Current public API #09 content/video projection traced so it is not mistaken for #24 authorization.
- [x] Both checked-in Study DDL models compared; neither is asserted as live schema or API #23 mapping.
- [x] AC-14 denied flow explicitly blocks #23/#24/media.
- [x] Upstream ST-09 lessonId gap and downstream ST-11 handoff are recorded.
- [ ] #22 access predicate, JWT binding, allow/reason and 403/404 contract finalized and source-backed.
- [ ] #23 idempotency/upsert key, state updates, transaction and retry rules approved.
- [ ] #24 independent-call authorization, publish policy, response projection/null behavior approved and source-backed.
- [ ] Loaded/checking/denied/failure states and recovery UI designed.
- [ ] Study Web route and auth/API sequence implemented and runtime-verified.
- [ ] ST-11 route and #24 request ownership/duplicate-read sequence reconciled.
- [ ] Design and accessibility claims verified/approved.

**Decision:** DD BLOCKED. Implementation BLOCKED. Runtime NOT VERIFIED. API/design declarations are insufficient to resolve entitlement and protected-content behavior.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 6. Acceptance, blockers and outputs

- Create ST-10.md, ST-10_markers.json, ST-10_markers_overlay.svg, screen_annotated.png after this plan. Preserve original image/HTML.
- DD must cover every visible marker, expected/current handoff, all 10 events, API method/route/auth/path/response/errors/status, state matrix, navigation and security implications.
- Keep status panel/API/business-code discrepancies explicit: 423_LOCKED is not catalogued; #22–#24 are Draft and absent from current source; #22 ApiEnvelope<Lesson> lacks allow/reason field; #23 repeated POST/upsert behavior unresolved; #24 access/publish/content projection unresolved.
- DD is expected to remain BLOCKED until access predicate/JWT mapping, 403 reason shape, 404/422 semantics, #23 unique key/update/idempotency/transaction, #24 authorization/publish/projection/null rules, loaded/error UI and ST-09 lessonId handoff are approved/source-backed.
- Update global tracker to separate DD/implementation/runtime status and increment artifact bundle count only after static audit. Next pointer after this session: ST-11.
- No context page change is planned unless source audit reveals an inaccurate registered page. If a context page changes, update it with evidence and run node scripts/validate-agent-context.mjs.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
