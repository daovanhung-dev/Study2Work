# AD-04 — Kế hoạch Detailed Design

> **Screen ID:** AD-04 · **Tên:** Chỉnh sửa người dùng · **Đợt/ưu tiên:** W4 / P1<br>
> **Route đề xuất:** `/admin/users/:userId/edit` · **AC:** AC-31 · **API:** #69, #70<br>
> **Trạng thái trước phiên:** screen `D`; API #70 source-backed locally, body contract remains `DERIVED`/Draft.

## 1. Phạm vi và nguyên tắc

- Hoàn thiện chỉ AD-04 trong phiên này: plan, markers, annotated image, A–F DD, inventory/tracker và worklog. Không bắt đầu Screen ID kế tiếp.
- Giữ nguyên `screen.png` và `code.html`; annotation là bản thứ hai.
- API #70 catalog/AC chỉ nêu path, response và error set; không nêu request body. Ghi body hiện có trong source là fallback `DERIVED`, không phải contract được duyệt.
- Phân biệt expected screen behavior, local source, static prototype claims và policy chưa xác nhận. Không tự tạo API unlock/ticket/audit, role mapping hoặc mutation ngoài #70.
- Manifest/skill registry nói Web UI-only DD chưa có skill canonical; `createDD-markdown` dành cho Web/API DD nên không nạp skill đó cho screen UI-only.
- Không chạy application tests/runtime. Đọc test source và thực hiện kiểm tra tĩnh tài liệu/asset sau khi hoàn tất.

## 2. Bằng chứng đã rà soát

| Nhóm | Nguồn | Kết luận cho AD-04 |
|---|---|---|
| Inventory / dependency | `list_screen.md` AD-03/AD-04/AD-05; global tracker | AD-03 chọn user → AD-04 edit → quay về AD-03; inventory mô tả `GET #69 → PUT #70 → GET #69`, dirty state/cancel và `loading/dirty/saving/validation-error`. Route là đề xuất; blocker cũ là body PUT #70 chưa đặc tả. |
| AC-31 | `AC_04_ADMIN_MANAGEMENT.drawio`, node chọn Update | Sau khi đọc user/profile/role, Admin chọn Update → PUT #70 → reload list/detail. Diagram không định nghĩa request body/field rules. |
| API catalog | `docs/lists/list_api.md` #69/#70 | #69 GET detail: `user_id:int64!`, `ApiEnvelope<UserProfile>`, 200, 401/403/404/500. #70 PUT: cùng path int64, `ApiEnvelope<UserProfile>`, 200, 401/403/404/422/500. Catalog #70 không khai báo body, query hoặc writable fields. |
| API #70 DD | `docs/dd/70_admin_user_update/{02_Overview,03_Request,04_Response,05_Data_Mapping,06_Error,OPEN_QUESTIONS}.md` | `Draft — Needs Confirmation`. Body hiện chạy là full-replacement **DERIVED**: required `full_name`, `phone`, `avatar_url`, `role`; `phone`/`avatar_url` nullable; roles `STUDENT/MENTOR/ADMIN`. Body/role/persistence/policy cần owner confirmation. |
| API #70 route/model | `app/api/v1.py`; `api_70_admin_user_update/models.py` | PUT route khai báo `AdminUserUpdateRequest` typed body và OpenAPI candidate schema. Strict Pydantic body `extra=forbid`; đúng bốn keys đều required. |
| API #70 validation/view/query | `validate.py`, `view.py`, `query.py` | Local view auth guard `ADMIN`, signed-int64 path, trim/validate fields, one bound UPDATE of `full_name`, `phone`, `avatar_url`, `role`, `updated_at`; map safe `UserProfile`; commit after mapping; rollback on missing row/query/projection/commit failure. |
| Response / errors | API #04 `UserProfile`, API #70 envelope, response helper, `app/core/middleware.py` | 200 `DESIGN_RESOURCE_UPDATED`; data is safe UserProfile; errors 401/403/404/422/500 with JSON-null `data`. #70 preserves email/status/created_at; no audit or token side effect. Middleware maps Pydantic request errors to 422. |
| API #69 handoff | API #69 catalog/source and prior AD-03 DD | #69 returns profile with signed-int64 `id`, `full_name`, `email`, `role`, nullable `avatar_url`/`phone`, `status`, `created_at`, `updated_at`; no `adminNotes` or audit fields. The route/user role permission fallback and live schema remain open. |
| Focused tests/context | `tests/modules/admin/api_70_admin_user_update/test_admin_user_update.py`; `.agents/server-study/tests.md` | Context records 19 focused passing cases at a prior checkpoint; source covers auth before DB, normalization, body/path 422, no-row 404, safe projection and rollback. Tests were inspected, not run; fake DB sessions do not verify live schema. Auth with malformed body is not characterized. |
| Visual source | `screen.png`, `code.html` | Locked static form. Name/email/role/status/admin notes and Save are disabled; top back and Cancel use inconsistent paths; “Gửi yêu cầu” and API-doc buttons have no handlers. Hard-coded record ID `USR-9281-VN`, lecturer/locked values, sync/RBAC/audit/legal/compliance assertions do not map to #69/#70. |
| Web boundary/design | Study Web subcontext and `.agents/web-study/design.md`; current app root | Study Web remains `UNWIRED`, with no editable source/package/router/API client. Screenshot typography/palette/density differs from intended Study Web guide. |

