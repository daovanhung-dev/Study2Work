# ST-08 — Khóa học của tôi · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-08` |
| Module | Student |
| Route | `/student/courses` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `BLOCKED` · **Implementation:** `BLOCKED` · **Runtime:** `NOT VERIFIED` |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-08.md](../../screen_stitch/03_student/ST-08_khoa-hoc-cua-toi/ST-08.md), [ST-08_PLAN.md](../../screen_stitch/03_student/ST-08_khoa-hoc-cua-toi/ST-08_PLAN.md), [ST-08_markers.json](../../screen_stitch/03_student/ST-08_khoa-hoc-cua-toi/ST-08_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Danh sách khóa đã ghi danh, filter trạng thái và thanh tiến độ.
- In-scope: GET #20 page/status → GET #21 nếu cần dữ liệu progress không kèm sẵn; merge theo course_id.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-13 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Danh sách khóa đã ghi danh, filter trạng thái và thanh tiến độ. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #20, #21
- Liên kết màn hình dự kiến: [ST-09](../ST-09-TongQuanKhoaDangHoc/00-overview.md), [ST-20](../ST-20-TongQuanTienDo/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/empty/partial-progress/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-08 source screen.png](../../screen_stitch/03_student/ST-08_khoa-hoc-cua-toi/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-08_khoa-hoc-cua-toi/screen_annotated.png))
- Luồng: GET #20 page/status → GET #21 nếu cần dữ liệu progress không kèm sẵn; merge theo course_id.
- Priority: P1; Gate/source status: **D**; **BLOCK:** #20/#21 Draft/NOT_FOUND, response UserProfile không biểu diễn list/progress; query/merge chưa chốt; AC-13 nhánh EMPTY/HAS DATA cùng tới node render; DDL BIGINT/UUID khác model; loaded/filter UI và design guide alignment còn thiếu; Study Web UNWIRED

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-08 — Khóa học của tôi

> **DD status:** `BLOCKED` · **Implementation:** `BLOCKED` · **Runtime:** `NOT VERIFIED`
> **Phạm vi phiên:** chỉ ST-08. Tài liệu mô tả thiết kế và bằng chứng hiện có; đây không phải xác nhận UI hoặc API đang chạy.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-08 — Khóa học của tôi (Page) |
| Mục tiêu | Cho Student xem các khóa đã ghi danh, lọc theo trạng thái và xem tiến độ từng khóa theo inventory/AC-13. |
| Actor | Student đã đăng nhập theo tiền điều kiện AC-13 và API catalog. |
| Route | `/student/courses` là route đề xuất trong inventory; Study Web hiện không có app source, router hoặc entrypoint để xác minh route khi chạy. |
| API thiết kế | #20 `GET /api/v1/users/me/courses`; #21 `GET /api/v1/users/me/progress`. Hai API mới được khai báo trong catalog/DD Draft; không tìm thấy route, module, query hoặc test tương ứng trong Study Server hiện tại. |
| Thiết kế UI có sẵn | `code.html` là HTML tĩnh với trạng thái empty; `screen.png` không hiển thị header và có dải đen dưới footer. `screen_rendered.png` là ảnh render tĩnh từ HTML dùng làm nền chú thích; không phải runtime capture. |
| Điều hướng liên quan | ST-07 → ST-08 sau kết quả ghi danh được xác minh; ST-08 → ST-09 theo course card (card hiện chưa có); ST-08 → ST-20 qua CTA/header/footer. Header/footer cũng có liên kết về ST-01. |
| Trạng thái tổng | DD bị chặn bởi response #20/#21 không thể hiện course/progress payload, semantics query/merge chưa chốt và loaded/filter state chưa được thiết kế. Implementation bị chặn thêm bởi Study Web chưa có trong checkout. |

### Nguồn và mức độ bằng chứng

