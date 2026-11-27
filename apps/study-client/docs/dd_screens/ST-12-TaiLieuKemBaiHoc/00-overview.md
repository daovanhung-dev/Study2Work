# ST-12 — Tài liệu kèm bài học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-12` |
| Module | Student |
| Route | `/student/lessons/:lessonId/resources` — khai báo trong Study Client; live runtime chưa xác minh |
| Actor/role | Student; client dùng Student Bearer service và API #26 kiểm tra enrollment |
| DD status | Draft/contract còn mở; **Implementation:** PARTIAL · **Runtime:** NOT VERIFIED |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.3 / 2026-11-27 |
| Nguồn đối chiếu | [ST-12.md](../../screen_stitch/03_student/ST-12_tai-lieu-kem-bai-hoc/ST-12.md), [ST-12_PLAN.md](../../screen_stitch/03_student/ST-12_tai-lieu-kem-bai-hoc/ST-12_PLAN.md), [ST-12_markers.json](../../screen_stitch/03_student/ST-12_tai-lieu-kem-bai-hoc/ST-12_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Tài nguyên theo lesson, xem/tải an toàn và quay lại vị trí học.
- In-scope: GET #26; nếu có resource_id hợp lệ GET #12; không tự mở URL ngoài chính sách.
- Out-of-scope: Xem gate bên dưới; local route/source evidence không chứng minh authenticated browser, live API/database hoặc deployment runtime.

### Current implementation — 2026-11-27

- Study Client có route và gọi #26 qua Student Bearer service. ST-12 theo dõi thay đổi `lessonId`, hủy request cũ, kiểm tra business code/payload/lesson ID, hiển thị loading/list/empty/error và cung cấp retry.
- API #26 kiểm tra Student, enrollment `ACTIVE`, lesson và course `PUBLISHED`; trả metadata resource với URL rỗng/null. ST-12 chỉ truyền `resourceId` sang GS-07; GS-07 gọi #12 để áp dụng current PUBLIC/PRIVATE handling. Five routed ST-12 tests cover list, empty, retry, ID handoff, and rejection of a non-null URL; one service test verifies #26 request mapping. The full Study Web suite passes 95 spec files/339 tests. The production build exits 0 at 474.39 kB initial; 18 component-style warnings remain across other screens, and ST-12 has no stylesheet budget warning.
- #26 đọc từ bảng `resources`; API #47 hiện ghi `lesson_uploads`, và chưa tìm thấy writer cho `resources`. Vì vậy dữ liệu ST-12 chưa có nguồn ghi được xác nhận. Không tự thêm side effect cho #47.
- Original Stitch unavailable state and the current loaded-list presentation are not aligned; the API #26 `Lesson` catalog shape also differs from the current `LessonResources` response. Local page/service tests do not approve those design or contract choices. Browser, live API/database, storage, and deployment runtime remain unverified. The DD excerpts below preserve expected behavior while current-source statements are reconciled against the implementation.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-15 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Tài nguyên theo lesson, xem/tải an toàn và quay lại vị trí học. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #26, #12
- Liên kết màn hình dự kiến: [ST-11](../ST-11-TrinhHocBaiLessonPlayer/00-overview.md), [GS-07](../GS-07-XemTaiTaiNguyen/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | empty/loading/available/forbidden |
| Current source | Study Client ST-12 | `loading / error+retry / resource list / empty`; runtime chưa xác minh |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-12 source screen.png](../../screen_stitch/03_student/ST-12_tai-lieu-kem-bai-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-12_tai-lieu-kem-bai-hoc/screen_annotated.png))
- Expected flow: GET #26, then #12 through GS-07 for a selected resource. Current ST-12 calls #26 and hands off the selected resource ID to GS-07; it does not open the list item's URL.
- Priority: P2; Gate/source status: **DD BLOCKED; IMPLEMENTATION PARTIAL; RUNTIME NOT VERIFIED:** #26 route/source and Student caller exist, but its resource-table producer is unresolved; #12's private URL policy and visible resource are handled by GS-07; DD/cardinality/access policy and canonical schema remain open; Stitch list design differs from the live page; live DB/runtime unverified.

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.
- 2026-11-20 — Cập nhật source hiện tại: #26/route đã wired; ST-12 kiểm tra payload/route và chuyển ID sang GS-07; API #47 `lesson_uploads` chưa nối với nguồn đọc `resources`.

## Trạng thái và ranh giới bằng chứng

