# Study2Work — Study API List từ `docs/BD/diagram`

> Phạm vi: Chỉ lấy API xuất hiện trực tiếp trong `docs/BD/diagram/`.
> Không lấy API từ API Catalog, DD cũ, BD suy dẫn hoặc endpoint tự bổ sung.

| # | Method | Endpoint | Diagram |
|---:|---|---|---|
| 1 | GET | `/api/v1/catalog/learning-paths` | SEQ-02 |
| 2 | GET | `/api/v1/catalog/courses/{slug}` | SEQ-02 |
| 3 | GET | `/api/v1/catalog/sample-lessons/{lesson_id}` | SEQ-02 |
| 4 | POST | `/api/v1/auth/register` | SEQ-03 |
| 5 | POST | `/api/v1/auth/login` | SEQ-03 |
| 6 | POST | `/api/v1/auth/verify-contact` | SEQ-03 |
| 7 | GET | `/api/v1/onboarding/current` | SEQ-04 |
| 8 | PATCH | `/api/v1/onboarding/draft` | SEQ-04 |
| 9 | GET | `/api/v1/onboarding/recommended-paths` | SEQ-04 |
| 10 | POST | `/api/v1/onboarding/confirm` | SEQ-04 |
| 11 | POST | `/api/v1/learning-paths/{path_id}/activate` | SEQ-05 |
| 12 | GET | `/api/v1/lessons/{lesson_id}/study` | SEQ-06 |
| 13 | PATCH | `/api/v1/lessons/{lesson_id}/progress` | SEQ-06 |
| 14 | GET | `/api/v1/exercises/{assignment_id}` | SEQ-07 |
| 15 | POST | `/api/v1/exercises/{assignment_id}/submissions` | SEQ-07 |
| 16 | PATCH | `/api/v1/admin/exercise-submissions/{submission_id}/review` | SEQ-07 |
| 17 | GET | `/api/v1/community-groups` | SEQ-09 |
| 18 | POST | `/api/v1/community-groups/{group_id}/open-link` | SEQ-09 |
| 19 | POST | `/api/v1/community-groups/{group_id}/reports` | SEQ-09 |
| 20 | PATCH | `/api/v1/admin/community-groups/{group_id}` | SEQ-09 |
| 21 | GET | `/api/v1/notifications` | SEQ-10 |
| 22 | PATCH | `/api/v1/notifications/{notification_id}/read` | SEQ-10 |
| 23 | PUT | `/api/v1/notification-settings/me` | SEQ-10 |
| 24 | POST | `/api/v1/admin/notifications` | SEQ-10 |
| 25 | POST | `/api/v1/admin/content/{content_type}/{content_id}/pre-publish-check` | SEQ-11 |
| 26 | POST | `/api/v1/admin/content/{content_type}/{content_id}/publish` | SEQ-11 |
| 27 | POST | `/api/v1/support-requests` | SEQ-12 |
| 28 | GET | `/api/v1/admin/learners/{learner_id}/support-profile` | SEQ-12 |
| 29 | POST | `/api/v1/admin/support-requests/{request_id}/resolve` | SEQ-12 |
| 30 | GET | `/api/v1/admin/reports/overview` | SEQ-13 |
| 31 | GET | `/api/v1/admin/reports/alerts` | SEQ-13 |
| 32 | GET | `/api/v1/admin/audit-logs` | SEQ-14 |

## Tổng số

**32 API**
