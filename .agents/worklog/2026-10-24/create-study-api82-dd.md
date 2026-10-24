---
task_id: "2026-10-24-create-study-api82-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #82 — Lấy danh sách lesson

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` (`node` không có trong PATH)
- selected worklogs:
  - `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ contract catalog; tách `DIRECT`/`DERIVED`/`SOURCE_REQUIRED`; chỉ lập luận truy vấn khi có bảng/cột chứng minh.
  - `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Review diagram và các DD cùng flow; không đoán schema/response semantics khi catalog và sơ đồ khác nhau.
  - `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: API #82 là phần tiếp theo trong catalog; inventory count là source/wiring evidence, không phải runtime proof.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo một DD Markdown tiếng Việt cho API #82; lập plan và bốn ma trận trước khi tạo thư mục DD; đọc trọn AC-34 cùng DD admin liên quan; kiểm tra package ngay sau authoring.
- Canonical contract/approved DD: `docs/lists/list_api.md` row #82 khai báo `GET /api/v1/admin/lessons`, Bearer JWT/Admin, query `course?:int64`, `status?:string`, `type?:string`, response `ApiEnvelope<Lesson>`, 200 `DESIGN_RESOURCE_RETRIEVED`, errors 401/403/500.

## CURRENT_BEHAVIOR

- Source/config: `apps/study-server/app/api/v1.py` hiện chỉ có route IDs #01–#09, #12–#14; không có `/admin/lessons`. Không có module/test API #82. Shared auth helper chỉ xác thực Student; Admin guard chưa có.
- Runnable tests: Docs-only; không chạy application tests.
- Runtime wiring: `UNWIRED / NOT_FOUND` theo current source scan; không phải runtime test result.

## SOURCE_TRACE

```text
Admin Bearer principal -> GET /api/v1/admin/lessons với query tùy chọn -> xác định query/filter/status theo AC-34 -> đọc logical Lesson/candidate schema -> map ApiEnvelope<Lesson> -> trả success hoặc lỗi catalog -> Admin lesson workflow tiếp tục
```

## PLAN BEFORE DD AUTHORING

### Evidence read before authoring

- Catalog `docs/lists/list_api.md`: API #82 and reusable `Lesson`; direct auth/role/query/response/status/error declarations recorded above.
- AC index `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md`, AC-34; full AC-34 node/edge flow in `AC_04_ADMIN_MANAGEMENT.drawio`: Admin opens list, #82 reads lessons, then detail/update/status/delete and reload. Permission precondition is lesson management. No filter semantics, ordering, pagination or type mapping is shown.
- Relevant DDs: #73 Admin list precedent and #78 Admin content queue, plus #81 linked AC-33 report. These show prior unresolved list-vs-singleton cardinality; pagination proposals from other endpoints are not transferred because #82 declares no page query.
- Source: current router, Student auth helper, middleware design-contract paths, API #09 lesson model/query/view as a public-curriculum field-mapping precedent only.
- Schema artifacts: legacy `DB.sql` `lessons` BIGINT table; `DB_UNICA_TABLES.md`; ERD relations; V1-PILOT `lessons` UUID/versioned model. Live schema is not verified. Legacy DDL permits nullable `course_id` while logical reusable `Lesson.course_id` is required.
- Current source search: no #82 route, Admin lessons module, or focused test; no compatible Lesson `type` column is evidenced in either schema artifact.

### API Requirement Matrix

| Requirement | Evidence | Class | DD treatment |
|---|---|---|---|
| `GET /api/v1/admin/lessons` | Catalog #82 | DIRECT | Retain exact method/path. |
| Bearer JWT, role Admin | Catalog #82 | DIRECT | Require authentication and Admin role; concrete claims/guard are SOURCE_REQUIRED. |
| Lesson-management permission | AC-34 precondition | DIRECT | Record permission gate; policy source/permission identifier are SOURCE_REQUIRED. |
| Optional `course:int64` | Catalog #82 | DIRECT field; physical predicate DERIVED | Candidate exact match on logical `course_id`; query against candidate schema only. |
| Optional `status:string` | Catalog #82 | DIRECT field; exact match DERIVED | If supplied, candidate equality; if absent, show all statuses for Admin management. Do not use public API #09 `PUBLISHED` restriction. |
| Optional `type:string` | Catalog #82 | DIRECT field; behavior SOURCE_REQUIRED | No Lesson type field is in reusable schema or inspected DDL; do not ignore or map to content-block type. |
| Success `200 DESIGN_RESOURCE_RETRIEVED` | Catalog #82 | DIRECT | Keep exact code. |
| Errors 401/403/500 with catalog codes | Catalog #82 | DIRECT | Keep exact set; no 422 or other business code is added. |
| Response `ApiEnvelope<Lesson>` | Catalog #82 | DIRECT, conflicts with list intent | Preserve in contract row; show collection as a DERIVED proposal only and leave owner confirmation open. |
| List semantics | Endpoint name + AC-34 “query lessons” and management flow | DIRECT intent; shape DERIVED | Candidate `ApiEnvelope<Lesson[]>`; no pagination because no page/size query or Page response is declared. |
| Default order | API #09 query precedent and sortable lesson fields | DERIVED | Candidate `course_id ASC, sort_order ASC, id ASC`; owner confirmation required. |
| Legacy vs pilot storage | `DB.sql`, `02_study_db.sql`, diagrams | DISCREPANCY / SOURCE_REQUIRED | Do not merge BIGINT legacy and UUID/versioned pilot models. Mark legacy mapping as a candidate only. |

