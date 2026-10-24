---
title: "Cover"
order: 0
dd_id: "95"
api_name: "Admin xóa hoặc hủy notification"
source_sheet: "Cover"
status: "Draft — Needs Confirmation"
---

# Study2Work — API Detail Design

## Thông tin tài liệu

| Thuộc tính | Giá trị |
|---|---|
| API ID | #95 |
| Tên API | Admin xóa hoặc hủy notification |
| Nhóm nghiệp vụ | AC-36 — Admin quản lý notification |
| Phương thức | DELETE |
| Endpoint | /api/v1/admin/notifications/{notification_id} |
| Trạng thái DD | Draft — Needs Confirmation |
| Trạng thái source | UNWIRED / NOT_FOUND trong Study server |
| Phạm vi | Contract, lifecycle proposal và data-mapping boundary; không thay đổi runtime |

## Tên hiển thị

**Xóa draft hoặc hủy scheduled notification theo policy**

Catalog yêu cầu DELETE draft hoặc cancel nếu policy cho phép. Diagram chỉ mô tả DELETE/mark cancelled. DD này giữ response DeleteResult trực tiếp và ghi rõ các policy nhánh là DERIVED, chưa phải runtime contract.

## Tài liệu liên quan

- [API catalog](../../../../../docs/lists/list_api.md)
- [AC-36 diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [DD #92 — Admin notification list](../92_admin_notifications_list/02_Overview.md)
- [DD #93 — Admin tạo/phát notification](../93_admin_notifications_create/02_Overview.md)
- [DD #94 — Admin cập nhật notification](../94_admin_notifications_update/02_Overview.md)
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
