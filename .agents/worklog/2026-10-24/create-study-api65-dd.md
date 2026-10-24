---
task_id: "2026-10-24-create-study-api65-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #65

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ đúng catalog response; tách candidate schema với nguồn live; đánh dấu `DERIVED` và để `SOURCE_REQUIRED` cho dữ liệu không có persistence.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Bám AC diagram theo thứ tự; không gộp API kế tiếp; giữ exact error set, candidate query và response conflict rõ ràng.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: API #65 chưa có DD; dùng nguồn diagram/catalog/current source riêng; schema pilot không được thay thế âm thầm cho contract int64.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tiếp tục mục tiêu một API DD mỗi phiên tại API #65; authoring bằng tiếng Việt; đọc kỹ diagram AC-26; tham khảo DD đã tạo; lập plan trước khi tạo folder; kiểm tra ngay sau authoring; chờ macro-review nhóm logic #65–#67 đến khi các DD trong nhóm có mặt.
- Canonical contract/approved DD: `docs/lists/list_api.md` row #65; `AC_UNICA/00_AC_API_INDEX.md` AC-26; page `AC-26 Theo dõi tiến độ` trong `AC_03_MENTOR_TEACHING.drawio`; `Page<T>`, `Course`, `UserSummary`, `PageMeta`, and `ApiEnvelope<T>` reusable schemas.

## CURRENT_BEHAVIOR

