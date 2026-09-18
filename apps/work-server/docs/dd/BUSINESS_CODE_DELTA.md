# BUSINESS_CODE_DELTA

| Business code | HTTP status | Meaning | Evidence status |
|---|---:|---|---|
| `AUTH_LOGIN_SUCCESS` | `200` | Login success | Source-confirmed |
| `AUTH_LOGOUT_SUCCESS` | `200` | Logout success | Source-confirmed |
| `INVALID_REQUEST` | `400` | Missing/invalid request or business precondition | Source-confirmed |
| `INVALID_CREDENTIALS` | `401` | Login credential mismatch | Source-confirmed |
| `UNAUTHORIZED` | `401` | Missing/invalid Bearer token | Source-confirmed |
| `FORBIDDEN` | `403` | Authenticated user has wrong role | Source-confirmed |
| `STUDENT_CREATED` | `201` | Student registration success | Source-confirmed |
| `STUDENT_CREATE_FAILED` | `409` | Student email already exists | Source-confirmed |
| `JOBS_LOADED` | `200` | Public job list loaded | Source-confirmed |
| `JOB_LOADED` | `200` | Job detail loaded | Source-confirmed |
| `JOB_NOT_FOUND` | `404` | JD not found or not owned | Source-confirmed |
| `ME_LOADED` | `200` | Current user loaded | Source-confirmed |
| `USER_NOT_FOUND` | `404` | Current user not found | Source-confirmed |
| `CV_LOADED` | `200` | CV loaded | Source-confirmed |
| `CV_CREATED` | `201` | CV created | Source-confirmed |
| `CV_UPDATED` | `200` | CV updated | Source-confirmed |
| `CV_NOT_FOUND` | `404` | CV not found | Source-confirmed |
| `CV_ALREADY_EXISTS` | `409` | Student already has a CV | Source-confirmed |
| `APPLICATIONS_LOADED` | `200` | Student applications loaded | Source-confirmed |
| `APPLICATION_CREATED` | `201` | Application created | Source-confirmed |
| `APPLICATION_ALREADY_EXISTS` | `409` | Duplicate application | Source-confirmed |
| `BUSINESS_JOBS_LOADED` | `200` | Business jobs loaded | Source-confirmed |
| `JOB_CREATED` | `201` | Business job created | Source-confirmed |
| `JOB_UPDATED` | `200` | Business job updated | Source-confirmed |
| `JOB_DELETED` | `200` | Business job deleted | Source-confirmed |
| `BUSINESS_APPLICATIONS_LOADED` | `200` | Business applications loaded | Source-confirmed |
| `PAYLOAD_TOO_LARGE` | `413` | Multipart file exceeds 10 MiB limit | Source-confirmed |
| `INTERNAL_SERVER_ERROR` | `500` | Safe generic server error envelope | Source-confirmed |
