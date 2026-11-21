# Plan Result — Study API #54 Lấy submissions Mentor

**Kết quả:** Implemented with DERIVED fallback decisions; contract remains Draft — Needs Confirmation.

## Nguồn đã nạp

- API catalog #54 và reusable `ApiEnvelope`, `Page`, `Submission`, `UploadAsset`.
- AC-23 index/diagram: mở danh sách, đọc theo quyền Mentor, chọn một bài, gọi #55 detail.
- DB table guide, ERD, checked-in `DB.sql`, upload migration #004.
- Related producer/reader APIs #34/#35/#36 and AC-23 consumers #55–#57.
- Current route/auth/response sources and Mentor ownership/pagination patterns #46/#49.
- Three coding worklogs selected by mandatory preflight and recorded in the active worklog.

## Contract giữ và fallback

| Item | Selected behavior | Evidence/status |
|---|---|---|
| Method/path/filters | GET `/api/v1/mentor/submissions`; optional course_id, status, page | Direct catalog/diagram |
| Response cardinality | `ApiEnvelope<Page<Submission>>` | DERIVED from AC-23 list/select; catalog/diagram were updated |
| Pagination | page defaults 1; size fixed 20; submitted_at DESC, id DESC; PageMeta in data | DERIVED from shared #46 pattern |
| Mentor scope | Numeric JWT subject equals direct `courses.mentor_id` | Existing #46/#49 pattern; assigned mentors unsupported |
| Files | Match `file_url` to upload URL + owner + SUBMISSION purpose + course | DERIVED; no FK/live schema proof |
| Empty result | 200 with empty items and zero totals | DERIVED collection behavior |
| 409 | Retained in declared set, no trigger implemented | AC-23 gives no state conflict condition |
| Query validation | Positive int64 course_id and int32 page; 422 | Added to catalog/diagram and route contract |

## Implementation boundary

- Read-only; no transaction commit or schema migration.
- Orphan/null assignment/course/student relations are excluded through inner joins, matching required ERD relations while preserving the nullable DDL discrepancy.
- API #55 owns selected-Submission detail and reuses the constrained file fallback; the diagram's rubric request remains unresolved. APIs #56/#57 retain their separate grade/feedback mutations.

## Verification

See `VERIFICATION_REPORT.md`. Fake-session tests do not prove live PostgreSQL schema or upload-link data.
