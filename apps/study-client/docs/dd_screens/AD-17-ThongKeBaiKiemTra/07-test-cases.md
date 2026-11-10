# AD-17 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-17-TC-001` | Planning ref / not run | `AC-35` | See source acceptance section | P2 |

## 2. Test planning references

### AD-17-TC-001 — Acceptance planning reference (AC-35)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-17](../../screen_stitch/05_admin/AD-17_thong-ke-bai-kiem-tra/AD-17.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-35`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-17_thong-ke-bai-kiem-tra/AD-17.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] 33 element groups được đánh số tuần tự; JSON/SVG/ảnh/DD dùng cùng IDs và tọa độ.
- [x] Original `screen.png`/`code.html` giữ nguyên; annotated PNG giữ nội dung và bố cục, output 2×.
- [x] A–F có actor, route candidate, API/auth, flow, states, errors, links và implementation status.
- [x] Mỗi event nêu element/điều kiện/đầu vào/xử lý/kết quả; API call, errors và static timer được tách bạch.
- [x] Direct catalog `ApiEnvelope<Quiz>` được giữ riêng với local `AdminQuizStatistics` proposal.
- [x] Không mô tả score distribution, completion rate, average duration hay background aggregate là dữ liệu đã có.
- [ ] Owner xác nhận response schema, metrics/formula/NULL/rounding và update/aggregation semantics.
- [ ] Owner xác nhận quiz-management permission policy so với shared `ADMIN` guard.
- [ ] BE/DB xác nhận active schema, tombstone/status rows, legacy BIGINT vs V1-PILOT UUID và live deployment.
- [ ] Frontend source/router/API client được wire, error/loading/empty/ready states và route handoff được triển khai.

**Kết luận nghiệm thu:** Checklist tài liệu và static artifacts có thể rà soát; DD READY chưa đạt do blocker response/metric/authorization. IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED.

#### Kế hoạch kiểm chứng từ source PLAN

> CẦN_XÁC_NHẬN: Plan nguồn không có section verification/test được nhận diện.


- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
