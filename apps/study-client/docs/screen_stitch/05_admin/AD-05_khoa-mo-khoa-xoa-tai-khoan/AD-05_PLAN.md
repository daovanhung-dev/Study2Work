# AD-05 — Kế hoạch Detailed Design

> **Screen ID:** AD-05 · **Tên:** Khóa/mở khóa/xóa tài khoản · **Đợt/ưu tiên:** W4 / P2<br>
> **Route đề xuất:** `/admin/users/:userId/actions` · **AC:** AC-31 · **API:** #69, #71, #72<br>
> **Trạng thái trước phiên:** screen `D`; #71/#72 có local route/module nhưng API DD/body/policy còn Draft/DERIVED.

## 1. Phạm vi và nguyên tắc

- Hoàn thiện chỉ AD-05 trong phiên này: plan, marker map, annotated image, A–F DD, screen inventory, source index, global tracker và worklog. Không bắt đầu Screen ID kế tiếp.
- Giữ nguyên `screen.png` và `code.html`; ảnh chú thích là tài sản bổ sung.
- AC-31 và API catalog mô tả method/path/response/error nhưng không chốt body #71, trạng thái allowlist, soft-delete/anonymization, audit reason, eligibility, token effect hay Admin safeguards. Local API behavior phải ghi `DERIVED`/source-backed riêng, không coi là owner-approved contract.
- Không phát minh endpoint audit, ticket, permission, undo, hard delete hay token revocation. Không biến copy “vĩnh viễn”, ISO/RBAC/gate hoặc “all active sessions stopped” thành server guarantee.
- Manifest khai báo `createDD-markdown` loại trừ `web-ui-only-dd`; không có canonical skill cho screen UI-only DD. `server-study` Markdown-only deliverable rule chỉ áp dụng API DD, không áp dụng AD-05 screen DD.
- Không chạy application tests/runtime. Đọc test source và kiểm tra tĩnh tài liệu/asset sau khi hoàn tất.

## 2. Bằng chứng đã rà soát

