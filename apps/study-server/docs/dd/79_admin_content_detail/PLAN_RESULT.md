# Kết quả lập kế hoạch — API #79 Lấy chi tiết Content

Trạng thái tài liệu: `Draft — Needs Confirmation`.

## Nguồn đã đối chiếu

| Nguồn | Đọc/đối chiếu | Kết quả |
|---|---|---|
| `docs/lists/list_api.md` | API #79 + reusable Content | Bearer/Admin, int64 path, singleton `ApiEnvelope<Content>`, errors 401/403/404/500. |
| `AC_UNICA/00_AC_API_INDEX.md` và `AC_04_ADMIN_MANAGEMENT.drawio` | AC-33 entry/nodes/edges | #78 queue → #79 reads content/version/author → #80/#81 decision → reload. |
| DD #78 | Overview/Mapping/Open Questions/Report | Queue selects active pending rows; revision and stale-item policy remain open. |
| APIs #49–#53 source | Content list/create/update/publish/delete | Current Study source uses `contents`; no creator field in insert; `archived_by` is updater. |
| Legacy `DB.sql`, migrations 006/007 and table guide | Physical candidate relations | `contents` and `content_versions` have BIGINT Content projection/snapshot fields; author source absent. |
| V1-PILOT `02_study_db.sql` | course_versions/content_blocks/review decisions | UUID-scoped model; not mapped directly to current BIGINT Content contract. |
| API #69/#78 and shared router/auth/middleware/response | Closest local runtime patterns | Raw int64 path detail, ADMIN guard, static queue precedence, error `data:null`. |
| Worklog selector and selected coding logs | Required preflight | #74/#75/#76 plus API #78 implementation worklog read before source edits. |

## Implementation decisions

- Add GET `/api/v1/admin/content/{content_id}` after fixed #78 route and register the dynamic contract path.
- Guard ADMIN before parsing raw path/DB access; invalid signed-int64 and missing/soft-deleted rows map to 404 per catalog/#69 precedent.
- Read one active `contents` row with a bound ID and map the exact eight Content fields. Do not filter current status again.
- Return only direct `ApiEnvelope<Content>`; no version/author fields or inferred join. Do not mutate or commit.
- Query/projection failures use safe 500 with rollback. Fake database tests establish local route behavior only.
- Keep DD Draft and record checked-in DDL vs live schema boundary plus AC-33 version/author discrepancy.

## Direct-versus-derived boundary

| Item | Evidence | Status |
|---|---|---|
| Path/auth/response/errors | API catalog #79 | DIRECT |
| Read version/author intent | AC-33 n6 | DIRECT, conflicts with response schema |
| `contents` current-row projection | DDL + APIs #49–#53 | CURRENT SOURCE candidate |
| Active-row filter | API #49/#53 and deleted_at column | DERIVED |
| Return current status without pending recheck | Catalog omits status filter; #78 already selects pending | DERIVED; stale policy open |
| Malformed/out-of-range path → 404 | API #69 precedent and #79 error set | DERIVED |
| Author and selected revision | No matching field/selector | SOURCE_REQUIRED; not implemented |

## AC-33 handoff

API #79 is read-only. API #80/#81 own approval/rejection and any decision/audit writes. Current detail path does not identify a revision, so the next APIs must not claim that `content_versions.archived_by` identifies the author or that the queue item remains current. The broader AC-33 sequence remains under review until revision identity and metadata projection are resolved.
