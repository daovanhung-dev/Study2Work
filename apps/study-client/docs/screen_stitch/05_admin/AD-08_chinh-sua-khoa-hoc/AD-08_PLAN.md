# AD-08 — Kế hoạch Detailed Design

> **Screen ID:** AD-08 · **Tên:** Chỉnh sửa khóa học quản trị · **Đợt/ưu tiên:** W4 / P1<br>
> **Route đề xuất:** `/admin/courses/:courseId/edit` · **AC:** AC-32 · **API:** #74, #75<br>
> **Trạng thái đầu phiên:** inventory `D`; local API #75 route/module/test source exists, API DD remains `Draft — Needs Confirmation`; Study Web `UNWIRED`.

## 1. Phạm vi và nguyên tắc

- Hoàn thiện riêng AD-08 trong phiên này: đối chiếu prototype và API contract/source; lập plan này trước marker/DD; tạo marker map, overlay và annotated image; viết DD A–F; cập nhật inventory, reverse API index, global tracker và worklog. Không xử lý AD-09.
- Giữ nguyên `screen.png` và `code.html`; chỉ thêm plan, DD, marker JSON/SVG và `screen_annotated.png`.
- Dùng numeric `Course.id` từ AD-07 làm `courseId` đề xuất. Không dùng mã học phần trong mockup làm ID.
- Expected behavior lấy từ AC-32, inventory/API catalog và yêu cầu màn hình. Current behavior lấy từ source, executable config/test source và prototype tĩnh. Không trộn hai phía.
- Catalog và AC không định nghĩa body cho #75. Local body/validation/legacy mapping là `DERIVED`, chưa phải contract được duyệt.
- Không thiết kế upload/multipart: local #75 chỉ có metadata `thumbnail_url`, không có upload endpoint trong module; thumbnail constraints/flow trong mockup không có contract.
- Không coi static labels về RBAC, trạng thái API, cache, S3, production readiness, audit/gateway hoặc data integrity là telemetry hay runtime behavior.
- Không đổi API catalog, AC-32, DDL, API implementation, hay live data. Không chạy app tests/runtime; ghi test history từ báo cáo hiện có và đánh dấu không chạy trong phiên.
- Context manifest không wire canonical skill cho UI-only DD; `createDD-markdown` loại trừ boundary này. Không nạp skill không phù hợp.

## 2. Bằng chứng và cách xử lý

| Nhóm | Expected / nguồn | Current / nguồn | Cách ghi trong AD-08 |
|---|---|---|---|
| Route và ID | Inventory đề xuất `/admin/courses/:courseId/edit`; AD-07 chuyển numeric `Course.id`. | Không có Study Web app/router/client; prototype Back-to-detail copy AD-07 nhưng `href=/admin/courses`; Cancel cũng tới `/admin/courses`. | Ghi route là proposed; coi cả hai link là prototype discrepancy; yêu cầu route/return decision. |
| Trình tự dữ liệu | AC-32 và inventory: GET #74 → sửa metadata → PUT #75 → revalidate #74. | Study Web không gọi API. Local #75 tự đọc projection #74 trong transaction và trả updated singleton `Page<Course>`. | Mô tả sequence mục tiêu và nêu rõ revalidation/cache strategy chưa quyết định. |
| Body | Catalog/AC chỉ khai báo `course_id`; không có request body. | Local strict model yêu cầu `title`, `description`, `thumbnail_url`, `price`; extra fields bị từ chối. | Bốn field chỉ là body candidate `DERIVED`, cần owner/API approval. |
| Validation | Chưa có body rules được duyệt. | Local source: signed int64 path; title max 200, giữ whitespace; description/thumbnail nullable; thumbnail không validate URI; price decimal string, scale ≤2, integer digits ≤10, số âm được nhận. | Ghi đúng hiện trạng source, không biến thành UI/product policy. Legacy DDL candidate không chứng minh live schema. |
| Mutation | AC-32 xếp #75 vào nhánh update metadata; #76 riêng cho status. | Local SQL cập nhật `name`, `description`, `thumbnail_url`, `price`, `updated_at`; giữ status/mentor; readback trong cùng Session; commit sau response mapping; rollback khi lỗi. | Ghi current backend behavior; transaction/mapping phụ thuộc API DD draft. |
| Response/schema | Catalog #75 trả `ApiEnvelope<Page<Course>>`; API #74 dùng cùng Course projection. | Local response singleton Page; legacy DDL dùng BIGINT, một DDL V1-PILOT khác dùng UUID/versioned. | Singleton và legacy mapping là `DERIVED`; live schema/deployment unknown. |
| Authorization | AC-32 yêu cầu Admin có course-management permission; catalog ghi Bearer JWT/Admin. | Local guard kiểm tra shared role `ADMIN`; không có check permission riêng. | Ghi permission mapping là `OPEN`; role không tự chứng minh permission. |
| Prototype | Màn hình chỉnh sửa Course metadata. | Tất cả control nhập liệu và Save disabled; links/số liệu/status/preview tĩnh; không có handler/fetch/client. | Tài liệu hóa visible UI nhưng không khẳng định runtime event. Prototype không phải implementation. |

## 3. Marker plan

