# VERIFICATION_REPORT — Study API #65

## Kết quả

- DD status: Draft — Needs Confirmation; direct catalog contract is preserved and the AC-26 response mismatch is explicit.
- Deliverables: 8 template sheets plus PLAN_RESULT.md, OPEN_QUESTIONS.md, and this report; 11 Markdown files total.
- Runtime API #65: locally wired in `app/api/v1.py`, middleware design-contract allowlist, and `mentor/api_65_mentor_course_progress`; focused HTTP tests exist. Runtime returns the local DERIVED progress-page shape, which differs from catalog `Page<Course>`.
- AC-26 macro-review #65–#67: VERIFIED_WITH_OPEN_QUESTIONS after DD #67 was created; see the group review below and [API #67 report](../67_mentor_student_progress/VERIFICATION_REPORT.md).
- Runtime tests: 20 API #65 tests passed; 47 tests passed across APIs #65, #62, and #9; full Study suite: 680 passed. Tests use fake DB sessions and do not verify live schema/deployment.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Selector returned #48, #49, #50; all three docs worklogs were read. Plan was recorded before authoring. | VERIFIED |
| Catalog/diagram | Catalog row #65 and AC-26 sequence were checked; #65 roster progress remains separate from #66 analytics and #67 student detail. | VERIFIED_STATIC_ONLY |
| Source/schema | #65 route/module/tests use the legacy BIGINT candidate. Legacy BIGINT and V1-PILOT UUID/versioned evidence remain separate; live metadata unverified. | VERIFIED_STATIC_ONLY |
| Manifest/front matter | Exact 11-file set; all 8 sheets carry dd_id 65 and Draft status. | VERIFIED |
| Catalog/error set | Exact method/path/auth/path parameter/no body or query/response/200; exact errors 401/403/404/500. | VERIFIED_STATIC_ONLY |
| Response/data mapping | Direct Course/PageMeta catalog shape and local MentorStudentProgress page are shown separately; local mapping remains DERIVED. Read-only table mapping is N/A. | VERIFIED_STATIC_ONLY |
| Template appendix | All 8 output appendices match the registered template suffix byte-for-byte; source template hashes match PLAN_RESULT.md. | VERIFIED |
| JSON/Markdown | Both JSON examples parse; local links resolve; tables have consistent widths; fences balance; trailing whitespace absent. | VERIFIED |
| git diff --check | No diagnostics. Custom checks also covered the untracked DD files. | PASS |
| AC-26 macro-review | #65 summary, #66 events and #67 selected-Student detail are distinct; shared progress formula/denominator and remaining contract/auth/schema/error questions were reconciled at document level. | VERIFIED_WITH_OPEN_QUESTIONS |
| Focused HTTP tests | `uv run pytest -q tests/modules/mentor/api_65_mentor_course_progress` — 20 passed, one upstream Starlette/httpx warning. | VERIFIED_LOCAL_HTTP |
| Linked regression HTTP tests | APIs #65/#62/#9 together — 47 passed, one upstream warning. | VERIFIED_LOCAL_HTTP |
| Full Study suite | `uv run pytest -q` — 680 passed, one upstream Starlette/httpx warning. | VERIFIED_LOCAL_SUITE |
| Ruff | `uv run ruff check app tests` — all checks passed. | VERIFIED_STATIC |
| Context validator | `deno run --allow-read --allow-env --allow-run scripts/validate-agent-context.mjs --skip-drift` reports only missing `.agents/db-admin/**` pages and `apps/db-admin-*` roots/links; no Study Server context errors. Node is unavailable here. | BASELINE_FAILURE_OUTSIDE_SCOPE |

## Output fingerprints — 8 sheets

