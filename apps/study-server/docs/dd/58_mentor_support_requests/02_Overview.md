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
| Authorization | Role Mentor; chỉ đọc request thuộc phạm vi phụ trách theo AC-24. Scope và identity binding chưa có source runtime. |
| Basis | Catalog và AC-24 là DIRECT; quy tắc lọc/mapping vật lý còn DERIVED/SOURCE_REQUIRED. |
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

- Chưa chốt physical table cho API #58.
- V1-PILOT candidate: support_tickets, support_messages, learner_profiles, file_objects; model khác ID/quan hệ, không chứng minh runtime schema.

## Tables write

- N/A — READ-ONLY API.

## Mục chú ý

- Endpoint/name là danh sách nhưng catalog và diagram khai báo response đơn ApiEnvelope<SupportRequest>; chưa có Page, array wrapper, page hoặc sort.
- Query course_id là optional nhưng support_tickets của V1-PILOT không có course_id hoặc quan hệ course.
- Query status là string; catalog không định nghĩa SupportStatus values, default, casing hoặc xử lý chuỗi rỗng.
- SupportRequest yêu cầu int64 IDs, course_id, Student/UserSummary, message IDs và UploadAsset[]; V1-PILOT dùng UUID và không có projection tương thích.
- API #59 đọc thread riêng; chưa rõ #58 có tải toàn bộ messages[] của từng request hay không, dù schema response bắt buộc messages[].
- Source Study hiện không có route, module hoặc test cho API #58.

## Assumptions

- Nếu cả hai query filter được gửi, candidate áp dụng đồng thời bằng AND; DERIVED, cần xác nhận.
- status candidate được so khớp nguyên giá trị được gửi; không trim, đổi casing hay gán default khi chưa có rule duyệt.
- Không tự chọn bản ghi đầu tiên, cắt danh sách hoặc đổi response thành array/Page để che mâu thuẫn cardinality.

## Conflicts

- AC-24 mô tả mở danh sách và endpoint plural nhưng catalog/diagram trả singular SupportRequest.
- Legacy ERD/DB.sql không có support tables; V1-PILOT có UUID support_tickets/support_messages nhưng thiếu course relation và khác projection.
- API Guidelines yêu cầu error data null; current helper mặc định {}; API #58 chưa có trong DESIGN_CONTRACT_PATHS.
- Query course_id yêu cầu lọc course nhưng schema hiện có không xác nhận relation.

## Security note

- AC-24 giới hạn dữ liệu theo Mentor. Không trả request ngoài scope hoặc dùng course_id client gửi làm authorization.
- Pilot assigned_to_subject_id là nullable UUID candidate; Mentor principal mapping và assignment semantics chưa xác nhận.
- Shared current-user guard hiện chỉ chấp nhận STUDENT; không dùng như Mentor guard.

## Performance note

- Không có pagination, page size, thứ tự request hoặc giới hạn messages trong contract.
- Nếu messages[] đầy đủ cho từng request, payload có thể lớn; cần xem lại sau khi cardinality/projection được xác nhận.
- Không suy thứ tự API từ index của pilot schema.

## Trạng thái liên quan

- [Plan và ma trận nguồn](./PLAN_RESULT.md).
- [Open Questions](./OPEN_QUESTIONS.md).
- [Verification report](./VERIFICATION_REPORT.md).
- Macro-review AC-24 #58–#61 chờ #59–#61; chưa đánh dấu hoàn tất.
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
