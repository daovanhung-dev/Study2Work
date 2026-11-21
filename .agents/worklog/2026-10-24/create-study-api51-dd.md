---
task_id: "2026-10-24-create-study-api51-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD API #51 — Cập nhật nội dung Mentor

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Mentor course access và legacy `courses.mentor_id` chỉ là candidate; giữ riêng model Content với Lecture; schema versioned pilot khác catalog BIGINT.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: AC-22 Content tree, schema Content, enum/payload và principal mapping còn gaps; không trộn schema hay thêm field như dữ kiện.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: API #50 tạo Content với `content_type/title/payload`; trạng thái pending-review, parent/order và physical mapping được gắn nhãn DERIVED/SOURCE_REQUIRED; API #51 là update/version flow trong AC-22.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Catalog #51 `PUT /api/v1/mentor/content/{content_id}`, Bearer JWT role Mentor, path `content_id:int64!`; catalog hiện không khai báo request body. Response `ApiEnvelope<Content>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`; errors đúng 401/403/404/422/500 và các `DESIGN_*` code tương ứng.
- Canonical contract/approved DD: `docs/lists/list_api.md` row #51 + reusable Content; AC-22 flow: PUT → `UPDATE Content + version` → reload cây. AC-22 có precondition Mentor quản lý course. AC-33 đọc content/version/author cho review và đọc `status=PENDING_REVIEW` trong hàng đợi.
- Vì diagram và catalog đều bỏ body fields dù PUT phải mang thay đổi, đề xuất body `content_type`, `title`, `payload` (đầy đủ, replace phần nội dung có thể sửa) lấy từ API #50 Content schema; đây là `DERIVED` proposal, không phải catalog contract.
- Đề xuất phiên bản mới vào review `PENDING_REVIEW` và giữ revision đã publish làm bản đang phục vụ đến khi revision mới được duyệt/publish; đây là `DERIVED` lifecycle proposal. Version storage/schema chưa có nguồn.

## CURRENT_BEHAVIOR

- Source/config: Search hiện tại không tìm thấy route `/api/v1/mentor/content/{content_id}`, module API #51 hoặc test API #51 trong Study Server.
- Schema: Legacy `DB.sql` có `courses`, `lessons`, không có generic Content/version table. V1-PILOT có `content_blocks` UUID và versioned course model nhưng không ánh xạ trực tiếp catalog Content BIGINT. Live schema chưa xác minh.
- Runnable tests: Không có test API #51; task docs-only, không chạy application tests.
- Runtime wiring: API #51 `UNWIRED` / `NOT_FOUND`. Nếu wire route, `DESIGN_CONTRACT_PATHS` cần được cập nhật để middleware trả đúng code catalog.

## SOURCE_TRACE

