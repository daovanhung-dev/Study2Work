# ME-17 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ME-17-TC-001` | Planning ref / not run | `AC-26` | See source acceptance section | P2 |

## 2. Test planning references

### ME-17-TC-001 — Acceptance planning reference (AC-26)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-17](../../screen_stitch/04_mentor/ME-17_tien-do-tung-hoc-vien/ME-17.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-26`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-17_tien-do-tung-hoc-vien/ME-17.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

### F1. Static checks đạt trong phiên này

- [x] Screen ID ME-17 và scope một màn hình được giữ đúng.
- [x] Kế hoạch riêng được tạo trước marker map/annotation/DD.
- [x] Ảnh nguồn screen.png được giữ nguyên; annotation là file riêng.
- [x] 39 marker sequential/unique/in-bounds và ánh xạ 1:1 tới element rows.
- [x] A–F có tổng quan, expected/current flow, element detail, event I/O/API/error, state/navigation, acceptance.
- [x] Clickable prototype anchors và refresh handler được phân tích; không bịa route hoặc API.
- [x] #65/#66/#67 và AC-26 discrepancy được tách riêng.
- [x] Source links, test-source status, schema/runtime limits và unsupported static claims được ghi rõ.
- [x] Không chạy application tests hoặc runtime; không tuyên bố RUNTIME VERIFIED.

### F2. Điều kiện còn chặn DD READY

- [ ] API owner xác nhận singular StudentCourseProgress hay ApiEnvelope<Page<Course>> và field/business-code mapping.
- [ ] Flow owner xác nhận AC-26 ordering và quan hệ ME-16/#65, ME-17/#67, ME-18/#66.
- [ ] ME-16→ME-17 route carrier và nguồn numeric course_id/student_id được chốt.
- [ ] Loaded timeline row, empty semantics, status-to-copy mapping và “bài còn thiếu” rule được duyệt.
- [ ] Nguồn hoặc quyết định loại bỏ course/student identity, enrollment, assignment/quiz, self-study, sync freshness, comments/milestones claims được ghi lại.
- [ ] Owner/assigned-Mentor rule, ACTIVE roster eligibility, 403/404 privacy, formula/duplicate policy và live schema được xác nhận.
- [ ] Chốt route/auth/session-expiry/network-error/refresh UX và Study Web runtime ownership.

**Kết luận:** ME-17 có static screen DD và trace nguồn hiện tại, nhưng chưa đạt DD READY vì các contract/design decisions trên còn cần owner approval để tránh suy đoán. IMPLEMENTATION BLOCKED độc lập với RUNTIME NOT VERIFIED.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 6. Blockers and status criteria

- `Page<Course>` direct contract conflicts with the singular local #67 response; the API DD asks for approval.
- No approved ME-16→ME-17 selected-row carrier; ME-16 #65 local response also differs from its direct contract.
- Timeline loaded state is absent. Current #67 is a per-lesson state snapshot ordered by curriculum, not chronological event history; it does not supply assignment, quiz, study-hour, comment or project-milestone data.
- Screenshot claims/fields have no source mapping; no additional API may be invented or merged from #65/#66.
- Direct-owner vs assigned Mentor, active-roster eligibility, 403/404 privacy, formula/default statuses, latest duplicate selection, pagination bound, and legacy BIGINT vs V1-PILOT UUID live schema are unresolved.
- Study Web feature route/client/runtime is absent. Do not claim `RUNTIME VERIFIED`.
- Final DD status should remain **DD BLOCKED** if the owner must still define the loaded timeline or approve response/mapping decisions; mark **IMPLEMENTATION BLOCKED** independently. Use `DD READY` only if every unresolved choice is explicitly outside implementation scope and the spec can be implemented without guessing.

### Trích từ DD nguồn: 7. Order of work and verification

1. [x] Write this plan before marker/DD creation.
2. [x] Create `ME-17_markers.json`, SVG overlay and `screen_annotated.png` from the unchanged PNG; review marker placement visually.
3. [x] Write `ME-17.md` sections A–F with 39 elements, recognized events, input/process/output/API/errors, state/navigation, trace links and named blockers.
4. [x] Update ME-17 inventory and global plan rows, the 83-screen artifact count and this worklog.
5. [x] Static audit JSON sequence/bounds, one-to-one marker/element mapping, source hashes, dimensions, links, visual annotation and `git diff --check`. Application tests/runtime were not run.
6. [x] Stop after ME-17; do not start ME-18.

**Outcome:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
