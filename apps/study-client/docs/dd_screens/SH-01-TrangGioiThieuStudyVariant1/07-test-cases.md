# SH-01 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `SH-01-TC-001` | Planning ref / not run | `AC-03` | See source acceptance section | P0 |

## 2. Test planning references

### SH-01-TC-001 — Acceptance planning reference (AC-03)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [SH-01](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/SH-01.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-03`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/SH-01.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: 9. Ma trận kiểm tra và rà soát (dự kiến; chưa chạy)

| Tình huống | Kết quả cần xác minh |
|---|---|
| #05 và #06 đều có dữ liệu | Mỗi khu vực ánh xạ riêng; không xuất hiện bản ghi mẫu tĩnh |
| #05 rỗng, #06 có dữ liệu | Thẻ khóa học vẫn hiện; trạng thái danh mục rỗng độc lập |
| #06 rỗng, #05 có dữ liệu | Thông tin danh mục vẫn còn; trạng thái khóa học không có thẻ giả |
| #05 lỗi, #06 thành công | Khu vực khóa học vẫn dùng được; thử lại danh mục chỉ tác động #05 |
| #06 lỗi, #05 thành công | Danh mục vẫn hiện; thử lại khóa học chỉ tác động #06 |
| #06 trả 422 vì category | Client không gửi category; ghi nhận hồi quy, không lặp mù |
| Tìm kiếm có khoảng trắng đầu/cuối | SH-01 loại khoảng trắng, chuyển q đã mã hóa tới GS-02; không gọi #07 tại đây |
| Tìm kiếm rỗng | Không gọi API; không tự đặt câu báo lỗi |
| Bấm thẻ danh mục | Không gửi bộ lọc khi G-05 còn mở |
| Chọn khóa học | Không tạo trạng thái chi tiết giả; tiếp tục chặn điều hướng cho tới khi quyết định #08/route |
| 401/403/500/lỗi mạng | Không tự chuyển đăng nhập cho GET công khai; khôi phục an toàn theo khu vực |
| Bàn phím/di động/tiếp cận | Rà soát focus, nhãn, vùng chạm 44px và bố cục 320px theo hướng dẫn chuẩn |
| Rà soát nguồn gốc | Không trình bày KPI, siêu dữ liệu khóa học, lời chứng thực, logo hoặc thu thập email chỉ có trên ảnh như dữ liệu đã xác thực |

