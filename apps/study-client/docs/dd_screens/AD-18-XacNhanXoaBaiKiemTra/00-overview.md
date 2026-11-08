# AD-18 — Xác nhận xóa bài kiểm tra · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-18` |
| Module | Admin |
| Route | `/admin/quizzes/:quizId/delete` (candidate; Study Web chưa wired)` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái:** `DD BLOCKED` · `IMPLEMENTATION BLOCKED` · `RUNTIME NOT VERIFIED` · **Study Web:** `UNWIRED` · **API #90:** route/module/query/model/validator/test source có trong Study Server; API DD vẫn `Draft — Needs Confirmation`; live schema/deployment chưa xác minh. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-18.md](../../screen_stitch/05_admin/AD-18_xac-nhan-xoa-bai-kiem-tra/AD-18.md), [AD-18_PLAN.md](../../screen_stitch/05_admin/AD-18_xac-nhan-xoa-bai-kiem-tra/AD-18_PLAN.md), [AD-18_markers.json](../../screen_stitch/05_admin/AD-18_xac-nhan-xoa-bai-kiem-tra/AD-18_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Admin xem Quiz/tác động history rồi xác nhận; AD-15 là entry và đường quay lại dự kiến.
- In-scope: Candidate DELETE #90 path-only; on success invalidate/refetch #87 theo inventory. `conflict` không được #90 catalog khai báo (không có 409); 422 local là invalid `quiz_id`, không phải conflict.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-35 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Admin xem Quiz/tác động history rồi xác nhận; AD-15 là entry và đường quay lại dự kiến. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #90
- Liên kết màn hình dự kiến: [AD-15](../AD-15-DanhSachBaiKiemTra/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | confirm/deleting/deleted/unauthorized/forbidden/not-found/validation-error/service-error/unknown-outcome/unwired; `conflict` unsupported |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-18 source screen.png](../../screen_stitch/05_admin/AD-18_xac-nhan-xoa-bai-kiem-tra/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-18_xac-nhan-xoa-bai-kiem-tra/screen_annotated.png))
- Luồng: Candidate DELETE #90 path-only; on success invalidate/refetch #87 theo inventory. `conflict` không được #90 catalog khai báo (không có 409); 422 local là invalid `quiz_id`, không phải conflict.
- Priority: P2; Gate/source status: **R** local #90 route/module/query/model/validator/test source; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** AC-35 chỉ yêu cầu soft-delete khi có attempts, no-attempt branch không xác định; local hard-delete/no-history và soft-delete on linked answer are DERIVED; tombstone/timestamp/repeat, #29 race, permission, #87/#89/#91 visibility, target data/detail API, live schema and Study Web UNWIRED remain open; **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-18 — Xác nhận xóa bài kiểm tra

> **Screen:** AD-18 · **Actor theo AC-35:** Admin có quiz-management permission · **Route candidate:** `/admin/quizzes/:quizId/delete` · **API candidate:** #90 `DELETE /api/v1/admin/quizzes/{quiz_id}` · **Entry/handoff:** [AD-15](../../screen_stitch/05_admin/AD-15_danh-sach-bai-kiem-tra/AD-15.md).
> **Trạng thái:** `DD BLOCKED` · `IMPLEMENTATION BLOCKED` · `RUNTIME NOT VERIFIED` · **Study Web:** `UNWIRED` · **API #90:** route/module/query/model/validator/test source có trong Study Server; API DD vẫn `Draft — Needs Confirmation`; live schema/deployment chưa xác minh.
> **Tài sản:** [ảnh nguyên trạng](../../screen_stitch/05_admin/AD-18_xac-nhan-xoa-bai-kiem-tra/screen.png) · [ảnh đánh số](../../screen_stitch/05_admin/AD-18_xac-nhan-xoa-bai-kiem-tra/screen_annotated.png) · [bản đồ marker](../../screen_stitch/05_admin/AD-18_xac-nhan-xoa-bai-kiem-tra/AD-18_markers.json) · [SVG marker](../../screen_stitch/05_admin/AD-18_xac-nhan-xoa-bai-kiem-tra/AD-18_markers.svg) · [kế hoạch](../../screen_stitch/05_admin/AD-18_xac-nhan-xoa-bai-kiem-tra/AD-18_PLAN.md) · [inventory](../../list_screen.md).

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

AD-18 là màn hình xác nhận thao tác xóa quiz được AC-35 nối từ danh sách AD-15. Màn hình cần cho Admin nhận diện đúng Quiz, hiểu tác động tới attempts/history và đưa ra xác nhận tường minh. Đây là mục tiêu thiết kế; giao diện web hiện chưa được triển khai. Mockup có record placeholder, cảnh báo chính sách, trường lý do audit bị khóa và nút xóa bị disabled.

| Thuộc tính | Expected behavior / nguồn | Current behavior / bằng chứng |
|---|---|---|
| Actor | AC-35 yêu cầu Admin có quyền quản lý quiz. | API #90 dùng shared `ADMIN` role guard; chưa có source cho fine-grained quiz-management permission. |
| Điều kiện trước | Quiz được chọn từ AD-15 hoặc nhận `quizId` hợp lệ; người dùng đã xác thực và được phân quyền. | Inventory chỉ định URL candidate. Study Web checkout không có editable app source/router/API client; route chưa wire. Mockup hiện không chọn bản ghi. |
| Route | `/admin/quizzes/:quizId/delete`. | Không tìm thấy frontend route/runtime. HTML link dùng `href="#"`. |
| Dữ liệu target | Tên, ID và course giúp xác nhận đúng Quiz; attempts/history impact theo chính sách được duyệt. | Không có GET admin detail. #87 local list trả `id`, `course_id`, `title`, `duration_minutes`, `passing_score`, `questions=[]`; không trả course title hoặc counts/history. Không thể dựng nội dung hiện trên mockup từ contract #87 hiện tại. |
| Điều kiện sau | Inventory kỳ vọng #90 delete và invalidate #87; trạng thái `deleted` được liệt kê. | Cơ chế cache/navigation chưa có client. Exact success destination chưa được inventory/AC chốt. |
| Điều hướng | AD-15 → AD-18; quay lại AD-15. | Hai anchor của mockup đều `href="#"`; route history, giữ filter/page và handoff chưa có runtime evidence. |
| Bảo mật | Chỉ Admin có quyền nghiệp vụ; không gửi dữ liệu không có trong contract. | Local API kiểm tra role `ADMIN`, không body/query; authentication/authorization chạy trước parse path/DB. Role chưa chứng minh permission riêng. |
| Trạng thái triển khai | DD đủ traceable nhưng blocker phải được quyết định trước implementation. | API route/module/test source hiện có; Study Web `UNWIRED`; API DD Draft; live DB/deployment và runtime không xác minh. |

### API #90 — direct contract và local source

| Thành phần | API catalog / AC-35 | Study Server hiện tại | Tác động lên UI |
|---|---|---|---|
| Method/path | `DELETE /api/v1/admin/quizzes/{quiz_id}`; path `quiz_id:int64!`; không body/query. | Route đã đăng ký cùng path template; chỉ truyền Authorization và raw path. | Không truyền audit reason hoặc UI-only fields. `quizId` route param phải được map sang numeric `quiz_id`; slug/UUID không tương thích với candidate int64. |
| Auth | Bearer JWT; role Admin. AC-35 nêu quiz-management permission. | Shared guard chỉ cho `ADMIN`, trước path validation và DB. | Cần owner quyết định permission mapping/route guard; không xem `ADMIN` tự động tương đương permission nghiệp vụ. |
| Success | HTTP 200 `DESIGN_RESOURCE_DELETED`; `ApiEnvelope<DeleteResult>`, gồm `id:int64`, `status:"deleted"`, `deleted_at:date-time`. | Envelope trả `success`, `businessCode`, `message`, `data`, `meta`, `traceId`. Local map nhánh soft/repeat từ `updated_at`; nhánh hard lấy `CURRENT_TIMESTAMP`. | Chỉ xử lý success khi HTTP 200 và envelope hợp lệ. Không suy ra data target hoặc audit log từ response. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR`. Không có 409. | Cùng status/business codes trên route. Local validator trả 422 với lỗi `quiz_id` không phải positive signed-int64; lỗi này là validation, không phải dependency conflict. | Không tạo state/API branch 409. Unauthorized/forbidden/not-found/invalid-id/service error phải được phân biệt. |
| Attempt/history policy | AC-35 node n10: soft-delete nếu Quiz đã có attempts; không xác định no-attempt branch. | Local code soft-deletes khi có attempt **hoặc linked answer**; nếu không có hai loại history này thì hard-delete children rồi Quiz. Đây là nhánh `DERIVED`, chưa được owner duyệt. | Không hứa hành vi từ mockup hoặc local implementation cho đến khi policy được chốt. |
| Retry/idempotency | Catalog không quy định timeout/retry/idempotency hoặc DELETE lặp. | Local tombstone DELETE lặp trả 200 với timestamp cũ; đây là local behavior, chưa phải contract được duyệt. | Không tự động retry request mơ hồ cho đến khi retry/idempotency/reconciliation policy được xác nhận. |

