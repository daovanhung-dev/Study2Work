---
task_id: "2026-10-24-create-study-api54-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #54 — Lấy submissions Mentor

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `available:74`, `selected:3`, `status:READY`, shortage `none`.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ nguyên catalog; source schema/DD không chứng minh runtime; Mentor identity/assignment vẫn SOURCE_REQUIRED; Study DD chỉ Markdown.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Giữ expected/current riêng; đánh dấu tree/response shape mismatch thay vì đổi contract; candidate query phải DERIVED và schema gap phải mở.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: AC-22 Content không tương đương Submission; không chuyển suy luận thành schema; giữ request, response và enum gaps rõ ràng.
  - related: `.agents/worklog/2026-10-24/create-study-api53-dd.md`
    - carry_forward: Dùng nhãn DIRECT/DERIVED/SOURCE_REQUIRED; lập kế hoạch trước authoring; chưa macro-review nhóm cho tới khi các API liên quan tồn tại.
  - related: `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`
    - carry_forward: Sau #53 có 53 DD; API #54 là ID tiếp theo chưa có DD; runtime implementation được đếm riêng theo router + view.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD tiếng Việt cho API #54 sau khi ghi plan; đọc AC-23 và nguồn persistence liên quan; phân biệt nguồn trực tiếp với đề xuất; kiểm tra tài liệu ngay sau authoring.
- Canonical contract: `docs/lists/list_api.md` row #54 — `GET /api/v1/mentor/submissions`, Bearer JWT role Mentor, query `course_id?:int64`, `status?:string`, `page?:int32`, `ApiEnvelope<Submission>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, lỗi đúng tập 401/403/409/500.
- `Submission`: `id:int64`, `assignment_id:int64`, `user_id:int64`, `content?:string`, `files:UploadAsset[]`, `status:SubmissionStatus`, `submitted_at:date-time`, `score?:decimal-string`, `feedback?:string`.
- AC-23: Mentor có quyền chấm bài submission của course; GET danh sách → đọc submissions theo quyền Mentor → chọn một submission → API #55 đọc Submission + files + rubric. Diagram không định nghĩa response collection, pagination metadata, sort, status enum hoặc điều kiện 409.

## CURRENT_BEHAVIOR

- Source/config: Không có route `/api/v1/mentor/submissions`, API #54 module hoặc test tương ứng trong `apps/study-server/app`/`tests`. Router hiện không có Mentor submission routes; auth helper hiện hành chỉ có shared Student current-user guard.
- Database artifacts: `DB_UNICA_TABLES.md`, ERD và checked-in `infra/postgres/study-server/DB.sql` có candidate `assignment_submissions`, `assignments`, `courses`; đây là design/pilot artifacts, live schema chưa xác minh. DDL cho phép NULL ở `assignment_submissions.assignment_id/user_id` và `assignments.course_id`, khác ghi chú ERD/table guide bắt buộc.
- Runnable tests: Không chạy; task chỉ tạo tài liệu và API #54 chưa có test source.
- Runtime wiring: `UNWIRED / NOT_FOUND`. Middleware design-code allowlist hiện không chứa endpoint #54; nếu route mới không được thêm vào allowlist thì fallback validation/internal codes sẽ khác catalog.

## SOURCE_TRACE

```text
Mentor Bearer principal -> parse optional course_id/status/page -> enforce access to courses that contain submissions -> read candidate assignment_submissions through assignments/course -> apply only supplied filters -> map catalog Submission envelope -> Mentor selects one item -> API #55 detail
```

Physical schema, Mentor identity/assignment relation, collection shape and pagination semantics remain unresolved.

## API REQUIREMENT MATRIX

| ID | Contract item | Value | Basis/status |
|---|---|---|---|
| #54 | Method/path | `GET /api/v1/mentor/submissions` | Catalog + AC-23; DIRECT |
| #54 | Actor/auth | Bearer JWT; role Mentor | Catalog + AC-23; DIRECT |
| #54 | Query `course_id` | optional `int64` | Catalog; DIRECT |
| #54 | Query `status` | optional `string` | Catalog; DIRECT; enum/blank policy unresolved |
| #54 | Query `page` | optional `int32` | Catalog; DIRECT; default/range/size unresolved |
| #54 | Body/path | None declared | Catalog; DIRECT omission |
| #54 | Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Submission>` | Catalog + AC-23; DIRECT |
| #54 | Errors | 401 auth; 403 access; 409 state conflict; 500 internal | Catalog; DIRECT exact set |
| #54 | List semantics | List endpoint/flow but singular `Submission` contract | Catalog/AC wording discrepancy; preserve literal contract, open question |

