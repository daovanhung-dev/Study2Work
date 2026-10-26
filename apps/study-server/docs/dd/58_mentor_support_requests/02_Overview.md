---
title: "Overview"
order: 2
dd_id: "58"
api_name: "Lấy support requests"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 58 |
| Module | MENTOR / TEACHING & SUPPORT |
| Method | GET |
| Endpoint | /api/v1/mentor/support/requests |
| Purpose | Đọc yêu cầu hỗ trợ trong phạm vi Mentor để chọn request và mở thread bằng API #59. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Role Mentor; numeric JWT subject chỉ đọc request thuộc course có `courses.mentor_id` bằng subject. Fallback theo direct-owner pattern của Mentor API Study hiện có. |
| Basis | Method/path/actor/filter fields là DIRECT. BIGINT support tables, direct-owner predicate, collection response và projection rules là `DERIVED` theo chỉ dẫn của user; live schema/deployment chưa xác minh. |
| Status | Draft — Needs Confirmation |
| Transaction | N/A — READ-ONLY API |
| Side effects | Không có mutation được khai báo. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md).
- [AC/API index, AC-24](../../diagrams/AC_UNICA/00_AC_API_INDEX.md).
- [AC-24 diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio).
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md).
- [DB ERD](../../diagrams/DB_UNICA_ERD.drawio).
- [Legacy DB.sql](../../../../../infra/postgres/study-server/DB.sql).
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql).
- [Current Study router](../../../../../apps/study-server/app/api/v1.py).
- [Current Study auth helper](../../../../../apps/study-server/app/utils/auth.py).
- [Current error middleware](../../../../../apps/study-server/app/core/middleware.py).
- [API Guidelines](../../../../../contracts/api-guidelines/README.md).
- [Related Mentor list DD #54](../54_mentor_submissions_list/02_Overview.md).
- [Study API DD workflow](../../../../../.agents/server-study/workflows/README.md).

## Tables read

- `support_requests`, `support_messages`, `support_message_uploads`, `courses`, `users`, `uploads`.
- Support tables có DDL trong legacy BIGINT bootstrap và migration 008; chưa chứng minh đã áp dụng vào live DB.
- V1-PILOT UUID support tables là model riêng, không được dùng trong query API #58.

## Tables write

- N/A — READ-ONLY API.

## Mục chú ý

- Endpoint/path là danh sách; fallback chọn `ApiEnvelope<SupportRequest[]>`, empty result là `[]`; không thêm pagination vì catalog không khai báo page/size.
- Query `course_id` và `status` kết hợp bằng AND; `status` là exact match. DDL cho phép `OPEN`, `IN_PROGRESS`, `WAITING_LEARNER`, `RESOLVED`, `CANCELLED`.
- `support_requests.course_id` và `student_id` dùng BIGINT FK tới `courses`/`users`; Mentor scope nối qua `courses.mentor_id`.
- Response list tải toàn bộ `messages[]` theo reusable schema; message order `created_at ASC, id ASC`; request order `created_at DESC, id DESC`.
- Attachments dùng bảng nối có thứ tự và `uploads` metadata; resolver giới hạn cùng author, course, role-purpose và `UPLOADED`.
- Query `course_id` parse/range errors trả 422 `DESIGN_VALIDATION_ERROR`; catalog/diagram được đồng bộ với shared validation handler.

## Assumptions

- Nếu cả hai query filter được gửi, áp dụng AND; lựa chọn `DERIVED`.
- `status` được so khớp chính xác; không trim hoặc đổi casing. Giá trị chưa biết trả danh sách rỗng.
- Không phân trang hoặc cắt `messages[]`; collection trả đủ dữ liệu theo reusable schema.
- Khi `resolved_at` là NULL, trường bị omit theo response serialization convention hiện tại.

## Conflicts

- Catalog/diagram ban đầu khai báo singleton; fallback collection đã được đồng bộ vào catalog, diagram và DD.
- Legacy DB ban đầu không có support tables; DDL/migration 008 bổ sung BIGINT model theo Study runtime conventions. Live migration chưa xác minh.
- V1-PILOT UUID support model không được dùng bởi API #58.
- API #58 được thêm vào `DESIGN_CONTRACT_PATHS`; error envelope dùng shared helper, `data:null`.

## Security note

- AC-24 giới hạn dữ liệu theo Mentor. Mọi list/message query nối `courses.mentor_id = :mentor_id`; query `course_id` chỉ là filter bổ sung.
- Dùng shared role-aware guard với `role="MENTOR"`; caller subject là numeric user ID theo Study token contract hiện tại.
- Upload chỉ trả khi link message rõ ràng và metadata khớp author, course, `SUBMISSION` cho Student hoặc `LECTURE` cho Mentor, cùng status `UPLOADED`.

## Performance note

- Không có pagination hoặc message limit trong catalog; collection/thread response có thể lớn. Đây là residual risk của fallback.
- API #59 vẫn tải thread riêng, nên #58 full messages có thể lặp dữ liệu nhưng khớp reusable `SupportRequest` schema.
- Stable ordering được chọn từ timestamp/ID, không suy từ index của pilot schema.

## Trạng thái liên quan

- [Plan, fallback decisions và ma trận nguồn](./PLAN_RESULT.md).
- [Open Questions](./OPEN_QUESTIONS.md).
- [Verification report](./VERIFICATION_REPORT.md).
- Macro-review AC-24 #58–#61: APIs #59–#61 cần reuse support schema, direct-owner predicate và attachment resolver trong các phiên sau.
---
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