### Discrepancy, blocker và trạng thái chứng cứ

1. **No-attempt delete:** AC-35 chỉ nói soft-delete nếu có attempts. Local #90 hard-delete khi không có attempt/answer, nhưng API DD đánh dấu nhánh này `DERIVED`; cần Product/BE duyệt trước khi bật action.
2. **Answer-only history:** local #90 soft-delete nếu có answer tham chiếu dù không có attempt. AC chỉ đề cập attempts; trường hợp này cần policy quyết định.
3. **Conflict:** row 76 của inventory nói “nếu conflict giữ nguyên màn”, nhưng #90 catalog không khai báo 409 và local #90 không trả dependency conflict cho history. Không đồng nhất HTTP 422 path validation với conflict. Đây là `DISCREPANCY` cần sửa contract/tracker sau khi owner quyết định.
4. **Race với attempt creation:** local #90 khóa Quiz trước khi kiểm tra history; không có current API #29 route/module trong checkout để chứng minh create-attempt có cùng lock/state guard. Không khẳng định cross-API race-safe.
5. **Permission:** AC-35 quiz-management permission khác với local role-only `ADMIN`; cần nguồn policy và cách guard.
6. **Visibility/lifecycle:** local #87 ẩn `status='DELETED'`; #89 từ chối sửa history/tombstone; #91 vẫn có thể trả thống kê từ Quiz/tombstone và attempt history. Cần duyệt hành vi sau xóa xuyên AC-35.
7. **Target data:** không có GET quiz detail. #87 không có course title/attempt count/history summary; HTML hiện hiển thị placeholder. Không thêm API hoặc trường dữ liệu theo suy đoán.
8. **Audit claim:** textarea/lý do kiểm toán bị disabled trong prototype; API #90 không nhận body. Không gửi reason hoặc khẳng định đã ghi audit event. Copy “ISO-27001”/“SAFE-GUARD” chỉ là nội dung mockup.
9. **Runtime/schema:** Study Web chưa wired; API #90 DD Draft; local legacy schema candidate không chứng minh live deployment. API test report là bằng chứng của lần chạy 2026-11-01, không phải runtime của màn hình ở phiên này.
