# BUSINESS_CODE_DELTA

All codes below are present in current runtime source; generic Prisma codes are centralized fallbacks.

| Business code | HTTP | Meaning | Evidence source |
| ---: | --- | --- | --- |
| SYSTEM_ROOT_LOADED | 200 | Work API root metadata loaded | src/api/v1.ts |
| SYSTEM_HEALTH_LIVE | 200 | Work API process is live | src/app.ts |
| SYSTEM_HEALTH_READY | 200 | Prisma readiness probe succeeded | src/app.ts |
| DEPENDENCY_UNAVAILABLE | 503 | Prisma readiness probe failed | src/app.ts |
| AUTH_LOGIN_SUCCESS | 200 | Login succeeded | src/modules/auth/view.ts |
| AUTH_LOGOUT_SUCCESS | 200 | Stateless logout response | src/modules/auth/view.ts |
| INVALID_REQUEST | 400 | Validation or business precondition failed | src/core/exceptions.ts and module validate.ts |
| INVALID_CREDENTIALS | 401 | Credential mismatch | src/modules/auth/view.ts |
| UNAUTHORIZED | 401 | Bearer authentication required/invalid | src/middleware/auth.middleware.ts |
| FORBIDDEN | 403 | Authenticated role is not allowed | src/middleware/auth.middleware.ts |
| STUDENT_CREATED | 201 | Student created | src/modules/students/view.ts |
| STUDENT_CREATE_FAILED | 409 | Student email already exists | src/modules/students/view.ts |
| JOBS_LOADED | 200 | Public jobs loaded | src/modules/jobs/view.ts |
| JOB_LOADED | 200 | Job loaded | src/modules/jobs/view.ts |
| JOB_NOT_FOUND | 404 | Job missing or not owned | src/modules/jobs/view.ts |
| ME_LOADED | 200 | Current user loaded | src/api/v1.ts and module views |
| USER_NOT_FOUND | 404 | Account missing | src/modules/students/view.ts and businesses/view.ts |
| CV_LOADED | 200 | CV loaded | src/modules/cv/view.ts |
| CV_CREATED | 201 | CV created | src/modules/cv/view.ts |
| CV_UPDATED | 200 | CV updated | src/modules/cv/view.ts |
| CV_NOT_FOUND | 404 | CV missing | src/modules/cv/view.ts |
| CV_ALREADY_EXISTS | 409 | Student already has a CV | src/modules/cv/view.ts |
| APPLICATIONS_LOADED | 200 | Student applications loaded | src/modules/applications/view.ts |
| APPLICATION_CREATED | 201 | Application created | src/modules/applications/view.ts |
| APPLICATION_ALREADY_EXISTS | 409 | Duplicate application | src/modules/applications/view.ts |
| BUSINESS_JOBS_LOADED | 200 | Business jobs loaded | src/modules/jobs/view.ts |
| JOB_CREATED | 201 | Business job created | src/modules/jobs/view.ts |
| JOB_UPDATED | 200 | Business job updated | src/modules/jobs/view.ts |
| JOB_DELETED | 200 | Business job deleted | src/modules/jobs/view.ts |
| BUSINESS_APPLICATIONS_LOADED | 200 | Business applications loaded | src/modules/applications/view.ts |
| PAYLOAD_TOO_LARGE | 413 | Multipart file exceeds 10 MiB | src/core/exceptions.ts and src/config/multer.ts |
| NOT_FOUND | 404 | Unknown resource route | src/app.ts |
| RESOURCE_CONFLICT | 409 | Unhandled generic Prisma unique conflict | src/core/exceptions.ts |
| RESOURCE_NOT_FOUND | 404 | Unhandled generic Prisma missing record | src/core/exceptions.ts |
| INTERNAL_SERVER_ERROR | 500 | Safe generic server error | src/core/exceptions.ts |

## Naming note

Business codes remain mapped to the same contract IDs and runtime behavior. This DD pass changes only API display/source-name metadata; it does not add, remove or rename a business code.
