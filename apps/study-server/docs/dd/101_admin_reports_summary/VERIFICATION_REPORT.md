# VERIFICATION_REPORT — Study API #101

**Status:** Verified with open questions
**Scope:** Markdown DD and worklog; no runtime/schema/catalog/diagram changes. No application tests were run.

## Sources and fingerprints

- Reviewed: catalog #101 and reusable `Report` schemas; AC-38 index/diagram; legacy Study DDL; pilot `report_snapshots` DDL; current router/auth/middleware; related DD #66/#91; selected `docs` worklogs; registered `createDD-markdown` templates and server-study Markdown-only workflow.
- Template fingerprint (SHA-256 over ordered basename + NUL + file bytes + NUL for 8 sheets): `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137`.
- Output fingerprint (same serialization over 8 sheets, `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`; excludes this report): `db935bfd17f0612d0cbb5fb524bb3edf08856b79a9c9aa4a3c0515d93e9d7fcb`.
- Each of the 8 sheet appendices is copied verbatim from its registered template.

| Check | Result | Status |
|---|---|---|
| Context/preflight | Root router, context map, server-study pages/workflow and three selected `docs` worklogs reviewed; plan recorded before creating the DD folder. | VERIFIED |
| Catalog contract | Method/path, Admin Bearer, query types, no body, response shape, HTTP 200 and exact 3 error codes match #101 row/schema. | VERIFIED_STATIC_ONLY |
| AC-38 flow | #101 aggregate summary → #102 community metrics → optional #103 export confirmed; group macro-review deferred. | VERIFIED_STATIC_ONLY |
| Schema candidates | Legacy timestamp columns and pilot `report_snapshots` reviewed separately; live schema and API mapping remain unverified. | VERIFIED_STATIC_ONLY |
| Runtime source | No #101 route/module/query/test; status `UNWIRED / NOT_FOUND`. | VERIFIED_STATIC_ONLY |
| File manifest/front matter | Exactly 11 Markdown files: 8 sheets and 3 reports; sheet front matter present. | VERIFIED |
| Template suffix | All sheet appendix suffixes match the registered templates exactly. | PASS — 8/8 |
| Request/response/mapping matrices | Query/body, all `Report`/`DateRange`/`ImpactMetric` fields, candidate queries and read-only mutation boundary listed. | VERIFIED_STATIC_ONLY |
| JSON examples | Success example parses as JSON. | PASS — 1 |
| Markdown links/tables/fences/whitespace | 18 local links resolve; 513 table rows are column-consistent; 3 code-fence pairs balance; final newlines and whitespace pass. | PASS |
| Inventory | Catalog 103; after #101, 101 DD folders/core sheets, 89 full 11-file packs, 2 missing DDs; 12 route+view source pairs and 91 without. | VERIFIED_STATIC_ONLY |
| `git diff --check` | No diagnostics; untracked DD also passed dedicated whitespace validation. | PASS |
| Runtime tests | Not run; docs-only. | NOT_RUN |

## Introduced defects

No runtime behavior is claimed. Any unresolved metric, date, persistence, authorization or AC-38 integration choices remain explicit in [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

## AC-38 macro-review — 2026-10-24

- Flow review: #101 aggregate summary → #102 community metrics and dashboard filters → optional #103 export / view-only branch. Diagram lists CSV/XLSX/PDF, an async job, and temporary storage only when the file is generated server-side.
- Contract gap: #101 uses `from?:date`/`to?:date`; #102 uses string query values. Matching the date format/window remains a proposal until the contract owner confirms it.
- Export gap: #103 endpoint row declares `ApiEnvelope<Report>` at HTTP 202, while Operation tracking declares `ApiEnvelope<Operation>` and polling through API #18. The draft recommendation to return Operation is `DERIVED`, not a resolution.
- Poll gap: API #18 still has `operation_id:int64` in its row versus UUID in shared schema/diagrams, owner-only versus owner/Admin authorization, and `Operation.result?:Payment` that does not express an export artifact. Study has no approved Operation/export persistence, queue, or generic file-storage mapping.
- Source boundary: #101–#103 have no current Study route+matching view pair; current Admin/report permission source is also absent. All three remain `UNWIRED / NOT_FOUND`; no runtime behavior is claimed.
- Decision: retain these items as open questions. No catalog, schema, diagram, runtime source, or client contract was changed.
