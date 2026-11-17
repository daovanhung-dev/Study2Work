# Task milestone ledger: ST-11–ST-26 FE interactions

## Scope and approvals

- Task: implement the remaining unambiguous FE interactions for ST-11–ST-26.
- User-approved boundary: FE-only; implement DD/API behaviors that are clear; leave blocked actions unavailable. No BE, auth, DB, schema, migration, canonical DD/API catalog edits, or production fake records.
- SPEC v1 approved: `apps/study-client/docs/implementation/study_client_dd_interactions_st11_st26/SPEC.md`, SHA-256 `83248A39F5E8646A42F79D7B5A01F74C4D955D7BEF3D133130A8D8208883CEE7`.
- PLAN v1 approved: `apps/study-client/docs/implementation/study_client_dd_interactions_st11_st26/PLAN.md`, SHA-256 `7795140B18674C7D5557F8D99DB8CE890A354AA101EAE0819E44C51F60F93F21`.
- Canonical worklog `.agents/worklog/2026-11-17/complete-st11-st26-dd-interactions.md` could not be written because `.agents` is mounted read-only; this companion ledger records the execution.

## Milestones

| Weight | Cumulative | Milestone | Status |
|---:|---:|---|---|
| 15% | 15% | Repository/worklog/context preflight and preserve pre-existing dirty work. | DONE |
| 25% | 40% | Reconcile DD/API/source; obtain exact SPEC and PLAN approvals. | DONE |
| 40% | 80% | Implement approved ST-14/ST-26 interactions and focused tests. | DONE |
| 20% | 100% | Run build/tests/Playwright, inspect screenshots and scoped diff; obtain final revision approval. | DONE |

## Implementation

- ST-14: one question at a time in API response order, previous/next and question grid; selections remain keyed by question ID within the page instance. Navigation causes no API request. Existing answer-save and submit actions remain.
- ST-26: all/unread filter query mapping, accessible active state, disable filters while loading/mutating, preserve filter after successful #44/#45 refresh. No local counts or optimistic row changes.
- Added focused component tests for both screens. Fixtures are test-only; no production fake business data was added.
- Preserved blocked behavior on the other screens and unresolved ST-26 `is_read` schema discrepancy; the FE reads that property only if provided.

## Verification

- `npm.cmd test` in `apps/study-client`: PASS, 6 test files and 22 tests.
- `npm.cmd run build` in `apps/study-client`: PASS. Angular emitted 7 CSS budget warnings (shared/student-layout and ST-14, ST-17, ST-19, ST-22, ST-24 stylesheets); no build errors.
- Playwright FE interaction verification: PASS at desktop and mobile for ST-14 and ST-26 using isolated test-only API response fixtures. Verified question navigation and selection persistence, all/unread queries and mutations/filter refresh, and zero browser console errors/warnings. This does not claim live Study Server/API success.
- Screenshots: `.static-preview/st14-st26-interaction-verification/{st14-desktop,st14-mobile,st26-desktop,st26-mobile}.png`.
- `git diff --check` on the 9 scoped ST-14/ST-26 source and test files: PASS; Git only reports configured LF-to-CRLF conversion notices.
- Dedicated verification server on port 51281 was stopped. Existing user server on 51280 was left untouched.
- Worktree contains many unrelated pre-existing changes and artifacts; none were reset, staged, committed, or pushed.

## Remaining gate

- Source snapshot SHA-256 over the 9 sorted ST-14/ST-26 source and test files: `D9AD2340716D5985291DED5DD06A2D0ABCA66F2BC0950313A8AA3D8A092EE099`.
- User approved source snapshot SHA-256 `D9AD2340716D5985291DED5DD06A2D0ABCA66F2BC0950313A8AA3D8A092EE099` on 2026-11-17.
- No commit or push is part of this task.
