---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "41"
api_name: "Thêm bình luận/trả lời"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 41 |
| Module | Student / Learning & Interaction |
| Method | POST |
| Endpoint | /api/v1/discussions/{discussion_id}/comments |
| Purpose | Thêm reply vào một thread thảo luận. |
| Consumer/Actor | Student |
| Authentication | Bearer JWT |
| Authorization | Role Student; DERIVED gate: có enrollment ACTIVE ở course của topic và topic ACTIVE. Trạng thái/policy này cần xác nhận. |
| Basis | DIRECT — approved catalog và AC-19; một số mapping được đánh dấu DERIVED |
| Status | Draft — Needs Confirmation; design-only, runtime UNWIRED / NOT_FOUND. |
| Transaction | DERIVED — tạo một row reply theo một thao tác nguyên tử; chưa có runtime hay transaction contract. |
| Side effects | AC-19 chỉ rõ INSERT Comment + update counters. Candidate physical write là một child row trong discussions; không có cột counter trong ERD/DDL để cập nhật. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — APPROVED_DESIGN_CONTRACT; API #41, Discussion, DiscussionComment, Page, PageMeta.
- [AC API index](../../../docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition, postcondition và API mapping của AC-19.
- [AC-19 activity diagram](../../../docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — nhánh REPLY, POST API #41, INSERT Comment + update counters, rồi GET API #42.
- [Discussion DB guide](../../../docs/diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../../docs/diagrams/DB_UNICA_ERD.drawio) — self-reference parent_id; design-only.
- [Checked-in DB DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate physical columns/defaults; không xác nhận live schema.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — envelope, trace ID và error response conventions.
- [Study auth helper](../../../app/utils/auth.py), [Study API router](../../../app/api/v1.py), API #39 [DD](../39_discussions/00_Cover.md), API #40 [DD](../40_discussions_create/00_Cover.md) — current auth boundary, runtime status và adjacent contract gaps.

## Tables read

- discussions — lấy topic cha và thêm một child row; mapping design-only.
- users — candidate author projection cho DiscussionComment.author; JWT chỉ cung cấp identity/roles theo current helper.
- enrollments — DERIVED access candidate: user hiện tại có enrollment ACTIVE trong course của topic; status/predicate chưa được AC-19/API #41 duyệt.

## Tables write

- discussions — candidate insert reply; parent_id trỏ về topic.
- Không có cột counter trong bảng hiện được mô tả; không tạo cột hoặc update giả định.

## Mục chú ý

- Catalog/AC-19 yêu cầu content:int64!; reusable Discussion.content và DiscussionComment.content là string, còn DDL khai báo discussions.content TEXT. Chưa có conversion rule.
- discussion_id được suy ra là ID topic gốc; mỗi reply lưu thành child với parent_id = discussion_id. Đây là DERIVED để khớp flow API #42 đọc topic cùng comments; cần xác nhận có cho reply lồng nhau hay không.
- course_id của reply được suy ra từ topic cha để giữ reply trong cùng course. DDL cho phép NULL nhưng DB guide/ERD mô tả quan hệ bắt buộc.
- Server timestamp cho created_at/updated_at và status mặc định ACTIVE là candidate đơn giản; DDL có timestamp NOT NULL và status default nhưng không xác nhận live behavior/enum.
- API #41 giữ response contract ApiEnvelope<Page<Discussion>>; mapping một updated thread vào page và metadata chưa có định nghĩa được duyệt. Activity diagram vẫn yêu cầu client gọi API #42 để tải lại thread.

## Assumptions

- Các suy luận được ghi DERIVED và chưa phải quyết định được duyệt: một reply là row con trực tiếp của topic; nó kế thừa course; identity lấy từ Student JWT; timestamp lấy từ server clock.
- content:int64 có thể được tuần tự hóa thành chuỗi thập phân để lưu TEXT, nhưng đây chỉ là đề xuất mapping và phải được xác nhận trước khi coi là contract.
- “Update counters” không được chuyển thành thao tác ghi database khi chưa có counter field. Nếu giao diện cần số đếm, tính từ child rows khi đọc là hướng đề xuất, không phải DB operation được duyệt.
- Giữ nguyên success/error codes và response schema trong catalog.

## Conflicts

- Input content:int64 không khớp reusable schema content:string hoặc physical TEXT.
- Access predicate theo course, visibility của topic và trạng thái nào được phép reply chưa được định nghĩa.
- Diagram nhắc update counters nhưng DB guide/ERD/DDL không có cột counter hoặc response field counter.
- Page<Discussion> không chỉ rõ page semantics/updated-thread representation; API #42 là bước reload.
- course_id/user_id là required trong DB guide/ERD nhưng nullable trong checked-in DDL.

## Security note

- Chỉ Student Bearer JWT được phép gọi theo catalog; lấy user_id từ principal, không từ request body.
- API #41 chưa wired; current Student guard chỉ là source precedent, không phải bằng chứng API #41 chạy.
- Kiểm tra quyền tham gia discussion của course trước write. Predicate đề xuất DERIVED là enrollment ACTIVE và topic ACTIVE; cần xác nhận trước khi coi là chính sách được duyệt.

## Performance note

- Không có runtime query, benchmark hoặc target cho API #41.
- Candidate flow đọc topic cha, ghi một child row, rồi client gọi API #42 tải thread. Counter aggregation nếu cần chỉ là đề xuất cho read path; chưa có query/performance evidence.
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

