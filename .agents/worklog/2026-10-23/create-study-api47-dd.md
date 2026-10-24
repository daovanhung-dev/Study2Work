---
task_id: "2026-10-23-create-study-api47-dd"
date: "2026-10-23"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Create Study API #47 DD

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3` (`node` unavailable)
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-23/create-study-api41-dd.md`
    - carry_forward: Preserve exact catalog contract; use `DERIVED` only for simple unsupported behavior; keep source/schema contradictions open and do not invent counter/table fields.
  - path: `.agents/worklog/2026-10-23/create-study-api42-dd.md`
    - carry_forward: DDs remain source-aware drafts; schema/title gaps and runtime `UNWIRED` status stay separate; macro-review connected APIs only when the group exists.
  - path: `.agents/worklog/2026-10-23/create-study-api43-dd.md`
    - carry_forward: Keep request/query/mutation/response-source matrices before authoring; do not equate similarly named fields without evidence; report the exact current-source boundary.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Create a Vietnamese, source-aware Markdown DD for Study API #47, then immediately validate its contract, source mappings, document structure and links.
- Canonical contract/approved DD: `docs/lists/list_api.md` API #47 and reusable `Lecture`/`UploadAsset` schemas; AC-21 index and activity diagram; legacy Study DB artifacts and the distinct V1-PILOT DDL; related DDs #46, #34, #9 and #11; registered `createDD-markdown` skill and Study Markdown-only workflow.

## CURRENT_BEHAVIOR

- Source/config: The catalog declares `POST /api/v1/mentor/courses/{course_id}/lectures`, Mentor Bearer auth, path `course_id:int64!`, body `title:string!`, `content:int64!`, `asset refs:string!`, `order:int32!`, response `ApiEnvelope<Lecture>`, HTTP 201 `DESIGN_RESOURCE_CREATED`, and exactly 401/403/404/422/500 errors. AC-21 links #46 → #34 upload/Object Storage → #47 insert Lecture/Content → #48 reload. Current router search has no API #47/mentor lecture route; no #47 module or Python test source exists. The legacy DDL has `courses`, `lessons`, `resources`; no `lectures`, `contents` or `uploads` table. Live schema is not verified.
- Runnable tests: Not run; documentation-only task.
- Runtime wiring: `UNWIRED / NOT_FOUND` for API #47. Current shared JWT guard is Student-specific; no Mentor guard is wired.

## SOURCE_TRACE

```text
Mentor UI selects a course -> API #34 stores media in Object Storage and returns UploadAsset (its durable ID/metadata source is unresolved) -> API #47 authenticates Mentor and checks course access -> candidate legacy lookup of course -> candidate INSERT into lessons -> return Lecture (assets projection remains SOURCE_REQUIRED) -> API #48 reloads detail
```

## PLAN BEFORE DD AUTHORING

1. Preserve the catalog contract verbatim: method/path, role, required path/body fields, response schema, HTTP 201 and the exact 401/403/404/422/500 business-code set. Do not add request fields or status codes.
2. Read the full AC-21 actor/precondition/flow and distinguish AC-22 `Content`, which is a separate Mentor content workflow. Keep the diagram phrase `INSERT Lecture/Content` visible as ambiguous; do not invent a physical Content table or combine it with AC-22.
3. Use legacy `lessons` as a `DERIVED` logical Lecture candidate only: `course_id → lessons.course_id`, `title → lessons.name`, `order → lessons.sort_order`, `content → lessons.content` only as a provisional decimal-string conversion, and `status` omitted from INSERT to use legacy default `DRAFT`. Use database current time for required `created_at`/`updated_at` as a candidate. Keep the int64/string/TEXT discrepancy and enum uncertainty open.
4. Align course access with API #46's candidate direct-owner predicate `courses.mentor_id = current numeric Mentor ID`, without adding a `PUBLISHED` gate. AC-21 also permits assigned courses, but no assignment relation or Mentor principal ID mapping is source-confirmed; label direct ownership `DERIVED`, leave assignment support `SOURCE_REQUIRED`, return 404 for a missing course and candidate 403 for an existing inaccessible course.
5. Treat `asset refs` as an opaque required catalog field. A provisional wire key `asset_refs` may be shown only as `DERIVED`; do not parse an unspecified format, trust client URLs, create an uploads table, or insert `resources` without a confirmed asset resolver. API #34 has no durable asset ID/metadata mapping; `Lecture.assets: UploadAsset[]` is required and cannot yet be sourced, so mark response completion blocked by `SOURCE_REQUIRED`.
6. Preserve the legacy BIGINT schema and V1-PILOT UUID/versioned schema as separate candidates. Do not map legacy `course_id:int64` to pilot `course_versions`/`content_blocks`/`file_objects`; live schema selection remains open.
7. Record the API guideline/current helper discrepancy: guideline error envelope uses `data:null`, current `error_response()` defaults to `{}`. Keep the expected and current forms separate; do not claim API #47 runtime behavior.
8. Create `apps/study-server/docs/dd/47_mentor_lectures_create/` from the registered Markdown templates: eight sheet positions with a single `07_lessons_insert.md` mapping for the only candidate committed write, plus `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`. Do not create a ZIP or modify runtime, catalog, diagrams or schema.
9. Immediately validate exact catalog contract/error codes, matrix coverage, every request/response field, mutation-to-mapping references, per-column rows, template structure/appendices/front matter, JSON examples, relative links, table widths, status labels and whitespace. Keep macro review of #46–#48 pending until #48 DD exists.

