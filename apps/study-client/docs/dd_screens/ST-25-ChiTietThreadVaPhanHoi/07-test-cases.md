# ST-25 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-25-TC-001` | Planning ref / not run | `AC-19` | See source acceptance section | P2 |

## 2. Test planning references

### ST-25-TC-001 — Acceptance planning reference (AC-19)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-25](../../screen_stitch/03_student/ST-25_chi-tiet-thread-va-phan-hoi/ST-25.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-19`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-25_chi-tiet-thread-va-phan-hoi/ST-25.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] ST-25 source PNG and HTML are inventoried with hashes; both remain unchanged; screenshot and fallback mismatch is explicit.
- [x] Annotation has one ordered unique marker per documented visual/control group; all 40 IDs map 1:1 to section C and avoid obscuring source content.
- [x] Sections A–F include expected/current separation, AC/API trace, access/security, input/processing/output/errors, states and navigation.
- [x] API #41/#42 fields, statuses and business codes match catalog; both Draft DDs and all open questions stay explicit.
- [x] No invented API, title mapping, content conversion, count mutation, sort, save/like, moderation or route behavior is stated as approved.
- [x] Every event has trigger, condition, data provenance, ordered processing, API boundary, output and exceptions; #41 success precedes #42 reload.
- [x] Local Markdown links and marker assets validate; tracker and worklog are current.
- [x] `git diff --check` and authored-file whitespace audit pass. No API tests/runtime were run.

**Screen status:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. API/product decisions and Study Web source are still required before DD READY or implementation.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Verification plan

- Verify source screenshot and HTML hashes remain unchanged; check source and annotated PNG dimensions.
- Validate marker JSON and SVG, 1–40 ordering/unique element IDs/bounds, and exact 1:1 mapping to section C; visually inspect callout overlap/readability.
- Check DD sections A–F, every marker row, sequential events and required trigger/condition/input/processing/API/output/exception coverage; verify #41/#42 catalog fields/statuses and open-question boundaries.
- Check local Markdown links, source-backed versus derived labels, ST-23/ST-24 handoff order and global tracker count/pointers.
- Run `git diff --check` plus a whitespace audit on authored files. Do not run API tests or runtime/browser probes for this docs-only task.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
