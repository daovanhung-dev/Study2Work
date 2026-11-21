# GS-07 — Kế hoạch chi tiết

> Ngày rà soát: 2026-11-06
>
> Trạng thái: `PLAN COMPLETE; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`
> Phạm vi phiên: chỉ GS-07; không bắt đầu Screen ID khác.

## 0. Kế hoạch re-audit (2026-11-08)

- Chỉ re-audit GS-07; các artifact có sẵn từ phiên 2026-11-06 là đầu vào cần xác minh lại theo source hiện tại.
- Đọc lại expected behavior tại `list_screen.md` row GS-07, F02/F04/G-07/API #12 và AC-06; giữ `resourceId` entry từ GS-06/ST-12 và return/error routing tới GS-06/ST-12/SH-06 như các quyết định riêng cần nguồn.
- Re-trace API #12 từ route composition qua path validation, SQL, response model, business code/error và test source; đối chiếu catalog/API DD và cả hai DDL artifacts. Chỉ đọc test, không chạy app tests; không suy luận live schema/deployment.
- Kiểm tra lại Study Web tree/router/package, prototype DOM/script/anchors, Study design target và các claim về auth, preview, URL, MIME, signer, expiry, zoom/fullscreen/download.
- Kiểm tra source PNG/HTML hash/dimensions; xem trực tiếp source và annotated image; đối chiếu marker JSON, SVG, annotated canvas và 1:1 map với element rows trong DD.
- Audit lại A–G, từng event input/process/output/error, state matrix, relative links, whitespace và scoped `git diff --check`; cập nhật DD, inventory, tracker và worklog chỉ theo bằng chứng.
- Giữ status riêng: `DD BLOCKED` nếu contract/decision chưa đủ, `IMPLEMENTATION BLOCKED` khi source/wiring/policy còn thiếu, `RUNTIME NOT VERIFIED` nếu không có deployed end-to-end evidence.

### Acceptance checklist của re-audit

- [x] Kế hoạch re-audit được cập nhật trước khi sửa DD, marker/annotation hoặc shared tracker.
- [x] Current source/API/test/DDL và expected AC/catalog/API DD được xác minh lại; test không chạy và runtime không tuyên bố.
- [x] Original assets giữ nguyên; ảnh source/annotation được xem lại; marker/JSON/SVG/DD mapping đạt.
- [x] Event/state/navigation/security/accessibility gaps và mọi discrepancy tiếp tục được ghi rõ, không điền bằng giả định.
- [x] Inventory/tracker/worklog cập nhật; static checks pass; GS-08 để phiên riêng.

### Bằng chứng recheck ghi nhận trước khi sửa DD

- API #12 route is composed in `apps/study-server/app/api/v1.py`; it has no Authorization dependency. Current validator accepts only positive signed-int64 IDs and maps invalid values to 404 before DB. Query reads `id`, `lesson_id`, `name`, `resource_type AS type`, `url`; parent lesson/course check runs only when `lesson_id` is non-null and requires non-DELETED lesson plus PUBLISHED course. Current model returns `id/name/type/url/lesson_id`, permits nullable URL/lesson ID and ignores extra fields. Success is 200 `DESIGN_RESOURCE_RETRIEVED`; query/mapping errors map to safe 500; current source has no visibility/enrollment/access check, signer or expiry.
- API catalog #12 is public/no Bearer and declares 200/404/500 `ApiEnvelope<Resource>`. API DD remains Draft and its `RUNTIME_STATUS: ... DECLARED_NOT_RUNNABLE` line is stale relative to the current composed route/test source; neither source nor the temporary-branch report proves production/live runtime. AC-06 separately specifies access decision, 403/404 and Object Storage signing for private resources.
- Test source covers direct URL/no-auth/visibility omission, null lesson path, invalid/missing resource and parent 404, SQL/mapping 500, bound query and OpenAPI int64 path. Tests were read only, not run. Legacy `DB.sql` has `resources` with nullable `lesson_id` and `url NOT NULL`, no `visibility`; V1-PILOT `02_study_db.sql` has no generic `resources` table. Live schema remains unverified.
- Current Study Web tree has docs, ignored `dist`, `node_modules` and build metadata; editable `src`, package manifest and router are absent. Prototype uses remote Google Fonts/Tailwind CDN, Plus Jakarta Sans, cobalt `#004ac6/#2563eb`, 1440px content width, and hides primary nav below `md` without a mobile menu; Study guide expects Inter/system, no remote font, ocean tokens and ~1120px content. Contrast/reflow/accessibility were not measured.
- At the start of re-audit, marker JSON placed GS07-EL-08, -09 and -10 at the same right-gutter center `(3308, 940)`, so three numbered controls overlapped. The DD also lacked consistent trigger/precondition/process/output/error fields for several events, and EV-03 repeated its `Input` line. These are recorded as initial findings; the defects were corrected below.

