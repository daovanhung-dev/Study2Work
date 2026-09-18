# SOURCE_READ_REPORT

## Input and source coverage

- Source of truth for runtime behavior: current Work Server TypeScript and Prisma schema.
- Template source: `.agents/skills/create_dd/docs/dd/DD_API_Template_MD`.
- Legacy compatibility boundary: `contracts/openapi/work/legacy-web.openapi.json`.
- Target catalog was inspected only to exclude unwired operations.

| No | Source | Status |
| ---: | --- | --- |
| 1 | `.agents/skills/create_dd/docs/dd/DD_API_Template_MD` | READ — used as source or boundary reference |
| 2 | [apps/work-server/prisma/schema.prisma](../../prisma/schema.prisma) | READ — used as source or boundary reference |
| 3 | [apps/work-server/src/api/v1.ts](../../src/api/v1.ts) | READ — used as source or boundary reference |
| 4 | [apps/work-server/src/app.ts](../../src/app.ts) | READ — used as source or boundary reference |
| 5 | [apps/work-server/src/config/multer.ts](../../src/config/multer.ts) | READ — used as source or boundary reference |
| 6 | [apps/work-server/src/core/config.ts](../../src/core/config.ts) | READ — used as source or boundary reference |
| 7 | [apps/work-server/src/core/database.ts](../../src/core/database.ts) | READ — used as source or boundary reference |
| 8 | [apps/work-server/src/core/exceptions.ts](../../src/core/exceptions.ts) | READ — used as source or boundary reference |
| 9 | [apps/work-server/src/core/middleware.ts](../../src/core/middleware.ts) | READ — used as source or boundary reference |
| 10 | [apps/work-server/src/core/responses.ts](../../src/core/responses.ts) | READ — used as source or boundary reference |
| 11 | [apps/work-server/src/core/security/access-token.ts](../../src/core/security/access-token.ts) | READ — used as source or boundary reference |
| 12 | [apps/work-server/src/core/security/password.ts](../../src/core/security/password.ts) | READ — used as source or boundary reference |
| 13 | [apps/work-server/src/middleware/auth.middleware.ts](../../src/middleware/auth.middleware.ts) | READ — used as source or boundary reference |
| 14 | [apps/work-server/src/modules/applications/models.ts](../../src/modules/applications/models.ts) | READ — used as source or boundary reference |
| 15 | [apps/work-server/src/modules/applications/query.ts](../../src/modules/applications/query.ts) | READ — used as source or boundary reference |
| 16 | [apps/work-server/src/modules/applications/routes.ts](../../src/modules/applications/routes.ts) | READ — used as source or boundary reference |
| 17 | [apps/work-server/src/modules/applications/validate.ts](../../src/modules/applications/validate.ts) | READ — used as source or boundary reference |
| 18 | [apps/work-server/src/modules/applications/view.ts](../../src/modules/applications/view.ts) | READ — used as source or boundary reference |
| 19 | [apps/work-server/src/modules/auth/models.ts](../../src/modules/auth/models.ts) | READ — used as source or boundary reference |
| 20 | [apps/work-server/src/modules/auth/query.ts](../../src/modules/auth/query.ts) | READ — used as source or boundary reference |
| 21 | [apps/work-server/src/modules/auth/routes.ts](../../src/modules/auth/routes.ts) | READ — used as source or boundary reference |
| 22 | [apps/work-server/src/modules/auth/validate.ts](../../src/modules/auth/validate.ts) | READ — used as source or boundary reference |
| 23 | [apps/work-server/src/modules/auth/view.ts](../../src/modules/auth/view.ts) | READ — used as source or boundary reference |
| 24 | [apps/work-server/src/modules/businesses/query.ts](../../src/modules/businesses/query.ts) | READ — used as source or boundary reference |
| 25 | [apps/work-server/src/modules/businesses/view.ts](../../src/modules/businesses/view.ts) | READ — used as source or boundary reference |
| 26 | [apps/work-server/src/modules/cv/models.ts](../../src/modules/cv/models.ts) | READ — used as source or boundary reference |
| 27 | [apps/work-server/src/modules/cv/query.ts](../../src/modules/cv/query.ts) | READ — used as source or boundary reference |
| 28 | [apps/work-server/src/modules/cv/routes.ts](../../src/modules/cv/routes.ts) | READ — used as source or boundary reference |
| 29 | [apps/work-server/src/modules/cv/validate.ts](../../src/modules/cv/validate.ts) | READ — used as source or boundary reference |
| 30 | [apps/work-server/src/modules/cv/view.ts](../../src/modules/cv/view.ts) | READ — used as source or boundary reference |
| 31 | [apps/work-server/src/modules/jobs/models.ts](../../src/modules/jobs/models.ts) | READ — used as source or boundary reference |
| 32 | [apps/work-server/src/modules/jobs/query.ts](../../src/modules/jobs/query.ts) | READ — used as source or boundary reference |
| 33 | [apps/work-server/src/modules/jobs/routes.ts](../../src/modules/jobs/routes.ts) | READ — used as source or boundary reference |
| 34 | [apps/work-server/src/modules/jobs/validate.ts](../../src/modules/jobs/validate.ts) | READ — used as source or boundary reference |
| 35 | [apps/work-server/src/modules/jobs/view.ts](../../src/modules/jobs/view.ts) | READ — used as source or boundary reference |
| 36 | [apps/work-server/src/modules/students/models.ts](../../src/modules/students/models.ts) | READ — used as source or boundary reference |
| 37 | [apps/work-server/src/modules/students/query.ts](../../src/modules/students/query.ts) | READ — used as source or boundary reference |
| 38 | [apps/work-server/src/modules/students/routes.ts](../../src/modules/students/routes.ts) | READ — used as source or boundary reference |
| 39 | [apps/work-server/src/modules/students/validate.ts](../../src/modules/students/validate.ts) | READ — used as source or boundary reference |
| 40 | [apps/work-server/src/modules/students/view.ts](../../src/modules/students/view.ts) | READ — used as source or boundary reference |
| 41 | [apps/work-server/src/services/public-selectors.ts](../../src/services/public-selectors.ts) | READ — used as source or boundary reference |
| 42 | `contracts/openapi/work/legacy-web.openapi.json` | READ — used as source or boundary reference |
| 43 | `contracts/openapi/work/openapi.json` | READ — used as source or boundary reference |

