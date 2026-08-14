# Study checkpoint

- APIs in checkpoint: 62.
- Status: all DDs remain Draft until missing contract/schema decisions are supplied.
- Source gaps/conflicts: see each Main gap value and root [OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md); no conflict is resolved by this batch.
- Validation: see root [VERIFICATION_REPORT.md](../VERIFICATION_REPORT.md).

| API | Method | Endpoint | Transport | Status | Main gap |
| ---: | --- | --- | --- | --- | --- |
| [API-STU-001](API-STU-001_get-api-v1-catalog-learning-paths/00_Cover.md) | `GET` | `/api/v1/catalog/learning-paths` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-002](API-STU-002_get-api-v1-catalog-learning-paths-slug/00_Cover.md) | `GET` | `/api/v1/catalog/learning-paths/{slug}` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-003](API-STU-003_get-api-v1-catalog-courses/00_Cover.md) | `GET` | `/api/v1/catalog/courses` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-004](API-STU-004_get-api-v1-catalog-courses-slug/00_Cover.md) | `GET` | `/api/v1/catalog/courses/{slug}` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-005](API-STU-005_get-api-v1-catalog-sample-lessons-lesson-id/00_Cover.md) | `GET` | `/api/v1/catalog/sample-lessons/{lessonId}` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-006](API-STU-006_get-api-v1-metadata-skills/00_Cover.md) | `GET` | `/api/v1/metadata/skills` | `public_http` | `Draft — Needs Confirmation` | OQ-STU-SKILLS-HISTORY |
| [API-STU-007](API-STU-007_get-api-v1-me-study-profile/00_Cover.md) | `GET` | `/api/v1/me/study-profile` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-008](API-STU-008_patch-api-v1-me-study-profile/00_Cover.md) | `PATCH` | `/api/v1/me/study-profile` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-009](API-STU-009_get-api-v1-me-onboarding/00_Cover.md) | `GET` | `/api/v1/me/onboarding` | `public_http` | `Draft — Needs Confirmation` | OQ-STU-ONBOARDING |
| [API-STU-010](API-STU-010_patch-api-v1-me-onboarding/00_Cover.md) | `PATCH` | `/api/v1/me/onboarding` | `public_http` | `Draft — Needs Confirmation` | OQ-STU-ONBOARDING |
| [API-STU-011](API-STU-011_post-api-v1-me-onboarding-complete/00_Cover.md) | `POST` | `/api/v1/me/onboarding/complete` | `public_http` | `Draft — Needs Confirmation` | OQ-STU-ONBOARDING |
| [API-STU-012](API-STU-012_get-api-v1-me-path-recommendations/00_Cover.md) | `GET` | `/api/v1/me/path-recommendations` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-013](API-STU-013_get-api-v1-me-primary-path/00_Cover.md) | `GET` | `/api/v1/me/primary-path` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-014](API-STU-014_put-api-v1-me-primary-path/00_Cover.md) | `PUT` | `/api/v1/me/primary-path` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-015](API-STU-015_get-api-v1-me-primary-path-history/00_Cover.md) | `GET` | `/api/v1/me/primary-path/history` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-016](API-STU-016_post-api-v1-courses-course-id-enrollments/00_Cover.md) | `POST` | `/api/v1/courses/{courseId}/enrollments` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-017](API-STU-017_get-api-v1-me-course-enrollments/00_Cover.md) | `GET` | `/api/v1/me/course-enrollments` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-018](API-STU-018_get-api-v1-courses-course-id-study/00_Cover.md) | `GET` | `/api/v1/courses/{courseId}/study` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-019](API-STU-019_get-api-v1-lessons-lesson-id-study/00_Cover.md) | `GET` | `/api/v1/lessons/{lessonId}/study` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-020](API-STU-020_patch-api-v1-lessons-lesson-id-progress/00_Cover.md) | `PATCH` | `/api/v1/lessons/{lessonId}/progress` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-021](API-STU-021_get-api-v1-me-progress-summary/00_Cover.md) | `GET` | `/api/v1/me/progress/summary` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-022](API-STU-022_get-api-v1-me-learning-history/00_Cover.md) | `GET` | `/api/v1/me/learning-history` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-023](API-STU-023_get-api-v1-assessments-assessment-id/00_Cover.md) | `GET` | `/api/v1/assessments/{assessmentId}` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-024](API-STU-024_get-api-v1-assessments-assessment-id-draft/00_Cover.md) | `GET` | `/api/v1/assessments/{assessmentId}/draft` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-025](API-STU-025_put-api-v1-assessments-assessment-id-draft/00_Cover.md) | `PUT` | `/api/v1/assessments/{assessmentId}/draft` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-026](API-STU-026_delete-api-v1-assessments-assessment-id-draft/00_Cover.md) | `DELETE` | `/api/v1/assessments/{assessmentId}/draft` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-027](API-STU-027_post-api-v1-assessments-assessment-id-attempts/00_Cover.md) | `POST` | `/api/v1/assessments/{assessmentId}/attempts` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-028](API-STU-028_get-api-v1-assessments-assessment-id-attempts/00_Cover.md) | `GET` | `/api/v1/assessments/{assessmentId}/attempts` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-029](API-STU-029_get-api-v1-assessment-attempts-attempt-id/00_Cover.md) | `GET` | `/api/v1/assessment-attempts/{attemptId}` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-030](API-STU-030_post-api-v1-file-upload-sessions/00_Cover.md) | `POST` | `/api/v1/file-upload-sessions` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-031](API-STU-031_post-api-v1-file-upload-sessions-id-finalize/00_Cover.md) | `POST` | `/api/v1/file-upload-sessions/{id}/finalize` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-032](API-STU-032_get-api-v1-file-assets-file-id-status/00_Cover.md) | `GET` | `/api/v1/file-assets/{fileId}/status` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-033](API-STU-033_post-api-v1-file-assets-file-id-download-urls/00_Cover.md) | `POST` | `/api/v1/file-assets/{fileId}/download-urls` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-034](API-STU-034_get-api-v1-notifications/00_Cover.md) | `GET` | `/api/v1/notifications` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-035](API-STU-035_post-api-v1-notifications-id-read/00_Cover.md) | `POST` | `/api/v1/notifications/{id}/read` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-036](API-STU-036_post-api-v1-notifications-read-all/00_Cover.md) | `POST` | `/api/v1/notifications/read-all` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-037](API-STU-037_get-api-v1-me-notification-preferences/00_Cover.md) | `GET` | `/api/v1/me/notification-preferences` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-038](API-STU-038_put-api-v1-me-notification-preferences/00_Cover.md) | `PUT` | `/api/v1/me/notification-preferences` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-039](API-STU-039_get-api-v1-community-groups/00_Cover.md) | `GET` | `/api/v1/community-groups` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-040](API-STU-040_post-api-v1-community-groups-id-rule-acceptances/00_Cover.md) | `POST` | `/api/v1/community-groups/{id}/rule-acceptances` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-041](API-STU-041_post-api-v1-community-groups-id-open-link/00_Cover.md) | `POST` | `/api/v1/community-groups/{id}/open-link` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-042](API-STU-042_post-api-v1-community-groups-id-reports/00_Cover.md) | `POST` | `/api/v1/community-groups/{id}/reports` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-043](API-STU-043_post-api-v1-support-requests/00_Cover.md) | `POST` | `/api/v1/support-requests` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-044](API-STU-044_get-api-v1-support-requests/00_Cover.md) | `GET` | `/api/v1/support-requests` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-045](API-STU-045_get-api-v1-support-requests-id/00_Cover.md) | `GET` | `/api/v1/support-requests/{id}` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-046](API-STU-046_post-api-v1-support-requests-id-cancel/00_Cover.md) | `POST` | `/api/v1/support-requests/{id}/cancel` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-047](API-STU-047_get-api-v1-admin-assessment-reviews/00_Cover.md) | `GET` | `/api/v1/admin/assessment-reviews` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-048](API-STU-048_post-api-v1-admin-assessment-attempts-attempt-id-reviews/00_Cover.md) | `POST` | `/api/v1/admin/assessment-attempts/{attemptId}/reviews` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-049](API-STU-049_post-api-v1-admin-learners-learner-id-primary-path-overrides/00_Cover.md) | `POST` | `/api/v1/admin/learners/{learnerId}/primary-path-overrides` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-050](API-STU-050_post-api-v1-admin-learners-learner-id-progress-adjustments/00_Cover.md) | `POST` | `/api/v1/admin/learners/{learnerId}/progress-adjustments` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-051](API-STU-051_get-api-v1-admin-content-kind/00_Cover.md) | `GET` | `/api/v1/admin/content/{kind}` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-052](API-STU-052_post-api-v1-admin-content-kind/00_Cover.md) | `POST` | `/api/v1/admin/content/{kind}` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-053](API-STU-053_post-api-v1-admin-content-kind-id-versions/00_Cover.md) | `POST` | `/api/v1/admin/content/{kind}/{id}/versions` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-054](API-STU-054_patch-api-v1-admin-content-kind-id-versions-version-id/00_Cover.md) | `PATCH` | `/api/v1/admin/content/{kind}/{id}/versions/{versionId}` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-055](API-STU-055_post-api-v1-admin-content-kind-id-versions-version-id-pre-publish-checks/00_Cover.md) | `POST` | `/api/v1/admin/content/{kind}/{id}/versions/{versionId}/pre-publish-checks` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-056](API-STU-056_post-api-v1-admin-content-kind-id-versions-version-id-publish/00_Cover.md) | `POST` | `/api/v1/admin/content/{kind}/{id}/versions/{versionId}/publish` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-057](API-STU-057_post-api-v1-admin-content-kind-id-archive/00_Cover.md) | `POST` | `/api/v1/admin/content/{kind}/{id}/archive` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-058](API-STU-058_get-api-v1-admin-content-issues/00_Cover.md) | `GET` | `/api/v1/admin/content-issues` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-059](API-STU-059_put-api-v1-admin-content-issues-id-status/00_Cover.md) | `PUT` | `/api/v1/admin/content-issues/{id}/status` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-060](API-STU-060_put-api-v1-admin-local-role-assignments-user-id/00_Cover.md) | `PUT` | `/api/v1/admin/local-role-assignments/{userId}` | `public_http` | `Draft — Needs Confirmation` | SOURCE_REQUIRED field-level detail |
| [API-STU-061](API-STU-061_get-api-v1-me-evidence/00_Cover.md) | `GET` | `/api/v1/me/evidence` | `public_http` | `Draft — Needs Confirmation` | OQ-STU-EVIDENCE-FILES |
| [API-STU-062](API-STU-062_get-api-v1-me-evidence-evidence-id/00_Cover.md) | `GET` | `/api/v1/me/evidence/{evidenceId}` | `public_http` | `Draft — Needs Confirmation` | OQ-STU-EVIDENCE-FILES |
