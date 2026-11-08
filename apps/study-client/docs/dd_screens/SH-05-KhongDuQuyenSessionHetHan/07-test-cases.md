# SH-05 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `SH-05-TC-001` | Planning ref / not run | `AC-02` | See source acceptance section | P0 |
| `SH-05-TC-002` | Planning ref / not run | `AC-11` | See source acceptance section | P0 |

## 2. Test planning references

### SH-05-TC-001 — Acceptance planning reference (AC-02)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [SH-05](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/SH-05.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-02`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/SH-05.md).
### SH-05-TC-002 — Acceptance planning reference (AC-11)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [SH-05](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/SH-05.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-11`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/SH-05.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: 10. Tiêu chí nghiệm thu

- [x] Có ảnh nguồn nguyên trạng, ảnh annotated, plan, DD và marker JSON cạnh `code.html`.
- [x] 11 marker đánh số liên tục; mỗi marker map một Element ID duy nhất và có bảng đặc tả tương ứng.
- [x] Mô tả các state 401/403 và phân biệt prototype preview với target/runtime source.
- [x] Mọi API/event có input, điều kiện, các bước xử lý, response mapping, state/output và ngoại lệ; R-X01 được ghi là runtime source ngoài catalog.
- [x] API #04/R-X01 đối chiếu route/module/model/validation/test source; chưa tuyên bố tests đã chạy.
- [x] Ma trận state/navigation, safe redirect, token handling và lỗi mạng/5xx có status rõ; quyết định chưa có được đánh dấu blocker.
- [x] Không có API, field, role rule hoặc error code tự tạo; mock/backend discrepancies được ghi cụ thể.
- [ ] Product/Security/Frontend/Backend chốt blockers B01–B07; frontend implementation chưa thể bắt đầu an toàn.
- [ ] Runtime smoke/visual verification chưa thực hiện vì Study Web runtime không có trong checkout.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Tiêu chí nghiệm thu SH-05

- Tạo đúng `screen_annotated.png`; giữ nguyên `screen.png` và `code.html`; ghi hash nguồn trước/sau.
- Có 11 marker nhìn rõ theo danh sách trên; mỗi marker `#n` ánh xạ một Element ID duy nhất trong SH-05.md và SH-05_markers.json; hidden 401 controls được mô tả là state-dependent, không gắn marker giả vào ảnh 403.
- DD tách riêng 401/403, prototype/current source/target behavior; mọi API field, business code, route và response bám source hoặc đánh dấu blocker/discrepancy.
- Có input → validation/permission → API/nội bộ → response mapping → state update → outcome/exceptions cho từng event; không coi HTML timer là API call.
- Có ma trận state/loading/error/refresh failure/offline/copy failure và điều kiện điều hướng; mọi `returnTo` an toàn.
- `DD BLOCKED` đến khi chốt production content/state mapping, 401 recovery policy (kể cả profile-missing/repeated 401), token persistence/refresh outcome, safe-route fallback và SH-02/G-14 login handoff; `IMPLEMENTATION BLOCKED` do thiếu Study Web source và các quyết định trên; `RUNTIME NOT VERIFIED`.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