### Request Usage Matrix

| Input | Intended use | Validation/effect | Status |
|---|---|---|---|
| `Authorization` Bearer JWT | Authenticate request | Missing/invalid token -> catalog 401 | DIRECT; current Admin guard absent |
| Admin role + lesson-management permission | Authorize list read | Deny -> catalog 403; check before DB query | DIRECT from catalog/AC-34; implementation SOURCE_REQUIRED |
| `course` | Restrict lessons to course | Candidate exact match `course_id = :course` | DERIVED physical mapping |
| `status` | Restrict by status when supplied | Candidate exact equality; omitted means no status predicate | DERIVED; enum/casing unknown |
| `type` | Intended type filter | Cannot implement until compatible Lesson type source is identified | SOURCE_REQUIRED; do not silently ignore |
| Query/body/path fields not in catalog | None | No body, path ID, pagination, page size or sort parameter | DIRECT absence from declared request |

### Query Matrix

| Step | Candidate operation | Inputs/outputs | Evidence and limits |
|---|---|---|---|
| 0 | Authenticate Admin and lesson-management permission | Bearer JWT / principal | Catalog + AC-34; guard/claim source absent. |
| 1 | Parse declared optional query fields | `course`, `status`, `type` | Types direct; detailed range/enum validation not specified. `type` blocks full implementation pending mapping. |
| 2 | Read candidate lesson rows | `lessons` fields mapped to reusable Lesson | Legacy BIGINT mapping only: `name -> title`, `sort_order -> order`; candidate, not live schema. Apply course/status filters only under stated derived semantics. |
| 3 | Stable ordering | `course_id`, `sort_order`, `id` | DERIVED proposal informed by API #09 sort order; no catalog sort input. |
| 4 | Map success envelope | Lesson collection proposal | Cardinality discrepancy: direct `Lesson` vs list intent. Candidate array only; no Page/pagination. |
| 5 | Return response | exact 200 or catalog 401/403/500 | Middleware/error helper currently do not prove catalog code behavior for an unwired Admin route. |

### Mutation Matrix

| Table/resource | Operation | Reason |
|---|---|---|
| `lessons` | None — read only | GET list; AC-34 makes later update/status/delete separate APIs #84–#86. No audit write is assigned to #82. |

### Response Source Matrix

| Response field | Logical source | Candidate mapping | Status/rule |
|---|---|---|---|
| `success`, `businessCode`, `message`, `data`, `meta`, `traceId` | ApiEnvelope contract/current middleware conventions | Exact envelope field contract; data cardinality unresolved | Envelope shape DIRECT; current helper uses `{}` on errors while guideline says `null`, a future integration discrepancy. |
| `id` | legacy `lessons.id` | `id` | Candidate BIGINT mapping. |
| `course_id` | legacy `lessons.course_id` | `course_id` | Required by reusable Lesson but nullable in legacy DDL; mapping gap remains open. |
| `title` | legacy `lessons.name` | `name AS title` | Candidate alias; API #09 source precedent. |
| `content` | legacy `lessons.content` | direct | Optional; preserve NULL as null if collection contract is approved. |
| `video_url` | legacy `lessons.video_url` | direct | Optional URI field; validate/serialization convention not established here. |
| `order` | legacy `lessons.sort_order` | `sort_order AS order` | Candidate alias; API #09 source precedent. |
| `status` | legacy `lessons.status` | direct | Status enum members/casing unresolved; do not invent whitelist. |
| `type` | No compatible Lesson field found | None | Query behavior SOURCE_REQUIRED; not part of reusable Lesson response. |
| list cardinality | AC-34 list intent | `Lesson[]` candidate | DERIVED proposal conflicts with direct `Lesson`; no Page wrapper. |

