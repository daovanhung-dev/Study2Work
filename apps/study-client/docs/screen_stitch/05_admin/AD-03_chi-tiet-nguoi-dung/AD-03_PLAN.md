# AD-03 — Kế hoạch Detailed Design

> **Screen ID:** AD-03 · **Tên:** Chi tiết người dùng · **Đợt/ưu tiên:** W4 / P1<br>
> **Route đề xuất:** `/admin/users/:userId` · **AC:** AC-31 · **API chính:** #69<br>
> **Trạng thái trước phiên:** `D` · **Kết quả dự kiến:** source API `R`; DD và implementation bị chặn bởi các quyết định còn mở; runtime chưa xác minh.

## 1. Phạm vi và nguyên tắc

- Hoàn thiện chỉ AD-03 trong phiên này: plan, marker map, annotated image, A–F DD, inventory/tracker và worklog.
- Giữ `screen.png` và `code.html` nguyên trạng. Không bắt đầu Screen ID kế tiếp.
- Tách contract/AC khỏi runtime source. Ghi `DIRECT`, `SOURCE_BACKED`, `DERIVED`, `UNWIRED` và `NOT VERIFIED` tại nơi áp dụng; không suy luận business policy từ mockup.
- API #69 hiện là source-backed cục bộ. Route Study Web chưa có trong source; route trong inventory chỉ là đề xuất.
- Không tạo audit feed, sync endpoint, 204 success, quyền Admin, PII masking, retention hay luật trạng thái nếu không có nguồn.
- Không chạy application tests hoặc runtime. Chỉ đọc test source và chạy kiểm tra tài sản/tài liệu sau khi hoàn tất.

## 2. Bằng chứng đã rà soát

| Nhóm | Nguồn | Kết luận dùng cho AD-03 |
|---|---|---|
| Inventory và handoff | `list_screen.md` AD-03, AD-02, AD-04, AD-05 | AD-03 là chi tiết tài khoản; từ AD-02/#68 nhận user đã chọn; đích kế tiếp AD-04 hoặc AD-05. Route đề xuất, trạng thái cũ `D`. |
| Activity | `AC_04_ADMIN_MANAGEMENT.drawio`, lane AC-31 | Admin đăng nhập và có quyền user management; chọn user → GET detail #69 → đọc profile/role → nhánh update #70, status #71 hoặc delete #72. Đây là flow nghiệp vụ trong diagram, không chứng minh quyền/endpoint đã được phê duyệt live. |
| API contract | `docs/lists/list_api.md` #69 | `GET /api/v1/admin/users/{user_id}`, Bearer JWT/Admin, path `user_id:int64!`, `ApiEnvelope<UserProfile>`, success 200; errors 401/403/404/500. Không có query/body/pagination. |
| API runtime | `app/api/v1.py`; `modules/admin/api_69_admin_user_detail/{validate,query,view,models}.py`; shared auth/response helpers | Route wire tới view. Shared guard kiểm tra Bearer/JWT và claim `ADMIN` trước parse path/query; guard-to-user-management mapping còn DERIVED. Raw signed-int64 parse; malformed/out-of-range và row missing map 404; safe allowlisted legacy `users` projection; query/mapping errors map 500; response `DESIGN_RESOURCE_RETRIEVED`. |
| Response schema | `UserProfile` từ API #04 và API #69 envelope model | `id:int`, `full_name:string`, `email:string`, `role:string`, `avatar_url:string|null`, `phone:string|null`, `status:string`, `created_at`, `updated_at`. `bio` không có trong runtime model; không trả `password_hash`. `meta` rỗng và `traceId` có trong envelope. |
| API DD / open questions | `docs/dd/69_admin_user_detail/02_Overview.md`, `03_Request.md`, `04_Response.md`, `06_Error.md`, `OPEN_QUESTIONS.md` | API DD `Draft — Needs Confirmation`. Legacy BIGINT table target, ADMIN policy mapping, path/no-row 404 derivation, enum values, PII/audit and lifecycle decisions remain open. |
| DB/source basis | `infra/postgres/study-server/DB.sql`; API #69 query | Checked-in legacy `users` has BIGSERIAL `id` and candidate profile columns. Query selects only the response allowlist and omits password hash. V1-PILOT UUID identity model differs; live schema/grants/deployment not verified. |
| Test evidence | `tests/modules/admin/api_69_admin_user_detail/test_admin_user_detail.py` | Source asserts safe field projection, auth before DB, malformed ID 404, no-row 404, query/mapping 500, no commit, OpenAPI int64/error set. Tests use fake sessions/rows and were inspected, not run. |
| Visual source | `screen.png`, `code.html` | Static detail screen in a no-selected-user/“CHƯA ĐỒNG BỘ” empty state. Edit/status controls disabled. Audit panel and 180-day retention, “RBAC Strict Audit Active”, system-normal/sync claims and 204/NULL_PAYLOAD text have no evidence in API #69. HTML has placeholder links and no request/interaction code. |
| Web boundary/design | `.agents/web-work/study/AGENTS.md`, `.agents/web-study/design.md`, current `apps/study-client/` root | Study Web is `UNWIRED`; root has `dist`, `docs`, `node_modules`, and `tsconfig.tsbuildinfo`, with no editable `src/`, package manifest, router or client. Prototype palette/typeface differs from the Study Web design guide. |

