# ME-01 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `ME-01-TC-001` | Planning ref / not run | `AC-21` | See source acceptance section | P1 |
| `ME-01-TC-002` | Planning ref / not run | `AC-23` | See source acceptance section | P1 |
| `ME-01-TC-003` | Planning ref / not run | `AC-24` | See source acceptance section | P1 |

## 2. Test planning references

### ME-01-TC-001 — Acceptance planning reference (AC-21)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-01](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-21`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01.md).
### ME-01-TC-002 — Acceptance planning reference (AC-23)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-01](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-23`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01.md).
### ME-01-TC-003 — Acceptance planning reference (AC-24)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [ME-01](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-24`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: 11. Tiêu chí nghiệm thu

- [x] Source PNG/HTML được giữ nguyên; mọi số liệu nhìn thấy được gọi là sample/design content.
- [x] Mỗi marker `#1–#23` có một element ID duy nhất và một hàng đặc tả; mọi nhóm controls được liệt kê.
- [x] API #46/#54/#58 được trace route → guard → view/query/mapper → response/error; API current source tách khỏi API DD/catalog snapshot.
- [x] Event có trigger, input, precondition, xử lý tuần tự, response/route output và ngoại lệ hoặc blocker.
- [x] States, access control, linked screens và thông tin cần truyền được ghi riêng.
- [ ] Product/API blockers B01–B12 được resolve; chỉ khi đủ nguồn mới xét `DD READY`.
- [ ] Study Web route/session/UI được implement và kiểm chứng; chỉ khi có runtime evidence mới xét `RUNTIME VERIFIED`.

### Trích từ DD nguồn: 12. Rà soát tĩnh artifact

- `screen.png`: nguồn 1086×1600; hash gốc giữ nguyên.
- `screen_annotated.png`: tỉ lệ giữ nguyên, canvas 2172×3200 (2×).
- `ME-01_markers.json`: 23 marker liên tiếp; tọa độ gốc pixel, origin top-left; target element IDs `ME01-EL-01..23`.
- [Kế hoạch riêng](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01_PLAN.md), [marker map](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01_markers.json), [SVG overlay](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01_markers_overlay.svg), [ảnh có đánh số](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/screen_annotated.png).
- `RUNTIME VERIFIED` không được suy ra từ ảnh, HTML, API source hay tests source.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 2. Kế hoạch rà soát tài sản

- `screen.png`: PNG hợp lệ 1086×1600, RGB; SHA-256 `f135d0b109a05d276654a6b8b51545d9f2996ab474c47b7829c9983739eea3d2`.
- `code.html`: HTML tĩnh 52,234 bytes; SHA-256 `f10dfa929e89288165bf0264b1b1f863f2380006d064f8e470118a7cfe626334`.
- PNG và HTML thể hiện cùng dashboard nhiều cột: header mentor, welcome/on-call, bốn KPI, danh sách bài nộp, khóa học, hỗ trợ, lịch 1-on-1, thông báo học vụ và footer. Các tên, điểm số, số lượng, SLA, lịch hẹn, đường dẫn Meet và thông báo là dữ liệu minh họa trong asset, không phải dữ liệu runtime.
- HTML dùng anchor `href="#"`, có input tìm kiếm và button tĩnh nhưng không có client handler/API/router. Tất cả placeholder destinations, số liệu minh họa, external font/CDN và màu xanh `#004ac6` cần đối chiếu với source/Study Web design guide; không sửa PNG/HTML.
- PNG hiện dùng được; không cần dựng `screen_rendered.png`. Dùng PNG nguyên trạng làm nền chú thích.

### Trích từ DD nguồn: 7. Blockers and status criteria

- `IMPLEMENTATION BLOCKED`: Student Web route/session source is absent; role bootstrap/handoff into a Mentor shell is not verified; display mapping is incomplete for dashboard sample data; per-row direct navigation conflicts with inventory/AC flow; #58 returns an unpaginated full thread collection; unreferenced schedule/rating/announcements/unread features lack approved data/routes; checked-in DB artifacts do not prove live schema.
- `DD BLOCKED`: keep only screen fields with source trace implementable; unresolved visual/sample fields, direct detail CTA routes, retry/cache behavior, query/loading policy and list content design require product/API decisions. Do not fabricate replacements.
- `RUNTIME NOT VERIFIED`: no Study Web runtime is present, and no live deployed UI/API/database check is performed in this docs task.
- No API, field, table, business rule, external provider or destination will be added by this session.

### Trích từ DD nguồn: 8. Output and review checklist

- [x] Complete plan and read source/API/AC before authoring the DD or marker image.
- [x] Preserve source hashes; create `ME-01_markers.json`, `ME-01_markers_overlay.svg`, and `screen_annotated.png` without editing originals.
- [x] Write `ME-01.md` with overview, full flow, marker-to-element map, event input/process/output/API details, state/navigation matrix, blockers, traceability and acceptance criteria.
- [x] Verify marker IDs `1..23` map once to DD elements; inspect image and link targets; check PNG dimensions/ratio and source hashes.
- [x] Update global `dd_screens/PLAN.md` and worklog with results; next screen is ME-02 in a separate session.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
