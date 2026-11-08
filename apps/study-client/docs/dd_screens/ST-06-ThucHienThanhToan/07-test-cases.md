# ST-06 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-06-TC-001` | Planning ref / not run | `AC-12` | See source acceptance section | P2 |

## 2. Test planning references

### ST-06-TC-001 — Acceptance planning reference (AC-12)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-06](../../screen_stitch/03_student/ST-06_thuc-hien-thanh-toan/ST-06.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-12`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-06_thuc-hien-thanh-toan/ST-06.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] ST-06 được xử lý trong phiên riêng; plan được lưu trước khi render, marker và DD.
- [x] Giữ nguyên `screen.png` và `code.html`; ghi provenance cho HTML-derived render vì ảnh nguồn gần như trống.
- [x] 14 marker DOM-measured, sequential và unique; DD element rows dùng cùng ID.
- [x] Expected inventory/AC/API behavior được tách khỏi current HTML, Study Web và Study Server source.
- [x] EV-01…EV-06 mô tả inputs, ordered handling, API/request/auth/status/errors, side-effect and output boundaries.
- [x] Ghi rõ API #17/#18 `DESIGN_ONLY / UNWIRED`, #18 ID/authorization discrepancy, missing payment/order/operation source, retry gap và invalid return links.
- [x] Phân biệt `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`; không claim test/runtime pass.
- [ ] Chốt Order/provider/gateway/payment/operation IDs, ownership, enums, lifecycle/polling, retry/idempotency, trusted paid signal và UI trigger trước khi chuyển thành implementable DD.
- [ ] Wire Study Web route/auth, #17/#18 backend, payment verification, state UI và ST-07 handoff trước runtime verification.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Completion and status criteria

- Create `screen_rendered_from_html.png` only after this plan is saved; target 2560×2048 from CSS viewport 1280×1024 at 2× after document/fonts settle.
- Create DOM-measured sequential, unique, in-bounds marker records and an annotation based on the derived render; keep callouts off text.
- Author `ST-06.md` sections A–F with every visible target and identified event; separate inventory/AC/API expectations from current source/prototype; mark #17/#18 `DESIGN_ONLY / UNWIRED`.
- Update only the ST-06 inventory/global-plan rows and append the session checkpoint; do not begin ST-07.
- Static audit: marker order/count/bounds and 1:1 DD mapping; JSON/XML parse; local links; image dimensions; original asset hashes; 83-screen inventory/folder count; core artifact count; scoped `git diff --check`.
- Do not run application tests/runtime. Keep statuses distinct: `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` until identifier, payment and operation contracts are resolved.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
