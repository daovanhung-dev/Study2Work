---
task_id: "2026-10-25-implement-api49-mentor-content-list"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Chuẩn bị implementation API #49 — Mentor content list

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: API #34 lưu metadata trong `uploads`; không xem storage object hay live DB là đã xác minh.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: API #47 dùng Mentor trực tiếp sở hữu course và `lessons`/`lesson_uploads`; schema runtime chưa được xác minh.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: API #48 đọc `lessons` cùng ordered `lesson_uploads`/`uploads`, dùng direct owner và giữ NULL content; không phải generic Content tree.
- shortage: `none` (selector tìm thấy đủ 3 worklogs cùng type)

## EXPECTED_BEHAVIOR

- Requirement: Implement API #49 theo AC-22, rà các API #50–#53 liên quan, lập plan trước runtime edits, gọi endpoint qua TestClient và giữ các thay đổi worktree có sẵn.
- Expected contract: `GET /api/v1/mentor/courses/{course_id}/content`, Bearer JWT Mentor, `course_id:int64!`, không body/query, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, catalog error set 401/403/404/500. Catalog, AC-22 diagram and DD now use `ApiEnvelope<Content[]>` as an implementation decision; DD remains `Draft — Needs Confirmation`.
- AC-22 yêu cầu Mentor có quyền quản lý course; #50–#53 tạo, sửa/version, publish và soft-delete Content rồi reload cây.

## CURRENT_BEHAVIOR

- Source/config: Route #49, view/models/query/validate, middleware dispatch entry and `contents` legacy DDL/migration 006 are now present in checked-in source.
- Runnable tests: 20 focused TestClient cases pass; the full Study suite passes 356 tests.
- Runtime wiring: Source-backed locally; fake database sessions and SQL artifacts do not verify live DB schema, migration deployment or service deployment.

## SOURCE_TRACE

```text
GET /api/v1/mentor/courses/{course_id}/content
  -> FastAPI router / signed-int64 OpenAPI schema
  -> shared Mentor JWT guard -> numeric principal
  -> SELECT courses.id/mentor_id -> direct-owner branch
  -> SELECT active contents rows -> validate projection/tree integrity
  -> Content[] success envelope or catalog 401/403/404/500
```

Implementation uses the current Study pattern: thin router → module `view.py`; Mentor guard uses `validate_current_user_request(..., role="MENTOR")`; SQL constants stay in `query.py`; `view.py` owns DB orchestration, rollback and envelope.

## IMPLEMENTATION_PLAN

1. Resolve contract/schema mismatch using the requested precedence. AC-22 describes loading an entire tree; legacy BIGINT infra matches current Study runtime and Mentor ownership APIs but has no generic Content table; V1-PILOT has a different UUID/versioned course model. Use the current legacy BIGINT runtime model and add a minimal `contents` relation backed by the catalog's Content fields. Keep `content_type` and `status` as strings because no closed enum members are approved; keep payload as JSONB object.
2. Resolve tree cardinality with a flat ordered `Content[]` result. `parent_id` expresses the hierarchy and avoids a recursively nested payload schema. Update the catalog and AC-22 diagram together because their current singular `Content` response cannot represent multiple nodes. An existing course with no nodes returns `[]`; only a missing course returns 404.
3. Add `contents` to legacy `DB.sql` and a new `006_contents.sql` migration artifact. Use BIGSERIAL ID, BIGINT course FK, self-referencing parent ID scoped to the same course, `content_type`, `title`, object JSONB `payload`, open string `status`, `content_order`, and nullable `deleted_at`. Do not run the migration against a live database.
4. Implement `mentor/api_49_mentor_content_list` with response models, signed-int64 path parsing, SQL-only query constants, and a view that authenticates `MENTOR`, checks direct `courses.mentor_id` ownership, selects all non-deleted nodes without status filtering, sorts by parent/order/id, validates projections, rolls back read failures, and returns the catalog envelope.
5. Wire the thin route and `DESIGN_CONTRACT_PATHS` template; preserve only the declared 401/403/404/500 API business codes. Expose the int64 path schema in OpenAPI while mapping malformed/out-of-range raw path values to the catalog 404.
6. Add API-level TestClient coverage for auth, direct ownership, missing course, empty tree, node hierarchy/order, soft-delete filtering, database/mapping failures, trace/envelope, and OpenAPI. Run the focused API suite, full Study suite, Ruff, OpenAPI/import and diff checks.
7. Update API #49 DD and source-context pages/manifest; record the new physical table as checked-in design/runtime source while keeping live migration status unverified. Macro-review #50–#53 and update their persistence notes where the new table changes their source inventory; leave version history, lifecycle transitions and payload/type rules open where their source remains incomplete.

### Conflict resolution