| Nhóm | Nguồn | Kết luận cho AD-05 |
|---|---|---|
| Inventory/dependency | `list_screen.md` AD-02–AD-05; global plan | AD-05 dùng AC-31/#69/#71/#72; numeric user ID từ AD-02/AD-03; post-action inventory yêu cầu refresh #68; links AD-02/AD-03. Current state list `confirm/in-progress/success/dependency-conflict` chưa fully source-backed. |
| AC-31 | `AC_04_ADMIN_MANAGEMENT.drawio`, diagram AC-31 | Actor Admin có user-management permission; chọn user → #69 detail → UPDATE/#70, STATUS/#71 hoặc DELETE/#72 → reload list/detail. #71/#72 nodes path-only; delete says “soft delete/anonymize theo policy”. Diagram có “revoke session nếu cần”, không bắt buộc/all-token semantics. |
| API catalog #69/#71/#72 | `docs/lists/list_api.md` | #69 GET path int64/UserProfile. #71 PATCH status path int64, response UserProfile, 200 updated, 401/403/404/422/500; catalog không nêu body. #72 DELETE path int64, no body/query, response DeleteResult, 200 deleted, same error set. |
| API #71 DD | `docs/dd/71_admin_user_status/{02_Overview,03_Request,04_Response,05_Data_Mapping,06_Error,OPEN_QUESTIONS}.md` | Draft. Body `{status: ACTIVE|SUSPENDED}` và current-state matrix là `DERIVED`. Local transaction row-locks `users`, updates status/updated_at, revokes eligible refresh tokens only when suspending. Existing access JWT may remain usable; active restore does not restore revoked refresh rows. |
| API #72 DD | `docs/dd/72_admin_user_delete/{02_Overview,03_Request,04_Response,05_Data_Mapping,06_Error,OPEN_QUESTIONS}.md` | Draft. Direct request is path-only. Local `DELETED` marker, `updated_at AS deleted_at`, repeat/missing 404, no PII anonymization, dependent-row delete, audit or token revoke are all local `DERIVED` behaviors. |
| API #71 route/model/validation/query/view | `app/api/v1.py`, `api_71_admin_user_status/*` | FastAPI typed request body can be schema-validated before the endpoint/view auth guard. View then calls shared ADMIN guard, signed-int64 parser, current-status row lock, update and conditional refresh-token revoke. Strict body has one required field; unsupported current statuses map 422. |
| API #72 route/model/validation/query/view | `app/api/v1.py`, `api_72_admin_user_delete/*` | No body/query. Shared ADMIN guard precedes raw path parse and DB. One conditional UPDATE marks any non-DELETED current row; missing/already DELETED → 404. Safe DeleteResult is checked before commit; failures roll back. |
| Login/session/access guard | API #03 `view.py`/`query.py`; `app/utils/auth.py` | Login/refresh checks account status is ACTIVE; #71 suspension revokes only unrevoked, unexpired refresh rows. Shared access JWT guard validates claims/roles without a current status lookup; existing access JWT may remain valid until expiry. #72 itself revokes no refresh rows. |
| Downstream visibility | API #68 and #69 query | Neither read query filters DELETED; after #72 the record remains visible to Admin with status marker. #71 rejects current DELETED status (local 422). Visibility/hide/redirect owner policy remains open. |
| Test/context evidence | focused #71/#72 test sources; `.agents/server-study/tests.md` | Context records 21 #71 and 11 #72 passing at prior checkpoints. Tests were inspected, not run; fake DB sessions do not verify live schema/deployment or authorization policy. Tests do not characterize invalid typed body + missing/invalid auth order. |
| Visual/source HTML | `screen.png`, `code.html` | Static no-selection state, selected lock tab, disabled reason textarea/confirm, read-only/policy badges, “permanent delete”, compliance/audit/gate claims; anchors route to `/admin/users`, nav/footer `#`, no client requests/events. |
| Study Web boundary/design | `.agents/web-work/study/*`, `.agents/web-study/design.md`, current app root | `UNWIRED`; root contains `dist`, docs, node_modules and tsbuildinfo but no editable source/package/router/API client. Design guide is intended target, not runtime evidence; screenshot visual system differs. |

## 3. Expected behavior and current behavior

### Expected behavior

1. Enter from AD-03 or AD-02 with the selected numeric `user_id`; load #69 and show current status only after response/policy approval.
2. Allow only approved status/delete actions for an Admin with AC-31 user-management permission. Exact ADMIN-claim mapping and safeguards are not approved.
3. #71 requires an owner-approved target body/status transition contract before lock/unlock can be implemented. #72 requires an owner-approved delete, retention, anonymization and visibility policy before its local fallback can be treated as intended behavior.
4. After an approved action succeeds, follow AC-31 reload of list/detail and preserve the selected numeric ID only where the route policy requires it. No retry/undo behavior is specified.
5. Audit reason, session impact, identity lifecycle and destructive warning must come from approved contract/policy; do not imply these are handled by the present APIs.

### Current local API behavior