### Kết quả sau chỉnh sửa và kiểm tra

- Tách marker #8, #9, #10 trên gutter phải trong JSON/SVG; render lại `screen_annotated.png` từ source không sửa. Kiểm tra cuối xác nhận 26 marker tuần tự/duy nhất/trong bounds; SVG có 26 circle/label/leader và nhúng đúng bytes của `screen.png`; marker map khớp 26 element rows.
- Chuẩn hóa đặc tả đủ 8 event theo trigger/type, precondition, input, processing, output và exception. Không nâng các state/code mock thành API contract.
- Ghi rõ API #12/AC-06, schema, Study Web wiring và design/accessibility discrepancies là blocker hiện hành; không chạy application test hoặc tuyên bố runtime.

## 1. Phạm vi và nguồn

- Screen ID/tên: **GS-07 — Xem/tải tài nguyên (Page)**; actor dự kiến theo AC-06 là Guest hoặc user có quyền trên resource; route đề xuất `/resources/:resourceId`.
- Inventory: API #12 `GET /api/v1/resources/{resource_id}`; preview metadata/media khi hỗ trợ; fallback download khi URL hợp lệ và được phép; link GS-06; states `loading/ready/403-unclear/404/link-expired`.
- Entry/handoff dự kiến: `resourceId` từ GS-06 resource selection hoặc ST-12 lesson-resource selection. Return route trong prototype ghi GS-06; ST-12 return/lesson context chưa có hợp đồng. SH-06 là generic 404 prototype nhưng hiện được thiết kế chủ yếu cho API #08; cách áp dụng cho #12 phải được chốt.
- AC-06: Guest; resource phải public hoặc user có quyền; postcondition là resource/file URL hợp lệ được mở/tải. AC diagram mô tả access decision, 403/404 và signed URL qua Object Storage cho private resource.
- Original `screen.png`: PNG hợp lệ 1588×1600; SHA-256 `11068f47467e5f5f47a074c833912a17816ce3cb4f95e34b59e5b2163b56259b`. Ảnh là static gated viewer/hand-off prototype; không có metadata resource thật hoặc loaded preview. Giữ nguyên.
- `code.html`: SHA-256 `e6550d5ba83fa27acc9f704b7599609ded9ab549175eaaadb4d03885e8bb058b`; tĩnh, không fetch/XHR/Axios. Có JS local `switchHandOffState(state)` đổi class/title/description/code sample của 6 state tabs; không gọi API, thay trạng thái quyền thật, bật download, hoặc render preview. Gated initial copy khác code sample sau khi click tab `gated`.
- Tạo 26 marker cho component groups, 3 disabled zoom controls và 6 state tabs riêng; map một-một với các row trong DD. Dùng side gutters để tránh che source content. Giữ `screen.png` và `code.html`; không cần render ảnh thay thế.

## 2. Expected/current và API #12 evidence

