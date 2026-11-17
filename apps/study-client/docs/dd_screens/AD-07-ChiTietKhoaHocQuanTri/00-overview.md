# AD-07 — Chi tiết khóa học quản trị · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-07` |
| Module | Admin |
| Route | `/admin/courses/:courseId` — route đã khai báo trong Angular Admin router; runtime/deployment chưa xác minh |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); **DD:** `BLOCKED` · **Implementation:** `PARTIAL SOURCE — route/page and GET #74 caller exist; actions to #75/#76/#77 and AD-12 handoff remain unavailable` · **Study Web runtime:** `NOT VERIFIED` |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-16 (current-source sync and ID label correction) |
| Nguồn đối chiếu | [AD-07.md](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/AD-07.md), [AD-07_PLAN.md](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/AD-07_PLAN.md), [AD-07_markers.json](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/AD-07_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Xem Course metadata/owner/status fields returned by #74; do not show counters unless their contract is added.
- In-scope: GET #74 with numeric `Course.id`; do not use public GET #8. AC-32 then branches to #75/#76/#77. API #82 supports `course?:int64`, making `/admin/lessons?course=<Course.id>` a handoff candidate pending route approval and #82 response-contract resolution.
- Out-of-scope: Xem gate bên dưới; không suy ra downstream action/handoff hoặc runtime/deployment đã được xác minh.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-32 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Xem Course metadata/owner/status fields returned by #74; do not show counters unless their contract is added. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #74
- Liên kết màn hình dự kiến: [AD-08](../AD-08-ChinhSuaKhoaHoc/00-overview.md), [AD-09](../AD-09-ThayDoiTrangThaiXoaKhoa/00-overview.md), [AD-12](../AD-12-DanhSachBaiHocQuanTri/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | initial/loading/ready/404/unauthorized/forbidden/service-error |
| Current source | Angular Admin route/page and GET #74 caller | Route/page exists; page state is `loading/loaded/error`; action buttons are disabled. Runtime/deployment: `NOT VERIFIED`. |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-07 source screen.png](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/screen_annotated.png))
- Luồng: GET #74 with numeric `Course.id`; do not use public GET #8. AC-32 then branches to #75/#76/#77. API #82 supports `course?:int64`, making `/admin/lessons?course=<Course.id>` a handoff candidate pending route approval and #82 response-contract resolution.
- Priority: P1; Gate/source status: **R** source/API #74 route/module/test; API DD `Draft — Needs Confirmation`; **DD BLOCKED; WRITE FLOW BLOCKED:** counter definition, AC-32 permission mapping, singleton Page/live schema, prototype-only course code/metrics/curriculum/quality claims, AD-12 query-route approval/#82 `Lesson` vs `Lesson[]` response remain open; current route/page/#74 caller exist; **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.
- 2026-11-16 — Đồng bộ trạng thái source: route/page và GET #74 caller có thật; action downstream vẫn disabled. Đổi nhãn field hiển thị từ mã khóa học sang ID khóa học.

## Trạng thái và ranh giới bằng chứng

# AD-07 — Chi tiết khóa học quản trị

> **Detailed Design:** `DD BLOCKED` · **Implementation:** `PARTIAL SOURCE` · **Study Web runtime:** `NOT VERIFIED`<br>
> **Screen:** AD-07 · **Actor:** Admin · **Route:** `/admin/courses/:courseId` (declared in Angular Admin router) · **AC:** AC-32 · **API chính:** #74<br>
> **Assets:** [screen nguyên trạng](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/screen.png) · [screen đánh số](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/screen_annotated.png) · [marker map](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/AD-07_markers.json) · [kế hoạch](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/AD-07_PLAN.md)

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### Expected behavior

AD-07 là màn hình chi tiết khóa học quản trị được inventory đề xuất ở `/admin/courses/:courseId`. AC-32 yêu cầu Admin có quyền course management; flow từ AD-06 chuyển numeric `Course.id`, đọc GET #74, rồi mới chọn nhánh cập nhật #75, đổi trạng thái #76 hoặc xóa #77 theo policy. API #74 là read-only. AD-12 được inventory liệt kê như màn hình liên quan. API #82 catalog và local source hỗ trợ filter `course?:int64`, nên `/admin/lessons?course=<Course.id>` là handoff candidate có căn cứ kỹ thuật; inventory chưa nêu query route này và API #82 response cardinality còn open.

API catalog #74 khai báo `GET /api/v1/admin/courses/{course_id}` với Bearer JWT/Admin và `ApiEnvelope<Page<Course>>`. Các field Course trong catalog là `id`, `title`, nullable `description`, nullable `thumbnail_url`, decimal-string `price`, `status`, `mentor`, và optional `category`. Local #74 response model dùng chung `Course` nhưng hiện không có `category`; local SQL cũng không đọc category. Singleton `Page<Course>` là hành vi local implementation, chưa được xác nhận là cardinality cuối của contract API.

### Current behavior và trạng thái bằng chứng

| Chủ đề | Expected / contract | Current source hoặc prototype | Trạng thái |
|---|---|---|---|
| Route và entry | `/admin/courses/:courseId`, nhận numeric `Course.id` từ AD-06. | Angular router declares the route; AD07Page reads `courseId`, calls GET #74, and has a router link back to `/admin/courses`. The original HTML prototype back link remains `href="#"`. | Route/page/GET caller `PRESENT`; handoff/runtime remain unverified. |
| Quyền | AC-32 yêu cầu Admin có quyền course management; catalog ghi Bearer JWT/Admin. | Local #74 kiểm tra shared JWT role `ADMIN`; không kiểm tra permission course-management riêng. | Permission mapping `OPEN`. |
| Tải detail | GET #74 theo path `course_id:int64`. | Angular AD07Page calls GET #74 through AD07ApiService/AdminApiService with the route ID. | Client caller and API source present; API DD `Draft — Needs Confirmation`. |
| Course fields | Catalog dùng `Page<Course>`. | Local #74 trả một Course trong singleton page; query chỉ lấy course và mentor. | Singleton shape `DERIVED`; cần xác nhận trong API DD. |
| Counters | AC-32 diagram nói đọc course/owner/counters. | Không có counter field hoặc query trong catalog/model/query hiện hành. | `DISCREPANCY`; không render/tính counter. |
| Prototype | Detail fields, actions, states. | `code.html` là HTML tĩnh, blank metadata, hard-coded zero metrics, empty curriculum, quality statements, links `#`, ba nút AD-08/09/12 disabled; không có fetch/navigation handler. | Design artifact, không phải runtime. |
| Runtime | API/client hoạt động trong Study Web. | Source and HTTP fixture spec exist; no browser/deployment/live-schema verification was performed. | `NOT VERIFIED`. |

### Current Study Web source re-audit — 2026-11-16

- Angular route `/admin/courses/:courseId` loads `AD07Page`; the page calls GET #74 using the raw route string and exposes `loading/loaded/error` states. The current page renders the route value as `ID khóa học` (not a course-code field), title, mentor full name, price, status, thumbnail URL and description.
- The curriculum/lesson panel states #74 has no such source; AD-08, AD-09 and AD-12 buttons remain disabled. The page has a RouterLink back to AD-06; no #75/#76/#77/#82 caller exists in AD-07.
- `admin-detail-pages.spec.ts` covers GET #74, Bearer auth, fields, disabled actions and unsupported claims. Its AD-07 case was run after the ID-label correction: 1 file, 2 tests passed. Production build passed with existing CSS-budget warnings. Browser/runtime/deployment remains `NOT VERIFIED`.
- API #74 local singleton-page behavior is `DERIVED`; API DD stays Draft. Counter, permission, schema, status, and AD-12 handoff decisions remain open.

### Actor, điều kiện và liên kết

- **Actor:** Admin theo AC-32 và catalog #74. Quyền fine-grained `course management` chưa được đối chiếu với local role guard.
- **Điều kiện vào dự kiến:** Phiên có JWT hợp lệ; numeric `Course.id` được chọn ở AD-06 hoặc có trong route. API hiện không có positive-only path validation contract: parser local chấp nhận signed-int64, kể cả số âm; không áp đặt validation khác từ UI.
- **Dữ liệu đầu vào:** `courseId` route value → API `course_id`; không dùng nhãn “Mã khóa học” để dựng ID.
- **Kết quả thành công:** Lưu Course trong screen state và hiển thị các field có nguồn. GET không thay đổi dữ liệu, không ghi audit và không cần commit.
- **Điều hướng:** AD-06 quay lại danh sách; AD-08 sửa khóa bằng #75; AD-09 status/delete bằng #76/#77. API #82 hỗ trợ `course?:int64`; `/admin/lessons?course=<Course.id>` là handoff candidate, pending route decision and #82 cardinality resolution.
- **Nguồn chính:** [inventory](../../list_screen.md), [global DD plan](../../screen_stitch/dd_screens/PLAN.md), [AC-32 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio), [API catalog](../../../../../docs/lists/list_api.md), [API #74 route](../../../../study-server/app/api/v1.py), [API #74 query](../../../../study-server/app/modules/admin/api_74_admin_course_detail/query.py), [API #74 view](../../../../study-server/app/modules/admin/api_74_admin_course_detail/view.py), [shared Course model](../../../../study-server/app/modules/shared/course_catalog/models.py), [Course mapper](../../../../study-server/app/modules/shared/course_catalog/helpers.py), [API #74 DD/open questions](../../../../study-server/docs/dd/74_admin_course_detail/OPEN_QUESTIONS.md), [API #74 tests](../../../../study-server/tests/modules/admin/api_74_admin_course_detail/test_admin_course_detail.py), [API #82 filter source](../../../../study-server/app/modules/admin/api_82_admin_lessons_list/validate.py), [API #82 DD/open questions](../../../../study-server/docs/dd/82_admin_lessons_list/OPEN_QUESTIONS.md), [legacy candidate DDL](../../../../../infra/postgres/study-server/DB.sql), [Study Web context](../../../../../.agents/web-work/study/AGENTS.md).