- #71 local body is strict required `{status: "ACTIVE"|"SUSPENDED"}`; this is `DERIVED` because catalog/AC omit body. The route's Pydantic body model is evaluated before the endpoint calls view auth; invalid body can therefore return framework 422 before the ADMIN check. Existing auth tests use a valid body and do not characterize the mixed-invalid case.
- #71 view validates shared Bearer/JWT `ADMIN`, parses raw signed-int64 path, locks current status `FOR UPDATE`, accepts only current `ACTIVE`/`SUSPENDED`, updates `status` and `updated_at`, maps safe UserProfile, and commits. If target is SUSPENDED, it revokes only rows in `refresh_tokens` that are unrevoked and unexpired in the same transaction. A same-state request still updates timestamp; repeated SUSPENDED can revoke any newly eligible refresh rows. ACTIVE does not restore previously revoked tokens.
- API #03 blocks new login/refresh unless user status is ACTIVE. Access JWT guard does not check current status/revocation, so existing access JWT can remain usable until expiry. #71 is not proof that all sessions end immediately.
- #72 local endpoint has no body/query. After ADMIN guard and signed-int64 parse, one conditional `UPDATE users SET status='DELETED', updated_at=CURRENT_TIMESTAMP WHERE id=:user_id AND status IS DISTINCT FROM 'DELETED' RETURNING id, updated_at AS deleted_at` runs. It does not physically delete/anonymize profile, check relations, write audit, or revoke refresh tokens. API #03 blocks new login/refresh because status is not ACTIVE; existing access JWT may remain valid. #68/#69 still return the marked row.
- #71 success is 200 `DESIGN_RESOURCE_UPDATED` with UserProfile. #72 success is 200 `DESIGN_RESOURCE_DELETED` with `DeleteResult{id,status:"deleted",deleted_at}`; the timestamp is an alias of this mutation's `updated_at`, not a persisted deletion timestamp. Both return catalog 401/403/404/422/500; error envelope uses `data:null`.

### Current prototype behavior

- No user is selected: ID text is truncated; status says unknown; intervention permission says blocked by policy. The first lock tab is selected, but selection state has no runtime handler.
- The action tabs are “Tạm khóa tài khoản”, “Mở khóa tài khoản”, and “Xóa tài khoản vĩnh viễn”. The last label conflicts with local #72 soft-marker behavior.
- Text says all active work sessions and login rights will stop; local #71 only revokes eligible refresh rows on suspend and current access JWTs can survive; #72 revokes no token rows.
- The required audit-reason textarea is disabled. #71 request has only a status key in local candidate; #72 has no body. Neither API writes an audit record.
- Confirm is disabled; all back links go to `/admin/users`. There is no client request, action handler, active user ID, or Study Web route implementation.
- ReadOnly, gate-active, ISO/IEC compliance, audit ID and “enforced gate” footer claims are static and have no source in #69/#71/#72.

## 4. Planned markers and element map

Coordinates use original `screen.png` at 1600×1428. Marker IDs are ordered top-to-bottom, then left-to-right. Related icon+label/copy are grouped in one element where they represent one content block.

| # | Coordinate (x,y) | Element/component | Source/design constraint |
|---:|---:|---|---|
| 1 | (18,35) | Study2Work/LMS/Admin Portal brand | Static shell brand. |
| 2 | (700,58) | Primary Admin navigation group | Five placeholder anchors use `#`. |
| 3 | (1115,58) | System Normal badge | Static health claim, no source. |
| 4 | (1304,55) | Notifications button | No handler/data. |
| 5 | (1560,55) | Admin identity/avatar | Hard-coded; no current Admin profile source here. |
| 6 | (20,95) | Global breadcrumb trail | Static labels/cursor styling. |
| 7 | (1577,115) | RBAC assurance badge | Does not establish AC-31 permission. |
| 8 | (180,154) | User-management/list/action breadcrumb | Static labels, no route state. |
| 9 | (1045,186) | Back to AD-02 link | Current href `/admin/users`; router not wired. |
| 10 | (180,230) | API #69/#71/#72 reference strip | Static API names, no request evidence. |
| 11 | (1200,323) | Page title | Static copy “Kiểm soát trạng thái và quyền truy cập tài khoản”. |
| 12 | (465,347) | Security shield hero icon | Decorative/section marker. |
| 13 | (1220,407) | Page subtitle | Claims session/revoke/delete impact; must be corrected to actual approved policy. |
| 14 | (380,480) | Execution-context panel heading | Static section label. |
| 15 | (1248,492) | Read-Only protocol badge | Static UI gate; not backend policy state. |
| 16 | (650,560) | Target account ID card | No selected ID; ID is truncated; use numeric `user_id` from prior screen when wired. |
| 17 | (915,560) | Current account-status card | Static “unknown”; map approved #69 `status` after load. |
| 18 | (1188,577) | Intervention-permission card | Static “blocked by policy”; permission decision has no source endpoint. |
| 19 | (1215,628) | Predicted-impact callout | Session/access impact copy conflicts with local #71/#72 behavior. |
| 20 | (700,695) | Action-method label | Static section label. |
| 21 | (645,774) | Lock-account tab | `role=tab`, selected in markup, no state handler; candidate #71 SUSPENDED only after approval. |
| 22 | (920,774) | Unlock-account tab | `role=tab`, unselected, no handler; candidate #71 ACTIVE, does not restore revoked tokens. |
| 23 | (1200,774) | Permanent-delete tab | `role=tab`, unselected, no handler; text conflicts with #72 soft marker. |
| 24 | (370,823) | Admin-reason label + mandatory audit indicator | Static requirement; no body/audit source. |
| 25 | (800,915) | Disabled audit-reason textarea | Disabled; #71 has no reason key and #72 has no body. |
| 26 | (1215,972) | Disabled/inactive badge | Static control state. |
| 27 | (380,1008) | System-policy warning icon | Decorative icon in static panel. |
| 28 | (1228,1122) | Policy warning title and body | Static no-mutation/audit/privacy claims; no API proof. |
| 29 | (910,1198) | Return-safe action | Anchor `/admin/users`; no preservation of selected user. |
| 30 | (1193,1198) | Confirm action button | Disabled, no handler/API call. |
| 31 | (1270,1265) | API handlers / Enforced Gate footer claim | Static; not actual request/gate state. |
| 32 | (380,1265) | Audit code / ISO compliance footer claim | No audit code or compliance data source. |
| 33 | (18,1368) | Copyright/system footer text | Static shell copy. |
| 34 | (1580,1368) | Privacy/RBAC/support footer links | `href="#"`; destinations undefined. |

