# AD-16 — Tạo/chỉnh sửa quiz · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-16` |
| Module | Admin |
| Route | `/admin/quizzes/new hoặc /admin/quizzes/:quizId/edit` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái:** `DD BLOCKED` · `IMPLEMENTATION BLOCKED` · `RUNTIME NOT VERIFIED`<br> |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-16.md](../../screen_stitch/05_admin/AD-16_tao-chinh-sua-quiz/AD-16.md), [AD-16_PLAN.md](../../screen_stitch/05_admin/AD-16_tao-chinh-sua-quiz/AD-16_PLAN.md), [AD-16_markers.json](../../screen_stitch/05_admin/AD-16_tao-chinh-sua-quiz/AD-16_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Builder create/update với dirty/draft-loss guard cần được chốt; AD-15 là entry, AD-17 là statistics handoff theo AC-35.
- In-scope: POST #88 khi tạo; PUT #89 khi sửa. Không giả định GET admin quiz detail; #87 metadata-only và `questions=[]` local. #89 catalog không khai báo body; local fallback yêu cầu replacement body. Autosave copy trong prototype chưa có persistence source.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-35 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Builder create/update với dirty/draft-loss guard cần được chốt; AD-15 là entry, AD-17 là statistics handoff theo AC-35. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #88, #89
- Liên kết màn hình dự kiến: [AD-15](../AD-15-DanhSachBaiKiemTra/00-overview.md), [AD-17](../AD-17-ThongKeBaiKiemTra/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | blank/draft/loading/ready/dirty/invalid/saving/created/updated/not-found/conflict/unauthorized/forbidden/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-16 source screen.png](../../screen_stitch/05_admin/AD-16_tao-chinh-sua-quiz/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-16_tao-chinh-sua-quiz/screen_annotated.png))
- Luồng: POST #88 khi tạo; PUT #89 khi sửa. Không giả định GET admin quiz detail; #87 metadata-only và `questions=[]` local. #89 catalog không khai báo body; local fallback yêu cầu replacement body. Autosave copy trong prototype chưa có persistence source.
- Priority: P1; Gate/source status: **R** local #88/#89 route/module/query/model/validator/test source; API DDs remain Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** thiếu GET detail/question set, #89 body discrepancy, question/choice editor và course option mapping; field/range rules, AC-35 permission vs `ADMIN`, legacy/V1-PILOT/live schema, autosave/navigation và Study Web `UNWIRED`; **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-16 — Tạo/chỉnh sửa bài kiểm tra

> **Trạng thái:** `DD BLOCKED` · `IMPLEMENTATION BLOCKED` · `RUNTIME NOT VERIFIED`<br>
> **Phạm vi:** Màn hình quản trị bài kiểm tra, AC-35, chỉ Screen ID AD-16.<br>
> **Quy ước chứng cứ:** `EXPECTED` là yêu cầu/contract; `CURRENT` là ảnh, HTML hoặc source hiện tại; `DERIVED` là hành vi chỉ có trong triển khai local nhưng chưa được owner duyệt; `BLOCKER` là điều kiện chưa đủ để triển khai an toàn.

Ảnh nguồn [screen.png](../../screen_stitch/05_admin/AD-16_tao-chinh-sua-quiz/screen.png) được giữ nguyên. Ảnh đánh số [screen_annotated.png](../../screen_stitch/05_admin/AD-16_tao-chinh-sua-quiz/screen_annotated.png) có 35 marker; [AD-16_markers.json](../../screen_stitch/05_admin/AD-16_tao-chinh-sua-quiz/AD-16_markers.json) là bản đồ ID/tọa độ, [AD-16_markers.svg](../../screen_stitch/05_admin/AD-16_tao-chinh-sua-quiz/AD-16_markers.svg) là overlay có thể kiểm tra. Kế hoạch được lập trước các artifact này tại [AD-16_PLAN.md](../../screen_stitch/05_admin/AD-16_tao-chinh-sua-quiz/AD-16_PLAN.md).

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### A.1. Mục tiêu, actor và trạng thái

| Thuộc tính | Đặc tả và bằng chứng |
|---|---|
| Screen ID / tên | `AD-16` — Tạo/chỉnh sửa quiz (Page); tiêu đề prototype “Thiết lập và biên tập bài kiểm tra trắc nghiệm”. |
| Mục tiêu | Cung cấp luồng cấu hình Quiz và Question/Choice để thực hiện nhánh CREATE API #88 hoặc UPDATE API #89 theo AC-35. |
| Actor | `EXPECTED`: Admin có `quiz management permission` theo AC-35. `CURRENT`: local endpoint dùng shared role guard `ADMIN`; mapping permission chi tiết chưa được xác nhận. |
| Điều kiện vào | Create đi từ AD-15 qua nhánh #88. Edit đi từ AD-15 qua #89 với Quiz ID. ID local/API là int64, nhưng route UI và truyền ID chưa được wire/duyệt. Yêu cầu authentication/authorization theo catalog là Bearer JWT, role Admin. |
| Điều kiện sau | AC-35 nêu Quiz được tạo/cập nhật. Nơi chuyển đến sau thành công, cách refetch AD-15, giữ filter/page, và điều kiện đi tiếp AD-17 chưa được định nghĩa. |
| Route | Candidate inventory: `/admin/quizzes/new` hoặc `/admin/quizzes/:quizId/edit`. Không có Study Web router/source trong checkout để xác minh route hoạt động. |
| Quan hệ màn hình | AD-15 là entry point/list; AD-17 là statistics screen tiếp theo theo AC-35. Nút Hủy quay về hash `#/admin/quizzes` trong HTML nhưng runtime navigation chưa được xác minh. |
| Triển khai UI | `UNWIRED`: folder Study Web hiện không có editable `src/`, package manifest, router hoặc API client. Screenshot/HTML chỉ là prototype tĩnh. |