## REQUEST USAGE MATRIX

| Request item | Source/use | Candidate query/response use | Rule/status |
|---|---|---|---|
| Authorization | Header | Authenticate Mentor and constrain course access | Role DIRECT; Mentor guard, identity and assignment mapping SOURCE_REQUIRED |
| `course_id` | Optional query int64 | Candidate filter through `assignments.course_id` | DIRECT field; positive-range/malformed behavior not defined |
| `status` | Optional query string | Candidate filter on `assignment_submissions.status` | DIRECT field; allowed values, blank handling and case policy SOURCE_REQUIRED |
| `page` | Optional query int32 | Candidate page selector | DIRECT field; default, range, size and output metadata SOURCE_REQUIRED |
| Body | None declared | None | DIRECT from catalog |

## QUERY MATRIX

| Query | Type | Candidate logical source | Candidate fields/predicate | Status |
|---|---|---|---|---|
| Q1 | SELECT | `assignment_submissions AS s` | Read Submission candidate columns by authorized course scope | Physical runtime query SOURCE_REQUIRED; V1-PILOT design candidate only |
| Q1 join | JOIN | `assignments AS a` | `a.id = s.assignment_id`; optional `a.course_id = :course_id` when supplied | Relationship in ERD; nullable DDL discrepancy; candidate only |
| Q1 access | JOIN/filter | `courses AS c` | `c.id = a.course_id`; `c.mentor_id = :mentor_id` as direct-owner candidate | DERIVED; does not establish assigned Mentor access or numeric claim mapping |
| Q1 filter | WHERE | `assignment_submissions.status` | Apply requested status only when supplied | Candidate from field/table; enum and normalization SOURCE_REQUIRED |
| Q1 ordering | ORDER BY | N/A | No sort declared | SOURCE_REQUIRED; do not invent ordering |
| Q1 pagination | LIMIT/OFFSET | N/A | `page` supplied without page size/default | SOURCE_REQUIRED; no exact query pagination can be prescribed |
| Q2 | COUNT | N/A | No count or Page metadata declared | SOURCE_REQUIRED; do not add count response |

## MUTATION MATRIX

| Operation | Target | Condition | Fields/effect | Status |
|---|---|---|---|---|
| None | N/A | API is read-only | No INSERT/UPDATE/DELETE | `N/A — READ-ONLY API` |

## RESPONSE SOURCE MATRIX

