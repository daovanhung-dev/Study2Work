# VERIFICATION_REPORT — Study API #40 DD

**Status:** PASS — documentation checks complete; runtime tests not run
**Date:** 2026-10-23
**Scope:** API #40 pack refreshed during the connected #39–#42 group review

## Contract reconciliation

Compared the draft with [`docs/lists/list_api.md`](../../../../../docs/lists/list_api.md) and AC-19 in [`00_AC_API_INDEX.md`](../../../docs/diagrams/AC_UNICA/00_AC_API_INDEX.md).

| Contract item | Catalog / AC-19 | DD result |
|---|---|---|
| Method and endpoint | `POST /api/v1/discussions` | Preserved |
| Actor and auth | Student, Bearer JWT | Preserved |
| Request | `course_id:int64!`, `title:string!`, `content:int64!` | Preserved exactly |
| Response | `ApiEnvelope<Page<Discussion>>` | Preserved exactly |
| Success | HTTP 201 `DESIGN_RESOURCE_CREATED` | Preserved |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR` | Preserved; no additional status/code added |
| Current route state | No discussion route/module found in current Study Server runtime | Marked `UNWIRED / NOT_FOUND` |
| Connected API #39–#42 proposals | Root/access/status, content mapping, response page and comment projection use shared DERIVED proposals | Aligned; confirmation remains open |

The request `content:int64` versus logical `Discussion.content:string` and physical `TEXT`, missing physical `title`, course access, status/visibility, timestamp values, and FK nullability remain open questions. The DD now labels base-10 decimal-string conversion, ACTIVE enrollment/topic status, server timestamps, and a one-item response page as DERIVED proposals only; none is presented as approved runtime behavior.

## Template structure and fingerprints

All eight sheets use the canonical template layout and audit appendix, with `dd_id: "40"`, orders `0–7`, and status `Draft — Needs Confirmation`. Sheet 07 is based on canonical `07_table.md`, specialized to the candidate `discussions` insert mapping. The three supporting Markdown reports and worklog are present; no ZIP was generated.

| Order | Output sheet | Canonical template | Template SHA-256 | Output SHA-256 |
|---:|---|---|---|---|
| 0 | `00_Cover.md` | `00_Cover.md` | `fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63` | `2eaa3cc1b43e9eecff9554fdd504aac5112b3502e02585a698e25428a0844db4` |
| 1 | `01_Lich_su.md` | `01_Lich_su.md` | `d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e` | `2f721e907f9aa6a17a2be2a07d246a5b2cc7f4a01e86e14dc91b0824c2e96b8d` |
| 2 | `02_Overview.md` | `02_Overview.md` | `c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6` | `2c6570b1151e358019210ca82386cc625904912f8ad486fec87d42d08920b766` |
| 3 | `03_Request.md` | `03_Request.md` | `37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa` | `cd50918e6ae1f8d3da9f670b18957db270065d5599f66a6b94b2cb753233d29c` |
| 4 | `04_Response.md` | `04_Response.md` | `5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8` | `4f94486d60aefd6a4522d55dd919c85f8cd830c469490b38bc04d20274c2b9e9` |
| 5 | `05_Data_Mapping.md` | `05_Data_Mapping.md` | `11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b` | `1089aa0fe153101cf5d9a71c884a1c9ec8eb09aa7baffbabe31c324ecaa07693` |
| 6 | `06_Error.md` | `06_Error.md` | `e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b` | `fcecdc56e73869a5c65bb686b0097ae199a605a26fcf2a130b7429dfd87b5c61` |
| 7 | `07_discussions_insert.md` | `07_table.md` | `4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356` | `c32772948cd926b07b293d24607fd37ebb96840896cdeda2852ad8a835d9d0b9` |

## Static checks

| Check | Result |
|---|---|
| Expected file set: eight ordered sheets, `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md` | PASS |
| Frontmatter metadata, `dd_id`, and sheet order | PASS |
| Markdown table row widths and JSON examples | PASS |
| Local Markdown links resolve | PASS |
| Field, condition, and error entries are individually tabulated | PASS |
| Trailing whitespace and conflict markers | PASS |
| Catalog request, response, success status, and error set | PASS |
| Connected-group consistency | PASS — API #40 root creation, empty comments and API #42 reload match the #39/#41/#42 DERIVED proposals. |
| `git diff --check` | PASS |

Runtime tests were intentionally not run: API #40 is not wired, and this task changes documentation only.