- Source/config: Catalog khai báo `GET /api/v1/mentor/courses/{course_id}/progress`, Bearer JWT, role Mentor, path `course_id:int64!`, không query/body, `ApiEnvelope<Page<Course>>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, lỗi đúng 401/403/404/500. AC-26 sequence là #65 aggregate enrollment/progress → #66 aggregate learning events → chọn Student → #67 đọc progress theo Student. Study router, module `api_65_*`, và test #65 không có trong source hiện tại.
- Runnable tests: Không chạy; docs-only, API #65 chưa wired và không có focused test.
- Runtime wiring: `UNWIRED / NOT_FOUND`. API auth helper hiện tại chỉ có Student guard; Mentor identity/authorization implementation chưa có. Middleware contract allowlist cũng chưa khai báo path #65.
- Database evidence: `DB_UNICA_TABLES.md` đánh dấu #65/#67 SELECT `DESIGN_ONLY` trên quan hệ enrollment/progress. Legacy `DB.sql` có BIGINT `courses`, `enrollments`, `users`, `lessons`, `lesson_progress`; status/unique/null rules còn thiếu hoặc khác ERD. V1-PILOT `02_study_db.sql` dùng UUID/versioned `course_enrollments`, `lesson_progress_facts`, `progress_snapshots`; đây là mô hình khác, không phải live-schema proof và không khớp contract int64.
- Response/runtime discrepancy: `Page<Course>` không chứa học viên hoặc tiến độ; `PageMeta` không có query `page/size`. API Guidelines kỳ vọng error `data:null`, còn current `error_response` chuyển `None` thành `{}`. Chưa có route để kiểm chứng endpoint-specific behavior.

## SOURCE_TRACE

```text
AC-26 Mentor mở dashboard -> API #65 kiểm tra course/permission -> candidate đọc learner enrollments và lesson progress trong course -> aggregate một dòng mỗi learner -> response contract hiện khai báo Page<Course> nhưng không thể biểu diễn progress -> UI gọi API #66 cho learning events, rồi API #67 khi drill-down learner -> render dashboard
```

## PLAN BEFORE DD AUTHORING

1. Giữ nguyên direct contract row #65: `GET /api/v1/mentor/courses/{course_id}/progress`; Bearer JWT / Mentor; `course_id:int64!`; không body/query; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Page<Course>>`; lỗi đúng 401/403/404/500. Không thêm endpoint, query, field trực tiếp vào catalog hoặc business code.
2. Bám diagram AC-26: API #65 chỉ đảm nhiệm enrollment/progress summary; không gộp learning-event analytics của #66 hoặc student detail của #67 vào response/side effect #65. #66/#67 DD chưa được tạo trong phiên này.
3. Candidate access check dùng legacy `courses.id/mentor_id`, cùng precedent #46/#62, nhưng đánh dấu `DERIVED`; Mentor JWT-to-user mapping, assigned-course policy và live schema vẫn `SOURCE_REQUIRED`.
4. Candidate read model dùng `enrollments` + `users` + `lessons` + `lesson_progress`. Dùng một dòng mỗi `user_id` để tránh nhân bản learner nếu có enrollment trùng. Không tự lọc `enrollments.status` vì AC-26 không chốt status semantics. Chỉ dùng lesson `PUBLISHED` làm denominator trong phương án đề xuất vì public curriculum #9 lọc published lesson; đây là `DERIVED`.
5. Đề xuất logic đơn giản, đánh dấu `DERIVED`: mỗi learner có `student:UserSummary`, `completed_lessons`, `total_lessons`, `progress_percent`; `completed_lessons` đếm lesson thuộc course có `lesson_progress.status='COMPLETED'`; `total_lessons` đếm published lesson của course; `progress_percent = floor(sum(COALESCE(progress_percent,0)) / total_lessons)`, bằng `0` nếu không có published lesson. Missing progress row được xem là 0 chỉ trong candidate formula. Không đưa candidate schema này thành contract DIRECT.
6. Giữ `ApiEnvelope<Page<Course>>` như contract trực tiếp, lập đủ từng field `Course`/`PageMeta` trong Response Source Matrix và ghi `DISCREPANCY`. Đưa `Page<MentorStudentProgress>` làm candidate response đề xuất riêng để review; Page request chưa có `page/size`, nên đề xuất một trang đầy đủ (`page=1`, `size=total`, `total_pages=1` nếu có item; rỗng trả page thành công) là `DERIVED`, cần review về scale.
7. Đề xuất 404 nếu course không tồn tại, 403 nếu course tồn tại nhưng Mentor không có quyền; đây là nhánh `DERIVED` theo codes catalog. Giữ câu hỏi về privacy policy/order và identity mapping.
8. Tạo 8 sheet theo template cùng `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md` tại `apps/study-server/docs/dd/65_mentor_course_progress/`. `07_table.md` ghi `N/A — READ-ONLY API`. Không có `BUSINESS_CODE_DELTA.md`, ZIP, source/schema/catalog/diagram edits.
9. Kiểm tra exact contract/error set; direct-vs-derived response conflict; field mapping; JSON examples; 11-file manifest; front matter; appendix template hash/equality; links/anchors; Markdown tables/fences/whitespace; `git diff --check` cho tracked changes. Không chạy application tests vì docs-only.
10. Ghi macro-review nhóm #65–#67 là pending, không đánh dấu hoàn thành trước khi #66/#67 DD tồn tại. Handoff sang API #66.

### API Requirement Matrix

| API ID | Method/path | Actor/auth | Input | Success/response | Errors | Basis/status |
|---|---|---|---|---|---|---|
| #65 | `GET /api/v1/mentor/courses/{course_id}/progress` | Mentor / Bearer JWT | `course_id:int64!`; no body/query | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Page<Course>>` | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR` | Catalog + AC-26 DIRECT; business payload/query/data semantics partially `DISCREPANCY` / `DERIVED` |

### Request Usage Matrix

| Request field | Source | Mapping step | Validate | SQL/use | Branch/response | Gap |
|---|---|---|---|---|---|---|
| `Authorization` | Header | 0 | Bearer JWT and Mentor role per catalog | Candidate principal for course scope | 401/403; not returned | No Mentor guard/identity binding in current source. |
| `course_id` | Required path | 1, 2 | Required int64 per catalog; no extra range rule | Candidate `courses.id` lookup; scope enrollment/progress | 404/403 or data query | Legacy BIGINT candidate; live mapping and 403/404 order unresolved. |
| Query/body | None | N/A | N/A | None | No pagination/filter input is declared | `PageMeta` still requires page/size/total fields. |

### Query Matrix