| Hạng mục | Expected/design source | Current evidence | Tác động |
|---|---|---|---|
| Route/client | `/resources/:resourceId`, fetch metadata lúc mở; return GS-06; có thể được gọi từ ST-12. | Study Web có docs/assets nhưng không có app source/router/API client; HTML để nguyên `:resourceId`, anchors `href="#"`; return link không có route. | `UNWIRED`; route param hydration, origin/back state và runtime navigation chưa xác minh. |
| API #12 contract | Catalog: public GET `/api/v1/resources/{resource_id}`, `resource_id:int64`, `ApiEnvelope<Resource>`, no body/query/Bearer; 200/404/500. | Route được register trong `apps/study-server/app/api/v1.py`, không có auth dependency; current view/model/query source và test files tồn tại. | `SOURCE_BACKED` theo source hiện tại; không chứng minh live deployment/runtime. |
| Response | Contract/DD Resource có `id`, `name`, `type`, `url`, `visibility`, `lesson_id` với `data.url` cho direct hoặc signed URL. | Current query trả `id`, `name`, `resource_type AS type`, `url`, `lesson_id`; response model bỏ extra `visibility`; `url` direct từ `resources.url`, có thể `null` theo model. | Không có `signed_url`, `expires_in`, visibility hoặc preview-capability field trong current source. |
| Parent/access gate | AC-06 cho public hoặc user đã có quyền; thiếu quyền → 403; private file cần signer. | Current view kiểm tra parent course PUBLISHED chỉ khi `lesson_id` khác null; resource không có lesson vẫn trả 200. Không kiểm tra visibility/enrollment/auth và không gọi signer. | Security/access policy conflict; không được kết luận 200 đồng nghĩa access private đã được xác thực. |
| Error/status | Inventory có 403-unclear, 404, expired-link; prototype thêm 423/501. | Current API source/catalog có 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`; không 401/403/410/423/501. | Các code/status trong state simulator là design-only. 500/network state còn thiếu trong mock. |
| Signed URL/auth | Prototype code card gửi `Authorization: Bearer <access_token>` và JS mô tả `signed_url` + `expires_in:3600`. | Catalog/current route public/no Bearer; #12 trả `data.url` direct; không có expiry/signer implementation. | Ghi discrepancy với AC-06/private-access và không biến code sample thành executable API contract. |
| Viewer controls | Preview PDF/media nếu hỗ trợ; fallback download khi được phép. | HTML không có iframe/video/object/embed; zoom/fullscreen/download controls disabled; “200 Ready” chỉ đổi text, không enable controls. `resource_type` enum/capability chưa được xác nhận. | Chưa có renderer mapping, MIME/allowlist, URL origin policy hoặc download behavior. |

### Current API #12 source trace

1. Route `GET /api/v1/resources/{resource_id}` nhận raw string path và gọi `get_resource_detail`; route không nhận `Authorization`/role dependency.
2. `validate_resource_id` parse integer dương signed-int64; malformed, `<=0`, overflow → HTTP 404 `DESIGN_RESOURCE_NOT_FOUND` trước DB.
3. `RESOURCE_BY_ID` query đọc `resources.id`, `lesson_id`, `name`, `resource_type AS type`, `url` theo bind `resource_id`, `LIMIT 1`.
4. Không có resource → 404. Nếu `lesson_id` khác null, `PUBLISHED_PARENT_COURSE` cần lesson không `DELETED` và parent course `PUBLISHED`; không có row → 404. `lesson_id=null` thì bỏ parent lookup.
5. `ResourceDetail` yêu cầu `id:int`, `name:string`, `type:string`; cho phép `url:string|null`, `lesson_id:int|null`; extra như `visibility` bị ignore.
6. Success trả HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, `data={id,name,type,url,lesson_id}`. SQL/mapping exception → HTTP 500 `DESIGN_INTERNAL_ERROR`, rollback khi SQLAlchemy error. Không có external storage side effect.
7. Test source xác nhận trực tiếp URL/no auth/visibility, null lesson success, invalid/missing/unpublished-parent 404, DB/mapping errors 500, SQL bỏ visibility và OpenAPI path int64. Đã đọc, **chưa chạy**; fake-session tests không xác minh live DB/deployment.

### Prototype behavior không được coi là API behavior

- `switchHandOffState('loading'|'gated'|'ready'|'403'|'404'|'expired')` chỉ đổi tab style và `detail-title`, `detail-desc`, `detail-code` bằng text hard-coded.
- Ready simulator nêu PDF/media preview, bật download, `signed_url` và `expires_in:3600`; handler không cập nhật disabled control hoặc tạo viewer/link/request.
- 403 code `AUTH_RESOURCE_UNAUTHORIZED`, 404 code `RESOURCE_NOT_FOUND`, 410/401 expired, 423 Locked và 501 đều không khớp current #12 contract/source. Initial screenshot còn ghi 423/501, trong khi click `gated` đổi code thành 423 + DESIGN_ONLY.
- API card thiếu prefix `/api/v1`, dùng host mẫu `api.study2work.edu.vn` và yêu cầu Bearer; không được dùng như config/contract.

## 3. Trace nguồn trước khi authoring

- Inventory/flows: `apps/study-client/docs/list_screen.md` GS-07, F02, F04, G-07, API #12; liên kết GS-06, ST-12, SH-06.
- Activity/expected rule: `apps/study-server/docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio` AC-06.
- UI assets: `screen.png`, `code.html`; HTML controls/anchors/script được parse tĩnh; image original được xem.
- API catalog/DD: `docs/lists/list_api.md`; `apps/study-server/docs/dd/12_resources_detail/{02_Overview,03_Request,04_Response,05_Data_Mapping,06_Error,07_table}.md`.
- Current API chain/tests: `apps/study-server/app/api/v1.py`; `app/modules/guest/api_12_resources_detail/{view,query,validate,models}.py`; `tests/modules/guest/api_12_resources_detail/test_resources_detail.py` (read only).
- Database evidence: `.agents/server-study/database.md`, `infra/postgres/study-server/DB.sql`, `infra/postgres/02_study_db.sql`; checked-in artifacts không chứng minh live schema.
- Cross-screen: GS-06 DD/plan/worklog; ST-12/API #26 inventory row; SH-06 DD 404 scope. Study Web remains `UNWIRED`; intended target `.agents/web-study/design.md`.
- Skill registry: `.agents/skills/INDEX.md` và `.agents/context-manifest.json` exclude `web-ui-only-dd` from `createDD-markdown`; không có canonical skill cho UI-only DD, không load API DD skill.

## 4. Planned output and acceptance

- Keep `screen.png` and `code.html` byte-identical.
- Create 26 ordered unique markers with exact DD element-ID mapping, SVG overlay and annotated image at scale 2 with side gutters.
- Create `GS-07.md` with overview, current/expected flow, every element, per-control event procedures, API #12 details/errors, simulator/API discrepancies, states, navigation/origin handoff, acceptance and sources.
- Update `dd_screens/PLAN.md` progress from 13/83 to 14/83 and set GS-08 as next; keep `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` separate.
- Create current-session worklog with exact-type preflight review and verification. Do not run backend tests or claim runtime verification.

### Acceptance checklist

- [x] Plan exists before marker/annotated/DD authoring.
- [x] Source PNG/HTML hashes unchanged; source image valid and complete.
- [x] 26 markers are ordered, unique, in bounds and map one-to-one to DD rows.
- [x] Disabled zoom/download, active local state tabs, back/breadcrumb/header/footer anchors and their actual static behavior are documented.
- [x] API #12 endpoint/auth/path/response/current code/errors are traced to source and catalog; no signed URL/403/410/423/501 mock is promoted as runtime behavior.
- [x] `url` direct/source semantics, nullable model, parent check condition, missing visibility and DB/live-schema boundary are explicit.
- [x] GS-06/ST-12 entry and return route semantics; SH-06 404 applicability; preview MIME/type policy and storage/permission gates are identified without invented behavior.
- [x] Tracker and worklog are updated; static asset/marker audit, visual review and `git diff --check` pass.

## 5. Initial classification

- `DD BLOCKED`: API #12 current public direct-URL response lacks AC-06 resource authorization/signer policy; mock states/codes conflict with the API; preview-capability and UI routing/origin state are unresolved.
- `IMPLEMENTATION BLOCKED`: storage/access policy, approved response/link semantics, viewer type allowlist/preview, status handling and Study Web wiring are not available.
- `RUNTIME NOT VERIFIED`: static HTML’s local state simulator and Study Server source/test files do not prove deployed screen or end-to-end operation.
