# GS-05 — Kế hoạch chi tiết

> Ngày lập ban đầu: 2026-11-06; re-audit: 2026-11-07<br>
> Trạng thái: `AUDIT COMPLETE; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`<br>
> Phạm vi phiên: chỉ GS-05; chưa bắt đầu GS-06.

## Re-audit plan — 2026-11-07

- Audit GS-05 only. Preserve the source `screen.png` and `code.html`; verify the HTML-derived render, annotation, JSON/SVG mapping and all hashes before deciding whether any image change is needed.
- Recheck the current inventory row, F02 and G-06, AC-05, API #10 catalog and Draft DD, executable Study Server route/module/test search, API #08 prerequisite source, legacy and V1-PILOT discussion/rating schema evidence, and Study Web tree/wiring.
- Review every existing element and event against the HTML DOM. Make event input, trigger/type, precondition, processing, output and exception explicit; retain expected-vs-current gaps for loaded reviews/replies, rating, pagination and course errors.
- Update only evidence-backed GS-05 documentation, inventory and tracker facts; preserve `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, and `RUNTIME NOT VERIFIED` while contract/design blockers remain.
- Run static artifact/marker/link/tracker/whitespace checks; do not run application tests or claim app runtime/live DB verification. Do not start GS-06 in this session.

## 1. Phạm vi và nguồn

- Screen ID/tên: **GS-05 — Đánh giá và thảo luận công khai (Tab)**; actor `Guest`; route đề xuất `/courses/:courseId?tab=reviews`.
- Expected từ `apps/study-client/docs/list_screen.md`: AC-05; API #08/#10; list review và reply; reuse #08, gọi #10 phân trang; course 404 phân biệt với review rỗng; không hiển thị sao trung bình khi không có rating contract; liên kết GS-03; states loading/empty/ready/error.
- Original `screen.png`: 1280×1024, SHA-256 `f6e8edf78933bc5b54a20bb135ce11f3a7b5937c368dd6a583356c2aabc90538`, 24 colors, entropy 0.350263; nhìn thấy chủ yếu nền trống và dải footer đen, không có review card nhận diện được.
- `code.html`: SHA-256 `e7072487f43a4e19e5faf9593f633b7db3d05f98a6806f753feca1fb59b49512`; static guest-facing empty-review document với header, breadcrumb, icon, H1, empty copy, return CTA và footer. Không có review/reply, loading/error, pagination, route/API logic; toàn bộ anchors dùng `href="#"`.
- Preserve hai original file. Sau plan này, render HTML thành asset riêng để kiểm tra nội dung/layout; nếu faithful và rõ hơn PNG, dùng render làm nền annotation và ghi nguồn. Không thay thế `screen.png`.
- Candidate marker groups (finalize against rendered image before annotation): header brand/nav; auth links; breadcrumb; empty icon; H1; empty message; return CTA; footer brand; footer nav. Không đánh số review/rating elements không có trong source.

## 2. Expected/current và API #10 evidence

| Hạng mục | Expected/design source | Current evidence | Tác động |
|---|---|---|---|
| Route/orchestration | GS-03 course ID → GS-05; inventory nói reuse #08 rồi #10 paginated. F02 nói lazy tab; AC-05 gọi #08/#09/#10 trước render. | Study Web source/router/cache không có; HTML links chỉ `#`. | Route, cache key/freshness/direct-entry/miss và eager-vs-lazy chưa giải quyết. |
| Course gate | API #08 course PUBLISHED mới được hiển thị; GS-05 row yêu cầu course 404 khác reviews empty. | API #08 có route/view/query/validator/test source; GET current source lọt qua PUBLISHED course và trả 404 nếu malformed/missing/unpublished. | API source-backed nhưng không chứng minh client cache/navigation hoặc deployment. |
| Reviews endpoint | Catalog: public GET `/api/v1/courses/{course_id}/reviews`, `page?:int32`, `rating filter?:string`, `ApiEnvelope<Page<Discussion>>`, 200/404/500. | Không tìm thấy API #10 route/module/test trong `apps/study-server/app` và `tests`. Current #97/#98 are ADMIN-only reported-discussion queue/detail routes, not a Guest review API. API #10 DD là `Draft — Needs Confirmation`. | #10 là `DECLARED_NOT_RUNNABLE`; không mô tả như hiện đang được gọi hoặc thay bằng endpoint moderation. |
| Review/reply model | API DD dự kiến root discussion + nested replies; public list; empty là HTTP 200; page size 20 trong DD là design-only. | Contract đòi `Discussion.title` nhưng không có source field; current legacy DDL `discussions` chỉ có id/course_id/user_id/parent_id/content/status/timestamps; không có title/rating field. V1-PILOT `assessment_reviews`/`assessment_review_scores` relate to assessment attempts and rubric scores, not course reviews. | Không tự sinh title, star/rating, aggregate, rating filter predicate hoặc public visibility rule; neither DDL proves live schema. |
| Visibility | API DD dự kiến `status='ACTIVE'` cho roots/replies nhưng gọi đó là assumption. | Chưa có API runtime; current DDL không chứng minh public moderation policy hoặc live schema. | BE/Product cần chốt moderation/visibility trước khi implement list. |
| Source UI | Expected list + replies and states. | Static HTML duy nhất là empty-like state; tất cả links `#`; không có data binding/JS. | Loaded/error/pagination designs chưa có nguồn. |

### API #10 Draft DD constraints giữ nguyên

