# ST-12 — Kế hoạch Detailed Design

## Trạng thái kế hoạch

- `primary_task_type`: `docs`
- `project_scopes`: `web-work`, `server-study`
- `cross_scope_dependencies`: ST-11 → ST-12 qua lesson context; ST-12 → GS-07 qua `resource_id`; API #26 → API #12.
- Phạm vi phiên: chỉ ST-12.
- Skill: không có skill UI-only DD được đăng ký trong `.agents/context-manifest.json`; `createDD-markdown` loại trừ `web-ui-only-dd`.
- Trạng thái khởi đầu: chưa có plan/DD/marker/ảnh chú thích cho ST-12.

## Kết quả mong đợi và hiện trạng nguồn

| Chủ đề | Kỳ vọng được khai báo | Hiện trạng được truy vết |
|---|---|---|
| Screen/route | Student, `/student/lessons/:lessonId/resources`, AC-15; API #26 tải tài nguyên theo lesson, #12 đọc resource được chọn; liên kết ST-11 và GS-07. | Study Web không có editable app source, package manifest hoặc Student router trong checkout. Route màn hình chưa được runtime xác minh. |
| API #26 | `GET /api/v1/lessons/{lesson_id}/resources`, Bearer JWT/Student, path `lesson_id:int64!`; catalog và AC diagram khai báo `ApiEnvelope<Lesson>`, errors 401/403/404/500. | Không tìm thấy route, module/query hoặc test API #26 trong Study Server. API DD là `Draft — Needs Confirmation`; payload `Lesson` không định nghĩa collection Resource. |
| API #12 | `GET /api/v1/resources/{resource_id}`, public theo catalog, `ApiEnvelope<Resource>`, 200/404/500. AC-06 mô tả quyền public/private và signer. | Route/module/test source có. Source yêu cầu positive signed-int64 ID; nếu resource có `lesson_id`, kiểm tra Lesson không `DELETED` và Course `PUBLISHED`; trả `id/name/type/url/lesson_id`, trong đó `url` là URL lưu DB. Không auth, visibility check, enrollment check hoặc signer. `lesson_id=null` bỏ qua parent check. |
| UI nguồn | Ảnh mô tả trạng thái không có tài liệu khả dụng; có CTA quay lại ST-11, trạng thái #26/#12, ghi chú kỹ thuật và link diễn đàn. | `screen.png` 1600×1504; HTML là prototype tĩnh, không có page handler/timer/API calls. Các anchor dùng `href="#"`; `data-path` không được router xử lý trong source hiện có. Ảnh và HTML được giữ nguyên. |
| Dữ liệu | Reusable `Resource` có `id/name/type/url?/visibility/lesson_id?`. | Catalog #26 trả `Lesson`; candidate DDL `resources` có `id, lesson_id, name, resource_type, url, created_at`, không có `visibility`; đây không phải live-schema evidence. |

## Tài sản nguồn cần bảo toàn

| Tệp | SHA-256 | Ghi chú |
|---|---|---|
| `screen.png` | `4cb94079bee1cc251b8be5efa6f6a7a59af3e1b41f5a689a0475b36e5486861f` | PNG 1600×1504; giữ nguyên bytes. |
| `code.html` | `69be5a1f8ed26c9636b32103499d1149a497c7edc7924bd1572e9eec5e928587` | UTF-8 HTML; giữ nguyên bytes. |

## Sơ đồ khu vực và marker dự kiến

Marker đánh vào thành phần có ý nghĩa giao diện/hành động. Tĩnh văn bản liên quan trong cùng component sẽ được nhóm trong một marker và mô tả riêng ở DD; không đánh số từng icon trang trí hoặc từng dòng text nội bộ.

