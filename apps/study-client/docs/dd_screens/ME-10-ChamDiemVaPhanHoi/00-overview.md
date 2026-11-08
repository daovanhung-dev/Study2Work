# ME-10 — Chấm điểm và phản hồi · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-10` |
| Module | Mentor |
| Route | `/mentor/submissions/:submissionId` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `DD READY` — đủ bản đồ element/sự kiện, source trace, state và blocker; các quyết định mở được nêu rõ, không được xem là contract đã duyệt.; **Implementation status:** `IMPLEMENTATION BLOCKED` — Study Web chưa có source/route; rubric, score và feedback attachment contract còn thiếu.; **Runtime status:** `RUNTIME NOT VERIFIED` — không có ME-10 runtime trong checkout; phiên này không chạy test hay screen runtime. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ME-10.md](../../screen_stitch/04_mentor/ME-10_cham-diem-va-phan-hoi/ME-10.md), [ME-10_PLAN.md](../../screen_stitch/04_mentor/ME-10_cham-diem-va-phan-hoi/ME-10_PLAN.md), [ME-10_markers.json](../../screen_stitch/04_mentor/ME-10_cham-diem-va-phan-hoi/ME-10_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Đọc bài làm + file, form điểm, rubric, nhận xét; tách 2 thao tác nếu API tách.
- In-scope: GET #55 → POST #56 điểm → POST #57 feedback khi người dùng yêu cầu → revalidate #55.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-23 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Đọc bài làm + file, form điểm, rubric, nhận xét; tách 2 thao tác nếu API tách. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #55, #56, #57
- Liên kết màn hình dự kiến: [ME-09](../ME-09-DanhSachBaiCanCham/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/dirty/grading/feedback-sent/conflict |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-10 source screen.png](../../screen_stitch/04_mentor/ME-10_cham-diem-va-phan-hoi/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-10_cham-diem-va-phan-hoi/screen_annotated.png))
- Luồng: GET #55 → POST #56 điểm → POST #57 feedback khi người dùng yêu cầu → revalidate #55.
- Priority: P1; Gate/source status: **D**; **BLOCK:** Rubric fields, score type, atomicity chưa khóa

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ME-10 — Chấm điểm và phản hồi

> **DD status:** `DD READY` — đủ bản đồ element/sự kiện, source trace, state và blocker; các quyết định mở được nêu rõ, không được xem là contract đã duyệt.
> **Implementation status:** `IMPLEMENTATION BLOCKED` — Study Web chưa có source/route; rubric, score và feedback attachment contract còn thiếu.
> **Runtime status:** `RUNTIME NOT VERIFIED` — không có ME-10 runtime trong checkout; phiên này không chạy test hay screen runtime.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### A.1. Mục tiêu và phạm vi

| Thuộc tính | Mô tả |
|---|---|
| Screen ID | ME-10 |
| Tên | Chấm điểm và phản hồi |
| Mục tiêu kỳ vọng | Mentor đọc một bài nộp đã chọn, nhập điểm/rubric, gửi feedback; xem kết quả từng mutation riêng. |
| Actor | Mentor có Bearer role `MENTOR`; API guard xác minh vai trò. Danh tính hiển thị trong ảnh chỉ là dữ liệu mẫu. |
| Route đề xuất | `/mentor/submissions/:submissionId`; đây là route UI trong inventory, chưa có router/source để xác minh. |
| API detail | #55 `GET /api/v1/mentor/submissions/{submission_id}` |
| API mutations | #56 `POST /api/v1/mentor/submissions/{submission_id}/grade`; #57 `POST /api/v1/mentor/submissions/{submission_id}/feedback` |
| Màn hình trước/quay lại | ME-09; expected ID đến từ `data.items[].id` của #54. Cả hai link quay lại trong mockup dùng `href="#"`. |
| Dữ liệu nhạy cảm | Submission content, file URL/metadata, `user_id`, score và feedback. Chỉ dùng response được server phân quyền; không log raw content, URL hay feedback. |
| Hiện trạng | Study Web `UNWIRED`. Ảnh/HTML là design input; không chứng minh runtime, session, đồng bộ hay kết quả scan. |

### A.2. Điều kiện vào/ra và dữ liệu

- **Expected:** ME-09 chọn một submission, chuyển ID qua proposed route ME-10. F09 nối #54 → #55 → #56 và #57 tách biệt → revalidate #55 → quay lại ME-09.
- **Current API #55:** path nhận ID signed-int64; nguồn route nhận raw string rồi view parse. #55 trả reusable `Submission` với `id`, `assignment_id`, `user_id`, `content?`, `files[]`, `status`, `submitted_at`, `score?` (decimal string), `feedback?`. Response không có `rubric`, assignment title, student display name, deadline, `max_score` hoặc feedback attachments.
- **Current API #56:** body strict `{score:int32, rubric_items:string}`. `score` được kiểm tra theo fallback DERIVED `0 <= score <= assignments.max_score`. API ghi score và `status=GRADED`; `rubric_items` được nhận nhưng bỏ qua vì không có persistence target được hỗ trợ.
- **Current API #57:** body strict `{feedback_text:string, attachments:string}`. API ghi một cột feedback; `attachments` opaque, bị bỏ qua. Không có precondition `status=GRADED`.
- **Đối chiếu tài sản:** PNG và HTML khớp nhau ở bố cục/label và các state mẫu chính; không thấy divergence nội dung đáng kể. Hai nguồn cùng tĩnh và không có API interaction.
- **Không tự tạo defaults:** không gửi điểm `0`, rubric rỗng, `attachments=""`, tên Student, điểm tối đa 100 hoặc dữ liệu phiên mẫu làm dữ liệu thật. Field/encoding/persistence chưa được owner duyệt.
- **Exit:** quay ME-09 theo history/back route nếu được implement; giữ filter/page/cache khi quay lại là quyết định UI chưa có source. Sau mỗi mutation success, F09 yêu cầu tải lại #55; hai mutation có thể thành công độc lập.

