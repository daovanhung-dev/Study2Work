# Verification Report — Study API #35

## Scope

DD-only deliverable for API #35. No runtime endpoint, live database schema, file storage provider behavior or persistence is claimed as verified. Existing API #27–#34 artifacts are outside this output and must remain unchanged.

## Template baseline

Canonical source: `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD`. Each output sheet retains the appendix from its corresponding canonical template file.

| Template file | SHA-256 |
|---|---|
| 00_Cover.md | fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63 |
| 01_Lich_su.md | d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e |
| 02_Overview.md | c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6 |
| 03_Request.md | 37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa |
| 04_Response.md | 5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8 |
| 05_Data_Mapping.md | 11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b |
| 06_Error.md | e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b |
| 07_table.md | 4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356 |

## Output fingerprints

| Output sheet | SHA-256 |
|---|---|
| 00_Cover.md | 0af58085d5c8e17daf0a96cb471b64dff10339d9d4165c42c34b737f89633041 |
| 01_Lich_su.md | 8080c1718bd20230614b01180631a4b0cfbf22af0ade9d2bb9f16f869a6caa43 |
| 02_Overview.md | 209c9206c78893102c14ec0df266b50c9fa2cbd73879e8abb3cd629ad74113b7 |
| 03_Request.md | c6288a60d37882db2e963f5a6a834232ec51c87f519bd993072e211a5d445150 |
| 04_Response.md | cb3f9a13c4e53dcfda0d1bed19d87374b981599cb2dd8bfce036f60189110017 |
| 05_Data_Mapping.md | 91f3bb798a4448886d412fb6f9e824c1b71e2df322988e9ad6f5d295c8a57dd8 |
| 06_Error.md | 99546a54a906649d5199d41b5ddea3ef0d1f6ecf6af99ddaba85ef9bf02df14c |
| 07_assignment_submissions_insert_update.md | 862813952974122e03ea9c581837728df5975c2ded1ee44abc7b83e1c59fda67 |

## Verification results

| Check | Result | Status |
|---|---|---|
| Required deliverable inventory | Eight sheets and three reports are present; worklog is present at the planned path. | PASS |
| Template appendix and fingerprints | Each sheet has required front matter (`dd_id: 35`, `Draft — Needs Confirmation`); appendix suffix exactly matches its corresponding template. Output SHA-256 values are recorded above. | PASS |
| Catalog contract and error-code set | Method/path, Student Bearer, path/body notation, `ApiEnvelope<Submission>`, HTTP 201 `DESIGN_RESOURCE_CREATED`, and the exact six catalog error codes are represented. No additional error code is defined. | PASS |
| AC/schema discrepancy coverage | AC-17 `SUBMITTED` and `INSERT/UPDATE` are recorded without selecting a branch. Candidate `assignment_submissions` mapping, single `file_url` versus `files:UploadAsset[]`, nullability conflict, and unresolved policy questions are documented. | PASS |
| JSON examples | Request body and all fenced JSON examples parse successfully. | PASS |
| Relative links and anchors | All local Markdown and source links resolve; linked anchors resolve. | PASS |
| Markdown tables and file hygiene | Table widths are consistent per table; code fences are balanced; no trailing whitespace or conflict markers were found in new DD/report/worklog files. | PASS |
| Existing DD #27–#34 preservation | No edits were made to those paths; confirmed during final worktree review. | PASS |
| `git diff --check` | Completed with no whitespace errors. | PASS |
| Runtime tests / live DB / Object Storage | Not run or queried; API #35 is not wired and scope is documentation-only. | NOT_RUN |
| Context validator | Not required; no agent context or manifest changed. | NOT_REQUIRED |

## Limitations

- API #35 route, module, query and tests are not present.
- Assignment access/deadline, request text policy, file-reference schema, submission upsert/retry policy, file persistence and live nullability are unresolved.
- Candidate mappings are design-only and do not claim the live database matches checked-in DDL.