| # | Element ID | Thành phần mục tiêu |
|---:|---|---|
| 1 | `ST12-EL-01` | Thương hiệu và thanh điều hướng đầu trang |
| 2 | `ST12-EL-02` | Tóm tắt người học/avatar |
| 3 | `ST12-EL-03` | Breadcrumb |
| 4 | `ST12-EL-04` | Nhãn route |
| 5 | `ST12-EL-05` | Nhãn Screen ID và trạng thái design |
| 6 | `ST12-EL-06` | Tiêu đề và mô tả màn hình |
| 7 | `ST12-EL-07` | Thẻ trạng thái hạ tầng dữ liệu |
| 8 | `ST12-EL-08` | Biểu tượng trạng thái chưa có tài liệu |
| 9 | `ST12-EL-09` | Nhãn chính sách kiểm soát truy cập |
| 10 | `ST12-EL-10` | Tiêu đề/thông điệp empty/fallback và giải thích |
| 11 | `ST12-EL-11` | CTA quay lại trình học ST-11 |
| 12 | `ST12-EL-12` | Dải ba tuyên bố bảo mật |
| 13 | `ST12-EL-13` | Tiêu đề vùng kiểm định kết nối |
| 14 | `ST12-EL-14` | Nhãn “Tự động làm mới mỗi 30s” |
| 15 | `ST12-EL-15` | Thẻ trạng thái API #26 |
| 16 | `ST12-EL-16` | Thẻ trạng thái API #12 |
| 17 | `ST12-EL-17` | Tiêu đề Hand-off Technical Notes |
| 18 | `ST12-EL-18` | Ghi chú không mở URL ngoài chính sách |
| 19 | `ST12-EL-19` | Ghi chú không giả lập metadata tài nguyên |
| 20 | `ST12-EL-20` | Ghi chú tiếp cận WCAG |
| 21 | `ST12-EL-21` | Ghi chú màu Ocean |
| 22 | `ST12-EL-22` | Badge phiên bản/“Valid Spec” |
| 23 | `ST12-EL-23` | Thẻ trợ giúp lấy tài liệu |
| 24 | `ST12-EL-24` | Link diễn đàn thảo luận |
| 25 | `ST12-EL-25` | Copyright ở footer |
| 26 | `ST12-EL-26` | Badge WCAG ở footer |
| 27 | `ST12-EL-27` | Nhóm link Điều khoản/Quyền riêng tư/Trợ giúp |

## Quy trình sự kiện cần mô tả trong DD