## 3. Expected behavior and current behavior

### Expected behavior

1. Enter AD-04 from AD-03 with the selected numeric `user_id` from #68/#69; do not encode email or a local `USR-*` alias in the path.
2. GET #69 populates the selected user before edit. Render only fields with approved ownership and PII rules.
3. Allow editing only fields/roles approved for the user-management policy. API #70's current local body is a candidate only: `full_name`, `phone`, `avatar_url`, `role`; it does not update email, status, or admin notes.
4. When the body contract is approved, PUT #70 using the exact accepted schema; validate inputs; protect against duplicate submits; show API errors without losing current form state.
5. On 200 `DESIGN_RESOURCE_UPDATED`, use the returned UserProfile and perform the inventory's #69 revalidation before returning to AD-03. Do not retry a committed PUT because a later GET fails.
6. Cancel/back returns to AD-03 according to the approved route/state behavior. Unsaved-change confirmation policy is not defined by source and must be approved before implementing a modal.

### Current local API behavior

- #70 is wired through `api/v1.py` to `update_admin_user`; API DD remains Draft.
- Local source has a strict full-replacement body with four required keys. `full_name` is trimmed, nonblank and ≤150 characters; `phone` is required key, string/null, trimmed, blank→null and ≤20 chars if string; `avatar_url` is required key, string/null, trimmed and blank→null, with no URL syntax/length validation; `role` must be one of `STUDENT`, `MENTOR`, `ADMIN`. Extra keys are rejected. Every body/allowlist rule is DERIVED because catalog/AC omit body.
- `user_id` is raw path text and must parse as signed int64; local malformed/out-of-range maps 422. Successful one-row UPDATE returns safe API #04 UserProfile and commits; zero rows maps 404; SQL/projection/commit failures roll back and map safe 500.
- UPDATE changes only `users.full_name`, `phone`, `avatar_url`, `role`, and `updated_at`. It preserves `email`, `status`, `created_at`; does not write notes/audit, revoke refresh tokens, or invalidate existing access JWT role claims.
- The route's typed Pydantic body can be rejected by FastAPI's request validation before endpoint/view authorization runs. API DD/context says guard precedes body validation; existing tests cover auth before DB with a valid body but do not characterize invalid body plus missing/invalid auth. Mark ordering unverified.

### Current prototype behavior

- Screen data and badges are hard-coded. The form contains name, email, role, status and admin note; every control and Save is disabled. There are no visible phone/avatar_url inputs even though local #70 requires both keys.
- Role options are `student/lecturer/admin`; status options are `active/locked/pending`. No approved mapping to #70's role literals or #71's separate status API exists.
- The input record ID `USR-9281-VN` is not an int64. Top back path `/admin/users/USR-9281-VN/details` conflicts with inventory route `/admin/users/:userId`; Cancel goes to `/admin/users`, not AD-03.
- “API #69 Fetch Account Meta Verified”, “85%” sync, “API #70 Body Payload Mutation Locked”, “RBAC Token Session: Valid (Level 4 Admin)”, compliance score, SSO actor, audit claim and manual gate-release request are static. No client API calls/handlers or ticket/unlock contract are present.

## 4. Planned markers and element map

Coordinates use original `screen.png` at 1280×1271. IDs are ordered top-to-bottom then left-to-right. Icons are grouped with the control/label they identify. Each marker will map to one AD-04 element row.

