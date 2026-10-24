# Plan Result — Study API #54 Lấy submissions Mentor

**Status:** `PARTIALLY COMPLETED — Draft đã tạo; contract/source questions còn mở`
**API:** `GET /api/v1/mentor/submissions`
**Output folder:** `apps/study-server/docs/dd/54_mentor_submissions_list/`
**Basis:** Catalog `DIRECT`; AC-23 flow `DIRECT`; physical query `DESIGN CANDIDATE`
**Deliverable:** 8 Markdown sheets + 3 reports; Study workflow không tạo ZIP.

## Nguồn đã nạp

- `docs/lists/list_api.md`: API #54, reusable `Submission`, `UploadAsset`, `ApiEnvelope` và business-code design-only.
- `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md`: actor, precondition, postcondition và thứ tự gọi API AC-23.
- `apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio`: đọc toàn bộ node/edge trang AC-23.
- `apps/study-server/docs/diagrams/DB_UNICA_TABLES.md` và `DB_UNICA_ERD.drawio`: candidate `assignment_submissions → assignments → courses`, owner relation `users → courses`.
- `infra/postgres/study-server/DB.sql`: checked-in V1-PILOT candidate columns; không chứng minh live schema.
- `apps/study-server/docs/dd/35_assignments_submissions/`: related Submission contract/schema gaps.
- Current Study router, auth helper, middleware, response helper, API Guidelines và scope context.
- Registered Markdown templates: `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/`.

## Contract giữ nguyên

| Item | Giá trị |
|---|---|
| Method/path | `GET /api/v1/mentor/submissions` |
| Auth | Bearer JWT; role `Mentor` |
| Query | `course_id?:int64`, `status?:string`, `page?:int32` |
| Body/path | Không khai báo |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Submission>` |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 409 `DESIGN_STATE_CONFLICT`; 500 `DESIGN_INTERNAL_ERROR` |

## Plan và ranh giới

1. Diagram xác nhận Mentor mở danh sách, backend đọc submissions theo quyền Mentor, chọn một submission rồi gọi API #55 để đọc details/files/rubric. API #54 không nhận rubric write hoặc feedback.
2. Giữ response `Submission` đúng như catalog dù tên và flow là danh sách; không tự bọc `items`, `Page<T>` hay pagination trong `meta`.
3. Optional `course_id` và `status` là filter candidates chỉ khi được gửi. Status enum/blank handling chưa có nguồn.
4. `page` không có `size`, default, range, ordering hoặc response metadata; không suy ra `LIMIT/OFFSET` hoặc page size.
5. Candidate tables là `assignment_submissions`, `assignments`, `courses`; join và quyền Mentor là design proposals, không phải SQL/runtime đã được xác nhận.
6. Chỉ nêu `courses.mentor_id` làm direct-owner candidate DERIVED; Mentor claim identity và assigned-course access vẫn SOURCE_REQUIRED.
7. Giữ toàn bộ fields của Submission; `files:UploadAsset[]` không map đủ từ `assignment_submissions.file_url` nên không tạo sample assets giả.
8. Bảng #54 là read-only; `07_table.md` giữ template và ghi `N/A — READ-ONLY API`.
9. Status DD `Draft — Needs Confirmation` vì cardinality, pagination, status, access và asset data chưa được nguồn chốt.
10. AC-23 macro-review #54–#57 sẽ chờ đến khi các DD liên quan có mặt.

## Ma trận Query dự kiến

| Query | Type | Candidate | Conditions | Gaps |
|---|---|---|---|---|
| Q1 | SELECT | `assignment_submissions` join `assignments`, candidate access via `courses` | Apply course/status filters only if supplied; scope to Mentor-authorized courses | Live schema, access mapping, nullable FKs, sort and pagination not verified |
| Q2 | COUNT | Không được catalog/diagram yêu cầu | Không tạo query count | Page metadata absent |

## Ma trận mutation dự kiến

| Operation | Kết quả |
|---|---|
| INSERT/UPDATE/DELETE | `N/A — READ-ONLY API` |

## Kết quả verification

Được cập nhật sau authoring và static checks trong `VERIFICATION_REPORT.md`.
