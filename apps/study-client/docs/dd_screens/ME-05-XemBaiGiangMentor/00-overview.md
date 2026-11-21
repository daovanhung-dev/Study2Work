# ME-05 — Xem bài giảng mentor · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-05` |
| Module | Mentor |
| Route | `/mentor/lectures/:lectureId` — registered in `mentor.route.ts` |
| Actor/role | Mentor; `MentorApiService` obtains the Mentor token and API #48 validates role `MENTOR`. |
| DD status | Partial implementation of the source-backed detail flow; full Stitch mockup remains blocked by fields/actions without API contracts. |
| Runtime status | `RUNTIME NOT VERIFIED`; route source and local API code do not prove deployed API/live DB/browser behavior. |
| Version / last updated | 0.2 / 2026-11-20 |
| Sources | [Stitch screen](../../screen_stitch/04_mentor/ME-05_xem-bai-giang-mentor/ME-05.md), [screen inventory](../../list_screen.md), [API #48 DD](../../../../study-server/docs/dd/48_mentor_lecture_detail/02_Overview.md) |

## 1. Mục tiêu và phạm vi

Sau khi có `lectureId`, gọi GET #48 và hiển thị trường lecture, trạng thái, Markdown content dạng văn bản thuần, danh sách metadata asset và điều hướng tới workspace/cây nội dung theo `course_id`. Không thêm API sửa lecture, playback, download hoặc status mutation.

## 2. Use case và luồng vào

| Use case | Actor | Hành vi |
|---|---|---|
| AC-21 | Mentor | ME-04 chuyển `data.id` của #47 sang `/mentor/lectures/:lectureId`; ME-05 tải lại bằng #48. #47 hiện tạo `content:string` chứa Markdown và lưu nguyên văn; #48 vẫn cho phép `content:null` ở dữ liệu cũ. |

API #48 là read-only, yêu cầu role `MENTOR` và chỉ cho Mentor trực tiếp sở hữu course. AC-21 còn nhắc course được phân công; assignment authorization chưa có trong source và vẫn là discrepancy.

## 3. Hành vi hiện tại trong Study Web

- Route dùng `paramMap`; ID mới hủy request cũ. Retry tải lại ID hiện hành và subscription kết thúc cùng component.
- Trước khi hiển thị, client kiểm tra envelope, `DESIGN_RESOURCE_RETRIEVED`, response ID trùng route ID, course/lecture IDs, content, order, status và từng asset field.
- Có trạng thái invalid ID, loading, ready, not-found, forbidden, error, content rỗng/null và danh sách asset rỗng. HTTP 403 `DESIGN_ACCESS_DENIED` hiển thị thông báo không tiết lộ chi tiết lecture và link về danh sách khóa học; lỗi tải có thể thử lại.
- Nội dung Markdown được hiển thị trong `<pre>` với Angular text binding; không render HTML. Asset chỉ hiển thị tên, MIME, size và status; `url` từ API không được mở vì quyền/expiry/provider chưa xác minh.
- Khi có lecture hợp lệ, có link đến ME-03 và ME-06. Mockup player, analytics, discussion, chapter tree, copy, preview, edit và status controls chưa có nguồn dữ liệu/route/API tương ứng nên không được dựng như chức năng thật.

## 4. Trạng thái và bằng chứng

| Hạng mục | Trạng thái |
|---|---|
| Route/API #48 source wiring | Có trong Study Web source; API #48 handler có local source. Deployment/browser chưa xác minh. |
| UI/UX | Có trạng thái tải/lỗi/403/404, retry, breadcrumb, content và asset metadata responsive; chỉ bao phủ phần dữ liệu #48. |
| Business logic | Route ID, envelope, business code, identity và response fields được kiểm tra trước render; API server giữ quyền quyết định owner. |
| Design coverage | Partial: phần lớn vùng mockup không được #48 trả về hoặc thiếu contract. Giữ trạng thái 75% trong [`screen_complete.md`](../../screen_complete.md). |
| API/database runtime | Chưa xác minh live schema/migration, storage URL access hoặc môi trường deployed. API #48 DD còn Draft. |

## 5. Liên kết tài liệu

[UI elements](01-ui-elements.md) · [Events](02-events.md) · [Data flow](03-data-flow.md) · [API integration](04-api-integration.md) · [Business rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test cases](07-test-cases.md)

## 6. Change log

- 2026-11-21 — Tách HTTP 403 `DESIGN_ACCESS_DENIED` thành trạng thái không có quyền truy cập, không đưa retry cho quyền đã bị từ chối; các lỗi tạm thời vẫn có retry. Runtime và unsupported mockup areas remain unverified/blocked.
- 2026-11-20 — Reconciled the page with the registered Study Web route, API #48 caller, T041 Markdown contract and current rendered states. Runtime and unsupported mockup areas remain unverified/blocked.
