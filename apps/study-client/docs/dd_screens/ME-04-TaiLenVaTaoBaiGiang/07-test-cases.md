# ME-04 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ME-04-TC-001` | Planning ref / not run | `AC-21` | See source acceptance section | P1 |

## 2. Test planning references

### ME-04-TC-001 — Acceptance planning reference (AC-21)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-04](../../screen_stitch/04_mentor/ME-04_tai-len-va-tao-bai-giang/ME-04.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-21`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-04_tai-len-va-tao-bai-giang/ME-04.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: 9. Acceptance checklist

- [x] Screen ID, route proposal, actor, links, source image/hash and inventory behavior are recorded.
- [x] Plan precedes marker JSON, SVG, annotated image and DD.
- [x] 60 unique ordered markers map to plan, JSON, SVG and this element matrix; original PNG/HTML preserved.
- [x] Every screen action/group has an event or an explicit no-event/source-gap note.
- [x] API #34/#46/#47/#48 route/source, request/response, auth, side effects and errors are traced.
- [x] Expected/current behavior and source/catalog/DD/live-schema boundaries remain separate.
- [x] Error/loading/upload/create/navigation/cancel states and cross-screen handoffs are recorded.
- [ ] Ownership, content, lifecycle, order, missing fields, upload cleanup and live schema decisions are resolved.
- [ ] Study Web route/runtime is implemented and verified.

#### Kế hoạch kiểm chứng từ source PLAN

> CẦN_XÁC_NHẬN: Plan nguồn không có section verification/test được nhận diện.


- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
