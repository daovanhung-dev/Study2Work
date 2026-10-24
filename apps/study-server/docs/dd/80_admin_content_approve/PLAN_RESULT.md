# PLAN_RESULT — API #80 Phê duyệt nội dung

## Kết quả plan trước authoring

- Status: PARTIALLY COMPLETED — NEEDS CONFIRMATION.
- Output folder: apps/study-server/docs/dd/80_admin_content_approve/.
- Scope: documentation-only, server-study; no runtime/schema/catalog/diagram edits; no ZIP.
- Catalog #80 contract is preserved exactly: PATCH /api/v1/admin/content/{content_id}/approve, Bearer JWT/Admin, content_id:int64!, no body/query, ApiEnvelope<Content>, HTTP 200 DESIGN_RESOURCE_UPDATED, errors 401/403/404/422/500 with catalog codes.
- AC-33 directly specifies the approve branch's logical status update and audit, but APPROVED/PUBLISHED is ambiguous. AC-22 separately provides Mentor API #52 to change publication status.
- Physical Content/revision/audit relations are not selected. Legacy DDL lacks generic Content. V1-PILOT content_review_decisions uses UUID version identity and is not directly compatible with Content int64.
- API #80 remains UNWIRED / NOT_FOUND; its DD is not an implementation claim.

## Source manifest and coverage

| Source | Unit reviewed | Use | Status |
|---|---|---|---|
| docs/lists/list_api.md | Row #80 and reusable Content schema | Direct request, response and exact errors | DIRECT |
| 00_AC_API_INDEX.md | AC-33 and AC-22 index entries | Actor, precondition and connected action sequence | DIRECT |
| AC_04_ADMIN_MANAGEMENT.drawio | Full AC-33 page nodes and edges | #78 → #79 → decision → #80 → status/audit → queue reload | DIRECT logical flow |
| AC_03_MENTOR_TEACHING.drawio | Full AC-22 page nodes and edges | Separate #52 publication status operation | DIRECT; lifecycle relation unresolved |
| DD #78/#79/#52 | Relevant Overview, Mapping and open questions | Queue state, revision identity, separate publication path | Related draft evidence; questions remain open |
| Legacy and V1-PILOT DDL | Content/review artifacts | Schema mapping boundary | Static artifacts; live schema unverified |
| Study router/auth/middleware/responses/tests context | Route/view, guard, error, test inventory | Current implementation boundary | Current source/context; #80 absent |
| Registered createDD-markdown template | 8 Markdown sheets and appendix data | Template structure/fingerprint | Registry-wired; source pack verified |
| .agents/worklog/2026-10-24/* | Selected #48–#50 logs and current inventory | Carry-forward and counts | Reviewed; no shortage |

## API Requirement Matrix

| Requirement | Source | DD coverage | Status |
|---|---|---|---|
| PATCH path, Bearer/Admin, path ID | Catalog #80 | Cover, Overview, Request, Mapping | DIRECT; route absent |
| No body/query | Catalog #80 | Request and Mapping | DIRECT omission |
| Content envelope, success and errors | Catalog #80 | Response, Error | DIRECT; exact catalog set retained |
| Pending-review context | AC-33 precondition and #78 node n3 | Overview, Mapping | DIRECT; enforcement branch DERIVED |
| Status update and audit | AC-33 node n9 | Overview, Mapping, logical table register | Logical effects DIRECT; physical/transition details SOURCE_REQUIRED |
| Separate publication action | AC-22 node n9/n10 and DD #52 | Overview, Open Questions | DISCREPANCY; no lifecycle reconciliation invented |

## Pre-authoring matrices

### Request Usage Matrix

| Input | Use | Status/gap |
|---|---|---|
| Authorization | Authenticate Admin and authorize before resource access | Role direct; Admin claim/guard SOURCE_REQUIRED |
| content_id | Select logical Content and response identity | Path type direct; physical key/revision unresolved |
| Body/query | No fields declared | DIRECT omission |

### Query Matrix

| Query | Purpose | Logical item | Physical mapping/status |
|---|---|---|---|
| Q1 | Load Content | Eight fields needed for Content response | SOURCE_REQUIRED; no generic Content relation |
| Q2 | Check pending/reviewable state and same revision as #79 | Current status, revision identity/version | SOURCE_REQUIRED; only pending precondition is direct |
| Q3 | Resolve Admin actor | Authenticated role and audit actor | SOURCE_REQUIRED; no Admin guard/claim map |

### Mutation Matrix

| ID | Logical operation | Direct evidence | Physical mapping/status |
|---|---|---|---|
| M1 | Update review/publication status | AC-33 APPROVED/PUBLISHED wording | SOURCE_REQUIRED; target state conflicts with separate #52 |
| M2 | Append approval audit/decision | AC-33 + audit | SOURCE_REQUIRED; V1-PILOT log is non-equivalent to direct Content ID |

### Response Source Matrix

| Field group | Contract | Source/gap |
|---|---|---|
| Envelope | success, businessCode, message, data, meta, traceId | Common envelope; route absent |
| data | One Content | Direct catalog shape |
| Content fields | id, course_id, content_type, title, payload, status, parent_id, order | All retained; physical source SOURCE_REQUIRED; status target unresolved |

## Verification plan

- Verify exact 11-file Study Markdown package and eight template appendix suffixes.
- Validate exact contract/error set, JSON examples, links/anchors, table structure, fences and whitespace.
- Recount catalog/DD/source wiring after #80 authoring.
- Application tests remain NOT_RUN; no API #80 route exists.
- AC-33 document-level macro-review #78–#81 is complete; unresolved group findings are recorded in [the group report](../81_admin_content_reject/VERIFICATION_REPORT.md).
