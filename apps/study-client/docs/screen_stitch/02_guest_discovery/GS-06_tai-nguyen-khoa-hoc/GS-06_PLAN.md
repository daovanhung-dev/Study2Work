# GS-06 — Kế hoạch chi tiết

> Kế hoạch ban đầu: 2026-11-06; rà soát nguồn và tài sản: 2026-11-07  
> Trạng thái: `RE-AUDIT PLAN COMPLETE; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`  
> Phạm vi phiên: chỉ GS-06; không bắt đầu GS-07.

## 0. Kế hoạch rà soát lại (2026-11-07; hoàn tất static audit 2026-11-08)

Thứ tự công việc trong phiên này:

1. Đọc lại mục tiêu 83 màn hình, inventory GS-06, AC-06, API catalog/DD #11/#12 và nguồn Study Web/Study Server hiện tại; phân biệt expected với current behavior.
2. Đối chiếu route/module/query/validator/model/test của #12 và tìm riêng route/module/test của #11; chỉ đọc test source, không chạy application tests.
3. So sánh schema candidate legacy với V1-PILOT; không suy luận rằng artifact DDL hay test fake-session chứng minh production/live schema.
4. Kiểm tra lại `screen.png`, `code.html`, `screen_annotated.png`, marker JSON/SVG, mapping marker↔element và tất cả event của DD; giữ nguyên PNG/HTML nguồn.
5. Cập nhật DD và marker/ảnh chỉ khi audit phát hiện thiếu hoặc sai; nếu mapping/ảnh hiện hữu hợp lệ thì giữ nguyên.
6. Cập nhật trạng thái GS-06 ở `list_screen.md` và bảng/checkpoint trong `dd_screens/PLAN.md`; hoàn thiện worklog, chạy kiểm tra tĩnh và context validator nếu có thay đổi registered context.

### Bằng chứng hiện tại được xác nhận trước khi sửa DD/marker/tracker

- API #11 vẫn là declaration/Draft: catalog khai báo public GET với `ApiEnvelope<Resource>` đơn, không query/body; tìm kiếm current Study Server `app/` và `tests/` không thấy route/module/test #11. Cardinality, list-empty, thứ tự/pagination và `visibility` chưa có nguồn runtime.
- API #12 có route/module/query/validator/model trong current Study Server và route được compose ở `/api/v1/resources/{resource_id}`. Route không nhận/kiểm tra Authorization; validator chỉ chấp nhận positive signed-int64 và map path sai thành 404; view đọc `resources.url` trực tiếp, conditional gate parent lesson/course chỉ chạy khi `lesson_id` khác null, và không gọi storage signer hoặc kiểm tra enrollment/visibility. Test source xác nhận các nhánh này nhưng không được chạy trong phiên.
- AC-06 yêu cầu resource public hoặc có quyền truy cập, có nhánh 403, và signed URL cho object private; API catalog #11/#12 chỉ public và 404/500. Đây là `DISCREPANCY`, chưa được phép hợp nhất bằng suy đoán.
- Schema candidate legacy `infra/postgres/study-server/DB.sql` khai báo `resources(id, lesson_id, name, resource_type, url, created_at)` và không có `visibility`; V1-PILOT `infra/postgres/02_study_db.sql` hiện không khai báo bảng `resources`. Live production schema/deployment không được xác minh.
- `apps/study-client/` hiện không có editable app source, package manifest hoặc screen router; chỉ có docs/assets, ignored `dist/` và build metadata. Study Web vẫn `UNWIRED`; asset tĩnh không chứng minh route/runtime.
- PNG gốc hiện là 1486×1600, SHA-256 `b90795438d5369466bb101e8f6730265667f8ecc45c0d047d66495410da87dcd`; HTML gốc SHA-256 `6843e2cc0f01a24e1db8100b8fec49d88e1f3fe39859b102bb9828d4905a8c31`. Giữ nguyên cả hai.
- Trước khi chỉnh DD/marker/tracker, thư mục đã có 23 markers, annotation và DD từ phiên 2026-11-06. Phiên này sẽ xác minh lại một-một, bounds, SVG/image consistency, event completeness và các liên kết thay vì mặc định chúng hợp lệ.

### Definition of completion riêng cho lần rà soát này

- Ghi đầy đủ 23 element và các tương tác hiện có; mỗi event có loại/trigger, precondition, input, processing, output và error/exception, tách rõ hành vi HTML tĩnh với luồng expected chưa runnable.
- Ghi API #11 `DECLARED_NOT_RUNNABLE`, #12 `SOURCE-BACKED LOCALLY`, Draft status, #12 direct-URL behavior, schema discrepancy, AC-06 conflict, `UNWIRED` Study Web và live-schema limitation.
- Chỉ giữ `DD BLOCKED`/`IMPLEMENTATION BLOCKED`/`RUNTIME NOT VERIFIED` khi các blockers còn đúng; không nâng `DD READY` hay `RUNTIME VERIFIED` bằng việc chỉ có file/test source.
- Xác minh `screen.png`/`code.html` hashes, ảnh chú thích, marker IDs/tọa độ/mapping, local links, tracker IDs/folders và whitespace.

