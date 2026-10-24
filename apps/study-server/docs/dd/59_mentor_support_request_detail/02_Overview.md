---
title: "Overview"
order: 2
dd_id: "59"
api_name: "Lấy nội dung request/thread"
source_sheet: "Overview"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 59 |
| Module | MENTOR / TEACHING & SUPPORT |
| Method | GET |
| Endpoint | /api/v1/mentor/support/{request_id} |
| Purpose | Đọc chi tiết một support request và conversation trong phạm vi Mentor. |
| Consumer/Actor | Mentor |
| Authentication | Bearer JWT |
| Authorization | Role Mentor; AC-24 yêu cầu request thuộc phạm vi phụ trách. Predicate và identity binding chưa có source runtime. |
| Basis | Catalog và AC-24 là DIRECT; mapping vật lý/nested projection còn SOURCE_REQUIRED. |
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
- [Related support request list DD #58](../58_mentor_support_requests/02_Overview.md).
- [Study API DD workflow](../../../../../.agents/server-study/workflows/README.md).

## Tables read

- Chưa chốt physical table cho API #59.
- V1-PILOT có `support_tickets` và `support_messages` candidate; ID UUID, thiếu course relation và không chứng minh live/runtime mapping.
- Legacy Study DB.sql/ERD không khai báo support request/message model.

## Tables write

- N/A — READ-ONLY API.

## Mục chú ý

- Đây là endpoint detail, response `ApiEnvelope<SupportRequest>` là object đơn như catalog; không có list-cardinality conflict của #58.
- Path `request_id` là int64 theo catalog; pilot ticket ID và message ID là UUID, không tương thích trực tiếp.
- AC-24 yêu cầu Mentor đọc request trong phạm vi phụ trách, nhưng current Study auth guard chỉ chấp nhận Student; principal/assignment mapping chưa có source.
- SupportRequest cần course_id, student, status và messages; SupportMessage cần author, content, attachments, created_at. Không có mapping vật lý được duyệt cho các nested projection.
- API #60 gửi reply và #61 resolve là action riêng; #59 không mutation.
- Source Study hiện không có route, module hoặc test cho API #59.

## Assumptions

- Không giả định `assigned_to_subject_id`, ownership của course hay enrollment là predicate quyền đã duyệt.
- Không giả định message order, page/limit, internal-message visibility hoặc null-versus-omit behavior.
- Ví dụ chỉ minh họa schema API; không xác nhận enum hay dữ liệu persistence.

## Conflicts

- Legacy DB.sql/ERD không có support tables; V1-PILOT UUID model không khớp contract int64 và không có course relation trên ticket.
- Pilot message có `is_internal`, nhưng contract/diagram chưa xác định actor nào được thấy internal messages.
- API Guidelines yêu cầu error `data:null`; current helper mặc định `{}` khi caller không truyền data. API #59 chưa wired.

## Security note

- Không trả request ngoài phạm vi Mentor theo AC-24.
- Không dùng `request_id` hoặc bất kỳ input client nào làm bằng chứng quyền truy cập.
- Predicate, subject mapping và thứ tự kiểm tra tồn tại/quyền cần được chủ API xác nhận trước implementation.

## Performance note

- Không có pagination hoặc message limit trong catalog.
- Response gồm toàn bộ `messages[]` theo reusable schema; payload bound/order chưa quy định.
- Không truy vấn/đưa attachment URL vào response nếu chưa có resolver và eligibility policy được duyệt.

## Trạng thái liên quan

- [Plan và ma trận nguồn](./PLAN_RESULT.md).
- [Open Questions](./OPEN_QUESTIONS.md).
- [Verification report](./VERIFICATION_REPORT.md).
- Macro-review AC-24 #58–#61 vẫn pending đến khi #60/#61 có DD và cả nhóm được đối chiếu.

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
