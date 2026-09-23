# Repository Capability Review

## Metadata

- task_id: repository-capability-review-2026-09-18
- date: 2026-09-18
- task_type: docs/review
- source_provenance: source-owned; Git history/blame not used
- mutation_policy: no source, config, schema, migration, generated output, or credential changes

## Scope

- Foundation, scripts, context registry, contracts, docs, and infra.
- Study client/server.
- Work web/server and Prisma.
- Work mobile apps.
- AI server.
- DB Admin web/server.
- Git-owned text/source/config/test/contract files were reviewed; dependencies, caches, build output, and binary assets were excluded.

## Expected behavior

- Produce an evidence-based assessment of repository engineering maturity and likely ability relative to an early fourth-year IT student.
- Separate implemented and verified behavior from design-only, placeholder, or unwired behavior.
- Do not attribute the uncommitted `apps/study-client/vite.config.ts` change to the author without provenance.

## Current behavior evidence

- Work server: strict TypeScript passes; Vitest 20 tests pass; canonical Prisma validation passes.
- Work web: strict TypeScript passes; Vitest 5 tests pass.
- DB Admin server: 45 pytest tests, Ruff, and mypy pass.
- DB Admin web: Angular production build and 15 browser tests pass; launcher tests 2/2 pass.
- Study server: application import passes, but pytest collection is blocked by a stale auth test import; Ruff has 2 import-order errors and mypy has 4 errors.
- Study web: current local Vite config contains an uncommitted malformed first line; vue-tsc and Vitest therefore fail against the current worktree. HEAD contains the valid import.
- Mobile Flutter analysis/tests were not runnable because Flutter/Dart are unavailable in the environment.
- AI server has no checked-in test suite.
- Contract validation passes, but event schemas are placeholder schemas and therefore do not establish meaningful event compatibility.
- Full context validation reports `CONTEXT_STALE` in multiple scopes; `--skip-drift` reports the registry wiring as valid.

## Key discrepancies

- Root documentation references canonical `docs/BD` documents that are absent.
- Work target OpenAPI contains paths not present in the current route graph; the legacy contract is closer but still incomplete.
- Study and Work contain tracked, actual-looking credential/key material in source/constants; values are intentionally not reproduced here.
- Mobile apps connect directly to Neon and persist/compare plaintext passwords locally; their own README files acknowledge this as non-production architecture.
- Work and Study have meaningful architecture in selected paths, but also legacy/unwired modules, static placeholders, and partially wired product surfaces.
- Current runtime source is preferred over stale context pages or design-only contracts when describing behavior.

## Verification commands

- `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift`: pass.
- `deno run --allow-read --allow-run --allow-env scripts/validate-contracts.mjs`: pass.
- `git diff --check`: pass.
- App-specific TypeScript, Python, Prisma, Angular, and Vitest/Pytest commands are recorded in the review response and were run without source modifications.

## Review conclusion

- The repository is a strong proxy for above-average student engineering ability, especially in backend boundaries, dependency injection, typed contracts, security/control-plane design, and process tooling.
- It is not evidence of production readiness across the whole system: breadth exceeds verified completion, security debt remains in mobile and tracked configuration, and several contracts/tests/docs are stale or vacuous.
- Recommended positioning: strong internship candidate and plausible junior backend/full-stack candidate if able to explain the implementation; not yet a production-ready engineer without hardening and verification work.

