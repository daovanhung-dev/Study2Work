# ME-03 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ME-03-TC-001` | Planning ref / not run | `AC-22` | See source acceptance section | P1 |
| `ME-03-TC-002` | Planning ref / not run | `AC-26` | See source acceptance section | P1 |

## 2. Test planning references

### ME-03-TC-001 — Acceptance planning reference (AC-22)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-03](../../screen_stitch/04_mentor/ME-03_workspace-khoa-hoc-cua-mentor/ME-03.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-22`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-03_workspace-khoa-hoc-cua-mentor/ME-03.md).
### ME-03-TC-002 — Acceptance planning reference (AC-26)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-03](../../screen_stitch/04_mentor/ME-03_workspace-khoa-hoc-cua-mentor/ME-03.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-26`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-03_workspace-khoa-hoc-cua-mentor/ME-03.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: 9. Acceptance checklist

- [x] Screen ID, route proposal, actor, expected links/states and current source status are recorded.
- [x] Current #49 route/auth/query/DB read/mapper/response/errors and test source are traced.
- [x] Current #65 route/auth/query/DB aggregate/mapper/response/errors and catalog discrepancy are traced.
- [x] API #46 course-list handoff and AC-21 assignment discrepancy are documented.
- [x] All 53 image markers map once to `ME03-EL-01..53`; source assets remain unmodified.
- [x] Screenshot fields without source are labeled sample or blocker; no new API/field/formula is introduced.
- [x] Relative references and marker coordinates checked; image visually reviewed.
- [ ] API #65 local contract approval, course context, permission semantics and unsupported panels are resolved.
- [ ] Study Web route/session/API wiring exists and is verified in runtime.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 4. Blockers and acceptance gate

- **ME03-B01 — access contract:** AC-22/AC-26 say Mentor has management/analytics permission; #49/#65 only enforce `MENTOR` role and direct owner. Assigned Mentor branch in AC-21/#46 is not supported. Resolve before route access behavior can be DD READY.
- **ME03-B02 — course summary:** no Mentor course detail API supplies code/cohort/standard/enrollment/update summary; #46 is paginated and has only basic Course fields. Direct entry and refresh context need an approved source.
- **ME03-B03 — API #65 contract:** catalog response `Page<Course>` conflicts with current derived `Page<MentorStudentProgress>`; full-roster page has no request bound. Owner approval/schema update is required.
- **ME03-B04 — unsupported panels:** per-module progress, student risk, weekly event feed, ratings/drop-off, repo resources, AI summary and Excel export are not produced by #49/#65 or listed as ME-03 APIs.
- **ME03-B05 — #49 semantics:** Content type/status/payload subtype and revision/publish rules remain open; flat Content tree is not verified as lesson/module structure.
- **ME03-B06 — client/runtime:** Study Web route/session/API wiring is absent; mockup labels and anchor destinations are not functional evidence.
- **ME03-B07 — visual/accessibility:** mockup tokens/font/control density conflict with the intended Study design guide; resolve during UI implementation planning.

Plan is accepted when: source hashes are preserved; all planned markers align once across plan/JSON/SVG/image/DD; every visible interactive/sample-data region is covered; API calls and error/status behavior trace to current source; unsourced behaviors stay blocked; relative links resolve; tracker and worklog separate DD, implementation and runtime states. Tests and runtime are not part of this docs-only verification.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
