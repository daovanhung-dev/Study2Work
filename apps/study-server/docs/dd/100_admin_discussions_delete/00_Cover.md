---
title: "Cover"
order: 0
dd_id: "100"
api_name: "Xóa discussion theo policy"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Cover"
format: markdown
status: "Draft — Needs Confirmation"
---

# Study2Work — API Detail Design

## Xóa discussion theo policy

| Thuộc tính | Giá trị |
|---|---|
| API ID | #100 |
| Method | `DELETE` |
| Endpoint | `/api/v1/admin/discussions/{discussion_id}` |
| Actor | Admin |
| Authentication | Bearer JWT |
| Path parameter | `discussion_id:int64!` |
| Request body/query | Không khai báo |
| Direct response | `ApiEnvelope<DeleteResult>` |
| Success | HTTP 200 `DESIGN_RESOURCE_DELETED` |
| Errors | 5 mã catalogued; xem [06_Error.md](./06_Error.md) |
| DD status | `Draft — Needs Confirmation` |
| Runtime status | `UNWIRED / NOT_FOUND` trong Study source hiện tại |

## Mục đích

Theo AC-37, Admin có thể chọn xóa nội dung sau bước xem xét và moderation. Xóa là soft delete và phải giữ audit trail. Sơ đồ không chọn cột/trạng thái vật lý, cách tạo `deleted_at`, hoặc việc append một audit event mới.

## Ranh giới bằng chứng

- Contract method/path, role, input, response, status và error codes lấy trực tiếp từ catalog #100.
- `DeleteResult` có `id`, `status:"deleted"`, `deleted_at`; cách lưu/đọc thời gian chưa được xác định.
- Legacy `discussions.status` và `updated_at` là candidate hiện có, không phải mapping được duyệt. Không thêm cột hoặc hard-delete row.
- Audit phải được giữ theo diagram; bảng audit pilot dùng UUID và chưa có mapping sang Discussion BIGINT.
- Xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) trước implementation.
---
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