## 5. Planned events and API processing

| Event | Trigger | Planned behavior | Current prototype / limit |
|---|---|---|---|
| EV-01 — Open action dialog and load account | AD-02/AD-03 handoff or route entry | Receive numeric signed-int64 `user_id`; require approved Admin permission; call GET #69; retain current profile/status baseline. | No selected account in mockup; route/client absent. |
| EV-02 — Select lock/unlock/delete mode | Click tabs #21–#23 | Change local draft selection only; confirm later only if selection/state/policy permit. Lock/unlock candidates map to #71 `SUSPENDED`/`ACTIVE`; delete candidate maps to #72. | Tabs are decorative, no listener. Body/schema/policy are blockers. |
| EV-03 — Confirm status change | Click confirm after selecting #21/#22 | Build exact #71 candidate `{status}` only after owner approval; send PATCH; parse status/envelope; on success refresh #68/#69 per AC-31 and policy. No audit reason is sent. | Confirm is disabled; no handler. Catalog/AC omit body. |
| EV-04 — Confirm delete | Click confirm after selecting #23 | Send bodyless DELETE #72 only after explicit deletion/lifecycle/policy approval; parse DeleteResult; refresh #68/#69; do not claim irreversible delete/anonymization unless contract says so. | Label says permanent; local route is soft marker, not physical delete. Confirm disabled. |
| EV-05 — Back/return safe | Click #9/#29 | Navigate to `/admin/users` or selected AD-03 route only after destination/return-state policy is agreed. No mutation. | Both links point to `/admin/users`; no router. |
| EV-06 — Reason/audit, policy, shell and support controls | Type reason, click disabled badge, render policy/footer/status | Keep non-actionable until body/audit/policy/support/source exists. Render no invented API or assurance claim. | Reason and confirm disabled; gate/audit/compliance copy static; nav/footer links unresolved. |

### API request/response and order

