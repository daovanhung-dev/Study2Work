---
title: "Overview"
order: 2
dd_id: "65"
api_name: "Lấy tiến độ toàn lớp"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #65 |
| Module | MENTOR / TEACHING & SUPPORT — AC-26 |
| Method | GET |
| Endpoint | /api/v1/mentor/courses/{course_id}/progress |
| Purpose | Đọc tiến độ tổng hợp của người học trong một course để Mentor xem dashboard lớp. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Shared MENTOR guard; direct owner check `courses.mentor_id = JWT sub` theo local API #62 precedent. Đây là DERIVED policy. |
| Basis | Method/path/input/response/status/errors DIRECT từ catalog; roster-level progress DIRECT ở mức mục tiêu AC-26; công thức và response thay thế DERIVED. |
| Status | Draft — Needs Confirmation |
| Current runtime state | WIRED locally — route, module, middleware design-code path, focused HTTP tests, and OpenAPI exist. |
| Transaction | Read-only — course lookup then one aggregate query; fake-session tests verify no commit, live DB consistency is unverified. |
| Side effects | Không có mutation hay lời gọi API #66/#67 được đặc tả trong #65. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #65–#67, ApiEnvelope<T>, Page<T>, PageMeta, Course, UserSummary.
- [AC/API index, AC-26](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition, postcondition và thứ tự API #65 → #66 → #67.
- [AC-26 activity diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — mở progress dashboard, tải class progress, tải analytics, chọn Student rồi đọc progress chi tiết.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) — #65/#67 có SELECT mapping ở trạng thái DESIGN_ONLY.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate BIGINT relations courses, enrollments, users, lessons và lesson_progress; không phải live-schema proof.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID/versioned progress relations; khác ID contract int64 và không được trộn với legacy model.
- [API #9 curriculum](../09_courses_curriculum/02_Overview.md) và [API #25 progress](../25_lessons_progress/02_Overview.md) — published lesson/progress evidence; không chốt công thức class aggregate.
- [API #46 managed courses](../46_mentor_courses/02_Overview.md) và [API #62 course students](../62_mentor_course_students/02_Overview.md) — Mentor ownership/roster precedent và các identity/pagination gap.
- Current [Study router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [API guidelines](../../../../../contracts/api-guidelines/README.md).
- [Canonical DD Markdown templates](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — tám sheet; fingerprint ở [PLAN_RESULT](./PLAN_RESULT.md).

## Tables/entities đọc

- courses — legacy candidate để xác định course và direct owner qua mentor_id.
- enrollments + users — legacy candidate để lập một dòng mỗi learner đã enroll.
- lessons — legacy candidate để đếm lesson thuộc course; lọc PUBLISHED là đề xuất DERIVED từ API #9.
- lesson_progress — legacy candidate chứa status/progress percent; DDL không enforce uniqueness hoặc percent range. Local fallback chọn row mới nhất theo `last_accessed_at DESC NULLS LAST, id DESC`.
- Các quan hệ trên là checked-in legacy design evidence; test dùng fake DB, không xác nhận schema live/production.

## Tables/entities ghi

N/A — READ-ONLY API. Không có INSERT/UPDATE/DELETE được đặc tả.

## Mục chú ý

- Giữ direct contract từ catalog trong hồ sơ: ApiEnvelope<Page<Course>>. Local runtime dùng Page<MentorStudentProgress> để đáp ứng mục tiêu AC-26; đây là `DISCREPANCY`, chưa phải catalog change hay owner approval.
- AC-26 tách #65 roster/progress, #66 learning-event analytics và #67 learner detail. Không nhập logic của hai API sau vào #65.
- Contract khai báo PageMeta nhưng không có query page/size. Local runtime trả toàn bộ roster trong một page (`page=1`, `size=total`); đây là DERIVED, không có bound theo request.
- Local access predicate `courses.mentor_id = JWT sub` kiểm tra trước roster query và lặp lại trong aggregate SQL; assigned-Mentor policy không được hỗ trợ bởi nguồn hiện có.
- Không dùng schema UUID/versioned của V1-PILOT như thể tương thích với contract int64.

## Phương án DERIVED để review — không phải wire contract

| Thành phần | Đề xuất đơn giản | Cơ sở/trạng thái |
|---|---|---|
| Item | student:UserSummary, completed_lessons:int32, total_lessons:int32, progress_percent:int32 | Dạng tối thiểu để biểu diễn class progress; DERIVED. |
| Learner set | Distinct user IDs từ ACTIVE enrollments có users.role='STUDENT' | DERIVED local fallback theo API #62. |
| Denominator | Số lesson PUBLISHED thuộc course | DERIVED local fallback theo visibility API #9. |
| Completed | Đếm latest selected lesson_progress rows có status='COMPLETED' trong denominator | DERIVED local fallback; legacy enum không có CHECK constraint. |
| Percent | floor(sum(COALESCE(progress_percent,0)) / total_lessons); trả 0 khi denominator bằng 0 | DERIVED local fallback; invalid progress state/range trả safe 500. |
| Duplicate progress | Dùng row mới nhất mỗi `(user_id, lesson_id)` theo `last_accessed_at DESC NULLS LAST, id DESC` | DERIVED do legacy DDL không có unique key; test/source xác nhận local policy. |
| Pagination | Không có input nên runtime trả một page đầy đủ: page=1, size=total; empty: size=0,total_pages=0 | DERIVED local fallback; catalog chưa có pagination limit/input. |

## Conflicts

| Nguồn A | Nguồn B | Xung đột | Ảnh hưởng |
|---|---|---|---|
| Catalog #65 | AC-26 | Catalog trả Page<Course>; AC cần class progress. | Contract hiện tại không có field learner/progress. |
| PageMeta | Request catalog #65 | Cần page/size/total/total_pages nhưng request không nhận page/size. | Pagination behavior không thể suy ra là bounded. |
| Legacy DDL | V1-PILOT DDL | BIGINT enrollment/progress khác UUID/versioned facts/snapshots. | Không thể coi hai schema là một nguồn mapping. |

## Security note

- Catalog yêu cầu Bearer JWT và role Mentor.
- Xác minh course scope trước khi trả learner roster; không suy ra mentor_id từ path.
- Local behavior xác thực role trước DB; course vắng mặt trả 404, course của Mentor khác trả 403, theo API #62 precedent. Privacy policy ở deployment chưa xác nhận.

## Reliability note

- Đây là read-only dashboard query; không kích hoạt tính toán nền hay gửi event được đặc tả.
- Không có freshness/SLA/snapshot contract cho progress cache hoặc learning events.
- Một page không giới hạn có thể tăng tải theo quy mô lớp; local fallback không chứng minh phù hợp ở production. Cần pagination decision trước khi dùng cho roster lớn.

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | 【Khái quát】 |  |
| 3 | `B3` | Get thông tin…. |  |
| 5 | `A5` | 【Mục chú ý】 |  |
| 7 | `B7` | Không có |  |

</details>
