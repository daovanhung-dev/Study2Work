# Plan Result — Study API #55 Lấy bài làm và rubric Mentor

**Trạng thái plan:** `PLAN_EXECUTED — DD draft and focused static verification complete`
**API:** `GET /api/v1/mentor/submissions/{submission_id}`
**Output folder:** `apps/study-server/docs/dd/55_mentor_submissions_detail/`
**Phân loại:** `docs` · scope `server-study` · không có dependency cross-scope
**Basis:** Catalog/AC-23 `DIRECT`; query, Mentor ownership và integrity handling `DESIGN CANDIDATE / DERIVED`
**Deliverable:** 8 Markdown sheets + 3 reports; theo Study workflow không tạo ZIP.

## Nguồn và coverage

| Source | Evidence used | Status |
|---|---|---|
| `docs/lists/list_api.md` | API #55, neighboring #54/#56/#57, `Submission`, `UploadAsset`, `Assignment`, success/error codes | `DIRECT` |
| `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md` | AC-23 actor, precondition, postcondition, four API order | `DIRECT` |
| `apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio` | All AC-23 nodes/edges: #54 list → choose → #55 reads Submission + files + rubric → #56 grade/status → #57 feedback | `DIRECT`; rubric schema not provided |
| `apps/study-server/docs/diagrams/DB_UNICA_TABLES.md` and `DB_UNICA_ERD.drawio` | Candidate `assignment_submissions → assignments → courses`; submission fields | `DESIGN_ONLY` |
| `infra/postgres/study-server/DB.sql` | Legacy candidate BIGINT `assignment_submissions`; one nullable `file_url`; nullable assignment/user FKs | Artifact only; not live-schema proof |
| `infra/postgres/02_study_db.sql` | V1-PILOT UUID rubrics linked to UUID assessments; no relation to legacy assignment submissions | Separate model; not mapped into this API |
| Prior DDs #35, #36, #46, #47, #54 | Submission/file gaps, Student detail privacy, Mentor ownership candidates and current AC-23 handoff | Reference; unresolved questions retained |
| Current Study source/context | Router, auth/JWT, middleware, error response, route/test inventory, scope pages | No #55 route/module/test; Mentor guard absent |
| `contracts/api-guidelines/README.md` | Envelope fields, error `data:null`, trace convention | Expected behavior; current helper returns `{}` for absent error data |
| Registered `createDD-markdown` + eight templates | Registry wiring, headings, metadata and template appendices | `WIRED`; templates fingerprinted |
| Scoped archive scan | No ZIP/XLSX/XLSM under Study docs/template source | No archive source to process |

## API Requirement Matrix

| API ID | Method/path | Actor/auth | Input | Success | Errors | AC-23 role |
|---|---|---|---|---|---|---|
| #55 | `GET /api/v1/mentor/submissions/{submission_id}` | Mentor / Bearer JWT | `submission_id:int64!`; no query/body | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Submission>` | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR` | Read one selected submission before grade #56 and feedback #57 |

## Request Usage Matrix

| Request item | Data Mapping use | Validation | Response use | Gap |
|---|---|---|---|---|
| `Authorization` | Decode access JWT; require Mentor | Bearer and valid token; current guard only accepts Student | None | Mentor guard/policy not wired |
| `submission_id` | Lookup candidate `assignment_submissions.id` | Required int64; no bound/invalid-path behavior declared | `data.id` | Catalog error set has no 400/422 |
| Query/body | N/A | N/A | N/A | None declared by catalog |

## Query Matrix

| Query | Type | Candidate relation/columns | Purpose | Basis/gap |
|---|---|---|---|---|
| Q1 | SELECT | `assignment_submissions s` LEFT JOIN `assignments a` by `a.id=s.assignment_id`, LEFT JOIN `courses c` by `c.id=a.course_id`; filter `s.id=:submission_id`; select Submission candidate fields and authorization relation | Find one row; check Mentor access before response serialization | Legacy design candidate; nullable FKs require orphan handling; direct owner `c.mentor_id=:mentor_id` is `DERIVED` |
| Q2 | SELECT | No approved UploadAsset association/metadata source | Resolve `files[]` | `SOURCE_REQUIRED`; no conversion from single `file_url` |
| Q3 | SELECT | No assignment → rubric relation; V1-PILOT rubrics use UUID `assessment_id` | Resolve diagram rubric | `SOURCE_REQUIRED`; no cross-model join |