```text
Mentor Bearer JWT -> PUT path content_id -> load Content + owning course/version (logical; physical schema SOURCE_REQUIRED) -> check Mentor course-management permission -> validate proposed editable body -> update Content and advance version atomically (AC-22) -> return ApiEnvelope<Content> -> AC-22 reloads tree
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Request body | Catalog and AC-22 PUT node list only `path{content_id:int64!}` while diagram says UPDATE Content + version | `DISCREPANCY`; proposed body is `DERIVED` | DD will preserve listed contract and separately show proposed full-replacement body from existing Content fields. |
| Version model | Diagram says `UPDATE Content + version`; no generic Content version relation/table in available compatible DDL | Logical effect DIRECT; physical model `SOURCE_REQUIRED`; history/state details DERIVED | Do not write physical SQL or invent columns/table. |
| Review state | AC-33 requires queue rows `PENDING_REVIEW`; AC-22 update has no state transition text | New revision pending is `DERIVED` | Keep prior published revision active as a simple proposal; macro-review needed with #52/Admin AC-33. |
| Runtime | No route/module/test found | `UNWIRED` / `NOT_FOUND` | Draft describes expected design, not current API behavior. |
| Mentor identity/course relation | AC-22 requires managed course; Study Mentor principal binding absent | `SOURCE_REQUIRED`; legacy direct owner only `DERIVED` candidate | Authorization query cannot be executable yet. |
| Middleware | Route absent from current allowlist | Conditional future `DISCREPANCY` | Route wiring must preserve catalog `DESIGN_*` validation/internal codes. |

## PLAN BEFORE DD AUTHORING

1. Keep the catalog's exact method/path/auth/path type, response/status and 5 declared errors; show explicitly that the catalog has no body contract.
2. Read AC-22 and linked AC-33; record PUT → `UPDATE Content + version` → reload and moderation status evidence. Do not invent version tables/columns from V1-PILOT schema.
3. Propose a simple full-replacement body `{content_type:ContentType!, title:string!, payload:object!}` using API #50's content-bearing request fields. Treat `course_id` as immutable target ownership from stored Content; keep `status`, `parent_id`, `order`, `id` server-managed. Label the entire proposal `DERIVED` and ask confirmation in OPEN_QUESTIONS.
4. Propose each successful update produces a new logical revision, the new revision enters `PENDING_REVIEW`, and a previously published revision remains active until the new revision is approved/published. Label as `DERIVED`; do not claim a physical history mechanism or Content response version field.
5. Candidate Q1 loads Content by `content_id`, then candidate owner/course context for Mentor authorization; legacy `courses.id/mentor_id` is only a DERIVED direct-owner candidate. Missing Content → catalog 404; access denied → catalog 403. Assignment and identity mapping stay SOURCE_REQUIRED.
6. Build API Requirement, Request Usage, Query, Mutation, and Response Source matrices before finalizing sheets. Mutation has logical UPDATE Content + version; physical table/columns, locking, current-revision semantics and transaction mapping are SOURCE_REQUIRED.
7. Cover validation with catalog 422 only. Do not add 409 for concurrency because not declared. Preserve exact 401/403/404/422/500 codes.
8. Create 8 Markdown sheets and 3 reports under `apps/study-server/docs/dd/51_mentor_content_update/`; preserve registered template appendices from current verified #50/template set. No ZIP or runtime/schema/catalog/diagram changes.
9. Immediately verify exact 11-file set, template suffix equality, frontmatter, path-only contract discrepancy, proposed body labeling, Content response fields, code set, JSON syntax, relative links, one-row mapping, code fences and whitespace. Pair-review #50↔#51 lifecycle; mark full AC-22 macro-review pending #52/#53.

### API Requirement Matrix

| Item | Expected | Source/status |
|---|---|---|
| Method/path | `PUT /api/v1/mentor/content/{content_id}` | Catalog + AC-22; DIRECT |
| Actor/auth | Bearer JWT, role Mentor | Catalog; DIRECT |
| Path | `content_id:int64!` | Catalog + AC-22; DIRECT |
| Body | Not declared | Catalog + AC-22; DIRECT omission and DISCREPANCY with update semantics |
| Proposed body | `content_type`, `title`, `payload` full replacement | Reuse #50 content-bearing fields; DERIVED proposal |
| Success | `ApiEnvelope<Content>`, HTTP 200 `DESIGN_RESOURCE_UPDATED` | Catalog + AC-22; DIRECT |
| Errors | 401 auth, 403 access, 404 missing Content, 422 validation, 500 internal | Catalog; DIRECT exact set |
| Mutation | `UPDATE Content + version` | AC-22; DIRECT logical effect, physical model SOURCE_REQUIRED |
| Review transition | New revision proposed PENDING_REVIEW | AC-33 queue + AC-22 update; DERIVED |

### Request Usage Matrix

| Request item | Source/use | Query/mutation/response | Status/gap |
|---|---|---|---|
| Authorization | Header; Bearer + Mentor role | Principal for course permission | Role DIRECT; principal binding SOURCE_REQUIRED |
| `content_id` | Path, int64 required | Q1 target lookup; response `data.id` | DIRECT; malformed-path behavior via middleware needs wiring |
| Proposed `content_type` | Body proposal | M1 logical update; response field | DERIVED; catalog body omission, enum list SOURCE_REQUIRED |
| Proposed `title` | Body proposal | M1 logical update; response field | DERIVED; length/normalization SOURCE_REQUIRED |
| Proposed `payload` | Body proposal | M1 logical update; response field | DERIVED; subtype schema SOURCE_REQUIRED |
| `course_id/status/parent_id/order` | Not proposed as body input | Stored scope/status/tree placement | Keep server-managed; confirm editable field set |

### Query Matrix

| Query ID | Purpose | Type | Candidate source | Columns/condition | Status |
|---|---|---|---|---|---|
| Q1 | Load Content for update | SELECT | Content relation not identified | `id = :content_id` | SOURCE_REQUIRED physical table/columns |
| Q2 | Load owning course/direct owner | SELECT | Legacy `courses AS c` candidate | `c.id = stored.course_id`; read `c.mentor_id` | DERIVED legacy-only; identity/assignment/live schema unresolved |
| Q3 | Load current version/revision | SELECT | No approved version model | Current revision and edit eligibility | SOURCE_REQUIRED; AC-22 only names version effect |

### Mutation Matrix

| Mutation | Logical operation | Target | Fields/effect | Transaction/status |
|---|---|---|---|---|
| M1 | UPDATE existing Content | Content logical entity | Replace `content_type/title/payload`; preserve identity/course/tree fields | AC-22 DIRECT logical intent; physical mapping SOURCE_REQUIRED |
| M2 | Advance/create version | Content version logical state | New revision from full body; preserve earlier revisions | AC-22 DIRECT version effect; exact storage/rules SOURCE_REQUIRED |
| M3 | Set new revision review state | New revision | Candidate `PENDING_REVIEW`; preserve prior published revision | DERIVED; confirm with #52 and AC-33 |

### Response Source Matrix

| Response field | Source/candidate | Rule/status |
|---|---|---|
| Envelope `success/businessCode/message/data/meta/traceId` | Study envelope convention + catalog | 200 `DESIGN_RESOURCE_UPDATED`; message exact text open |
| `data.id` | Existing Content identified by path | Preserve ID; physical projection SOURCE_REQUIRED |
| `data.course_id` | Stored Content | Preserve course ownership; SOURCE_REQUIRED mapping |
| `data.content_type/title/payload` | Proposed request body | Return accepted/current revision; body proposal DERIVED, schema SOURCE_REQUIRED |
| `data.status` | Proposed lifecycle | `PENDING_REVIEW` for new revision; DERIVED pending confirmation |
| `data.parent_id/order` | Stored tree placement | Preserve in this API proposal; physical mapping/immutability SOURCE_REQUIRED |
| Version metadata | No Content response field exists | Version effect is not exposed in Content schema; keep internal and SOURCE_REQUIRED |

## CHANGES

- Files changed: `apps/study-server/docs/dd/51_mentor_content_update/` (8 sheets + 3 reports) and this worklog.
- CONTEXT_UPDATES: None planned; only documentation changes.
- Context pages changed: None.
- Assumptions: Use only existing Content fields for a body proposal; full replacement is DERIVED. New revision review flow is DERIVED. Keep all physical version data, schema, concurrency and access identity unresolved where source is absent.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector + read of 3 selected logs | #48, #49, #50 read in full. | COMPLETE |
| AC-22/AC-33, API catalog, DDL/current source | Inspected for API #51 intent and current absence. | COMPLETE |
| Targeted DD contract/template/matrix validation | Exact catalog path/body discrepancy, codes, all Content fields, template appendix tails, relative links, JSON, Markdown tables, fences, whitespace and pre-report manifest passed. | VERIFIED |
| `git diff --check` | No diagnostics. | VERIFIED |
| `deno run --allow-read scripts/validate-contracts.mjs` | Could not start because `ajv/dist/2020.js` is not a declared Deno dependency; `node`/`nodejs` unavailable. DD-specific checks were performed directly. | DECLARED_NOT_RUNNABLE |

## HANDOFF

- Remaining blockers: Body contract approval, version model/storage, review/publication transition, Content schema, Mentor principal/assignment and concurrency behavior.
- Next owner/action: API #51 DD was statically verified and is now macro-reviewed with #49–#53; request-body/version/review proposals remain open. Continue at API #54.

## GROUP_MACRO_REVIEW

- Status: VERIFIED_WITH_OPEN_QUESTIONS after API #53 was created.
- Cross-API findings: #49 tree cardinality/visibility remains unresolved; #50/#51 PENDING_REVIEW and tree placement are DERIVED; #52 publication transitions remain DERIVED and AC-33 APPROVED/PUBLISHED is ambiguous; #53 proposes direct-child blocking, no cascade, unpublish-first for PUBLISHED, and history-preserving soft delete.
- Shared blockers: generic Content/version schema, payload/enums/readiness, Mentor principal/assignment, dependency coverage, soft-delete/audit storage, and filtering deleted items from active tree/review queue.
- Application tests were not run; this records document-level macro-review only.
