# AD-12 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-12-TC-001` | Planning ref / not run | `AC-34` | See source acceptance section | P1 |

## 2. Test planning references

### AD-12-TC-001 — Acceptance planning reference (AC-34)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-12](../../screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/AD-12.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-34`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/AD-12.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Giữ `screen.png` và `code.html` nguyên trạng; có ảnh chú thích riêng, 42 marker tuần tự và marker map.
- [x] Mục C có đúng một hàng cho mỗi marker #1–#42.
- [x] Mục D mô tả input, xử lý, API/source, output và ngoại lệ cho EV-01…EV-09; UI-only event được phân biệt với current behavior.
- [x] Truy vết API #82 route/module/query/model/DDL/test source; phân biệt catalog singleton với local array response; test không được tuyên bố đã chạy.
- [x] Ghi rõ access, current data fields, empty/error states, AD-13 handoff và AC-34 chain.
- [x] Ghi blocker search/course/type/status/pagination/actions/Add, RBAC permission, nullability/live schema, UI wiring và copy/design discrepancy.
- [ ] Mọi quyết định contract đủ để triển khai UI không còn mở. **Chưa đạt:** các blocker ở mục A/B/D còn cần owner/API/schema resolution.
- [ ] `DD READY`. **Không đạt trong phiên này:** trạng thái `DD BLOCKED`; implementation blocked; runtime not verified.

### Sources

- [Screen inventory và AC-34 flow](../../list_screen.md)
- [API catalog #82](../../../../../docs/lists/list_api.md)
- [AC-34 Admin management diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [API #82 route và #83 route](../../../../study-server/app/api/v1.py)
- [API #82 module](../../../../study-server/app/modules/admin/api_82_admin_lessons_list)
- [API #82 focused test source](../../../../study-server/tests/modules/admin/api_82_admin_lessons_list/test_admin_lessons_list.py)
- [Legacy Study Server DDL candidate](../../../../../infra/postgres/study-server/DB.sql)
- [API #82 DD (Draft)](../../../../study-server/docs/dd/82_admin_lessons_list)
- [Study Web design target](../../../../../.agents/web-study/design.md)

#### Kế hoạch kiểm chứng từ source PLAN

> CẦN_XÁC_NHẬN: Plan nguồn không có section verification/test được nhận diện.


- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