### A.3. Tách Expected behavior và Current behavior

**Expected behavior** lấy từ [inventory ME-10/F09](../../list_screen.md) và [AC-23 activity/API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md): Mentor có quyền chấm; đọc Submission + files + rubric; lưu score/status và feedback; Student có thể nhận kết quả. Flow F09 nói #56 và #57 có thể thành công độc lập và cần hiển thị trạng thái riêng rồi revalidate #55.

**Current behavior** lấy từ mockup/HTML và Study Server source: màn hình chỉ có mockup tĩnh. #55–#57 có route/view/query source, nhưng dùng một số fallback `DERIVED`; API DD còn `Draft — Needs Confirmation`, checked-in DDL chỉ là candidate, live DB/deployment chưa được xác minh. Các mô tả “Đang đồng bộ”, `PENDING_AUTH`, AES-256, WCAG, tự kiểm định và thang 0–100 là copy/giá trị mẫu, không phải bằng chứng hoạt động.

### A.4. Discrepancy và blocker bắt buộc giữ

| ID | Expected / asset | Current source | Quyết định/ảnh hưởng |
|---|---|---|---|
| ME10-B01 Rubric | AC-23 yêu cầu #55 đọc Submission + files + rubric; ảnh có rubric 0/0. | #55 query/model không có rubric; legacy Assignment/Submission không có quan hệ rubric được duyệt. #56 nhận `rubric_items` nhưng không persist. | Chốt rubric source, key/type/schema và persistence trước khi UI cho chấm theo tiêu chí. |
| ME10-B02 Score | Mockup ghi `0–100`, input disabled, `--/100`. | #56 yêu cầu `int32`, so sánh DERIVED với `assignments.max_score`, ghi NUMERIC(6,2). #55 không trả `max_score`. | Chốt scale, integer/decimal, bounds, max-score source và cách hiển thị decimal. |
| ME10-B03 Atomicity | Inventory/F09 tách trạng thái hai mutation. AC-23 mô tả #56 rồi #57. | #56 và #57 là hai POST, mỗi request lock/update/commit riêng; không có transaction xuyên request. | UI phải thể hiện điểm và feedback thành công/thất bại riêng; không dùng một kết quả chung. |
| ME10-B04 Combined action | Ảnh có một nút “Lưu điểm số và gửi nhận xét”. | #56 và #57 độc lập, body và lỗi khác nhau. | Chốt hai nút/action riêng hoặc thiết kế orchestration có partial-success rõ; không bật nút hiện tại như một mutation nguyên tử. |
| ME10-B05 Feedback attachment | #57 catalog yêu cầu `attachments:string`; mockup không có attachment picker. | Runtime chỉ kiểm tra chuỗi, không parse, lưu, echo hay gắn vào Submission.files. | Chốt format, asset source, persistence, response field và ownership; không gửi placeholder. |
| ME10-B06 Submission files | AC-23 muốn đọc file; mockup đang chờ kết nối. | #55 trả tối đa một `UploadAsset` theo exact URL + owner + purpose + course, fallback DERIVED; API #35 producer chưa chứng minh ghi đúng URL. | Xác nhận producer/storage relation; không hiển thị URL/file chưa match. |
| ME10-B07 Access | AC-23 cần Mentor có quyền chấm course. | #55–57 dùng shared MENTOR guard và direct `courses.mentor_id` fallback; assigned Mentor chưa có source. | Xác nhận direct owner/assigned Mentor, JWT mapping và 403/404 policy. |
| ME10-B08 Runtime/schema | Ảnh ghi sync, scan, AES và chữ ký số. | Không có editable Study Web source/router; candidate legacy DDL/fake-DB tests không xác minh live environment. | Gỡ hoặc xác minh các claim trước khi dùng như cam kết sản phẩm; runtime chưa verified. |
| ME10-B09 Lifecycle/visibility | AC-23 nói Student có thể nhận kết quả. | #56 đặt GRADED; #57 không yêu cầu GRADED; thời điểm Student visibility chưa được chốt. | Chốt regrade, history/audit, release timing và status lifecycle. |
| ME10-B10 Body/auth precedence | API catalog liệt kê 401/403/422 cho #56/#57 nhưng không quy định thứ tự khi body không hợp lệ. | Route dùng Pydantic body bắt buộc; FastAPI validation xảy ra trước khi gọi route function/view, middleware đổi `RequestValidationError` thành 422 `DESIGN_VALIDATION_ERROR`; view-level MENTOR guard chưa chạy ở nhánh này. | Xác nhận response precedence cho request thiếu/sai/extra body fields khi session thiếu/không hợp lệ; giữ 422 và auth response riêng trong UI mapping. |
