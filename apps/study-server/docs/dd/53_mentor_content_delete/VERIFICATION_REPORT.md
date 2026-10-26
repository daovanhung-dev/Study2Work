# Verification Report — API #53 Xóa nội dung Mentor

## Phạm vi

Cập nhật DD theo diagram/catalog, local Study source, migrations 006/007, APIs #49–#52, endpoint tests và `createDD-markdown` template. DD vẫn `Draft — Needs Confirmation`: dependency/status/retry policy chưa được duyệt. Fake-DB tests và local migration artifacts không xác minh live PostgreSQL hoặc deployment.

## Deliverable manifest

| File | Vai trò | Trạng thái |
|---|---|---|
| 00_Cover.md | Cover | Updated |
| 01_Lich_su.md | Lịch sử | Updated |
| 02_Overview.md | Overview | Updated |
| 03_Request.md | Request | Updated |
| 04_Response.md | Response | Updated |
| 05_Data_Mapping.md | Flow/query/mutation/response mapping | Updated |
| 06_Error.md | Error | Updated |
| 07_content_soft_delete.md | Logical soft-delete mapping | Updated |
| PLAN_RESULT.md | Plan and pre-authoring matrices | Updated |
| OPEN_QUESTIONS.md | Contract/schema/lifecycle gaps | Updated |
| VERIFICATION_REPORT.md | Verification record | Updated |

## Verification checks

| Check | Evidence | Result |
|---|---|---|
| Catalog contract | DELETE path, Mentor Bearer, int64 path, no body/query, `ApiEnvelope<DeleteResult>`, HTTP 200 and exact 401/403/404/422/500 code set match row #53. `DeleteResult` fields are id:int64, status:"deleted", deleted_at:date-time. | PASS |
| AC-22 / AC-33 | AC-22 confirms managed-course permission, soft delete and tree reload; AC-33 moderation states/audit ambiguity retained. | PASS; open questions retained |
| Route/source | DELETE operation is registered; route template is shared with #51 PUT and already appears in `DESIGN_CONTRACT_PATHS`. Auth precedes DB; active Content/Course are locked; active-child and PUBLISHED guards return 422; soft delete writes `deleted_at = CURRENT_TIMESTAMP`. | PASS — local source only |
| Response | OpenAPI declares int64 ID, literal deleted status and date-time timestamp; success test verifies the actual `DeleteResult` and business code. | PASS |
| Endpoint tests | API #53 focused TestClient/fake-DB suite: 18 passed. | PASS; no live DB claim |
| Linked API tests | APIs #49–#52 plus #53 focused suites: 113 passed. | PASS |
| Full Study tests | `uv run pytest -q`: 449 passed, 1 upstream Starlette/httpx deprecation warning. | PASS |
| Schema boundary | Checked-in migration 006/DB.sql define `contents.deleted_at`; migration 007 defines Content snapshots. Live schema and migration application remain unverified. | PASS — local artifact only |
| DD appendix | Compared eight appendix suffixes byte-for-byte with registry-wired templates; relative links and JSON examples also checked. | PASS |
| Static checks | Focused Ruff check/format and API #52/#53 mypy scope. | PASS |
| Context validator | `deno run -A scripts/validate-agent-context.mjs --skip-drift`. It reports the existing missing DB Admin context/source tree, unrelated to Study Server. | BLOCKED_BY_BASELINE |

## AC-22/AC-33 macro-review #49–#53

Status: VERIFIED_WITH_OPEN_QUESTIONS. Current source implements read/create/update/publish/delete against the checked-in legacy Content mapping; this does not approve the DERIVED rules.

- #49 returns active Content rows and validates parent links; deleting a parent with an active direct child would leave an invalid active tree, so #53 currently blocks that case.
- #50 locks the owning Course before insertion; #53 uses the same Course lock while deleting. #51 does not change `parent_id` and snapshots revisions. #52 owns the current publication-status mutation.
- #53 blocks PUBLISHED Content and permits other statuses under the present DERIVED fallback. Moderation queue withdrawal, full dependency coverage, assigned-Mentor authorization, repeat-delete policy, and audit/history retention remain open.
- Local fake-DB tests verify orchestration and response mapping only. They do not verify SQL execution, lock behavior, schema, migration application, or deployed availability.

## Remaining questions

See [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md). DD status remains Draft — Needs Confirmation.
