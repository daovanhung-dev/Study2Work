# Báo cáo kiểm chứng — API #93 Tạo/phát notification

## Phạm vi và trạng thái

- DD folder: `apps/study-server/docs/dd/93_admin_notifications_create/`.
- DD status: `Draft — Needs Confirmation`; contract trực tiếp được giữ, local fallback DERIVED.
- Runtime status: route/module wired and HTTP-tested with fake DB projections.
- Không kiểm tra live database, migration deployment, provider delivery hoặc owner approval.

## Nguồn đã đối chiếu

- API catalog #93, reusable Notification/Operation schemas và Operation tracking summary.
- AC-36 API index/diagram; CREATE/SEND và conditional Push/Email edge.
- Legacy Study BIGINT DDL, migration 009 và separate V1-PILOT notification/delivery model.
- DD #92, #96, #63, #64, #18; shared Admin auth, database and response helpers.
- Study workflow, registered `createDD-markdown` skill, 8 standard templates and selected coding worklogs.

## Template and package

- Package: 13 Markdown files — 8 standard sheets, 2 supplementary mappings, and 3 reports.
- All 8 standard sheets match their respective template appendix; both supplementary mappings match the canonical `07_table.md` appendix: 10/10.
- Sheet front matter contains `dd_id: "93"`: 10/10.
- Local links/anchors: 52/52 pass. Fenced JSON examples: 2/2 parse. All sheet files have final newlines and no trailing whitespace.
- Recipient grain and delivery outbox have separate mapping files; neither marks local DDL as live/approved schema.

## Runtime verification

| Check | Result | Status |
|---|---|---|
| Focused API #93 HTTP suite | 26 passed; 1 upstream Starlette/httpx warning | PASS |
| Linked #63/#64/#87/#92/#93 regression | 111 passed; same warning | PASS |
| Full Study Server suite | 1243 passed; 1 upstream Starlette/httpx warning | PASS |
| Ruff lint | Full `app` and `tests` check passes | PASS |
| Ruff format | All 8 changed Python files pass scoped format check | PASS |
| OpenAPI | 54 `/api/v1` path templates / 64 operations; #93 shares #92 path | PASS |
| Manifest JSON | Parses; #93 source/test paths registered | PASS |
| `git diff --check` | No whitespace errors | PASS |
| Agent context validator | Study source paths have no missing-path findings; overall validation fails on missing DB Admin scope files/roots and cannot evaluate source drift because the manifest `sourceCommit` object is unavailable | SCOPE LIMIT |

A repository-wide Ruff format check reports 60 other files in the existing worktree would be reformatted. No broad formatter write was made; API #93 and directly changed route/test files pass scoped formatting.

## Preserved discrepancies and limits

- Catalog/diagram response `Notification` conflicts with generic Operation tracking prose.
- Request has no action/schedule field although diagram dispatches only when action is Send; immediate enqueue is DERIVED.
- The implementation uses checked-in legacy BIGINT `notifications`/`notification_deliveries` candidates; neither is proven deployed or approved for Admin campaign use.
- AudienceSegment expansion and fine-grained notification-management permission are not implemented.
- Batch UUID/notification ID metadata is DERIVED and does not create an Operation record or settle API #18/#96 linkage.
- No provider/worker is invoked; HTTP 202 means the local transaction committed, not that a message was delivered.
