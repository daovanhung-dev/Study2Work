# Platform Identity checkpoint

- APIs in checkpoint: 25.
- Status: all DDs remain Draft until missing contract/schema decisions are supplied.
- Source gaps/conflicts: see each Main gap value and root [OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md); no conflict is resolved by this batch.
- Validation: see root [VERIFICATION_REPORT.md](../VERIFICATION_REPORT.md).

| API | Method | Endpoint | Transport | Status | Main gap |
| ---: | --- | --- | --- | --- | --- |
| [API-IAM-001](API-IAM-001_post-api-v1-auth-register/00_Cover.md) | `POST` | `/api/v1/auth/register` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-IAM-002](API-IAM-002_post-api-v1-auth-verify-email/00_Cover.md) | `POST` | `/api/v1/auth/verify-email` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-IAM-003](API-IAM-003_post-api-v1-auth-resend-verification/00_Cover.md) | `POST` | `/api/v1/auth/resend-verification` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-IAM-004](API-IAM-004_post-api-v1-auth-login/00_Cover.md) | `POST` | `/api/v1/auth/login` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-IAM-005](API-IAM-005_post-api-v1-auth-mfa-challenges-challenge-id-verify/00_Cover.md) | `POST` | `/api/v1/auth/mfa/challenges/{challengeId}/verify` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-IAM-006](API-IAM-006_post-api-v1-auth-refresh/00_Cover.md) | `POST` | `/api/v1/auth/refresh` | `public_http` | `Draft — Needs Confirmation` | OQ-IAM-AUTHVERSION |
| [API-IAM-007](API-IAM-007_post-api-v1-auth-logout/00_Cover.md) | `POST` | `/api/v1/auth/logout` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-IAM-008](API-IAM-008_post-api-v1-auth-logout-all/00_Cover.md) | `POST` | `/api/v1/auth/logout-all` | `public_http` | `Draft — Needs Confirmation` | OQ-IAM-AUTHVERSION |
| [API-IAM-009](API-IAM-009_post-api-v1-auth-forgot-password/00_Cover.md) | `POST` | `/api/v1/auth/forgot-password` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-IAM-010](API-IAM-010_post-api-v1-auth-reset-password/00_Cover.md) | `POST` | `/api/v1/auth/reset-password` | `public_http` | `Draft — Needs Confirmation` | OQ-IAM-AUTHVERSION |
| [API-IAM-011](API-IAM-011_get-api-v1-me/00_Cover.md) | `GET` | `/api/v1/me` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-IAM-012](API-IAM-012_put-api-v1-me-password/00_Cover.md) | `PUT` | `/api/v1/me/password` | `public_http` | `Draft — Needs Confirmation` | OQ-IAM-AUTHVERSION |
| [API-IAM-013](API-IAM-013_post-api-v1-me-email-change-requests/00_Cover.md) | `POST` | `/api/v1/me/email-change-requests` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-IAM-014](API-IAM-014_post-api-v1-me-email-changes/00_Cover.md) | `POST` | `/api/v1/me/email-changes` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-IAM-015](API-IAM-015_get-api-v1-me-sessions/00_Cover.md) | `GET` | `/api/v1/me/sessions` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-IAM-016](API-IAM-016_delete-api-v1-me-sessions-session-id/00_Cover.md) | `DELETE` | `/api/v1/me/sessions/{sessionId}` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-IAM-017](API-IAM-017_post-api-v1-me-mfa-enrollments/00_Cover.md) | `POST` | `/api/v1/me/mfa/enrollments` | `public_http` | `Draft — Needs Confirmation` | OQ-IAM-MFA-ENROLLMENT |
| [API-IAM-018](API-IAM-018_post-api-v1-me-mfa-enrollments-id-confirm/00_Cover.md) | `POST` | `/api/v1/me/mfa/enrollments/{id}/confirm` | `public_http` | `Draft — Needs Confirmation` | OQ-IAM-MFA-ENROLLMENT |
| [API-IAM-019](API-IAM-019_post-api-v1-me-deletion-requests/00_Cover.md) | `POST` | `/api/v1/me/deletion-requests` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-IAM-020](API-IAM-020_delete-api-v1-me-deletion-request/00_Cover.md) | `DELETE` | `/api/v1/me/deletion-request` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-IAM-021](API-IAM-021_get-api-v1-admin-users/00_Cover.md) | `GET` | `/api/v1/admin/users` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-IAM-022](API-IAM-022_put-api-v1-admin-users-user-id-status/00_Cover.md) | `PUT` | `/api/v1/admin/users/{userId}/status` | `public_http` | `Draft — Needs Confirmation` | OQ-IAM-AUTHVERSION |
| [API-IAM-023](API-IAM-023_put-api-v1-admin-users-user-id-global-roles/00_Cover.md) | `PUT` | `/api/v1/admin/users/{userId}/global-roles` | `public_http` | `Draft — Needs Confirmation` | OQ-IAM-AUTHVERSION |
| [API-IAM-024](API-IAM-024_get-well-known-jwks-json/00_Cover.md) | `GET` | `/.well-known/jwks.json` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-IAM-025](API-IAM-025_post-api-v1-auth-token-exchanges/00_Cover.md) | `POST` | `/api/v1/auth/token-exchanges` | `public_http` | `Draft — Needs Confirmation` | OQ-IAM-AUTHVERSION |
