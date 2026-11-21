---
task_id: "2026-10-24-create-study-api62-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #62 — Lấy tập người nhận

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` (`node` không có trong PATH)
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Bảo toàn contract catalog; dùng diagram và DB candidates để phân biệt DIRECT/DERIVED/SOURCE_REQUIRED; DD chưa xác minh không được gọi là runtime.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Giữ response shape catalog khi lệch ý diagram; giữ discrepancy mở, không tự đổi shape; Markdown Study không tạo ZIP.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Tạo matrices và plan trước authoring; truy nguyên active data/status từ diagram nhưng đánh dấu đề xuất là DERIVED; không invent physical schema.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo một API DD tiếng Việt cho #62; lập plan trước khi tạo thư mục DD; đọc AC-25 và tài liệu DD liên quan; kiểm tra ngay sau authoring. Đây là một API trong nhóm AC-25; macro-review cả #62–#64 sẽ thực hiện sau khi các DD cùng nhóm có mặt.
- Canonical contract `docs/lists/list_api.md` row #62: `GET /api/v1/mentor/courses/{course_id}/students`; Bearer JWT, role Mentor; `course_id:int64!`; không khai báo query/body; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Page<Course>>`; exact errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
- AC-25 direct flow: Mentor chọn course/soạn thông báo → API #62 → backend đọc active enrollments → UI chọn người nhận/nhập nội dung → API #63 tạo/phát Notification → API #64 đọc trạng thái gửi.
- Deliverable dự kiến: `apps/study-server/docs/dd/62_mentor_course_students/` gồm 8 sheets + `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`; Markdown only, không tạo ZIP.

## CURRENT_BEHAVIOR

- Source/config: Router hiện có API IDs #01–#09 và #12–#14; không có route/module cho #62 trong current source; focused test/path không tìm thấy. API #62 là `UNWIRED / NOT_FOUND`. Current auth guard là Student-specific; chưa có Mentor principal/assignment resolver.
- Schema: Legacy `infra/postgres/study-server/DB.sql` có BIGINT `courses`/`users`/`enrollments`; `enrollments.status` là VARCHAR, default `ACTIVE`. Table guide mô tả `user_id`/`course_id` required nhưng DDL cho phép NULL và không khai báo unique `(course_id,user_id)`. V1-PILOT `infra/postgres/02_study_db.sql` có UUID `course_enrollments` gắn `learner_id`/`course_version_id`, status enum `ENROLLED|IN_PROGRESS|COMPLETED`, và UUID course owner. Không khẳng định schema live/approved hay mapping sang API int64.
- Direct diagram says “Đọc active enrollments” nhưng không chốt predicate/status enum, user projection hay pagination.
- Response conflict: catalog yêu cầu `Page<Course>`; endpoint/AC-25 yêu cầu tập học viên/người nhận. Không thể map enrollment → Course fields trực tiếp từ evidence. Giữ catalog contract, đánh dấu `DISCREPANCY`; recommendation `Page<UserSummary>` chỉ là DERIVED để owner xác nhận.
- Request/response pagination: catalog không khai báo `page`/`size` dù response là `Page<T>`; pagination metadata/default/result bounds là `SOURCE_REQUIRED`.
- Envelope/error wiring: API Guidelines yêu cầu error `data:null`; current `error_response()` serializes absent data as `{}`. API #62 path chưa thuộc `DESIGN_CONTRACT_PATHS`; đây là discrepancy cho future wiring, không phải runtime behavior #62.
- Runnable tests: Không chạy; docs-only, API #62 chưa wired.

## SOURCE_TRACE

