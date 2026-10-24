---
title: "Cover"
order: 0
dd_id: "103"
api_name: "Xuất báo cáo tác động cộng đồng"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Cover"
format: markdown
status: "Draft — Needs Confirmation"
---

# Study2Work — API Detail Design

## Xuất báo cáo tác động cộng đồng

| Thuộc tính | Giá trị |
|---|---|
| API ID | #103 |
| Method | GET |
| Endpoint | /api/v1/admin/reports/community-impact/export |
| Actor | Admin |
| Authentication | Bearer JWT |
| Query | filters?:string, format?:string |
| Request body | Không có |
| Contract response theo endpoint row | ApiEnvelope<Report> |
| HTTP success | 202 DESIGN_OPERATION_ACCEPTED |
| Errors | 401, 403, 503, 500; xem 06_Error.md |
| DD status | Draft — Needs Confirmation |
| Runtime status | UNWIRED / NOT_FOUND trong Study source hiện tại |

## Mục đích

Cho phép Admin yêu cầu xuất báo cáo tác động cộng đồng theo AC-38. Sơ đồ mô tả export CSV/XLSX/PDF hoặc job, tùy cách generate file; nếu file được tạo phía server thì lưu tạm. UI có thể tải file hoặc theo dõi Operation qua API #18.

## Ranh giới bằng chứng

- Endpoint row trực tiếp khai báo response Report tại HTTP 202.
- Operation tracking paragraph trong cùng catalog trực tiếp nói API #103 trả Operation; đây là DISCREPANCY, chưa tự chọn contract.
- Recommendation DERIVED cho flow async: nhận Operation rồi poll API #18; kết quả file có thể dùng ExportAsset. Các field/lifecycle/storage cần được duyệt.
- Không có route/export worker/Operation store trong Study runtime hiện tại.
- Xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md) và [06_Error.md](./06_Error.md) trước khi chuyển DD sang Final hoặc triển khai.

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
