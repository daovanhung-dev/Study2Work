# ST-26 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-26-TC-001` | Planning ref / not run | `AC-20` | See source acceptance section | P2 |

## 2. Test planning references

### ST-26-TC-001 — Acceptance planning reference (AC-20)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-26](../../screen_stitch/03_student/ST-26_thong-bao-hoc-vien/ST-26.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-20`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-26_thong-bao-hoc-vien/ST-26.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [ ] Exactly 41 unique ordered markers match the 41 DD element rows and the annotation image.
- [ ] All 14 events specify trigger, precondition, typed input, ordered processing, exact API contract or explicit absence, output and exceptions.
- [ ] #43–#45 request fields, endpoint, Student auth, response types and catalog status/business codes are represented without additions.
- [ ] Draft API questions, legacy-vs-pilot schema discrepancy, missing read/category/deep-link fields and absence of Student runtime remain visible blockers.
- [ ] Screenshot samples, including unread count, destinations, channel toggles, statistics, support/contact claims and “API #48” label, are not treated as backend truth.
- [ ] List refresh after #44/#45 follows inventory; no local count mutation, blind mutation retry or unsafe deep-link routing is asserted.
- [ ] Loading/ready/empty/unread/read/marking/error and blocked navigation states are traceable to a requirement or labeled proposal.
- [ ] Related screen links are identified; unsupported route parameters and history behavior are left unresolved.
- [ ] All local source links resolve; original screenshot/HTML hashes stay unchanged; no runtime/test claim is made.

**Kết luận:** ST-26 DD currently `BLOCKED`; implementation is `BLOCKED`; runtime is `NOT VERIFIED`. Product/API/DB decisions are required before the loaded notification screen can be implemented safely.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 8. Verification checklist

- [x] Original `screen.png`/`code.html` SHA-256 values unchanged.
- [x] Annotated canvas is 1305×1648 and its source crop is pixel-identical (`AE=0`); callouts do not cover original content.
- [x] Marker JSON is valid; 41 marker IDs are ordered and unique; `x/y` are inside the source, leader anchors equal the source offset in the annotated canvas, badges sit in gutters, SVG parses, and each marker maps to exactly one DD row.
- [x] DD includes sections A–F and 14 sequential events with all required event fields.
- [x] API #43–#45 methods/endpoints/inputs/responses/status/business codes match catalog; Draft/open-question limitations (7/7/8) are visible.
- [x] All 23 relative Markdown links in ST-26 DD/plan resolve.
- [x] Tracker row/status, 83 screen IDs, 44 core artifact sets, and next pointer ME-10 reflect current inventory.
- [x] `git diff --check` and authored-file whitespace scan pass; tests/runtime were not run or claimed.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
