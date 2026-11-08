# AD-19 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-19-TC-001` | Planning ref / not run | `AC-36` | See source acceptance section | P1 |

## 2. Test planning references

### AD-19-TC-001 — Acceptance planning reference (AC-36)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-19](../../screen_stitch/05_admin/AD-19_danh-sach-thong-bao-quan-tri/AD-19.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-36`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-19_danh-sach-thong-bao-quan-tri/AD-19.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

### Artifact và truy vết

- [x] 48 marker tuần tự/unique có trong JSON, SVG và DD; tọa độ dùng nguồn 1600×1411.
- [x] screen.png giữ nguyên; screen_annotated.png là 3200×2822 và đã visual review.
- [x] Mỗi marker ánh xạ tới đúng một element row; element/event IDs được liệt kê rõ.
- [x] Có plan trước khi tạo markers, image annotation và DD.
- [x] Inventory/AC/catalog/current source/test evidence được dẫn; expected và current không bị nhập làm một.

### Logic và contract

- [x] Có event load, search, filter, reset, refresh, CTA, row handoff, pagination, guidelines và shell navigation.
- [x] API #92 direct response/errors được tách khỏi Page/error behavior của current source.
- [x] Không tự thêm search query, metrics API, recipient field, status/channel alias, policy rule hoặc route.
- [x] Empty/loading/ready/error/auth/permission/pagination/navigation states và unresolved handoff được ghi.
- [ ] Owner xác nhận singleton vs Page, pagination, enum/filter/search/metrics, permission/grain/schema, CTA/guidelines route và operation bridge.
- [ ] Study Web route/API client, live DB/migrations, runtime permission and response behavior được xác minh.
- [ ] Do các mục blocker còn mở, DD status chưa đạt DD READY; implementation và runtime chưa verified.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: Source review and order

1. Inventory row 77, API reverse index #092 and G-12 in apps/study-client/docs/list_screen.md; global AD-19 row and 71/83 checkpoint in dd_screens/PLAN.md.
2. AC-36 admin management diagram and direct API catalog row #92 in docs/lists/list_api.md.
3. API #92 Draft DD, open questions and AC-36 macro-review; preserve owner-confirmation status.
4. Current implementation trace: apps/study-server/app/api/v1.py → api_92_admin_notifications_list/validate.py → query.py/models.py → view.py; check focused test source, not run it.
5. Checked-in legacy DDL and migration 009 only as schema candidates; keep V1-PILOT UUID model separate.
6. Inspect current Study Web tree, exact HTML handlers/links and source screenshot; compare only to .agents/web-study/design.md for design rules.
7. Source review is recorded in the active worklog. This plan must be saved before creating marker JSON/SVG, annotated PNG or AD-19.md.

### Trích từ DD nguồn: Acceptance audit to perform

- [x] Keep source screen.png and code.html hashes unchanged.
- [x] Create sequential unique markers with in-bounds coordinates and one row per marker.
- [x] Ensure JSON, SVG and DD coordinates agree; annotated PNG is 3200×2822 and visually reviewed.
- [x] Complete DD sections A–F with ordered event flows, exact catalog contract, separate local-source behavior and blockers.
- [x] Validate all relative links and element/event IDs; verify inventory/folder count remains 83/83 and core artifact count advances 71/83 → 72/83.
- [x] Update inventory row 77, reverse #092, G-12 and global plan/checkpoint; do not edit AD-20/AD-21 screen files.
- [x] Run static artifact checks and git diff --check; no application tests/runtime in this documentation turn.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
