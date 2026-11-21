---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "42"
api_name: "Tải lại thread thảo luận"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 42 |
| Module | Student / Learning & Interaction |
| Method | GET |
| Endpoint | /api/v1/discussions/{discussion_id} |
| Purpose | Đọc lại một topic gốc cùng các comment để hiển thị thread mới nhất sau thao tác tạo topic/reply. |
| Consumer/Actor | Student |
| Authentication | Bearer JWT |
| Authorization | DERIVED gate thống nhất với API #41: Student có enrollment ACTIVE trong course của topic; topic phải ACTIVE. Cần xác nhận policy. |
| Basis | DIRECT — approved catalog và AC-19; truy vấn/order/page là DERIVED |
| Status | Draft — Needs Confirmation; design-only, runtime UNWIRED / NOT_FOUND. |
| Transaction | N/A — GET chỉ đọc. |
| Side effects | Không có mutation. Không lưu counter; DiscussionComment[] là danh sách comment trực tiếp của topic. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — APPROVED_DESIGN_CONTRACT; API #42, Discussion, DiscussionComment, Page, PageMeta.
- [AC API index](../../../docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-19 precondition/postcondition và trình tự bốn API.
- [AC-19 activity diagram](../../../docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — sau API #40/#41, API #42 đọc topic + comments rồi hiển thị thread mới nhất.
- [Discussion DB guide](../../../docs/diagrams/DB_UNICA_TABLES.md) và [DB ERD](../../../docs/diagrams/DB_UNICA_ERD.drawio) — discussion root/comment qua self-reference parent_id; design-only.
- [Checked-in DB DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate physical columns, ACTIVE defaults, nullable FK; không xác nhận live schema.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — envelope, data=null cho error và trace ID.
- [Study auth helper](../../../app/utils/auth.py), [Study API router](../../../app/api/v1.py), API #39 [DD](../39_discussions/00_Cover.md), API #40 [DD](../40_discussions_create/00_Cover.md), API #41 [DD](../41_discussions_comment/00_Cover.md) — auth precedent, current runtime boundary và luồng liên quan.

## Tables read

- discussions — candidate topic gốc và comment rows trực tiếp.
- users — candidate UserSummary cho topic/comment authors.
- enrollments — DERIVED access gate: principal có enrollment ACTIVE cùng course_id.

## Tables write

- N/A — API #42 là read-only.

## Mục chú ý

- AC-19 xác định response là ApiEnvelope<Page<Discussion>> và bước xử lý là đọc topic cùng comments.
- DERIVED: discussion_id phải là topic gốc (parent_id IS NULL); API #42 đọc các child row có parent_id trỏ tới topic.
- DERIVED: chỉ hiển thị topic/comment ACTIVE; topic phải thuộc course có enrollment ACTIVE của Student.
- DERIVED: comments xếp created_at tăng dần, sau đó id tăng dần để thứ tự ổn định; thread hiển thị comment cũ trước, mới sau.
- DERIVED: một thread được trả trong Page có page=1, size=1, total=1, total_pages=1; API #39 vẫn là endpoint phân trang danh sách nhiều thread.
- Không có cột counter trong DB guide/ERD/DDL và schema response không có count field. Không ghi hoặc trả persistent counter.
- Discussion.title là field bắt buộc của schema reusable nhưng không tồn tại trong DB guide/ERD/DDL. Không tạo title từ content.

## Assumptions

- ACTIVE enrollment và ACTIVE discussion là gate đơn giản suy ra từ AC-19 precondition và DDL defaults; đây là đề xuất, chưa phải rule được phê duyệt.
- Topic root và child comments được truy vấn trong cùng course; không hỗ trợ nested reply trong response này theo mô hình API #41, trừ khi contract được điều chỉnh.
- Comment status ACTIVE được xem là visible; comment status khác bị bỏ khỏi comments array.
- Với topic không tìm thấy hoặc ID trỏ tới comment, trả 404. Không được thêm 422 vì catalog API #42 không khai báo code đó.
- Author lookup dùng users.full_name và optional avatar_url; nếu FK/profile bắt buộc bị thiếu, coi là data integrity error và trả 500.
- Read path không thay đổi updated_at hoặc bất kỳ row nào.

## Conflicts

- Required Discussion.title chưa có physical source.
- DB guide/ERD xem course_id/user_id required, trong khi DDL cho phép NULL; live schema chưa được kiểm tra.
- DiscussionStatus enum members và trạng thái visible chưa được định nghĩa đầy đủ; ACTIVE filter là DERIVED.
- Contract dùng Page<Discussion> cho detail thread nhưng không định nghĩa page metadata; one-item page là DERIVED.
- Path parse failure không có 422 trong catalog; mapping với framework default cần được quyết định.

## Security note

- Chỉ Student Bearer JWT được phép gọi theo catalog; user_id lấy từ principal.
- Kiểm tra enrollment ACTIVE cho course của topic; không coi việc biết discussion_id là đủ quyền.
- API #42 chưa wired; current Student auth helper là precedent source, không chứng minh API này runtime-verified.

## Performance note

- Q1 đọc một topic; Q2 đọc toàn bộ comment trực tiếp ACTIVE của topic và author profiles.
- Không có phân trang riêng cho comments; payload tăng theo số comment. Contract hiện không có comment cursor/limit.
- Không có index hoặc benchmark được xác nhận cho parent_id/status/created_at. Live schema chưa được kiểm tra.
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


