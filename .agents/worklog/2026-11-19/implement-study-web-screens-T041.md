---
task_id: "2026-11-19-implement-study-web-screens-T041"
date: "2026-11-19"
primary_task_type: "coding"
secondary_task_types: ["fix", "docs", "test"]
project_scopes: ["web-work (Study Web)", "server-study"]
cross_scope_dependencies:
  - "Study Web screens -> Study Server API contracts, legacy BIGINT schema and object storage"
status: "IN_PROGRESS"
---

# Worklog: Implement remaining Study Web screens — T041

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; 151 available; T040, T038 and T039 selected; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-18/implement-remaining-study-screens-T040.md`
    - carry_forward: 83 screen IDs are an inventory, not acceptance coverage; previous safe UI copy/layout work is present; payment/enrollment and verification remained blocked then. Its former coding-only/no-test boundary is superseded by the user's current approval to implement the backend/schema contracts and verify this plan.
  - path: `.agents/worklog/2026-11-17/implement-remaining-study-screens-T038.md`
    - carry_forward: preserve the dirty tree; route presence is not acceptance; historical source-backed flows and gates require current-source recheck.
  - path: `.agents/worklog/2026-11-17/implement-remaining-study-screens-T039.md`
    - carry_forward: ST10/ME07/ME08 were corrected in that work; other gates were retained where API/schema/permission/policy evidence was missing. Its previous no-backend boundary is superseded by the approved plan.
- additional context read: `.agents/worklog/2026-11-19/load-full-project-and-web-context.md`, `.agents/worklog/README.md`, `.agents/worklog/TEMPLATE.md`, `.agents/project/agent-control.md`, and user-provided root `AGENTS.md`.
- baseline: branch `develop`, HEAD `602d5196`; 62 pre-existing changes in `apps/study-client`, `apps/study-server`, and `infra/postgres/study-server`, plus other dirty files. Preserve all pre-existing work; do not reset, clean, or broadly reformat.

## EXPECTED_BEHAVIOR

- Requirement: audit all 83 Study Web screen IDs and complete every remaining incomplete screen so behavior follows the screen DD, Study UI conventions, approved logic and backend responses.
- Scope: Study Web (`web-work`) and directly required Study Server/database contracts. Work Web and Mobile are out of scope.
- Approved decisions:
  - Resources: `PUBLIC` and `PRIVATE` visibility; private resources require active enrollment and short-lived signed URLs. Existing resources default private. API #11 returns `Resource[]`, ordered by `id ASC`; valid empty courses return `200 []`.
  - Payment: VNPay sandbox; only verified server-side provider results can establish payment success or enrollment entitlement.
  - Mentor lecture content: Markdown string; upload references remain upload IDs.
  - Notifications: in-app only, one recipient-owned notification per Student, course scoped; #63 receives course ID, recipient ID array and string content; write the batch atomically.
  - Operations: UUID, owner-only poll, `PENDING|SUCCEEDED|FAILED`; notification batch completes immediately, payment/export complete after backend processing.
  - Admin moderation: `HIDE|LOCK|WARN`; #100 uses `DELETED` and `deleted_at`; retain replies/reports; write audit in the same transaction.
  - Reports: `unique_learners`, `completions`, `discussion_topics`, `discussion_replies`; inclusive UTC dates, default trailing 30 days; `learning|community` segments; CSV/XLSX/PDF export via Operation and one-hour signed URL.
- Canonical evidence: current Study source wins over stale DD claims; update API/screen DD and context to match approved contract and implementation.

## MILESTONES

Progress starts at 0%.

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 10% | 10% | Complete preflight, record approved decisions and worktree boundary, and inventory current-source discrepancies for the implementation target. | `DONE` |
| 35% | 45% | Implement backend APIs, legacy-schema migrations and provider/storage/operation flows for approved contracts; focused backend verification passes. | `PENDING` |
| 35% | 80% | Reconcile all 83 IDs and complete partial/gated Study Web screens supported by the approved contracts; client build and focused specs pass. | `PENDING` |
| 20% | 100% | Run final verification, review scoped diff, update DD/context/worklog and validate registered context. | `PENDING` |

Current verified progress: `10%` (M1 complete; M2–M4 pending).

Plan Revision v1.2: reuse existing migrations 015 (orders) and 016 (uploads, notification delivery and recipients/read-state); do not create duplicate tables. Add only missing incremental schema contracts after migration 019. No repository migration runner was found, so migrations remain checked-in SQL artifacts and will not be applied to a live DB in this task.

## EVENT_LOG

| Event ID | Operation / target | Result |
|---|---|---|
| T041.S01.A01.E01 | INSPECT git status, branch, HEAD and worklog contract | Branch `develop`, HEAD `602d5196`; 62 pre-existing Study-scope changes; preserve all existing state. Read worklog and root agent rules. |
| T041.S01.A02.E02 | RUN coding selector; READ agent-control/template | Selector `READY`; T040/T038/T039 selected, no shortage. Confirmed per-tool Event receipts and required worklog fields. |
| T041.S01.A03.E03 | READ selected coding worklogs and 11/19 context log | Carry-forward gates, current source precedence, approved previous UI changes, and prior verification limitations recorded above. |
| T041.S01.A04.E04 | CREATE T041 worklog | Added preflight, user-approved contracts, baseline, discrepancies, milestone plan and handoff. |
| T041.S01.A05.E05 | VERIFY worklog; READ server context and migration inventory | Readback succeeded; server source/DB migration rules loaded; server and migration worktree diff is clean; migrations 015/016 and API tests found. |
| T041.S01.A06.E06 | READ migration 015/016 and API #16/#18/#43/#63/#64 queries | Orders and notification-recipient/read-state artifacts exist; Operation query is notification-delivery-specific, not generic. |
| T041.S01.A07.E07 | READ legacy DDL, migration discovery and payment/enrollment source | `payments` lacks `order_id`; `resources` lacks visibility/storage key; migration 015 creates `orders`; #17 fails closed; #19 requires paid Order. No migration apply runner found. |
| T041.S01.A08.E08 | PATCH worklog with migration correction | Attempt failed on mismatched `Files changed` context; apply_patch confirmed no hunk was applied. |
| T041.S01.A08.E09 | READ exact T041 worklog target lines | Confirmed failed patch left the file unchanged and located exact hunk context. |
| T041.S01.A09.E10 | UPDATE T041 worklog with migration/source findings and M1 status | Corrected existing-order/read-state evidence, recorded Plan Revision v1.2 and marked M1 done at 10%. |
| T041.S02.A01.E11 | READ worklog, server modules/tests/workflow/runtime and Study Web router context | M1 readback verified at 10%; server layering/test boundaries and current route gates loaded. One incorrect frontend-rules path returned `NOT_FOUND` and was retried. |
| T041.S02.A01.E12 | READ Study frontend rules/design and inspect storage/config search results | Loaded Angular four-folder/layer rules and Study ocean design; located S3 upload provider; search did not find a presign function. |

## CURRENT_BEHAVIOR

- Source/config: API #11 query reads rows ordered by ID but its view serializes only the first row. API #26 is present and returns `LessonResources.resources[]`, but only checks Student auth and published course, not enrollment/visibility. Migration 015 creates legacy BIGINT `orders`; migration 016 creates recipient/read-state and delivery support. The legacy `payments` table lacks `order_id`, and there is no generic operations table. API #17 currently fails closed with 503 before persistence. API #18 currently queries notification delivery rows only. APIs #99–#103 are not routed in Study Server. ME04 currently loads #46 and keeps create controls disabled.
- Runnable tests: prior worklogs contain historical passing results; no current test has been run for T041.
- Runtime wiring: Study routes and source modules exist locally; live database, provider credentials and deployed runtime are not verified.

## SOURCE_TRACE

```text
Study Web screen -> typed feature data-access -> Study API descriptor -> FastAPI route/view/validation/query -> legacy BIGINT tables or VNPay/S3 -> ApiEnvelope -> screen state
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #26 source coverage | Current `v1.py` and `api_26_lessons_resources` include a route/view/model/query; DD and older worklogs say no source. | `DISCREPANCY` | Reconcile docs to source; secure the existing route rather than create a duplicate. |
| API #11 collection response | Current query reads all rows ordered by ID; view returns `rows[0]`; user approved `Resource[]` and empty `200 []`. | `SOURCE_CHANGED / CONTRACT_CHANGE_APPROVED` | Update endpoint model and GS-06 client mapping. |
| Resource access/schema | #12 returns a stored direct URL; legacy resources table has no visibility/storage key; live schema is unknown. | `CONTRACT_GAP` | Add visibility/storage mapping and access checks; default legacy rows private and fail closed for unsafe URL mapping. |
| Payment/order/operations | Migration 015 creates `orders`; legacy `payments` lacks `order_id`; no generic Study operations table exists; #17 returns 503. | `SOURCE_REQUIRED / CONTRACT_CHANGE_APPROVED` | Extend existing order/payment schema and implement VNPay sandbox plus durable generic operations. |
| Admin/report APIs | #99–#103 have no Study Server routes; policy packs were approved in conversation. | `NOT_FOUND / CONTRACT_APPROVED` | Implement routes, persistence, auth and export worker. |

## CHANGES

- Files changed: active worklog created and updated with current migration/source evidence; implementation files pending.
- CONTEXT_UPDATES: pending source/API/DD changes and final source drift check.
- Context pages changed: pending.
- Assumptions: target local Study legacy BIGINT schema; no production deployment. Sandbox credentials remain environment configuration and must not be committed.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | `READY`; T040/T038/T039 selected. | `VERIFIED_PREFLIGHT` |
| Migration/schema inspection | Read migrations 015/016, legacy DDL, database context and relevant query source. | `VERIFIED_STATIC` |
| Study backend/client tests, build and browser checks | Not run for T041 yet. | `NOT_RUN` |
| Live database/VNPay runtime | Not checked; sandbox credentials/deployment are external. | `NOT_VERIFIED` |

## HANDOFF

- Remaining blockers: none for approved local contracts; live VNPay credentials/database deployment remain external runtime dependencies.
- Next action: trace exact API caller/query/tests and migration conventions, implement backend foundations before dependent screens.
