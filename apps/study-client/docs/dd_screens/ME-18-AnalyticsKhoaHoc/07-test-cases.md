# ME-18 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ME-18-TC-001` | Planning ref / not run | `AC-26` | See source acceptance section | P2 |

## 2. Test planning references

### ME-18-TC-001 — Acceptance planning reference (AC-26)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-18](../../screen_stitch/04_mentor/ME-18_analytics-khoa-hoc/ME-18.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-26`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-18_analytics-khoa-hoc/ME-18.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

### F1. Static checks

- [x] Chỉ xử lý ME-18 trong phiên này; plan được lập trước markers/DD.
- [x] Giữ nguyên screen.png/code.html; annotation là file riêng.
- [x] 35 marker tuần tự, unique, in-bounds, khớp một-một 35 element rows.
- [x] DD có sections A–F; events I/O/processing/API/error, disabled controls, placeholder navigation, states và source discrepancies được mô tả.
- [x] #66 catalog, AC-26 diagram, API source, Draft DD and fake-DB test source được đối chiếu; no application tests/runtime claim.
- [x] #65/#66/#67 không bị gộp; AC-26 order conflict được giữ lại.

### F2. Blockers trước DD READY

- [ ] API owner resolve ApiEnvelope<Page<Course>> vs local analytics summary contract.
- [ ] Product/domain owner define completion rate, average duration, discussion interaction, calculation/grain/source and no-data semantics.
- [ ] Chốt event-ledger source hoặc phê duyệt current-state proxy; không dùng proxy như event history.
- [ ] Chốt time-window options/semantics and endpoint support before enabling selector.
- [ ] Chốt ETL/sync activation, refresh operation and CSV export contracts before enabling those actions.
- [ ] Chốt courseId:int64 carrier and direct-owner versus assigned-Mentor policy.
- [ ] Flow owner resolve inventory versus AC-26 sequence.
- [ ] Define loaded chart layout, auth/session/network UX, freshness/retention and client route.

**Kết luận:** ME-18 được đặc tả theo evidence hiện có nhưng chưa DD READY vì response, KPI, period, empty/ETL meaning và loaded chart design chưa thể triển khai mà không suy đoán. IMPLEMENTATION BLOCKED và RUNTIME NOT VERIFIED được ghi độc lập.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 6. Blockers and status criteria

- Catalog/diagram Page<Course> conflicts with local summary response.
- Inventory does not define KPI names/formulas, time window, aggregation, no-data meaning or export contract; #66 cannot populate completion/average-duration/discussion KPIs.
- AC requests learning-event aggregation while current-state lesson_progress cannot recover event history.
- Course ID carrier and ownership policy (direct owner versus assigned Mentor) are not resolved; Study Web route/auth/client remains UNWIRED.
- “Inactive ETL” and “ready schema” claims have no API/source fields; zero/null summary cannot identify a pipeline status.
- Do not claim DD READY while response/KPI/period/loaded visual choices require product/API decisions. Expected result is DD BLOCKED and IMPLEMENTATION BLOCKED, independently of RUNTIME NOT VERIFIED.
- Verification is static only: preserve source hashes, check 35 marker IDs/order/bounds and one-to-one DD rows, parse JSON/SVG/PNG, resolve local links, inspect annotated image, update trackers/worklog and run git diff --check. Do not run application tests/runtime.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
