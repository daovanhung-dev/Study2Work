# VERIFICATION_REPORT — Study API #24

## Template fingerprints

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
| Template file inventory/order and source fingerprint | Eight baseline template files inventoried and fingerprints recorded above. | VERIFIED |
| Required DD deliverables | Eight ordered sheets and the three planned reports are present (11 Markdown files). | VERIFIED |
| Front matter/headings and Markdown tables | Static checker passed required sheet metadata, top headings, balanced code fences, table widths/separators and whitespace. | VERIFIED |
| JSON examples | Success and error examples parsed as valid JSON. | VERIFIED |
| Relative links and anchors | All local targets and referenced anchors resolved. | VERIFIED |
| API #24 contract codes | Response code set matches catalog: 200/401/403/404/500. | VERIFIED |
| Source conversion coverage and gaps | Catalog and AC-14/15 represented; runtime, access/publish, schema and serialization gaps retained as open questions. | VERIFIED |
| Runtime tests | Not run; API #24 route/module/test are absent and the plan excludes application tests. | NOT_RUN |
| Context validator | Not run; no context page or manifest changed. | NOT_REQUIRED |

## Output fingerprints

SHA-256 of the eight authored sheet files:

| File | SHA-256 |
|---|---|
| `00_Cover.md` | `10c22da6babb9c96546733005dd632c3afc5ca3bb7cb22e4b6f56cebd907993a` |
| `01_Lich_su.md` | `9e7a04464e534a8e43c85fe1e9e47628881675230134cf246d972ef5c09adb46` |
| `02_Overview.md` | `03d5112daddd9e87c13c0581e5faac8c3789a324b0af118aa356b6c4e9446f25` |
| `03_Request.md` | `84e2900ca84638d6de74ba18e8b7049b6b4f169dbfbac4f409b48fb26fdb973a` |
| `04_Response.md` | `6664cf872c4a4ceb88a67f794efda1c5c653bd6ae6e1790a4dab276cd1479c8b` |
| `05_Data_Mapping.md` | `35a9254af6f0da42dd3628b2a2401c943b2aa81b0f1ae0dc0720e92bd8a3729a` |
| `06_Error.md` | `4d7ac7864a24e72e735b44fab529d93ecdbeb5119abe157b73681d82d5735f8a` |
| `07_table.md` | `b4cc65162b2723dd8b9232466a89fd1940f902e32aab53510e8009295a90de76` |

## Source defects preserved

- API #24 route/module/query/focused test are absent from current Study source.
- AC-15 access/publish check has no API-specific predicate or query.
- Checked-in DDL is design evidence; live schema has not been verified.
- `lessons.course_id` nullability differs between checked-in DDL and DB design/catalog expectation.
- Catalog response is `ApiEnvelope<Lesson>`; diagram uses generic `ApiEnvelope`.

## Introduced defects

- None found by the static Markdown, link/anchor, table, JSON and contract-code checks performed for this DD.
