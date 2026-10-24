# Verification Report — Study API #55 Lấy bài làm và rubric Mentor

**Result:** `DRAFT_VERIFIED_WITH_OPEN_QUESTIONS`
**DD status:** Draft — Needs Confirmation
**Output:** 8 Markdown sheets + `PLAN_RESULT.md` + `OPEN_QUESTIONS.md` + this report.

## Source coverage

| Source | Result |
|---|---|
| API catalog | Exact method/path, Mentor Bearer auth, int64 path, `ApiEnvelope<Submission>`, status/code set and reusable fields recorded. Neighboring #56/#57 contracts compared. |
| AC-23 index and diagram | Actor, precondition, postcondition, all nodes/edges and sequence #54 → #55 → #56 → #57 read. Node #55 says Submission + files + rubric. |
| DB table guide and ERD | Candidate relationship `assignment_submissions → assignments → courses`; required FK semantics and submission columns read. |
| Legacy DDL | `infra/postgres/study-server/DB.sql` fields inspected. It permits nullable assignment/user/course FKs and stores one `file_url`; design artifact only. |
| V1-PILOT DDL | `infra/postgres/02_study_db.sql` has UUID `rubrics.assessment_id → assessments.id` and `rubric_criteria`; no relation to legacy assignment submissions. Live DB not queried. |
| Prior DDs | #35/#36 submission field and privacy/file questions, #46/#47 Mentor ownership questions, #54 list-to-detail handoff and shared gaps reviewed. |
| Current runtime source | Router, auth claim parser/Student guard, response helper and middleware allowlist inspected. No #55 route/module/test found. |
| Skill/workflow/template | `createDD-markdown` is registered for `server-study`; Study delivers Markdown only. Eight templates opened and fingerprinted; archive/workbook scan returned no in-scope files. |

## Checks

| Check | Result |
|---|---|
| Catalog request/success/error | PASS — exact GET/path/auth/path type, `ApiEnvelope<Submission>`, 200 and 401/403/404/500; no undeclared status added. |
| Response field coverage | PASS — all Submission and nested UploadAsset fields represented; rubric kept out of response and recorded as contract/diagram discrepancy. |
| AC-23 sequence | PASS — diagram node/edge sequence #54 → #55 → #56 → #57 retained; #55 is read-only. |
| Exact file manifest | PASS — exactly 11 expected Markdown files. |
| Template appendices/front matter | PASS — eight sheets have `dd_id: 55`, Draft status, and byte-identical template appendix suffixes. |
| JSON examples | PASS — success and error examples parse as JSON. |
| Relative links | PASS — all local relative links resolve. |
| Tables/fences/whitespace | PASS — table widths, closed fences, no trailing whitespace; `git diff --check` clean. |
| Source implementation | No API #55 route/module/test found by scoped scan; source-only claim, not runtime proof. |
| Application tests | `NOT_RUN` — documentation-only task, API #55 has no test module. |
| Live DB/runtime | `NOT_VERIFIED` — checked-in artifacts do not prove live schema. |

## Open design decisions

- AC-23 requests rubric but `Submission` response schema does not include it; no assignment-rubric relation is approved.
- `UploadAsset[]` cannot be mapped from a single legacy `file_url`.
- Mentor identity/assignment scope, direct-owner predicate and 403/404 masking need confirmation.
- Legacy nullable FK conflicts with design guide; live schema is unverified.
- Grade score type/range, SubmissionStatus, null/omit and Student disclosure timing need alignment with #56/#36.
- Malformed path and error envelope/middleware mapping have current-source discrepancies.
- API #54 response is currently singular while AC-23 requires a list selection before #55; the #54 cardinality question remains open.

## Template fingerprints

| Template file | SHA-256 |
|---|---|
| `00_Cover.md` | `fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63` |
| `01_Lich_su.md` | `d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e` |
| `02_Overview.md` | `c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6` |
| `03_Request.md` | `37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa` |
| `04_Response.md` | `5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8` |
| `05_Data_Mapping.md` | `11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b` |
| `06_Error.md` | `e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b` |
| `07_table.md` | `4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356` |

## Output fingerprints

SHA-256 values for all DD files except this self-referential report.

| Output file | SHA-256 |
|---|---|
| `00_Cover.md` | `556ad3f14ba37f61c3ca48d00ae8f02ce5cafb33647b188635641dcd2d59e1ce` |
| `01_Lich_su.md` | `b38ba7b7c78e63213b789850319ed872d0eebdbdaf702cf20cb6dcca948ad168` |
| `02_Overview.md` | `7d70b3c7e1e74408db702fde729d92501cf5a07f983604277e2b0c94af8b174a` |
| `03_Request.md` | `25ca9cee95a1a4609f742ae418cdd3ad6eaeccda3c459f0592f87d4681b88fc3` |
| `04_Response.md` | `353f1cf66c521de1c0a3bb63d775d24df63e3ccc660f07bb13fbfec8cb7ed6dc` |
| `05_Data_Mapping.md` | `0bca7081b4b668b247d597ef437970e7f09b5a23cd9710abd7a8aa009d4f9ee2` |
| `06_Error.md` | `49220e4ce99b891a4916c11e97547b520454130f96f26c0f39f9a8deb402b1b2` |
| `07_table.md` | `1632eb9a48a9e797382eb12ce4ed22d096069fb0305dea6d8fa9592b6dee7e69` |
| `OPEN_QUESTIONS.md` | `f5f78853a03ed4f9518e0c84a83d4c9a094acdb3c0e5a01f543a0c427070e778` |
| `PLAN_RESULT.md` | `304ed7d0725bd0ec94cf0465c83606255ea97ff11c9017f293d4096c4eeef96b` |

## Boundary

No runtime code, test, schema, API catalog, AC diagram or `.agents/server-study` context page was changed. AC-23 group review #54–#57 is complete at document level; unresolved rubric, asset and access questions remain open.

## Rà soát vĩ mô AC-23 #54–#57

**Kết quả:** VERIFIED_WITH_OPEN_QUESTIONS.

- Thứ tự diagram nhất quán: #54 list → #55 detail/files/rubric → #56 grade/status → #57 feedback → success.
- Mục đích #54 là lấy danh sách nhưng response catalog là một ApiEnvelope<Submission>; không tự đổi response shape. Nếu cần collection, contract owner phải duyệt cập nhật catalog/schema.
- Diagram #55 nói đọc rubric nhưng reusable Submission không có field này. Request rubric items của #56 chưa có wire key, item schema hoặc persistence legacy được xác nhận.
- API #56 sở hữu mutation score/status; API #57 sở hữu feedback sau khi chấm. #57 không thay đổi score/status candidate.
- Submission.files là file học viên nộp và vẫn thiếu resolver UploadAsset. Không ánh xạ attachments của feedback sang files hoặc assignment_submissions.file_url.
- Candidate direct-owner chung và Mentor JWT identity/assignment còn mở. Foreign keys nullable trong DDL vẫn khác quan hệ required của guide/ERD.
- Error envelope data null/object và dynamic-route business-code mapping là vấn đề wiring tương lai.
- Không chạy runtime test hoặc AC-23 end-to-end.