```text
Mentor Bearer principal -> chọn course -> GET #62 với course_id -> xác minh quyền Mentor với course -> đọc active enrollments và learner projection -> trả contract catalog Page<Course> (shape/mapping conflict cần xác nhận) -> UI chọn recipients -> POST #63 gửi thông báo -> GET #64 theo dõi trạng thái
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Response resource | Catalog `Page<Course>`; route/AC-25 đọc active enrollments để chọn học viên | `DISCREPANCY` | Giữ đúng catalog trong API Requirement Matrix; không map course giả từ enrollment; đề xuất `Page<UserSummary>` chỉ để owner xác nhận. |
| Pagination input | Response `Page<T>` có PageMeta; request chỉ có path | `SOURCE_REQUIRED` | Không tự thêm query fields/default; lựa chọn người nhận có thể không truy cập đủ page. |
| Enrollment source/status | Legacy BIGINT `enrollments.status` default ACTIVE; V1-PILOT UUID `course_enrollments` và enum khác | `DISCREPANCY / DERIVED / SOURCE_REQUIRED` | Candidate predicate cần giữ rõ nguồn; live schema và active definition chưa được duyệt. |
| Enrollment integrity/grain | Legacy DDL permits nullable user/course references and has no `(course_id,user_id)` unique; table guide describes required references | `DISCREPANCY / SOURCE_REQUIRED` | Orphan handling and recipient deduplication/count grain are unresolved. |
| Mentor scope | AC-25 yêu cầu Mentor có quyền gửi tới học viên của course; legacy `courses.mentor_id` là candidate; principal/assignment chưa có nguồn | `SOURCE_REQUIRED` | Không chốt direct-owner authorization như runtime fact. |
| Recipient handoff | API #63 nhận `recipients:string!`; encoding/ID representation không mô tả | `SOURCE_REQUIRED` | Không thể khẳng định cách serialize lựa chọn từ #62 sang #63. |
| API #62 runtime | Không có route/module/test source | `UNWIRED / NOT_FOUND` | DD chỉ là design artifact. |
| Error envelope/wiring | Guideline wants error `data:null`; helper defaults `{}`; #62 path not in design-code allowlist | `DISCREPANCY / CONDITIONAL_FUTURE_WIRING` | Revisit during implementation; not current API #62 behavior. |

## PLAN BEFORE DD AUTHORING

1. Dùng đúng contract #62: method/path, Mentor Bearer, required int64 course_id, no query/body, HTTP 200/resource-retrieved, `ApiEnvelope<Page<Course>>`, và đúng bốn error codes 401/403/404/500. Không thêm 422 hoặc query fields.
2. Bám AC-25: đọc active enrollments trước bước UI chọn người nhận; #62 read-only; #63 sở hữu tạo/phát notification; #64 đọc delivery status. Không thêm mutation/dispatch vào #62.
3. Ghi response mismatch ở mọi ma trận liên quan. Giữ `Page<Course>` như catalog; nêu `Page<UserSummary>` là recommendation DERIVED/open vì schema dùng lại được và phù hợp picker, không biến thành approved contract.
4. Candidate query legacy: course + enrollments + users; enrollment filter `status='ACTIVE'` là DERIVED từ default legacy và nhãn “active” trong diagram. Pilot UUID/course-version/learner-profile là evidence xung đột riêng; không ghép hai schema, không tạo physical SQL như runtime fact.
5. Authorization: giữ requirement Mentor có quyền với course; direct `courses.mentor_id` là candidate theo DD #46, chưa bao gồm assigned course và chưa có Mentor claim mapping. Missing course 404 và unauthorized 403 theo catalog; privacy/check ordering vẫn mở.
6. Giữ `page`/`size` ngoài request matrix vì catalog không khai báo; đánh dấu PageMeta calculation, ordering, page bounds, empty behavior và cách lấy các trang tiếp theo là SOURCE_REQUIRED. Không hardcode defaults từ API #6/#46.
7. Request/Query/Mutation/Response Source matrices đầy đủ; 07_table là `N/A — READ-ONLY API`; Error sheet chỉ có bốn catalog cases.
8. Đọc/đối chiếu 8 registered template files và fingerprints; giữ appendix byte-for-byte; tạo 8 sheets và 3 reports, không ZIP.
9. Static verify exact manifest, front matter, exact error rows, nested response fields, JSON, links/anchors, table widths, fences, whitespace, appendix fingerprints và `git diff --check`. Runtime tests `NOT_RUN`.
10. Chưa đóng macro-review cho AC-25 tới khi #63/#64 có DD; ghi open handoff về recipient wire format và delivery flow.

### API Requirement Matrix — plan gate

| API ID | Method/path | Actor/auth | Input | Success/response | Errors | Status |
|---|---|---|---|---|---|---|
| #62 | `GET /api/v1/mentor/courses/{course_id}/students` | Bearer JWT; Mentor | `course_id:int64!`; no body/query | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Page<Course>>` | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR` | Catalog DIRECT; response/content/pagination conflicts open |

### Request Usage Matrix — plan gate

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Header; authenticate Bearer and Mentor role | Principal scopes course access | Role DIRECT; guard, claim and identity binding SOURCE_REQUIRED |
| `course_id` | Required path int64 | Q1 course/access check and Q2 enrollment filter | Type DIRECT; legacy BIGINT and pilot UUID models conflict |
| Body/query | None declared | None | DIRECT; do not add pagination query fields |
| `X-Trace-Id` | Shared optional header convention | Envelope/response trace if wired | Convention only; not API #62 catalog input |

### Query Matrix — plan gate

| Query | Type | Candidate source/columns | Predicate/purpose | Status |
|---|---|---|---|---|
| Q1 course/access | SELECT | Legacy `courses.id`, `courses.mentor_id` | Locate path course and validate Mentor permission | Candidate only; principal binding, assignment and live schema SOURCE_REQUIRED |
| Q2 roster | SELECT | Legacy `enrollments.course_id`, `status`, `user_id`, `enrolled_at`; `users.id`, `role`, `full_name`, `avatar_url` | Read active enrollment learner candidates for AC-25 recipient selector | Candidate `status='ACTIVE'` from diagram + legacy default; Student role filter DERIVED; no runtime mapping |
| Q3 page count | COUNT | Distinct active learner IDs if a recipient-page contract is approved | Populate `PageMeta.total` and total pages | SOURCE_REQUIRED; catalog has no page/size input and current response element is Course |

### Mutation Matrix — plan gate

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | API #62 is read-only roster lookup | No INSERT/UPDATE/DELETE or delivery dispatch | `N/A — READ-ONLY API`; #63 owns notification creation/delivery |

### Response Source Matrix — plan gate

| Response field | Contract | Candidate mapping | Gap/status |
|---|---|---|---|
| Envelope `success`, `businessCode`, `message`, `meta`, `traceId` | ApiEnvelope | Shared envelope/trace convention | Catalog success code DIRECT; text/serialization convention only |
| `data.items[]` | `Course[]` | No valid mapping from enrollment/user rows to Course list as a recipient roster | `DISCREPANCY`; do not change direct contract silently |
| `data.items[].id` | int64 | Course.id per Course schema | Enrollment candidate does not supply per-recipient course record fields; mapping as roster item SOURCE_REQUIRED |
| `data.items[].title` | string | Course.title | SOURCE_REQUIRED in roster response; legacy maps `courses.name` only for course entity |
| `data.items[].description` | string? | Course.description | SOURCE_REQUIRED for roster response |
| `data.items[].thumbnail_url` | uri? | Course.thumbnail_url | SOURCE_REQUIRED for roster response |
| `data.items[].price` | decimal-string | Course.price | SOURCE_REQUIRED for roster response |
| `data.items[].status` | CourseStatus | Course.status | Enum and roster semantics SOURCE_REQUIRED |
| `data.items[].mentor` | UserSummary | Course mentor projection | Not the enrolled Student; SOURCE_REQUIRED for recipient flow |
| `data.items[].category` | Category? | Optional Course.category | Roster query has no approved category relation; SOURCE_REQUIRED/optional omission rule |
| `data.pagination.page` | int32 | Effective page | No input/default in #62 contract; SOURCE_REQUIRED |
| `data.pagination.size` | int32 | Effective size | No input/default in #62 contract; SOURCE_REQUIRED |
| `data.pagination.total` | int64 | Distinct recipients/course rows | Entity and count grain conflict; SOURCE_REQUIRED |
| `data.pagination.total_pages` | int32 | Count and effective size | Pagination semantics SOURCE_REQUIRED |
| Proposed `UserSummary` item | Not current contract | Legacy `users.id`, `full_name`, `avatar_url` from active enrollment; reusable schema exists | `Page<UserSummary>` is a DERIVED recommendation only; owner/catalog confirmation required |

## Source coverage captured before DD creation

- AC-25 Draw.io page was parsed cell-by-cell; its edges establish #62 → active enrollment read → recipient selection → #63 → notification/recipients insert → external Push/Email → #64 status poll.
- API #63 row confirms `recipients:string!` but defines no ID encoding or delimiter; #62 response-to-#63 handoff remains open.
- #46 DD was reviewed for direct-owner candidate and Page<Course> patterns; #54 DD for missing pagination rules; #61 DD/report for the latest Study Markdown package convention.
- Legacy `DB_UNICA_TABLES.md`/`DB.sql` and V1-PILOT DDL were compared; no artifact establishes which enrollment schema is live.

## CHANGES

- Files changed: `apps/study-server/docs/dd/62_mentor_course_students/` (8 sheets + 3 reports) and this worklog. No source, test, schema, catalog, diagram or context page changed.
- CONTEXT_UPDATES: None planned; no current source/schema/catalog/context page changes.
- Context pages changed: None planned.
- Assumptions: Keep active-enrollment filter, proposed `Page<UserSummary>`, and any fixed-page behavior clearly DERIVED/open; do not promote to runtime or catalog fact.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/review | Deno selector selected #48/#49/#50; each was read in full. | `VERIFIED` |
| Context and registry | Root/global context, context map, Study scope pages and `createDD-markdown` registry entry read. | `VERIFIED_STATIC_ONLY` |
| AC-25 diagram | Parsed all nodes/edges: active enrollments → recipient selection → #63 dispatch → #64 delivery status. | `VERIFIED_STATIC_ONLY` |
| Catalog and schemas | API #62–#64 rows and reusable Page/Course/Enrollment/UserSummary schemas read. | `VERIFIED_STATIC_ONLY` |
| Current source/tests | No #62 route, module or focused test found; Student-only current guard noted. | `VERIFIED_STATIC_ONLY` |
| Database | Legacy enrollment model and V1-PILOT course_enrollments/UUID model compared; live schema remains unverified. | `VERIFIED_STATIC_ONLY` |
| DD authoring and static checks | 11/11 manifest; 8/8 front matter/template appendix/fingerprint; exact four errors; response field coverage; 2 JSON examples; 29 links/11 anchors; table widths, fences and whitespace pass; `git diff --check` clean. | `VERIFIED_STATIC_ONLY` |

## HANDOFF

- Remaining blockers: Catalog response resource mismatch, pagination controls/metadata, approved live enrollment schema/status, Mentor identity/assignment, #63 recipient encoding.
- Next owner/action: API #62–#64 macro-review completed with open questions; continue one API per session at #65. Do not treat static document checks as runtime verification.


## GROUP_MACRO_REVIEW — AC-25 after API #64

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` at document level.
- Cross-API findings: #62 direct `Page<Course>` still conflicts with learner roster; missing page/size controls; #63 has no approved recipient key/encoding or course scope; #64 accepts notification_id int64 but #63 only returns Operation UUID; #64 Operation response does not represent delivery summary.
- API #18 remains a separate generic job poll with ID/owner/result/persistence conflicts and a detached AC-25 diagram node.
- No catalog, source, schema or diagram edits were made; open questions remain in the connected DDs. See `apps/study-server/docs/dd/64_mentor_notifications_status/VERIFICATION_REPORT.md`.
