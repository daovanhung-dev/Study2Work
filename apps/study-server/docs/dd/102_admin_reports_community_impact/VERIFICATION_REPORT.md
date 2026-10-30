# VERIFICATION_REPORT — Study API #102

**Status:** Verified with open questions
**Scope:** Markdown DD and worklog; no runtime/schema/catalog/diagram changes. No application tests were run.

## Sources and fingerprints

- Reviewed: API catalog #102 and reusable `Report` schemas; AC-38, AC-18, AC-19 and DB ERD/table guide; legacy and V1-PILOT DDL; current router/auth/middleware; DD #101, #66 and #91; selected `docs` worklogs; registered `createDD-markdown` templates and Study Markdown-only workflow.
- Template fingerprint (SHA-256 over ordered basename + NUL + file bytes + NUL for 8 sheets): `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137`.
- Output fingerprint (same serialization over 8 sheets, `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`; excludes this report): `2c9de4cbc4ad4c56571fdf6aa320ff1358651a6e3649add665468b1547c6f181`.
- Each sheet appendix is copied verbatim from its matching registered template.

| Check | Result | Status |
|---|---|---|
| Context/preflight | Root router, context map, server-study pages/workflow and selected `docs` worklogs reviewed; plan saved before DD folder creation. | VERIFIED |
| Catalog contract | Method/path, Admin Bearer, query strings, no body/path, response shape, HTTP 200 and exact 3 error codes match #102. | VERIFIED_STATIC_ONLY |
| AC diagrams | AC-38 flow and AC-18/AC-19 learning/community boundaries parsed; DB ERD/table guide checked for candidate relations. | VERIFIED_STATIC_ONLY |
| Schema/source | Legacy enrollment/discussion timestamps and self-reference are candidates; pilot UUID model not merged; no #102 route/module/query/test. | VERIFIED_STATIC_ONLY |
| File manifest/front matter | Exactly 11 Markdown files: 8 sheets and 3 reports; sheet front matter present. | VERIFIED |
| Template suffix | All sheet appendix suffixes match registered templates exactly. | PASS — 8/8 |
| Request/response/mapping matrices | Query/body, all `Report`/`DateRange`/`ImpactMetric` fields, four candidate queries and read-only mutation boundary listed. | VERIFIED_STATIC_ONLY |
| JSON examples | All three success/error JSON examples parse. | PASS — 3 |
| Markdown links/tables/fences/whitespace | 23 local links resolve; no anchors; all 523 table rows are width-consistent; 5 code-fence pairs balance; final newlines and whitespace pass. | PASS |
| Inventory | Catalog 103; after #102, 102 DD folders/core packs and 90 full 11-file packs; #103 is missing. Source route+view count is 12, 91 without. | VERIFIED_STATIC_ONLY |
| `git diff --check` | No diagnostics; untracked DD also passed dedicated whitespace validation. | PASS |
| Runtime tests | Not run; docs-only. | NOT_RUN |

## Introduced defects

No runtime behavior is claimed. Metric definitions, segment vocabulary, date parsing, Admin authorization, comment persistence and AC-38 export integration remain explicit in [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

## AC-38 macro-review — 2026-10-24

- Flow review: #101 aggregate summary → #102 community metrics and dashboard filters → optional #103 export / view-only branch. Diagram lists CSV/XLSX/PDF, an async job, and temporary storage only when the file is generated server-side.
- Contract gap: #101 uses `from?:date`/`to?:date`; #102 uses string query values. Matching the date format/window remains a proposal until the contract owner confirms it.
- Export gap: #103 endpoint row declares `ApiEnvelope<Report>` at HTTP 202, while Operation tracking declares `ApiEnvelope<Operation>` and polling through API #18. The draft recommendation to return Operation is `DERIVED`, not a resolution.
- Poll gap: API #18 still has `operation_id:int64` in its row versus UUID in shared schema/diagrams, owner-only versus owner/Admin authorization, and `Operation.result?:Payment` that does not express an export artifact. Study has no approved Operation/export persistence, queue, or generic file-storage mapping.
- Source boundary: #101–#103 have no current Study route+matching view pair; current Admin/report permission source is also absent. All three remain `UNWIRED / NOT_FOUND`; no runtime behavior is claimed.
- Decision: retain these items as open questions. No catalog, schema, diagram, runtime source, or client contract was changed.
