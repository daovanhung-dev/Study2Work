# AD-20 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-20-TC-001` | Planning ref / not run | `AC-36` | See source acceptance section | P1 |

## 2. Test planning references

### AD-20-TC-001 — Acceptance planning reference (AC-36)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-20](../../screen_stitch/05_admin/AD-20_soan-gui-thong-bao-he-thong/AD-20.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-36`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-20_soan-gui-thong-bao-he-thong/AD-20.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Source `screen.png` và `code.html` được giữ nguyên; hash được ghi trong worklog.
- [x] Có ảnh annotation 2×, marker JSON và plan; 54 marker tuần tự ánh xạ 1:1 tới bảng element.
- [x] Expected contract, current mockup behavior và local API fallback được tách biệt.
- [x] API #93 body/response/errors và local guard/validator/DB side effects được mô tả; không chạy application tests/runtime trong phiên này.
- [x] Handoff AD-20→SH-07 và các mâu thuẫn Notification/Operation, UUID/int64 được ghi rõ.
- [ ] DD READY: chưa đạt; audience, channel, permission, draft/send, physical model, response/operation bridge và UI route còn blocker.
- [ ] IMPLEMENTATION READY: chưa đạt; Study Web route/API client absent, nút chính không hoạt động, request UI không cung cấp explicit recipients.
- [ ] RUNTIME VERIFIED: chưa đạt; không chạy Study Web hoặc live DB/provider.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: Source review and order

1. Read list_screen row 78, API reverse index #093, flow F13 and G-12 in `apps/study-client/docs/list_screen.md`; read global row/checkpoint in `dd_screens/PLAN.md`.
2. Compare AC-36 create/send branch, direct API catalog #93, reusable Notification/Operation schemas and generic operation-tracking prose.
3. Read API #93 DD, Q-93-01…10 and verification report; preserve Draft/open-question status.
4. Trace current route → shared ADMIN guard → validator → recipients query → notification/delivery inserts → response/commit/errors; inspect tests without running them. Treat checked-in DDL/migration only as candidates.
5. Check API #18 design/current registration and SH-07 handoff. Preserve Notification-vs-Operation and UUID-vs-int64 discrepancies; do not assert a valid operation poll.
6. Recheck Study Web source tree and inspect exact HTML/screenshot; compare the intended style only with `.agents/web-study/design.md`.
7. The source review and status were recorded in `.agents/worklog/2026-11-07/design-study-screen-ad20.md`. This plan is saved before marker JSON/SVG, annotated PNG or AD-20.md.

### Trích từ DD nguồn: Acceptance audit to perform

- [ ] Preserve original `screen.png`/`code.html`; record unchanged hashes.
- [ ] Generate unique sequential markers #1–#54 with in-bounds source coordinates and one matching DD row each.
- [ ] Ensure JSON, SVG and DD coordinates agree; render 2484×3200 PNG and visually inspect it for legibility/coverage.
- [ ] Complete DD sections A–F and describe each observed affordance/event, expected/current API shape, validation/error boundary, state and navigation blocker.
- [ ] Check API #093 reverse index and screen row 78; keep API contract as D and update screen doc/tracker status accurately.
- [ ] Verify inventory/folder count remains 83/83 and core artifact count advances 72/83 → 73/83.
- [ ] Run static artifact/relative-link/hash/dimension/marker checks and `git diff --check`; do not run application tests/runtime for this documentation task.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
