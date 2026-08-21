# University checkpoint

- APIs in checkpoint: 16.
- Status: all DDs remain Draft until missing contract/schema decisions are supplied.
- Source gaps/conflicts: see each Main gap value and root [OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md); no conflict is resolved by this batch.
- Validation: see root [VERIFICATION_REPORT.md](../VERIFICATION_REPORT.md).

| API | Method | Endpoint | Transport | Status | Main gap |
| ---: | --- | --- | --- | --- | --- |
| [API-UNI-001](API-UNI-001_post-api-v1-universities/00_Cover.md) | `POST` | `/api/v1/universities` | `public_http` | `Draft — Needs Confirmation` | OQ-UNI-INCOMPLETE-FLOWS |
| [API-UNI-002](API-UNI-002_post-api-v1-universities-university-id-verification-submissions/00_Cover.md) | `POST` | `/api/v1/universities/{universityId}/verification-submissions` | `public_http` | `Draft — Needs Confirmation` | OQ-UNI-INCOMPLETE-FLOWS |
| [API-UNI-003](API-UNI-003_get-api-v1-universities-university-id-members/00_Cover.md) | `GET` | `/api/v1/universities/{universityId}/members` | `public_http` | `Draft — Needs Confirmation` | OQ-UNI-INCOMPLETE-FLOWS |
| [API-UNI-004](API-UNI-004_post-api-v1-universities-university-id-member-invitations/00_Cover.md) | `POST` | `/api/v1/universities/{universityId}/member-invitations` | `public_http` | `Draft — Needs Confirmation` | OQ-UNI-INCOMPLETE-FLOWS |
| [API-UNI-005](API-UNI-005_post-api-v1-universities-university-id-affiliation-invitations/00_Cover.md) | `POST` | `/api/v1/universities/{universityId}/affiliation-invitations` | `public_http` | `Draft — Needs Confirmation` | OQ-UNI-INCOMPLETE-FLOWS |
| [API-UNI-006](API-UNI-006_post-api-v1-me-university-affiliations-invitation-id-accept/00_Cover.md) | `POST` | `/api/v1/me/university-affiliations/{invitationId}/accept` | `public_http` | `Draft — Needs Confirmation` | OQ-UNI-INCOMPLETE-FLOWS |
| [API-UNI-007](API-UNI-007_delete-api-v1-me-university-affiliations-affiliation-id-consent/00_Cover.md) | `DELETE` | `/api/v1/me/university-affiliations/{affiliationId}/consent` | `public_http` | `Draft — Needs Confirmation` | OQ-UNI-INCOMPLETE-FLOWS |
| [API-UNI-008](API-UNI-008_post-api-v1-universities-university-id-cohorts/00_Cover.md) | `POST` | `/api/v1/universities/{universityId}/cohorts` | `public_http` | `Draft — Needs Confirmation` | OQ-UNI-INCOMPLETE-FLOWS |
| [API-UNI-009](API-UNI-009_put-api-v1-universities-university-id-cohorts-cohort-id-members/00_Cover.md) | `PUT` | `/api/v1/universities/{universityId}/cohorts/{cohortId}/members` | `public_http` | `Draft — Needs Confirmation` | OQ-UNI-INCOMPLETE-FLOWS |
| [API-UNI-010](API-UNI-010_post-api-v1-universities-university-id-internship-programs/00_Cover.md) | `POST` | `/api/v1/universities/{universityId}/internship-programs` | `public_http` | `Draft — Needs Confirmation` | OQ-UNI-INCOMPLETE-FLOWS |
| [API-UNI-011](API-UNI-011_post-api-v1-universities-university-id-campus-job-distributions/00_Cover.md) | `POST` | `/api/v1/universities/{universityId}/campus-job-distributions` | `public_http` | `Draft — Needs Confirmation` | OQ-UNI-INCOMPLETE-FLOWS |
| [API-UNI-012](API-UNI-012_post-api-v1-universities-university-id-partnerships/00_Cover.md) | `POST` | `/api/v1/universities/{universityId}/partnerships` | `public_http` | `Draft — Needs Confirmation` | OQ-UNI-INCOMPLETE-FLOWS |
| [API-UNI-013](API-UNI-013_post-api-v1-enterprises-enterprise-id-university-partnerships-id-respond/00_Cover.md) | `POST` | `/api/v1/enterprises/{enterpriseId}/university-partnerships/{id}/respond` | `public_http` | `Draft — Needs Confirmation` | OQ-UNI-INCOMPLETE-FLOWS |
| [API-UNI-014](API-UNI-014_post-api-v1-universities-university-id-referrals/00_Cover.md) | `POST` | `/api/v1/universities/{universityId}/referrals` | `public_http` | `Draft — Needs Confirmation` | OQ-UNI-INCOMPLETE-FLOWS |
| [API-UNI-015](API-UNI-015_get-api-v1-universities-university-id-reports-outcomes/00_Cover.md) | `GET` | `/api/v1/universities/{universityId}/reports/outcomes` | `public_http` | `Draft — Needs Confirmation` | OQ-UNI-INCOMPLETE-FLOWS |
| [API-UNI-016](API-UNI-016_get-api-v1-universities-university-id-affiliations-id/00_Cover.md) | `GET` | `/api/v1/universities/{universityId}/affiliations/{id}` | `public_http` | `Draft — Needs Confirmation` | OQ-UNI-INCOMPLETE-FLOWS |
