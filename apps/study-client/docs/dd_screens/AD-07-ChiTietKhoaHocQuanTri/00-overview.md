# AD-07 — Chi tiết khóa học quản trị · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-07` |
| Module | Admin |
| Route | `/admin/courses/:courseId` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Detailed Design:** `DD BLOCKED` · **Implementation:** `IMPLEMENTATION BLOCKED` · **Study Web runtime:** `NOT VERIFIED` (`UNWIRED` in current checkout)<br> |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-07.md](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/AD-07.md), [AD-07_PLAN.md](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/AD-07_PLAN.md), [AD-07_markers.json](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/AD-07_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Xem Course metadata/owner/status fields returned by #74; do not show counters unless their contract is added.
- In-scope: GET #74 with numeric `Course.id`; do not use public GET #8. AC-32 then branches to #75/#76/#77. API #82 supports `course?:int64`, making `/admin/lessons?course=<Course.id>` a handoff candidate pending route approval and #82 response-contract resolution.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

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
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-07 source screen.png](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/screen_annotated.png))
- Luồng: GET #74 with numeric `Course.id`; do not use public GET #8. AC-32 then branches to #75/#76/#77. API #82 supports `course?:int64`, making `/admin/lessons?course=<Course.id>` a handoff candidate pending route approval and #82 response-contract resolution.
- Priority: P1; Gate/source status: **R** source/API #74 route/module/test; API DD `Draft — Needs Confirmation`; **DD BLOCKED; IMPLEMENTATION BLOCKED:** counter definition, AC-32 permission mapping, singleton Page/live schema, prototype-only course code/metrics/curriculum/quality claims, AD-12 query-route approval/#82 `Lesson` vs `Lesson[]` response, and Study Web `UNWIRED` remain open; **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-07 — Chi tiết khóa học quản trị

> **Detailed Design:** `DD BLOCKED` · **Implementation:** `IMPLEMENTATION BLOCKED` · **Study Web runtime:** `NOT VERIFIED` (`UNWIRED` in current checkout)<br>
> **Screen:** AD-07 · **Actor:** Admin · **Route đề xuất:** `/admin/courses/:courseId` · **AC:** AC-32 · **API chính:** #74<br>
> **Assets:** [screen nguyên trạng](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/screen.png) · [screen đánh số](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/screen_annotated.png) · [marker map](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/AD-07_markers.json) · [kế hoạch](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/AD-07_PLAN.md)

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### Expected behavior

AD-07 là màn hình chi tiết khóa học quản trị được inventory đề xuất ở `/admin/courses/:courseId`. AC-32 yêu cầu Admin có quyền course management; flow từ AD-06 chuyển numeric `Course.id`, đọc GET #74, rồi mới chọn nhánh cập nhật #75, đổi trạng thái #76 hoặc xóa #77 theo policy. API #74 là read-only. AD-12 được inventory liệt kê như màn hình liên quan. API #82 catalog và local source hỗ trợ filter `course?:int64`, nên `/admin/lessons?course=<Course.id>` là handoff candidate có căn cứ kỹ thuật; inventory chưa nêu query route này và API #82 response cardinality còn open.

API catalog #74 khai báo `GET /api/v1/admin/courses/{course_id}` với Bearer JWT/Admin và `ApiEnvelope<Page<Course>>`. Các field Course trong catalog là `id`, `title`, nullable `description`, nullable `thumbnail_url`, decimal-string `price`, `status`, `mentor`, và optional `category`. Local #74 response model dùng chung `Course` nhưng hiện không có `category`; local SQL cũng không đọc category. Singleton `Page<Course>` là hành vi local implementation, chưa được xác nhận là cardinality cuối của contract API.

### Current behavior và trạng thái bằng chứng

