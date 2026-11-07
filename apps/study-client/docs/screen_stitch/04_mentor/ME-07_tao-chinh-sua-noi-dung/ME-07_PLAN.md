# ME-07 — Kế hoạch Detailed Design: Tạo/chỉnh sửa nội dung

> **Plan status:** COMPLETE — source trace, annotation, 31-marker map, DD and static audit are complete for this Screen ID.
> **Screen status dự kiến:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.

## 1. Phạm vi và đầu vào

- Phiên này chỉ xử lý **ME-07**; không soạn tài liệu cho ME-06 hoặc ME-08. Chỉ mô tả handoff giữa các màn hình này.
- Phân loại: `primary_task_type: docs`; `secondary_task_types: [test]`; `project_scopes: [web-work, server-study]`; cross-scope dependency: route `courseId/contentId` ↔ #49 Content[] ↔ #50/#51 mutations ↔ #49 refresh.
- Expected theo [`list_screen.md` ME-07](../../../list_screen.md#L167): route đề xuất `/mentor/courses/:courseId/content/:contentId?`; actor Mentor; editor theo `content_type/payload`; quản lý dirty state; GET #49 tìm item (edit), POST #50 (create) hoặc PUT #51 (update), sau đó refresh #49; links ME-06/ME-08; states `draft/dirty/validating/saving/conflict`.
- Goal objective `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md` yêu cầu plan trước, ảnh chú thích + marker map + source-traced DD, tracker/worklog update, một Screen ID/phiên và tách `DD READY`, `IMPLEMENTATION BLOCKED`, `RUNTIME VERIFIED`.
- `screen.png`: 1600×1400, SHA-256 `e952ed4554505d34c087a4f0812cb06f71839ea193ddb3c84f998118e4349af3`; đã xem toàn ảnh; giữ nguyên.
- `code.html`: SHA-256 `98c9eba51f9b827452d5f46f5e440945decc85c3a0b6d80017c34eccbbbe7ead`; static populated editor shell. 14 anchors (đều `href="#"`), 2 inputs, 1 select, 1 disabled button, 1 image, không form/custom event/API binding.
- Study Web context là `UNWIRED`; không có editable client source/package/router. UI-only DD không có canonical skill trong registry, vì `createDD-markdown` dành cho Web/API DD.

## 2. Source trace và các discrepancy đã xác nhận

### Expected workflow

1. Vào route có `courseId` và optional `contentId`. Có `contentId` thì edit; không có thì create. Đây là route proposal của inventory, chưa được Study Web wire.
2. Với edit, dùng Content của course từ GET #49 để tìm node ID. #49 là collection phẳng, không có endpoint detail riêng/version field. Với create, cần `courseId` từ ME-06; nhu cầu GET #49 cho create mode và nguồn permissions cần được chốt.
3. Khi form được duyệt và hợp lệ, create gọi POST #50; edit gọi PUT #51.
4. Sau thành công, inventory yêu cầu refresh #49 và quay lại ME-06; điểm đến/cache behavior hiện chưa có client source.

### Current #49/#50/#51 behavior

- #49 route `/api/v1/mentor/courses/{course_id}/content` → `get_course_contents`: auth role MENTOR trước DB; parse signed int64; direct owner `courses.mentor_id`; đọc `contents` active; trả 200 `Content[]` phẳng gồm `id/course_id/content_type/title/payload/status/parent_id/order`. `data:[]` hợp lệ; malformed/missing course → 404, wrong owner → 403, SQL/mapping/tree integrity → safe 500. Không có version selector.
- #50 `POST /api/v1/mentor/content`: strict body `{course_id:int64, content_type:string, title:string, payload:object}`; không nhận `parent_id` hoặc `order`; kiểm tra MENTOR + direct owner; tạo root (`parent_id=NULL`) với `order` tự cấp trong root siblings (đầu tiên là 0), status `PENDING_REVIEW`; success 201 `DESIGN_RESOURCE_CREATED` + Content. Course missing/non-owner đều hiện trả 403; body validation 422; DB/mapping 500.
- #51 `PUT /api/v1/mentor/content/{content_id}`: route có int64 path; current strict body `{content_type:string,title:string,payload:object}` nhưng catalog chỉ mô tả path. API DD ghi body/full replacement/version/status là `DERIVED`, chưa approved. Handler khóa Content+Course, direct-owner; snapshot toàn trạng thái trước sửa vào `content_versions`; thay ba body fields và set current status `PENDING_REVIEW`; giữ `course_id/parent_id/order`; commit rồi trả 200 `DESIGN_RESOURCE_UPDATED` + Content. Malformed/missing content → 404; wrong owner → 403; body 422; SQL/snapshot/commit/mapping failure 500. Response không có version token.
- API #50/#51 route/module/focused test source tồn tại local; test source được kiểm tra, không chạy. API DD #50/#51 Draft; DDL/migrations 006/007 checked-in, live schema/deployment chưa xác minh.

### Mockup ↔ API gaps

- Select có `theory/reading/practice`; API `content_type` là open string và chưa có enum/schema mapping. Không coi các giá trị UI là approved.
- Input `sort_order` ghi “số nguyên dương”/`min=1`; #50 tự cấp root order bắt đầu 0; #51 không nhận order và giữ nguyên order. Không endpoint hiện tại để gửi input này.
- Vùng editor là placeholder “đang chờ kết nối giao thức”; không có input nào tạo payload JSON. #50/#51 đều yêu cầu `payload` object nhưng subtype/schema chưa có.
- “Lưu bản nháp” đang disabled trong HTML. #50/#51 hiện gán `PENDING_REVIEW`; nhãn “bản nháp” và workflow review chưa được owner duyệt.
- Screen có moderation mode/security rule/session status/progress and image, nhưng #49–#51 không trả các dữ liệu này. Không phản ánh permission/progress như server state từ mockup.
- API #51 body current code differs from path-only catalog; course assignment wording AC-22 khác direct-owner guard; `content_versions` history không đồng nghĩa UI có current-version selector/conflict token.
- `.agents/web-study/design.md` là intended visual/accessibility target: no remote font imports, responsive content width ~1120px and keyboard-visible states. Mockup HTML uses remote Plus Jakarta Sans, width 1440px and no wired focus/event states; keep as design discrepancy, do not treat it as runtime.

## 3. Kế hoạch artifact và marker inventory

1. Kế hoạch này được ghi trước JSON/SVG marker map, `screen_annotated.png` và `ME-07.md`.
2. Tạo 31 markers covering top shell, route/breadcrumb context, form controls, disabled/editor/security states, session panel, image and footer. Keep source pixels (1600×1400); output annotated image at scale 2 (3200×2800).
3. Marker coordinates target whitespace/component edges to avoid obscuring labels and controls; after rendering, inspect visually and adjust any collision.
4. DD must have exactly 31 corresponding element rows, and event IDs in order; each current/expected claim points to inventory/AC/source or is marked open.
5. Update global ME-07 row, project checkpoint count, and this session worklog. Do not modify another Screen ID.

| # | Element |
|---:|---|
| 1–5 | Brand, primary navigation, notification, Mentor identity, breadcrumb path |
| 6–8 | Page kicker/icon, title, review-mode badge |
| 9–16 | Title input, type select, order input, editor status label, editor placeholder, locked media note, cancel link, disabled save button |
| 17–21 | Standards panel title, security note, title/type/order guideline rows |
| 22–25 | Session verification panel, status badge, progress indicator, permissions explanation |
| 26–27 | Promotional image and caption |
| 28–31 | Footer brand/legal text and three footer links |

## 4. Event plan and state checklist

1. Resolve `courseId`/optional `contentId`; create/edit mode is proposed from route params only.
2. Edit path reads #49 collection to locate `contentId`, verifies it belongs to route course, maps current fields to form. Create path carries course ID from ME-06; whether to call #49 in create mode is open.
3. Title/type/order/content editor changes establish dirty state. Input rules are only candidates from mockup until approved; do not fabricate title length, type enum or payload requirements.
4. Save: #50 only if create and body contract is approved; #51 only if edit and derived body is confirmed. Disable duplicate submit; retry/idempotency/conflict are not source-backed.
5. On success, show server result and revalidate #49 before return to ME-06. On failure, keep draft input local, map 401/403/404/422/500 distinctly; exact client UX and session-refresh behavior remain unimplemented.
6. Cancel returns to ME-06 only after destination/unsaved-confirm policy is agreed; current anchor is `#`.
7. States to document separately: create-ready, edit-loading, ready, dirty, validating, saving, saved-await-refresh, access-denied, not-found, validation-error, server/network error, and conflict (design placeholder only; no API #51 version/409 source).

## 5. Acceptance checklist for this session

- Original image/HTML hashes unchanged.
- Plan exists before annotations and DD.
- 31 markers are sequential/unique/in-bounds, non-overlapping, and each maps to one DD element; SVG map and annotated PNG match.
- Every visible input/action/panel has a source mapping, static-only label or explicit `BLOCKED` status; all recognized events have a detailed ordered flow.
- Request/response/body/DB effects use current #49–#51 source; catalog/AC/API DD disagreements remain explicit.
- Statuses are separate: DD remains blocked while unapproved API decisions remain; implementation blocked due missing payload/order/editor/client source; runtime not verified.
- Static audit and `git diff --check` complete; no tests/browser/runtime/live DB probe.
