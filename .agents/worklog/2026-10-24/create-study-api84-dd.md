---
task_id: "2026-10-24-create-study-api84-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #84

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ contract catalog, tách `DIRECT` và `DERIVED`, không đoán schema; API Admin chưa được runtime wire và Study chỉ giao Markdown.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Giữ gap schema/live DB/Mentor identity; ghi ma trận Request, Query, Mutation, Response; không biến suy luận thành contract.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Content Admin/mentor không được trộn; giữ field/body/business rules chưa có nguồn ở `SOURCE_REQUIRED`; status/error phải theo catalog.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tiếp tục chuỗi một API DD mỗi phiên tại API #84; lập plan và các ma trận trước khi tạo folder; viết DD tiếng Việt theo template; xác minh tĩnh ngay sau authoring.
- Canonical contract/approved DD: Catalog API #84, AC-34 diagram, reusable `Lesson`, DD Admin #82/#83/#75; `createDD-markdown` được registry wire cho `server-study`, và Study workflow giao Markdown folder, không tạo ZIP.

## CURRENT_BEHAVIOR

- Source/config: Catalog và AC-34 xác nhận API #84 `PUT /api/v1/admin/lessons/{lesson_id}`, Bearer JWT/Admin, path `lesson_id:int64!`, `ApiEnvelope<Lesson>`, 200 `DESIGN_RESOURCE_UPDATED`, errors 401/403/404/422/500. Catalog và diagram chỉ liệt kê path, không có body/query fields. `Lesson` có bảy fields; `title`, `content`, `video_url`, `order` là các metadata candidate, còn status có API #85 riêng. Không có source route/module/test Admin; `app/utils/auth.py` hiện có Student guard; middleware error allowlist không có path Admin. Legacy lessons DDL là BIGINT và có `name/content/video_url/sort_order/status/updated_at`; V1-PILOT lessons dùng UUID/versioned fields khác; live schema chưa xác minh.
- Runnable tests: Không chạy; task chỉ tạo DD. Không có test API #84 trong current source.
- Runtime wiring: `UNWIRED / NOT_FOUND` theo router + matching view criterion; đây không phải kết luận kiểm thử runtime.

## SOURCE_TRACE

```text
Admin Bearer principal -> PUT lesson theo path ID + body candidate -> xác minh quyền -> UPDATE legacy lessons candidate và trả row -> map ApiEnvelope<Lesson> -> AC-34 reload danh sách
```

## PLAN BEFORE DD AUTHORING