### API Requirement Matrix

| API ID | Method / endpoint | Actor / auth | Request | Response / status | Rules, effects and gaps | Folder / status |
|---|---|---|---|---|---|---|
| #47 | `POST /api/v1/mentor/courses/{course_id}/lectures` | Mentor / Bearer JWT | `course_id:int64!`; `title:string!`; `content:int64!`; `asset refs:string!`; `order:int32!` | `ApiEnvelope<Lecture>`; 201 `DESIGN_RESOURCE_CREATED`; errors exactly 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR` | AC-21; candidate direct-owner check and legacy `lessons` insert; content and asset projection need confirmation; no publish behavior inferred | `47_mentor_lectures_create`; `Draft — Needs Confirmation` |

### Request Usage Matrix

| Request field | Source | Data Mapping step | Validate | SQL/mutation usage | Branch / response usage | Gap |
|---|---|---|---|---|---|---|
| `Authorization` | Header | `0` | Valid Bearer JWT and Mentor role per catalog | Principal supplies candidate `mentor_id`; do not accept a mentor ID from body | 401 if missing/invalid; 403 if role/access denied | Current shared guard only supports Student; Mentor claim-to-numeric-user mapping is unresolved |
| `course_id` | Path | `1`, `2` | Parse `int64`; no positive-only rule added | Q1 `courses.id = :course_id`; M1 `lessons.course_id` | `Lecture.course_id`; missing course → candidate 404 | Legacy BIGINT versus pilot UUID schema and live schema unresolved |
| `title` | Body catalog label | `1`, `4` | Required string; max 200 only as `DERIVED` from legacy `lessons.name VARCHAR(200)`; no inferred minimum | M1 `lessons.name` | `Lecture.title` via name alias | Wire naming is direct only for this field; physical mapping is legacy candidate |
| `content` | Body | `1`, `4` | Required `int64`; no positivity or range beyond type | Candidate decimal-string conversion to `lessons.content TEXT` | `Lecture.content?:string` | `DISCREPANCY`: could be content ID, not body text; conversion is not approved |
| `asset refs` | Body catalog phrase | `1`, pending asset-resolution step | Required string; preserve opaque value; provisional wire key `asset_refs` is `DERIVED` only | No committed DB mutation until reference format and resolver are defined | `Lecture.assets[]` needs full `UploadAsset` records | API #34 has no source-backed persistence/lookup; do not invent parser/table/URL trust |
| `order` | Body | `1`, `4` | Required `int32`; no positivity rule inferred | M1 `lessons.sort_order` | `Lecture.order` | Legacy INT is a candidate physical mapping |

### Query Matrix

| Query ID | Purpose | Type | Candidate base table | Columns / predicates | Result / branch | Evidence |
|---|---|---|---|---|---|---|
| Q1 | Resolve course and candidate owner | SELECT | `courses AS c` | `c.id` | `c.id = :course_id`; no row → candidate 404 | Legacy DDL direct |
| Q1 | Compare candidate direct owner | SELECT | `courses AS c` | `c.mentor_id` | `c.id = :course_id`; compare with authenticated Mentor principal; mismatch → candidate 403 | Direct ownership `DERIVED`; assignment access `SOURCE_REQUIRED` |
| Q2 | Resolve upload references | N/A | N/A | No source-backed UploadAsset registry, ID format or lookup contract | Do not issue a guessed query; keep response assets unresolved | `SOURCE_REQUIRED`; API #34 DD |

### Mutation Matrix

