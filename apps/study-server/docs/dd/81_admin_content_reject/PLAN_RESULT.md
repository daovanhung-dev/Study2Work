# PLAN_RESULT — API #81 Từ chối nội dung

## Kết quả

- Status: `IMPLEMENTED_LOCALLY — DERIVED FALLBACKS; Draft — Needs Confirmation`.
- Scope: API #81 module/route/middleware, focused HTTP tests, API #81 DD synchronization, related Study context and this worklog. No schema or diagram change was made; migration 011 from #80 is reused as a candidate only.
- Direct contract retained: `PATCH /api/v1/admin/content/{content_id}/reject`, Bearer JWT/Admin, required signed-int64 path and required body `{reason:string}`, no query, HTTP 200 `DESIGN_RESOURCE_UPDATED`, `ApiEnvelope<Content>`, exact 401/403/404/422/500 catalog codes.
- AC-33 direct logical effect: set status `REJECTED` with review reason, then reload queue #78. Response remains the eight-field reusable Content projection with status `REJECTED`; reason is not returned.

## Source precedence and trace

1. AC-33 Admin diagram/index: pending queue → detail → reject with reason → `REJECTED` + review reason → reload queue.
2. Legacy schema: BIGINT `contents` has status/deleted_at but no reason column; migration 011 has BIGINT `content_review_audit_logs` with nullable reason. V1-PILOT decision rows use incompatible UUID revision keys.
3. Catalog row #81: required reason string, int64 Content ID, direct Content response and exact errors.
4. Current #78/#79/#80 and #51/#52: queue uses `PENDING_REVIEW`; #79 has no revision token; #80 uses a lock/update/audit transaction; #51 creates the pending state; #52 owns separate publication transitions.

```text
PATCH → typed reason body → shared ADMIN guard → raw signed-int64 path
→ lock active Content → require PENDING_REVIEW (DERIVED)
→ conditional status update to REJECTED → insert one reason-bearing decision row
→ validate Content response → commit → return direct Content envelope
```

## Chosen implementation fallbacks

| Gap | Local choice | Status |
|---|---|---|
| Physical reason storage | Store request reason in the same `content_review_audit_logs` row that records actor and old/new status. No new schema or second audit append. | DERIVED; live unverified |
| Eligible state | Require current active status `PENDING_REVIEW`; other state → catalog 422. | DERIVED from AC-33 precondition/#78 queue |
| Reason validation | Strict string, body required, unknown fields forbidden; no trim/length/blank rule. Empty string is preserved. | Type direct; remaining rules intentionally unspecified |
| Actor | Shared ADMIN guard's numeric JWT `sub`; never from request. | Current helper + DERIVED BIGINT mapping |
| Transaction | Lock, conditional update, reason-bearing insert, response validation and final commit; rollback failures. | DERIVED from #80/#76 pattern |
| Revision | Act on active row at #81 call time; no revision identity claim. | OPEN / SOURCE_REQUIRED |
| Response | Exact reusable eight-field Content with `REJECTED`; omit null parent ID per current route serialization. | Direct schema/status intent |

## Files and scope

- Added API #81 `models.py`, SQL-only `query.py`, `validate.py`, `view.py`, route and middleware path entry.
- Added focused HTTP tests; no migration/schema/diagram change.
- Updated API #81 mapping, error, response, table and open-question documents while preserving Draft status and template appendices.
- Updated directly affected API #80 notes that previously described #81 as unwired, plus Study Server context and manifest.
- No ZIP, staging or commit.

## Remaining confirmation boundaries

Live schema/deployment/FKs, dedicated moderation permission, reason retention/visibility/blank policy, exact revision continuity with #79, and rejected-content publish/delete/resubmission policy remain open. Fake DB tests do not prove these boundaries.
