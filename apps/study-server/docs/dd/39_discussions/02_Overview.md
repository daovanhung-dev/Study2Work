---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "39"
api_name: "Lấy danh sách thread"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 39 |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | GET |
| Endpoint | /api/v1/discussions |
| Purpose | Lấy danh sách thread thảo luận theo contract API #39 và AC-19. |
| Consumer/Actor | Student |
| Authentication | Bearer JWT |
| Authorization | Student role; DERIVED: enrollment ACTIVE cho course của topic. Khi course_id vắng mặt, scope theo tất cả enrollment ACTIVE của principal. |
| Basis | APPROVED_DESIGN_CONTRACT; AC-19; DB design evidence |
| Status | Draft — Needs Confirmation |
| Current runtime state | UNWIRED / NOT_FOUND — Study Server hiện chưa có route/module/test discussion. |
| Transaction | N/A — GET read-only |
| Side effects | N/A — không có mutation được định nghĩa. |

## Sources

- [API catalog](../../../../../docs/lists/list_api.md) — API #39 request, response schema và status/business code.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-19 actor, precondition, postcondition và API mapping.
- [AC-19 activity diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — flow list discussion, tạo topic/reply và reload thread.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) — discussion self-reference, fields và API #39–#42 design-only status.
- [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — design fields/relations của discussions.
- [Checked-in Study DDL](../../../../../infra/postgres/study-server/DB.sql) — schema file trong repository; không xác nhận live schema.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — envelope và error data.
- [Course review DD #10](../10_courses_reviews/05_Data_Mapping.md) — tham khảo mapping discussion rows; semantics review không áp dụng mặc định cho AC-19.
- Current [Study router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), và [Study tests](../../../tests/) — đối chiếu runtime boundary.
- Canonical DD template: [DD_API_Template_MD](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — tám sheet theo thứ tự baseline.

## Tables read

- discussions — candidate source cho thread gốc và reply theo parent_id.
- users — candidate source cho Discussion.author và DiscussionComment.author.
- enrollments — DERIVED source cho gate principal/course/status ACTIVE.

## Tables write

- N/A — GET read-only; không có insert, update hoặc delete.

## Mục chú ý

- Catalog khai báo query{course_id?:int64, page?:int32, sort?:string}, ApiEnvelope<Page<Discussion>> và đúng các nhánh HTTP/business code 200/401/403/500.
- AC-19 mô tả Student đã đăng nhập và có quyền tham gia discussion của course; điều kiện xác định quyền chưa được chỉ rõ.
- PageMeta yêu cầu page, size, total, total_pages, trong khi request API #39 chỉ khai báo page, không có size.
- Discussion.title là required trong catalog nhưng không có cột discussions.title trong ERD/checked-in DDL.
- API #39 trả root threads kèm direct comments ACTIVE theo đề xuất DERIVED; API #42 trả cùng cấu trúc cho một root.
- DB guide xếp API #39–#42 là DESIGN_ONLY; current router/module/test scan không tìm thấy discussion implementation.

## Assumptions

- Giữ nguyên contract API #39; DD này không sửa API catalog, AC diagrams, ERD, DDL hoặc runtime.
- Dùng parent_id IS NULL để nhận diện thread gốc theo DB guide.
- Dùng status ACTIVE và enrollment ACTIVE làm visibility/access proposal DERIVED từ AC-19 và DDL defaults.
- Page mặc định 1, size cố định 20; thread mới nhất trước nếu không truyền sort, theo precedent API #10.
- Giữ Discussion.title trong logical response schema nhưng đánh dấu nguồn vật lý là chưa có; không map title từ content.
- Trạng thái là Draft — Needs Confirmation; không tạo ZIP theo workflow Study Server.

## Conflicts

- Discussion.title chưa có source vật lý.
- discussions.course_id và discussions.user_id là nullable trong checked-in DDL nhưng DB guide/ERD mô tả required; live schema chưa xác minh.
- Request có page nhưng không có size, trong khi response PageMeta yêu cầu size.
- ACTIVE enrollment/topic visibility là đề xuất DERIVED, cần xác nhận.
- Response Discussion.comments[] gồm direct child ACTIVE trong cả #39 và #42; #42 chỉ trả một root thread.

## Security note

- Contract yêu cầu Bearer JWT và Student role.
- Không nhận user ID từ query; principal thuộc token hiện hành.
- Dùng enrollment ACTIVE làm course participation predicate DERIVED; cần được xác nhận.
- Không trả raw SQL, stack trace, credential hoặc cột credential từ users.

## Performance note

- Page size 20 theo precedent API #10; comments đầy đủ trên từng thread có thể làm response lớn.
- sort đề xuất created_at_desc (default) hoặc created_at_asc; thread có id tie-break, cần xác nhận.
- Invalid sort/page và page ngoài miền cần xác nhận vì catalog không khai báo 422.
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