## 1. Phạm vi và nguồn

- Screen ID/tên: **GS-06 — Tài nguyên khóa học (Tab)**; actor dự kiến `Guest`; route đề xuất `/courses/:courseId?tab=resources`.
- Expected từ `apps/study-client/docs/list_screen.md`: AC-06; API #11 lấy resource theo `courseId`, người dùng chọn `resource_id`, API #12 được gọi trước khi mở URL; không suy diễn visibility; liên kết GS-03, GS-07 và ST-12. Inventory kỳ vọng `empty/list/forbidden/expired-link`.
- AC-06 diagram kỳ vọng actor Guest, tiền điều kiện “resource public hoặc user có quyền”, gọi #11, chọn một resource, gọi #12, kiểm tra quyền, rồi mở/tải URL; có nhánh 403/404 và Object Storage signer cho private object. Đây mâu thuẫn với public-only API catalog và current #12 source.
- Original `screen.png`: PNG hợp lệ 1486×1600; SHA-256 `b90795438d5369466bb101e8f6730265667f8ecc45c0d047d66495410da87dcd`. Ảnh thể hiện hand-off/gated empty state, metadata hợp đồng và state inventory; không có danh sách resource thật. Giữ nguyên ảnh và `code.html`; không cần render lại.
- `code.html` là prototype tĩnh có nội dung mẫu (tên course, mã học phần, đơn vị hướng dẫn), header/tab/footer và hướng dẫn tích hợp. Không có data binding, request, router hoặc handler được xác minh. `href="#"` không xác nhận destination.
- Annotation dự kiến dùng 23 marker cho các component/nhóm hiển thị; từng control có thể thao tác có marker riêng, còn label/subfield trong một card được mô tả dưới marker của card đó. Tạo `GS-06_markers.json`, overlay riêng và `screen_annotated.png`; không ghi đè ảnh gốc.

## 2. Expected/current và API evidence

| Hạng mục | Expected/design source | Current evidence | Tác động |
|---|---|---|---|
| Route và UI | Guest mở tab tài nguyên của cùng `courseId`; chọn item sang GS-07; ST-12 cũng tham chiếu resource flow. | Study Web hiện `UNWIRED`; chỉ có asset tĩnh, không có route/client source để xác minh. | Route là đề xuất; direct entry, back behavior, tab state, auth/session và cache chưa được xác nhận. |
| API #11 | Public `GET /api/v1/courses/{course_id}/resources`; catalog/DD khai báo `ApiEnvelope<Resource>`, không query/pagination. | Không có route, module, query hay test tương ứng trong Study Server `app/` và `tests/`; chỉ có catalog và DD. | `DECLARED_NOT_RUNNABLE`; `Resource` singleton mâu thuẫn với tên/list relationship 1:N. Không tự đổi sang array/Page hoặc dùng `{ items, total }` từ HTML. |
| API #11 fields/access | Contract draft nêu `id`, `name`, `type`, `url`, `visibility`, `lesson_id`; contract ghi Public/PUBLISHED. | Checked-in legacy DDL `resources` có `id`, `lesson_id`, `name`, `resource_type`, `url`, `created_at`; không có `visibility`. Live schema chưa xác minh. | Visibility và response shape chưa đủ nguồn để quyết định list/render/access. |
| API #12 declaration | Public `GET /api/v1/resources/{resource_id}`, `ApiEnvelope<Resource>`, catalog 200/404/500. | Route/view/query/validator/model tồn tại và được register trong `app/api/v1.py`; không có auth dependency ở route. View trả `id/name/type/url/lesson_id`, dùng direct `url`, bỏ field extra như `visibility`. | API #12 `SOURCE_BACKED` ở source hiện tại; không đồng nghĩa policy private/signed URL của AC-06 đã chạy. |
| API #12 parent check | AC-06 đòi access decision; API DD mô tả parent course PUBLISHED và signer cho private resource như derived/TBD. | View kiểm tra parent PUBLISHED nếu resource có `lesson_id`; `lesson_id=null` vẫn trả success, không lookup parent. Không gọi signer hay kiểm tra enrollment/visibility. Lỗi path/resource/unpublished là 404; query/mapping lỗi là 500. | Public direct URL + thiếu resource-level permission là security blocker; không tự bật open/download. |
| Error/state contract | AC-06/HTML nêu 403 forbidden và 410 expired signed link; inventory yêu cầu empty/list/forbidden/expired-link. | Catalog và #12 current source chỉ có 404/500; không có signed URL hoặc TTL/410. #11 chưa runnable. | 403/410 chỉ là expected design states cần contract; không mô tả như response hiện có. Tách empty thật khỏi integration/contract block. |
| Static visual | HTML yêu cầu list chỉ xuất hiện khi API trả collection; nút tải đang disabled; UI ghi không tạo dữ liệu giả. | Screenshot thể hiện gated/empty hand-off, 4 state cards, hai API reference cards, 2 button-like controls và footer. Không có item/card resource mẫu. | Chỉ mô tả các element nhìn thấy. Nội dung tên course, mã FE-PRO-802, badge “mock data”, URL route và tiêu chuẩn v1 là nội dung prototype, không phải API data/runtime. |

