# ME-06 — Cây nội dung khóa học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-06` |
| Module | Mentor |
| Route | `/mentor/courses/:courseId/content` — registered in `mentor.route.ts` |
| Actor/role | Mentor; #49 validates role `MENTOR` and direct course ownership. |
| DD status | Partial implementation of #49-backed content tree. Full Stitch filters, expand/collapse, reordering and analytics remain blocked by missing contract/source. |
| Runtime status | `RUNTIME NOT VERIFIED`; local source does not prove deployed API, live DB or browser behavior. |
| Version / last updated | 0.2 / 2026-11-20 |
| Sources | [Stitch screen](../../screen_stitch/04_mentor/ME-06_cay-noi-dung-khoa-hoc/ME-06.md), [screen inventory](../../list_screen.md), [API #49 DD](../../../../study-server/docs/dd/49_mentor_content_list/02_Overview.md) |

## 1. Mục tiêu và phạm vi

GET #49 trả danh sách phẳng `Content[]`. ME-06 xác thực từng node và dùng `parent_id` để dựng thứ tự cha-con, giữ `id`, `status`, `order` và các field khác từ response. Không suy diễn type/status label, payload subtype, version, counts, lesson duration hoặc course KPI.

## 2. Luồng và quyền

- Route param `courseId` phải là positive int64 an toàn trước khi gọi #49.
- API #49 yêu cầu Mentor role và direct owner; chỉ sau phản hồi hợp lệ mới hiển thị link thêm nội dung, sửa, hành động và về workspace.
- #49 trả 200 `DESIGN_RESOURCE_RETRIEVED` với toàn bộ node active, kể cả status khác nhau; empty array là kết quả hợp lệ. Query hiện order theo `parent_id NULLS FIRST, content_order ASC, id ASC`.
- 401/403/404/500 được tách khỏi ready/empty; lỗi có retry. Thay course ID hủy request trước để không trộn dữ liệu.
- ME-07/#50/#51 và ME-08/#52/#53 là các flow riêng. ME-06 không gọi reorder route, không cập nhật status và không tạo node con bằng cách suy đoán.

## 3. Hành vi Study Web hiện tại

- Route param reactive; stale reads bị hủy; component teardown đóng subscription.
- Client kiểm tra envelope, exact success business code, `course_id`, unique safe IDs, `content_type`, title, object `payload`, status, int32 `order`, parent tồn tại và không cycle.
- Client dựng danh sách cây từ flat rows theo parent, giữ thứ tự sibling do API trả; padding hiển thị có giới hạn để tránh tràn ngang. Hai action link mỗi row dùng hit area ≥44px theo accessibility rule của inventory và có thể wrap khi hẹp.
- Có invalid-ID, loading, not-found, forbidden, recoverable error/retry, empty và ready states. Add/edit/action links chỉ hiện sau #49 success.
- Design-only search/status filters, expand/collapse, reorder, chapter/quiz/lab-specific fields, KPI/chart/audit panels vẫn chưa được triển khai.

## 4. Trạng thái và bằng chứng

| Hạng mục | Trạng thái |
|---|---|
| Route/API #49 source wiring | Client route/caller và server route/module/query/validation/test source có trong checkout; API descriptor `WIRED`; deployment chưa xác minh. |
| UI/UX | Có danh sách cây cha-con, empty/error/loading/404/403/retry và navigation; còn thiếu các panel/controls của Stitch. |
| Logic | Course/response/tree integrity được kiểm tra; thứ tự giữ theo API. Reorder/status filtering và assigned-course permission còn thiếu. |
| Tỷ lệ hiện tại | 75% trong [`screen_complete.md`](../../screen_complete.md) — UI 50%, UX 75%, logic 75%, API 100%. |
| API/database | API #49 DD còn Draft; live migration/schema và browser runtime chưa xác minh. |

## 5. Liên kết tài liệu

[UI elements](01-ui-elements.md) · [Events](02-events.md) · [Data flow](03-data-flow.md) · [API integration](04-api-integration.md) · [Business rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test cases](07-test-cases.md)

## 6. Change log

- 2026-11-21 — Tăng action link của từng node lên hit area tối thiểu 44px và cho phép nhóm action wrap trên viewport hẹp; route/API/tree behavior không đổi.
- 2026-11-20 — Reconciled ME-06 DD with the registered route, #49 caller and current tree rendering. API #49 is locally source-wired; API DD and deployed runtime remain unverified.