1. Xác nhận registry wire, đọc skill `createDD-markdown` và 8 template; lưu SHA-256; áp dụng Study override Markdown-only. Không có ZIP trong các thư mục archive thuộc scope đã kiểm tra.
2. Xác nhận catalog/AC-34/reusable schema, current router/auth/middleware, legacy/pilot schema và DD #82/#83/#75.
3. Giữ catalog/diagram path-only làm DIRECT. Đề xuất body full-replacement gồm `title`, `content`, `video_url`, `order` với nhãn `DERIVED`; không đưa `course_id`, `status` (API #85), `id` hoặc timestamps vào client body. Requiredness, null/omit semantics và validation cụ thể vẫn cần owner xác nhận.
4. Candidate mutation chỉ UPDATE `lessons` metadata; mapping vật lý legacy (`title -> name`, `order -> sort_order`) là candidate, `updated_at` server-side là DERIVED; giữ nguyên status/course relation. Không claim live schema.
5. Lập đầy đủ Requirement, Request Usage, Query, Mutation và Response Source matrices trước folder. Candidate `UPDATE ... RETURNING` theo ID; không dùng SQL như runtime contract.
6. Tạo 8 sheet theo template và 3 report trong `84_admin_lesson_update`; giữ đúng error set và response `Lesson`; tạo DD `Draft — Needs Confirmation` vì body/schema/auth chưa được duyệt.
7. Kiểm tra exact file set/template appendix, contract/error coverage, JSON, links/anchors, bảng, fences và whitespace; cập nhật inventory/worklog. Không sửa runtime, schema, catalog, diagram hoặc tạo ZIP.

## PREAUTHORING EVIDENCE AND MATRICES

### API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #84 | Method/path | `PUT /api/v1/admin/lessons/{lesson_id}` | Catalog + AC-34; DIRECT |
| #84 | Actor/auth | Bearer JWT; role Admin; AC-34 lesson-management permission | Catalog/AC; DIRECT requirement, Study guard SOURCE_REQUIRED |
| #84 | Path | `lesson_id:int64!` | Catalog + AC-34; DIRECT |
| #84 | Body/query | Catalog và diagram chỉ khai báo path; không có body/query schema | DIRECT absence; update body SOURCE_REQUIRED |
| #84 | Proposed body | `title`, `content`, `video_url`, `order` | DERIVED candidate từ Lesson fields + UPDATE node; cần xác nhận |
| #84 | Success | HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<Lesson>` | Catalog + AC-34; DIRECT |
| #84 | Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR` | Catalog + AC-34; DIRECT |
| #84 | Mutation boundary | Update lesson metadata; status transition/audit thuộc API #85 | Diagram branch; direct operation boundary, exact fields unresolved |

### Request Usage Matrix

| Request item | Source/use | Query/mutation/response use | Rule/status |
|---|---|---|---|
| Authorization | Header Bearer JWT | Authenticate/authorize Admin before DB | Auth method/role DIRECT; Admin guard and permission mapping SOURCE_REQUIRED |
| `lesson_id` | Required path int64 | Candidate `lessons.id` WHERE and response `data.id` | Type DIRECT; positive/range and malformed mapping not specified |
| `title` | Proposed JSON body | Candidate update `lessons.name`; response `data.title` | DERIVED field; requiredness/length/blank rules need confirmation |
| `content` | Proposed JSON body | Candidate update `lessons.content`; response `data.content` | DERIVED; requiredness/null/omit semantics need confirmation |
| `video_url` | Proposed JSON body | Candidate update `lessons.video_url`; response `data.video_url` | DERIVED; nullable/URI validation details need confirmation |
| `order` | Proposed JSON body | Candidate update `lessons.sort_order`; response `data.order` | DERIVED; int32 DIRECT as response type, input rule/range unresolved |
| `course_id`, `status`, `id`, timestamps | Not in proposed client body | `course_id` and `status` returned unchanged; ID from path; timestamps not in Lesson | Keep course reassignment/status change out; #85 owns status |

### Query Matrix

| Query | Type | Candidate source | Columns/condition | Purpose/status |
|---|---|---|---|---|
| Q1 | UPDATE predicate | Legacy `lessons AS l` | `l.id = :lesson_id` | Candidate row match; legacy DDL only |
| Q1 | SET field | Legacy `lessons AS l` | `name = :title` | DERIVED body-to-column mapping |
| Q1 | SET field | Legacy `lessons AS l` | `content = :content` | DERIVED body-to-column mapping |
| Q1 | SET field | Legacy `lessons AS l` | `video_url = :video_url` | DERIVED body-to-column mapping |
| Q1 | SET field | Legacy `lessons AS l` | `sort_order = :order` | DERIVED body-to-column mapping |
| Q1 | SET timestamp | Legacy `lessons` candidate | `updated_at = CURRENT_TIMESTAMP` | DERIVED; owner/trigger behavior SOURCE_REQUIRED |
| Q1 | RETURNING field | Legacy `lessons AS l` | `id` | Candidate response source |
| Q1 | RETURNING field | Legacy `lessons AS l` | `course_id` | Candidate response source; nullable discrepancy |
| Q1 | RETURNING field | Legacy `lessons AS l` | `name` | Candidate source for `data.title` |
| Q1 | RETURNING field | Legacy `lessons AS l` | `content` | Candidate response source |
| Q1 | RETURNING field | Legacy `lessons AS l` | `video_url` | Candidate response source |
| Q1 | RETURNING field | Legacy `lessons AS l` | `sort_order` | Candidate source for `data.order` |
| Q1 | RETURNING field | Legacy `lessons AS l` | `status` | Candidate unchanged status response source |
| Q1 no row | Result branch | `UPDATE ... RETURNING` | No returned row | Candidate 404 `DESIGN_RESOURCE_NOT_FOUND`; missing/deleted row policy needs confirmation |
| No SELECT/child query | N/A | N/A | No pre-read, status mutation, dependency/audit or course reassignment query evidenced | Do not add guessed query/table |

### Mutation Matrix

| Mutation ID | Operation/target | Fields | Value source | Condition/transaction | Status |
|---|---|---|---|---|---|
| M1 | UPDATE candidate `lessons` | `name` | Body `title` | `id = path lesson_id`; candidate `UPDATE ... RETURNING`; commit/rollback ownership unresolved | DERIVED physical candidate; legacy schema only |
| M1 | UPDATE candidate `lessons` | `content` | Body `content` | Null/omission semantics unresolved | DERIVED physical candidate |
| M1 | UPDATE candidate `lessons` | `video_url` | Body `video_url` | URI/null validation unresolved | DERIVED physical candidate |
| M1 | UPDATE candidate `lessons` | `sort_order` | Body `order` | `int32` response field; input range rule unresolved | DERIVED physical candidate |
| M1 | UPDATE candidate `lessons` | `updated_at` | Server time | Only if no DB trigger/other owner; keep DERIVED | SOURCE_REQUIRED for ownership |
| M1 | Not updated | `course_id`, `status`, `id`, `created_at` | N/A | `status` remains API #85; no course move/delete/audit evidenced | Explicitly out of candidate mutation |

### Response Source Matrix

| Response field | Contract type | Candidate source | Mapping/null rule | Evidence status |
|---|---|---|---|---|
| HTTP status | integer | Catalog branch | 200/401/403/404/422/500 | DIRECT |
| `success` | boolean | Envelope | true success / false error | DIRECT reusable envelope |
| `businessCode` | string | Catalog | Exact branch code only | DIRECT |
| `message` | string | Application | Safe message; exact text unspecified | DERIVED text; no raw DB detail |
| `data.id` | int64 | `UPDATE ... RETURNING id` candidate | Path entity ID | Legacy mapping candidate; live schema unresolved |
| `data.course_id` | int64 | Returned row `course_id` candidate | Preserve existing relation; NULL conflicts with required response | Legacy nullable discrepancy |
| `data.title` | string | Returned `name` candidate | Alias `name -> title` | Legacy candidate; confirmed alias by API #09 source |
| `data.content` | string? | Returned `content` candidate | Null/omit rule unresolved | Legacy nullable candidate |
| `data.video_url` | uri? | Returned `video_url` candidate | URI/null/omit rule unresolved | Legacy TEXT candidate |
| `data.order` | int32 | Returned `sort_order` candidate | Alias `sort_order -> order` | Legacy candidate; confirmed alias by API #09 source |
| `data.status` | LessonStatus | Returned existing `status` candidate | Do not mutate in #84 | Enum members/casing unresolved |
| `meta` | object | Envelope convention | `{}` candidate on success; error fieldErrors per guideline if defined | Current helper/error guideline discrepancy on `data` |
| `traceId` | uuid | Trace middleware | Propagate request trace or generate | Current Study source convention |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #84 runtime | Current router and module/test scan finds no Admin lesson route, matching view or focused test | `UNWIRED / NOT_FOUND` | DD is design-only; no runtime claim |
| Request body | Catalog/AC-34 specify path only while operation says PUT/UPDATE | `DISCREPANCY / SOURCE_REQUIRED` | Candidate body remains DERIVED and draft; requiredness/semantics need owner confirmation |
| Persistence schema | Legacy BIGINT `lessons` and V1-PILOT UUID/versioned model differ; live metadata unavailable | `DISCREPANCY / SOURCE_REQUIRED` | Physical mapping is candidate only |
| Admin authorization | Catalog/AC-34 require Admin/lesson-management permission; current Study helper is Student-only | `SOURCE_REQUIRED` | Future implementation needs approved Admin policy/guard |
| Error integration | Middleware allowlist lacks Admin path; API guideline says error `data:null`, helper defaults `{}` | `DISCREPANCY` | Resolve when wiring endpoint |
| Lesson response mapping | Reusable `Lesson.course_id` required while legacy column is nullable; status enum members not specified | `DISCREPANCY / SOURCE_REQUIRED` | Preserve mapping gap and do not invent values |

## CHANGES

- Files changed: `apps/study-server/docs/dd/84_admin_lesson_update/` (8 template sheets + 3 reports); `.agents/worklog/2026-10-24/create-study-api84-dd.md`; inventory worklog refreshed after static verification.
- CONTEXT_UPDATES: None planned.
- Context pages changed: None planned.
- Assumptions: Preserve existing dirty and untracked worktree content; no application/runtime edits.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector and prior review | Deno selector returned #48, #49, #50; all three read in full; no shortage. | `VERIFIED` |
| Source/contract/template review | Catalog #84, AC-34 index/diagram, reusable Lesson, DDLs, current router/auth/middleware, DD #82/#83/#75, API #09 source, API guidelines and 8 templates reviewed; 8/8 template appendix fingerprints recorded. | `VERIFIED_STATIC_ONLY` |
| Catalog status/error comparison | Catalog row #84 is path-only and the DD preserves success code plus exact five error codes. | `VERIFIED_STATIC_ONLY` |
| Exact DD package and template appendix | Exact 11-file set; all 8 appended template sections byte-match their registered source templates. | `VERIFIED` |
| Markdown/contract static validation | 4 JSON blocks parse; 209 Markdown table rows grouped consistently; 7 code fences balanced; 36 local links resolve; no trailing whitespace; exact catalog response/error set retained. | `VERIFIED` |
| `git diff --check` | No diagnostics. | `VERIFIED` |
| Application tests | Not run; docs-only and endpoint is unwired. | `NOT_RUN` |
| Context validator | No `.agents` context page/registry changed. | `NOT_APPLICABLE` |

## HANDOFF

- Remaining blockers: Owner confirmation of the request body/PUT semantics, active schema, Admin policy, nullability/status rules, timestamp/transaction ownership and error-envelope integration.
- Next owner/action: AC-34 macro-review is complete; continue the DD sequence at API #87 in the next API-DD session.

## GROUP_MACRO_REVIEW — AC-34 #82–#86

- Status: `VERIFIED_WITH_OPEN_QUESTIONS`; see `apps/study-server/docs/dd/86_admin_lesson_delete/VERIFICATION_REPORT.md`.
- Findings carried into #84: preserve metadata-only mutation; status/audit stay in #85, delete/reference behavior stays in #86, and successful update reloads through #82. Body/PUT semantics and the #82 list contract remain unresolved.
- No API approval, route implementation, live schema check or application test is implied by this review.
