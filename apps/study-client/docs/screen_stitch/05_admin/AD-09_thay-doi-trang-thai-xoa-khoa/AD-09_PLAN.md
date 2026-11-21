# AD-09 — Kế hoạch Detailed Design

> **Screen ID:** AD-09 · **Tên:** Thay đổi trạng thái/xóa khóa · **Đợt/ưu tiên:** W4 / P2<br>
> **Route trong inventory / Angular:** `/admin/courses/:courseId/actions` (route source-present; permission mapping open) · **AC:** AC-32 · **API:** #74, #76, #77<br>
> **Trạng thái inventory tại lần lập plan ban đầu:** `D`; #76/#77 route/module/test sources exist locally, both API DDs remain `Draft — Needs Confirmation`; Study Web `UNWIRED` (historical snapshot; current re-audit in §8).

## 1. Phạm vi và nguyên tắc

- Hoàn thiện riêng AD-09 trong phiên này: source trace, plan này trước marker/DD, marker JSON/SVG, annotated image, A–F screen DD, inventory/API reverse index/global plan/worklog updates, and static audit. Do not begin another Screen ID.
- Preserve `screen.png` and `code.html` unchanged. New screen artifacts are plan, DD, ordered marker JSON/SVG and 2× `screen_annotated.png`.
- Receive numeric `Course.id` from AD-06/#73 or AD-07/#74. Never substitute a display course code; require current course context before applying an operation.
- AC-32 and inventory define the status/delete branch and expected reload. Current API code and tests describe local behavior only. Keep the two evidence sets separate.
- API #76 catalog and AC-32 omit request body/enum members. Its strict `{status}` body and uppercase `DRAFT|PUBLISHED|SUSPENDED` are `DERIVED`; do not treat `archive` as a valid API status.
- API #77 catalog/AC call delete/soft-delete conditional and return `DeleteResult`. Current local implementation soft-marks `DELETED`, checks a candidate dependency set and returns 422 on dependency; it does not hard-delete or cascade. These policy choices are still `DERIVED` and owner confirmation remains required.
- Do not transmit the prototype's audit reason: #76 candidate body has only `status`, its audit row stores actor/old/new values, and #77 has no audit write. The ISO-27001 statement is unsupported by these API contracts.
- Do not claim #76/#77 write-flow wiring, automatic RBAC, lifetime retention, enrollment access effects, reversibility/irreversibility, restore behavior, or production DB state from mockup copy.
- Historical initial snapshot: no Study Web route/client was identified. Current 2026-11-16 source audit is recorded in §8. The original artifact-authoring pass did not run app tests/runtime; historical API test-source/report evidence is not runtime proof.
- Context manifest has no canonical skill for `web-ui-only-dd`; `createDD-markdown` excludes this boundary. No unrelated skill will be loaded.

## 2. Evidence and design treatment

| Topic | Expected / contract | Current source or prototype | Treatment in DD |
|---|---|---|---|
| Route/actor/ID | AC-32 Admin with course-management permission; AD-09 linked to AD-06/AD-07; numeric Course ID; `/admin/courses/:courseId/actions`. | Initial plan snapshot had no Study Web route/client. Current Angular route/page/#74 read caller exists; Stitch prototype has no selected Course and links Back/Cancel to `/admin/courses`. | Route/read flow source-present; fine-grained permission mapping open. Current Angular Back/footer target AD-07; write/reload destination remains open. |
| Flow | AC-32: GET #73 → GET #74 with course/owner/counters → choose update/status/delete; #76 status + audit, #77 soft-delete per policy; reload course management. | Local #73/#74 are GET sources; #73/#74 do not exclude `DELETED`; #76/#77 local mutation handlers are present. | #74 context required. Do not promise counter values; reload #73/#74 destination/sequence is a UI decision. |
| Status actions | Catalog semantic labels mention draft/published/suspended; PATCH #76 accepts `course_id:int64`, returns Page<Course>. | Catalog/diagram omit body; local strict candidate accepts `{status:DRAFT|PUBLISHED|SUSPENDED}`; no transition/readiness check; same status no-op; changed value writes audit atomically. | Radio choices must be treated as prototype only. `archive` does not map to a confirmed #76 status. Body/enum/transitions remain DERIVED/open. |
| Delete action | DELETE #77 per policy; catalog `DeleteResult`; AC-32 says soft-delete by policy. | Local #77 blocks any enrollment and active generic Content/lesson/quiz/assignment; otherwise sets status `DELETED`; no child mutation, hard delete or audit. Repeat delete returns 404. | Do not present “permanent irreversible DB delete” as supported. Dependency set, deleted marker, repeat semantics and restore policy require approval. |
| Reason/audit | AC-32 #76 node calls for status + audit log; no direct reason field in API catalog or diagram. | Prototype labels audit reason required by ISO; textarea is disabled. Local #76 candidate body has only status; audit stores actor, previous/new status; #77 does not audit. | Do not send/persist reason or claim ISO requirement absent approved contract. |
| Authorization | AC-32 requires course-management permission; catalog says Bearer JWT/Admin. | Local #76/#77 shared guard checks role `ADMIN`; no separate course-management permission source. | Keep permission mapping `OPEN`; never infer access from static RBAC badge. |
| Schema/lifecycle | API paths use int64; no live schema proof in direct contract. | Legacy BIGINT DDL/migration 010 differ from V1-PILOT UUID/versioned Course. #73/#74 expose `DELETED`; #76 does not exclude it and can replace status. | Live schema, tombstone visibility, restore and other writer policy remain blockers. |
| Prototype event behavior | User selects a status/delete operation then confirms according to approved API flow. | Native radio selection works locally, default `draft`; empty `change` listener. Reason and Confirm disabled; no API transport. | Document selection only as prototype behavior; no mutation event is implemented. |