## 3. Expected behavior and current behavior

### Expected flow from inventory/AC/API contract

1. An authenticated Admin with approved user-management permission opens the proposed detail route from AD-02 using the selected user's `id` as `user_id`; do not put email or phone in the URL.
2. The client requests API #69 with Bearer JWT and the path ID. The catalog defines no query or body.
3. On 200 `DESIGN_RESOURCE_RETRIEVED`, map the returned `UserProfile` fields to approved profile elements. Do not infer audit history from profile data.
4. Provide return navigation to AD-02. Offer AD-04 / AD-05 handoffs only after those screens, permissions, destination routes, and API contracts are resolved.
5. Handle 401, 403, 404, 500 and network failure as distinct outcomes. Detail success requires a profile object; an empty/sync-pending state is not an API #69 success contract.

### Current behavior from source/prototype

- API #69 is wired locally and performs the safe read described above. `ADMIN` claim mapping is a local fallback for AC-31 permission, not an approved user-management policy.
- The local query targets the checked-in legacy `users` candidate. A fake-DB test suite does not establish live schema or deployment.
- The HTML is static: no router, API call, form, input, event listener, or enabled mutation control. Back/breadcrumb/footer anchors use fragments or `#` placeholders.
- The prototype renders no selected account and shows `204 / NULL_PAYLOAD`; this conflicts with API #69's 200 `UserProfile` success and 401/403/404/500 error set. Do not present 204 as current API behavior.
- The audit-history card, retention duration, sync status, RBAC assurance, and automatic monitoring are unsupported by API #69 source. Their API/event source and approved copy are unresolved.

## 4. Planned markers and element mapping

Coordinates are on the unscaled `screen.png` (1600×1456). IDs follow top-to-bottom, then left-to-right reading order. Each row will map to exactly one AD-03 element row; controls containing an icon and label are grouped as one component.

