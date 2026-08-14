# Operations checkpoint

- APIs in checkpoint: 10.
- Status: all DDs remain Draft until missing contract/schema decisions are supplied.
- Source gaps/conflicts: see each Main gap value and root [OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md); no conflict is resolved by this batch.
- Validation: see root [VERIFICATION_REPORT.md](../VERIFICATION_REPORT.md).

| API | Method | Endpoint | Transport | Status | Main gap |
| ---: | --- | --- | --- | --- | --- |
| [API-OPS-001](API-OPS-001_get-api-v1-admin-verification-cases/00_Cover.md) | `GET` | `/api/v1/admin/verification-cases` | `public_http` | `Draft — Needs Confirmation` | OQ-OPS-MISSING-READ-CONTRACTS |
| [API-OPS-002](API-OPS-002_post-api-v1-admin-verification-cases-id-decisions/00_Cover.md) | `POST` | `/api/v1/admin/verification-cases/{id}/decisions` | `public_http` | `Draft — Needs Confirmation` | OQ-OPS-MISSING-READ-CONTRACTS |
| [API-OPS-003](API-OPS-003_get-api-v1-admin-job-reviews/00_Cover.md) | `GET` | `/api/v1/admin/job-reviews` | `public_http` | `Draft — Needs Confirmation` | OQ-OPS-MISSING-READ-CONTRACTS |
| [API-OPS-004](API-OPS-004_post-api-v1-admin-job-reviews-id-decisions/00_Cover.md) | `POST` | `/api/v1/admin/job-reviews/{id}/decisions` | `public_http` | `Draft — Needs Confirmation` | OQ-OPS-MISSING-READ-CONTRACTS |
| [API-OPS-005](API-OPS-005_post-api-v1-admin-trusted-publisher-grants/00_Cover.md) | `POST` | `/api/v1/admin/trusted-publisher-grants` | `public_http` | `Draft — Needs Confirmation` | OQ-OPS-MISSING-READ-CONTRACTS |
| [API-OPS-006](API-OPS-006_post-api-v1-admin-trusted-publisher-grants-id-revoke/00_Cover.md) | `POST` | `/api/v1/admin/trusted-publisher-grants/{id}/revoke` | `public_http` | `Draft — Needs Confirmation` | OQ-OPS-MISSING-READ-CONTRACTS |
| [API-OPS-007](API-OPS-007_get-api-v1-admin-audit-logs/00_Cover.md) | `GET` | `/api/v1/admin/audit-logs` | `public_http` | `Draft — Needs Confirmation` | OQ-OPS-MISSING-READ-CONTRACTS |
| [API-OPS-008](API-OPS-008_post-api-v1-admin-audit-exports/00_Cover.md) | `POST` | `/api/v1/admin/audit-exports` | `public_http` | `Draft — Needs Confirmation` | OQ-OPS-MISSING-READ-CONTRACTS |
| [API-OPS-009](API-OPS-009_post-api-v1-admin-break-glass-sessions/00_Cover.md) | `POST` | `/api/v1/admin/break-glass-sessions` | `public_http` | `Draft — Needs Confirmation` | OQ-OPS-MISSING-READ-CONTRACTS |
| [API-OPS-010](API-OPS-010_get-api-v1-admin-operational-reports/00_Cover.md) | `GET` | `/api/v1/admin/operational-reports` | `public_http` | `Draft — Needs Confirmation` | OQ-OPS-MISSING-READ-CONTRACTS |
