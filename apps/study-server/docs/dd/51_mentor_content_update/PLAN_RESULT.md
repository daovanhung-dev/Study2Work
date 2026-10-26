# Plan Result — API #51 Mentor Content update

## Task classification

```yaml
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: []
```

## Source order and decision

1. AC-22 diagram: Mentor performs `UPDATE Content + version`, then reloads the tree.
2. Legacy infra: migration 006 defines BIGINT `contents` base fields, but no version relation; V1-PILOT `content_blocks` is a different UUID/lesson model.
3. API catalog: exact path, response and 401/403/404/422/500 error set, but no request body.
4. Simplest clear fallback, explicitly `DERIVED`: body uses API #50 editable fields; add a legacy snapshot table for the pre-update Content state.

The fallback does not become approved contract. The DD remains `Draft — Needs Confirmation`.

## Requirement and implementation matrix

| Requirement | Evidence | Runtime result | Status |
|---|---|---|---|
| Mentor Bearer + role | API catalog; shared `validate_current_user_request` | Shared guard with `role="MENTOR"` before DB access | Source-backed implementation; assigned Mentor unresolved |
| `content_id:int64!` | API catalog + AC-22 | Raw path parsed as signed int64; malformed/out-of-range maps to catalog 404 | Direct path; error mapping follows API #48 pattern |
| Update Content + version | AC-22 | Lock active Content/Course; insert prior state in `content_versions`; update `contents` in one transaction | Version schema/semantics DERIVED |
| Request fields | API #50 body; #51 catalog omits body | Required strict `content_type`, `title`, object `payload`; forbid extras | DERIVED; catalog update pending |
| Review transition | AC-33 queue + API #50 precedent | New current projection is `PENDING_REVIEW` | DERIVED; #52 and Admin approval integration open |
| Success response | Catalog #51 + shared #49 Content response | HTTP 200 `DESIGN_RESOURCE_UPDATED`, no version field added | Direct catalog shape |
| Error set | Catalog #51 | 401/403/404/422/500 only | Direct; no 409 added |
| Legacy migration | Existing migration 006 | Add migration 007 snapshot table and update legacy `DB.sql`/docs | Source artifact only; live schema not verified |

## Body and persistence fallback

- Full replacement body: `content_type`, `title`, `payload`.
- Stored `course_id`, `parent_id`, `content_order`, and `id` remain server-managed.
- Each PUT archives the current row with sequential `version_no`; the current `contents` row is implicit next version.
- `archived_by` means the Mentor performing the next update, not the original author required by AC-33.
- Current row moves to `PENDING_REVIEW`; old state is preserved in history, but public published-version selection is not defined here.

## Transaction and error plan

- Authentication and request validation follow current Study router/middleware.
- Lock Content plus its course before comparing `courses.mentor_id` with JWT subject.
- Absent/deleted -> 404; different direct owner -> 403.
- Snapshot insert and current-row update are atomic; validate both returned projections before commit.
- Query, mapping, serialization or commit error -> safe 500 and rollback.

## DD and context outputs

- Preserve template order for eight sheets; add one table mapping sheet because two tables are mutated.
- Keep body/schema/status/author/lifecycle assumptions labeled `DERIVED` or `SOURCE_REQUIRED`.
- Update Study Server route, module, DB, middleware and test context; add migration 007 to manifest.
- Do not change V1-PILOT tables or claim live DB/deployment behavior.