1. **ST12-EV-01 — Vào route và tải danh sách (#26):** mô tả contract kỳ vọng, `lessonId`, Student Bearer và status codes; đồng thời ghi `NOT_FOUND` cho runtime route/API, response `Lesson` mismatch và cardinality/empty/loading/error chưa chốt. Không tuyên bố màn hình hiện thực hiện request.
2. **ST12-EV-02 — Chọn tài nguyên và lấy metadata (#12):** chỉ là flow điều kiện sau khi #26 có payload Resource đã được duyệt và UI có chọn item. Ghi current #12 source, response trực tiếp, public/no auth, URL/access discrepancy; không mở URL từ prototype.
3. **ST12-EV-03 — Quay lại ST-11:** ghi CTA/`data-path`/`href="#"` hiện tại và route kỳ vọng có `lessonId`; history/position preservation chưa có contract.
4. **ST12-EV-04 — Mở diễn đàn trợ giúp:** ghi anchor prototype và destination/course context chưa xác nhận; không tự nối sang route khác.
5. **ST12-EV-05 — Shell/footer anchors:** mô tả `href="#"`/`data-path` là dữ liệu tĩnh, không có router handler.
6. Badge refresh 30 giây là copy tĩnh; không tạo timer/API polling event nếu chưa có yêu cầu và source.

## Trạng thái cần đặc tả

- Current screenshot: một trạng thái tĩnh “chưa có tài liệu hoặc policy đang cấu hình”, không phân biệt empty response, blocked API, unauthorized hoặc service error.
- Expected state machine cần để mở: route/auth check → loading #26 → approved empty / available collection / 401 / 403 / 404 / 500 / network error; nếu chọn resource thì loading #12 → metadata/open decision / 404 / 500. Các tên trạng thái chỉ là tiêu chí thiết kế, không phải behavior source-backed.
- Không xác nhận empty-list semantics, retry, polling, cache, selection, preview/download, token lifetime hay 404 destination.

## Blocker phải giữ nguyên trong DD

- `#26` không có current source; catalog/diagram response `Lesson` không khớp mục đích Resource collection.
- #26 cardinality, ordering, pagination, empty behavior, entitlement/JWT binding, 403/404 distinction, resource visibility, URL/signer ownership, path constraints và ResourceType enum còn mở trong API DD.
- #12 current source khác UI/API DD copy: không yêu cầu auth, không signer, không trả `visibility`, và trả stored URL; chỉ gate parent khi resource gắn lesson.
- API #12 là public nên việc gọi sau #26 không chứng minh server-side Student authorization; phải chốt chính sách resource access trước khi expose/open URL.
- Mockup claims “Zero Information Disclosure”, E2E, no public metadata, one-time token, refresh 30s, WCAG compliance/Valid Spec không có bằng chứng runtime; không coi là policy đã triển khai.
- Không có resource item/card trong ảnh; không thể suy ra trigger chọn tài liệu hoặc `resource_id` để gọi #12.
- ST-11 source cũng là unavailable fallback; entry/return context với GS-07 và lesson progress chưa được wire.
- Study Web runtime, production DB schema, API deployment và end-to-end behavior chưa được xác minh.

## Tiêu chí kiểm tra đầu ra ST-12

- [x] Plan gốc đã tồn tại trước DD/ảnh; re-audit của phiên này được ghi trước khi sửa DD.
- [x] Original `screen.png` và `code.html` giữ nguyên hash đã ghi trong marker map.
- [x] 27 marker liên tiếp, duy nhất, nằm trong ảnh và khớp một-một với element ID trong DD.
- [x] Ảnh chú thích giữ nguyên tỷ lệ 2×; đã xem trực tiếp, số rõ và không che nội dung quan trọng.
- [x] DD có A–F, luồng vào/ra, 5 sự kiện, API #26/#12, trạng thái/lỗi/điều hướng, bảo mật/accessibility, blockers và nguồn truy vết.
- [x] Expected/current behavior và DD/implementation/runtime status được tách biệt.
- [x] Tracker/worklog cập nhật; static audit và scoped `git diff --check` đạt; không chạy tests/runtime.

## Nguồn đã đối chiếu

- `apps/study-client/docs/list_screen.md` — ST-12, F04, API index, G-07.
- `docs/lists/list_api.md` — API #12/#26 và reusable `Resource`.
- `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md`, `AC_02_STUDENT_LEARNING.drawio` — AC-15.
- `apps/study-server/docs/dd/26_lessons_resources/` — Draft và open questions Q-26-01..07.
- `apps/study-server/docs/dd/12_resources_detail/` — API #12 Draft; đối chiếu riêng với current source.
- `apps/study-server/app/api/v1.py`, `app/modules/guest/api_12_resources_detail/`, `tests/modules/guest/api_12_resources_detail/`.
- `infra/postgres/study-server/DB.sql` — candidate `resources` DDL, không phải live schema.
- ST-11 DD, GS-07 DD, `.agents/web-work/study/INDEX.md`, `.agents/web-study/design.md`.

## Re-audit trước khi hoàn thiện DD (2026-11-07)

Phần đầu của plan mô tả baseline lúc lập kế hoạch trước đó. Khi bắt đầu phiên ST-12 này, sáu core artifact đã tồn tại; đã kiểm tra lại từng artifact và source hiện hành trước mọi DD/marker edit.

- **Asset/UI hiện có:** `screen.png` là 1600×1504; SHA-256 ảnh và HTML khớp source hash trong `ST-12_markers.json`. HTML có 14 anchor, toàn bộ `href="#"`, `data-path` là metadata tĩnh; không có form/input, player, request, listener hoặc timer. Screenshot đúng với empty/unavailable fallback và các status/technical claims hard-code. Study Web vẫn không có editable `src`, package manifest hay router; ignored `dist` không có route ST-12.
- **Marker audit trực quan:** Annotated PNG là 3200×3008. Marker map/SVG có 27 số theo thứ tự và 27 label; mỗi `ST12-EL-01…27` có hàng tương ứng trong DD. Đã xem ảnh: số/leader đặt gần nhóm mục tiêu, không che copy hoặc control. Không có element resource item/selection nên không thêm marker.
- **API #26 expected vs current:** Catalog/AC-15 khai báo Student Bearer, `GET /api/v1/lessons/{lesson_id}/resources`, `ApiEnvelope<Lesson>`, status 200/401/403/404/500. `OPEN_QUESTIONS.md` Q-26-01…07 còn mở payload/cardinality/empty, entitlement/publish, visibility, URL/signer, 404/errors và path/schema. Scoped route/module/test search không thấy Student #26. Không thể tạo Resource item hoặc `resource_id` từ declaration `Lesson`.
- **API #12 current source:** Route `GET /api/v1/resources/{resource_id}` được đăng ký trong `app/api/v1.py`; `view.py` gọi validator rồi query metadata, chỉ tra parent khi `lesson_id` khác NULL. Response hiện trả `id/name/type/url/lesson_id`; `url` là giá trị trực tiếp từ `resources.url`, model bỏ field dư `visibility`; route không dùng Bearer/auth, không kiểm tra enrollment/visibility và không gọi signer. ID không hợp lệ/không tìm thấy/parent không đạt gate dùng 404; SQL/mapping failure dùng 500, SQL failure rollback. Test source characterization được đọc, không chạy. API catalog cũng ghi Public/no Bearer và #12 DD vẫn Draft.
- **Stale API #12 DD statement:** `12_resources_detail/00_Cover.md` nói API chưa được xác minh trong runtime/OpenAPI; current route source và focused test source hiện có, gồm OpenAPI-path characterization. Giữ API DD `Draft — Needs Confirmation`, ghi rõ source-vs-DD cover discrepancy ở screen DD; không sửa API DD trong scope màn hình.
- **AC-06 vs resource access:** AC-06 diagram có access decision và Object Storage signed-URL branch cho private resources; API #12 current source không thực thi nhánh này. Catalog #12 public/no Bearer. Đây là security/URL blocker; không xem call #26 hoặc Student route guard là bảo đảm quyền cho #12.
- **Schema evidence:** `infra/postgres/study-server/DB.sql` là legacy BIGINT candidate được #12 query dùng; `resources.lesson_id` nullable và không có `visibility`. Scoped search trong `infra/postgres/02_study_db.sql` không thấy table `resources`; V1-PILOT là mô hình versioned/UUID riêng. Không gộp hai schema hoặc khẳng định live DB.
- **Cross-screen:** ST-11 hiện là static unavailable fallback, không có resource-selection control; GS-07 cũng tham chiếu #12 nhưng route/runtime chưa wire. Inventory yêu cầu #12 chỉ khi có `resource_id` hợp lệ; hiện không có nguồn item/ID hoặc return-context contract.

**Kế hoạch trước khi sửa DD:** Giữ nguyên ảnh nguồn, marker JSON/SVG và annotated PNG nếu static geometry/1:1 checks cuối cùng đạt. Cập nhật DD để phân biệt rõ #12 current source với API #12 DD cover/AC-06 signed URL design; bổ sung DDL family mismatch và blocker access/URL; giữ #26/#12 errors, empty/list, selector, link destination và return context ở trạng thái chưa chốt. Cập nhật ST-12 inventory/global-plan rows và worklog. Không thêm response field, endpoint, auth behavior, timer, URL policy hay resource item. Trạng thái giữ `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.


## Kết quả re-audit tĩnh (2026-11-07)

- 27 marker IDs/labels map 1:1 với 27 element rows; SVG XML parse, image embed byte-for-byte khớp `screen.png`, ảnh chú thích đã được xem; source PNG 1600×1504, annotation 3200×3008.
- DD có headings A–F, 5 event IDs liên tiếp; local Markdown links resolve. HTML có 14 placeholder anchors, không có product event/timer/request, form/input hoặc media control. Source image/HTML hashes giữ nguyên.
- Global inventory/folders 83/83; 82/83 core bundles, chỉ ST-01 còn thiếu. Không chạy application tests, runtime, deployment hoặc live DB check.
- Outcome: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. #26 collection/access contract, #12 direct public URL/access policy, resource item selection/return context và schema/live DB alignment còn mở.
