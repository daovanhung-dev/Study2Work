# Work JSON API

The current React Work API contract is
`contracts/openapi/work/legacy-web.openapi.json`. The older target catalog in
`contracts/openapi/work/openapi.json` is not the current Express route source.

`apps/work-server/src/routes/api_routes.ts` mounts the current API at
`/api/v1`. Public operations are student/business login, student registration,
and job listing/detail. Student and business operations use
`ensureAuthenticated` plus `checkRole` and consume the 11-table Prisma schema.

Successful and handled error responses use the envelope keys
`success`, `businessCode`, `message`, `data`, `meta`, and `traceId`. BigInt and
Date values are normalized before JSON serialization. Bearer authentication is
stateless and cookie/session authentication is not supported.
