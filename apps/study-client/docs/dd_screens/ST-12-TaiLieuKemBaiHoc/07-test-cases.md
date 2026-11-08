# ST-12 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ST-12-TC-001` | Planning ref / not run | `AC-15` | See source acceptance section | P2 |

## 2. Test planning references

### ST-12-TC-001 — Acceptance planning reference (AC-15)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ST-12](../../screen_stitch/03_student/ST-12_tai-lieu-kem-bai-hoc/ST-12.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-15`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/03_student/ST-12_tai-lieu-kem-bai-hoc/ST-12.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: H. Tiêu chí nghiệm thu

- [x] Tài sản nguồn và HTML tĩnh được phân biệt với runtime.
- [x] 27 marker có mapping duy nhất sang 27 element trong §C.
- [x] API #26 declaration/absence và API #12 current route/source được mô tả riêng.
- [x] Các event có input, precondition, steps, endpoint/response/error và kết quả hoặc blocker.
- [x] Empty/loading/error/authorization/navigation states không bị gán nhầm cho screenshot fallback.
- [x] Resource URL, visibility, signer, route return và no-data claims được ghi đúng trạng thái mở.
- [x] Relative links được kiểm tra tĩnh.
- [ ] API #26 response/cardinality/access/empty policy được duyệt; required để DD READY.
- [ ] Safe URL/access/preview/download policy, loaded-state UI và route handoff được duyệt; required để DD READY/implementation.
- [ ] Study Web implementation và browser flow được chạy/verify; hiện ngoài evidence.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: Tiêu chí kiểm tra đầu ra ST-12

- [x] Plan gốc đã tồn tại trước DD/ảnh; re-audit của phiên này được ghi trước khi sửa DD.
- [x] Original `screen.png` và `code.html` giữ nguyên hash đã ghi trong marker map.
- [x] 27 marker liên tiếp, duy nhất, nằm trong ảnh và khớp một-một với element ID trong DD.
- [x] Ảnh chú thích giữ nguyên tỷ lệ 2×; đã xem trực tiếp, số rõ và không che nội dung quan trọng.
- [x] DD có A–F, luồng vào/ra, 5 sự kiện, API #26/#12, trạng thái/lỗi/điều hướng, bảo mật/accessibility, blockers và nguồn truy vết.
- [x] Expected/current behavior và DD/implementation/runtime status được tách biệt.
- [x] Tracker/worklog cập nhật; static audit và scoped `git diff --check` đạt; không chạy tests/runtime.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
