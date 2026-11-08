# ME-16 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ME-16-TC-001` | Planning ref / not run | `AC-26` | See source acceptance section | P2 |

## 2. Test planning references

### ME-16-TC-001 — Acceptance planning reference (AC-26)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-16](../../screen_stitch/04_mentor/ME-16_tien-do-toan-khoa-hoc/ME-16.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-26`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-16_tien-do-toan-khoa-hoc/ME-16.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Có ảnh nguồn `screen.png` giữ nguyên; baseline SHA-256 được ghi trong plan/worklog.
- [x] Có `ME-16_PLAN.md` trước marker map và DD.
- [x] Có annotated image với marker liên tục từ `#1` đến `#42`; JSON dùng cùng IDs và tọa độ trong 1600×1440.
- [x] Mỗi marker có một dòng element tương ứng; 42 element có loại, mục đích/vị trí, nguồn, trạng thái/thuộc tính và event hoặc ghi rõ không có event.
- [x] Event có input, precondition, processing order, API/source, success/error/edge output; prototype behavior tách khỏi behavior dự kiến.
- [x] #65 route/auth/path/response/eligibility/formula/errors đối chiếu local source và catalog; test source được đọc nhưng không chạy.
- [x] #67 handoff và #66 analytics boundary được nêu riêng; AC-26 discrepancy giữ nguyên, chưa tự reconcile.
- [x] Loading/ready/empty/denied cùng not-found/error/current cosmetic refresh được phân biệt; điều hướng và ID handoff được liệt kê.
- [x] Unsupported copy, route, data field, threshold, refresh policy, schema/deployment và auth UX được ghi là static/unwired/blocker.
- [ ] Product/domain owner xác nhận #65 response, assigned-vs-owner permission, course ID mapping, roster bound, filters/search/reminder definitions và AC-26 ordering.
- [ ] Study Web route/client/runtime và live schema/deployment được xác minh.

**Kết quả:** `DD READY`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Các checklist chưa tick là phụ thuộc triển khai/owner; chúng không bị xem là đã giải quyết bởi tài liệu này.

#### Kế hoạch kiểm chứng từ source PLAN

> CẦN_XÁC_NHẬN: Plan nguồn không có section verification/test được nhận diện.


- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
