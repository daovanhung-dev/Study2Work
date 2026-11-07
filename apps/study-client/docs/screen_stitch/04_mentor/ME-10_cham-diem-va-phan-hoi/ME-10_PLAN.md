# Kế hoạch Detailed Design — ME-10

> **Plan status:** COMPLETE — plan được ghi trước marker map, ảnh chú thích và DD.
> **Trạng thái mục tiêu sau kiểm tra:** `DD READY`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
> **Phạm vi phiên:** chỉ Screen ID **ME-10**.

## 1. Phân loại, phạm vi và nguồn

```text
primary_task_type: docs
secondary_task_types: []
project_scopes:
  - web-work
  - server-study
cross_scope_dependencies:
  - ME-09/#54 cung cấp submission ID → đề xuất route ME-10 → API #55 detail → API #56 grade và #57 feedback độc lập → GET #55 revalidate → quay lại ME-09
```

- Inventory: [ME-10 và F09 trong `list_screen.md`](../../../list_screen.md); AC-23; API catalog #55–#57.
- Asset đầu vào: `screen.png` 1600×1556, SHA-256 `7ea38f3a02bbe2d4e136ff24c854435fa5946eb6ad148bf73e488058b5a7a41a`; `code.html` SHA-256 `fb1c5ddfdde5dbb47969aa39a4dca2b7ccfdb0bb64cd633d243a78e4690e03cc`. Giữ nguyên hai file nguồn.
- Đối chiếu trực quan PNG/HTML: cùng bố cục, copy và các trạng thái mẫu trọng yếu (mã phiên, đang đồng bộ, chờ kết nối, rubric rỗng, form disabled, PENDING_AUTH/version); không phát hiện khác biệt nội dung đáng kể trong màn hình được cấp. Cả hai đều là static design input.
- Study Web hiện `UNWIRED`: không có editable source/package/router cho màn hình; HTML là mockup tĩnh, không gọi API. `createDD-markdown` không được registry wire cho `web-ui-only-dd`; không có skill canonical cho loại screen DD này.
- API #55–#57 có route/view/query source và test source trong Study Server. API DD vẫn `Draft — Needs Confirmation`; source hiện hành chứng minh hành vi local, không phê duyệt các fallback `DERIVED`, không chứng minh live schema hay deployment.
- #56/#57 route khai báo Pydantic body bắt buộc; FastAPI xử lý body validation trước khi gọi route function/view, còn middleware chuẩn hóa `RequestValidationError` thành 422 `DESIGN_VALIDATION_ERROR`. Vì vậy body thiếu/sai/extra field có thể kết thúc trước view-level MENTOR guard. Catalog chưa xác định thứ tự ưu tiên này; cần xác nhận contract.
- Hạn chế bắt buộc: không tự thêm trường rubric, body key, score scale, attachment format, status rule, storage hay transaction chung; giữ riêng yêu cầu, hiện trạng source và quyết định còn mở.

## 2. Mục tiêu và điều kiện nghiệm thu

Tạo một DD truy vết đầy đủ cho ảnh ME-10, phân ranh rõ expected/current behavior, xác định mọi thành phần nhìn thấy, chuỗi sự kiện/API/error, state/navigation và blockers. Marker JSON, SVG và PNG đánh số phải đồng nhất 1:1 với các dòng phần tử DD. Đường dẫn tương đối trong tài liệu phải tồn tại. Không đánh dấu implementation/runtime sẵn sàng khi Study Web chưa có source.

## 3. Expected behavior

Theo inventory/AC-23/F09:

1. Mentor mở bài đã chọn ở ME-09 bằng submission ID.
2. #55 đọc bài nộp cùng file và rubric; UI cho phép nhập điểm, rubric và nhận xét.
3. Gửi điểm qua #56 và gửi phản hồi qua #57 là hai thao tác riêng khi người dùng yêu cầu; mỗi thao tác có kết quả riêng, sau đó tải lại #55 để đồng bộ.
4. Có thể quay lại ME-09. Loading, dirty, grading, feedback-sent và conflict được inventory nêu; cách hiển thị lỗi phải theo API thực tế và các quyết định contract.

Đây là yêu cầu mong đợi, chưa phải kết luận contract đã được duyệt.

## 4. Current behavior và trace cần giữ trong DD

