# AD-17 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-17-TC-001` | Planning ref / not run | `AC-35` | See source acceptance section | P2 |

## 2. Test planning references

### AD-17-TC-001 — Acceptance planning reference (AC-35)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-17](../../screen_stitch/05_admin/AD-17_thong-ke-bai-kiem-tra/AD-17.md); full acceptance stays gated until the response, metric and permission blockers are resolved.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Source tests do not establish approved contract semantics or browser/live runtime. Do not report `RUNTIME VERIFIED` from unit tests alone.
- **References:** `AC-35`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-17_thong-ke-bai-kiem-tra/AD-17.md).

## 3. Source acceptance / verification status

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] 33 element groups được đánh số tuần tự; JSON/SVG/ảnh/DD dùng cùng IDs và tọa độ.
- [x] Original `screen.png`/`code.html` giữ nguyên; annotated PNG giữ nội dung và bố cục, output 2×.
- [x] A–F có actor, current source route, API/auth, flow, states, errors, links và implementation status.
- [x] Mỗi event nêu element/điều kiện/đầu vào/xử lý/kết quả; API call, errors và static timer được tách bạch.
- [x] Direct catalog `ApiEnvelope<Quiz>` được giữ riêng với local `AdminQuizStatistics` proposal.
- [x] Không mô tả score distribution, completion rate, average duration hay background aggregate là dữ liệu đã có.
- [ ] Owner xác nhận response schema, metrics/formula/NULL/rounding và update/aggregation semantics.
- [ ] Owner xác nhận quiz-management permission policy so với shared `ADMIN` guard.
- [ ] BE/DB xác nhận active schema, tombstone/status rows, legacy BIGINT vs V1-PILOT UUID và live deployment.
- [x] Angular route/page/API caller and loading/loaded/error source states exist; focused source tests are available. This does not close the contract, permission or runtime gates.

### T006 focused source checks

- Angular AD-17 page and Admin route specs: 5/5 passed.
- Study Server API #91 focused pytest: 19/19 passed using fake session/query; one Starlette/httpx deprecation warning.
- These checks do not verify browser rendering, live API deployment, PostgreSQL schema or approved metric semantics.

**Kết luận nghiệm thu:** DD READY chưa đạt do response/metric/authorization blockers. Angular implementation is PARTIAL SOURCE; Stitch prototype remains static. RUNTIME NOT VERIFIED.

#### Kế hoạch kiểm chứng từ source PLAN

> CẦN_XÁC_NHẬN: Plan nguồn không có section verification/test được nhận diện.


- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- `AD-17-TC-001` remains an acceptance planning reference and was not executed as a standalone acceptance test.