| # | Planned coordinate (x,y) | Element/component | Mapping / constraint |
|---:|---:|---|---|
| 1 | (16,18) | Study2Work/LMS/Admin Portal brand | Static brand; destination not defined. |
| 2 | (292,22) | Primary admin navigation | Five placeholder anchors; destinations not wired. |
| 3 | (1250,36) | System Normal pill | Static unsupported health claim; do not derive from #69. |
| 4 | (1300,36) | Notifications icon | No handler or route/API. |
| 5 | (1583,59) | Admin identity/avatar | Static identity; no self-profile source in this screen. |
| 6 | (510,96) | Global breadcrumb trail | Placeholder shell navigation. |
| 7 | (1583,111) | RBAC verification badge | Static assertion; does not prove API authorization policy. |
| 8 | (523,166) | User-management/detail breadcrumb | “Danh sách tài khoản” fragment; route handoff must use AD-02 contract. |
| 9 | (1578,166) | API #69 / data-sync badge | Static sync wording is unsupported; API #69 is a read, not sync. |
| 10 | (20,235) | Back to user list button | Intended AD-02 handoff; current `href` is a fragment. |
| 11 | (54,315) | Detail hero: icon, title, subtitle, AD-03 code | Static page heading; description overstates audit source until resolved. |
| 12 | (54,487) | Identity/contact card heading | Container heading; no independent request. |
| 13 | (899,487) | “Chưa đồng bộ” badge | Unsupported state; do not map to API #69 response. |
| 14 | (957,487) | Administrative-actions card heading | Static container. |
| 15 | (956,574) | Edit user (AD-04) button | Disabled in prototype; future navigation only after #70 and AD-04 decisions. |
| 16 | (48,581) | No-selected-user information panel | Prototype empty copy; API #69 does not define 204/null success. |
| 17 | (956,647) | Lock/status (AD-05) button | Disabled in prototype; future status/delete branch uses #71/#72 contracts. |
| 18 | (957,730) | Identity-confirmation advisory | Static rule; authoritative activation condition needs owner confirmation. |
| 19 | (50,780) | Full-name row | `data.full_name`; source required on success. |
| 20 | (50,851) | Email row | `data.email`; PII visibility/masking policy open. |
| 21 | (960,867) | Login/role audit heading and count | No audit endpoint/row source in #69; do not show fabricated count. |
| 22 | (50,921) | User-ID row | `data.id`; use as signed-int64 handoff to #69. |
| 23 | (958,940) | Audit empty-state panel | Unsupported by #69; empty history must not imply no events without an audit source. |
| 24 | (50,990) | Phone row | `data.phone:string|null`; PII policy open; preserve null if displayed. |
| 25 | (50,1059) | System-role row | `data.role:string`; enum members/label mapping open. |
| 26 | (50,1129) | Account-status row | `data.status:string`; enum members/lifecycle visibility open. |
| 27 | (957,1166) | Security protocol / retention note | “180 ngày” and logging protocol have no source in #69. |
| 28 | (52,1203) | API endpoint/response footnote | Endpoint aligns to #69; `204 / NULL_PAYLOAD` conflicts with source. |
| 29 | (54,1298) | Privacy/compliance banner | Nghị định and automatic monitoring copy requires policy/legal owner approval. |
| 30 | (1285,1320) | RBAC Strict Audit Active badge | Static unsupported audit/RBAC assertion. |
| 31 | (15,1397) | Copyright and system footer text | Static shell text. |
| 32 | (880,1414) | Privacy/RBAC/support footer links | `href="#"`; destinations not defined. |

## 5. Planned events and API processing

| Event | Trigger | Planned handling | Current prototype / evidence |
|---|---|---|---|
| EV-01 — Open detail | Route entry from AD-02 or direct link | Obtain `user_id` from route; require approved auth/permission; call #69 once with Bearer JWT; no query/body. API checks auth before parsing. Map 200 envelope and `UserProfile`; handle 401, 403, 404, 500/network distinctly. Invalid/out-of-range and no-row 404 are current local behavior, with derivation noted in API DD. | No route/request code; static empty state. |
| EV-02 — Return to AD-02 | Back button or list breadcrumb | Navigate to approved list route; preserve list query only if AD-02 navigation contract defines it. Never include PII in URL. | Fragment anchors only. |
| EV-03 — Edit handoff | Edit button | Button currently disabled. If enabled later, pass user ID to AD-04; #69 is read-only and #70 body/policy belongs to the AD-04/API #70 contract. No mutation from AD-03. | Disabled button, no handler. |
| EV-04 — Account action handoff | Lock/status button | Button currently disabled. If enabled later, route to AD-05; #71/#72 policy and confirmation belong there. Do not claim session revocation from AC diagram alone. | Disabled button, no handler. |
| EV-05 — Audit/history render | Page render | Render audit rows/count/empty state only after an approved audit API, event schema, permission and retention contract exists. #69 cannot supply this data. | Static “0 bản ghi”, empty message and 180-day retention. |
| EV-06 — Shell/footer navigation | Click nav, notification, profile, policy/support | Use only routes and actions defined by another screen/contract; no API request may be inferred from static badge/copy. | Placeholder `#` anchors and icon with no handler. |