### Pre-authoring decisions

1. Keep this DD `Draft — Needs Confirmation`.
2. Keep the catalog's singular `ApiEnvelope<Lesson>` as the direct contract and document a clearly marked `ApiEnvelope<Lesson[]>` proposal for list semantics; request owner resolution rather than choosing silently.
3. Do not add pagination fields/query inputs or error codes absent from catalog.
4. Record `type` as `SOURCE_REQUIRED`, since no compatible field exists in either inspected schema artifact.
5. Present the legacy mapping only as candidate mapping; explicitly flag nullable legacy `course_id`, incompatible V1-PILOT UUID schema, Admin guard gap, status enum/casing, and error `data` discrepancy.
6. Create the 8 template sheets plus `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md` after this plan is complete.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Admin lesson contract vs collection intent | Catalog #82 says `ApiEnvelope<Lesson>`; AC-34 and operation name describe querying lessons | `DISCREPANCY` | Preserve direct response; label `Lesson[]` as proposal; owner confirmation required. |
| `type` query | Catalog has field; reusable Lesson and inspected DDL do not define compatible type | `SOURCE_REQUIRED` | Do not omit filter silently or map it to content-block type. |
| Legacy and V1-PILOT lesson storage | BIGINT `lessons` vs UUID chapter/version model | `DISCREPANCY / SOURCE_REQUIRED` | Candidate field mapping cannot be claimed as active schema. |
| `course_id` nullability | Legacy DDL nullable; reusable Lesson requires int64 | `DISCREPANCY` | Rows with NULL cannot map to declared Lesson. |
| Admin authorization | Catalog/AC-34 require Admin + management permission; current helper is Student-only | `SOURCE_REQUIRED` | No current source-backed Admin guard. |
| Runtime implementation | Current router/module/test scan | `UNWIRED / NOT_FOUND` | No API #82 implementation source found. |

## CHANGES

- Files changed: `apps/study-server/docs/dd/82_admin_lessons_list/` (11 Markdown files), this worklog, and `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`.
- CONTEXT_UPDATES: None planned; no runtime/schema/catalog/diagram edits.
- Context pages changed: None planned.
- Assumptions: Keep every behavior outside the diagram and catalog explicitly labeled `DERIVED` or `SOURCE_REQUIRED`; retain Draft status while material contract gaps remain.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog preflight | Deno selector selected #48/#49/#50; all three were read fully; no shortage. | VERIFIED |
| Diagram/catalog/schema/source review | Catalog #82 + Lesson, full AC-34 diagram/index, #73/#78/#81 DD references, current router/auth/middleware, legacy and V1-PILOT schema artifacts reviewed. | VERIFIED_STATIC |
| Pre-authoring matrices | Requirement, request usage, query, mutation, response source matrices and decision list recorded above before DD directory creation. | VERIFIED |
| Static DD validation | Exact 11-file package; 8/8 template appendix parity; 3 JSON examples parsed; 29 tables consistent; 14 fences balanced; 32 local links/anchors resolve; final newline/trailing whitespace clean; `git diff --check` clean. | PASS — STATIC |
| Current inventory | 103 catalog API IDs; 82 DD folders / 21 missing; 70 complete 11-file packages / 12 core-only; 12 route-plus-view source pairs / 91 without. | VERIFIED_STATIC_ONLY |
| Application tests | Not planned; documentation-only. | NOT_RUN |

## HANDOFF

- Remaining blockers: Contract cardinality, `type` mapping, deleted-lesson visibility, Admin guard, active schema choice/course nullability, status enum/casing and error-envelope behavior need owner/source confirmation.
- Next owner/action: AC-34 macro-review is complete; continue the DD sequence at API #87 in the next API-DD session.

## GROUP_MACRO_REVIEW — AC-34 #82–#86

- Status: `VERIFIED_WITH_OPEN_QUESTIONS`; document-level review recorded in `apps/study-server/docs/dd/86_admin_lesson_delete/VERIFICATION_REPORT.md`.
- Findings carried into #82: keep direct `ApiEnvelope<Lesson>` vs list intent and `type` mapping open; do not add a deleted-item filter until #86's marker/visibility policy is selected. AC-34 mutations #84–#86 reload through #82.
- No API approval, route implementation, live schema check or application test is implied by this review.
