# ME-09 — Kế hoạch Detailed Design: Danh sách bài cần chấm

> **Plan status:** COMPLETE — recorded before marker map, annotation and screen DD; static artifact audit passed.
> **Screen status dự kiến:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.

## 1. Phạm vi và nguồn

- Phiên này chỉ xử lý **ME-09**. ME-10 chỉ được ghi là đích handoff, không author DD cho màn hình đó.
- Phân loại: `primary_task_type: docs`; `secondary_task_types: [test]`; `project_scopes: [web-work, server-study]`; cross-scope dependency: API #54 response `data.items[].id` → proposed ME-10 path `submissionId` → API #55 detail.
- Expected behavior lấy từ [`list_screen.md` ME-09](../../../list_screen.md#L169), F09 và AC-23: Mentor xem danh sách, lọc theo course/status, chọn một submission để sang ME-10. Inventory đánh dấu response cardinality #54 bị chặn.
- Source review: `.agents/web-work/study/AGENTS.md` và `INDEX.md` ghi Study Web `UNWIRED`; current checkout không có editable source/package/router. `.agents/web-study/design.md` là intended target, không phải runtime evidence.
- Skill registry `.agents/context-manifest.json` loại trừ `web-ui-only-dd` khỏi `createDD-markdown`; không có canonical skill cho screen DD này.
- Giữ nguyên `screen.png` (1600×1280, SHA-256 `cc69bf224b53dc95a7900800d16bb626d2bd956d3cf8474db3adb68d3db9f18f`) và `code.html` (SHA-256 `9127d4ce896dbb1347f5ae55c3cf616d9fc5c4bdc351a4f88b8d258e7f320cc8`).

## 2. Expected flow và current trace

### Expected behavior

1. Mentor mở route đề xuất `/mentor/submissions`; bảo vệ route phía UI chưa có source để kiểm tra.
2. ME-09 tải danh sách theo Mentor, mặc định không lọc course, status và page (giá trị UI mặc định chưa được contract xác nhận).
3. Mentor có thể chọn course/status và theo inventory xem được deadline/owner; inventory chưa xác định API bổ sung hoặc quy tắc ánh xạ cho các trường này.
4. Mentor chọn một hàng; ME-09 truyền ID sang ME-10. F09 xác định tiếp #55 detail, rồi #56 grade và #57 feedback trên ME-10.

### Current API #54 source

- `GET /api/v1/mentor/submissions`; bearer role `MENTOR` được xác minh trước DB.
- Query: `course_id?: int64` dương; `status?: string` khớp chính xác; `page: int32` dương, mặc định 1. Kích thước trang cố định 20.
- Tất cả truy vấn đếm/danh sách lọc `courses.mentor_id` bằng numeric JWT subject. Có `course_id` của Mentor khác → 403; course không tồn tại/no match → 200 page rỗng.
- Đếm và đọc `assignment_submissions` JOIN `assignments`, `courses`, `users`; sắp `submitted_at DESC, id DESC`; file metadata tùy chọn tra exact URL + owner + `SUBMISSION` purpose + course. API là read-only, không commit.
- Success 200 `DESIGN_RESOURCE_RETRIEVED`, envelope `ApiEnvelope<Page<Submission>>`, `data.items` và `data.pagination`; field item gồm `id`, `assignment_id`, `user_id`, `content?`, `files[]`, `status`, `submitted_at`, `score?`, `feedback?`. Null optionals bị loại khỏi JSON; `score` là decimal string. Lỗi truy vấn/ánh xạ 500 `DESIGN_INTERNAL_ERROR`; thiếu/sai auth 401; sai role/owner 403; query constraint 422. Không có nhánh 409 trong source.
- Current test source covers auth, direct ownership, filters, pagination/order, empty page, upload join, malformed rows/errors, bounds and OpenAPI. Tests are inspected only; no test will be run in this session.

### Current UI source

- `screen.png` shows only the empty state. `code.html` also shows that state and contains no result rows, table or response mapping.
- Course selector values are static (`all`, `fe`, `be`, `ux`); status options are static lower-case labels (`pending`, `graded`, `recheck`). Search input suggests assignment search. #54 expects numeric course ID, accepts status as an exact string and has no search query parameter. HTML listeners do not connect any of these controls to #54.
- Refresh only disables/animates locally for 750ms; reset only changes local control values. No fetch, URL state, loading/error rendering or navigation handler exists.
- Empty-state text advertises automatic sync, a 48-hour SLA, standard rubric and a training contact. These are visible design copy only; #54 returns no deadline/rubric/owner/course-title fields and no sync event.

## 3. Discrepancies to preserve in the DD

| ID | Evidence | Required decision / impact |
|---|---|---|
| ME09-B01 | `list_screen.md` still says singular `Submission`; current route/model and AC-23 diagram use `Page<Submission>`. API #54 DD calls collection a DERIVED fallback and remains `Draft — Needs Confirmation`. | API/schema owner must approve collection shape; screen DD cannot silently replace expected contract. |
| ME09-B02 | Screenshot/HTML show empty state only; inventory expects rows with deadline/owner. #54 has neither deadline nor owner/course display names. | Approve loaded-row layout and provide authoritative data/API mapping. |
| ME09-B03 | Static course/status values do not match #54 input constraints or documented status lifecycle; no course options source is specified in ME-09 orchestration. | Approve course option source, exact status values/default and filter serialization. |
| ME09-B04 | Search field has no matching #54 query parameter or current UI event. | Decide remove/disable it or define an API/search contract. |
| ME09-B05 | “Auto sync”, 48-hour policy, rubric and support claims have no #54 data/event source; #55 has no rubric mapping in current source. | Confirm/remove copy and define refresh policy; do not represent these as working behavior. |
| ME09-B06 | API #54 open questions: file URL producer relation, assigned-Mentor access, status/409, nullable relations/timezone/live schema and error-catalog approval. | API/schema owners must close open questions for a stable implementation contract. |
| ME09-B07 | Study Web feature source and route are absent. | No current UI implementation/runtime evidence. |

## 4. Annotation plan

Create 27 sequential markers in visual reading order and one DD element for each. Use 1600×1280 source coordinates and 2× annotated output (3200×2560). Put marker discs in nearby whitespace or component edges; preserve legibility and do not modify either source asset.

| # | Element inventory |
|---:|---|
| 1–8 | Brand; primary nav Overview; Courses; active Grading; Support; Notifications nav; notification bell; Mentor identity/avatar |
| 9–12 | Screen context label; page title; supporting description; automatic-sync badge (design claim) |
| 13–16 | Course filter; status filter; assignment search input; Reset filters |
| 17–20 | Empty-state illustration; empty title; explanatory copy; Reload list action |
| 21–23 | Deadline claim; rubric claim; training-support claim |
| 24–27 | Footer copyright; teacher regulations; evaluation standards; technical support |

## 5. Event and state plan

- `Load`: proposed route entry → obtain authenticated Mentor session and call #54 using approved defaults/filters. Current route guard, token storage, default filter values and UI transport are not wired; distinguish intended flow from source.
- `Change course/status`: validate selected values against approved #54 query. Current static values are not numeric course IDs and status enum is not defined. No production request is specified until decisions close.
- `Input search`: current API has no text query; do not call #54 with an invented parameter. Treat as blocked affordance.
- `Reset`: current prototype restores local values only. Canonical reset defaults and reload semantics remain undecided.
- `Refresh`: current prototype only animates locally. Expected future refresh may call #54, but request/disabled/error/retry behavior needs approval and no autosync claim is made.
- `Select submission`: when a future ready-state row is approved, map response `data.items[].id` to ME-10 `submissionId`; proposed route `/mentor/submissions/:submissionId` is not wired. API #55/score/feedback events belong to ME-10.
- States for DD: `loading`, `empty`, `ready`, `error`, `auth-required`, `access-denied`, `filter-validation-error`, and `refreshing`. Only `empty` is represented by the current screenshot; remaining states are requirements pending approved implementation decisions.

## 6. Verification and completion rule

1. This plan was written before marker map, overlay, annotated image and DD authoring.
2. Created 27 ordered JSON markers and matching SVG IDs; static audit passed uniqueness, bounds and one-to-one mapping to 27 DD element rows.
3. Generated a 2× annotated PNG and visually inspected the full image. Moved marker #4 below the active nav and marker #22 above the policy strip to keep labels/icons unobscured.
4. Wrote ME-09 DD with expected/current split, element/event/state detail, API #54 route→view→query→response trace, ME-10 handoff, blockers and source links.
5. Updated the ME-09 row and current artifact checkpoint in `dd_screens/PLAN.md`; worklog records asset hashes, static audit and `git diff --check`.
6. API tests and screen runtime were not run. No live-schema or Study Web implementation claim is made.

### Result

- `screen.png` and `code.html` hashes match the pre-authoring values.
- Source PNG is 1600×1280; annotated PNG is 3200×2560.
- JSON/SVG contain 27 markers; element map contains 27 unique matching IDs; event sections E01–E09 are sequential; all relative DD links resolve.
- The design/API blockers in §3 remain open; screen status remains `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED`.

**Completion target:** deliver all static screen artifacts while retaining `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` until the listed contract/data/UI decisions are resolved.