# ST-12 — Tài liệu kèm bài học

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | `ST-12` — Tài liệu kèm bài học (Bảng) |
| Mục tiêu kỳ vọng | Cho Student xem tài nguyên gắn với lesson, lấy metadata của tài nguyên được chọn khi cần, rồi quay lại bài học hoặc mở luồng xem tài nguyên đã được duyệt. |
| Actor | Student theo AC-15 và catalog API #26. Tên/avatar `Nguyễn Văn A` trong prototype là dữ liệu tĩnh, không chứng minh danh tính hiện tại. |
| Route đề xuất | `/student/lessons/:lessonId/resources`; the current Study Client route and page are source-backed, but runtime is not verified. |
| AC | AC-15 — Xem nội dung bài học; precondition là Student có quyền xem lesson. |
| API thiết kế | #26 `GET /api/v1/lessons/{lesson_id}/resources`, sau đó #12 `GET /api/v1/resources/{resource_id}` nếu đã có `resource_id` hợp lệ và policy xác nhận cần gọi API chi tiết. |
| Màn hình liên quan | ST-11 là lesson context; GS-07 là màn hình xem/tải resource. Current ST-12 links to ST-11 with `lessonId` and to GS-07 with `resourceId` plus lesson return context; access/open policy remains source-backed only. |
| Tài sản | [`screen.png`](../../screen_stitch/03_student/ST-12_tai-lieu-kem-bai-hoc/screen.png) nguyên trạng 1600×1504; [`code.html`](../../screen_stitch/03_student/ST-12_tai-lieu-kem-bai-hoc/code.html) prototype tĩnh; [`screen_annotated.png`](../../screen_stitch/03_student/ST-12_tai-lieu-kem-bai-hoc/screen_annotated.png) là bản đánh số riêng. |
| Trạng thái | `DD BLOCKED` · `IMPLEMENTATION PARTIAL` · `RUNTIME NOT VERIFIED`. Đây là ba nhãn độc lập. |

### EXPECTED_BEHAVIOR — điều được yêu cầu/khai báo

- `list_screen.md` ST-12 đề xuất route Student, gọi #26 để lấy tài nguyên lesson, gọi #12 khi đã có resource ID hợp lệ, không tự mở URL ngoài chính sách; liên kết ST-11 và GS-07.
- API catalog yêu cầu Bearer JWT với role Student cho #26, `lesson_id:int64!`, không query/body, nhưng lại khai báo `ApiEnvelope<Lesson>`. API #26 DD đang Draft và xác nhận type/cardinality/empty behavior chưa chốt.
- AC-15 yêu cầu Student có quyền xem lesson và hậu điều kiện hiển thị nội dung, tài nguyên, điều hướng bài tiếp theo. Diagram mô tả API #26 trong luồng đó; đây là expected design, không phải runtime.
- Ảnh ST-12 thể hiện một trạng thái không có tài liệu khả dụng và copy bảo mật. Nó không định nghĩa response/API condition tạo ra trạng thái này.

### CURRENT_BEHAVIOR — bằng chứng hiện tại

- Current source contains the Student route, #26 caller, API-backed resource list/empty/error states, retry, a lesson-context back link, and a GS-07 resource-ID handoff. Local routed/service tests cover these source behaviors. They do not prove an authenticated browser session, live #26/#12 response, storage, or deployment. The static `screen.png` and `code.html` remain prototype assets, not runtime evidence.
- `screen.png` là ảnh thiết kế ở trạng thái unavailable/fallback. HTML có cấu trúc tĩnh cùng nội dung, tải Tailwind/font ngoài; không có page-level `fetch`, listener, timer hoặc router. Các anchor đều `href="#"`; `data-path` chỉ là attribute trong HTML.
- API #26 route/module/query/test source hiện tại tồn tại; server handler trả `LessonResources.resources[]` sau Student, enrollment ACTIVE và PUBLISHED checks. Mismatch catalog `ApiEnvelope<Lesson>` vẫn còn.
- API #12 current source returns `visibility`; PUBLIC uses direct HTTP(S), while PRIVATE requires Student auth, published parent and ACTIVE enrollment, then a signed URL with 300-second TTL. ST-12 passes only the resource ID and lesson return context to GS-07; GS-07 owns the #12 call/open action. The current local Guest #07–#12 test suite has 90 passing tests; this is not live runtime evidence.
- Cover của API #12 DD vẫn ghi chưa xác minh runtime/OpenAPI, dù current tree có route, module và focused test source (trong đó có OpenAPI-path assertion). Guest #07–#12 local suite passes 90 tests; đây là discrepancy tài liệu/source, không phải live runtime proof, và API DD vẫn `Draft — Needs Confirmation`.
- `infra/postgres/study-server/DB.sql` là DDL candidate legacy BIGINT; `resources.lesson_id` nullable, không có `visibility`. Scoped search trong V1-PILOT `infra/postgres/02_study_db.sql` không thấy table `resources`; đây là schema model riêng. Không chứng minh live schema hoặc mapping giữa hai model.

### Điều kiện vào/ra

- **Precondition kỳ vọng:** route có `lessonId` hợp lệ và người dùng là Student có quyền xem lesson theo AC-15. Catalog #26 khai báo Student Bearer; authorization predicate/claim binding chưa được API owner chốt.
- **Postcondition kỳ vọng:** danh sách Resource được hiển thị theo contract đã duyệt; khi chọn item, metadata/open action tuân theo policy; người học có thể quay lại ST-11 với context đã được xác nhận.
- **Hiện tại:** route, #26 request/list payload, empty/error/retry behavior and the ID-only GS-07 handoff are source-backed and locally tested. Authenticated browser session, live API/database, storage and deployment transitions remain unverified. Do not interpret fallback copy as a specific HTTP empty/403 result.
