# AI checkpoint

- APIs in checkpoint: 10.
- Status: all DDs remain Draft until missing contract/schema decisions are supplied.
- Source gaps/conflicts: see each Main gap value and root [OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md); no conflict is resolved by this batch.
- Validation: see root [VERIFICATION_REPORT.md](../VERIFICATION_REPORT.md).

| API | Method | Endpoint | Transport | Status | Main gap |
| ---: | --- | --- | --- | --- | --- |
| [API-AIX-001](API-AIX-001_post-api-v1-me-cvs-cv-id-ai-writing-jobs/00_Cover.md) | `POST` | `/api/v1/me/cvs/{cvId}/ai-writing-jobs` | `public_http` | `Draft — Needs Confirmation` | OQ-AIX-EVALUATION-KILL-SWITCH |
| [API-AIX-002](API-AIX-002_post-api-v1-enterprises-enterprise-id-jobs-job-id-ai-jd-jobs/00_Cover.md) | `POST` | `/api/v1/enterprises/{enterpriseId}/jobs/{jobId}/ai-jd-jobs` | `public_http` | `Draft — Needs Confirmation` | OQ-AIX-EVALUATION-KILL-SWITCH |
| [API-AIX-003](API-AIX-003_post-api-v1-enterprises-enterprise-id-applications-application-id-ai-match-explanations/00_Cover.md) | `POST` | `/api/v1/enterprises/{enterpriseId}/applications/{applicationId}/ai-match-explanations` | `public_http` | `Draft — Needs Confirmation` | OQ-AIX-EVALUATION-KILL-SWITCH |
| [API-AIX-004](API-AIX-004_post-api-v1-enterprises-enterprise-id-jobs-job-id-ai-shortlist-jobs/00_Cover.md) | `POST` | `/api/v1/enterprises/{enterpriseId}/jobs/{jobId}/ai-shortlist-jobs` | `public_http` | `Draft — Needs Confirmation` | OQ-AIX-EVALUATION-KILL-SWITCH |
| [API-AIX-005](API-AIX-005_get-api-v1-ai-jobs-ai-job-id/00_Cover.md) | `GET` | `/api/v1/ai-jobs/{aiJobId}` | `public_http` | `Draft — Needs Confirmation` | OQ-AIX-EVALUATION-KILL-SWITCH |
| [API-AIX-006](API-AIX-006_post-api-v1-ai-jobs-ai-job-id-reviews/00_Cover.md) | `POST` | `/api/v1/ai-jobs/{aiJobId}/reviews` | `public_http` | `Draft — Needs Confirmation` | OQ-AIX-EVALUATION-KILL-SWITCH |
| [API-AIX-007](API-AIX-007_post-api-v1-admin-ai-kill-switch/00_Cover.md) | `POST` | `/api/v1/admin/ai/kill-switch` | `public_http` | `Draft — Needs Confirmation` | OQ-AIX-EVALUATION-KILL-SWITCH |
| [API-AIX-008](API-AIX-008_put-api-v1-admin-ai-model-configs-config-id/00_Cover.md) | `PUT` | `/api/v1/admin/ai/model-configs/{configId}` | `public_http` | `Draft — Needs Confirmation` | OQ-AIX-EVALUATION-KILL-SWITCH |
| [API-AIX-009](API-AIX-009_post-api-v1-admin-ai-prompt-policies-policy-id-versions/00_Cover.md) | `POST` | `/api/v1/admin/ai/prompt-policies/{policyId}/versions` | `public_http` | `Draft — Needs Confirmation` | OQ-AIX-EVALUATION-KILL-SWITCH |
| [API-AIX-010](API-AIX-010_post-api-v1-admin-ai-evaluation-runs/00_Cover.md) | `POST` | `/api/v1/admin/ai/evaluation-runs` | `public_http` | `Draft — Needs Confirmation` | OQ-AIX-EVALUATION-KILL-SWITCH |
