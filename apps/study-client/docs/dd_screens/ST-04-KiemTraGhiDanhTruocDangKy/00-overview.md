# ST-04 — Kiểm tra ghi danh trước đăng ký · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-04` |
| Module | Student |
| Route | `/student/enroll/:courseId` — current Study Web route; authenticated guard is unresolved |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái thiết kế:** `DD BLOCKED` · **Trạng thái triển khai:** `PARTIAL / ENROLLMENT GATED` · **Runtime:** `NOT VERIFIED` |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-04.md](../../screen_stitch/03_student/ST-04_kiem-tra-ghi-danh-truoc-dang-ky/ST-04.md), [ST-04_PLAN.md](../../screen_stitch/03_student/ST-04_kiem-tra-ghi-danh-truoc-dang-ky/ST-04_PLAN.md), [ST-04_markers.json](../../screen_stitch/03_student/ST-04_kiem-tra-ghi-danh-truoc-dang-ky/ST-04_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Xem giá, quyền học hiện có, nhánh khóa miễn phí/trả phí; không tự xác nhận đã ghi danh.
- In-scope: GET #8 trước; #15 chỉ gọi khi BE chốt identity/selection; nếu miễn phí → #19, nếu trả phí → #16. Current Study Web reads #08 and keeps the enrollment decision gated.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-12 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Xem giá, quyền học hiện có, nhánh khóa miễn phí/trả phí; không tự xác nhận đã ghi danh. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #08, #15
- Liên kết màn hình dự kiến: [ST-05](../ST-05-KiemTraDonHangCheckout/00-overview.md), [ST-07](../ST-07-KetQuaDangKyKhoaHoc/00-overview.md), [ST-08](../ST-08-KhoaHocCuaToi/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/not-eligible/already-enrolled/free/paid |
| Current Study Web source | `/student/enroll/:courseId`, #08 caller, then enrollment gate | `PARTIAL`; no Student guard/session and no safe #15 caller |
| Runtime | Worklog/context Study Web | `NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-04 source screen.png](../../screen_stitch/03_student/ST-04_kiem-tra-ghi-danh-truoc-dang-ky/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-04_kiem-tra-ghi-danh-truoc-dang-ky/screen_annotated.png))
- Luồng: GET #8 trước; #15 chỉ gọi khi BE chốt identity/selection; nếu miễn phí → #19, nếu trả phí → #16.
- Priority: P1; Gate/source status: **#08 R + Study Web caller; #15 R in Study Server but unsafe for anonymous/invalid-token requests; DD BLOCKED**; **BLOCK:** #15 identity/selection, auth/free-paid/entitlement flow chưa chốt; Study Web has no Student session/guard

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-04 — Kiểm tra ghi danh trước đăng ký

> **Trạng thái thiết kế:** `DD BLOCKED` · **Trạng thái triển khai:** `PARTIAL / ENROLLMENT GATED` · **Runtime:** `NOT VERIFIED`

> Screen ID này được mô tả theo một phiên độc lập. Phạm vi, nguồn, thứ tự và blocker được ghi trong [ST-04_PLAN.md](../../screen_stitch/03_student/ST-04_kiem-tra-ghi-danh-truoc-dang-ky/ST-04_PLAN.md).

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ST-04 — Kiểm tra ghi danh trước đăng ký |
| Mục tiêu | Trước khi ghi danh, đọc khóa học đã xuất bản và kiểm tra quan hệ ghi danh của Student; sau đó điều hướng theo nhánh đã được AC-12 xác nhận. Quy tắc chọn enrollment cho Student hiện chưa được xác định nên chưa thể hoàn thiện luồng này. |
| Actor / quyền | Student đã đăng nhập theo tiền điều kiện AC-12. API #08 và hợp đồng #15 hiện khai báo Public; mâu thuẫn định danh của #15 được giữ là blocker. |
| Route | `/student/enroll/:courseId` là route **đề xuất trong inventory**; không có router Study Web hiện hành để xác minh hoặc chạy route này. |
| Đầu vào | `courseId` trên route là chuỗi theo ký hiệu inventory. API #08/#15 yêu cầu `course_id:int64`. Chưa có contract chuyển slug/chuỗi khác sang ID. |
| Điều kiện trước | AC-12 yêu cầu Student đăng nhập và course tồn tại. API #08 hiện chỉ trả course `PUBLISHED`. |
| Kết quả sau | Theo AC-12: đã ghi danh → Khóa học của tôi; chưa ghi danh và đủ điều kiện miễn phí → #19; nhánh trả phí → ST-05/#16, ST-06/#17 và xác nhận phía máy chủ trước #19/#20. Điều kiện giá, entitlement và cách chọn enrollment chưa chốt. |
| Màn hình liên quan | Trước: GS-03. Sau: ST-05, ST-07, ST-08; inventory cũng liệt kê ST-04 tự quay lại. Điều hướng tĩnh trong prototype còn có `/`, `/courses`, `/student/courses`, `/student/progress`, `/login`, `/register`. |
| API | #08 `GET /api/v1/courses/{course_id}` — source-backed and called by ST-04. #15 `GET /api/v1/courses/{course_id}/enrollment-status` has current route/module/query/model/test, but optional-token fallback can return an unrelated enrollment; client descriptor remains `UNWIRED`. |
| Trạng thái nguồn | Study Web has a route/page and #08 caller; Student auth/guard is absent. Study Server has routes for #15–#20, but contracts and security remain gated. Browser, deployment and live DB are unverified. |

### Expected behavior và current behavior

**Expected behavior — AC-12 và inventory:** Student đã đăng nhập; đọc #08 để xác nhận course `PUBLISHED`; tiếp theo kiểm tra #15; chỉ khi kết quả và rule server được xác nhận mới đi nhánh đã ghi danh, miễn phí hoặc trả phí. Thành công thanh toán phải được server xác minh trước khi tạo enrollment. Không xem client callback hoặc giá hiển thị là bằng chứng entitlement.

**Current behavior — source/assets:** `code.html` chỉ render public header, breadcrumb, card chứa copy lỗi tĩnh, anchor quay lại `/courses` và footer. Hai asset nguồn `screen.png` và `code.html` được giữ nguyên. Study Web hiện có route `/student/enroll/:courseId`; page gọi GET #08 qua `GS03CourseDetailService`, map course `PUBLISHED` sang enrollment gate, map 404 sang not-found và các lỗi khác sang error. Không có Student guard/session và page không gọi #15, #16, #17, #18, #19 hoặc #20. API #15 hiện có route/module/query/model/test trong Study Server, nhưng handler cho phép thiếu token hoặc token không hợp lệ rơi về enrollment bất kỳ của course; vì vậy page không dùng response đó để xác nhận enrollment. Focused FE tests cover #08 gate/not-found; authenticated/browser/live DB runtime chưa xác minh.

**DISCREPANCY:** Prototype đang hiển thị Đăng nhập/Đăng ký và trạng thái không xác nhận, trong khi AC-12 đặt tiền điều kiện Student đã đăng nhập. Prototype dùng màu cobalt và Plus Jakarta Sans; hướng dẫn thiết kế Study Web quy định token ocean và Inter/system. Không có nguồn phê duyệt ngoại lệ cho các khác biệt này.

### Ràng buộc nghiệp vụ và bảo mật

- API #15 contract khai báo Public và chỉ nhận `course_id`; current handler accepts optional Bearer and resolves a valid Student token, but with absent or invalid Authorization it queries any enrollment for the course, ordered by descending enrollment ID and limited to one. The response contains `user_id`; this behavior conflicts with the Student identity requirement and is unsafe for the screen to call. Do not call #15 or branch from its result until backend fixes the auth/selection contract.
- AC-12 yêu cầu Student đã đăng nhập, nhưng hiện chưa có Study Web guard hoặc contract thống nhất danh tính giữa UI và API #15.
- `price` dạng chuỗi decimal từ #08 không tự xác định currency, ngưỡng miễn phí, eligibility hay payment state. Không suy luận miễn phí từ một giá trị mẫu hoặc từ format.
- API #19 phải kiểm tra danh tính/entitlement phía máy chủ và cần chống ghi danh trùng; các quyết định này chưa có source hiện hành.
- Hai DDL ứng viên khác nhau: legacy dùng BIGINT `courses`/`enrollments`; V1-PILOT dùng UUID/versioned course enrollment. Không có bằng chứng live schema/deployment.
