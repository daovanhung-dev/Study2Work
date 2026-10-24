---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
dd_id: "44"
api_name: "Đánh dấu một thông báo đã đọc"
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | 44 |
| API name | Đánh dấu một thông báo đã đọc |
| Module | STUDENT / LEARNING & INTERACTION |
| Method | `PATCH` |
| Endpoint | `/api/v1/notifications/{notification_id}/read` |
| Purpose | Đánh dấu notification thuộc `Student` hiện tại là đã đọc. |
| Consumer/Actor | `Student` |
| Authentication | `Bearer` `JWT` |
| `Authorization` | Role `Student`; principal lấy từ `JWT`, không lấy user ID từ request. |
| Basis | API catalog và nhánh ONE của AC-20; physical update là `DERIVED` candidate. |
| Status | Draft — Needs Confirmation |
| Current runtime state | `UNWIRED` / `NOT_FOUND` — không tìm thấy route/module/query/test API #44 trong Study source hiện tại. |
| Transaction | Một câu `UPDATE` atomic trong transaction do caller/use-case sở hữu — `DERIVED`. |
| Side effects | Đổi read flag của đúng notification thuộc principal; không gửi notification ra provider. |

## Sources

- [API catalog](../../../../../docs/lists/list_api.md) — API #43–#45, `Notification`/`Page` schemas, `status` và error contract.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition, postcondition và nhóm AC-20.
- [AC-20 activity diagram](../../diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) — cạnh ONE, API #44, `UPDATE` `read_at` và cập nhật UI.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) — mục `notifications`, quan hệ và method API #44–#45.
- [DB ERD](../../diagrams/DB_UNICA_ERD.drawio) — cột `notifications` và quan hệ users-to-`notifications`.
- [Checked-in Study DDL](../../../../../infra/postgres/study-server/DB.sql) — physical definition; không chứng minh live schema.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — envelope, `X-Trace-Id`, lỗi và idempotency guideline.
- Current [Study router](../../../app/api/v1.py), [Student auth helper](../../../app/utils/auth.py) và [response helper](../../../app/core/responses.py) — current boundary; #44 chưa được wire.
- [API #43 response contract](../43_users_me_notifications/04_Response.md) và [open questions #43](../43_users_me_notifications/OPEN_QUESTIONS.md) — `Notification` gaps và read-state conflict.
- [API #42 singleton Page precedent](../42_discussions_detail/04_Response.md) — response `Page` một item được ghi `DERIVED`.
- [Canonical DD Markdown template](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — tám sheet; template hashes ghi tại [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md).

## Tables read

- `notifications` — candidate target row và response projection từ checked-in DDL.
- `NotificationRecipient` — logical recipient entity trong diagram; không có physical table trong DB guide/ERD/DDL.
- users — quan hệ FK của `notifications`.`user_id`; API candidate lấy user ID từ `JWT`, không query riêng.

## Tables write

- `notifications` — candidate update `is_read`=`TRUE` cho row id và `user_id` khớp.
- Không ghi `read_at` vì DDL không có cột đó.

## Mục chú ý

- Giữ nguyên contract API #44: `PATCH` path notification ID, không body/query; `success`/error set theo catalog.
- `UPDATE` `notifications` SET `is_read`=`TRUE` là candidate physical fallback cho ý nghĩa đã đọc; đây là `DERIVED`, khác logical diagram `NotificationRecipient`.`read_at`.
- Query phải kèm `user_id`=:`principal_id`; không cập nhật row của `Student` khác.
- Không dùng `notifications`.`user_id` IS NULL cho read theo từng `Student` vì chưa có recipient/read-state model.
- Không đổi type thành `channels`, không đổi `is_read` thành `NotificationStatus`, không dựng `read_at` từ boolean.
- Response `Page<Notification>` một item là đề xuất `DERIVED` theo API #42; cần chốt cùng API #45.
- Không thêm header `Idempotency-Key` vào request vì catalog chỉ khai báo path; guideline applicability cần xác nhận.

## Assumptions

- Path `notification_id` phải parse thành `int64`; input không parse/range vượt `int64` dùng 422 code đã khai báo.
- ID `int64` hợp lệ nhưng không có row khớp principal trả 404; gồm row không tồn tại, thuộc user khác hoặc broadcast row `user_id` IS NULL.
- Gán `is_read`=`TRUE` lặp lại giữ nguyên trạng thái; mutation candidate idempotent về state.
- Khi thành công, `data` là `Page` singleton với `page`=1, `size`=1, `total`=1, `total_pages`=1 — `DERIVED`.
- Những đề xuất này chưa được phê duyệt; source gap được ghi trong OPEN_QUESTIONS.md.

## Conflicts

- AC-20 yêu cầu `NotificationRecipient`.`read_at`; DB guide/ERD/DDL chỉ định `notifications`.`user_id` nullable và `is_read`.
- Catalog `Notification` bắt buộc `channels`/`status`, nhưng DDL chỉ có type/`is_read`; enum values chưa được định nghĩa.
- Catalog response là `Page<Notification>` nhưng request không có `page`; singleton `page` là `DERIVED`.
- API guideline nhắc `Idempotency-Key` cho retryable mutation nhưng API #44 catalog không khai báo header; state update candidate idempotent.
- Expected error envelope `data`:null khác current helper fallback `data`:{}.
- API #43 lọc unread theo `is_read` nhưng `Notification` response không expose `is_read`; mapping read/unread tới `status`/`read_at` chưa có nguồn.

## Security note

- Chỉ dùng `principal_id` do `Student` `JWT` helper trả về.
- Owner condition `notifications`.`user_id`=:`principal_id` bắt buộc; không lấy `user_id` từ path/body/query.
- Với ID không thuộc principal, trả cùng 404 như row không tồn tại để không tiết lộ notification của user khác — `DERIVED` theo error set.
- Không log/echo `Bearer` token, raw SQL, stack trace hoặc database exception.

## Performance note

- Cập nhật bằng PK id và owner predicate trong một câu `UPDATE` ... `RETURNING`; không cần SELECT trước candidate update.
- Không thêm index/schema vì DDL đã định nghĩa PK và task chỉ tạo DD.
- Live database/query plan chưa được kiểm tra.
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
