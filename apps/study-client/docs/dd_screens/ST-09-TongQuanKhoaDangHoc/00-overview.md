# ST-09 — Tổng quan khóa đang học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-09` |
| Module | Student |
| Route | `/student/courses/:courseId` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** BLOCKED · **Implementation:** BLOCKED · **Runtime:** NOT VERIFIED |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
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
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-09 source screen.png](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/screen_annotated.png))
- Luồng: Xác nhận course thuộc #20 → GET #37; GET #9 chỉ chứa phần public; lesson access #22 trước khi học.
- Priority: P1; Gate/source status: **D**; #09 local source-backed/public (API DD Draft, int64 range check absent); #20/#37 and #22–#24 not source-backed; **BLOCK:** Chưa có contract course-learning tree đầy đủ

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-09 — Tổng quan khóa đang học

> **DD status:** BLOCKED · **Implementation:** BLOCKED · **Runtime:** NOT VERIFIED
> **Phạm vi phiên:** ST-09. Tài liệu tách hành vi mong đợi khỏi bằng chứng hiện tại; asset tĩnh không xác nhận runtime.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-09 — Tổng quan khóa đang học (Page) |
| Mục tiêu mong đợi | Cho Student đã ghi danh xem đề cương khóa, tiến độ học và đi tới bài học hoặc chi tiết tiến độ theo AC-13/AC-18 và inventory. |
| Actor | Student đã đăng nhập theo AC-13, API #20 và #37. Guest hoặc Student chưa ghi danh không được xem nội dung học được bảo vệ; chính sách hiển thị chính xác đang chờ contract. |
| Route | /student/courses/:courseId là route trong inventory. Study Web không có source app/router để xác minh route; compiled dist bị ignore chỉ có route /. |
| Path parameter | courseId được inventory/API liên quan kỳ vọng là int64, nhưng frontend parse, invalid-ID state và binding từ ST-08 chưa có implementation. |
| API thiết kế | #20 GET /api/v1/users/me/courses để xác nhận enrollment; #37 GET /api/v1/users/me/progress/{course_id}; #09 GET /api/v1/courses/{course_id}/curriculum để lấy curriculum public. API #20/#37 chỉ có catalog/DD Draft; #09 có backend route/module/query/test source. |
| Màn hình liên quan | ST-08 → ST-09 qua lựa chọn khóa học (card không có trong asset ST-08); ST-09 → ST-10 để kiểm tra quyền/start một lesson; inventory cũng liên kết ST-09 → ST-21 để xem tiến độ chi tiết, nhưng không có control trong asset ST-09. |
| Thiết kế hiện có | PNG hoàn chỉnh cho gated/unavailable handoff. HTML là mockup tĩnh, không có API fetch, route binding hay auth/profile state. |
| Trạng thái | DD BLOCKED: enrollment/progress payload và lesson-access semantics thiếu hoặc không khớp. Implementation BLOCKED: Study Web source/route absent, #20/#37 và #22–#24 không có current backend source. Runtime NOT VERIFIED. |

### Nguồn và trạng thái bằng chứng

| Nguồn | Nội dung dùng | Trạng thái |
|---|---|---|
| [Screen inventory](../../list_screen.md) và [global plan](../../screen_stitch/dd_screens/PLAN.md) | Tên, route, actor, AC-13/AC-18, API IDs, states và màn hình nối. | Expected design |
| [ST-09 plan](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/ST-09_PLAN.md) | Scope, source audit, event coverage, marker plan và blockers. | Plan complete |
| [AC API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) và AC-02 Student Learning | Student/session assumption; AC-18 progress expectation gồm lesson, quiz và assignment. | Business design; không định nghĩa aggregation formula |
| [API catalog](../../../../../docs/lists/list_api.md), API #09 DD, API #20/#37 DD và open questions | Declared routes, role, parameter, response label và business-code labels. | #09 current source-backed; #20/#37 Draft, chưa runnable |
| [API #09 route](../../../../study-server/app/api/v1.py), module [view](../../../../study-server/app/modules/guest/api_09_courses_curriculum/view.py), [query](../../../../study-server/app/modules/guest/api_09_courses_curriculum/query.py), [models](../../../../study-server/app/modules/guest/api_09_courses_curriculum/models.py) | Public curriculum request, validation, SQL filters/order, response projection. | Current source; test source tồn tại và đã đọc, không chạy |
| Study Server source/tests | Exact route/module/test search cho #20, #37 và #22–#24. | NOT_FOUND trong checkout |
| Study Web source/artifact | Editable app source/package manifest không có. Ignored dist artifact chỉ có route /; không có Student course/progress routes hoặc calls. Provenance/serving unknown. | Feature routing UNWIRED; dist không chứng minh deployment |
| [Source PNG](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/screen.png), [source HTML](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/code.html), [marker map](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/ST-09_markers.json), [annotated PNG](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/screen_annotated.png) | Visual layout, static copy và element locations. | Asset tĩnh; không phải runtime capture |

### Discrepancies cần giữ rõ

1. API state panel trong ảnh ghi #09/#20/#37 đều D. #09 hiện có route/module/query/test source và đã được đánh `R` trong API dependency index; API #09 DD vẫn Draft, còn badge ảnh là stale. #20/#37 vẫn chỉ là declared design. ST-09 screen status vẫn `D` vì client flow chưa được nối.
2. Inventory cần course outline và per-lesson progress. PNG/HTML chỉ có gated state, không có lesson list, progress bar, loading/error/empty states.
3. Catalog #20/#37 khai báo response ApiEnvelope<UserProfile>; type này không mô tả membership collection hoặc progress fields.
4. Current #09 là public endpoint và trả content, video_url cho lesson PUBLISHED; response không xác minh enrollment hay lesson entitlement.
5. HTML có CTA ST-10 nhưng không truyền lessonId; inventory ST-21 link không có control trong asset.
6. HTML links đều href="#" và data-path chỉ là hint, không điều hướng.
