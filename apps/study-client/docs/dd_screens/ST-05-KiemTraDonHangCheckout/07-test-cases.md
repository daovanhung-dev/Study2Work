# ST-05 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-05-TC-001` | Planning ref / not run | `AC-12` | See source acceptance section | P2 |

## 2. Test planning references

### ST-05-TC-001 — Acceptance planning reference (AC-12)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-05](../../screen_stitch/03_student/ST-05_kiem-tra-don-hang-checkout/ST-05.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-12`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-05_kiem-tra-don-hang-checkout/ST-05.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] ST-05 chỉ được xử lý trong phiên này; plan được lưu trước khi render/marker/DD.
- [x] Giữ nguyên `screen.png` và `code.html`; ghi provenance cho HTML-derived render vì ảnh nguồn trống.
- [x] 13 marker được đo theo DOM, đánh số tuần tự/duy nhất và có bảng element mapping cùng ID trong DD.
- [x] Tách expected inventory/AC/API contract khỏi current HTML, Study Web và Study Server behavior.
- [x] Ghi đủ EV-01…EV-06, including API method/path/auth/request/response/status/errors và current-vs-design boundaries.
- [x] Nêu rõ #08 current read-only source, #16 catalog/Draft-only, API/schema/order/payment blockers, CTA mismatch và revalidation sequence discrepancy.
- [x] Phân biệt `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`; không tuyên bố runtime/test pass.
- [ ] Xác nhận Order schema, provider enum/relationship, amount/currency, stale-price policy, idempotency/transaction và direct-call rules để đạt implementable DD.
- [ ] Wire Study Web route/auth guard, approved confirmation UI, API #16, order ID mapping và ST-06 integration trước khi triển khai.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Completion and status criteria

- Create `screen_rendered_from_html.png` only after this plan is saved; target 2560×2048 from CSS viewport 1280×1024 at 2× after document/fonts settle.
- Create sequential, unique, in-bounds DOM-measured marker records and annotation based on the derived render; keep marker positions off important text.
- Author `ST-05.md` sections A–F with every visible target and every identified event, distinguish expected design from current behavior, and mark API #16 `DESIGN_ONLY / UNWIRED`.
- Update inventory row 19 and global plan with the completed session and explicit blockers; do not change unrelated screens or API reverse-index classifications.
- Static audit: marker order/count/bounds and 1:1 DD mapping; JSON/XML parse; local links; image dimensions; original asset hashes; 83-screen inventory/folder count; core artifact count; scoped `git diff --check`.
- Do not run application tests/runtime. Keep statuses distinct: `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` until contract gaps are resolved.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
