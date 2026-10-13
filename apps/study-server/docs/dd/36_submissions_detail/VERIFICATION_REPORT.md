# Verification Report — Study API #36

## Result

**Status:** Draft — Needs Confirmation
**Endpoint:** `GET /api/v1/submissions/{submission_id}`
**Verification scope:** Markdown/design artifact only. No runtime tests or live database checks were run.

## Contract and source checks

- API #36 in `docs/lists/list_api.md` matches `GET /api/v1/submissions/{submission_id}`, Student Bearer JWT, `submission_id:int64!`, `ApiEnvelope<Submission>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, and exactly the 401/403/404/500 catalog errors.
- AC-17 diagrams and the API index were reviewed for the submission summary flow. AC-23, DB table notes, checked-in DDL, API guidelines, adjacent DDs #33–#35, and current Study route/auth/test inventory were also reviewed.
- Current API #36 runtime state is recorded as `UNWIRED / NOT_FOUND`.
- Access predicate and 403/404 behavior, score/feedback visibility, `files[]` versus `file_url`, and DB notes-versus-DDL nullability remain open questions.

## Static checks

| Check | Result |
|---|---|
| Eight canonical sheets and three reports present | PASS |
| Canonical template appendix content matches all eight sheets | PASS |
| Front matter contains API #36 identity and `Draft — Needs Confirmation` | PASS |
| JSON examples parse | PASS |
| Markdown table rows have consistent cell counts | PASS |
| Relative Markdown links and checked anchors resolve | PASS |
| No trailing whitespace in DD Markdown files | PASS |
| Catalog method, path, request, response, success and exact error set match | PASS |
| `git diff --check` | PASS; new untracked files also passed the explicit whitespace scan above |

## Template fingerprints

SHA-256 fingerprints of the canonical eight template sheets used for appendix comparison:

| Template sheet | SHA-256 |
|---|---|
| `00_Cover.md` | `fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63` |
| `01_Lich_su.md` | `d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e` |
| `02_Overview.md` | `c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6` |
| `03_Request.md` | `37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa` |
| `04_Response.md` | `5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8` |
| `05_Data_Mapping.md` | `11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b` |
| `06_Error.md` | `e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b` |
| `07_table.md` | `4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356` |

## Output sheet fingerprints

SHA-256 fingerprints of the eight authored DD sheets at verification time:

| DD sheet | SHA-256 |
|---|---|
| `00_Cover.md` | `c5a7afdfccc70d305e6c8cca074ad950d0756109ca67379a3f0c82689945122d` |
| `01_Lich_su.md` | `a1b4482c77a2d878a5cfe8c450c18d9d7cfefc0777174f12557b51c2ddb55035` |
| `02_Overview.md` | `890ed387db34145f107540f43a72945ed4677ddaea26ef390641744aaaaf61c2` |
| `03_Request.md` | `304633cf09902e7f172fc85fd6735b24cc783d15779da740aa0b65c306be5d00` |
| `04_Response.md` | `19f374b23f09fa7a6e2bdb241cd3af7a838f5800cb17f1842dd8345e8b2a1f0e` |
| `05_Data_Mapping.md` | `eceb5056aaac1915e7e59333acc4cb1e6ffac9ac5703f3ca2356c622a360b96c` |
| `06_Error.md` | `43909aef72db33f6a2747dce5a7bf2dd0558749ef14d341846b90458812a1b1f` |
| `07_table.md` | `e41d45987a70e574bb386f9a813b751208cd50769dd7619a60a2f61823de86b1` |

## Limitations

- Runtime behavior is not implemented or verified; this deliverable documents the design contract and current wiring state only.
- No live database was accessed. DB table notes and checked-in DDL are treated as design evidence and their disagreement is recorded in `OPEN_QUESTIONS.md`.
- No ZIP was created, following the Study Server DD workflow.
