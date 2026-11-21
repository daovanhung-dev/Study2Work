# ST-04 — Kiểm tra ghi danh trước đăng ký · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-04` |
| Module | Student |
| Route | `/student/enroll/:courseId` — current Study Web route; authenticated guard is unresolved |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái thiết kế:** `DISCREPANCY / CATALOG AUTH OPEN` · **Trạng thái triển khai:** `PARTIAL / PAID HANDOFF PENDING` · **Runtime:** `NOT VERIFIED` |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-04.md](../../screen_stitch/03_student/ST-04_kiem-tra-ghi-danh-truoc-dang-ky/ST-04.md), [ST-04_PLAN.md](../../screen_stitch/03_student/ST-04_kiem-tra-ghi-danh-truoc-dang-ky/ST-04_PLAN.md), [ST-04_markers.json](../../screen_stitch/03_student/ST-04_kiem-tra-ghi-danh-truoc-dang-ky/ST-04_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Xem giá, quyền học hiện có, nhánh khóa miễn phí/trả phí; không tự xác nhận đã ghi danh.
- In-scope: GET #8 trước; Student Bearer #15 xác định enrollment của caller; `ACTIVE` mở ST-08, free action gọi #19 rồi xác nhận #20, paid course chuyển ST-05/#16. Paid flow còn chờ ST-05/#16–#18.
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
| Current Study Web source | `/student/enroll/:courseId`, #08/#15 caller, explicit #19 free enrollment, #20 confirmation | `PARTIAL`; Student session is checked by protected API service, but no route guard or return-after-login flow exists |
| Runtime | Worklog/context Study Web | `NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-04 source screen.png](../../screen_stitch/03_student/ST-04_kiem-tra-ghi-danh-truoc-dang-ky/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-04_kiem-tra-ghi-danh-truoc-dang-ky/screen_annotated.png))
- Luồng hiện hành: GET #08 → Student Bearer #15; ACTIVE mở ST-08; free CTA gọi #19 rồi xác nhận #20; paid handoff sang ST-05/#16. Payment branch tiếp tục ở ST-05/ST-06.
- Priority: P1; Gate/source status: **#08/#15/#19/#20 current source callers present; #15 no longer falls back to another user's row.** **DISCREPANCY:** catalog still says #15 Public/no-Bearer while AC-12 and caller are Student-specific; route guard/return-after-login remain absent; paid flow is pending ST-05/#16–#18.

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
| Actor / quyền | Student đã đăng nhập theo AC-12. API #08 là Public; catalog #15 vẫn ghi Public/no-Bearer nhưng current server/caller dùng Student Bearer — giữ đây là discrepancy contract. |
| Route | `/student/enroll/:courseId` là route hiện có trong Study Web; API authentication xảy ra khi gọi protected Student API. Route guard và return-after-login chưa có. |
| Đầu vào | `courseId` trên route là chuỗi theo ký hiệu inventory. API #08/#15 yêu cầu `course_id:int64`. Chưa có contract chuyển slug/chuỗi khác sang ID. |
| Điều kiện trước | AC-12 yêu cầu Student đăng nhập và course tồn tại. API #08 hiện chỉ trả course `PUBLISHED`. |
| Kết quả sau | `ACTIVE` → Khóa học của tôi; không có enrollment + price `0` → explicit #19 rồi #20; price dương → ST-05/#16. Payment thành công phải được backend xác minh trước enrollment. |
| Màn hình liên quan | Trước: GS-03. Sau: ST-05, ST-07, ST-08; inventory cũng liệt kê ST-04 tự quay lại. Điều hướng tĩnh trong prototype còn có `/`, `/courses`, `/student/courses`, `/student/progress`, `/login`, `/register`. |
| API | #08 public `GET /api/v1/courses/{course_id}`; #15 `GET /api/v1/courses/{course_id}/enrollment-status` now requires Student identity in current source and is called by ST-04. Catalog still says Public/no-Bearer. Free enrollment uses #19, then #20 confirms. |
| Trạng thái nguồn | Study Web route calls #08/#15/#19/#20; protected requests use Student session, but the route has no auth guard. Study Server has source routes for #15–#20. Browser, deployment and live DB are unverified. |

### Expected behavior và current behavior

**Expected behavior — AC-12 và inventory:** Student đã đăng nhập; đọc #08 để xác nhận course `PUBLISHED`; tiếp theo kiểm tra #15; chỉ khi kết quả và rule server được xác nhận mới đi nhánh đã ghi danh, miễn phí hoặc trả phí. Thành công thanh toán phải được server xác minh trước khi tạo enrollment. Không xem client callback hoặc giá hiển thị là bằng chứng entitlement.

**Current behavior — source/assets:** `code.html` remains the inert prototype source; the application page keeps the same card shell and now renders live state. Study Web route `/student/enroll/:courseId` calls public #08, then Student Bearer #15 through `StudentApiService`. #15 returns only the caller's latest row and returns generic 404 when Student identity cannot be resolved; the old course-wide fallback is removed. `ACTIVE` opens `/student/courses`; a missing enrollment branches on the #08 price, with explicit #19 free enrollment and #20 confirmation before opening ST-08. The paid branch links to ST-05. The API catalog still declares #15 Public/no-Bearer, so that discrepancy remains open. Existing focused tests assert the earlier gate-only/no-request behavior and are stale; they were not run. Browser and live DB runtime remain unverified.

**DISCREPANCY:** Prototype đang hiển thị Đăng nhập/Đăng ký và trạng thái không xác nhận, trong khi AC-12 đặt tiền điều kiện Student đã đăng nhập. Prototype dùng màu cobalt và Plus Jakarta Sans; hướng dẫn thiết kế Study Web quy định token ocean và Inter/system. Không có nguồn phê duyệt ngoại lệ cho các khác biệt này.

### Ràng buộc nghiệp vụ và bảo mật

- API #15 source now requires Student identity and queries only that user's latest enrollment. Missing/invalid identity receives generic 404; the prior course-wide lookup was removed. Canonical `list_api.md` still says Public/no-Bearer, so auth semantics remain a documented contract discrepancy. The result contains `user_id`.
- AC-12 requires a logged-in Student; ST-04 uses protected `StudentApiService`, but the route itself has no guard or return-after-login behavior. The page shows a login link when protected API calls fail for auth.
- Current #19 source requires a PAID Order when `course.price > 0`; ST-04 treats a zero price as free, calls #19 only after a user action, then confirms via #20. This threshold is derived from current server source; no payment success is inferred from displayed price or browser callback.
- API #19 phải kiểm tra danh tính/entitlement phía máy chủ và cần chống ghi danh trùng; các quyết định này chưa có source hiện hành.
- Hai DDL ứng viên khác nhau: legacy dùng BIGINT `courses`/`enrollments`; V1-PILOT dùng UUID/versioned course enrollment. Không có bằng chứng live schema/deployment.