| Nguồn | Điều dùng làm bằng chứng | Trạng thái |
|---|---|---|
| [Screen inventory](../../list_screen.md) và [global screen plan](../../screen_stitch/dd_screens/PLAN.md) | Tên/route dự kiến, actor, AC-13, API IDs, quan hệ ST-09/ST-20, các state mong đợi. | Expected design; không phải runtime. |
| [AC API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) và [AC-02 Student Learning diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) | Student đã đăng nhập; hậu điều kiện hiển thị danh sách khóa kèm progress; AC-13 liệt kê #20 và #21. | Business design; một số chi tiết orchestration không khớp inventory. |
| [API catalog](../../../../../docs/lists/list_api.md), [API #20 DD](../../../../study-server/docs/dd/20_users_me_courses/00_Cover.md), [#20 open questions](../../../../study-server/docs/dd/20_users_me_courses/OPEN_QUESTIONS.md), [API #21 DD](../../../../study-server/docs/dd/21_users_me_progress/00_Cover.md), [#21 open questions](../../../../study-server/docs/dd/21_users_me_progress/OPEN_QUESTIONS.md) | Endpoint, role, tham số và business codes đang được khai báo; các DD API đều Draft — Needs Confirmation. | Declared design only; không chứng minh route hoạt động. |
| Study Server source/tests | Tìm chuỗi endpoint và tên module #20/#21 trong `apps/study-server/app` và `apps/study-server/tests`. | `NOT_FOUND` cho cả hai endpoint trong checkout đã rà soát. Không có test runnable xác minh các hợp đồng này. |
| [Study UI design guide](../../../../../.agents/web-study/design.md) | Hướng dẫn giao diện đích cho Study. | Design guidance; không phải bằng chứng UI đã wired. |
| [Nguồn HTML tĩnh](../../screen_stitch/03_student/ST-08_khoa-hoc-cua-toi/code.html), [PNG gốc](../../screen_stitch/03_student/ST-08_khoa-hoc-cua-toi/screen.png), [ảnh render sạch](../../screen_stitch/03_student/ST-08_khoa-hoc-cua-toi/screen_rendered.png), [ảnh chú thích](../../screen_stitch/03_student/ST-08_khoa-hoc-cua-toi/screen_annotated.png) | Bố cục và nội dung nhìn thấy trong asset ST-08. | HTML/ảnh mẫu; không có fetch, session, state store hoặc router runtime. |
| [DDL legacy](../../../../../infra/postgres/study-server/DB.sql) và [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) | Hai artifact mô tả các mô hình enrollment/course/progress khác nhau. | Design artifacts only; không API #20/#21 query nào chọn mô hình, và không xác nhận live schema. |

### Sai khác cần giữ nguyên

1. Inventory mô tả filter status, course list và progress bar; HTML/PNG chỉ có empty state. Không có element để chú thích cho loaded state.
2. Inventory nói gọi #21 khi #20 chưa kèm progress; AC-13 mô tả gọi cả #20 và #21. Response #20 hiện chỉ khai báo `ApiEnvelope<UserProfile>`, vì vậy chưa thể biết #20 có progress để điều kiện hóa request #21.
3. AC-13 cần ghép courses và progress theo `course_id`; catalog khai báo cả #20 lẫn #21 trả `ApiEnvelope<UserProfile>`, còn node API trong diagram chỉ ghi `ApiEnvelope`. Các response declaration không mô tả collection khóa học hoặc tiến độ.
4. AC-13 decision node ghi `NO → empty state; YES → render`, nhưng cả cạnh `EMPTY` lẫn `HAS DATA` đều trỏ tới cùng node “Hiển thị khóa học + % hoàn thành”. Destination của nhánh empty chưa rõ.
5. Legacy DDL dùng `BIGSERIAL`/BIGINT với `enrollments` và `lesson_progress`; V1-PILOT DDL dùng UUID course/enrollment model với `course_enrollments`, `lesson_progress_facts` và `progress_snapshots`. Không có API #20/#21 query source để chọn model; không suy luận ID type, join hay progress source.
6. HTML imports Google Fonts và Tailwind CDN, dùng Plus Jakarta Sans và `max-w-[1440px]`; Study Web guide chỉ định Inter/system, không thêm remote imports và content width khoảng 1120px. Chưa có approved exception.
7. Các anchor HTML có `href`, nhưng Study Web router/source không có trong checkout; điều hướng chỉ là ý đồ trong asset.
