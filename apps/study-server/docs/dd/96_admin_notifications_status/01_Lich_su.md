---
title: "Lịch sử update"
order: 1
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Lịch sử"
format: markdown
dd_id: "96"
api_name: "Xem trạng thái delivery notification Admin"
status: "Draft — Needs Confirmation"
---

# Lịch sử update

| Version | Ngày | Người cập nhật | Nội dung | Trạng thái |
|---|---|---|---|---|
| 0.1 | 2026-10-24 | Study2Work docs | Tạo DD từ catalog #96 và AC-36; giữ `ApiEnvelope<Notification>`; ghi delivery aggregate, Admin schema, permission và enum còn thiếu nguồn. | Draft — Needs Confirmation |
| 0.2 | 2026-10-26 | Study2Work coding | Wire GET bằng một aggregate read-only query; tái dùng Notification projection và QUEUED/FAILED/SENT precedence của #92; invalid ID hoặc không có delivery status trả 404 theo fallback DERIVED. | Draft — Needs Confirmation |

## Ghi chú

DD vẫn là `Draft — Needs Confirmation`. Source/test local của #96 hiện wired; fallback schema, status precedence, empty-delivery 404 và role-only ADMIN authorization vẫn `DERIVED` hoặc `SOURCE_REQUIRED`. Không coi local test là bằng chứng live schema/deployment.
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Lịch sử`
- Dimension: `A1:F19`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `13`
- Số vùng merge: `17`

<details>
<summary>Danh sách vùng merge</summary>

- `E14:F14`
- `E15:F15`
- `E16:F16`
- `E17:F17`
- `E19:F19`
- `E18:F18`
- `E10:F10`
- `E11:F11`
- `E12:F12`
- `E13:F13`
- `E3:F3`
- `E4:F4`
- `E9:F9`
- `E7:F7`
- `E8:F8`
- `E5:F5`
- `E6:F6`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | Lịch sử update |  |
| 1 | `E1` | Ngày tạo |  |
| 1 | `F1` | Ngày update cuối cùng |  |
| 2 | `E2` | yyyy/mm/dd |  |
| 2 | `F2` | yyyy/mm/dd |  |
| 3 | `A3` | Version |  |
| 3 | `B3` | Ngày update |  |
| 3 | `C3` | Người update |  |
| 3 | `D3` | Nội dung update |  |
| 3 | `E3` | Remarks |  |
| 4 | `A4` | 1.0 |  |
| 4 | `B4` | yyyy/mm/dd |  |
| 4 | `D4` | Create new |  |

</details>