## 3. Marker plan

- Use **38 markers** in top-to-bottom order: Admin shell and navigation; route/breadcrumb; action card title; target/current/enrollment context; three radio options; reason/policy; actions; data-safeguard/footer.
- Give each radio option its own marker. Group a heading with its adjacent cue when they form one visible element. Separate Cancel and disabled Confirm.
- Markers use original-image pixel coordinates (1538×1600), small circles placed toward nearby whitespace/card edges so labels remain readable. Render SVG at source coordinates and composite onto a 2× image (3076×3200).
- Section C must contain exactly one row for each marker #1–#38. Marker labels identify elements, not approved API behavior.

## 4. Events to specify

1. **EV-01 — Enter action route/load context:** receive numeric ID; use #74 to identify Course/current status; show no-action/not-found/access states. Study Web handler absent.
2. **EV-02 — Select operation:** native radio group has values `draft`, `archive`, `delete`; only local visual selection works. Candidate status body cannot be inferred from the lower-case radio values; deletion is a separate #77 request. `archive` has no confirmed mapping.
3. **EV-03 — Confirm status change (#76):** describe local candidate request, lock/update/audit/readback/commit order; distinguish direct catalog from DERIVED body/enum and permission; no audit-reason field.
4. **EV-04 — Confirm delete (#77):** describe no-body request and current lock → dependency check → soft-delete → result pipeline; 422 dependencies, 404 missing/already-deleted, 500 safe failures; no hard delete/cascade/audit.
5. **EV-05 — Cancel/back/reload:** current anchor returns to `/admin/courses`; target detail/list route and post-mutation refresh are unresolved. No mutation request on cancel.
6. **EV-06 — Shell/footer/policy affordances:** anchors `#`, static RBAC/retention/legal claims; no runtime effect.

## 5. API and data trace

- **#74 context:** `GET /api/v1/admin/courses/{course_id}`, Bearer/Admin, int64 path; `ApiEnvelope<Page<Course>>`; current local result includes Course/mentor and status, no counters; no deleted filter. API DD #74 Draft.
- **#76 status:** `PATCH /api/v1/admin/courses/{course_id}/status`, Bearer/Admin, int64 path. Direct catalog response `ApiEnvelope<Page<Course>>`; 200 `DESIGN_RESOURCE_UPDATED`; errors 401/403/404/422/500. Request body omitted by catalog/AC. Local strict candidate `{status:"DRAFT"|"PUBLISHED"|"SUSPENDED"}`; no audit reason.
- **#76 local effect:** auth role ADMIN → path parse → lock status row → if different update `status`/`updated_at` and add actor/old/new audit row → read #74 projection → build singleton Page → commit. Same target does not update timestamp or append duplicate audit. Errors in query/audit/projection/commit rollback and safe 500.
- **#77 delete:** `DELETE /api/v1/admin/courses/{course_id}`, Bearer/Admin, int64 path, no body/query. Direct response `ApiEnvelope<DeleteResult>` with `{id:int64,status:"deleted",deleted_at:date-time}`; 200 `DESIGN_RESOURCE_DELETED`; errors 401/403/404/422/500.
- **#77 local effect:** auth role ADMIN → parse path → lock course not already DELETED → check any enrollment or any active generic Content/lesson/quiz/assignment row → if found rollback and 422; otherwise set status `DELETED`/DB timestamp, map `updated_at` to `deleted_at`, commit. It does not delete children or append audit. Dependency set, marker, and timestamp mapping are DERIVED.
- API #76/#77 DDs remain Draft; tests historically use fake DB sessions. Live database/schema, migration deployment, dedicated permission and frontend route are unverified.

## 6. Blockers and target status

1. Approve #76 request body, status enum/casing, transition/readiness policy, same-status/retry semantics, publish/suspend learner effects and permission mapping.
2. Resolve prototype `archive` option; it is not in the local candidate body enum.
3. Approve #77 dependency policy, soft-delete marker/timestamp mapping, repeat-delete behavior, visibility/restore policy, linked writer behavior and whether delete auditing is required.
4. Decide whether audit reason is required; it is not present in #76/#77 contract/source.
5. Confirm live schema/deployment and AC-32 permission versus shared role `ADMIN`.
6. Implement the approved #76/#77 write flow, permission/error/session handling, and post-mutation reloading. Current route/page/#74 read flow exists; mutation and reload policy remain open.
7. Replace or source unsupported permanent-delete, ISO/audit-reason, RBAC, retention and learner-dependency claims.

Target status recorded by the initial artifact-authoring pass (historical): an evidence-complete design with **DD BLOCKED** and **IMPLEMENTATION BLOCKED** pending status/delete and permission/schema decisions. Current implementation status is recorded in §8. Runtime remains **NOT VERIFIED**.

## 7. Execution and verification order

1. [x] Docs preflight; read three exact-type worklogs and AD-08 cross-screen handoff; load project/scope/context and registry.
2. [x] Review AD-09 assets/DOM, inventory, AC-32, API catalog/DD/source/tests, #73/#74 handoff and schema candidates; record expected/current discrepancies in worklog.
3. [x] Write this plan before markers, annotation or screen DD.
4. [x] Create ordered marker JSON/SVG and 2× annotated PNG; visually inspect marker placement.
5. [x] Author A–F DD with one row per marker, event sequence, API/error matrix, state/navigation matrix and blockers.
6. [x] Update AD-09 inventory and reverse API source status for #76/#77; update global tracker/checkpoint.
7. [x] Static audit hashes/dimensions, JSON/XML, marker order/bounds and C-row bijection, links, screen ID/folder/core-artifact counts, whitespace and final image. Do not run application tests/runtime.
8. [x] Finalize worklog; stop after AD-09.

## 8. Current Study Web source re-audit — 2026-11-16

This dated addendum supersedes only the “Study Web UNWIRED/no route-client” current-state statements above. The original Stitch and API evidence remains unchanged; the previous audit is retained as history.

### 8.1 Current source facts

- `admin.routes.ts` registers `courses/:courseId/actions` → `AD09Page`; the route spec covers the registration.
- `AD09Page` reads the raw route `courseId`, calls `AD09ApiService.getCourse()` → GET #74, and exposes `loading/loaded/error` states. Loaded UI displays title, status, mentor, price and the exact raw route ID. The #74 projection has no counters.
- Status, delete and reason controls remain disabled. AD09 has no #76/#77 browser caller; do not enable or invent these requests while API body/status/delete/permission policy remains open.
- Current Angular Back/footer links return to AD-07 using the raw route ID; the load-error link returns to AD-06. The Stitch prototype Back/Cancel links both go to AD-06. Post-mutation reload policy remains unresolved.
- The current ID display label correction is “ID khóa học”; it displays the route value without numeric conversion.
- Current source `loading/loaded/error` does not prove deployed/runtime behavior: `RUNTIME NOT VERIFIED`.

### 8.2 Re-audit disposition

- Keep **DD BLOCKED** and all API #76/#77 body, enum, lifecycle, dependency, audit and permission blockers.
- Update implementation status to **PARTIAL SOURCE; WRITE FLOW BLOCKED**. The read-only route and #74 caller exist; mutations do not.
- Keep prototype artifact rows as evidence of the static Stitch HTML. Record their navigation separately from Angular behavior.
- Focused spec/build, link/stale-claim scan and context validation are recorded in the active worklog after execution; they do not establish browser or production runtime.