| Response field | Type | Candidate source | Mapping/null rule | Evidence status |
|---|---|---|---|---|
| `success` | boolean | Envelope branch | true on success; false on error | Shared envelope convention |
| `businessCode` | string | Catalog | Exact success/error code | DIRECT |
| `message` | string | Application message | Safe text; exact wording unspecified | DERIVED |
| `data.id` | int64 | `assignment_submissions.id` | Candidate direct mapping | Pilot candidate; live source unverified |
| `data.assignment_id` | int64 | `assignment_submissions.assignment_id` | Required logical field; DDL nullable | Candidate + schema discrepancy |
| `data.user_id` | int64 | `assignment_submissions.user_id` | Required logical field; DDL nullable | Candidate + schema discrepancy |
| `data.content` | string? | `assignment_submissions.content` | Preserve nullable value; null/omit serialization open | Candidate mapping |
| `data.files[]` | `UploadAsset[]` | No approved asset relation | Do not synthesize from one `file_url` | SOURCE_REQUIRED; blocks complete projection |
| `data.files[].id` | int64 | No approved source | No asset ID lookup | SOURCE_REQUIRED |
| `data.files[].name` | string | No approved source | No metadata source | SOURCE_REQUIRED |
| `data.files[].url` | uri | Candidate `file_url` is insufficient | URL/access/signing policy unresolved | SOURCE_REQUIRED |
| `data.files[].content_type` | string | No approved source | No metadata column/source | SOURCE_REQUIRED |
| `data.files[].size_bytes` | int64 | No approved source | No metadata column/source | SOURCE_REQUIRED |
| `data.files[].status` | UploadStatus | No approved source | Enum/lifecycle unresolved | SOURCE_REQUIRED |
| `data.status` | SubmissionStatus | `assignment_submissions.status` | Preserve stored candidate value | Values/lifecycle unresolved |
| `data.submitted_at` | date-time | `assignment_submissions.submitted_at` | Timestamp zone/precision/serialization open | Candidate mapping |
| `data.score` | decimal-string? | `assignment_submissions.score` | Candidate NUMERIC(6,2) conversion unresolved | Candidate + format gap |
| `data.feedback` | string? | `assignment_submissions.feedback` | Preserve nullable value; disclosure rule not specified | Candidate mapping |
| `meta` | object | Shared envelope | No page/count fields added | DIRECT shape; empty metadata candidate |
| `traceId` | uuid | Request trace | Propagate request trace ID | Shared convention; route absent |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| List shape | API/AC label GET submissions but response says `Submission`, not `Page<Submission>` | `DISCREPANCY / SOURCE_REQUIRED` | Keep literal schema in draft; do not fabricate `items`/pagination wrapper |
| Pagination | `page` only; no `size`, default, range or page metadata | `SOURCE_REQUIRED` | Cannot define stable page query or navigation semantics |
| Status filter | Query is `string`; enum values and blank/case rules absent | `SOURCE_REQUIRED` | Do not infer SubmissionStatus members |
| Access scope | AC-23 requires permission for submissions of course; optional `course_id`; Mentor assignment model absent | `DERIVED / SOURCE_REQUIRED` | Direct-owner is only a candidate, not approved access policy |
| Files | Logical `files:UploadAsset[]`; candidate DDL has one `file_url` and no asset association/metadata | `DISCREPANCY / SOURCE_REQUIRED` | Full response cannot be assembled from current design schema |
| Error 409 | Catalog includes `DESIGN_STATE_CONFLICT`; GET flow defines no conflict condition | `SOURCE_REQUIRED` | Preserve code, do not invent a filter/state rule |
| Schema | ERD/table guide mark assignment/user/course links required; pilot DDL allows NULL; live schema unknown | `DISCREPANCY / NOT_VERIFIED` | Candidate joins may drop or encounter orphan rows; do not claim live behavior |
| Runtime | No route/module/test for #54; current auth helper Student-only | `UNWIRED / NOT_FOUND` | DD does not establish Mentor runtime support |

## PLAN BEFORE DD AUTHORING

1. Preserve exact method/path, Bearer Mentor contract, three optional query parameters, `ApiEnvelope<Submission>`, success and four catalog error branches.
2. Use AC-23 node/edge order: GET list → read submissions by Mentor permission → select one → API #55 detail. Do not add data requirements from #55's rubric step to #54.
3. Keep the list/singular mismatch visible; use the singular Submission schema for the example and do not change it to an array or Page.
4. Treat `assignment_submissions`, `assignments`, and `courses` only as checked-in design candidates. Show only logical query relationships and flag nullable DDL/guide conflict and unverified live schema.
5. Apply optional `course_id` and `status` only when supplied, without inventing defaults, values or normalization. Record Mentor all-course behavior and access predicate as unresolved; direct course owner is only a DERIVED candidate.
6. Do not specify `LIMIT/OFFSET` from `page` alone; no page size/default/order/count contract exists.
7. Map every Submission and nested UploadAsset field one row at a time. Do not fabricate files or map a single `file_url` into an UploadAsset array.
8. Keep `07_table.md` as `N/A — READ-ONLY API`; no SQL mutation or DB write mapping.
9. Create 8 sheets plus `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md` in `54_mentor_submissions_list/`; use the registered template and its appendix. No ZIP, source, schema, catalog or diagram edits.
10. Verify exact 11-file set, all eight template appendix tails, front matter, exact catalog/error set, every query/response field, JSON, relative links, Markdown tables/fences/whitespace and `git diff --check`.
11. Leave AC-23 group macro-review for #54–#57 pending until the related DDs exist; preserve group-level questions for a later review.