- HTML có header/nav, breadcrumb, session badge, nút quay lại, khung bài làm ở trạng thái “Đang chờ kết nối dữ liệu”, mã mẫu `SUB-VERIFYING`, refresh/report buttons, claim AES-256/WCAG 2.1 AA; form điểm `0–100` đang disabled, rubric `0/0`/empty state, feedback textarea, character counter, security warning, nút gửi disabled, trạng thái `PENDING_AUTH`, version và footer.
- Các link dùng `href="#"`; refresh/report/save không có handler. Script duy nhất cập nhật bộ đếm ký tự khi textarea phát `input`. Không có fetch, API client, navigation/router, debounce, max length, validation, persistence hay live sync.
- #55: MENTOR guard trước path/DB; signed-int64 path lỗi → 404; candidate `assignment_submissions` LEFT JOIN assignment/course để nhận biết orphan; owner khác → 403 theo fallback direct-owner; lỗi quan hệ/projection → 500. Reusable `SubmissionResponse` gồm bài nộp, optional score/feedback và tối đa một upload khớp URL/owner/purpose/course. **Không có rubric field/query.** Thành công 200 `DESIGN_RESOURCE_RETRIEVED`, read-only.
- #56: request source strict `{score:int32, rubric_items:string}`; extra fields bị cấm. Path không hợp lệ → 404; lock row, direct-owner check, range `0 <= score <= assignments.max_score` là DERIVED; update score NUMERIC(6,2), status=`GRADED`, giữ feedback; `rubric_items` không được lưu. Commit riêng sau projection hợp lệ. Không thấy status precondition/409; có thể chấm lại theo source hiện tại.
- #57: request source strict `{feedback_text:string, attachments:string}`; extra fields bị cấm. Path lỗi → 422; lock row, direct-owner check, chỉ cập nhật feedback; score/status giữ nguyên; không yêu cầu `GRADED`; gọi lại ghi đè feedback hiện có; `attachments` bị bỏ qua, không parse/lưu/echo. Commit riêng sau projection hợp lệ.
- #56 và #57 có row lock và transaction cục bộ riêng. Không tồn tại transaction xuyên hai HTTP request; UI phải thể hiện partial success và không tuyên bố thao tác nguyên tử.
- Candidate DB là legacy BIGINT tables; DDL/test source không xác minh schema live. File lookup theo URL là DERIVED, chưa có bằng chứng API #35 ghi cùng URL.

## 5. Phân vùng marker dự kiến

Tạo 39 marker đánh số liên tục; marker chỉ định thành phần nhìn thấy, không ngụ ý có chức năng runtime.

| Marker | Element ID | Phần tử |
|---:|---|---|
| 1 | ME10-EL-01 | Logo/brand Study2Work LMS Mentor |
| 2 | ME10-EL-02 | Nav Tổng quan |
| 3 | ME10-EL-03 | Nav Khóa học phụ trách |
| 4 | ME10-EL-04 | Nav Chấm bài đang chọn |
| 5 | ME10-EL-05 | Nav Hộp thư hỗ trợ |
| 6 | ME10-EL-06 | Nav Thông báo |
| 7 | ME10-EL-07 | Chuông thông báo |
| 8 | ME10-EL-08 | Danh tính/avatar Mentor mẫu |
| 9 | ME10-EL-09 | Breadcrumb Chấm bài → Chi tiết |
| 10 | ME10-EL-10 | Badge mã phiên mẫu |
| 11 | ME10-EL-11 | Eyebrow hệ thống điều phối |
| 12 | ME10-EL-12 | Tiêu đề màn hình |
| 13 | ME10-EL-13 | Mô tả màn hình |
| 14 | ME10-EL-14 | Nút quay lại ME-09 phía trên |
| 15 | ME10-EL-15 | Tiêu đề panel tệp bài làm |
| 16 | ME10-EL-16 | Badge “Đang đồng bộ” |
| 17 | ME10-EL-17 | Trạng thái chờ kết nối dữ liệu/illustration |
| 18 | ME10-EL-18 | Mã submission và progress kiểm định mẫu |
| 19 | ME10-EL-19 | Nút làm mới kết nối |
| 20 | ME10-EL-20 | Nút báo cáo sự cố tải file |
| 21 | ME10-EL-21 | Claim giao thức AES-256 |
| 22 | ME10-EL-22 | Claim khung WCAG 2.1 AA |
| 23 | ME10-EL-23 | Dải lưu ý về file đã quét/xác minh |
| 24 | ME10-EL-24 | Nhãn điểm và khóa chỉnh sửa |
| 25 | ME10-EL-25 | Input điểm disabled, `/100` và gợi ý |
| 26 | ME10-EL-26 | Tiêu đề rubric và bộ đếm 0/0 |
| 27 | ME10-EL-27 | Empty state rubric tự động |
| 28 | ME10-EL-28 | Nhãn nhận xét và character counter |
| 29 | ME10-EL-29 | Textarea nhận xét |
| 30 | ME10-EL-30 | Gợi ý Markdown |
| 31 | ME10-EL-31 | Cảnh báo an toàn dữ liệu |
| 32 | ME10-EL-32 | Nút lưu điểm và gửi nhận xét disabled |
| 33 | ME10-EL-33 | Nút quay lại ME-09 phía dưới |
| 34 | ME10-EL-34 | Trạng thái chữ ký số mẫu `PENDING_AUTH` |
| 35 | ME10-EL-35 | Version mẫu `v2.4.1` |
| 36 | ME10-EL-36 | Brand/copyright footer |
| 37 | ME10-EL-37 | Link Quy chế Giảng viên |
| 38 | ME10-EL-38 | Link Tiêu chuẩn đánh giá |
| 39 | ME10-EL-39 | Link Hỗ trợ kỹ thuật |