| # | Coordinate (x,y) | Element/component | Source/design constraint |
|---:|---:|---|---|
| 1 | (14,14) | Study2Work/LMS/Admin Portal brand | Static brand. |
| 2 | (242,27) | Primary admin navigation group | Five placeholder anchors. |
| 3 | (848,27) | System Normal pill | Static health claim; not #69/#70 data. |
| 4 | (1024,27) | Notifications icon | No handler/API. |
| 5 | (1262,43) | Admin identity/avatar block | Static shell identity; no self-profile source here. |
| 6 | (500,76) | Global breadcrumb trail | Placeholder navigation. |
| 7 | (1260,76) | RBAC verification badge | Does not prove policy/authorization. |
| 8 | (550,139) | User-management/detail/edit breadcrumb | Static labels, not a route implementation. |
| 9 | (954,139) | Back to AD-03 link | Current path contains `USR-* /details`; conflicts with numeric route proposal. |
| 10 | (110,193) | Record-code badge | `USR-9281-VN`; incompatible with signed-int64 path unless source mapping is approved. |
| 11 | (294,193) | “CHẾ ĐỘ KHÓA GHI (GATE ACTIVE)” badge | Static gate state; no gate API. |
| 12 | (16,226) | Page title and subtitle | Static title/copy. |
| 13 | (862,226) | API #69/#70 reference card | Label only; does not verify API calls. |
| 14 | (1049,226) | ReadOnly Enforcement state | Static enforcement claim, not source-backed. |
| 15 | (32,319) | Update Body Gate warning banner | Static body-lock copy; no API-side gate. |
| 16 | (1058,375) | “Tra cứu tài liệu API” button | No handler/destination. |
| 17 | (43,502) | Edit form heading and subtitle | Container title; current form is not interactive. |
| 18 | (872,502) | Target profile card heading / Active ID badge | Static record state. |
| 19 | (818,507) | “Vô hiệu hóa chỉnh sửa” badge | Static lock state. |
| 20 | (872,556) | Target avatar, name, organization and ID | `avatar_url` may exist in #69; org/code mapping unsupported. |
| 21 | (43,600) | Full-name label/input/helper | Candidate `full_name`; current input disabled; API body rule is DERIVED. |
| 22 | (872,640) | Last-edited/actor/compliance metadata | `updated_at` exists, but actor and compliance score do not come from #69. |
| 23 | (43,718) | Email field, Readonly badge and helper | `email` from #69; not writable in #70; PII policy open. |
| 24 | (872,790) | Security and legal rules card heading | Static copy. |
| 25 | (43,845) | Role select, RBAC Schema badge and helper | `role` body candidate uses uppercase allowlist; `lecturer` mapping not approved. |
| 26 | (822,845) | Status select and Active badge | #70 does not update status; options mismatch API #71 local fallback; disabled in prototype. |
| 27 | (872,845) | Versioned data-policy notice | Static policy text, no mapping to #70. |
| 28 | (43,950) | Admin-notes label/textarea/500-char badge | No #69/#70 note field; textarea disabled. |
| 29 | (872,979) | API #69 sync-readiness progress | Static 85%; no sync/percentage field in #69. |
| 30 | (872,1024) | API #69 Fetch Account Meta Verified line | Static claim; no screen client/runtime. |
| 31 | (872,1050) | API #70 Body Payload Mutation Locked line | Static claim; does not reflect server route state. |
| 32 | (43,1065) | Internal audit-history note | No audit event/API in #69/#70. |
| 33 | (872,1077) | RBAC Token Session Valid line | Static claim; role update does not revoke token in current source. |
| 34 | (43,1128) | System-policy locked-submit note | Static rule; no approved gate contract. |
| 35 | (476,1130) | Cancel action | Anchor `/admin/users`; conflicts with AD-03 handoff. |
| 36 | (817,1130) | Save changes button | Disabled; no handler. |
| 37 | (872,1152) | Manual unlock/help callout | No ticket workflow source. |
| 38 | (1126,1157) | “Gửi yêu cầu” button | No endpoint/handler; do not invent ticket action. |
| 39 | (16,1227) | Copyright/system footer text | Static shell copy. |
| 40 | (700,1248) | Privacy/RBAC/support footer links | `href="#"`; destinations undefined. |

## 5. Planned events and API processing

| Event | Trigger | Planned behavior | Current prototype / limit |
|---|---|---|---|
| EV-01 — Open edit screen | AD-03 handoff or direct route | Resolve numeric signed-int64 `userId`; require approved Admin permission; call GET #69; load `UserProfile`; map full_name, email, role, status, avatar_url, phone and ID only into approved fields/state. Keep data and PII out of URL/log. | No router/client; static hard-coded `USR-*` record. |
| EV-02 — Change form values | Name/role change after form and permissions are approved | Normalize local values per approved schema; compare with original state to derive dirty state; do not include email/status/adminNotes in #70. For current source body, carry `phone` and `avatar_url` unchanged from the #69 response unless the UI contract explicitly exposes them. | All inputs/selects disabled; no change event/listener. Phone/avatar_url are absent from visible form. |
| EV-03 — Save | Click Save when dirty, valid, authorized and gate policy allows | Validate exact body; PUT #70 once; parse status/business code/envelope; map response; on 200 revalidate via #69 and return to AD-03. Prevent duplicate submit while pending. Details remain blocked until body/role policy is approved. | Save is disabled; no API call or handler. |
| EV-04 — Cancel/back | Click top back or Cancel | Return to AD-03 with current numeric ID. Unsaved-change confirmation and preservation of dirty values require an approved navigation contract. | Back uses `/admin/users/USR-9281-VN/details`; Cancel uses `/admin/users`; both conflict with inventory handoff. |
| EV-05 — API documentation and manual unlock request | Click API docs or “Gửi yêu cầu” | Navigate/submit only if a documented destination or support API/workflow exists. Keep action unavailable until defined. | Buttons have no handlers; no ticket/unlock endpoint. |
| EV-06 — Shell/policy/audit status | Render badges, legal policy, audit text, identity metadata or sync progress | Render only values with an approved source. #69/#70 provide neither audit rows, compliance score, sync completion nor gate state. Do not present hard-coded claims as current backend state. | All are static prototype content. |