## Mutation Matrix

| Operation | Target | Result |
|---|---|---|
| INSERT/UPDATE/DELETE | N/A | Read-only; `07_table.md` will state `N/A — READ-ONLY API` |

## Response Source Matrix

| Response field | Candidate source | Rule/gap |
|---|---|---|
| Envelope `success`, `businessCode`, `message`, `meta`, `traceId` | API envelope/current Study conventions | Exact branch code; error data null-vs-empty discrepancy |
| `data.id` | `s.id` | BIGINT candidate; live schema unverified |
| `data.assignment_id` | `s.assignment_id` | Required logical field; nullable in legacy DDL |
| `data.user_id` | `s.user_id` | Required logical field; nullable in legacy DDL; no extra profile join |
| `data.content` | `s.content` | Optional; null/omit policy unspecified |
| `data.files[]` and `UploadAsset` children | No approved source | `SOURCE_REQUIRED`; do not fabricate assets or `[]` |
| `data.status` | `s.status` | Enum members/lifecycle unspecified |
| `data.submitted_at` | `s.submitted_at` | Timestamp zone/precision unspecified |
| `data.score` | `s.score` | Candidate NUMERIC→decimal-string; API #56 body is `int32`, range unresolved |
| `data.feedback` | `s.feedback` | Optional; null/omit and Student disclosure timing unspecified |
| Rubric | No field in reusable `Submission` | Diagram/schema discrepancy; do not silently extend response |

## Quyết định và trình tự authoring

1. Giữ nguyên contract #55 và error set; không thêm field, query, 422 hay business code.
2. Giữ chuỗi AC-23 #54 → #55 → #56 → #57; #55 đọc, không lưu grade/feedback.
3. Kế thừa các gap từ #35/#36/#46/#47/#54 về files, Mentor identity/course scope, schema và grade disclosure.
4. Đề xuất lookup `assignment_submissions` qua assignment/course bằng parameter binding; direct owner là candidate DERIVED; check quyền trước khi trả dữ liệu.
5. Giữ row không tồn tại → 404, role/course không có quyền → 403; orphan/null FK → 500 là candidate integrity handling, cần xác nhận.
6. Không map `file_url` thành `UploadAsset[]`; không nối V1-PILOT rubrics UUID vào legacy submission BIGINT; giữ rubric conflict và không thêm vào response schema.
7. Điền Data Mapping và bốn ma trận trước khi hoàn thiện Request/Response; mọi field, condition, column và error một row riêng.
8. Tạo 8 sheet từ template, giữ nguyên phụ lục template byte-for-byte; tạo `OPEN_QUESTIONS.md` và `VERIFICATION_REPORT.md`.
9. Chạy static checks trên 11 file, đối chiếu diagram, field/code set, JSON, link, table/fence/whitespace, template suffix và `git diff --check`; không chạy application tests cho docs-only.
10. Cập nhật inventory; để AC-23 macro-review #54–#57 ở trạng thái pending đến sau API #56/#57.

## Các điểm cần xác nhận được giữ trong Draft

- Rubric được diagram yêu cầu nhưng `Submission` response schema không có; không thấy quan hệ phù hợp trong legacy schema.
- Assets array thiếu identity/metadata/association; candidate chỉ có một `file_url`.
- Mentor JWT/assignment scope; direct owner và chính sách 403/404 chưa được duyệt.
- Legacy FK nullable trái table guide; live schema chưa xác minh.
- SubmissionStatus, null/omit, timestamp/decimal serialization, grade disclosure và `score` của API #56 chưa khớp kiểu.
- Invalid path và error envelope có khác biệt giữa contract và current middleware/helper.
- Handoff AC-23 từ #54 sang #55 chưa khớp vì #54 response contract đang singular dù flow cần collection để chọn `submission_id`.

## Kết quả sau khi thực hiện plan

- Đã tạo 8 sheet Markdown cùng `OPEN_QUESTIONS.md` và `VERIFICATION_REPORT.md`; tổng bộ DD là 11 file.
- Static verification đạt cho file manifest, template suffix/front matter, contract/error set, response fields, JSON, relative links, tables, fences, whitespace và `git diff --check`.
- Trạng thái vẫn `Draft — Needs Confirmation` vì các điểm trong mục trên chưa được nguồn/owner chốt; không có runtime, schema hay diagram nào bị sửa.