- Dùng **61 marker** theo thứ tự đọc từ trên xuống, trái sang phải: admin shell/breadcrumb; hero và sync notice; form/preview; diagnostics; data-integrity banner và footer.
- Gom những nhãn hoặc nội dung phụ thuộc chung thành một marker khi chúng tạo thành một element logic (ví dụ title + required cue, label + rebate cue, preview title + summary). Tách các input, actions, status rows, metric cards và footer links khi chúng có vai trò riêng.
- Tọa độ dùng pixel trên `screen.png` (1385×1600); marker circle đặt sát vùng đại diện và tránh phủ nội dung trọng yếu. Xuất overlay SVG ở kích thước ảnh nguồn và `screen_annotated.png` ở 2×.
- Bảng C trong DD phải có đúng một hàng cho mỗi marker #1–#61, cùng tên/nhóm element và event tương ứng.

## 4. Luồng và event cần đặc tả

1. **EV-01 — Route/load:** nhận numeric `courseId`; mục tiêu gọi GET #74 với Bearer JWT; phân biệt 200/401/403/404/500 và lỗi mạng. Hiện không được Study Web thực thi.
2. **EV-02 — Hiển thị form:** chỉ sau GET success, map các field từ Course response; body candidate không có `course_code`, `mentor_id`, status hoặc counters. Không đưa static batch code/metrics vào state.
3. **EV-03 — Edit/change:** mục tiêu quản lý dirty state cho các field được owner duyệt; hiện control disabled. Body/field policy chưa được duyệt, nên chỉ ghi candidate mapping và decision gate.
4. **EV-04 — Save:** mục tiêu PUT #75 với Bearer JWT và body chỉ sau khi contract được duyệt; mô tả local candidate validation và backend error mapping riêng. Không gọi multipart upload. Ghi rõ re-read GET #74 vs dùng response/invalidate cache còn open.
5. **EV-05 — Cancel/back:** mục tiêu quay về AD-07 hoặc AD-06 theo approved route/history. Current anchors đều về `/admin/courses`; route state restoration chưa có nguồn.
6. **EV-06 — Shell/preview/footer controls:** hiện là anchor `#`, no-handler button hoặc static display; không phát sinh API effect. Ghi runtime destination/resource là chưa cấu hình.

## 5. API/source trace cần có trong DD

- API #74: `GET /api/v1/admin/courses/{course_id}`, Bearer JWT/Admin, `course_id:int64`; target load/revalidation. Local source returns one Course in Page; API DD #74 remains Draft. No `course_code`, counters, curriculum, enrollment metrics, or category mapping.
- API #75: `PUT /api/v1/admin/courses/{course_id}`, Bearer JWT/Admin, path `int64`; catalog response `ApiEnvelope<Page<Course>>`, success `DESIGN_RESOURCE_UPDATED`; catalog errors 401/403/404/422/500. Body absent from catalog/AC.
- Local #75 source requires strict JSON candidate `{title:string, description:string|null, thumbnail_url:string|null, price:string}`; body rules and values remain `DERIVED`. API DD #75 is Draft.
- Current local errors: malformed/out-of-range path and body/validation are 422 at #75 path; 401 auth missing/invalid, 403 role denied, 404 missing course, 500 query/readback/projection/commit failure. Avoid assuming frontend copy, retry, timeout, or auto-redirect policy.
- Historical verification report says 27 focused, 113 linked, 872 full Study tests passed with fake DB/session fixtures. This session will not run tests; fake fixtures do not establish live schema/deployment or UI runtime.

## 6. Blockers and completion target

1. Approve #75 body fields, PUT replacement/null semantics, title/thumbnail/price validation and live schema mapping.
2. Decide if and how thumbnail upload works; identify a real endpoint/storage contract before enabling file selection.
3. Resolve AC-32 course-management permission against shared `ADMIN` guard.
4. Confirm response cardinality and whether the client consumes #75 response, refetches #74, or invalidates cache.
5. Approve Study Web route, save/cancel return destination, error/session behavior, and implement the route/client.
6. Remove or source static course code, mentor selector, chapter/enrollment metrics, Active status, multipart/S3 claim, Production Ready/version/audit/data-integrity statements.

Target status after this session: complete the evidence-based design package, but mark **DD BLOCKED** and **IMPLEMENTATION BLOCKED** until the decisions above are resolved. Runtime remains **NOT VERIFIED**.

## 7. Execution and verification order

1. [x] Complete docs preflight; read selected docs worklogs and required context pages.
2. [x] Review inventory, prototype/image, AC-32, API catalog/DD/source/tests, schema candidates and Study Web source boundary; update worklog expected/current trace.
3. [x] Write this plan before creating marker JSON, annotation or DD.
4. [x] Create ordered marker JSON/SVG and 2× annotated PNG; inspect image and move markers away from text where practical.
5. [x] Author A–F DD with 1:1 marker rows, sequenced events, API matrix/errors, state/navigation matrix and explicit blockers.
6. [x] Update AD-08 inventory and API #075 reverse source index; update global tracker/checkpoint.
7. [x] Static audit source hashes/dimensions, marker sequence/uniqueness/bounds and C-table bijection, JSON/XML/links, inventory IDs/folders and core bundle count. Application tests/runtime not run.
8. [x] Finalize worklog; do not process another Screen ID.