| Query ID | Purpose/type | Source/columns | Join/predicate | Group/order/pagination | Result/branch |
|---|---|---|---|---|---|
| Q1 | Course existence and access / SELECT candidate | Legacy `courses.id`, `courses.mentor_id` | `c.id=:course_id`; candidate `c.mentor_id=:mentor_id` | N/A | Missing→404; existing inaccessible→403 are DERIVED. |
| Q2a | Learner roster / SELECT candidate | `enrollments.course_id`, `enrollments.user_id` | `e.course_id=:course_id`; no status predicate until approved | Deduplicate by `user_id` | Base learner set; enrollment schema DESIGN_ONLY. |
| Q2b | Student projection / SELECT candidate | `users.id`, `users.full_name`, `users.avatar_url` | `u.id=e.user_id` | `u.full_name ASC, u.id ASC` candidate | `UserSummary` candidate; row integrity/role filter unresolved. |
| Q2c | Lesson denominator / SELECT candidate | `lessons.id`, `lessons.course_id`, `lessons.status` | `l.course_id=:course_id`; candidate `l.status='PUBLISHED'` | Count per course | PUBLISHED denominator derived from public curriculum; not direct AC-26 rule. |
| Q2d | Learner progress / SELECT candidate | `lesson_progress.user_id`, `lesson_id`, `status`, `progress_percent` | Left join by learner and published lesson | Group by learner; aggregate formula in Plan item 5 | Missing progress row contributes 0 in proposal; enums/schema unverified. |

### Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | GET is read-only | No INSERT/UPDATE/DELETE | `N/A — READ-ONLY API` |

### Response Source Matrix

| Response field | Type | Source | Transform/rule | Status/gap |
|---|---|---|---|---|
| Envelope | `success`, `businessCode`, `message`, `data`, `meta`, `traceId` | Reusable `ApiEnvelope<T>` | Success branch; trace per shared convention | DIRECT schema; endpoint absent. |
| `data.items[]` | `Course[]` | Catalog reusable schema | Preserve catalog type | DIRECT contract, but progress/roster mismatch. |
| `data.items[].id` | int64 | Candidate `courses.id` | Direct candidate | Not a learner row; does not resolve progress semantics. |
| `data.items[].title` | string | Candidate `courses.name` | `name → title` | Candidate only; irrelevant to class progress. |
| `data.items[].description` | string? | Candidate `courses.description` | Direct optional mapping | Nullable semantics candidate. |
| `data.items[].thumbnail_url` | uri? | Candidate `courses.thumbnail_url` | Direct optional mapping | Nullable semantics candidate. |
| `data.items[].price` | decimal-string | Candidate `courses.price` | Decimal string serialization | Candidate only. |
| `data.items[].status` | CourseStatus | Candidate `courses.status` | Direct enum projection | Enum unconfirmed. |
| `data.items[].mentor` | UserSummary | Candidate `users` via `courses.mentor_id` | Fields id/full_name/avatar_url? | Candidate only; no learner/progress data. |
| `data.items[].category` | Category? | No approved course-category relation | Omit if absent only per optional schema | `SOURCE_REQUIRED`; no invented join. |
| `data.pagination` | PageMeta | Page schema | `page,size,total,total_pages` | DIRECT schema; request has no page/size. |
| Candidate `student` | UserSummary | Legacy `users` via enrollment | One unique learner | DERIVED alternative response only. |
| Candidate `completed_lessons` | int32 | `lesson_progress.status` + published `lessons` | Count completed lessons | DERIVED; enum/query not canonical. |
| Candidate `total_lessons` | int32 | Published `lessons` | Count course lessons | DERIVED from API #9 visibility. |
| Candidate `progress_percent` | int32 | `lesson_progress.progress_percent` | Average across published lessons, floor; empty denominator→0 | DERIVED recommendation; contract update required. |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #65 source | Current router/module/test inventory | `UNWIRED / NOT_FOUND` | DD is design-only. |
| Contract response | Catalog `Page<Course>` vs AC-26 class progress | `DISCREPANCY` | Existing `Course` has no learner/progress fields; preserve direct contract and show derived proposal separately. |
| Pagination | `PageMeta` but no page/size input | `DISCREPANCY / DERIVED` | Candidate full single-page response is unbounded; confirm or revise request/contract. |
| Mentor access | AC precondition + legacy `courses.mentor_id`; no Mentor guard in source | `DERIVED / SOURCE_REQUIRED` | Direct-owner rule and JWT identity mapping need approval/source. |
| Progress schema | Legacy BIGINT tables vs V1-PILOT UUID/versioned facts/snapshots | `DISCREPANCY / NOT_VERIFIED` | Do not treat either checked-in artifact as live schema. |
| Progress formula/status | AC-26 says aggregate enrollment/progress; no formula/status policy | `DERIVED` | Candidate formula disclosed; enrollment status, lesson visibility and zero-lesson behavior need review. |
| Error envelope | Guidelines say error data null; current helper returns `{}` for absent data | `DISCREPANCY` | Show expected and current forms separately. |

