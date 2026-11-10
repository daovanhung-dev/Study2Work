# ST-24 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-24-TC-001` | Planning ref / not run | `AC-19` | See source acceptance section | P2 |

## 2. Test planning references

### ST-24-TC-001 — Acceptance planning reference (AC-19)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-24](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/ST-24.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-19`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/ST-24.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Screen ID, actor, proposed route, AC-19/API #40 and ST-23/ST-25 relationships are traceable to inventory/API/AC sources.
- [x] Original 1600×1591 PNG and HTML are preserved; screenshot/HTML discrepancy and static sample values are explicit.
- [x] 26 ordered markers map one-to-one to the 26 element rows; compound toolbar child controls are enumerated in element/event details.
- [x] Eleven events include trigger, inputs, prerequisite, ordered handling, output and exceptions; absent submit action is explicitly blocked, not fabricated.
- [x] API #40 method/path/auth/body/201/error codes match catalog; all eight API DD open questions and the `content`/`title`/DDL discrepancies remain visible.
- [x] `draft/invalid/submitting/created`, preview, unavailable and error states plus ST-23/ST-25 navigation are separated into expected/current evidence.
- [x] No tags, lesson IDs, file upload API, title max, content conversion, status default, authorization predicate, transaction, retry or redirect behavior is invented.
- [ ] **DD READY:** blocked until API #40 Q-01…Q-08 are resolved, missing submit/success/error design is approved, course/lesson option sources are defined, and text editor/body mapping is implementable.
- [ ] **IMPLEMENTATION READY:** blocked until Study Web routes/UI and Student API #40 are wired against an approved contract.
- [ ] **RUNTIME VERIFIED:** not verified; PNG and HTML are static design artifacts and API #40 has no current route/test.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Verification plan

- Record original PNG and HTML SHA-256 and verify both remain unchanged; verify output PNG dimensions.
- Validate JSON and SVG; marker numbering `1..26`, unique element IDs and coordinates within both source and annotated canvases; match exactly 26 marker rows in DD C. Visually inspect annotated image for collisions/readability.
- Verify DD sections A–F; eleven events in order with trigger/input/process/output/exception; API #40 fields/statuses match catalog and the eight draft questions remain explicit; local Markdown links resolve; no unapproved API body, content encoding, title source, submit action, validation limit or business rule is introduced.
- Update `dd_screens/PLAN.md` count/pointers based on actual current core artifacts and record blockers/status separately.
- Run `git diff --check`. No tests/API calls/runtime checks; no `.agents` context page/manifest change planned. Run context validator only if a context page/manifest is changed.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
