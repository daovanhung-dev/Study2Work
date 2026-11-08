# ST-07 — Kết quả đăng ký khóa học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-07` |
| Module | Student |
| Route | `/student/enroll/result/:courseId` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái thiết kế:** `DD BLOCKED` · **Trạng thái triển khai:** `IMPLEMENTATION BLOCKED` · **Runtime:** `NOT VERIFIED` |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-07.md](../../screen_stitch/03_student/ST-07_ket-qua-dang-ky-khoa-hoc/ST-07.md), [ST-07_PLAN.md](../../screen_stitch/03_student/ST-07_ket-qua-dang-ky-khoa-hoc/ST-07_PLAN.md), [ST-07_markers.json](../../screen_stitch/03_student/ST-07_ket-qua-dang-ky-khoa-hoc/ST-07_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Hiển thị kết quả chỉ sau backend xác nhận entitlement/enrollment; không suy ra success từ callback hay static copy.
- In-scope: AC-12 #19 Enrollment+Progress transaction → #20 reload; exact #19 trigger/screen owner chưa chốt. #18 chỉ khi có trusted operation_id và contract thống nhất.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-12 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Hiển thị kết quả chỉ sau backend xác nhận entitlement/enrollment; không suy ra success từ callback hay static copy. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #18, #19, #20
- Liên kết màn hình dự kiến: [ST-08](../ST-08-KhoaHocCuaToi/00-overview.md), [ST-09](../ST-09-TongQuanKhoaDangHoc/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | awaiting-confirmation/enrolled/conflict/failure |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-07 source screen.png](../../screen_stitch/03_student/ST-07_ket-qua-dang-ky-khoa-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-07_ket-qua-dang-ky-khoa-hoc/screen_annotated.png))
- Luồng: AC-12 #19 Enrollment+Progress transaction → #20 reload; exact #19 trigger/screen owner chưa chốt. #18 chỉ khi có trusted operation_id và contract thống nhất.
- Priority: P2; Gate/source status: **#18/#19/#20 D; DD BLOCKED**; **BLOCK:** AC-12 không nêu ST-07 riêng/#18 detached; Operation ID/access/lifecycle và ST-06 handoff chưa rõ; #19 identity/eligibility/duplicate/transaction chưa chốt; #20 UserProfile không biểu diễn Course list; Study Web/API UNWIRED; post-#19 reload recovery và destination chưa rõ

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-07 — Kết quả đăng ký khóa học

> **Trạng thái thiết kế:** `DD BLOCKED` · **Trạng thái triển khai:** `IMPLEMENTATION BLOCKED` · **Runtime:** `NOT VERIFIED`
>
> Phạm vi và thứ tự authoring được ghi tại [ST-07_PLAN.md](../../screen_stitch/03_student/ST-07_ket-qua-dang-ky-khoa-hoc/ST-07_PLAN.md). `screen_annotated.png` được tạo từ [screen_rendered_from_html.png](../../screen_stitch/03_student/ST-07_ket-qua-dang-ky-khoa-hoc/screen_rendered_from_html.png); ảnh gốc [screen.png](../../screen_stitch/03_student/ST-07_ket-qua-dang-ky-khoa-hoc/screen.png) được giữ nguyên vì gần như trống.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-07 — Kết quả đăng ký khóa học |
| Mục tiêu dự kiến | Hiển thị kết quả enrollment sau khi backend xác nhận điều kiện ghi danh; AC-12 sequence tạo Enrollment + Progress rồi reload My Courses trước khi báo đã đăng ký. |
| Actor / quyền | Student đã đăng nhập theo AC-12 và catalog APIs #18/#19/#20. AC-12 yêu cầu Student; quyền #18 và cách xác định caller/owner chưa thống nhất. |
| Route | `/student/enroll/result/:courseId` theo inventory; chưa được wire trong Study Web. Path `courseId` không cung cấp `operationId`. |
| Đầu vào | Candidate `courseId:int64` từ route; Student session; paid branch cần trusted payment outcome/Operation ID từ ST-06; free branch cần entitlement proof. Hiện không có handoff data contract cho các state này. |
| Điều kiện trước | AC-12: Student đăng nhập, course tồn tại. Ghi danh chỉ sau nhánh free eligible hoặc trusted payment success. API #19 còn yêu cầu Student Bearer. Trigger/vị trí gọi #19 giữa ST-04/ST-07 chưa được chốt; không được suy ra từ route load. |
| Kết quả sau | Expected: Enrollment + Progress được tạo theo transaction #19; #20 reload rồi hiển thị registered/open course theo AC-12. Destination ngoài nút “Khóa học của tôi” chưa được xác định. Current HTML chỉ báo “Chưa thể xác nhận kết quả đăng ký.”, không có response binding. |
| Màn hình liên quan | Trước: ST-04 free/paid decision; ST-05→ST-06 cho paid branch; ST-06 chỉ được bàn giao sang ST-07 khi có trusted success. Sau: ST-08 “Khóa học của tôi”; ST-09 course detail là candidate từ inventory. HTML chỉ liên kết ST-08, không truyền course ID. |
| API liên quan | #18 `GET /api/v1/operations/{operation_id}` conditional và detached trong AC-12; #19 `POST /api/v1/courses/{course_id}/enrollments`; #20 `GET /api/v1/users/me/courses`. Cả ba hiện `DESIGN_ONLY / UNWIRED`. |
| Hiện trạng | `code.html` là static public shell/result card với 14 literal anchors; không có route/auth/API/event handler/Enrollment data. `screen.png` 1280×1024 gần như trống; render HTML được giữ riêng. |