| API | Direct contract | Current local source | UI treatment / blocker |
|---|---|---|---|
| #69 | GET `/api/v1/admin/users/{user_id}`, Bearer JWT/Admin, path int64; 200 `DESIGN_RESOURCE_RETRIEVED`, UserProfile; 401/403/404/500. | Shared ADMIN guard, path parse, read-only safe legacy `users` candidate; no audit field. | Load target/current status; do not use hard-coded ID. PII visibility and fine-grained permission remain open. |
| #71 | PATCH `/api/v1/admin/users/{user_id}/status`, path int64; body absent in catalog/AC; 200 `DESIGN_RESOURCE_UPDATED`, UserProfile; 401/403/404/422/500. | Strict required `{status: ACTIVE|SUSPENDED}` is DERIVED. Current state gate ACTIVE/SUSPENDED only; row lock, update; SUSPENDED revokes unexpired/unrevoked refresh tokens in same transaction. Existing access JWT may survive. | Candidate lock→SUSPENDED, unlock→ACTIVE, but do not enable until body, transition, audit, permission and session effect are approved. |
| #72 | DELETE `/api/v1/admin/users/{user_id}`, path int64, no body/query; 200 `DESIGN_RESOURCE_DELETED`, `DeleteResult`; 401/403/404/422/500. | Conditional `status='DELETED'`, update timestamp, dependent/token rows preserved; repeat/missing 404; `deleted_at` aliases updated_at. | “Vĩnh viễn” and session-ending claims are unsupported. Delete/anonymization/retention/retry/visibility/token policy must be approved. |

## 6. Open decisions / blockers

1. **Admin permission and safeguards:** confirm mapping of `ADMIN` claim to AC-31 permission, tenant/scope/MFA/step-up and self/last-Admin lock/delete protection.
2. **#71 request/status policy:** approve body shape, complete status vocabulary, valid transition matrix, same-state behavior and whether status current state such as deleted/pending should be 422/404/blocked.
3. **Session effects:** decide refresh-token and access-token revocation on suspend/delete, and re-authentication after unlock; local source is not immediate access-token revocation.
4. **#72 deletion:** approve soft marker versus anonymization/physical erase, fields/retention, dependency constraints, persisted deletion timestamp, repeated-delete response, and visibility in #68/#69.
5. **Audit reason:** define whether required reason persists, audit table/event/API, actor, retention and empty/length validation; neither current API accepts it.
6. **Navigation and user selection:** numeric user ID handoff, direct entry without selected ID, post-action refresh/list/detail destination and status display.
7. **Body/auth order:** clarify whether malformed #71 body may return 422 before auth; source route has typed body and mixed-invalid order tests are absent.
8. **Deployment/runtime:** verify legacy schema/deployment and wire Study Web route/client; current screen is static and root app is `UNWIRED`.
9. **Visual/design:** align mockup with `.agents/web-study/design.md` and accessibility guidance after feature contract is settled.

## 7. Execution and verification order

1. [x] Complete docs worklog preflight; read three exact-type worklogs; read project/scope contexts, manifest skill registry and Study Web design guide.
2. [x] Review inventory, AC-31, API catalog/Drafts/source/tests, target HTML/image and current Study Web root; record expected/current and discrepancies.
3. [x] Write this plan before marker JSON/SVG, annotation or AD-05 DD.
4. [x] Create ordered marker JSON/SVG and 2× annotation; preserve originals.
5. [x] Author A–F DD with one element row per marker; describe status/delete/audit/session/API/error/navigation flows without elevating derived source behavior to approved contract.
6. [x] Update `list_screen.md` AD-05 row/API #71/#72 source index and global plan/checkpoint.
7. [x] Verify original hashes, annotation dimensions, marker order/coordinates/1:1 rows, JSON/XML/links, 83 inventory/folder IDs, core bundle count, whitespace and scoped diff.
8. [x] Update worklog final verification; do not run app tests/runtime; do not process another Screen ID.

## 8. Completion decision

Expected result: API #71 and #72 reverse source status rows change `D→R` because route/module/model/validation/query/view/test source exists locally. Formal API DDs stay Draft; #71 body/status and #72 deletion behavior remain DERIVED. AD-05 DD remains blocked by action/session/permission/audit/lifecycle/navigation policy; implementation remains blocked by those decisions and Study Web `UNWIRED`; runtime is not verified. This session handles AD-05 only.
