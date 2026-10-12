# PLAN_RESULT — Study API #40 DD

**Task:** Tạo DD draft cho `POST /api/v1/discussions`
**Status:** Draft — Needs Confirmation
**Date:** 2026-10-12

## Kết quả

Tạo tám sheet Markdown theo template Study Server, cùng `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md` và worklog. Không tạo ZIP theo `.agents/server-study/workflows/README.md`; không thay đổi runtime, catalog, diagrams, ERD hoặc DDL.

## Requirement matrix

| API | Method | Endpoint | Actor/Auth | Input | Response contract | Source behavior | Folder |
|---:|---|---|---|---|---|---|---|
| 40 | POST | `/api/v1/discussions` | Student / Bearer JWT | `body{course_id:int64!, title:string!, content:int64!}` | `ApiEnvelope<Page<Discussion>>` | AC-19 new-topic branch says `INSERT Discussion`; access and persistence mapping remain unresolved | `40_discussions_create` |

## Source and evidence classification

| Source | Role | Evidence used | Status |
|---|---|---|---|
| [`docs/lists/list_api.md`](../../../../../docs/lists/list_api.md) | API catalog | API #40 request, response, HTTP/business codes; reusable schemas | `APPROVED_DESIGN_CONTRACT`; not runtime-verified |
| [`AC_UNICA/00_AC_API_INDEX.md`](../../../docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) | AC index | AC-19 Student actor, course participation precondition, topic/comment postcondition and API mapping | Design evidence |
| [`AC_UNICA/AC_02_STUDENT_LEARNING.drawio`](../../../docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) | Activity flow | AC-19 branch: new topic → API #40 → `INSERT Discussion`; reply uses API #41 | Design evidence; details incomplete |
| [`DB_UNICA_TABLES.md`](../../../docs/diagrams/DB_UNICA_TABLES.md) and [`DB_UNICA_ERD.drawio`](../../../docs/diagrams/DB_UNICA_ERD.drawio) | Discussion DB design | Candidate fields, parent self-reference and title gap | `DESIGN_ONLY` |
| [`infra/postgres/study-server/DB.sql`](../../../../../infra/postgres/study-server/DB.sql) | Checked-in DDL | `discussions` and `users` candidate columns/defaults/nullability | `DESIGN_ONLY`; live schema unverified |
| [`contracts/api-guidelines/README.md`](../../../../../contracts/api-guidelines/README.md) | Shared API convention | Envelope, trace ID and error fields | Contract convention |
| `apps/study-server/app/api/v1.py`, `app/utils/auth.py`, `app/modules/`, `tests/` | Current runtime source | No discussion route/module/test; shared helper checks JWT subject and Student role | Current source; API #40 `UNWIRED / NOT_FOUND` |
| [`39_discussions`](../39_discussions/00_Cover.md) | Adjacent DD | Course access, title, visibility, FK nullability and comments questions | Draft context; do not treat as approved behavior |
| `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD` | Canonical template | Eight sheet layouts and Excel audit appendices | Read and fingerprinted |

## Input coverage

| Source set | Units inspected | Use |
|---|---|---|
| API catalog | API #40 row, reusable `Discussion`, `Page`, `PageMeta`, `UserSummary`, `DiscussionComment` | Approved request/response/error baseline |
| Diagram directory | Full inventory; AC index, AC-19 activity flow, discussion ERD node and DB guide section reviewed | AC-19 flow and source conflicts; unrelated AC flows not used |
| Checked-in DB DDL | `users` and `discussions` definitions | Candidate field types, defaults and nullability only |
| Runtime | `v1.py`, app/modules discussion scan, tests scan, `app/utils/auth.py` | Confirm API is absent; note current JWT principal fields |
| Adjacent DD | API #39 cover, request/response/mapping, error, open questions and reports | Carry forward unresolved discussion-domain boundaries |
| Template | Eight Markdown files | Structure, order and appendices |

## Reconciliation matrices

### Request usage

| Request field | Mapping use | Status |
|---|---|---|
| `course_id` | Candidate `discussions.course_id`; course access predicate unresolved | Candidate; DDL FK nullable |
| `title` | Required logical request/response field; no physical column | `SOURCE_REQUIRED / DISCREPANCY` |
| `content` | Candidate `discussions.content`; request int64 vs DDL TEXT/logical string | `DISCREPANCY`; no cast invented |
| Bearer JWT | Student role and principal identity | Catalog expected behavior; route unwired |

### Query and mutation

| Item | Candidate | Status |
|---|---|---|
| Course access query | No table/predicate selected | `SOURCE_REQUIRED` |
| Author lookup | `users` by current principal ID if profile response is required | Candidate only |
| Mutation | One `INSERT discussions` for AC-19 new-topic branch; `parent_id=NULL` candidate | Design-only; required title/timestamps and content mapping unresolved |
| Other writes | No counter/update operation specified for API #40's branch | Not added |

### Response sources

| Response field | Candidate source | Gap |
|---|---|---|
| `id`, `course_id` | Inserted discussion row | Generated ID/live schema and FK nullability unverified |
| `title`, `content` | Logical Discussion schema/request | No title column; content types conflict |
| `author` | Current principal plus candidate `users` lookup | Profile read not specified |
| `status`, `comments` | Discussion row/child rows | Enum, initial state and inclusion unresolved |
| `pagination` | `PageMeta` schema | Create endpoint provides no page policy |

## Scope and handoff

- Keep API #40 contract exact: HTTP 201 `DESIGN_RESOURCE_CREATED`; errors 401, 403, 422 and 500 with catalog codes.
- Preserve `content:int64!` and `ApiEnvelope<Page<Discussion>>`; list their mismatches as open decisions.
- Mark current route/module/test state `UNWIRED / NOT_FOUND`; do not run runtime tests for this documentation-only task.
- Preserve existing API #27–#39 artifacts and source files; create only the API #40 DD and its worklog.
- Review [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) before approving the DD or implementing API #40.