| Mutation ID | Operation | Target | Condition | Fields / source | Audit / mapping | Transaction and failure |
|---|---|---|---|---|---|---|
| M1 | INSERT | Legacy candidate `lessons` | Q1 course exists and candidate direct owner check passes | `course_id` from path `course_id` | No audit column in legacy DDL; [07_lessons_insert.md](../../../apps/study-server/docs/dd/47_mentor_lectures_create/07_lessons_insert.md) | Candidate one-table transaction; rollback on failure |
| M1 | INSERT | Legacy candidate `lessons` | Q1 course exists and candidate direct owner check passes | `name` from request `title` | No audit column in legacy DDL; [07_lessons_insert.md](../../../apps/study-server/docs/dd/47_mentor_lectures_create/07_lessons_insert.md) | Candidate one-table transaction; rollback on failure |
| M1 | INSERT | Legacy candidate `lessons` | Q1 course exists and candidate direct owner check passes | `content` from decimal-string candidate based on request `content` | No audit column in legacy DDL; [07_lessons_insert.md](../../../apps/study-server/docs/dd/47_mentor_lectures_create/07_lessons_insert.md) | DERIVED; rollback on failure |
| M1 | INSERT | Legacy candidate `lessons` | Q1 course exists and candidate direct owner check passes | `sort_order` from request `order` | No audit column in legacy DDL; [07_lessons_insert.md](../../../apps/study-server/docs/dd/47_mentor_lectures_create/07_lessons_insert.md) | Candidate one-table transaction; rollback on failure |
| M1 | INSERT | Legacy candidate `lessons` | Q1 course exists and candidate direct owner check passes | `created_at` from `CURRENT_TIMESTAMP` | No audit column in legacy DDL; [07_lessons_insert.md](../../../apps/study-server/docs/dd/47_mentor_lectures_create/07_lessons_insert.md) | Candidate timestamp; rollback on failure |
| M1 | INSERT | Legacy candidate `lessons` | Q1 course exists and candidate direct owner check passes | `updated_at` from `CURRENT_TIMESTAMP` | No audit column in legacy DDL; [07_lessons_insert.md](../../../apps/study-server/docs/dd/47_mentor_lectures_create/07_lessons_insert.md) | Candidate timestamp; rollback on failure |
| M1 | INSERT | Legacy candidate `lessons` | Q1 course exists and candidate direct owner check passes | Omit `status`; use legacy default `DRAFT` | No audit column in legacy DDL; [07_lessons_insert.md](../../../apps/study-server/docs/dd/47_mentor_lectures_create/07_lessons_insert.md) | Candidate default; enum unresolved |
| M2 | Not specified | No committed `resources`/upload mutation | Asset resolver and format are absent | Do not store raw opaque string or client-supplied URL | No mapping file until a physical write is confirmed | Blocking `SOURCE_REQUIRED`; do not claim complete asset association |

### Response Source Matrix

| Response field | Type | Source type | Candidate source | Data Mapping step | Transform / null rule | Gap |
|---|---|---|---|---|---|---|
| `success` | boolean | Branch constant | API result | `6` | `true` on success | N/A |
| `businessCode` | string | Contract constant | API catalog | `6` | `DESIGN_RESOURCE_CREATED` | Direct |
| `message` | string | Application message | Application | `6` | Safe localized message | Exact message text not specified |
| `data.id` | int64 | INSERT result | `lessons.id` | `5` | Direct | Legacy candidate; ID schema unresolved |
| `data.course_id` | int64 | INSERT result | `lessons.course_id` | `5` | Direct | Legacy candidate |
| `data.title` | string | INSERT result alias | `lessons.name` | `5` | `name → title` | Legacy candidate |
| `data.content` | string? | INSERT result | `lessons.content` | `5` | Candidate decimal string; preserve nullable source only if contract allows omission/null | Request is int64; meaning unresolved |
| `data.assets[]` | `UploadAsset[]` | Unresolved reference source | N/A | Pending | Must not fabricate; no supported null rule because field is required | `SOURCE_REQUIRED`; blocks complete response mapping |
| `data.order` | int32 | INSERT result alias | `lessons.sort_order` | `5` | `sort_order → order` | Legacy candidate |
| `data.status` | LessonStatus | INSERT result/default | `lessons.status` | `5` | Legacy default candidate `DRAFT` | Enum members and legacy-vs-pilot schema unresolved |
| `meta` | object | Envelope default | N/A | `6` | `{}` | API guideline |
| `traceId` | uuid | Correlation value | Request trace | `6` | Propagate request trace | API guideline; no API #47 route today |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #47 implementation | No route/module/test source for #47 in current Study tree | `UNWIRED / NOT_FOUND` | DD is design-only |
| `content` meaning/type | Request is `int64`; Lecture schema and legacy `lessons.content` are string/TEXT; no physical Content table in legacy ERD/DDL | `DISCREPANCY / SOURCE_REQUIRED` | Decimal-string storage is only a `DERIVED` proposal; if it is a content ID, source relationship is missing |
| Asset reference resolution | API #34 returns `UploadAsset`, but upload ID generation, persistence and lookup are unresolved; legacy ERD has only `resources(name, resource_type, url)` | `SOURCE_REQUIRED` | Cannot resolve required `Lecture.assets[]`; do not invent uploads table or URL format |
| `INSERT Lecture/Content` and AC-22 | AC-21 uses ambiguous logical phrase; AC-22 separately models a `Content` tree; legacy schema has `lessons.content` but no `contents` table | `DISCREPANCY` | Candidate #47 writes one `lessons` row; confirm whether a separate Content resource is intended |
| Mentor ownership/assignment | AC-21 permits owner or assigned course; API #46 candidate uses `courses.mentor_id`; no assignment relation or Mentor identity mapping is source-confirmed | `DERIVED / SOURCE_REQUIRED` | Direct owner check is provisional; assignment support cannot be implemented from current source |
| Schema selection | Legacy DDL is BIGINT `courses`/`lessons`; V1-PILOT DDL uses UUID, versioned courses, different `lessons`, `content_blocks`, and `file_objects`; live schema not verified | `DISCREPANCY / NOT_VERIFIED` | Do not combine models; confirm target schema before coding |
| Lesson status | Legacy `lessons.status` defaults to `DRAFT`; `LessonStatus` member set is absent from catalog | `DERIVED / SOURCE_REQUIRED` | DRAFT candidate only; response enum needs confirmation |
| Error envelope | Guidelines require `data:null`; current helper returns `{}` when omitted | `DISCREPANCY` | Expected and current envelope representations remain distinct |

