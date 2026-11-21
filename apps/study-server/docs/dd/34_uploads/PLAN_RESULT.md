# Plan Result — Study API #34

## Status

Implemented locally; DD status is Draft — Ready for Review. API #47 remains UNWIRED.

## Source changes

- Added `POST /api/v1/uploads` with multipart file, purpose and optional course_id.
- Extended the shared auth guard to accept a role string or role sequence; current single-role API callers preserve their behavior.
- Added purpose/role rules, ACTIVE enrollment check and direct Mentor course owner check.
- Added lazy S3-compatible stream upload/delete adapter using existing Object Storage configuration and server-generated UUID keys.
- Added `uploads` legacy BIGINT table artifact and `004_uploads.sql`; migration was not applied to live DB.
- Added `python-multipart` to `pyproject.toml` and `uv.lock`.
- Added API #34 HTTP tests for policy, malformed forms, metadata, S3/DB failures and compensation.
- Updated API catalog and API #34/#47 DDs with approved asset decisions; #47 remains unwired pending `content:int64` semantics.

## Persistence mapping

- `uploads.id` is generated as BIGSERIAL and returned as UploadAsset int64 ID.
- The row persists owner, purpose, optional course, storage key, filename, public URL, content type, measured byte size and UPLOADED status.
- Object upload precedes the metadata INSERT; DB failure rolls back and triggers best-effort object deletion.

## Verification boundary

Focused API #34 tests and broader Study checks are recorded in [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md). Local verification does not establish live DB migration, real S3 behavior or deployment.
