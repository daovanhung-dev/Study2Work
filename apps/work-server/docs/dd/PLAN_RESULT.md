# PLAN_RESULT

## Scope

- 21 current runtime operations: 18 Work Web compatibility routes plus 3 system routes.
- Target-only operations from `contracts/openapi/work/openapi.json` are excluded.

## API inventory

| No | API ID | Method | Endpoint | Output folder | Source runtime handler/use-case | Tables read | Tables write | Basis | Status |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `getWorkApiRoot` | GET | /api/v1 | `getWorkApiRoot_GET_api_v1` | Inline handler in createV1Router — GET / | N/A | N/A | DIRECT — current registered route | Draft — Ready for Review |
| 2 | `getWorkHealthLive` | GET | /health/live | `getWorkHealthLive_GET_health_live` | Inline handler in createApp — GET /health/live | N/A | N/A | DIRECT — current registered route | Draft — Ready for Review |
| 3 | `getWorkHealthReady` | GET | /health/ready | `getWorkHealthReady_GET_health_ready` | Inline handler in createApp — GET /health/ready | Prisma dependency probe (SELECT 1) | N/A | DIRECT — current registered route | Draft — Ready for Review |
| 4 | `loginStudent` | POST | /api/v1/auth/student/login | `loginStudent_POST_auth_student_login` | auth.view.loginStudent | SinhVien | SinhVien | DIRECT — current registered route | Draft — Ready for Review |
| 5 | `loginBusiness` | POST | /api/v1/auth/business/login | `loginBusiness_POST_auth_business_login` | auth.view.loginBusiness | DoanhNghiep | DoanhNghiep | DIRECT — current registered route | Draft — Ready for Review |
| 6 | `logout` | POST | /api/v1/auth/logout | `logout_POST_auth_logout` | auth.view.logout | N/A | N/A | DIRECT — current registered route | Draft — Ready for Review |
| 7 | `registerStudent` | POST | /api/v1/students | `registerStudent_POST_students` | students.view.registerStudent | N/A | SinhVien | DIRECT — current registered route | Draft — Ready for Review |
| 8 | `getMe` | GET | /api/v1/me | `getMe_GET_me` | api/v1 dispatcher → students.view.getStudentMe or businesses.view.getBusinessMe | SinhVien, DoanhNghiep | N/A | DIRECT — current registered route | Draft — Ready for Review |
| 9 | `listJobs` | GET | /api/v1/jobs | `listJobs_GET_jobs` | jobs.view.getJobs; query: jobs.query.listJobs | JD | N/A | DIRECT — current registered route | Draft — Ready for Review |
| 10 | `getJob` | GET | /api/v1/jobs/:id | `getJob_GET_jobs_id` | jobs.view.getJob | JD | N/A | DIRECT — current registered route | Draft — Ready for Review |
| 11 | `getMyCv` | GET | /api/v1/students/me/cv | `getMyCv_GET_students_me_cv` | cv.view.getMyCv | Cv | N/A | DIRECT — current registered route | Draft — Ready for Review |
| 12 | `createCv` | POST | /api/v1/students/me/cv | `createCv_POST_students_me_cv` | cv.view.createCv | Cv | Cv | DIRECT — current registered route | Draft — Ready for Review |
| 13 | `updateCv` | PUT | /api/v1/students/me/cv/:cvId | `updateCv_PUT_students_me_cv_cvId` | cv.view.updateCv | Cv | Cv | DIRECT — current registered route | Draft — Ready for Review |
| 14 | `getMyApplications` | GET | /api/v1/students/me/applications | `getMyApplications_GET_students_me_applications` | applications.view.getStudentApplications | UngVien, JD, DoanhNghiep | N/A | DIRECT — current registered route | Draft — Ready for Review |
| 15 | `applyToJob` | POST | /api/v1/jobs/:jobId/applications | `applyToJob_POST_jobs_jobId_applications` | applications.view.applyToJob | JD, UngVien | UngVien | DIRECT — current registered route | Draft — Ready for Review |
| 16 | `getBusinessApplications` | GET | /api/v1/businesses/me/applications | `getBusinessApplications_GET_businesses_me_applications` | applications.view.getBusinessApplications | UngVien, SinhVien, JD | N/A | DIRECT — current registered route | Draft — Ready for Review |
| 17 | `listBusinessJobs` | GET | /api/v1/businesses/me/jobs | `listBusinessJobs_GET_businesses_me_jobs` | jobs.view.getBusinessJobs | JD | N/A | DIRECT — current registered route | Draft — Ready for Review |
| 18 | `createBusinessJob` | POST | /api/v1/businesses/me/jobs | `createBusinessJob_POST_businesses_me_jobs` | jobs.view.createBusinessJob | DoanhNghiep | JD | DIRECT — current registered route | Draft — Ready for Review |
| 19 | `updateBusinessJob` | PUT | /api/v1/businesses/me/jobs/:jobId | `updateBusinessJob_PUT_businesses_me_jobs_jobId` | jobs.view.updateBusinessJob | JD | JD | DIRECT — current registered route | Draft — Ready for Review |
| 20 | `deleteBusinessJob` | DELETE | /api/v1/businesses/me/jobs/:jobId | `deleteBusinessJob_DELETE_businesses_me_jobs_jobId` | jobs.view.deleteBusinessJob | JD | JD | DIRECT — current registered route | Draft — Ready for Review |
| 21 | `getStudentCv` | GET | /api/v1/students/:studentId/cv | `getStudentCv_GET_students_studentId_cv` | cv.view.getStudentCv | Cv | N/A | DIRECT — current registered route | Draft — Ready for Review |

## Source-backed decisions

- Current runtime source is authoritative for route, field, validation, business code, transaction and response behavior.
- Legacy plaintext login fallback and best-effort bcrypt rehash are documented as current compatibility behavior.
- Public projections exclude password/hash fields.

## Naming reconciliation

- `dd_id`, output folder and legacy compatibility operation ID remain unchanged.
- `api_name` and the Cover/Overview source field now use the current runtime handler or use-case.
- Inline system routes are identified by their owning `createApp` or `createV1Router` handler; no function name is invented.
