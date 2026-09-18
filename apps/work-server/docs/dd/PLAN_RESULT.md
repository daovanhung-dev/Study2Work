# PLAN_RESULT

## Scope

- Current registered Work Server routes only: 18 operations.
- Basis: `DIRECT — current registered route`.
- Target-only `openapi.json` routes and unwired services are excluded.

## API inventory

| No | API ID | Method | Endpoint | Output folder | Tables read | Tables write | Status |
|---|---|---|---|---|---|---|---|
| 1 | `loginStudent` | `POST` | `/api/v1/auth/student/login` | `loginStudent_POST_auth_student_login` | `SinhVien` | N/A | Draft — Needs Confirmation |
| 2 | `loginBusiness` | `POST` | `/api/v1/auth/business/login` | `loginBusiness_POST_auth_business_login` | `DoanhNghiep` | N/A | Draft — Needs Confirmation |
| 3 | `logout` | `POST` | `/api/v1/auth/logout` | `logout_POST_auth_logout` | N/A | N/A | Draft — Needs Confirmation |
| 4 | `registerStudent` | `POST` | `/api/v1/students` | `registerStudent_POST_students` | `SinhVien` | `SinhVien` | Draft — Needs Confirmation |
| 5 | `listJobs` | `GET` | `/api/v1/jobs` | `listJobs_GET_jobs` | `JD` | N/A | Draft — Needs Confirmation |
| 6 | `getJob` | `GET` | `/api/v1/jobs/:id` | `getJob_GET_jobs_id` | `JD` | N/A | Draft — Needs Confirmation |
| 7 | `getMe` | `GET` | `/api/v1/me` | `getMe_GET_me` | `SinhVien`, `DoanhNghiep` | N/A | Draft — Needs Confirmation |
| 8 | `getMyCv` | `GET` | `/api/v1/students/me/cv` | `getMyCv_GET_students_me_cv` | `Cv` | N/A | Draft — Needs Confirmation |
| 9 | `createCv` | `POST` | `/api/v1/students/me/cv` | `createCv_POST_students_me_cv` | `Cv` | `Cv` | Draft — Needs Confirmation |
| 10 | `updateCv` | `PUT` | `/api/v1/students/me/cv/:cvId` | `updateCv_PUT_students_me_cv_cvId` | `Cv` | `Cv` | Draft — Needs Confirmation |
| 11 | `getMyApplications` | `GET` | `/api/v1/students/me/applications` | `getMyApplications_GET_students_me_applications` | `UngVien`, `JD`, `DoanhNghiep` | N/A | Draft — Needs Confirmation |
| 12 | `applyToJob` | `POST` | `/api/v1/jobs/:jobId/applications` | `applyToJob_POST_jobs_jobId_applications` | `JD`, `UngVien` | `UngVien` | Draft — Needs Confirmation |
| 13 | `listBusinessJobs` | `GET` | `/api/v1/businesses/me/jobs` | `listBusinessJobs_GET_businesses_me_jobs` | `JD` | N/A | Draft — Needs Confirmation |
| 14 | `createBusinessJob` | `POST` | `/api/v1/businesses/me/jobs` | `createBusinessJob_POST_businesses_me_jobs` | `JD`, `DoanhNghiep` | `JD` | Draft — Needs Confirmation |
| 15 | `updateBusinessJob` | `PUT` | `/api/v1/businesses/me/jobs/:jobId` | `updateBusinessJob_PUT_businesses_me_jobs_jobId` | `JD` | `JD` | Draft — Needs Confirmation |
| 16 | `deleteBusinessJob` | `DELETE` | `/api/v1/businesses/me/jobs/:jobId` | `deleteBusinessJob_DELETE_businesses_me_jobs_jobId` | `JD` | `JD` | Draft — Needs Confirmation |
| 17 | `getBusinessApplications` | `GET` | `/api/v1/businesses/me/applications` | `getBusinessApplications_GET_businesses_me_applications` | `UngVien`, `SinhVien`, `JD` | N/A | Draft — Needs Confirmation |
| 18 | `getStudentCv` | `GET` | `/api/v1/students/:studentId/cv` | `getStudentCv_GET_students_studentId_cv` | `Cv` | N/A | Draft — Needs Confirmation |

## Sources and gaps

- Route/service/schema sources were read for every operation.
- `apps/work-server` has no checked-in server integration test suite; runtime test status remains source-level only.
- Passwords are hashed with bcrypt for new writes; public Prisma projections exclude password/hash fields.
- Legacy plaintext rows remain compatibility-readable and are opportunistically rehashed after successful login.
- Runtime secrets are environment-backed; no literal database/JWT credential is included in source-backed DD.
