# AD-13 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-13-TC-001` | Planning ref / not run | `AC-34` | See source acceptance section | P1 |

## 2. Test planning references

### AD-13-TC-001 — Acceptance planning reference (AC-34)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-13](../../screen_stitch/05_admin/AD-13_chi-tiet-bai-hoc-quan-tri/AD-13.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-34`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-13_chi-tiet-bai-hoc-quan-tri/AD-13.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Giữ nguyên `screen.png`/`code.html`; tạo ảnh đánh số riêng và marker JSON; marker đọc được và không che nội dung chính.
- [x] Có mục A–F; 61 marker khớp 61 element rows; source/API links có thể truy vết.
- [x] Mô tả EV-01…EV-08 với input, processing, output/error và tách current source khỏi expected UI flow.
- [x] Đối chiếu #83 route, guard, path validation, query, reusable Lesson mapping, envelope/errors, rollback/no mutation và focused test source.
- [x] Ghi AD-12 numeric handoff, AD-14 mutation boundary và AC-34 dependency conflict.
- [x] Đánh dấu resources/progress/metrics/SSE/audit/concurrency/media/permission/schema/UI claims không được #83 xác nhận.
- [ ] Contract, live schema, permission và dependency/output rules đủ để triển khai đầy đủ mà không suy đoán. **Chưa đạt:** các owner/API/schema blockers còn mở.
- [ ] `DD READY`. **Không đạt:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.

### Sources

- [Screen inventory / AC-34 flow](../../list_screen.md)
- [AD-12 handoff DD](../../screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/AD-12.md)
- [API catalog #83](../../../../../docs/lists/list_api.md)
- [AC-34 Admin management diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [API #83 route](../../../../study-server/app/api/v1.py)
- [API #83 module](../../../../study-server/app/modules/admin/api_83_admin_lesson_detail)
- [API #83 focused test source](../../../../study-server/tests/modules/admin/api_83_admin_lesson_detail/test_admin_lesson_detail.py)
- [API #83 DD overview and open questions (Draft)](../../../../study-server/docs/dd/83_admin_lesson_detail/02_Overview.md)
- [API #86 dependency check source](../../../../study-server/app/modules/admin/api_86_admin_lesson_delete/query.py)
- [Legacy Study DDL candidate](../../../../../infra/postgres/study-server/DB.sql)
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql)
- [Study Web design target](../../../../../.agents/web-study/design.md)

#### Kế hoạch kiểm chứng từ source PLAN

> CẦN_XÁC_NHẬN: Plan nguồn không có section verification/test được nhận diện.


- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
