# VERIFICATION_REPORT — Study API #66

## Kết quả

- DD status: Draft — Needs Confirmation.
- Deliverables: 8 standard sheets + OPEN_QUESTIONS.md, PLAN_RESULT.md và VERIFICATION_REPORT.md; tổng cộng 11 Markdown files.
- Runtime: API #66 route/module/middleware path wired; focused HTTP tests exercise success and error branches using fake DB sessions.
- Local response: DERIVED activity proxy from current lesson progress timestamps. It does not count learning events or event frequency.
- AC-26 related APIs: #65 course roster/progress, #66 activity proxy and #67 selected-Student progress remain separate; no server-to-server call.
- Direct discrepancy: diagram/catalog success type remains ApiEnvelope<Page<Course>>, while local summary is an activity object. Catalog and diagram were not modified.
- Runtime tests do not establish PostgreSQL live schema, migration deployment or production behavior.

## Checks

| Check | Result | Status |
|---|---|---|
| Worklog preflight | Selected 3 coding worklogs; read all 3; no shortage. | PASS |
| Source reconciliation | AC-26 diagram → checked-in DDL/table guide → API catalog → runtime #65/#66/#67 review completed. No approved event ledger found. | PASS — STATIC SOURCE REVIEW |
| API #66 focused HTTP | 18 passed; auth, role, raw int64 path, owner, aggregate, empty result, invalid projection, safe DB error, trace, read-only and OpenAPI covered. | PASS |
| API #65–#66 linked regression | 38 passed. | PASS |
| Full Study suite | 698 passed; one upstream Starlette/httpx TestClient deprecation warning. | PASS |
| Ruff | Changed Study Server Python modules/routes/middleware/tests passed. | PASS |
| Import | compileall for API #66 module and focused test module passed. | PASS |
| OpenAPI | 39 path templates / 40 operations. API #66 exposes required int64 course_id and Authorization header; responses exactly 200/401/403/404/500. | PASS |
| DD folder/static | 11 files; 8 sheets have dd_id 66 and Draft status; Markdown fences and local relative links pass. | PASS |
| Template appendix | All 8 standard sheet suffixes match registered Markdown templates byte-for-byte. | PASS |
| Manifest | Six API #66 source/test entries exist in server-study requiredSourcePaths. | PASS |
| git diff --check | Scoped API #66/runtime/context/DD paths pass. | PASS |
| Context validator | AGENT_CONTEXT_INVALID because the existing DB Admin context/source and linked context-map targets are absent. No server-study/API #66-specific error was reported. | BASELINE LIMIT |
| Live DB/deployment | Not exercised by fake-session tests or local source inspection. | NOT VERIFIED |

## Template output SHA-256

| Sheet | SHA-256 |
|---|---|
| 00_Cover.md | b4e179e32783ff16f2d0ae1ac5e018497f5040c608b7298ecdbeaffa0808bb8a |
| 01_Lich_su.md | 1a269bd73f7cf32b5183f4911718d78f69b7d5c62eb97bec543900d0b5124c9c |
| 02_Overview.md | 212a440b40372b09299915c415cf8b29f9d4f22d2b893530851c3638cbe20366 |
| 03_Request.md | f3f193c4d69401cf54e261ed3b23020b38f582b31ab80592d8e813000a10eb01 |
| 04_Response.md | 8345d87f11614b9f6dc5e923c3eb6ab2e119ac33b183e9bb5b7613d9b3b61bc3 |
| 05_Data_Mapping.md | e9b23dd6f9feab43cf9554f5225ba02f602d6e6a915c3f31806988f7e6239b57 |
| 06_Error.md | fae9b8c92e03aedd6de4d771bff5558591bb3944c58aadb9c819502a6aefb8d4 |
| 07_table.md | af29fb9f20f07264f8850ecac279142d17c35c0b21c783b7407a9d2679d93ec9 |

## Macro-review AC-26 #65–#67

Status: VERIFIED_WITH_OPEN_QUESTIONS — source/DD review and local tests.

- #65 returns class roster progress; #66 returns a distinct Student/lesson activity proxy; #67 is the selected-Student progress detail. The diagram does not show server-to-server calls.
- tracked_lesson_accesses counts distinct current progress pairs with last_accessed_at, not events. students_with_activity is not enrollment count. last_activity_at is the latest timestamp still present in current progress rows.
- The legacy DDL has no learner event history. V1-PILOT last_event_id, progress snapshots, audit_events and outbox_events do not establish a learner event source.
- Direct diagram/catalog Page<Course> does not express analytics fields; the local summary remains DERIVED and the DD remains Draft.
- Mentor direct-owner scope and legacy BIGINT mapping are local choices; live identity/schema and deployment remain unverified.
- Review of DD #67 found stale notes that Mentor guard is absent and error data defaults to an object. Current shared auth accepts MENTOR and current error helper emits null; #67 itself remains UNWIRED and should reconcile these notes in its implementation session.
