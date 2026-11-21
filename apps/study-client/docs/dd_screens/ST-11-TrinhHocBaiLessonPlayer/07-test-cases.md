# ST-11 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-11-TC-001` | Planning ref / not run | `AC-14` | See source acceptance section | P1 |
| `ST-11-TC-002` | Planning ref / not run | `AC-15` | See source acceptance section | P1 |

## 2. Test planning references

### ST-11-TC-001 — Acceptance planning reference (AC-14)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-11](../../screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/ST-11.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-14`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/ST-11.md).
### ST-11-TC-002 — Acceptance planning reference (AC-15)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-11](../../screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/ST-11.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-15`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/ST-11.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và blockers

### Blockers

| ID | Blocker | Owner/decision |
|---|---|---|
| ST11-B01 | Inventory says player but supplied screenshot/HTML is only unavailable fallback; no loaded/player design or progress/resource/Next controls. | Product/design |
| ST11-B02 | ST-10/ST-11 both list #24; request owner/response handoff/cache and duplicate-fetch policy unresolved. | Product/frontend/API |
| ST11-B03 | ST-09/ST-10 do not currently provide lessonId; Study Web route/auth/router absent. | Product/frontend |
| ST11-B04 | API #24 absent from runtime; entitlement/JWT binding, publish scope, 403/404, payload/null/path and media URL access unresolved. | API/backend/security |
| ST11-B05 | API #25 absent; neither lesson-progress candidate maps `position`/`percent` as requested (a separate block-level `last_position_seconds` is not lesson mapping); percent/range, completion state, identity/upsert key, aggregate, transaction, autosave/throttle/retry/idempotency unresolved. | API/backend/database/product |
| ST11-B06 | API #26 absent; `ApiEnvelope<Lesson>` conflicts with Resource use-case; response cardinality/order/empty, entitlement, visibility, signed URL policy and URL owner unresolved. | API/backend/security/storage |
| ST11-B07 | API #27 absent; curriculum scope/order/tie-break, direct auth, 403/404, payload and last-lesson semantics unresolved. | API/backend/product |
| ST11-B08 | No Student route/module/query/focused test for #24–#27; Admin #82–#86 are not substitutes; Study Web remains UNWIRED. | Frontend/backend/build owner |
| ST11-B09 | Playback engine/control/accessibility/media security and error/loading/recovery UI are not designed or source-backed. | Product/design/frontend/security |

### Acceptance checklist

- [x] Original PNG and HTML hashes recorded; source files preserved.
- [x] All 14 visible marker groups have exactly one matching DD element row.
- [x] Expected inventory/AC behavior is separated from current static fallback behavior.
- [x] All declared APIs #24–#27 include method/path/auth/input/response/status and current source status.
- [x] Progress body fields and #25/#26/#27 contract mismatches/open questions are traced.
- [x] ST-10 duplicate #24 request and missing lessonId handoff are explicit.
- [x] Current links and absence of media/player/progress/resources/Next controls are documented.
- [ ] Loaded player, loading/error/denied/finished states and recovery UI approved/designed.
- [ ] #24–#27 canonical API rules, error mapping, auth, schema, update/URL/order semantics approved and source-backed.
- [ ] ST-10/ST-11 #24 ownership and lessonId handoff resolved.
- [ ] Progress throttle/autosave/position/completion/aggregate/retry/idempotency policy approved.
- [ ] Study Web route/player/API wiring and ST-12/13/17 navigation implemented and runtime-verified.
- [ ] Accessibility, media URL/security and responsive behavior verified in runtime.

**Decision:** DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED. Current artifacts do not define an implementable loaded lesson player, and API declarations do not close the progress/security contract.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 5. DD contents, blockers and acceptance

- DD will contain overview/evidence, expected vs current flow, Mermaid sequence with unresolved decisions, 14-element mapping, 8 event contracts, API/security matrix for #24–#27, state/navigation matrix, design/accessibility observations, blockers and acceptance checklist.
- Blockers to retain: fallback vs player design; ST-10/ST-11 #24 ownership; missing ST-09 lessonId and Study Web route/auth; no current #24–#27 Student APIs/tests; entitlement/JWT/publish/error rules; #25 position/range/state/upsert/aggregate/autosave; #26 Resource payload/cardinality/visibility/signed URL; #27 order/tie-break/no-next/404; no player/media URL/security/accessibility contract; loaded/error/recovery/player controls absent.
- DD READY is not expected from current evidence. Status remains **DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED** until canonical design/API decisions and sources close these items.
- No tests/runtime calls are requested. Static verification after authoring: source hashes unchanged; dimensions; marker IDs sequential/unique and matching DD; SVG circles/embedded source bytes; local links; visual review; `git diff --check`; tracker/worklog.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