## 6. Chuỗi sự kiện dự kiến cho DD

1. `Load detail`: route entry với submissionId → validate nguồn ID/session; #55 → map success/error/empty-content fields → detail/loading/denied/not-found/system-error. Không giả định rubric hoặc file tồn tại.
2. `Refresh connection`: hiện HTML chỉ có nút, không có handler. Nếu future action gọi #55, ghi rõ request/retry/double-submit/cancel và state sau contract approval.
3. `Input score`: prototype input disabled và không có min/max. Không bật trước khi score scale, field/range, rubric mapping và #56 body được chốt.
4. `Edit feedback`: textarea tự do; hiện chỉ cập nhật ký tự local, không có giới hạn/validation. Dirty state và bảo toàn nội dung khi lỗi là yêu cầu cần thiết kế, nhưng không tự áp giới hạn.
5. `Submit grade (#56)`: chỉ khi form/body contract được xác nhận; nêu strict int32/range fallback, response, lỗi và revalidation. Không giả định `rubric_items` được lưu.
6. `Submit feedback (#57)`: event tách riêng, ghi `feedback_text`/`attachments` theo current fallback nhưng nhấn mạnh `attachments` không persisted; state thành công không phụ thuộc #56.
7. `Partial success/retry`: nếu một API thành công còn API kia lỗi, giữ kết quả/dirty input riêng; retry chỉ thao tác thất bại sau quyết định idempotency/overwrite; không submit API còn lại ngầm.
8. `Return ME-09`: hai link mockup chưa wired. Future return cần quyết định giữ filter/page/cache; source không chứng minh điều này.

## 7. State, blocker và status

- Tối thiểu mô tả `initial/loading`, `ready`, `detail-error`, `not-found`, `access-denied`, `auth-required`, `dirty`, `grade-saving`, `grade-saved`, `feedback-saving`, `feedback-saved`, `partial-success`, `retryable-system-error`, `conflict` (inventory label, nhưng #55–#57 source hiện không phát 409), `returning`.
- Blockers cần thể hiện: rubric wire/schema/persistence; score scale/decimal/range; `rubric_items` semantics; feedback attachment payload/storage; #55 response rubric gap; grade eligibility/regrade/history; cross-call atomicity (source hiện separate); Student result visibility; Mentor direct-owner vs assigned; URL producer/API #35; schema live; route/UI implementation.
- Tách ba trạng thái: `DD READY` khi đủ tài sản/marker, đầy đủ element/event/state, truy vết source và ghi rõ mọi quyết định mở; `IMPLEMENTATION BLOCKED` vì Study Web source/route absent và contract decisions chưa khóa; `RUNTIME NOT VERIFIED` vì chưa có screen runtime (không chạy server/UI test).

## 8. Việc thực hiện sau plan

1. Sinh `ME-10_markers.json` theo 39 dòng trên; cùng `ME-10_markers_overlay.svg`.
2. Render `screen_annotated.png` đúng tỷ lệ 2× từ PNG gốc và SVG overlay; không thay đổi `screen.png`/`code.html`.
3. Quan sát ảnh hoàn chỉnh, chỉnh marker nào che chữ/control; kiểm tra bounds, unique IDs/numbers và 1:1 với DD.
4. Viết `ME-10.md` các mục A–F, gồm element map, event IDs/tuần tự/API/error/cache/output/exception, state matrix, navigation, security/privacy, accessibility/adaptation, open decisions và acceptance checklist.
5. Cập nhật row ME-10 và checkpoint/số lượng hiện tại trong `screen_stitch/dd_screens/PLAN.md`; hoàn tất worklog cùng phiên.
6. Chạy kiểm tra tĩnh cho JSON/SVG/PNG/links/hash/diff formatting; không chạy tests hoặc runtime trong phiên docs này.

## 9. Kết quả thực hiện

- Plan hoàn tất trước `ME-10_markers.json`, `ME-10_markers_overlay.svg`, `screen_annotated.png` và `ME-10.md`.
- Tạo 39 marker tuần tự. Ảnh chú thích lấy `screen.png` nguyên trạng, scale 2× thành 3200×3112; đã xem trực tiếp toàn ảnh và dời các marker ở header, heading, score/rubric, advisory và footer ra khoảng trắng.
- DD có 39 element rows, 10 event IDs, state/navigation matrix, API #55–#57 source trace/error mapping, privacy/accessibility, open decisions và acceptance checklist.
- Rà soát bổ sung route signature và validation middleware: body Pydantic không hợp lệ của #56/#57 có thể trả 422 trước view-level MENTOR guard; đã ghi thành contract precedence question, không coi là behavior đã được API catalog phê duyệt.
- Static audit: JSON hợp lệ; IDs/numbers unique và in-bounds; SVG có đúng 39 group IDs theo thứ tự; relative links hợp lệ; PNG/HTML nguồn giữ đúng hash; `git diff --check` sạch.
- Tracker đã cập nhật ME-10 thành `DD READY`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Chỉ xác nhận runtime khi screen thực tế được wire và chạy kiểm chứng riêng.