### API #69 response mapping to the visible profile rows

| API field | Type / nullability | Screen destination | Current status |
|---|---|---|---|
| `data.id` | integer / legacy signed-int64 candidate | User-ID row; subsequent route path | Source-backed local projection; live schema and upstream handoff remain unverified. |
| `data.full_name` | string | Full-name row | Source-backed; required on success. |
| `data.email` | string | Email row | Source-backed; PII masking/visibility policy open. |
| `data.phone` | string or null | Phone row | Source-backed nullable field; PII policy open. |
| `data.role` | string | System-role row | Source-backed string; enum values and display labels open. |
| `data.status` | string | Account-status row | Source-backed string; enum values and deleted/anonymized visibility open. |
| `data.avatar_url` | string or null | Not shown by this screenshot | Available in response; do not add a visual element in this session. |
| `data.created_at`, `data.updated_at` | date-time | Not shown by this screenshot | Available in response; display/timezone rules not needed unless layout changes. |
| `data.bio` | omitted by runtime `UserProfile` | None | Catalog optionality does not create a runtime field or a screen field. |
| `success`, `businessCode`, `message`, `meta`, `traceId` | envelope fields | State/error handling only | `200 DESIGN_RESOURCE_RETRIEVED`; error envelopes use `data:null` and 401/403/404/500. |

## 6. Known blockers and decisions

1. **Admin access:** AC-31 says user-management permission; runtime checks claim `ADMIN`. Owner must confirm whether that claim is sufficient and whether tenant/MFA/permission-relation checks are required.
2. **Live schema:** local query targets legacy BIGINT `users`; V1-PILOT uses UUID identity/profile relations. Confirm live relation, grants and deployment.
3. **PII and profile presentation:** email/phone masking, Admin visibility, role/status enum values and lifecycle behavior after #71/#72 need approval.
4. **Audit data:** no API #69 audit fields or event feed. Identify audit API/source, permission, event types, count/empty semantics and retention owner before rendering the audit card as data.
5. **Unsupported prototype behavior:** sync/204/null, system health, RBAC verification, automatic monitoring, 180-day retention and legal compliance badge need removal or authoritative contract/design approval.
6. **Frontend wiring:** Study Web lacks source/router/package manifest. Implementing route, auth shell, loading/error states, and navigation requires restoring/wiring the frontend.
7. **Design consistency:** screenshot typography/palette differ from `.agents/web-study/design.md`; align or get design approval during frontend implementation.

## 7. Execution and verification sequence

1. [x] Read goal objective, router/context/worklog requirements, exact-type docs worklogs, screen inventory, cross-scope boundaries, manifest, AC-31, API catalog/DD, current route/module/query/model/auth/response/test source, prototype and screenshot.
2. [x] Write this plan before marker JSON/SVG, annotation, or AD-03 DD.
3. [x] Create 32 unique, ordered marker definitions and matching SVG/2× annotated PNG without editing original assets.
4. [x] Write AD-03 A–F DD with one row per marker, API/event/error mapping, screen states, navigation handoff and unresolved decisions clearly separated.
5. [x] Update AD-03 inventory row and global tracker with source/API and independent DD/implementation/runtime statuses; add session checkpoint.
6. [x] Update worklog with completed trace and verification results.
7. [x] Verify original hashes unchanged; annotation dimensions 3200×2912; marker IDs unique/sequential/in-bounds; marker rows match DD; JSON/SVG/local links valid; 83 screen IDs/folders remain consistent; scoped diff passes whitespace checks.
8. [x] Do not run application tests or runtime; mark source tests `INSPECTED_NOT_RUN` and runtime `NOT_VERIFIED`.

## 8. Completion decision

Expected outcome: API #69 source classification changes `D→R`; AD-03 DD remains `BLOCKED` because permission/PII/audit/schema decisions prevent a fully implementable design; implementation is `BLOCKED` by Study Web `UNWIRED` plus policy/schema; runtime remains `NOT VERIFIED`. No other Screen ID is started.