- Diagram precedence: AC-22 requires loading a content tree before CRUD/publish; its singular response label conflicts with that purpose.
- Infra precedence: legacy `courses` is BIGINT and is the schema family used by APIs #46–#48; the V1-PILOT `courses/course_versions/chapters/lessons/content_blocks` model uses UUID and is not compatible with the current router/auth source.
- Catalog precedence: the current reusable `Content` fields provide the minimal physical projection, but `ApiEnvelope<Content>` cannot return a tree. Chosen fallback is `ApiEnvelope<Content[]>` with `parent_id` links, synchronized in the catalog and diagram.
- Reusable fields do not define closed `ContentType`/`ContentStatus` members or payload keys; implementation will preserve them as open string and JSON object values rather than invent enums or subtype payload rules.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Cây hay một Content | AC-22 mô tả tree; diagram/catalog hiện ghi một `Content` | `RESOLVED_BY_IMPLEMENTATION_DECISION` | Chuyển response thành phẳng `Content[]`, dùng `parent_id` cho quan hệ cây và đồng bộ diagram/catalog/DD |
| Legacy persistence | Legacy runtime schema uses BIGINT `courses`; API #50–#53 share the Content entity; API #49 adds base `contents` to local DDL/migration 006 | `RESOLVED_BY_IMPLEMENTATION_DECISION` | Base mapping exists in checked-in artifacts; live migration/schema remains unverified and version history is open |
| V1-PILOT persistence | `infra/postgres/02_study_db.sql` dùng UUID cho `course_versions/chapters/lessons/content_blocks`; `content_blocks` gắn `lesson_id`, có `block_type/content_json/position` | `NOT_SELECTED` | Không trộn model/course IDs UUID vào legacy API runtime |
| Content projection | Catalog yêu cầu `content_type`, `title`, object `payload`, `status`, optional `parent_id`, `order`; enum members/payload keys chưa có nguồn | `RESOLVED_PARTIALLY` | Lưu strings/JSON object đúng field; không thêm closed enum hoặc payload schema; direct row mapping only |
| Mentor access | AC-22 yêu cầu quyền quản lý; `courses.mentor_id` là pattern runtime ở #46–#48; assignment relation chưa có trong legacy infra | `RESOLVED_BY_IMPLEMENTATION_DECISION` | Dùng direct owner `courses.mentor_id`; không mở rộng sang assigned-course access |
| Empty-tree behavior | AC-22 mở màn hình trước thao tác create; catalog liệt kê 404 nhưng không gắn điều kiện | `RESOLVED_BY_IMPLEMENTATION_DECISION` | Existing course with no nodes returns HTTP 200 and `data: []`; missing course returns 404 |
| Error dispatch | API #49 route template is in `DESIGN_CONTRACT_PATHS`; `error_response` omitted data is JSON null | `RESOLVED_BY_IMPLEMENTATION` | Shared error dispatch preserves catalog codes 401/403/404/500 |
| Related mutations | Local `contents` covers base Content fields, parent/order and deleted_at; #50–#53 still lack wired mutations/version history and approved lifecycle rules | `OPEN` | Macro-review records the shared base mapping while keeping version, lifecycle, access and delete policies open |

## CHANGES

- Files changed: API #49 module/route/middleware/tests; legacy `DB.sql` and migration 006; API catalog; AC-22 and ERD diagrams; DB table guide; API #49 DD; linked API #50–#53 persistence notes; server-study context pages and manifest; worklog. Existing unrelated dirty files were preserved.
- CONTEXT_UPDATES: `.agents/server-study/{AGENTS,architecture,apis/declared-routes,core/database-security,core/runtime,database,modules/README,tests}.md` and `.agents/context-manifest.json` updated with source/test/DDL status.
- Context pages reviewed: `.agents/server-study/AGENTS.md`, `INDEX.md`, `apis/declared-routes.md`, `architecture.md`, `core/database-security.md`, `core/runtime.md`, `database.md`, `modules/README.md`, `tests.md`, `workflows/README.md`.
- Assumptions/boundaries: `Content[]`, legacy `contents` table and direct-owner authorization are implementation decisions made to fit AC-22/current Study source; they remain subject to product/schema confirmation. No closed enum or payload subtype was invented; no legacy Lesson rows were converted into Content. Live DB status is unknown.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run -A scripts/select-worklogs.mjs --type coding --limit 3` | Found 43 same-type worklogs; selected and read the API #34/#47/#48 worklogs. | VERIFIED |
| Review DD #49 và related DD #50–#53 (pre-edit) | Confirmed tree-vs-single-object gap and missing pre-existing physical Content mapping. | VERIFIED_STATIC_ONLY |
| Review router, Mentor modules, middleware, response helper (pre-edit) | API #49 route/module absent before coding; current helper defaults omitted error data to JSON null. | VERIFIED_STATIC_ONLY |
| Review legacy DDL and V1-PILOT DDL (pre-edit) | Legacy BIGINT schema had no generic Content relation; the UUID pilot model was incompatible. | VERIFIED_STATIC_ONLY |
| `git status --short` | Pre-edit worktree showed existing API #34/#47/#48, context, DB, and worklog changes; these were preserved while API #49 files were added after the plan checkpoint. | VERIFIED |
| Focused API #49 tests | 20 passed; one upstream Starlette/httpx deprecation warning. | VERIFIED |
| Full Study suite | 356 passed; one upstream Starlette/httpx deprecation warning. | VERIFIED |
| Ruff | `uv run ruff check app tests` passed. | VERIFIED |
| `git diff --check` | Passed in final post-edit verification. | VERIFIED |
| Drawio XML | ERD and AC-22 parse; Content[] output present. | VERIFIED |
| Context validator | Full and `--skip-drift` runs fail because DB Admin context/source is absent; full run also reports existing dirty-scope drift. No server-study structural error in skip-drift output. | BASELINE_BLOCKER |

## HANDOFF

- Remaining boundaries: The selected `contents` physical model and array projection are local implementation decisions, not evidence of live DB schema. Content type/status enumerations, payload subtypes, assigned-course policy, publish lifecycle and API #51 version-history model remain open. Repository context validation is blocked by existing missing DB Admin context/source.
- Next owner/action: API #49 is locally implemented and verified; the next coding session may start API #50 using the checked-in `contents` base model while preserving unresolved lifecycle/version and live-schema boundaries.
