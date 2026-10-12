# VERIFICATION_REPORT — Study API #26

## Input and coverage

| Source | Scope/units | Read | Status / note |
|---|---|---|---|
| `docs/lists/list_api.md` | API catalog and reusable schemas | Yes | API #26 row and `ApiEnvelope`, `Lesson`, `Resource` schemas checked. |
| `00_AC_API_INDEX.md` | AC index, AC-15 | Yes | Actor, precondition, postcondition and endpoint membership checked. |
| `AC_02_STUDENT_LEARNING.drawio` | AC-15 diagram page | Yes | API node, access/publish note and resource read step checked. |
| `DB_UNICA_TABLES.md` | `resources` section | Yes | Relation, columns and visibility discrepancy checked. |
| `DB.sql` | `resources` DDL | Yes | Candidate columns/nullability checked; design evidence only. |
| Study runtime source | Router, module inventory, API #12 adjacent route | Yes | API #26 absent; API #12 remains separate. |
| Study tests | Test inventory | Yes | No focused API #26 test found. |
| DD template | Eight Markdown sheets | Yes | Files/order and headings inspected before authoring. |
| Prior docs worklogs | API #16–#18 | Yes | Selector returned three; all read; no shortage. |

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
| Required deliverables | 8 ordered sheets plus 3 reports | VERIFIED |
| Front matter/headings/tables/fences | Static Markdown structure check passed for all 11 files. | VERIFIED |
| JSON examples | Success and error examples parse as valid JSON. | VERIFIED |
| Relative links and anchors | All local targets and referenced anchors resolve. | VERIFIED |
| API #26 contract | Method/path/actor/request/response and 200/401/403/404/500 codes match catalog. | VERIFIED |
| Request/response/query/data coverage | Request, query, response source and candidate DB columns represented; unresolved mappings remain explicit. | VERIFIED |
| Worktree boundary | This task adds only DD #26 and its worklog; pre-existing changes preserved. | VERIFIED |
| Study application tests | Not run; documentation-only task | NOT_RUN |
| Context validator | Not required; no canonical context page/manifest changed | NOT_REQUIRED |

## Output fingerprints

SHA-256 fingerprints for the eight authored sheets.

| File | SHA-256 |
|---|---|
| `00_Cover.md` | `fe3dd8ca9f589cfdc9f44f5b7bd94e868eef02bb6edce801ae006b57ac6f24e9` |
| `01_Lich_su.md` | `028a0362af78c1f3e66a327a1ec4ec594d12738fcddb89cf1d5568cc9c543c16` |
| `02_Overview.md` | `095db7509d1b9492aba91481d54ffbbb10992d17d8d9d8e5be63d7ad0d5fa133` |
| `03_Request.md` | `134e7cb8af13de692281f65d475bd680944c99f897db0b78e91c5d30ccea67ff` |
| `04_Response.md` | `fc6b0b1496468ffa805734112506e5a0bd5e4ecdef27220e3e56676cdc8c650e` |
| `05_Data_Mapping.md` | `6e6b14ea69db140ab64966ca1ef92cb2145cb9c19fac8ad61da3fd94fa8cf4a0` |
| `06_Error.md` | `0faae7594ebbc6042b519b027341dbdafa879f21d97c89d8c2bec99fd4120be1` |
| `07_table.md` | `167404db4f33bcbe863effce13b9f1fa14fbc71f82bf339029e67a364909759d` |

## Source defects preserved

- API #26 catalog/diagram response type is `ApiEnvelope<Lesson>` although the endpoint intent is attached resources and reusable `Lesson` has no Resource collection.
- Reusable `Resource.visibility` has no matching ERD/DDL column.
- ERD marks `resources.lesson_id` required while checked-in DDL omits `NOT NULL`.
- Cardinality, ordering, empty behavior, access/publish predicates and signed URL responsibility remain unspecified.
- API #26 route/module/query/focused test are absent from current Study source/test inventory.

## Introduced defects

- None found by the static Markdown, JSON, link/anchor, contract-code and source comparison checks performed for this DD.

