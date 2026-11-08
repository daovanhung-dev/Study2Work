# ME-11 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ME-11-TC-001` | Planning ref / not run | `AC-24` | See source acceptance section | P2 |

## 2. Test planning references

### ME-11-TC-001 — Acceptance planning reference (AC-24)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-11](../../screen_stitch/04_mentor/ME-11_hop-thu-ho-tro-hoc-vien/ME-11.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-24`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-11_hop-thu-ho-tro-hoc-vien/ME-11.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Screen ID, role, proposed route, prior/next screens and API boundaries identified.
- [x] Expected behavior and current source/runtime evidence kept separate.
- [x] 33 sequential markers in JSON/overlay/annotated PNG map one-to-one to 33 DD rows.
- [x] Six identified events include inputs, current behavior, processing/result, error/edge handling, and unresolved decisions.
- [x] API #58 route, query/auth/ownership, data mapping, order, error codes, transaction behavior and source trace recorded.
- [x] Empty, ready, auth, access, validation, error, filter, refresh and navigation states documented; unresolved ones remain explicitly blocked.
- [x] Source `screen.png` and `code.html` preserved; artifact dimensions/source hashes included in plan/worklog.
- [x] Relative source and cross-screen links checked during static audit.
- [ ] Loaded request-row presentation, status grouping/counts and course-option mapping approved.
- [ ] AC-24 empty-state precondition reconciled with inventory/mockup.
- [ ] SLA, real-time notification, canned answer and meeting claims verified or revised.
- [ ] Study Web route/session/client API integration implemented and runtime verified.
- [ ] Live migration/schema deployment verified; API #58 fallback decisions approved by contract owner.

**Kết luận:** artifacts của empty state và API source trace đã hoàn thiện; ME-11 còn `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` cho tới khi các open decision chính được giải quyết. Màn hình tiếp theo theo luồng Mentor là ME-12 trong một phiên riêng.

#### Kế hoạch kiểm chứng từ source PLAN

> CẦN_XÁC_NHẬN: Plan nguồn không có section verification/test được nhận diện.


- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
