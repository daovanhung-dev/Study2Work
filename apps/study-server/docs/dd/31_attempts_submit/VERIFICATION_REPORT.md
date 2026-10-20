# VERIFICATION_REPORT — Study API #31

## Phạm vi

DD-only cho POST /api/v1/attempts/{attempt_id}/submit tại apps/study-server/docs/dd/31_attempts_submit/. Không chạy runtime tests vì API #31 chưa được wire và task không triển khai runtime.

## Nguồn đối chiếu

- docs/lists/list_api.md — API #31 request, response and business-code contract.
- apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md and AC_02_STUDENT_LEARNING.drawio — AC-16 sequence and grading branches.
- apps/study-server/docs/diagrams/DB_UNICA_TABLES.md, DB_UNICA_ERD.drawio and infra/postgres/study-server/DB.sql — candidate attempt/answer grading mappings and schema discrepancies.
- contracts/api-guidelines/README.md — envelope and error conventions.
- .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/ — canonical Markdown template.
- .agents/server-study/workflows/README.md — no-ZIP Study DD policy.
- apps/study-server/docs/dd/29_quizzes_attempts/ and 30_attempts_answers/ — adjacent draft conventions.

## Template fingerprint

| Template file | SHA-256 |
|---|---|
| 00_Cover.md | fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63 |
| 01_Lich_su.md | d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e |
| 02_Overview.md | c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6 |
| 03_Request.md | 37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa |
| 04_Response.md | 5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8 |
| 05_Data_Mapping.md | 11bc77bc0522d3af27b9499114991c881a5dd3210c6f2cb949be088dcc5b |
| 06_Error.md | e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b |
| 07_table.md | 4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356 |

## Output fingerprint

SHA-256 of the nine design sheets (the eight canonical sheets plus the required `quiz_answers` mutation mapping):

| Output file | SHA-256 |
|---|---|
| 00_Cover.md | 74e95b58d72a5ba86fb19836280252d900a26b27d77483d1224cdbfb36ec9d08 |
| 01_Lich_su.md | 5ea7e22ed90dc8b567f79e11b7f43cd330cc9f1d3913fe1c1883233a0ae5b460 |
| 02_Overview.md | c7f5f22651674177f89e1341d9905553392d50090e736f3fda111b01fad7782d |
| 03_Request.md | 9c412c8600de58c092ff2e86848365cdf842a5f3b4da10d56249fbd7987d90ee |
| 04_Response.md | f4a2269e78791dc5720d02941c63e1bfe26787950edb7e60c56dfdc7476c89aa |
| 05_Data_Mapping.md | b47c490495ff2867164e8d27d222b525605fd0d3863c1790c31a483eb280009a |
| 06_Error.md | 381ef1ace4b1ad249b7f8926e573b4d952481a057695f0f2ed7dbb52ca39f4d6 |
| 07_table.md | 8f98b1e544a0aa731196944670eb751a10c6b6dcb6d3562db540fbda706204a4 |
| 08_quiz_answers_update.md | cc688f39fe07232d167154a0030676a95bb30e0d40cd676b2b5b97522128cfae |

## Kết quả kiểm tra

| Check | Result | Status |
|---|---|---|
| Template file set/order | Eight canonical sheets are present in order from `00_Cover.md` through `07_table.md`; an additional table mapping covers the second candidate write target `quiz_answers`. All 12 expected Markdown files are present. | PASS |
| Front matter | All nine design sheets have valid YAML-style front matter and `Draft — Needs Confirmation` status. | PASS |
| Markdown tables | 399 data rows checked; table column counts are consistent. | PASS |
| JSON examples | Both response examples parse as JSON. | PASS |
| Relative links and anchors | 19 relative links resolve; the fragment link resolves to its question anchor. Six explicit question anchors are present. | PASS |
| Contract path/response/error codes | Endpoint, path type, response envelope, success code and all six catalog errors match `list_api.md`; no extra business code is introduced. | PASS |
| AC-16 and candidate mapping | Submit/automatic-grading flow and `PENDING_GRADE`/`GRADED` branches match AC-16. Candidate reads/writes are traced to DB design/ERD/DDL and remain labeled design-only. | PASS |
| DDL discrepancy | The `quiz_answers.is_correct BOOLEAN NOT NULL` requirement and the absence of an API #30 source-defined pre-submit correctness value are recorded in the DD and open questions. | PASS |
| Runtime wiring | Current route/module/test scan found no API #31 implementation: `UNWIRED / NOT_FOUND`. | CONFIRMED |
| Whitespace/conflict markers | No trailing whitespace or merge conflict markers found; `git diff --check` is clean. | PASS |
| Runtime tests | Not run; documentation-only task and API #31 is not wired. | NOT_RUN |
| Context validator | Not required; no agent-context page or manifest changed. | NOT_REQUIRED |

## Kết luận

Static documentation verification passed. Runtime tests were not run because this is a DD-only task and API #31 is not wired. The DD remains `Draft — Needs Confirmation` pending the decisions in `OPEN_QUESTIONS.md`.
