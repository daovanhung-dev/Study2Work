# PLAN_RESULT — API #81 Từ chối nội dung

## Kết quả plan trước authoring

- Status: PARTIALLY COMPLETED — NEEDS CONFIRMATION.
- Output folder: apps/study-server/docs/dd/81_admin_content_reject/.
- Scope: documentation-only, server-study; no runtime/schema/catalog/diagram edits; no ZIP.
- Exact catalog contract retained: PATCH /api/v1/admin/content/{content_id}/reject, Bearer JWT/Admin, required content_id:int64! and body reason:string!, no query, ApiEnvelope<Content>, HTTP 200 DESIGN_RESOURCE_UPDATED, errors 401/403/404/422/500 with catalog codes.
- AC-33 directly says reject branch passes reason and updates status REJECTED plus review reason, then reloads #78.
- Response remains Content with eight fields and no reason/reviewer/version metadata.
- Generic Content/review persistence is not selected. Legacy DDL lacks it; V1-PILOT content_review_decisions uses UUID revision identity and is not a direct Content int64 mapping.
- API #81 remains UNWIRED / NOT_FOUND.

## Source manifest

| Source | Unit reviewed | Use | Status |
|---|---|---|---|
| docs/lists/list_api.md | #81 row and Content schema | Exact contract and response fields | DIRECT |
| 00_AC_API_INDEX.md | AC-33 | Actor, pending precondition and endpoint sequence | DIRECT |
| AC_04_ADMIN_MANAGEMENT.drawio | Full AC-33 page nodes and edges | Reject reason → REJECTED/review reason → reload queue | DIRECT logical effect |
| DD #78/#79/#80 | Queue, detail and approval pages/open questions | Pending predicate, revision identity and audit relationship | Related draft evidence; unresolved points retained |
| DD #52/#53 | Lifecycle questions | Separate publish/delete interactions | Related proposals, not approval |
| Legacy and V1-PILOT DDL | Generic Content/review artifacts | Physical mapping boundary | Static artifacts; live schema unverified |
| Study router/auth/middleware/responses/test context | Current route and guard state | API #81 absence/integration boundary | Current source/context |
| Registered template pack | Eight sheets and appendices | Markdown structure | Registry-wired; fingerprint verified |
| Worklog preflight | Selected #48/#49/#50 docs worklogs | Carry-forward | Read; no shortage |

## API Requirement Matrix

| Requirement | Source | DD coverage | Status |
|---|---|---|---|
| PATCH path, Bearer/Admin, path content_id | Catalog #81 | Cover/Overview/Request/Mapping | DIRECT; route absent |
| Body reason:string! | Catalog #81 and AC-33 node n10 | Request/Mapping/Error | DIRECT required string; additional constraints absent |
| No query | Catalog #81 | Request/Mapping | DIRECT omission |
| Content response/status/errors | Catalog #81 | Response/Error | Direct schema and exact codes retained |
| Set REJECTED and save reason | AC-33 node n11 | Overview/Mapping/logical write register | Logical effect DIRECT; physical mapping SOURCE_REQUIRED |
| Queue reload after rejection | AC-33 edge n11 → n12 and #78 predicate | Overview/Mapping | Resulting exclusion from PENDING_REVIEW is a direct-flow inference |
| Audit parity with #80 | #80 says + audit; #81 does not | Open Questions | SOURCE_REQUIRED; no extra append assumed |

## Pre-authoring matrices

### Request Usage Matrix

| Input | Use | Status/gap |
|---|---|---|
| Authorization | Admin authentication and moderation permission | Admin claim/guard SOURCE_REQUIRED |
| content_id | Load Content and response identity | Physical key/revision SOURCE_REQUIRED |
| reason | Persist logical review reason | Required string direct; validation/storage rules open |
| Query | None | DIRECT omission |

### Query Matrix

| Query | Purpose | Logical items | Physical mapping/status |
|---|---|---|---|
| Q1 | Load target Content | Eight response fields/current state | SOURCE_REQUIRED; no generic Content relation |
| Q2 | Check pending eligibility and same revision as #79 | Current state/revision identity | Pending precondition direct; check/selector SOURCE_REQUIRED |
| Q3 | Resolve Admin reviewer | Role and actor identity | SOURCE_REQUIRED; no Admin guard/claim mapping |

### Mutation Matrix

| ID | Logical operation | Direct evidence | Physical status |
|---|---|---|---|
| M1 | Set Content status to REJECTED | AC-33 node n11 | Physical relation/column SOURCE_REQUIRED |
| M2 | Store rejection reason | Catalog body and AC-33 node n11 | Physical field/relation SOURCE_REQUIRED |
| M3 | Separate audit append | Not stated in reject node | Do not infer; confirm parity with #80 |

### Response Source Matrix

| Field group | Contract | Source/gap |
|---|---|---|
| Envelope | success, businessCode, message, data, meta, traceId | Common envelope; route absent |
| data | One Content | Direct catalog shape |
| Content fields | id, course_id, content_type, title, payload, status, parent_id, order | All retained; physical mapping SOURCE_REQUIRED; logical status REJECTED |

## Verification plan

- Verify exact 11-file package and 8/8 appendix parity.
- Check catalog input/response/error set, Content fields, JSON, local links/anchors, tables/fences and whitespace.
- Recount DD folder/full-package and route/view totals after #81.
- Application tests remain NOT_RUN; API #81 has no route.
- AC-33 document-level macro-review #78–#81 is complete. The queue/detail/decision sequence is traceable, while response cardinality, version identity, state naming, audit parity, Admin guard, persistence and lifecycle questions remain open; see [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).