### Expected behavior và current behavior

**Expected behavior — inventory/AC-12/AC-13:** Free branch có thể bỏ Order/Payment; paid branch chỉ đi tiếp sau Payment Gateway success. AC-12 sau đó gọi #19 để tạo Enrollment và initialize Progress trong một transaction, gọi #20 reload My Courses, rồi hiển thị “Đã đăng ký”/mở khóa học. Inventory thêm result screen ST-07, các state `awaiting-confirmation/enrolled/conflict/failure` và API #18/#19/#20.

**Current behavior — source/assets:** `code.html` hiển thị header, breadcrumb, H1, icon, static H2 “Chưa thể xác nhận kết quả đăng ký.”, supporting copy nói hệ thống chưa ghi nhận trạng thái kích hoạt ghi danh, CTA “Về khóa học của tôi”, footer. Không có course ID/name, Enrollment ID/status, Operation ID, payment result hoặc dynamic error. CTA đi tới literal `/student/courses`. Original PNG không thể dùng để xác định layout; HTML render được lưu riêng.

**DISCREPANCY:** AC-12 không có node/route riêng cho ST-07; flow kết thúc ở #20 và result “Đã đăng ký”/open course. API #18 là node rời. Inventory mô hình hóa thêm màn hình và states. Không tự quyết định màn hình nào sở hữu POST #19, thời điểm gọi, hay cách truyền Operation result.

### Quy tắc nghiệp vụ và bảo mật

- API #19 yêu cầu Bearer JWT, role Student. Catalog body ghi cả `course_id:int64!` và `user từ JWT:string!`, nhưng không có JSON key/claim wire được chốt. Không gửi thêm `user_id` hoặc giả định tên field.
- API #19 chỉ được gọi khi backend chứng minh course/enrollment eligibility; paid course cần trusted payment success. Client callback, URL, static card, icon check hoặc #20 UserProfile response không phải bằng chứng paid/enrolled.
- AC-12 yêu cầu transaction cho Enrollment + Progress và chống ghi danh trùng. API #19 DD chưa xác định duplicate predicate, concurrency/idempotency, initial EnrollmentStatus, lesson set hoặc giá trị Progress.
- API #18 không được gọi nếu chưa có Operation ID được bàn giao và thống nhất kiểu: catalog row `int64`, AC diagram/shared Operation schema `uuid`. Owner-only vs owner/Admin, lifecycle/status/result/poll rules chưa chốt.
- API #20 yêu cầu Student Bearer, nhưng response `UserProfile` không biểu diễn danh sách Enrollment/Course như AC-13. Không dùng nó để quyết định course membership cho đến khi contract được sửa/duyệt.
- DDL `enrollments`/`lesson_progress` là checked-in design artifact; DB table docs ghi FK bắt buộc nhưng SQL để FK columns nullable và enrollment pair chưa có unique constraint. Live schema/deployment chưa được xác minh.
- Study Web route/auth/client và APIs #18/#19/#20 chưa wire. Prototype dùng remote Plus Jakarta Sans/Material Symbols và Tailwind CDN; guide Study Web ưu tiên Inter/system stack và không thêm remote imports; link focus treatment cũng chưa được xác minh theo guide.
