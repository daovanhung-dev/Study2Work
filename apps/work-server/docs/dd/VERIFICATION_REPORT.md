# VERIFICATION_REPORT

## Overall result

- Status: `PASS_WITH_DECLARED_NOT_RUNNABLE_COMMANDS`
- Runtime route folders: `21`
- Markdown files: `176`

## Template fingerprint

| Template file | SHA-256 |
| ---: | --- |
| 00_Cover.md | fd5f568c5329d3069fbaff617a6f4ed3b5ffaf050e042c95b7c9100a05f79e63 |
| 01_Lich_su.md | d1cec6573433a9551812bf47552f8a44d7c533d790341941047c410e1d57771e |
| 02_Overview.md | c2879c2f0e007395558dfee4167484786c5aadb3fdd63ab135ca111e7c5f8aa6 |
| 03_Request.md | 37aaa1e9d7f3e83329e81ab38d922c9dff959284d5b7b3ae353878798dd4b7aa |
| 04_Response.md | 5bcb43ba5eb487302dd5d5efde4383b9f452f9fed2149f55315d64ff78a19ab8 |
| 05_Data_Mapping.md | 11bc77bc0522d3af27b9499114991c8819046ac32bde5c1efdc841be088dcc5b |
| 06_Error.md | e0160ea07fdbc74f2cafebd6ed3b21e60029662d28d67f5f6a0b4d95ba72be9b |
| 07_table.md | 4c9a0e037872333210aaf44ba9fbf00a0e63343a69d55250e537d2c3c5e2d356 |

## Source-name reconciliation

- `PASS` — all 21 DD folders retain their original `dd_id` and folder name.
- `PASS` — all 21 `api_name` values now identify the current source handler/use-case or the owning inline handler.
- `PASS` — `API_CATALOG.md`, `COVERAGE_MATRIX.md`, `PLAN_RESULT.md`, Covers and Overviews include source runtime mapping.
- `PASS` — compatibility endpoints and operation IDs remain unchanged.
- `PASS` — old descriptive display labels were removed from the 21 API DD folders.
- `PASS` — report tables have consistent column counts and root source links resolve from `docs/dd`.
- `PASS` — ZIP contents match the current 176 deliverables byte-for-byte.

## Verification items

- `PASS` — 21 runtime route folders are present.
- `PASS` — 176 Markdown files are present: 21 folders × 8 files plus 8 root reports.
- `PASS` — every folder contains `00_Cover.md` through `06_Error.md` and exactly one `07_*` mapping file.
- `PASS` — read-only endpoints contain `N/A — READ-ONLY API`; mutation endpoints contain operation-specific mapping files.
- `PASS` — JSON fences parse successfully.
- `PASS` — relative Markdown links resolve.
- `PASS` — no stale source path, generic success/error placeholder, unresolved template placeholder or old DD status remains.
- `PASS` — request/response/error/mutation rows follow the one-field/one-condition/one-column rule.
- `PASS` — `work-server-dd.zip` is readable and contains exactly the generated DD files.
- `PASS` — Deno TypeScript fallback: `node_modules/typescript/bin/tsc --noEmit`.
- `PASS` — Deno Vitest fallback: 1 file, 12 tests passed.
- `PASS` — Deno Prisma fallback: `prisma validate` with non-production placeholder database URLs.
- `PASS` — Deno contract fallback: `scripts/validate-contracts.mjs`.
- `PASS_WITH_DRIFT_SKIPPED` — `scripts/validate-agent-context.mjs --skip-drift`.
- `DECLARED_NOT_RUNNABLE` — requested `pnpm` commands because `pnpm`/Node are unavailable in the environment.
- `CONTEXT_STALE` — exact context validator without `--skip-drift` reports pre-existing uncommitted Work Server source snapshot drift; it does not report a DD structure failure.
- `PASS` — `deno run --allow-read --allow-run --allow-env scripts/validate-contracts.mjs`.
- `PASS` — final DD naming/static check: 21 folders, 176 Markdown files, 176 ZIP entries, JSON/link/table/content checks passed.

## Source discrepancies preserved

- Legacy `matkhau` login alias and plaintext compatibility fallback.
- Target-only catalog endpoints remain excluded.
- Runtime source wins over stale historical DD text.
