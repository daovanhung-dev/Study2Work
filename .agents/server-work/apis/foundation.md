# Work JSON API

The compatibility React Work API contract is
`contracts/openapi/work/legacy-web.openapi.json`. The system-route subset of the
target catalog is also now wired from `contracts/openapi/work/openapi.json`.

`apps/work-server/src/api/v1.ts` mounts the current API at `/api/v1`;
`src/routes/api_routes.ts` remains a compatibility re-export.

System routes are:

- `GET /api/v1` → `SYSTEM_ROOT_LOADED`
- `GET /health/live` → `SYSTEM_HEALTH_LIVE`
- `GET /health/ready` → `SYSTEM_HEALTH_READY`, or `503 DEPENDENCY_UNAVAILABLE`

Unauthenticated routes are:

- `POST /auth/student/login`
- `POST /auth/business/login`
- `POST /students` (multipart registration with optional image)
- `GET /jobs` and `GET /jobs/:id`

`POST /auth/logout` is Bearer-protected. After the router-level
`ensureAuthenticated` boundary:

- `GET /me`
- Student: `GET/POST /students/me/cv`, `PUT /students/me/cv/:cvId`,
  `GET /students/me/applications`, `POST /jobs/:jobId/applications`
- Business: `GET/POST /businesses/me/jobs`, `PUT/DELETE /businesses/me/jobs/:jobId`,
  `GET /businesses/me/applications`, `GET /students/:studentId/cv`

There is no business registration route and no current API route for chat,
notifications, interviews, university, TopCV/TopJD or Admin. Role-specific
student and business operations use `checkRole` and the 12-model Prisma schema.

Successful and handled error responses use the envelope keys
`success`, `businessCode`, `message`, `data`, `meta`, and `traceId`. BigInt and
Date values are normalized before JSON serialization; error data is `null`.
The response also carries the same trace identifier in `X-Trace-Id`. Invalid
IDs, email/password input, dates, empty partial updates, pagination and upload
constraints are rejected as JSON `400`; upload files over 10 MiB are `413`.
Images must use the configured JPEG/PNG/GIF extension and MIME allowlist.
Public response projections exclude `matkhau` and password hashes.
Bearer authentication is stateless and cookie/session authentication is not
supported. The legacy route surface remains source-aligned to
`legacy-web.openapi.json`; only the root/live/ready system subset of the larger
`openapi.json` catalog is wired. Target tenant, billing, university, interview,
storage and webhook domains remain unwired.
