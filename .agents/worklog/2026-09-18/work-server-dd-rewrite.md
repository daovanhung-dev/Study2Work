# Work Server DD rewrite — 2026-09-18

## Task classification

```text
primary_task_type: docs
secondary_task_types:
  - test
project_scopes:
  - server-work
cross_scope_dependencies:
  - contracts/openapi/work/legacy-web.openapi.json
  - contracts/openapi/work/openapi.json
```

## Expected behavior

- `apps/work-server/docs/dd` documents the current Work Server runtime accurately.
- The DD uses the checked-in `createDD-markdown` template.
- The scope contains 21 wired routes: 18 Work Web compatibility routes and 3 system routes.
- Every route has request, response, mapping, error and DB/read-only documentation.
- Status is `Draft — Ready for Review`.
- No target-only OpenAPI operation is documented as implemented.

## Current source behavior used as evidence

- Runtime registration is split between `src/app.ts` and `src/api/v1.ts`.
- Domain route boundaries are under `src/modules/*/routes.ts`.
- Zod request models are under each module `models.ts`.
- Validation/normalization is under each module `validate.ts`.
- Use-case and business rules are under each module `view.ts`.
- Prisma calls are under each module `query.ts`, with transaction boundaries in mutation views.
- Success/error envelopes, trace propagation, auth and centralized exception mapping are under `src/core` and middleware.
- Public Prisma selectors exclude password/hash fields.
- BigInt and Date are serialized by `jsonSafe`.
- Login accepts `password` and legacy `matkhau`; legacy plaintext rows can be rehashed best-effort with bcrypt cost 12.

## Discrepancies corrected

- Replaced stale `src/routes/api_routes.ts`/`src/services/*.ts` route descriptions with current module/core source references.
- Removed generic `Source success message` and `Source error message` placeholders.
- Corrected transaction documentation for CV, application and business-job compound mutations.
- Documented login rehash as a conditional write instead of treating login as purely read-only.
- Added system DDs for `/api/v1`, `/health/live` and `/health/ready`.
- Replaced stale read-only table mappings with `N/A — READ-ONLY API` where no mutation exists.
- Added current centralized and route-specific business codes, including readiness and generic fallback codes.

## Deliverables

- 21 API folders × 8 Markdown files.
- `README.md`, `API_CATALOG.md`, `COVERAGE_MATRIX.md`, `SOURCE_READ_REPORT.md`.
- `PLAN_RESULT.md`, `BUSINESS_CODE_DELTA.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`.
- `work-server-dd.zip` containing the generated DD set.

## Verification

- DD static verification: PASS.
- Typecheck fallback through Deno: PASS.
- Vitest fallback through Deno: PASS, 12/12 tests.
- Prisma validate fallback through Deno: PASS with non-production placeholder URLs.
- Contract validation fallback through Deno: PASS.
- Context validation with `--skip-drift`: PASS.
- Exact context validation: `CONTEXT_STALE` because the existing source snapshot is older than the current uncommitted Work Server refactor.
- Requested `pnpm` commands: `DECLARED_NOT_RUNNABLE` because `pnpm` and Node are unavailable.

## API naming reconciliation — 2026-09-18

### Expected behavior

- DD `api_name` values identify the current runtime handler/use-case.
- Compatibility `dd_id`, folder names, endpoint paths and OpenAPI operation IDs remain stable.
- Inline system routes are documented against their owning `createApp` or `createV1Router` handler without inventing a function name.

### Current source behavior

- Auth, students, jobs, CV and application APIs are dispatched from module `routes.ts` files into `view.ts` use-cases.
- `getMe` dispatches from `src/api/v1.ts` to `getStudentMe` or `getBusinessMe` based on the authenticated role.
- Public job listing uses `jobs.view.getJobs` and the Prisma query `jobs.query.listJobs`.
- System endpoints use inline handlers in `src/app.ts` and `src/api/v1.ts`.

### Discrepancy and resolution

- Previous DD display labels such as `List public jobs`, `Get current user` and `Create CV` were descriptive labels rather than exact runtime names.
- Resolved by changing `api_name` and adding `Source runtime handler/use-case` fields; contract IDs and folders were intentionally not renamed.

### Updated artifacts

- 21 API folders: all Markdown front matter, Cover and Overview naming metadata.
- `README.md`, `API_CATALOG.md`, `COVERAGE_MATRIX.md`, `PLAN_RESULT.md`, `SOURCE_READ_REPORT.md`, `OPEN_QUESTIONS.md`, `BUSINESS_CODE_DELTA.md` and `VERIFICATION_REPORT.md`.
- Rebuilt `apps/work-server/docs/dd/work-server-dd.zip`.

### Verification target

- Validate source-name consistency, report table structure, Markdown links/tables/JSON, contract ID preservation and ZIP contents.

### Verification result

- `PASS` — 21 DD folders, 176 Markdown files and 176 ZIP entries.
- `PASS` — all source-name mappings, report table widths, JSON fences, relative links and ZIP byte contents.
- `PASS` — `deno run --allow-read --allow-run --allow-env scripts/validate-contracts.mjs`.
- `PASS` — `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift`.
- `DECLARED_NOT_RUNNABLE` — all requested `pnpm` commands because `pnpm` is unavailable.
- `CONTEXT_STALE` — exact agent-context validation reports the pre-existing server-work source snapshot drift.
