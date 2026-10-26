# PLAN_RESULT — API #80 Phê duyệt nội dung

## Kết quả

- Status: `IMPLEMENTED_LOCALLY — DERIVED FALLBACKS; Draft — Needs Confirmation`.
- Scope: API #80 runtime, focused HTTP tests, legacy DDL/migration candidate, DB guide/ERD, API #80 DD, directly affected API #81 audit-reason notes and Study context.
- Direct catalog contract is preserved: `PATCH /api/v1/admin/content/{content_id}/approve`, Bearer JWT/Admin, required int64 path, no body/query, HTTP 200 `DESIGN_RESOURCE_UPDATED`, `ApiEnvelope<Content>`, exact errors 401/403/404/422/500.
- AC-33 logical approval/audit effect is implemented against the checked-in legacy BIGINT `contents` candidate. Migration 011 is not applied to or verified against a live database.

## Quyết định triển khai

| Gap | Local implementation choice | Status |
|---|---|---|
| `APPROVED/PUBLISHED` wording | Set `APPROVED`; current API #52 remains the separate `APPROVED` ↔ `PUBLISHED` publication operation. | DERIVED |
| Eligible state | Lock active row and require `PENDING_REVIEW`; another active state returns catalog 422. | DERIVED |
| Physical audit | Add `content_review_audit_logs` with legacy BIGINT Content/Admin FKs, old/new status, nullable reason and timestamp. | DERIVED; live unverified |
| Actor | Shared `ADMIN` guard's numeric JWT `sub`; never from request. | DERIVED from current helper |
| Transaction | Lock, update, append audit, validate response, then commit; rollback failures. | DERIVED from AC-33 + API #76 pattern |
| Response | Direct reusable eight-field Content projection; no audit/reason/reviewer/version fields. | DIRECT |
| Revision identity | Act on active row locked at call time; do not claim it is the exact revision shown in #79. | OPEN / SOURCE_REQUIRED |
| API #81 | Runtime is implemented locally in its own task and uses one reason-bearing decision row in the migration 011 candidate. This reuse is DERIVED and awaits owner review/live schema verification. | DERIVED / OPEN |

## Source order reviewed

1. AC-33 diagram/index: pending queue → detail → approval, status/audit → reload.
2. Legacy BIGINT `contents` and `content_versions`; V1-PILOT UUID decision log remains incompatible with the int64 API contract.
3. API catalog #80 and reusable Content schema: no body/query, one Content response, exact status/business-code set.
4. Current API #51/#52, #78/#79 and shared ADMIN/audit patterns were traced before coding.

## Local delivery

- Added API #80 module, route, middleware contract path and focused TestClient coverage.
- Added migration 011 and matching candidate in `DB.sql`, `DB_UNICA_TABLES.md` and `DB_UNICA_ERD.drawio`.
- Updated all 11 API #80 Markdown files while retaining Draft status and template appendices; updated only directly affected API #81 schema/reason notes.
- Updated `.agents/server-study`, `.agents/project/source-status.md` and `.agents/context-manifest.json`.
- No ZIP, staging, commit, or live migration was performed.
