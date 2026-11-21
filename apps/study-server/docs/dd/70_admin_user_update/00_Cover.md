---
title: "Cover"
order: 0
dd_id: "70"
api_name: "Cập nhật thông tin/role Conditional"
source_sheet: "Cover"
status: "Draft — Needs Confirmation"
---

# Study2Work — API Detail Design

## Thông tin tài liệu

| Thuộc tính | Giá trị |
|---|---|
| Project/System | Study2Work — Study Server |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-31 |
| Loại tài liệu | API Detail Design |
| API ID | 70 |
| API name | Cập nhật thông tin/role Conditional |
| HTTP method | PUT |
| Endpoint | /api/v1/admin/users/{user_id} |
| Version | 1.1 |
| Status | Draft — Needs Confirmation |
| Created by | Codex |
| Reviewed by | Chờ xác nhận |
| Approved by | Chờ xác nhận |
| Created date | 2026-10-24 |
| Updated date | 2026-10-25 |

## Tên hiển thị

~~~text
PUT /api/v1/admin/users/{user_id} — Cập nhật thông tin/role
~~~

## Phạm vi và trạng thái

Catalog và AC-31 xác nhận Admin cập nhật user/profile bằng API #70, trả `ApiEnvelope<UserProfile>`. Input trực tiếp chỉ nêu `path{user_id:int64!}`; request body không được đặc tả. Runtime hiện dùng fallback `DERIVED`: PUT thay thế đủ `full_name`, `phone`, `avatar_url`, `role`; role chỉ nhận các nhãn đang dùng trong Study (`STUDENT`, `MENTOR`, `ADMIN`).

Study Server hiện có route, module và focused HTTP tests cho API #70. Module yêu cầu JWT role `ADMIN`, chuẩn hóa profile theo API #14, cập nhật checked-in legacy BIGINT `users` và trả safe `UserProfile`. Body/role/path mapping là fallback `DERIVED`; live schema, permission policy, audit/PII và token effect chưa xác minh. API #71 phụ trách đổi status; API #70 không thêm status, delete, audit hoặc revoke session.

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