## CHANGES

- Files changed: `apps/study-server/docs/dd/47_mentor_lectures_create/` (eight sheets and three reports), plus this worklog. Existing unrelated dirty DDs/worklogs are preserved.
- CONTEXT_UPDATES: None; this task changes no runtime/schema/catalog/context page.
- Context pages changed: None planned.
- Assumptions: Use the simplest clearly labeled candidate where evidence allows; never turn a candidate into an approved rule. Keep API #47 assets blocking rather than fabricating data.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector and review | Deno selector selected #41–#43; all three full worklogs read; no shortage. | `VERIFIED` |
| Contract and AC-21 coverage | Catalog rows #46–#50 and reusable schemas read; AC-21 nodes/edges confirm #46 → #34 → #47 → #48 and exact #47 contract. AC-22 read to keep Content workflow separate. | `VERIFIED` |
| Schema/source coverage | Legacy DDL/table guide/ERD and V1-PILOT DDL read; API #46/#34/#9/#11 precedents, router, auth and response helper reviewed. | `VERIFIED` |
| Template/skill gate | `createDD-markdown` is registered for `server-study`; all eight Markdown templates opened, headings/front matter/appendices and SHA-256 fingerprints checked; no archive found under Study docs. | `VERIFIED` |
| API #47 source scan | No route/module/test Python source found. | `VERIFIED` |
| DD pack creation/static checks | 11/11 files exist; template appendices are byte-identical; front matter, catalog contract/errors, request/response coverage, legacy column mapping, links, JSON examples, table widths, whitespace and source status passed. | `VERIFIED` |
| Count snapshot | Catalog has 103 IDs; 47 DD folders have eight core sheets; 35 have all three reports; route + matching `view.py` covers #01–#09 and #12–#14 (12 IDs). | `VERIFIED_STATIC_ONLY` |
| Context validator | `deno run --allow-read --allow-env scripts/validate-agent-context.mjs` returned `AGENT_CONTEXT_INVALID` for missing DB Admin context/source paths and unavailable baseline commit `9a70eb6764a6587093a92d3bd7e4cc0bea1651c4`; unrelated to the Study DD changes. | `BLOCKED_UNRELATED_REPO_CONTEXT` |
| Runtime tests | Not run; documentation-only and API #47 is unwired. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: Asset resolver/persistence, content semantics, course assignment/identity mapping, target schema and status enum need confirmation before the DD can be treated as implementation-ready.
- Next owner/action: API #48 DD and macro-review were completed on 2026-10-24; continue with API #49. See the follow-up below.

## FOLLOW-UP — 2026-10-24 AC-21 MACRO REVIEW

- Updated the #47 Plan Result, Open Questions and Verification Report after comparing #46/#47/#48.
- Result: Candidate direct-owner access, no PUBLISHED filter, schema separation, Lecture response shape, and AC-22 Content boundary are coherent across the group. The required assets[] projection remains blocked because API #34 has no approved resolver/persistence source; assignment/identity, live schema, content null behavior and LessonStatus remain open.
- Static comparison does not prove API runtime or database behavior.
- Follow-up files: `apps/study-server/docs/dd/46_mentor_courses/` and `apps/study-server/docs/dd/47_mentor_lectures_create/`.
