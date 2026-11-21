# ST-09 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-09-TC-001` | Planning ref / not run | `AC-13` | See source acceptance section | P1 |
| `ST-09-TC-002` | Planning ref / not run | `AC-18` | See source acceptance section | P1 |

## 2. Test planning references

### ST-09-TC-001 — Acceptance planning reference (AC-13)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-09](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/ST-09.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-13`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/ST-09.md).
### ST-09-TC-002 — Acceptance planning reference (AC-18)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-09](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/ST-09.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-18`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/ST-09.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Blockers và tiêu chí nghiệm thu

### Blockers

| ID | Blocker | Owner/decision needed |
|---|---|---|
| ST09-B01 | API #20 route/module/test absent; response ApiEnvelope<UserProfile> không biểu diễn course membership; status/paging semantics chưa chốt. | API/backend/Product |
| ST09-B02 | API #37 route/module/test absent; response type, aggregate formula, zero/partial/completion semantics chưa định nghĩa. | API/backend/Product |
| ST09-B03 | API #09 public current projection includes lesson content/video_url and has no enrollment/access check. | Backend/security/product: approve public projection or define protected access contract |
| ST09-B04 | APIs #22–#24 absent; lesson access/start/content sequence and error semantics unresolved. | Backend/product |
| ST09-B05 | Expected loaded course/lesson/progress states and controls absent from PNG/HTML; ST-21 control absent. | Product/design |
| ST09-B06 | Study Web editable source/router absent; ignored dist root-only, provenance/serving unknown. | Frontend/build/deployment owner |
| ST09-B07 | ST-08 course card handoff and route guards/session behavior unverified. | Frontend/product |
| ST09-B08 | HTML’s static API badge, token/accessibility claims disagree with source/guidance; CTA lacks lessonId; footer/legal destinations unresolved. | Product/design/frontend |
| ST09-B09 | API #09 declares `course_id:int64`, but the source validator does not explicitly enforce signed-int64 bounds. | API/backend: align path-range behavior with the declared contract |

### Acceptance checklist

- [x] 20 visual marker IDs have one-to-one element descriptions in the same order.
- [x] Original screen.png remains unchanged; HTML source remains unchanged.
- [x] Main route, actors, relationships and evidence states are recorded.
- [x] All identified static and expected events have input, processing, output and gaps described.
- [x] #09 is traced against current route/module/query/model/test source; test source read, not run.
- [x] #20/#37 and #22–#24 are distinctly marked NOT_FOUND in current source.
- [x] Authorization risk and public #09 payload are documented.
- [x] API #09's current registered source is distinguished from its Draft DD and stale mockup badge; path-range discrepancy is recorded.
- [ ] Loaded course tree, per-lesson progress, loading/empty/error states are designed and approved.
- [ ] API #20/#37 payload, rules and error contracts are finalized and source-backed.
- [ ] Lesson access/start/content APIs and ST-10 handoff are finalized.
- [ ] ST-21 navigation control and progress formula are finalized.
- [ ] Study Web route/session/API integration is implemented and runtime-verified.
- [ ] Design-system and accessibility discrepancies are resolved or explicitly approved.

**Decision:** DD BLOCKED; not implementable without product/API decisions in B01–B05 and B09. Implementation BLOCKED by missing frontend and backend wiring. Runtime NOT VERIFIED.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 6. Outputs, acceptance and blockers

- Done: `ST-09.md`, `ST-09_markers.json`, `ST-09_markers_overlay.svg`, and `screen_annotated.png` created after this plan. Original `screen.png` and `code.html` hashes are preserved.
- DD covers 20 visible element groups, 10 identified events, current/expected flow, #09/#20/#37 contracts and source state, state/navigation/access matrix, privacy/security, design/accessibility discrepancies, blockers and checklist.
- Done: context pages describe the ignored compiled root-only `dist` artifact separately from absent editable source while retaining Study Web `UNWIRED` for feature routes. The required context validator was run; it exits 1 on existing broad context/source-inventory failures outside ST-09.
- Done: global tracker now records separate DD/implementation/runtime statuses; counts are 18 complete bundles and 65 incomplete, with ST-10 as next W1 pointer. Static audit passed; the context validator was run and reports unrelated repository-wide failures. Do not start ST-10 this session.
- DD is expected to remain BLOCKED: #20/#37 and #22–#24 are not source-backed; #09 is public and currently returns content/video_url without entitlement checks; progress/list schemas and lesson tree/access semantics are unresolved; Study Web has no ST-09 route source.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
