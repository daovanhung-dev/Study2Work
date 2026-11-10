# AD-10 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-10-TC-001` | Planning ref / not run | `AC-33` | See source acceptance section | P1 |

## 2. Test planning references

### AD-10-TC-001 — Acceptance planning reference (AC-33)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-10](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/AD-10.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-33`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-10_hang-doi-kiem-duyet-noi-dung/AD-10.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Có asset gốc `screen.png` và HTML `code.html`; giữ nguyên hash nguồn.
- [x] Annotated image và JSON marker map có 39 số tuần tự, duy nhất; mỗi marker có đúng một hàng ở C.
- [x] Mô tả expected AC/catalog tách khỏi current prototype/server source.
- [x] EV-01…EV-08 nêu trigger, input, xử lý hiện tại/target có căn cứ, API boundary, output và lỗi/điều kiện mở tương ứng.
- [x] Có states/navigation table, handoff ID và dependency AD-11.
- [x] Local links, JSON/SVG, dimensions, coordinates/bounds và ảnh annotated đã kiểm tra tĩnh/visual.
- [ ] Contract owner giải quyết Page-vs-single Content, pagination/order/error 422 và ContentType values.
- [ ] API/AC cung cấp hoặc loại bỏ author/course-name/submitted-time/version cần cho table/review; chốt stale/deleted visibility.
- [ ] Chốt moderation permission, live schema/deployment và Study Web route/client wiring.
- [ ] DD đủ để lập trình viên triển khai mà không tự suy diễn các quyết định mở. Hiện chưa đạt.

### Quyết định và blocker cần xử lý trước implementation

1. **Response cardinality:** catalog/AC #78 singular Content so với queue và current Page; owner phải đồng bộ contract.
2. **Filters/pagination/errors:** chốt enum/casing, `all` mapping, course ID option source, keyword search, page size/order/default và 422 contract.
3. **Table metadata:** xác định có bổ sung API projection/joins hay bỏ/đổi cột course name, lecturer, submitted time; không tự tổng hợp từ `payload`.
4. **Revision:** chốt current vs submitted version, identity cho #79–#81, stale queue behavior và deleted-content visibility.
5. **Permission/schema:** chốt moderation-specific permission nếu cần; xác nhận live DB/schema thay vì suy luận từ legacy DDL hoặc V1-PILOT.
6. **Frontend/runtime:** wire route, auth/client, loading/empty/error state, filters, pagination, refresh, row navigation, return/reload, accessibility và polling nếu có approved requirement.

**Trạng thái:** `DD BLOCKED` · `IMPLEMENTATION BLOCKED` · `RUNTIME NOT VERIFIED`. API #78 có current route/module/test source (`R` ở source index sau cập nhật), nhưng API DD còn Draft và local fake-database evidence không xác nhận live deployment/schema/policy. Không có application tests/runtime được chạy trong phiên này.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 7. Execution and verification order

1. [x] Docs preflight; exact-type selector and three selected worklogs recorded/read; context map, scope pages and registry consulted.
2. [x] Review AD-10 assets/DOM, AC-33, API catalog/DD/open questions, #78 current route/module/query/model/validator/test source, related Content/#79 projections and checked-in schema candidates.
3. [x] Save this plan before marker JSON/SVG, annotated PNG or screen DD.
4. [x] Create 39 ordered JSON/SVG markers and 2× annotated PNG; review image visually.
5. [x] Author A–F DD, 39 element rows, EV-01…EV-08, API/error trace, states/navigation and blockers.
6. [x] Update AD-10 and reverse API #078 source status plus global tracker/checkpoint.
7. [x] Static audit: source hashes/dimensions, JSON/XML, marker order/coordinates/bounds and C-row bijection, local links, inventory/folder/core-artifact counts, whitespace and final image. Do not run application tests/runtime.
8. [x] Finalize worklog and stop after AD-10; AD-11 remains a separate session.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
