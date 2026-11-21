# ME-03 — Business Rules

## 1. Rule index
| Rule ID (package alias) | Tên / source ID | Áp dụng | Thực thi | Tests |
|---|---|---|---|---|
| `ME-03-BR-001` | Source rules/gates bundle (alias only) | See source DD | Not re-inferred | See source acceptance |

## 2. Rules, security, discrepancy và gate từ source
- Inventory purpose: Tổng quan cây nội dung, tiến độ lớp, hành động tạo bài giảng.
- Gate/status (giữ nguyên): **D**
- BR IDs trong file này chỉ là alias trỏ tới source rule/gate bundles; không thêm business rule. Không khẳng định rule FE/BE mới khi source chưa xác nhận.

### Trích từ DD nguồn: 6. Điều hướng và bảo mật

| From → To | Route/context | Trạng thái |
|---|---|---|
| ME-02 → ME-03 | `/mentor/courses/:courseId`; pass integer Course ID từ item đã chọn. | Route proposal; ME-02/#46 chỉ list trực tiếp owned courses hiện nay. Assignment semantics còn discrepancy. |
| ME-03 → ME-04 | `/mentor/courses/:courseId/lectures/new`. | Inventory link; target DD riêng. |
| ME-03 → ME-06 | `/mentor/courses/:courseId/content`. | Inventory link; target DD riêng. |
| ME-03 → ME-16 | `/mentor/courses/:courseId/progress`. | Inventory link; target DD riêng. |
| ME-03 → ME-09 / ME-14 / schedule / activity / repository / AI | Prototype labels/actions. | Chưa được ME-03 inventory xác nhận hoặc thiếu destination/data policy. |

- Không serialize JWT vào URL; không dùng `courseId` do client tự quyết để cấp quyền. Cả #49/#65 verify role và direct owner phía server.
- AC-22/AC-26 nêu quyền quản lý/xem analytics; current role guard chưa có fine-grained permission check. Cần quyết định role/permission matrix và assigned Mentor access trước implementation.
- #65 trả tên và optional avatar của từng Student; chính sách roster visibility, export, analytics logging, retention và privacy chưa được catalog xác nhận. Không log JWT, payload Content hoặc raw progress rows ở browser logs.
- Checked-in DDL/migrations là local source artifact. Không tuyên bố production schema/deployment hoặc roster freshness đã kiểm chứng.

### Trích từ DD nguồn: 7. Responsive, accessibility và visual target

- Dùng `.agents/web-study/design.md` khi thiết kế FE: `ocean-primary #0B5F8A`, Inter/system sans, max content width khoảng 1120px, gutters responsive, mobile <768px, controls ≥44px, focus-visible rõ, motion tôn trọng reduced motion.
- Prototype dùng remote Plus Jakarta Sans và Tailwind CDN, `#2563EB`/màu khác, layout KPI dày, header button 40px và anchors không có destination. Không chuyển các token này thành current Study Web implementation.
- Đảm bảo semantic buttons/links, accessible names cho icon actions, labels cho search, heading order, contrast, keyboard tab sequence, focus visibility và reflow 320px trước khi implementation được mở.
- Progress/risk/status phải có text/icon và alternative cho chart; màu xanh/vàng/đỏ không là tín hiệu duy nhất. Empty/loading/error/partial copy phải phản ánh response thật.

### Trích từ DD nguồn: 8. Blockers và quyết định còn mở

| ID | Blocker | Bằng chứng / quyết định cần có |
|---|---|---|
| ME03-B01 | Access scope | AC-21 assignment vs API #46/#49/#65 direct owner; AC-22 management vs AC-26 analytics permission; chốt owner/assignment and fine-grained permission. |
| ME03-B02 | Course hero source | Chọn API/approved route-state for code, cohort, standard, enrolled count, update time, course status and title on direct entry/refresh. |
| ME03-B03 | API #65 contract | Owner approve local `MentorStudentProgress` schema or update catalog; define bound/pagination, roster eligibility, progress denominator/rounding/missing row/empty lessons. |
| ME03-B04 | Content structure | Define `ContentType`, `ContentStatus`, payload subtypes, revision selection and mapping to sections/lessons; current response flat and includes all statuses. |
| ME03-B05 | Analytics/risk/feed/quality | Approved APIs or explicit removal of per-module, at-risk, activity, review/drop-off and cohort widgets; define formulas/period/permissions. |
| ME03-B06 | Resource/AI/export | Resolve resource destinations and URL policy, AI product/data/consent contract, Excel format/API/download lifecycle. |
| ME03-B07 | Interactions/destinations | Approve ME-09/ME-14 scheduling/activity/rubric navigation, courseId/state handoff and action enablement. |
| ME03-B08 | Study Web wiring | App source, auth/session/router, API client, error/partial/cache/retry/accessibility implementation. |
| ME03-B09 | Visual conformance | Apply Study design target and approve loaded/empty/mobile layouts; supplied mockup is not token/accessibility conformant. |

**Readiness:** `DD BLOCKED` until unresolved business/data grains and interaction boundaries are decided or excluded from this screen. `IMPLEMENTATION BLOCKED` remains a separate delivery status. `RUNTIME NOT VERIFIED` remains separate evidence status.

## 3. Quy tắc chưa xác nhận
- `CẦN_XÁC_NHẬN`: các quyết định/blocker trong inventory và DD nguồn chưa được giải quyết.
- Related IDs/source refs: Không có BR ID nguồn được chuẩn hóa.; xem [API](04-api-integration.md), [Events](02-events.md), [Tests](07-test-cases.md).
