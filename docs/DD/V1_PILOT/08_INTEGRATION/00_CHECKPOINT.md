# Integration and Realtime checkpoint

- APIs in checkpoint: 11.
- Status: all DDs remain Draft until missing contract/schema decisions are supplied.
- Source gaps/conflicts: see each Main gap value and root [OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md); no conflict is resolved by this batch.
- Validation: see root [VERIFICATION_REPORT.md](../VERIFICATION_REPORT.md).

| API | Method | Endpoint | Transport | Status | Main gap |
| ---: | --- | --- | --- | --- | --- |
| [API-INT-001](API-INT-001_get-identity-internal-v1-users-platform-user-id-projection/00_Cover.md) | `GET` | `/internal/v1/users/{platformUserId}/projection` | `internal_http` | `Draft — Needs Confirmation` | OQ-IAM-AUTHVERSION |
| [API-INT-002](API-INT-002_post-study-internal-v1-evidence-export-requests/00_Cover.md) | `POST` | `/internal/v1/evidence-export-requests` | `internal_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-INT-003](API-INT-003_get-study-internal-v1-evidence-export-requests-request-id/00_Cover.md) | `GET` | `/internal/v1/evidence-export-requests/{requestId}` | `internal_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-INT-004](API-INT-004_post-work-internal-v1-evidence-export-results/00_Cover.md) | `POST` | `/internal/v1/evidence-export-results` | `internal_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-INT-005](API-INT-005_post-work-internal-v1-evidence-revocations/00_Cover.md) | `POST` | `/internal/v1/evidence-revocations` | `internal_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-INT-006](API-INT-006_post-work-internal-v1-identity-events/00_Cover.md) | `POST` | `/internal/v1/identity-events` | `internal_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-INT-007](API-INT-007_post-study-internal-v1-identity-events/00_Cover.md) | `POST` | `/internal/v1/identity-events` | `internal_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-INT-008](API-INT-008_post-work-internal-v1-ai-provider-callbacks-provider/00_Cover.md) | `POST` | `/internal/v1/ai-provider-callbacks/{provider}` | `internal_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-INT-009](API-INT-009_post-study-internal-v1-progress-rebuild-jobs/00_Cover.md) | `POST` | `/internal/v1/progress-rebuild-jobs` | `internal_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-INT-010](API-INT-010_post-work-internal-v1-search-index-removals/00_Cover.md) | `POST` | `/internal/v1/search-index-removals` | `internal_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-INT-011](API-INT-011_get-wss-work-api-study2work-vn-api-v1-realtime/00_Cover.md) | `GET` | `wss://work-api.study2work.vn/api/v1/realtime` | `websocket` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
