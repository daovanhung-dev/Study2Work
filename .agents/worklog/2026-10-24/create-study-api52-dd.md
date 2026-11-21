---
task_id: "2026-10-24-create-study-api52-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #52 — Publish/unpublish Content

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `available:72`, `selected:3`, `status:READY`, shortage `none`.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ contract catalog; Mentor identity, Content schema và live DB chưa xác minh; không gộp Content với Lecture; Study chỉ giao Markdown.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: AC-22 Content tree và Content schema/payload/enums chưa có persistence mapping; giữ `SOURCE_REQUIRED`, không tạo query giả.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: #50 tạo Content; `PENDING_REVIEW` và root/order là đề xuất `DERIVED`; không có bảng generic Content tương thích trong DDL.
  - path: `.agents/worklog/2026-10-24/create-study-api51-dd.md` (đọc thêm vì là API liền kề)
    - carry_forward: #51 cập nhật `Content + version`; body/revision lifecycle là `DERIVED`; AC-33 `APPROVED/PUBLISHED` còn mơ hồ khi #52 xử lý publication riêng.
  - path: `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md` (đọc thêm vì yêu cầu đếm)
    - carry_forward: Catalog có 103 ID; định nghĩa đếm source là route method/path khớp catalog và có module view; cập nhật baseline mới sau phiên này.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD tiếng Việt cho API #52, lập plan trước authoring, đọc AC-22/AC-33 cùng DD #49–#51, phân biệt contract trực tiếp với suy luận, static verify ngay sau authoring.
- Canonical contract: `docs/lists/list_api.md` row #52: `PATCH /api/v1/mentor/content/{content_id}`, Bearer JWT role Mentor, `path{content_id:int64!}`, response `ApiEnvelope<Content>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`, errors chính xác 401/403/404/422/500 với các `DESIGN_*` codes tương ứng.
- Diagram: AC-22 PATCH → `UPDATE publication status` → reload content tree. AC-33 queue yêu cầu `PENDING_REVIEW`; approval node ghi `APPROVED/PUBLISHED + audit`, nhưng không phân tách approval với publication.

## CURRENT_BEHAVIOR

