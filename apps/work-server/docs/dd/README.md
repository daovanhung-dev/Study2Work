# Work Server API DD

Source-backed API Detail Design for the current Work Server runtime.

## Scope

- 21 wired runtime routes.
- Status: `Draft — Ready for Review`.
- Template: `.agents/skills/create_dd/docs/dd/DD_API_Template_MD`.
- Target-only Work catalog operations are intentionally excluded.

## API folders

- [getWorkApiRoot](./getWorkApiRoot_GET_api_v1/00_Cover.md) — `GET /api/v1`
- [getWorkHealthLive](./getWorkHealthLive_GET_health_live/00_Cover.md) — `GET /health/live`
- [getWorkHealthReady](./getWorkHealthReady_GET_health_ready/00_Cover.md) — `GET /health/ready`
- [loginStudent](./loginStudent_POST_auth_student_login/00_Cover.md) — `POST /api/v1/auth/student/login`
- [loginBusiness](./loginBusiness_POST_auth_business_login/00_Cover.md) — `POST /api/v1/auth/business/login`
- [logout](./logout_POST_auth_logout/00_Cover.md) — `POST /api/v1/auth/logout`
- [registerStudent](./registerStudent_POST_students/00_Cover.md) — `POST /api/v1/students`
- [getMe](./getMe_GET_me/00_Cover.md) — `GET /api/v1/me`
- [listJobs](./listJobs_GET_jobs/00_Cover.md) — `GET /api/v1/jobs`
- [getJob](./getJob_GET_jobs_id/00_Cover.md) — `GET /api/v1/jobs/:id`
- [getMyCv](./getMyCv_GET_students_me_cv/00_Cover.md) — `GET /api/v1/students/me/cv`
- [createCv](./createCv_POST_students_me_cv/00_Cover.md) — `POST /api/v1/students/me/cv`
- [updateCv](./updateCv_PUT_students_me_cv_cvId/00_Cover.md) — `PUT /api/v1/students/me/cv/:cvId`
- [getMyApplications](./getMyApplications_GET_students_me_applications/00_Cover.md) — `GET /api/v1/students/me/applications`
- [applyToJob](./applyToJob_POST_jobs_jobId_applications/00_Cover.md) — `POST /api/v1/jobs/:jobId/applications`
- [getBusinessApplications](./getBusinessApplications_GET_businesses_me_applications/00_Cover.md) — `GET /api/v1/businesses/me/applications`
- [listBusinessJobs](./listBusinessJobs_GET_businesses_me_jobs/00_Cover.md) — `GET /api/v1/businesses/me/jobs`
- [createBusinessJob](./createBusinessJob_POST_businesses_me_jobs/00_Cover.md) — `POST /api/v1/businesses/me/jobs`
- [updateBusinessJob](./updateBusinessJob_PUT_businesses_me_jobs_jobId/00_Cover.md) — `PUT /api/v1/businesses/me/jobs/:jobId`
- [deleteBusinessJob](./deleteBusinessJob_DELETE_businesses_me_jobs_jobId/00_Cover.md) — `DELETE /api/v1/businesses/me/jobs/:jobId`
- [getStudentCv](./getStudentCv_GET_students_studentId_cv/00_Cover.md) — `GET /api/v1/students/:studentId/cv`

## Common contract

- Success: `success=true`, route business code/message/data, `meta`, `traceId`.
- Error: `success=false`, business code/message, `data=null`, `meta`, `traceId`.
- `X-Trace-Id` response header equals body `traceId`.
- BigInt and Date use `jsonSafe`; password/hash fields are never public.

## Naming convention

- API IDs and folder names are compatibility identifiers and intentionally remain aligned with `contracts/openapi/work/legacy-web.openapi.json`.
- The DD `api_name` is the current source runtime handler/use-case.
- Full source mapping for all 21 routes is recorded in `API_CATALOG.md` and each API Cover/Overview.
- Inline system handlers are documented as inline in `createApp` or `createV1Router`; no runtime function is fabricated.
