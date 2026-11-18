# Review ST-04 DD, API, runtime — 2026-11-18

Type: review. Scope: current-state audit of ST-04 frontend, DD package, API #08/#15 backend, and live local browser. No source edits or test/build execution.

Preflight: `node scripts/select-worklogs.mjs --type review --limit 3` found only one prior review worklog (`review-st03-dd-api-runtime.md`); shortage 2. Read that log.

Findings:
- P1: API #15 optional auth resolves absent/invalid token to no user and queries latest enrollment by course, returning `user_id` and enrollment fields. Current-state unauthorized disclosure / wrong-student selection risk. Backend route exists despite stale DD saying missing.
- P1: ST-04 only calls #08. It cannot show entitlement, price, or already enrolled/free/paid branches. #15 remains UNWIRED in frontend; do not connect until identity contract and backend access are fixed.
- P2: Authenticated student sees `Vui lòng đăng nhập` after #08 success. CTA goes to `/student`, while prototype specifies `/courses`; `/courses` itself currently redirects to 404 in local runtime.
- Live browser: `/student/enroll/1` loaded actual course `SEED API10 - Published Reviews` and displayed blocked message. `/student/enroll/99999999` displayed course-not-found state. Mobile width screenshot looked coherent but differs from static public-shell prototype due authenticated Student layout. No direct #15 request was made.

Verification: source inspection and UI interaction only. Tests/build/linters were not run, per code-review skill. DD/contract is partly stale and G-01 remains blocked.
