# ST-09 — Tổng quan khóa đang học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-09` |
| Module | Student |
| Route | `/student/courses/:courseId` — route/page gate có trong Angular; runtime chưa xác minh |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft; AC-18 lesson/quiz/assignment aggregate and safe course-learning tree remain blocked. Current source status: `IMPLEMENTATION PARTIAL`; route, #20 membership and #37 progress reads are source-wired; `RUNTIME NOT VERIFIED`. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.3 / 2026-11-21 |
| Nguồn đối chiếu | [ST-09.md](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/ST-09.md), [ST-09_PLAN.md](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/ST-09_PLAN.md), [ST-09_markers.json](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/ST-09_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Đề cương, tiến độ từng bài và CTA tiếp tục học.
- In-scope: Xác nhận course thuộc #20 → GET #37; GET #9 chỉ chứa phần public; lesson access #22 trước khi học.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-13,AC-18 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Đề cương, tiến độ từng bài và CTA tiếp tục học. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #09, #20, #37
- Liên kết màn hình dự kiến: [ST-10](../ST-10-KiemTraQuyenVaBatDauHoc/00-overview.md), [ST-21](../ST-21-TienDoTheoKhoaHoc/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | enrolled/not-enrolled/loading/no-lessons |
| Current source | Worklog/context Study Web | Route reacts to `courseId`; paged #20 confirms ACTIVE membership before #37. A matching course row remains usable when COUNT/LIST cardinality differs; if no match is returned on a mismatched page, enrollment stays unresolved with retry. No lesson tree or media data is rendered. |
| Runtime | Worklog/context Study Web | `NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-09 source screen.png](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/screen_annotated.png))
- Luồng: Xác nhận course thuộc #20 → GET #37; GET #9 chỉ chứa phần public; lesson access #22 trước khi học.
- Priority: P1; expected contract remains **DD BLOCKED**; current route, #20 membership and #37 progress callers are source-wired. #09 is source-backed/public; #22–#24 do not provide the course-learning tree in this screen. The catalog #37 response shape still differs from current source and current #37 counts PUBLISHED lessons only; **BLOCK:** Chưa có contract course-learning tree đầy đủ.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-09 — Tổng quan khóa đang học

> **DD status:** BLOCKED · **Implementation:** BLOCKED · **Runtime:** NOT VERIFIED

## Current implementation update — 2026-11-17

- `/student/courses/:courseId` mounts ST-09 behind `StudentLayout`. It paginates #20 with `status=ACTIVE` to confirm membership, then calls #37 for course-level lesson counts and percentage. The page does not use public #09 as an enrollment check or render sample lesson/media content.
- Current #20 projects enrolled `CourseSummary` rows and #37 projects course-level progress totals; neither has a focused test package. #09 remains public curriculum. A full course tree, per-lesson progress, and a safe ST-10 lessonId handoff are still unresolved; deployed API behavior has not been verified.

## Current-source reconciliation — 2026-11-20

The page now reacts to `courseId` changes and cancels stale #20/#37 requests.
#20 ACTIVE membership pages and #37 course identity/progress fields are
validated before render. Current #37 counts PUBLISHED lessons only, whereas
AC-18 describes lesson, quiz and assignment progress; no tree/lesson selection
or ST-10 handoff is implemented. The API catalog still declares `UserProfile`
for #20/#37; runtime remains unverified. Since #20 is queried with
`status=ACTIVE` and the page guard accepts only that enrollment state, the
course badge displays it as “Đang hoạt động” while leaving the API value
unchanged.
> **Phạm vi phiên:** ST-09. Tài liệu tách hành vi mong đợi khỏi bằng chứng hiện tại; asset tĩnh không xác nhận runtime.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-09 — Tổng quan khóa đang học (Page) |
| Mục tiêu mong đợi | Cho Student đã ghi danh xem đề cương khóa, tiến độ học và đi tới bài học hoặc chi tiết tiến độ theo AC-13/AC-18 và inventory. |
| Actor | Student đã đăng nhập theo AC-13, API #20 và #37. Guest hoặc Student chưa ghi danh không được xem nội dung học được bảo vệ; chính sách hiển thị chính xác đang chờ contract. |
| Route | `/student/courses/:courseId` is source-wired under the authenticated Student route group; deployed runtime is unverified. |
| Path parameter | ST-09 reads `courseId` reactively and validates it as a safe positive ID before #20; invalid IDs stay local and do not trigger API reads. |
| API thiết kế | #20 GET /api/v1/users/me/courses confirms ACTIVE enrollment; #37 GET /api/v1/users/me/progress/{course_id} returns source-backed progress; #09 remains public curriculum and is not used for access. API DD/catalog projections still differ from current #20/#37 source. |
| Màn hình liên quan | ST-08 → ST-09 qua lựa chọn khóa học (card không có trong asset ST-08); ST-09 → ST-10 để kiểm tra quyền/start một lesson; inventory cũng liên kết ST-09 → ST-21 để xem tiến độ chi tiết, nhưng không có control trong asset ST-09. |
| Thiết kế hiện có | Source PNG/HTML are static design evidence. Current Angular page validates #20 membership and #37 progress, with loading/error/retry/unresolved/not-enrolled states; it does not expose a lesson tree. |
| Trạng thái | DD BLOCKED: AC-18 aggregate, course tree and lesson-access semantics remain unresolved. Implementation PARTIAL: route and #20/#37 callers are source-wired; #22–#24 are absent from current backend source. Runtime NOT VERIFIED. |

### Nguồn và trạng thái bằng chứng

| Nguồn | Nội dung dùng | Trạng thái |
|---|---|---|
| [Screen inventory](../../list_screen.md) và [global plan](../../screen_stitch/dd_screens/PLAN.md) | Tên, route, actor, AC-13/AC-18, API IDs, states và màn hình nối. | Expected design |
| [ST-09 plan](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/ST-09_PLAN.md) | Scope, source audit, event coverage, marker plan và blockers. | Plan complete |
| [AC API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) và AC-02 Student Learning | Student/session assumption; AC-18 progress expectation gồm lesson, quiz và assignment. | Business design; không định nghĩa aggregation formula |
| [API catalog](../../../../../docs/lists/list_api.md), API #09 DD, API #20/#37 DD và open questions | Declared routes, role, parameter, response label và business-code labels. | API DDs remain Draft; current #09/#20/#37 route and response source is reviewed separately below. |
| [API #09 route](../../../../study-server/app/api/v1.py), module [view](../../../../study-server/app/modules/guest/api_09_courses_curriculum/view.py), [query](../../../../study-server/app/modules/guest/api_09_courses_curriculum/query.py), [models](../../../../study-server/app/modules/guest/api_09_courses_curriculum/models.py) | Public curriculum request, validation, SQL filters/order, response projection. | Current source; test source tồn tại và đã đọc, không chạy |
| Study Server source/tests | #20 membership and #37 course-progress route/module/query/model sources; #22–#24 protected learning flow. | #20/#37 source-backed; #22–#24 not found. Focused tests were not run. |
| Study Web source | ST-09 route/page and #20/#37 callers under the Student route group. | Implementation partial; deployed runtime is unverified. |
| [Source PNG](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/screen.png), [source HTML](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/code.html), [marker map](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/ST-09_markers.json), [annotated PNG](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/screen_annotated.png) | Visual layout, static copy và element locations. | Asset tĩnh; không phải runtime capture |

### Discrepancies cần giữ rõ

1. API state panel trong ảnh ghi #09/#20/#37 đều D. #09/#20/#37 current route/module/query source is present; the original badge and no-caller descriptions are design-time snapshots. API DD/catalog discrepancies and deployed runtime remain open.
2. Inventory cần course outline và per-lesson progress. Current ST-09 shows validated #37 course-level progress but has no lesson list or safe lessonId handoff; source PNG/HTML remain static design assets.
3. Catalog #20/#37 khai báo response ApiEnvelope<UserProfile>; type này không mô tả membership collection hoặc progress fields.
4. Current #09 là public endpoint và trả content, video_url cho lesson PUBLISHED; response không xác minh enrollment hay lesson entitlement.
5. HTML có CTA ST-10 nhưng không truyền lessonId; inventory ST-21 link không có control trong asset.
6. HTML links đều href="#" và data-path chỉ là hint, không điều hướng.