### API #70 body candidate and response mapping

| Field | Local source rule | Screen use / decision |
|---|---|---|
| `full_name` | Required strict string; trim; reject blank; max 150 characters. Body schema/rule is `DERIVED`. | Candidate editable field #21; screenshot disables it. |
| `phone` | Required key; string or null; trim; blank→null; max 20 if string. `DERIVED`. | Not visible; preserve value/null from #69 in full-replacement request unless UI contract changes. |
| `avatar_url` | Required key; string or null; trim; blank→null; no URL syntax/length validation. `DERIVED`. | Not visible; preserve value/null from #69 unless product decides to expose an editor. |
| `role` | Required strict literal `STUDENT`, `MENTOR`, or `ADMIN`; allowlist and transition policy `DERIVED`. | Candidate select #25; current `student/lecturer/admin` labels are unmapped. |
| `email`, `status`, `adminNotes`, IDs/timestamps | Not in #70 request body. | Email/status are returned/preserved by API; notes have no source. Do not send these keys. |
| Success response | 200 `DESIGN_RESOURCE_UPDATED`, `ApiEnvelope<UserProfile>` with `id`, `full_name`, `email`, `role`, `avatar_url`, `phone`, `status`, `created_at`, `updated_at`; `meta` empty, trace ID. | Use returned profile as confirmed mutation result, then inventory requests #69 revalidation. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR`; error `data:null`. | Preserve form state on validation/server errors; auth shell and retry policy are not specified here. |

## 6. Open decisions / blockers

1. **Body approval:** approve or replace local strict full-replacement body; direct catalog/AC does not list request schema.
2. **Visible fields:** decide whether phone/avatar_url must be editable/visible or carried unchanged from #69; reject any silent data clearing.
3. **Role/status policy:** approve `MENTOR`↔“Giảng viên” label mapping and role-transition/self-admin/last-admin rules. Status belongs to #71, not #70; screenshot status options are unsupported.
4. **Identity:** align `USR-9281-VN` and prototype routes to numeric `user_id:int64`; no transformation source exists.
5. **PII/audit/lifecycle:** email/phone visibility, audit trail, admin notes, suspended/deleted/anonymized user behavior remain unresolved.
6. **Security/token:** shared `ADMIN` claim is only a local fallback; API #70 does not revoke role-bearing tokens; tenant/MFA/step-up and immediate access policy require owner decision.
7. **Gate/support workflow:** lock state, sync percentages, API verification badges and manual release-ticket action lack source/API.
8. **Request validation order:** clarify whether body parse/422 may happen before view-level auth; source context and API DD claim auth-first but route has a typed body and tests do not cover the mixed-invalid case.
9. **Runtime/design:** Study Web is unwired; align screenshot with `.agents/web-study/design.md` before implementation.

## 7. Execution and verification order

1. [x] Read current objective, router/context/worklog preflight, exact-type docs worklogs, Study Web/Study Server contexts, inventory, AC, API #69/#70 catalog/DD/source/test source and AD-04 assets.
2. [x] Write this plan before marker JSON/SVG, annotation or AD-04 DD.
3. [x] Create ordered markers, JSON/SVG, and 2× annotation without editing originals.
4. [x] Author A–F AD-04 DD with one element row per marker, detailed events, local API body/status/error mapping, navigation, expected/current discrepancies and blockers.
5. [x] Update inventory/API source rows and global tracker/checkpoint; keep DD/implementation/runtime statuses separate.
6. [x] Update worklog after final verification.
7. [x] Verify source hashes unchanged, annotation dimensions 2560×2542, marker IDs/coordinates/order and 1:1 DD rows, JSON/SVG/local links, 83 inventory/folder match, core bundle count and scoped whitespace.
8. [ ] Do not run app tests/runtime; mark test source inspected-not-run and runtime not verified.

## 8. Completion decision

Expected result: API #70 screen inventory source status changes `D→R` because current route/module/model/query/validation/test source is present; AD-04 DD remains blocked until body/schema/role/PII/navigation/gate decisions are approved; implementation remains blocked by those decisions and Study Web `UNWIRED`; runtime remains `NOT VERIFIED`. This session handles AD-04 only.