### API #11/#12 boundary giữ nguyên

- API #11 request design: `GET /api/v1/courses/{course_id}/resources`, path `course_id:int64`, public/no Bearer theo catalog, không body/query; response `ApiEnvelope<Resource>`, statuses 200/404/500 theo catalog. API chưa có current backend implementation.
- API #12 request: `GET /api/v1/resources/{resource_id}`, path `resource_id:int64`, public/no Bearer theo catalog, không body/query. Current validator chỉ nhận positive int64; malformed/non-positive/out-of-range path thành 404 trước DB.
- Current #12 success envelope có `businessCode=DESIGN_RESOURCE_RETRIEVED`, `message=Resource metadata retrieved`, `data={id,name,type,url,lesson_id}`, `meta={}`, `traceId`. `url` là direct `resources.url`; không thêm `signed_url` hoặc expiry.
- Current #12 `ResourceDetail` loại `visibility` (extra ignored). Test source kiểm tra direct URL, bỏ visibility và không yêu cầu auth; test source chỉ là bằng chứng được đọc, chưa chạy.
- AC-06, list_api, API DD và source khác nhau về visibility/access, status 403 và storage signing. Giữ `DISCREPANCY`; không tự hợp nhất bằng giả định.

## 3. Trace nguồn trước khi authoring

- Inventory/F02/G-07/API index: `apps/study-client/docs/list_screen.md` (GS-06 row, F02, G-07, API #11/#12 rows).
- Activity flow: `apps/study-server/docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio` (AC-06 nodes `n1`–`n10`, access decision and error edge).
- Current design assets: `screen.png`, `code.html` in this directory. Checksum the original again after output creation.
- API #11 declaration: `docs/lists/list_api.md`; `apps/study-server/docs/dd/11_courses_resources/` overview/request/response/data mapping/error; search current app and tests for absent route/module.
- API #12 current chain: `apps/study-server/app/api/v1.py` route; `app/modules/guest/api_12_resources_detail/{view,query,validate,models}.py`; `tests/modules/guest/api_12_resources_detail/test_resources_detail.py`; API DD `docs/dd/12_resources_detail/`.
- DDL candidate: `infra/postgres/study-server/DB.sql` courses/lessons/resources; DDL is checked-in design/source, not live schema.
- Study Web status and design target: `.agents/web-work/study/` and `.agents/web-study/design.md`; current Study Web remains `UNWIRED`.

## 4. Planned output and acceptance

- Keep `screen.png` and `code.html` byte-identical.
- Create `GS-06_markers.json`, a vector overlay and `screen_annotated.png`; keep markers ordered and unique, align them to visible grouped elements and avoid covering primary copy or controls.
- Create `GS-06.md` with overview, expected/current flow, element table, sequential event procedures, #11/#12 request/response/status trace, state matrix, navigation/data handoff, acceptance checklist, source links and explicit blockers.
- Update `list_screen.md` and `dd_screens/PLAN.md` with API #12 source status, GS-06 blockers and a dated checkpoint. Current file inventory has all six core artifacts for 83/83 IDs; this is file-presence evidence only, not proof that all 83 DDs passed quality review. Keep GS-07 as the next separate-session screen and keep `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` separate.
- Create this session worklog with prior-worklog review, source trace, discrepancy register and static audit. Read but do not run backend tests or claim runtime verification.

### Acceptance checklist

- [x] Plan existed before annotation/DD authoring and was updated before this re-audit's DD/tracker edits.
- [x] Original PNG/HTML hashes unchanged; original image is valid and the annotated image was visually inspected.
- [x] Every marker is unique, ordered, within canvas bounds and maps 1:1 to one DD element row.
- [x] All visible static controls/cards/states are documented; each actionable element and conditional tooltip state has a sequential event or explicit disabled/unknown behavior, with type/trigger/precondition/input/process/output/error.
- [x] #11 absence, singleton/list discrepancy and missing visibility source are explicit.
- [x] #12 current direct URL/public behavior, conditional parent check, response fields and errors are source-backed; API DD's stale `DECLARED_NOT_RUNNABLE` note and temporary-branch report are separated from production verification; tests are not described as run.
- [x] AC-06 vs API catalog/backend mismatch and unsupported 403/410/signer claims remain explicit blockers.
- [x] Overall tracker counts/status and next screen are updated; static diff and artifact checks pass.

## 5. Initial classification

- `DD BLOCKED`: #11 is not runnable and cardinality/visibility contract is unresolved; AC-06's authorization and signer flow is not implemented by current #12.
- `IMPLEMENTATION BLOCKED`: security/access decision, collection schema, 403/410 and signed-URL behavior, route/client wiring, loaded/list/error state designs remain unapproved or unwired.
- `RUNTIME NOT VERIFIED`: static prototype and source/test files do not establish deployed browser/API behavior.