- Source/config: Search hiện tại không thấy API #52 route/module/test; `DESIGN_CONTRACT_PATHS` chưa có mentor content path. Router có 12 unique catalog API IDs source-backed (#01–#09, #12–#14); #08/#09 chưa được runtime-verified sau merge.
- DD inventory: tại lúc nhận yêu cầu có 51 folder (#01–#51), 52 thiếu; sau khi hoàn tất #52 có 52 folder đủ 8 sheet cốt lõi, 51 thiếu (#53–#103). Có 40 full 11-artifact packs; #01–#12 còn thiếu ba report.
- Programming inventory: So khớp exact method/path trong catalog với `app/api/v1.py` và module view cho 12/103 IDs; 91 chưa có route+view pair. `/auth/refresh`, `/hello`, `/test/db` là source route không khớp catalog ID riêng. Đây là source inventory, không đồng nghĩa runtime pass.
- Schema: Legacy `infra/postgres/study-server/DB.sql` không có generic Content/version table; V1-PILOT `content_blocks` có UUID, `lesson_id`, `block_type`, `content_json`, khác model BIGINT `Content`. Live schema chưa xác minh.
- Runnable tests: Không chạy; task docs-only và không có test #52 trong source.
- Runtime wiring: API #52 `UNWIRED / NOT_FOUND`; current middleware allowlist không có path này.

## SOURCE_TRACE

```text
Mentor Bearer principal -> PATCH content_id (+ proposed target state) -> load logical Content/current publication state + course authorization -> readiness validation before publish -> UPDATE publication state -> return ApiEnvelope<Content> -> AC-22 client reloads content tree
```

Physical relations, current-version selection, Mentor identity mapping and readiness fields remain `SOURCE_REQUIRED`.

## PLAN BEFORE DD AUTHORING

1. Preserve exact catalog method/path, actor/auth, path type, response, HTTP success and error-code set. Record that catalog and AC-22 diagram declare no body or query.
2. Propose `{published:boolean!}` as an explicitly `DERIVED` request field so the client specifies a target state instead of an ambiguous toggle. Do not represent it as approved contract; no other field/body is proposed.
3. Use AC-33's directly named states as evidence, not as a complete enum. Proposed logical transitions: `APPROVED → PUBLISHED` only after readiness passes; `PUBLISHED → APPROVED` for unpublish; same target state is a no-op; `PENDING_REVIEW`, `REJECTED`, and other unconfirmed states do not transition and map to catalog 422. All transition semantics are `DERIVED` and need macro-review.
4. Readiness's exact required ContentType/payload/assets/metadata checks remain `SOURCE_REQUIRED`; do not invent enum members, required fields, tables, columns or response fields.
5. Query matrix uses logical Content/state lookup and authorization/readiness checks only. Physical Content/version/current-state relations are `SOURCE_REQUIRED`; legacy `courses.mentor_id` is only a `DERIVED` direct-owner candidate and does not cover assigned Mentor or identity mapping.
6. Mutation matrix describes publication-status update only, matching AC-22. Propose no Content revision/version creation for publish/unpublish (`DERIVED` separation from #51); physical transaction and status storage remain open.
7. Response Source Matrix covers envelope and every reusable Content field. Return stored content fields unchanged, with `data.status` reflecting resulting logical state; do not add `is_published` or version fields to response.
8. Record discrepancies: missing body for a two-direction operation; AC-33 approve `APPROVED/PUBLISHED` ambiguity; missing generic Content schema; Mentor identity/access source missing; #52 absent from middleware allowlist.
9. Create exact 8 template sheets plus `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md` in `apps/study-server/docs/dd/52_mentor_content_publish/`; no ZIP, runtime/schema/catalog/diagram change.
10. Immediately check exact 11-file set, template appendix byte equality, catalog/error set, all 8 Content fields, `published` proposal labeling, state references, JSON, links, Markdown tables/fences/whitespace and `git diff --check`. Update this worklog and count worklog after verification.

### API Requirement Matrix

| Item | Expected | Basis/status |
|---|---|---|
| Method/path | `PATCH /api/v1/mentor/content/{content_id}/publish` | Catalog + AC-22; DIRECT |
| Actor/auth | Bearer JWT; role Mentor | Catalog; DIRECT |
| Path | `content_id:int64!` | Catalog + AC-22; DIRECT |
| Canonical body/query | Not declared | Catalog + AC-22; DIRECT omission |
| Proposed target | `published:boolean!` | Needed to express both actions without a blind toggle; DERIVED proposal |
| Success | HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<Content>` | Catalog + AC-22; DIRECT |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR` | Catalog; exact set DIRECT |
| Logical mutation | Update publication status, then reload tree | AC-22; DIRECT effect |

### Request Usage Matrix

| Request item | Source/use | Effect | Status |
|---|---|---|---|
| Authorization | Bearer token; require Mentor role and course-management permission | Principal for stored Content/course access | Role DIRECT; identity/assignment SOURCE_REQUIRED |
| `content_id` | Required int64 path | Locate logical Content and response `data.id` | DIRECT; physical lookup SOURCE_REQUIRED |
| Body | Not declared in catalog or diagram | None in canonical contract | DIRECT omission |
| Proposed `published` | Proposed required boolean target state | Select publish vs unpublish branch | DERIVED; request contract confirmation required |
| Query parameters | None declared | None | DIRECT omission |

### Query Matrix

| Query | Logical purpose | Required data | Physical source/status |
|---|---|---|---|
| Q1 | Load Content and current publication/review state by `content_id` | Content fields needed for response, `course_id`, current state/revision | Generic Content/version relation `SOURCE_REQUIRED` |
| Q2 | Check Mentor access to stored course | Course owner/assignment and principal key | Legacy `courses.id/mentor_id` is only DERIVED candidate; identity and assignment SOURCE_REQUIRED |
| Q3 | Validate readiness before transition to published | Approved state and type-specific completeness | `APPROVED`/`PUBLISHED` are diagram terms; exact readiness fields/rules and storage SOURCE_REQUIRED |

### Mutation Matrix

| Branch | Proposed precondition | Logical effect | Status |
|---|---|---|---|
| `published=true` | Current logical state `APPROVED`; readiness passes | Set publication state to `PUBLISHED` | DERIVED; exact state storage SOURCE_REQUIRED |
| `published=false` | Current logical state `PUBLISHED` | Return to `APPROVED`, retaining approval | DERIVED; review/publication coupling needs confirmation |
| Target already matches current state | Same desired state | No-op; return current Content | DERIVED idempotency proposal |
| Pending/rejected/other state | Not eligible for proposed transition | No mutation; catalog 422 | DERIVED; complete enum SOURCE_REQUIRED |
| Version/content body | N/A | No content revision or payload change proposed | DERIVED from AC-22 publication-status-only step; physical model SOURCE_REQUIRED |

### Response Source Matrix

| Response field | Source/projection | Status/gap |
|---|---|---|
| Envelope `success` | Success/error branch | Study convention; actual endpoint absent |
| `businessCode` | Catalog literal | DIRECT: `DESIGN_RESOURCE_UPDATED` |
| `message` | Safe application text | Wording unspecified; DERIVED |
| `data.id` | Target Content by path | Logical target DIRECT; physical mapping SOURCE_REQUIRED |
| `data.course_id` | Stored Content | SOURCE_REQUIRED physical mapping |
| `data.content_type` | Stored Content | Enum/source mapping SOURCE_REQUIRED |
| `data.title` | Stored Content | SOURCE_REQUIRED physical mapping |
| `data.payload` | Stored Content | Structure/source mapping SOURCE_REQUIRED |
| `data.status` | Resulting publication/review state | APPROVED/PUBLISHED are diagram terms; enum and target semantics DERIVED/SOURCE_REQUIRED |
| `data.parent_id` | Stored Content | Optional null/omit policy and physical mapping SOURCE_REQUIRED |
| `data.order` | Stored Content | SOURCE_REQUIRED physical mapping |
| `meta` | Envelope | No pagination contract; helper alignment required |
| `traceId` | Request trace | Study envelope convention; endpoint absent |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Body for publish/unpublish | Catalog and AC-22 list only path; purpose requires both directions | `DISCREPANCY`; proposed body `DERIVED` | Confirm target-state input before implementation |
| Approval/publication | AC-33 says `APPROVED/PUBLISHED + audit`; AC-22 provides separate #52 | `DISCREPANCY / MACRO_REVIEW` | State transitions cannot be canonicalized yet |
| Readiness | Catalog purpose names readiness, no criteria/schema | `SOURCE_REQUIRED` | Validation details remain open |
| Runtime/schema/auth | No route/module/test, generic Content DDL absent, Mentor guard absent | `UNWIRED / NOT_FOUND / SOURCE_REQUIRED` | Design-only; no executable persistence/auth claim |
| Error wiring | `/mentor/content/{content_id}/publish` absent from middleware allowlist | `CONDITIONAL_FUTURE_DISCREPANCY` | Future wiring needs exact `DESIGN_*` mapping |

## CHANGES

- Files changed: `apps/study-server/docs/dd/52_mentor_content_publish/` (8 sheets + 3 reports); this worklog; refreshed `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`.
- CONTEXT_UPDATES: None; documentation-only API design.
- Context pages changed: None planned.
- Assumptions: `{published:boolean!}`, state transition and same-state no-op are proposals explicitly marked `DERIVED`; readiness rules and physical schema are not invented.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector | Deno selector returned #48, #49, #50; 72 matching worklogs, no shortage. | `VERIFIED` |
| Prior worklog review | #48, #49, #50 read fully; #51 and count inventory reviewed as related context. | `VERIFIED` |
| Diagram/catalog/schema/source pre-read | AC-22 and AC-33 nodes/edges, #52 row, Content schema, route absence, allowlist and DDL mismatch inspected. | `VERIFIED_STATIC_ONLY` |
| DD authoring | Created 8 registered template sheets and 3 reports; all eight appendix tails byte-match the registered templates. | `VERIFIED` |
| Contract/content/error checks | Exact catalog 200 success + 401/403/404/422/500 codes; all eight Content response fields and body-omission discrepancy covered. | `VERIFIED_STATIC_ONLY` |
| Markdown integrity | Exact 11-file manifest; JSON examples parse; local links resolve; table widths, fences and whitespace pass; untracked DD files checked separately. | `VERIFIED` |
| `git diff --check` | No diagnostics. | `VERIFIED` |
| Source/runtime boundary | No API #52 route/module/test found; middleware path absent. No application tests run because API #52 is unwired and task is docs-only. | `VERIFIED_STATIC_ONLY / NOT_RUN` |
| Inventory after task | 103 catalog endpoints; 52 DD folders, 51 missing; 12 route+view source implementations, 91 without. | `VERIFIED_STATIC_ONLY` |
| `node scripts/validate-agent-context.mjs` | Exit 1 `AGENT_CONTEXT_INVALID`; repository reports missing registered db-admin pages/links and broad pre-existing source drift, including server-study. No context page or unrelated scope was changed in this docs task. | `PRE_EXISTING_REPOSITORY_FAILURE` |
| AC-22/AC-33 macro-review | #49–#53 linked lifecycle/tree/delete reviewed; unresolved decisions retained. | `VERIFIED_WITH_OPEN_QUESTIONS` |

## HANDOFF

- Remaining blockers: Confirm request target-state field, readiness criteria, approval-to-publication lifecycle, Content/version persistence, Mentor identity/assignment and live schema.
- Next owner/action: API #52 DD was statically verified and is now macro-reviewed with #49–#53; approval/publication and transition proposals remain open. Continue at API #54.

## GROUP_MACRO_REVIEW

- Status: VERIFIED_WITH_OPEN_QUESTIONS after API #53 was created.
- Cross-API findings: #49 tree cardinality/visibility remains unresolved; #50/#51 PENDING_REVIEW and tree placement are DERIVED; #52 publication transitions remain DERIVED and AC-33 APPROVED/PUBLISHED is ambiguous; #53 proposes direct-child blocking, no cascade, unpublish-first for PUBLISHED, and history-preserving soft delete.
- Shared blockers: generic Content/version schema, payload/enums/readiness, Mentor principal/assignment, dependency coverage, soft-delete/audit storage, and filtering deleted items from active tree/review queue.
- Application tests were not run; this records document-level macro-review only.
