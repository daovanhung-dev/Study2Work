---
title: "Lịch sử update"
order: 1
dd_id: "66"
api_name: "Lấy analytics tổng hợp"
source_sheet: "Lịch sử"
status: "Draft — Needs Confirmation"
---

# Lịch sử cập nhật

| Phiên bản | Ngày | Người cập nhật | Nội dung | Trạng thái |
|---|---|---|---|---|
| 1.0 | 2026-10-24 | Codex | Tạo DD theo catalog #66 và AC-26; ghi nhận response Page<Course> chưa có analytics fields. | Draft — Needs Confirmation |
| 1.1 | 2026-10-25 | Codex | Wire API #66 với activity proxy từ lesson_progress.last_accessed_at; ghi rõ không phải event count và giữ discrepancy response. | Draft — Needs Confirmation |

## Nguồn thay đổi

- [API catalog](../../../../../docs/lists/list_api.md) — method/path, actor, input, response và error codes.
- [AC-26 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [activity diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — vị trí #66 giữa tổng hợp #65 và drill-down #67.
- [DD API #65](../65_mentor_course_progress/02_Overview.md) — boundary enrollment/progress, course access gaps và response mismatch.
- [Worklog tạo DD #66](../../../../../.agents/worklog/2026-10-24/create-study-api66-dd.md) — DD ban đầu và evidence boundary.
- [Worklog implement API #66](../../../../../.agents/worklog/2026-10-25/implement-api66-mentor-course-analytics.md) — source reconciliation, fallback, implementation và verification.

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
