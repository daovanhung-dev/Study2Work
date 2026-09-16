# Work JSON API

The current React Work API contract is
`contracts/openapi/work/legacy-web.openapi.json`. The older target catalog in
`contracts/openapi/work/openapi.json` is not the current Express route source.

`apps/work-server/src/routes/api_routes.ts` mounts the current API at `/api/v1`.

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
Bearer authentication is stateless and cookie/session authentication is not
supported. The source-aligned contract is `legacy-web.openapi.json`; the larger
`openapi.json` health/domain catalog is not wired to this Express source.
