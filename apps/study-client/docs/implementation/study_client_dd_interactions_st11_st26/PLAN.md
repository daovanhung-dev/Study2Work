# PLAN: Remaining unambiguous Study Web interactions, ST-11–ST-26

- Revision: 1
- Status: Draft for user approval
- Approved SPEC: `SPEC.md`, SHA-256 `83248A39F5E8646A42F79D7B5A01F74C4D955D7BEF3D133130A8D8208883CEE7`.
- Scope: implement R1/R2 only; preserve all other current behavior and blocked states.

## Implementation sequence

### 1. ST-14 question navigation

Files:
- `apps/study-client/src/app/features/student/ST14/pages/st14-page.ts`
- `apps/study-client/src/app/features/student/ST14/pages/st14-page.html`
- `apps/study-client/src/app/features/student/ST14/pages/st14-page.css`

Changes:
1. Add page-local current-question index and a safe getter for the question at that index.
2. Replace the all-questions list with one current question in API-returned order.
3. Add previous/next buttons and an accessible question grid. Disable edge navigation and mark the selected grid item for assistive technology.
4. Keep selection keyed by question ID; do not add answered/flagged indicators or additional API requests from navigation.
5. Retain current answer save and submit behavior.

### 2. ST-26 all/unread notification filter

Files:
- `apps/study-client/src/app/features/student/ST26/pages/st26-page.ts`
- `apps/study-client/src/app/features/student/ST26/pages/st26-page.html`
- `apps/study-client/src/app/features/student/ST26/pages/st26-page.css` only if required by existing tab styles.

Changes:
1. Add an `all`/`unread` active-filter state and a filter event handler.
2. Make `all` call #43 with page 1 and no `unread_only`; make `unread` call #43 with `unread_only=true` and page 1.
3. Disable filter controls during list load or a read mutation to avoid overlapping UI requests.
4. Keep the selected filter when #44/#45 succeeds and reloads the list.
5. Preserve optional `is_read` rendering; add no local count, optimistic status, category filter, or deep link.

### 3. Focused component tests

Add Vitest component tests:
- `apps/study-client/src/app/features/student/ST14/pages/st14-page.spec.ts`
- `apps/study-client/src/app/features/student/ST26/pages/st26-page.spec.ts`

Test only the accepted behavior using test-local API fixtures and spies:
- ST-14 order, first/middle/last navigation, grid selection, answer selection preserved after navigation, and no API write from navigation.
- ST-26 exact query arguments for both filters and active-filter preservation after #44/#45 mutation refresh.
- No production fixture or mock-data path is added.

### 4. Verification and review

1. From `apps/study-client`, run `npm test` and `npm run build`; record each result separately.
2. Start a dedicated local dev-server port without terminating or replacing a user-owned process.
3. Use Playwright at desktop and mobile viewports. If API/auth endpoints are unavailable, intercept only the two required GETs and the approved read mutations in the isolated browser session with test-only fixtures; report this as FE interaction verification, not backend/API integration proof.
4. Capture screenshots under `.static-preview/st14-st26-interaction-verification/`; preserve existing preview artifacts.
5. Inspect console errors, relevant network calls, keyboard/tab access, responsive layout, and `git diff --check` plus the scoped diff.
6. Do not stage, commit, push, edit BE/auth/DB/DD/API catalogs, remove artifacts, or modify unrelated dirty files.

## Completion criteria

- R1 and R2 acceptance criteria in SPEC pass.
- Focused component tests, Study Client build, and Playwright interaction checks are recorded with explicit PASS/FAIL/NOT_RUN and any backend limitation distinguished.
- No fake app data or blocked functionality is introduced.
- Present exact final source diff and verification results for the user's revision approval.

## Rollback boundary

Only revert edits made during this task to the six scoped page files and two new test files if a regression is found. Preserve every pre-existing modification and untracked artifact.
