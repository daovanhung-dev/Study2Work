# ST-01 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-01-TC-001` | Planning ref / not run | `AC-13` | See source acceptance section | P1 |
| `ST-01-TC-002` | Planning ref / not run | `AC-18` | See source acceptance section | P1 |
| `ST-01-TC-003` | Planning ref / not run | `AC-20` | See source acceptance section | P1 |

## 2. Test planning references

### ST-01-TC-001 — Acceptance planning reference (AC-13)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-01](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/ST-01.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-13`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/ST-01.md).
### ST-01-TC-002 — Acceptance planning reference (AC-18)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-01](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/ST-01.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-18`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/ST-01.md).
### ST-01-TC-003 — Acceptance planning reference (AC-20)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-01](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/ST-01.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-20`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/ST-01.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Screen ID, Student actor, proposed route, AC/API, linked screens và current source status được ghi cùng nguồn.
- [x] `screen.png` và `code.html` được giữ nguyên; static gate, wrong endpoint paths, no-synthetic-data copy và design mismatch được phân biệt với runtime.
- [x] 37 marker liên tục/duy nhất có một hàng element tương ứng; SVG overlay và JSON lưu mapping.
- [x] 10 event có trigger/type, element/precondition, input, ordered handling, output và exceptions; actions chưa wired giữ design-only status.
- [x] API #20/#21/#38/#43 fields/paths/errors được đối chiếu catalog và Draft DD; không thêm API, fields, statuses, defaults hoặc formulas.
- [x] AC-13 empty-branch và AC-18 ordering discrepancies được nêu rõ; AC-20 mark-read không bị kéo vào ST-01.
- [x] Widget states, navigation, security, design target và source absence được tách biệt.
- [ ] **DD READY:** chưa đạt; chờ chốt #20/#21 schemas/merge/empty, #38 award projection/filter/page, #43 projection/recipient/order, AC orchestration và route/data design.
- [ ] **IMPLEMENTATION READY:** chưa đạt; Study Web route/client và các APIs #20/#21/#38/#43 chưa wired trong source hiện tại.
- [ ] **RUNTIME VERIFIED:** chưa đạt; không chạy UI/API runtime trong docs task.

**Result:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 9. Verification plan

- Kiểm tra source hashes/dimensions giữ nguyên; visual inspect ảnh gốc và ảnh chú thích.
- Kiểm tra JSON/SVG parse, marker #1–#37 liên tục/duy nhất/in-bounds, 37 IDs ↔ 37 DD rows, không che nội dung, SVG labels và connector geometry tương ứng.
- Kiểm tra DD A–F, 10 event sections đầy đủ trường, API catalog/errors, AC discrepancies, local links, global inventory/status/pointers, 83 folder count/core-bundle count.
- Chạy `git diff --check` trên tracked files và trailing-whitespace scan trên authored files. Không chạy application tests, app runtime hay live DB query trong docs task.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
