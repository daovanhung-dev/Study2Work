# AD-01 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-01-TC-001` | Planning ref / not run | `AC-38` | See source acceptance section | P1 |

## 2. Test planning references

### AD-01-TC-001 — Acceptance planning reference (AC-38)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-01](../../screen_stitch/05_admin/AD-01_dashboard-quan-tri/AD-01.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-38`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-01_dashboard-quan-tri/AD-01.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu và blockers

### Static acceptance checklist

- [x] Có ảnh nguồn nguyên trạng và ảnh chú thích; ảnh nguồn được giữ nguyên.
- [x] 35 marker tuần tự/duy nhất/in-bounds và có 35 element row tương ứng.
- [x] Các event trong HTML được mô tả đúng gồm disabled, no-op, placeholder navigation và timer-only refresh.
- [x] API #101 được đối chiếu với catalog, AC-38, Draft DD, route composition và current auth/profile code.
- [x] Expected behavior, current behavior, `DERIVED`, `UNWIRED`, `NOT_FOUND` và `DISCREPANCY` được tách riêng.
- [x] Error codes, state candidates và handoff được truy vết; chưa suy diễn lỗi 422, KPI formula, identity source hoặc service health.
- [ ] Được owner duyệt KPI keys/formulas/population/unit/order và mapping tới bốn card.
- [ ] Được owner duyệt date defaults, timezone, boundaries, partial/no-data và invalid-range behavior.
- [ ] Có API #101 implementation/test và report-specific authorization; xác định Admin profile source.
- [ ] Có Study Web app route/client mapping, audit/status endpoints nếu các panel này phải là dữ liệu live, và xử lý đúng Study Web design tokens.
- [ ] Xác minh schema/runtime/deployment trước khi đánh dấu `RUNTIME VERIFIED`.

### Open blockers

1. **API #101 `DESIGN_ONLY`:** catalog và Draft DD có, nhưng current router/module/query/model/test không có. Không thể xác nhận request thực thi/response thật.
2. **KPI:** bốn card là total users, active courses, pending moderation và system load. API #101 contract chỉ có `ImpactMetric[]`; các count proposal trong DD API có nghĩa khác và chưa được phê duyệt.
3. **Date range:** optional query bounds nhưng response period bắt buộc; các button disabled và default/inclusive/timezone/invalid range chưa rõ.
4. **Identity/authorization:** current Admin APIs có `ADMIN` role guard, nhưng #101 report permission không có source. Không có Admin self-profile route; API #04 hiện chỉ Student.
5. **Audit/service status:** activity, DB/auth/queue status, “System Normal”, readiness và compliance copy không được #101 trả; `/health/ready` chỉ kiểm tra cấu hình dependency, không probe DB.
6. **Study Web:** thiếu source/package/router nên không có route, API caller, loading/error mapping hoặc link destination runtime.
7. **Design system:** palette/font của screenshot khác Study Web visual target; chưa có approval cho ngoại lệ.

**Kết luận:** `DD BLOCKED`; tài liệu truy vết rõ phần có thể xác nhận và phần cần quyết định, nhưng chưa đủ để frontend triển khai KPI/range/identity mà không tự suy đoán. `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Tiêu chí kết thúc phiên

- Giữ nguyên hash `screen.png` và `code.html`; có ảnh nguyên trạng + ảnh annotated hợp lệ.
- 35 marker tuần tự, duy nhất, trong bounds và khớp chính xác 35 element rows.
- DD có A–F, mô tả sự kiện thực có source, trace API/error mapping, state/navigation và mọi blocker chưa xác nhận.
- Tracker/worklog khớp **DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED** nếu các contract blockers vẫn mở.
- Không bắt đầu AD-02 trong phiên này; chỉ nêu AD-02 là ứng viên cho phiên riêng.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
