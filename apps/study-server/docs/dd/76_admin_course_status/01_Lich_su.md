---
title: "Lịch sử update"
order: 1
dd_id: "76"
api_name: "Thay đổi trạng thái khóa học Admin"
source_sheet: "Lịch sử"
status: "Draft — Needs Confirmation"
---

# Lịch sử update

## Metadata

| Thuộc tính | Giá trị |
|---|---|
| API ID | #76 |
| Tên API | Thay đổi trạng thái khóa học Admin |
| Endpoint | PATCH /api/v1/admin/courses/{course_id}/status |
| Tài liệu | 76_admin_course_status |
| Trạng thái | Draft — Needs Confirmation |

## Lịch sử thay đổi

| Version | Ngày | Nội dung | Người cập nhật |
|---|---|---|---|
| 0.1 | 2026-10-24 | Tạo DD từ API catalog và AC-32; body status, casing, audit mapping và transition policy được đánh dấu cần xác nhận. | Codex |
| 0.2 | 2026-10-26 | Implement API #76 với fallback DERIVED cho body/status, bảng audit legacy BIGINT, transaction và singleton Page; giữ Draft, permission/schema live còn mở. | Codex |

## Nguồn chính

- API catalog #76 và reusable schemas.
- AC-32 index/activity diagram.
- API #71 status DD và API #73–#75 trong cùng luồng quản trị course.
- Current Study source, legacy DB artifact, API #76 migration candidate và V1-PILOT schema; không nguồn nào chứng minh live schema.
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