## CHANGES

- Files changed: `apps/study-server/docs/dd/54_mentor_submissions_list/` (8 sheets + 3 reports); this worklog; inventory count worklog.
- CONTEXT_UPDATES: None; no runtime/schema/catalog/diagram or `.agents/server-study` page changes.
- Assumptions: Produce a design-only draft despite open contract gaps; all inferred candidate behaviors remain labeled `DERIVED` or `SOURCE_REQUIRED`.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/read | Deno selector returned #48/#49/#50; all three selected worklogs were read. | `VERIFIED` |
| Context and skill routing | Root router, context map, server-study entry/index/workflow, manifest skill wiring, `createDD-markdown` skill and worklog template read. | `VERIFIED_STATIC_ONLY` |
| AC-23 | Parsed all nodes and edges in AC-23 page; confirms GET-list → read → select → detail → grade → feedback. | `VERIFIED_STATIC_ONLY` |
| Catalog/DB/source scan | Read #54 contract/schema, table guide, ERD relations, pilot DDL, prior #35 DD and current router/auth/middleware source; live schema not checked. | `VERIFIED_STATIC_ONLY` |
| Template baseline | Opened registered templates; fingerprints recorded in `VERIFICATION_REPORT.md`; existing API #53 appendix tails match source templates. | `VERIFIED_STATIC_ONLY` |
| Static DD verification | Exact 11-file manifest; eight front matters/statuses, template appendix tails, JSON, relative links, table widths, code fences and whitespace passed. | VERIFIED |
| Catalog contract | Method/path/query/response and exact 200/401/403/409/500 business-code set match row #54. | VERIFIED_STATIC_ONLY |
| Source scan | No API #54 route/module/test match; no Mentor guard exists in current shared auth helper. | VERIFIED_STATIC_ONLY |
| Git diff check | git diff --check returned no diagnostics. | VERIFIED |
| DD inventory | 54 folders; 54/54 have eight core sheets; 42 full 11-file packs; 49 IDs #55–#103 remain without a DD. | VERIFIED_STATIC_ONLY |
| Context validator | Node v24 with `--skip-drift` still returned AGENT_CONTEXT_INVALID for pre-existing missing db-admin context/source paths and broken db-admin links. The earlier Deno run also reported pre-existing server-study source drift; no API #54 worklog error was reported. | FAILED_PREEXISTING_CONTEXT_DRIFT |
| Runtime tests | Not run; docs-only and endpoint has no test module. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: Confirm response cardinality, page size/default/sort/meta, status enum, Mentor assigned-course identity/access model, file asset persistence/metadata and 409 condition.
- Next owner/action: Continue at API #55; keep AC-23 macro-review pending until APIs #55–#57 DDs are created.

## GROUP_MACRO_REVIEW

- Trạng thái: VERIFIED_WITH_OPEN_QUESTIONS sau khi tạo DD API #57.
- Flow chung: #54 list → #55 detail/files/rubric → #56 score/status GRADED → #57 feedback → success; mỗi API giữ đúng phần read/write của mình.
- API #54 vẫn có mismatch giữa mục đích danh sách và response Submission đơn; 409 chưa có nhánh trong AC-23. Giữ contract catalog hiện tại tới khi owner quyết định.
- API #55 có gap rubric trong response; #56 nhận rubric items nhưng chưa có key, schema hoặc persistence legacy được xác nhận.
- API #56 giữ mutation score/status; #57 tách riêng feedback.
- Submission.files vẫn thiếu UploadAsset resolver. attachments của #57 không phải files học viên nộp, không dùng lại file_url; chưa có bảng hoặc field response được suy diễn.
- Mentor JWT identity, assigned-course, direct-owner candidate và quan hệ nullable/orphan còn mở.
- Error data null/object và middleware dynamic path mapping là gap wiring tương lai.
- Không chạy runtime tests hay AC-23 end-to-end; đây chỉ là macro-review tài liệu.