## Preserved discrepancies

- Login accepts canonical `password` and legacy `matkhau` alias.
- Legacy plaintext password fallback remains until successful login rehash.
- Target OpenAPI contains unwired domains excluded from this runtime DD.

## Runtime naming reconciliation

| API ID | Source runtime handler/use-case |
| --- | --- |
| `getWorkApiRoot` | Inline handler in createV1Router — GET / |
| `getWorkHealthLive` | Inline handler in createApp — GET /health/live |
| `getWorkHealthReady` | Inline handler in createApp — GET /health/ready |
| `loginStudent` | auth.view.loginStudent |
| `loginBusiness` | auth.view.loginBusiness |
| `logout` | auth.view.logout |
| `registerStudent` | students.view.registerStudent |
| `getMe` | api/v1 dispatcher → students.view.getStudentMe or businesses.view.getBusinessMe |
| `listJobs` | jobs.view.getJobs; query: jobs.query.listJobs |
| `getJob` | jobs.view.getJob |
| `getMyCv` | cv.view.getMyCv |
| `createCv` | cv.view.createCv |
| `updateCv` | cv.view.updateCv |
| `getMyApplications` | applications.view.getStudentApplications |
| `applyToJob` | applications.view.applyToJob |
| `getBusinessApplications` | applications.view.getBusinessApplications |
| `listBusinessJobs` | jobs.view.getBusinessJobs |
| `createBusinessJob` | jobs.view.createBusinessJob |
| `updateBusinessJob` | jobs.view.updateBusinessJob |
| `deleteBusinessJob` | jobs.view.deleteBusinessJob |
| `getStudentCv` | cv.view.getStudentCv |