| Chủ đề | Expected / contract | Current source hoặc prototype | Trạng thái |
|---|---|---|---|
| Route và entry | Proposed `/admin/courses/:courseId`, nhận numeric `Course.id` từ AD-06. | Không có Study Web route/client; HTML back link dùng `href="#"`. | `UNWIRED`; route vẫn là proposal. |
| Quyền | AC-32 yêu cầu Admin có quyền course management; catalog ghi Bearer JWT/Admin. | Local #74 kiểm tra shared JWT role `ADMIN`; không kiểm tra permission course-management riêng. | Permission mapping `OPEN`. |
| Tải detail | GET #74 theo path `course_id:int64`. | Route/module #74 được đăng ký trong local server source; không có UI client gọi API. | API source `R`; API DD `Draft — Needs Confirmation`. |
| Course fields | Catalog dùng `Page<Course>`. | Local #74 trả một Course trong singleton page; query chỉ lấy course và mentor. | Singleton shape `DERIVED`; cần xác nhận trong API DD. |
| Counters | AC-32 diagram nói đọc course/owner/counters. | Không có counter field hoặc query trong catalog/model/query hiện hành. | `DISCREPANCY`; không render/tính counter. |
| Prototype | Detail fields, actions, states. | `code.html` là HTML tĩnh, blank metadata, hard-coded zero metrics, empty curriculum, quality statements, links `#`, ba nút AD-08/09/12 disabled; không có fetch/navigation handler. | Design artifact, không phải runtime. |
| Runtime | API/client hoạt động trong Study Web. | Study Web app source/package/router không có trong checkout hiện tại. | `NOT VERIFIED` / `UNWIRED`. |

### Actor, điều kiện và liên kết

- **Actor:** Admin theo AC-32 và catalog #74. Quyền fine-grained `course management` chưa được đối chiếu với local role guard.
- **Điều kiện vào dự kiến:** Phiên có JWT hợp lệ; numeric `Course.id` được chọn ở AD-06 hoặc có trong route. API hiện không có positive-only path validation contract: parser local chấp nhận signed-int64, kể cả số âm; không áp đặt validation khác từ UI.
- **Dữ liệu đầu vào:** `courseId` route value → API `course_id`; không dùng nhãn “Mã khóa học” để dựng ID.
- **Kết quả thành công:** Lưu Course trong screen state và hiển thị các field có nguồn. GET không thay đổi dữ liệu, không ghi audit và không cần commit.
- **Điều hướng:** AD-06 quay lại danh sách; AD-08 sửa khóa bằng #75; AD-09 status/delete bằng #76/#77. API #82 hỗ trợ `course?:int64`; `/admin/lessons?course=<Course.id>` là handoff candidate, pending route decision and #82 cardinality resolution.
- **Nguồn chính:** [inventory](../../list_screen.md), [global DD plan](../../screen_stitch/dd_screens/PLAN.md), [AC-32 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio), [API catalog](../../../../../docs/lists/list_api.md), [API #74 route](../../../../study-server/app/api/v1.py), [API #74 query](../../../../study-server/app/modules/admin/api_74_admin_course_detail/query.py), [API #74 view](../../../../study-server/app/modules/admin/api_74_admin_course_detail/view.py), [shared Course model](../../../../study-server/app/modules/guest/_shared/course_catalog/models.py), [Course mapper](../../../../study-server/app/modules/guest/_shared/course_catalog/helpers.py), [API #74 DD/open questions](../../../../study-server/docs/dd/74_admin_course_detail/OPEN_QUESTIONS.md), [API #74 tests](../../../../study-server/tests/modules/admin/api_74_admin_course_detail/test_admin_course_detail.py), [API #82 filter source](../../../../study-server/app/modules/admin/api_82_admin_lessons_list/validate.py), [API #82 DD/open questions](../../../../study-server/docs/dd/82_admin_lessons_list/OPEN_QUESTIONS.md), [legacy candidate DDL](../../../../../infra/postgres/study-server/DB.sql), [Study Web context](../../../../../.agents/web-work/study/AGENTS.md).
