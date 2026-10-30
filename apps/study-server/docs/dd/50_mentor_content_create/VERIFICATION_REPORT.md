# Verification Report — API #50 Tạo nội dung mới

## Phạm vi

Kiểm tra implementation local của `POST /api/v1/mentor/content`, bộ DD
Markdown, các page context Study Server và manifest sau khi wire route. Runtime
tests dùng fake DB; checked-in DDL/migration 006 không chứng minh live schema
hoặc migration deployment. DD giữ trạng thái `Draft — Needs Confirmation` vì
các quyết định DERIVED và lifecycle/schema production còn cần xác nhận.

## Deliverable manifest

| File | Vai trò | Trạng thái |
|---|---|---|
| `00_Cover.md` | Cover | PASS |
| `01_Lich_su.md` | Lịch sử | PASS |
| `02_Overview.md` | Overview | PASS |
| `03_Request.md` | Request + request usage | PASS |
| `04_Response.md` | Response + Content projection | PASS |
| `05_Data_Mapping.md` | Query, mutation, mapping matrices | PASS |
| `06_Error.md` | Exact catalog errors | PASS |
| `07_table.md` | Local `contents` mapping | PASS |
| `PLAN_RESULT.md` | Plan and pre-authoring matrices | PASS |
| `OPEN_QUESTIONS.md` | Source/approval gaps | PASS |
| `VERIFICATION_REPORT.md` | Verification record | PASS |

## Contract and source checks

| Check | Result | Evidence level |
|---|---|---|
| Request/response | `POST /api/v1/mentor/content`, four required body fields, HTTP 201 `DESIGN_RESOURCE_CREATED`, `ApiEnvelope<Content>` | Catalog match; local route/model implemented |
| Error set | 401/403/422/500 with declared `DESIGN_*` codes; no 404 added | Catalog match; TestClient-covered |
| Authorization | Shared Mentor guard, numeric JWT subject, direct `courses.mentor_id` ownership | Current source; assigned-course policy remains open |
| Mutation | Locks course, allocates non-negative next active-root order, inserts root Content as `PENDING_REVIEW`, validates RETURNING row, then commits | Local implementation; defaults marked DERIVED |
| Middleware | `/api/v1/mentor/content` is in `DESIGN_CONTRACT_PATHS` | Current middleware; framework 422 TestClient-covered |
| Local schema | Legacy `contents` table in `DB.sql` and migration 006 matches the local BIGINT/JSONB projection | Checked-in artifact only; live status unknown |
| Macro-review | AC-22 #49–#53 sequence reviewed; unresolved lifecycle/version questions retained | `VERIFIED_WITH_OPEN_QUESTIONS` |

## Verification results

| Check | Result | Status |
|---|---|---|
| Focused API #50 tests | `25 passed`; one upstream Starlette/httpx deprecation warning | VERIFIED |
| Full Study Server suite | `381 passed`; same deprecation warning | VERIFIED |
| Ruff | `uv run ruff check app tests` — all checks passed | VERIFIED |
| Import/OpenAPI | 21 `/api/v1` paths; `/api/v1/mentor/content` present; request int64 schema covered by focused test | VERIFIED |
| Context manifest | JSON parses and lists API #50 module/test source paths | VERIFIED_STATIC_ONLY |
| `git diff --check` | No diagnostics | VERIFIED |
| Context validator | Deno compatibility invocation fails on existing DB Admin context/source/link gaps; full mode also reports repository snapshot drift. `--skip-drift` reports the DB Admin baseline only and no API #50 missing source/page finding. | BLOCKED_BY_REPOSITORY_BASELINE |

## Limitations and open decisions

- Fake DB tests verify route orchestration and response mapping, not PostgreSQL
  locking, live schema, migration application, deployment or production data.
- `PENDING_REVIEW`, root placement, zero-based order and 403 for absent courses
  are implementation decisions derived from current diagram/catalog evidence;
  they remain subject to product confirmation.
- Content type members, payload subtype schema, assigned-course access,
  versioning, moderation/audit behavior and live migration state remain open.
- The repository context validator baseline is outside this Study Server task;
  unrelated DB Admin context/source was left untouched.

## AC-22/AC-33 Macro-review #49–#53

**Status:** VERIFIED_WITH_OPEN_QUESTIONS.

- AC-22 flow: #49 reads the flat `Content[]` tree, #50 creates a root and the
  client reloads the tree, #51 updates Content/version, #52 publishes/unpublishes,
  and #53 soft-deletes. Mutation defaults and transitions remain subject to
  their own source/approval evidence.
- #50/#51 use `PENDING_REVIEW` as a DERIVED proposal for new Content/revisions;
  AC-33's approve action mentions `APPROVED`/`PUBLISHED` plus audit, so automatic
  publication behavior is unresolved.
- #52 owns publication transitions. #53 proposal requires unpublishing a
  `PUBLISHED` node through #52 first and does not mutate `Content.status`.
- #53 proposal blocks deletion when direct children remain and does not
  cascade/reparent. Soft-delete history, moderation queue filtering and audit
  storage remain unconfirmed.
- The local legacy `contents` base mapping and API #50 middleware route are now
  implemented. Live schema, version persistence, assigned Mentor access,
  payload/type enums, readiness rules and lifecycle/error contracts remain open.