## CHANGES

- Files changed: apps/study-server/docs/dd/65_mentor_course_progress/ (8 template sheets + 3 reports), this worklog, and refreshed .agents/worklog/2026-10-24/inventory-study-api-dd-counts.md.
- CONTEXT_UPDATES: None; no source/schema/catalog/diagram/context page was changed.
- No ZIP, runtime code, application test, schema migration, catalog edit or diagram edit was created.
- Assumptions remain labeled DERIVED; unresolved contract and schema questions remain open.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/review | Deno selector returned docs worklogs #48, #49 and #50; all were read in full; the plan preceded authoring. | VERIFIED |
| Catalog/diagram/source/schema | Read API #65 catalog row, AC-26 flow, current router/module/test inventory, legacy DDL, V1-PILOT DDL and related DD evidence. | VERIFIED_STATIC_ONLY |
| Source wiring | No API #65 route declaration, module view or focused test file was found. | VERIFIED_STATIC_ONLY |
| DD manifest/front matter/template | Exact 11 Markdown files; 8/8 front matter and registered-template appendix suffixes match. | VERIFIED |
| Contract/error set | Method/path/auth/path input/no body-query/response/status and exact 401/403/404/500 set checked. | VERIFIED_STATIC_ONLY |
| Response and mapping matrices | Every direct Course/PageMeta field is represented; derived student-progress proposal remains separate and marked DERIVED. | VERIFIED_STATIC_ONLY |
| JSON/Markdown/links | Two JSON samples parse; relative links resolve; tables, fences and whitespace pass. | VERIFIED |
| git diff --check | No diagnostics; custom validation covered the new untracked DD folder. | PASS |
| API inventory after #65 | Catalog 103; DD folders 65 (#01–#65), missing 38 (#66–#103); 12 route+view source pairs and 91 without. | VERIFIED_STATIC_ONLY |
| Runtime tests | Not run; docs-only. | NOT_RUN |
| Context validator | Not applicable; no context page or manifest changed. | NOT_APPLICABLE |

## HANDOFF

- Remaining blockers: Response schema conflict, pagination, Mentor identity/assignment, live progress schema/status/formula, empty roster behavior and error envelope remain open in the draft.
- Next owner/action: DD #66 and #67 now exist; AC-26 group macro-review is recorded below. Continue at API #68.

## GROUP_MACRO_REVIEW — 2026-10-24

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` at document/source review level; see the [API #65 report](../../../apps/study-server/docs/dd/65_mentor_course_progress/VERIFICATION_REPORT.md) and [API #67 report](../../../apps/study-server/docs/dd/67_mentor_student_progress/VERIFICATION_REPORT.md).
- Findings: #65 roster summary, #66 course event aggregate and #67 selected-Student lesson detail stay separate; no API-to-API call. #65/#67 candidate lesson denominator and floor-average formula match. #66 event-active Student count is not enrollment count and must not use progress state as event source.
- Shared gaps: all direct response schemas are Page<Course> without page/size inputs; Mentor identity/course assignment/privacy, live BIGINT-vs-UUID schema, enrollment eligibility, progress duplicate/status/formula rules, error `data:null` vs helper `{}` and middleware allowlist remain open.
- No runtime tests were run; macro-review is document-level only.