Mã nguồn kiểm thử phía máy chủ liên quan: [API #05 tests](../../../../study-server/tests/modules/guest/api_05_categories/test_categories.py) (gồm test_categories_empty_result_is_successful_empty_page) và [API #06 tests](../../../../study-server/tests/modules/guest/api_06_courses/test_courses.py) (gồm test_courses_rejects_category_until_relation_exists cùng kiểm tra phân trang/lỗi). Đây là test source sử dụng fake session/data; chưa chạy trong phiên tài liệu. Hiện không có mã UI Study Web để kiểm thử.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 6. States, blockers and review gates

- **Static/design state:** current `screen.png` and `code.html` do not have a shared runtime state or API binding. HTML shows hard-coded examples and an empty-state block simultaneously. Do not equate this with current application behavior.
- **Future independently loaded regions:** categories `INITIAL → LOADING → READY/EMPTY/ERROR`; courses `INITIAL → LOADING → READY/EMPTY/ERROR`. A failure in one region must not erase a success in the other. 401/403 from public GET is unexpected; 422/500/network remain errors and must not become empty success.
- **Navigation/input:** blank search does not request; nonblank search transfers trimmed/encoded q to GS-02; auth/catalog routes remain proposals; invalid/unknown destinations are not fabricated.
- **Blockers:** (1) Study Web source/router absent; (2) no decision selecting screenshot versus HTML as authoritative; (3) API #06 contract lists category while current source rejects it and no legacy course-category relation exists; (4) direct course-card target GS-03/#08 conflicts with SH-01 next-screen list; (5) KPI, ratings, price currency, durations, testimonials, logos, certification and email collection lack source/approval; (6) variant-2 not found; (7) API DD approval and live DB/schema/deployment are not verified; (8) image/design guide drift needs frontend implementation decision.

### Trích từ DD nguồn: 7. Static acceptance checklist

- [x] This revised plan precedes marker map, annotation and DD update.
- [x] 26 unique ordered markers map one-to-one to 26 DD Element IDs and describe every visible component group.
- [x] Annotated image retains original screenshot content/aspect within the annotation canvas; badges do not cover text or controls.
- [x] PNG/HTML source hashes are unchanged; only current `variant-1` is documented.
- [x] API #05/#06 current route, source, test source, catalog and DDL evidence are cross-linked; unsupported category/marketing data are explicit blockers.
- [x] DD includes API request/response/error mapping, 14 event paths, states, navigation, privacy, accessibility and design drift.
- [x] Thêm bảng đối chiếu tường minh các yêu cầu A–F của objective với section tương ứng trong DD để dễ nghiệm thu.
- [x] Relative Markdown links, marker numbering, image dimensions/hash and whitespace audit pass.
- [x] Tracker/worklog updated; status distinguishes `DD READY`/`DD BLOCKED`, `IMPLEMENTATION BLOCKED` and `RUNTIME NOT VERIFIED`.

### Trích từ DD nguồn: 9. Kế hoạch rà soát bổ sung (2026-11-07)

- **Scope:** chỉ re-audit SH-01 trong worktree hiện tại; không đổi contract, backend source, UI behavior hoặc assets gốc.
- **Đối chiếu:** kiểm tra lại inventory/AC-03, API #05/#06 route-module-query-model-test source, DDL candidate, Study Web source status, 26 marker↔element IDs, 14 event descriptions, fragment-link targets, source hashes và kích thước PNG.
- **Cải thiện dự kiến:** thêm bảng cross-reference A–F vào DD để chứng minh các deliverable của objective được đặt ở đâu; không thêm nghiệp vụ mới.
- **Gate:** giữ nguyên các discrepancy/blocker và ba trạng thái `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`; sau chỉnh sửa chạy lại static artifact/link/whitespace audit và `git diff --check` theo phạm vi.
- **Finding từ HTML:** có 16 fragment href, trong đó chỉ 5 trỏ tới section ID có thật; 5 `#` quay lên đầu trang và 6 auth/legal fragment không resolve. DD phải mô tả đúng các nhóm này, không gọi toàn bộ là `href="#"`.
- **Finding từ event audit:** EV-06/07 đã nêu mapping và nhánh rỗng trong phần xử lý nhưng chưa tách output/result thành trường dễ nghiệm thu; cần thêm kết quả thành công/rỗng riêng cho từng vùng. Dọn whitespace ở metadata DD để static check sạch.

### Kết quả re-audit

- Current API/source trace giữ nguyên: #05/#06 public routes, #06 category filter trả 422; DDL legacy không có course-category relation; Study Web source/router/package manifest không có trong checkout.
- Đã thêm cross-reference A–F trong DD §1.3; EV-06/07 có kết quả thành công/rỗng tách riêng; mô tả prototype fragment được sửa theo đúng target hiện có; metadata whitespace đã dọn.
- Static audit đạt: 26 marker tuần tự/duy nhất khớp 26 element rows và SVG labels; target nằm trong ảnh nguồn; 14 event tuần tự có trigger/điều kiện, input, process, result/output và exception/error; JSON/SVG parse; local Markdown links resolve; 16 fragment links được phân loại 5 section-target, 5 bare `#`, 6 unresolved.
- `screen.png` 559×1600 và `screen_annotated.png` 1230×3200; ảnh chú thích được xem trực tiếp; source `screen.png`/`code.html` hashes không đổi; authored whitespace scan và scoped `git diff --check` sạch.
- Không chạy application tests, Study Web runtime hay live DB. Status vẫn `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Screen tiếp theo W0 là SH-02 trong phiên riêng.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