- Request design: public GET, no Bearer/body; required `course_id:int64`; optional `page:int32` default 1 (min 1 design-only); “rating filter” chưa có physical query-name/semantics. `size` không được API catalog/DD khai báo là client parameter.
- Draft response design: `ApiEnvelope<Page<Discussion>>`; list items map id/course_id/title/content/author/status/comments. Author exposes id/full_name/nullable avatar_url. Reply has id/discussion_id/content/author/created_at. `title` source is TBD; response has no rating or aggregate field.
- Draft pagination: size 20, `created_at DESC, id DESC`, count only root discussion rows; all are draft conventions, not current API behavior.
- Draft errors follow declared 404 `DESIGN_RESOURCE_NOT_FOUND` and 500 `DESIGN_INTERNAL_ERROR`; malformed optional `page`/rating behavior has no declared 422 and remains TBD.
- API DD assumes `parent_id IS NULL` roots, `status='ACTIVE'` visibility and active child replies. It flags these as needing confirmation; do not promote them to approved business rules.

## 3. Trace source to inspect before authoring

- Inventory/flow: GS-05 row, F02, AC-05, G-06 and API index in `apps/study-client/docs/list_screen.md`; corresponding AC-05 cells in `apps/study-server/docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio`.
- Current UI: `screen.png`, `code.html`; check app source inventory again to retain `UNWIRED` status.
- API #08 current trace: route → validator/view/query/model/test source; only used as existing public-course gate/prerequisite.
- API #10 declaration: `docs/lists/list_api.md` and `apps/study-server/docs/dd/10_courses_reviews/{02_Overview,03_Request,04_Response,05_Data_Mapping,06_Error,07_table}.md`; search executable route/module/tests and current DDL for discussions/title/rating.
- DDL and context: `infra/postgres/study-server/DB.sql`, `infra/postgres/02_study_db.sql`, `.agents/server-study/database.md`; the V1-PILOT `assessment_reviews` tables are assessment-grading records, and neither checked-in DDL proves production/live schema.

## 4. Planned DD structure and event coverage

1. Overview: Guest, proposed route, pre/postconditions, related GS-03, distinct DD/implementation/runtime statuses.
2. Expected vs current flow and image metadata/hashes.
3. One row per annotation marker; mark loaded review card, replies, pagination, rating and errors as absent from current static UI.
4. Events: initialize/resolve course gate and invoke declared #10 only after contract is runnable; 200 ready mapping (design-only); 200 empty; #10 404/500; pagination input/handoff; back to GS-03; static header/footer links. No review create/reply action unless a source/contract requires it.
5. API comparison: API #08 current source versus #10 catalog/Draft DD; no #10 runtime claims. Distinguish declared contract fields from missing source fields.
6. States/navigation/accessibility constraints, AC-05 eager vs F02 lazy, cache unresolved, acceptance and blocker list.

## 5. Acceptance checklist

1. [x] This plan exists before creating render, annotation or DD.
2. [x] Render HTML separately to `screen_rendered.png`; preserve original PNG/HTML and record hash/dimensions.
3. [x] Finalize ordered unique marker map from rendered/current visible elements; no markers for absent loaded UI.
4. [x] Create SVG overlay and `screen_annotated.png`; visually inspect for mapping, legibility and overlap.
5. [x] Write `GS-05.md` with full trace, each element, event input/process/output/error, state transitions and linked screen handoff.
6. [x] Static audit JSON/IDs, DD rows, links, hashes, image sizes, SVG/marker bounds, inventory counts/artifact totals and `git diff --check`; do not run tests.
7. [x] Update global tracker and worklog; statuses are `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED` because API #10, schema/title/rating/visibility and Study Web wiring are unresolved.

### DD READY gates still unresolved

- API #10 has no executable route/module/test; DD stays Draft — Needs Confirmation.
- Discussion title and rating/aggregate source are missing; literal rating query name/semantics unresolved.
- Public roots/replies visibility and moderation rules are assumptions; checked-in DDL/live schema do not establish approval.
- No visual/interaction design for loaded review cards, replies, pagination, loading/error states.
- AC-05 eager request sequence conflicts with F02 lazy tab; #08 cache policy/direct-entry behavior is missing.
- Study Web remains `UNWIRED`; proposed routes and `href="#"` anchors are not runtime evidence.

## Re-audit result — 2026-11-07

- API #08 current route is public and gates on a PUBLISHED course; its path annotation is `str`, while the API catalog declares int64, and the shared parser does not enforce signed-int64/positive bounds. Focused fake-session test source was read but not run.
- API #10 remains catalog/Draft only with no current route/module/test or generated Study OpenAPI. Existing #97/#98 routes are ADMIN discussion moderation and do not provide Guest course reviews. Draft title, rating/filter/aggregate and ACTIVE root/reply rules remain unresolved.
- The legacy `discussions` candidate has no `title` or course-rating fields. V1-PILOT assessment-review tables relate to assessment attempts and rubric scores, not course reviews. Live schema remains unverified.
- AC-05 aggregate/eager request sequence and 404/403 course branch remain distinct from F02 lazy-tab, inventory #08 cache reuse and current #08 404 behavior. Keep these as blockers.
- Preserved `screen.png` and `code.html`; verified recorded hashes and 1280×1024, 1440×1200 and 3040×2400 dimensions. Visual review found the original near blank, the HTML render readable, and nine gutter markers clear. JSON marker sequence maps 1:1 to DD rows and SVG labels/centers; SVG embeds the exact rendered PNG.
- Re-audit made element types/positions explicit and all eight events specify event type, trigger, precondition, input, processing, output and error/exception handling. Local links resolve; 83 inventory IDs match tracker rows and screen folders; authored files are whitespace-clean; scoped `git diff --check` passed.
- `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. No application tests, runtime or live database were run. GS-06 remains a separate session.
