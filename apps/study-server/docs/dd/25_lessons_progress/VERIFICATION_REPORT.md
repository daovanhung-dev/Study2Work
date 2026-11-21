# VERIFICATION_REPORT — Study API #25

## Template fingerprints

SHA-256 fingerprints for the eight baseline files in `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/`.

| File | SHA-256 |
|---|---|
| `00_Cover.md` | `fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63` |
| `01_Lich_su.md` | `d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e` |
| `02_Overview.md` | `c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6` |
| `03_Request.md` | `37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa` |
| `04_Response.md` | `5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8` |
| `05_Data_Mapping.md` | `11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b` |
| `06_Error.md` | `e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b` |
| `07_table.md` | `4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356` |

## Verification status

| Check | Result | Status |
|---|---|---|
| Template inventory/order and source fingerprint | Eight expected sheets are present in template order; hashes above match baseline files. | VERIFIED |
| Required DD deliverables | Eight ordered sheets and three reports are present (11 Markdown files). | VERIFIED |
| Front matter, headings, Markdown tables and code fences | Required metadata/order, table widths and balanced fences passed static checks. | VERIFIED |
| One-line field mapping and whitespace | Request/response/DB fields are represented per row; no trailing whitespace in 12 authored files. | VERIFIED |
| JSON examples | Request body and two response examples parsed as valid JSON. | VERIFIED |
| Relative links and anchors | All local targets and referenced anchors resolved. | VERIFIED |
| API #25 contract codes | Method/path/request/response and 200/401/403/404/422/500 code set match catalog. | VERIFIED |
| Source coverage and gaps | Catalog, AC-14, DB design/DDL and current source are distinguished; unresolved items remain in open questions. | VERIFIED |
| Runtime tests | Not run; documentation-only task and endpoint is not wired. | NOT_RUN |
| Context validator | Not required; no context page or manifest changed. | NOT_REQUIRED |

## Output fingerprints

SHA-256 fingerprints for the eight authored sheets.

| File | SHA-256 |
|---|---|
| `00_Cover.md` | `87d626cf5e4040a08a2f99a218bd52f9c9b78a85a75512264c6dedcb95eeb563` |
| `01_Lich_su.md` | `1c1d4e4857e2db67646f922f7956403ccb09b3f202ab8d3dd8a31329f3fdf5a6` |
| `02_Overview.md` | `a4707f802f3f9cb84ba3d70e70aebe06292e4e544f320e7e66bc58ee981e5e90` |
| `03_Request.md` | `a82546e105104c5bcdf34fd9a3fb337063568777e32a249793357b7ac536005c` |
| `04_Response.md` | `353f67b63e44f0caf02bf3fc9bf08da44e92f12316466ab721057ee3a73a4173` |
| `05_Data_Mapping.md` | `3649ec4e0af49e303dff1ea8cbae00309bd5ee9d36489e6eb06b3c3fa9d64406` |
| `06_Error.md` | `81f705b0512255440bf5f8ad1d26367337f59e7cf193e389226fba0fb0567672` |
| `07_lesson_progress_update.md` | `062a641aaf827de1b2f8d54d105267dc53c07f52618fb181bf6b9006ad6146b2` |

## Source defects preserved

- API #25 route/module/query/focused test were not found in current Study source/test inventory.
- Candidate `lesson_progress` schema has no `position` column or declared `(user_id, lesson_id)` unique constraint.
- AC-14 names course aggregate update but gives no source, target, formula, transaction or failure behavior.
- Catalog declares `ApiEnvelope<Lesson>`; AC-14 diagram uses generic `ApiEnvelope`.
- Checked-in DDL/ERD are design evidence; live schema was not verified.

## Introduced defects

- None found by the static Markdown, JSON, table, link/anchor and contract-code checks performed for this DD.
