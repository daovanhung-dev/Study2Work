# AD-18 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-18-TC-001` | Planning ref / not run | `AC-35` | See source acceptance section | P2 |

## 2. Test planning references

### AD-18-TC-001 — Acceptance planning reference (AC-35)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-18](../../screen_stitch/05_admin/AD-18_xac-nhan-xoa-bai-kiem-tra/AD-18.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-35`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-18_xac-nhan-xoa-bai-kiem-tra/AD-18.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Có ảnh nguồn nguyên trạng, HTML nguồn; original hashes được ghi trong worklog.
- [x] Có 40 marker tuần tự trên ảnh đánh số; từng marker khớp một element row và marker JSON.
- [x] Ghi rõ route/UI hiện `UNWIRED`, mockup disabled/static và không có request handler.
- [x] Phân biệt AC-35/direct API catalog với local #90 branches; không coi local derived policy là approved.
- [x] Mô tả API method/path/auth/params/body/response/status/business codes; không tạo 409.
- [x] Ghi rõ target-data gap, permission gap, attempt race, lifecycle visibility và schema/runtime blockers.
- [x] Có state/navigation matrix, error/unknown-outcome handling limits và liên kết AD-15.
- [x] Giữ riêng trạng thái `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`.
- [ ] Owner duyệt no-attempt/answer-only/tombstone/race/permission/visibility policy; cần quyết định trước khi `DD READY`.
- [ ] Study Web route, selected-Quiz data handoff, action/error/recovery UI và cache invalidation được thiết kế/wire.
- [ ] Live schema/deployment và API contract/DD được xác minh/cập nhật trước runtime claim.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: Acceptance audit

- [x] Original `screen.png` 1600×1442 and `code.html` hashes stay unchanged.
- [x] Marker IDs 1–40 are sequential, unique, in-bounds, visually legible and map one-to-one to DD element rows.
- [x] SVG and JSON coordinates match DD; annotated PNG renders at 3200×2884 and has been visually reviewed.
- [x] DD includes A–F, detailed EV-01…EV-06, API #90 direct catalog vs local source, route/data mapping, error/status matrix and blockers.
- [x] Relative links resolve; screen inventory remains 83 IDs/folders; core artifact count increases by one (70/83 → 71/83).
- [x] Reverse API index #090, G-11, global AD-18 status/checkpoint and worklog reflect current evidence.
- [x] `git diff --check` and static artifact audit pass. App tests/runtime were not run for this documentation task.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
