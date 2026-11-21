# ST-07 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-07-TC-001` | Planning ref / not run | `AC-12` | See source acceptance section | P2 |

## 2. Test planning references

### ST-07-TC-001 — Acceptance planning reference (AC-12)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-07](../../screen_stitch/03_student/ST-07_ket-qua-dang-ky-khoa-hoc/ST-07.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-12`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-07_ket-qua-dang-ky-khoa-hoc/ST-07.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] ST-07 được xử lý riêng; plan được lưu trước HTML render, marker và DD.
- [x] Giữ nguyên `screen.png` và `code.html`; HTML-derived render provenance ghi riêng.
- [x] Có 13 marker tuần tự/duy nhất, DOM-measured và ánh xạ 1:1 với 13 element rows trong DD.
- [x] Tách expected inventory/AC/API design khỏi current HTML, Study Web, Study Server source và DDL.
- [x] EV-01…EV-07 ghi trigger/input/ordered handling/API boundary/response/error/side-effect/output; API #18/#19/#20 được đánh dấu design-only/unwired.
- [x] Ghi rõ AC-12 vs ST-07 result-screen discrepancy, #18 detached/ID-owner gaps, #19 enrollment transaction/identity/idempotency gaps, #20 response mismatch và CTA handoff.
- [x] Phân biệt `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`; không claim application tests/runtime.
- [ ] Chốt sở hữu/thời điểm #19, entitlement/payment proof, #18 handoff/lifecycle, #19 duplicate/Progress contract, #20 course-list response, post-create reload failure và success destination trước khi DD implementable.
- [ ] Wire Study Web route/auth/client và Study APIs #18/#19/#20, xác nhận live schema, rồi mới thực hiện runtime verification.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Completion and verification criteria

- Save this plan before creating the derived render, marker map/SVG, annotation or ST-07 DD.
- If source screenshot is unusable, preserve it and create separate `screen_rendered_from_html.png`; annotate that render and document its provenance.
- Finalize unique sequential DOM-measured markers and in-bounds positions; 1:1 match every marker to an ST-07 DD element row; keep callouts off meaningful text.
- Author ST-07.md sections A–F with expected/current separation, route/actor/preconditions, visible elements, each identified event's inputs/ordered handling/API/auth/status/errors/side effects/output, state matrix and navigation payloads.
- Keep unresolved API/AC/source discrepancies as blockers. Do not claim `DD READY`, implementation completion, or runtime verification where gates are open.
- Update only ST-07's inventory/global plan rows plus append the session checkpoint; do not start ST-08.
- Static audit: source hashes unchanged; image dimensions/provenance; JSON/XML; marker order/count/bounds/DD mapping; local Markdown links; 83 inventory IDs and folders; core artifact count; authored text whitespace; scoped `git diff --check`.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
