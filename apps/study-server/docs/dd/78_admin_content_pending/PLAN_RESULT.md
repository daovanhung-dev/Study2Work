# Kết quả plan — API #78 Lấy pending content

## Phạm vi

Triển khai `GET /api/v1/admin/content/pending`, HTTP tests, DD #78 và Study Server context. Không sửa catalog/diagram/schema/migration/client; không triển khai #79–#81. Không tạo ZIP.

## Thứ tự nguồn và bằng chứng

| Order | Source | Evidence | Status |
|---:|---|---|---|
| 1 | AC-33 diagram/index | Admin queue; `status=PENDING_REVIEW`; #78 → #79 detail → #80/#81 → reload. | DIRECT |
| 2 | Legacy `DB.sql`, migrations 006/007 | BIGINT `contents` and `content_versions` candidate; payload JSONB object and nullable deleted_at. | CHECKED_IN CANDIDATE; live DB unknown |
| 3 | API catalog #78 / reusable schemas | Query type/course/page, `ApiEnvelope<Content>`, exact 401/403/500. | DIRECT |
| 4 | Current APIs #49–#53 | Content projection, active-row filter, create/update set PENDING_REVIEW, update snapshots previous state. | CURRENT SOURCE |
| 5 | DD #78 and linked #79–#81 | Earlier source-gap/cardinality/version questions and moderation boundary. | Draft evidence; stale physical/auth claims corrected for #78 |

## Implementation decisions

- Shared `ADMIN` guard before raw query parse and DB access.
- Use current logical rows from `contents`; filter `status='PENDING_REVIEW' AND deleted_at IS NULL`.
- Optional exact filters: `type -> content_type`, `course -> course_id`; no ContentType whitelist.
- Because collection/page flow conflicts with catalog singleton Content, local runtime uses `Page<Content>` as DERIVED. Page defaults to 1, size fixed 20, order `id ASC`, count/list use same filters, and empty/out-of-range page returns 200 empty.
- Invalid numeric `course`/`page` returns derived 422 `DESIGN_VALIDATION_ERROR`; API row currently omits 422.
- Reuse the API #49 Content projection; no version/author join, mutation, audit, schema change or migration.
- DD remains `Draft — Needs Confirmation`; catalog and diagram remain unchanged.

## Status

Runtime and focused HTTP suite were added. Full verification, final fingerprints and context count are recorded in `VERIFICATION_REPORT.md` and the worklog after the requested tests/static checks complete.