~~~text
00_Cover.md        d5b730d7f89f4c108022e9653adca49c7283a379baff4f798674286ba3b6245c
01_Lich_su.md      21677792c979a87fc6507caa96fd40aacefc858b5307bc40d832257758137268
02_Overview.md     ae39cabf74a051b7cd77832fae9c91a114bef75006c612f1a3f1088e8278d076
03_Request.md      281cf1bb156c7086273200dad1a4dbe40be90c9be7a6cf8797862566ac3db2b4
04_Response.md     8f7d50d252d3631313e36f8e7d1a462f2ccaf526e8e189f1d6fa0260f676f760
05_Data_Mapping.md b1df5b0bbee856682d5d3b9d0476f7716a2b2549c69a2d27eb820f3a6ae9c0a5
06_Error.md        14cbd3e66b24884709510cc4170e68f71a9bd91a1e0abd64aa635bdaa09706c4
07_table.md        734a6b88a13b596ae5c800e6938b1cb81ce596bca70e22fb3ff8aa7b4ff116bc
~~~

## Remaining owner decisions and verification limits

- Runtime returns Page<MentorStudentProgress>, while catalog direct contract remains Page<Course>; obtain owner approval/update before calling the local shape canonical.
- Request has no page/size, so current full-roster page is unbounded. Mentor assignment/privacy policy, live progress schema/freshness, enrollment filtering and status/formula still need owner confirmation.
- Local error helper emits data:null and API #65 middleware mapping is wired/tested; live DB/deployment remains unverified.

Review [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md), [PLAN_RESULT.md](./PLAN_RESULT.md), and the neighboring [API #62 report](../62_mentor_course_students/VERIFICATION_REPORT.md).

## Macro-review AC-26 #65–#67 — 2026-10-24 (pre-implementation)

Status: `VERIFIED_WITH_OPEN_QUESTIONS` — review tài liệu/source tĩnh sau khi DD #67 tồn tại.

- **Luồng:** Mentor mở dashboard; #65 trả class-level enrollment/progress candidate; #66 riêng course-wide learning-event candidate; UI chọn Student rồi gọi #67. Diagram không mô tả server-to-server calls.
- **Payload trực tiếp:** Cả ba catalog row đều khai báo `ApiEnvelope<Page<Course>>`, không schema nào chứa progress hoặc analytics. Đây là discrepancy nhóm; catalog được giữ nguyên trong các DD. Các PageMeta cũng không có page/size request nên chưa có pagination semantics/bounds.
- **Candidate boundary:** #65 là roster summary; #66 là event aggregate. `students_with_learning_events` đếm Student có event hợp lệ, không đồng nghĩa tổng enrollment của #65. Không dùng `lesson_progress`, `last_accessed_at`, progress snapshots hoặc `last_event_id` để thay event source #66.
- **Progress consistency:** #65 và #67 candidate dùng cùng tập lesson PUBLISHED và cùng formula floor-average; #67 chỉ thêm current state theo lesson cho Student được chọn. Candidate #67 không thêm quiz/assignment vì AC-26 không nêu chúng; API #37/AC-18 là flow khác. Tập eligible enrollment, status, duplicate progress rows, formula, rounding và empty behavior vẫn phải được duyệt.
- **Authorization/data:** Ba API yêu cầu Mentor role và course scope; #67 còn phải xác minh Student thuộc cùng roster eligibility như #65. Mentor principal binding, owner/assignment, privacy-aware 403/404 order và schema live chưa có nguồn.
- **Shared error gap:** Cả ba có direct error set 401/403/404/500. Shared helper trả `data:null`. Tại thời điểm review 2026-10-24, #65–#67 chưa có route/module/focused test; review này không phải runtime verification.

## Runtime follow-up AC-26 — 2026-10-25

- API #65 hiện có local route/module/tests và middleware registration. Response progress và trang full-roster là DERIVED; catalog vẫn khai báo `Page<Course>` và chưa thay đổi.
- API #66 và #67 vẫn chưa wire. Progress facts của #65 không chứng minh nguồn learning-event cho #66.
- Auth/eligibility/formula/error behavior cục bộ của #65 qua HTTP tests với fake DB; live database, deployment, owner approval và pagination bounds production chưa xác minh.

Xem [API #67 report](../67_mentor_student_progress/VERIFICATION_REPORT.md) và open questions của từng DD.

