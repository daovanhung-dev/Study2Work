---
title: "Cover"
order: 0
dd_id: "94"
api_name: "Admin cập nhật notification"
source_sheet: "Cover"
status: "Draft — Needs Confirmation"
---

# Study2Work — API Detail Design

## Thông tin tài liệu

| Thuộc tính | Giá trị |
|---|---|
| API ID | #94 |
| Tên API | Admin cập nhật notification |
| Nhóm nghiệp vụ | AC-36 — Admin quản lý notification |
| Phương thức | PUT |
| Endpoint | /api/v1/admin/notifications/{notification_id} |
| Trạng thái DD | Draft — Needs Confirmation |
| Trạng thái source | Wired; local fake-DB HTTP tests pass; live schema/deployment unverified |
| Phạm vi | Contract trực tiếp và fallback triển khai DERIVED trên legacy BIGINT candidate |

## Tên hiển thị

**Admin cập nhật title/content của notification còn QUEUED**

Catalog và AC-36 chỉ xác định path, response, errors và ý định UPDATE. Runtime dùng fallback hẹp: body strict `{title, content}`, chỉ sửa notification có ít nhất một delivery và mọi delivery đang `QUEUED`. Fallback này dựa trên các cột legacy hiện có; chưa được owner duyệt và không biểu thị trạng thái Draft/Scheduled.

## Tài liệu liên quan

- [API catalog](../../../../../docs/lists/list_api.md)
- [AC-36 diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [DD #92 — Admin notification list](../92_admin_notifications_list/02_Overview.md)
- [DD #93 — Admin tạo/phát notification](../93_admin_notifications_create/02_Overview.md)
- [AC-36 macro-review](../96_admin_notifications_status/AC-36_MACRO_REVIEW.md)
- [Study declared routes](../../../../../.agents/server-study/apis/declared-routes.md)

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Cover`
- Dimension: `A1:AN46`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `1`
- Số vùng merge: `40`

<details>
<summary>Danh sách vùng merge</summary>

- `O42:R42`
- `S42:Z42`
- `AA42:AD42`
- `AE42:AN42`
- `O43:R46`
- `S43:V46`
- `W43:Z46`
- `AA43:AD46`
- `AE43:AN46`
- `O40:R40`
- `S40:Z40`
- `AA40:AN40`
- `O41:R41`
- `S41:Z41`
- `AA41:AN41`
- `O38:R38`
- `S38:Z38`
- `AA38:AN38`
- `O39:R39`
- `S39:Z39`
- `AA39:AN39`
- `O36:R36`
- `S36:Z36`
- `AA36:AN36`
- `O37:R37`
- `S37:Z37`
- `AA37:AN37`
- `O34:R34`
- `S34:Z34`
- `AA34:AN34`
- `O35:R35`
- `S35:Z35`
- `AA35:AN35`
- `G14:AG20`
- `O32:R32`
- `S32:Z32`
- `AA32:AN32`
- `O33:R33`
- `S33:Z33`
- `AA33:AN33`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 14 | `G14` | Tên Project　API design<br>Tên API |  |

</details>
