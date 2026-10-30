# API #34 Upload file — Decisions and remaining verification

**DD status:** Draft — Ready for Review
**Endpoint:** POST /api/v1/uploads

## Decisions approved and implemented

| Topic | Decision | Source/status |
|---|---|---|
| Purpose and role | `SUBMISSION` for Student; `LECTURE` for Mentor. | Approved plan; source and HTTP tests present. |
| Student course scope | `course_id` optional; when supplied, require an `enrollments` row with matching user/course and `status = 'ACTIVE'`. | Approved plan; source and tests present. |
| Mentor course scope | `course_id` required for `LECTURE`; require direct `courses.mentor_id` ownership. | Approved plan; source and tests present. |
| File acceptance | Any binary/MIME; no application allowlist or size cap; size is measured from received bytes. | Approved plan; source and tests present. |
| Filename and MIME fallback | Missing filename → `upload`; missing Content-Type → `application/octet-stream`. | Approved plan; source and tests present. |
| Object storage | Existing S3 configuration; server UUID key under `uploads/`; public URL from configured base. | Approved plan; source-backed adapter; live provider not exercised. |
| Persistence | New legacy BIGINT `uploads` table; metadata inserted after object upload; status `UPLOADED`. | Approved plan; DDL/migration source artifact, not applied to live DB. |
| Failure handling | Storage failure → 503; metadata DB failure → rollback, best-effort object delete, 500. | Approved plan; local tests cover both branches. |
| API #47 asset contract | `asset_refs` JSON string containing ordered UploadAsset int64 IDs; `[]` allowed; duplicates rejected; resolve only same Mentor + LECTURE + same course. | Approved plan; reflected in catalog and #47 DD; no #47 route/runtime. |

## Remaining evidence boundary

- Live database schema and migration application are not verified by this source change.
- Real Object Storage credentials, network access, public URL reachability and provider behavior are not exercised by local stub tests.
- API #47 `content:int64` semantics remain unresolved; API #47 stays UNWIRED.