### A.2. Contract API và current source

| API | Contract trực tiếp trong catalog | Current local source (không thay thế contract) |
|---|---|---|
| #88 Create | `POST /api/v1/admin/quizzes`; Bearer JWT/Admin; body `{config:string!, questions:string!}`; response `ApiEnvelope<Quiz>`; 201 `DESIGN_RESOURCE_CREATED`; 401/403/422/500. API DD `Draft — Needs Confirmation`. | Route #88 parse raw body sau shared `ADMIN` guard. Strict outer body gồm đúng hai chuỗi `config`, `questions`; validator decode hai chuỗi JSON và áp dụng nested shape `config{course_id:int,title:string,duration_minutes?:int|null,passing_score:string}`, `questions[{text,type,choices[{text,is_correct?}]}]`. Shape này là `DERIVED`. Local code chỉ xác nhận Course tồn tại, ghi Quiz + Question + Choice theo thứ tự request (candidate order zero-based), map response rồi mới commit; lỗi sau khi bắt đầu transaction rollback. Response local có `is_correct`. |
| #89 Update | `PUT /api/v1/admin/quizzes/{quiz_id}`; Bearer JWT/Admin; path `quiz_id:int64!`; catalog **không khai báo body**; response `ApiEnvelope<Quiz>`; 200 `DESIGN_RESOURCE_UPDATED`; 401/403/404/422/500. API DD `Draft — Needs Confirmation`. | Route local nhận raw body và path; shared `ADMIN` guard chạy trước parse. Local handler yêu cầu positive int64 và reuse validator/body như #88. Khóa Quiz/children; nếu có attempt hoặc answer history trả 422 trước write; xác nhận Course tồn tại (local fallback cho phép chuyển Quiz sang Course khác), không thấy policy course-status/enrollment; cập nhật metadata rồi xóa Choices trước Questions và thêm replacement set theo request order (candidate order zero-based); response mapping hoàn tất trước commit. Local source không có optimistic version. Body, full replacement, history refusal, course move, locks và tombstone handling là `DERIVED`. |

Không có `GET /api/v1/admin/quizzes/{quiz_id}` để tải dữ liệu edit. #87 là list metadata-only trong local source (`questions=[]`), còn catalog response cardinality cũng khác local Page projection. Vì vậy AD-16 không có nguồn xác nhận để prefill Quiz và Question Builder khi mở edit route. Không gọi #87 thay thế detail.

### A.3. Quy tắc dữ liệu, bảo mật và blocker

- Direct catalog chỉ công bố top-level body strings cho #88; cấu trúc JSON bên trong hai chuỗi chưa được catalog/API DD duyệt. Local nested fields, QuestionType `SINGLE_CHOICE|MULTIPLE_CHOICE|TRUE_FALSE`, `is_correct` mặc định false, thứ tự câu hỏi/lựa chọn và giới hạn storage là `DERIVED`.
- Local validator không yêu cầu title có ký tự tối thiểu hoặc Question/Choice array có số lượng tối thiểu; không suy ra câu hỏi rỗng được chấp nhận theo business policy chỉ vì local model cho phép. Cần owner chốt ràng buộc Quiz/Question/Choice.
- UI hiện đánh dấu tên và khóa học là bắt buộc, nhưng HTML không đặt thuộc tính `required`; local validator không yêu cầu title có ký tự tối thiểu. Local #88 yêu cầu `course_id` signed int64, title tối đa 200 ký tự, `duration_minutes` int32 nullable, `passing_score` decimal string lưu được trong NUMERIC(5,2) (local helper cho phép đến ±999.99). Đây là kiểm tra storage của source, không xác nhận business range.
- Prototype đặt `min=1,max=300` cho duration và `min=0,max=100` cho điểm. Các khoảng này không có trong contract catalog hoặc AC-35. UI score dùng number input nhưng local request nhận string; chuyển đổi/chính xác thập phân chưa có mapping được duyệt. UI hiện không có course option hoặc ID source.
- Local migration `013_quiz_question_type_and_choice_order.sql` bổ sung `question_type` nullable và `quiz_choices.sort_order`; đây là candidate trên legacy BIGINT schema, không chứng minh migration đã deploy. V1-PILOT dùng UUID `assessments/questions/options`, không được trộn với ID/schema hiện tại của API #88/#89.
- Admin response local có answer key `is_correct`; bất kỳ mapping nào sang Student API #28 phải loại bỏ field này. AC-35 permission chi tiết và local shared `ADMIN` guard chưa được reconcile.
- Các thông báo autosave, Safe Mode, RBAC, “SYSTEM NORMAL”, schema sync và Questions Builder Gate chỉ là copy prototype. Không có localStorage, API call, form submit hay auth check phía client.
- `.agents/web-study/design.md` là target ocean-blue, Inter/system, centered/responsive; prototype hiện dùng full-width cobalt/Plus Jakarta. Target design là quy chuẩn hướng tới, không phải bằng chứng runtime.
