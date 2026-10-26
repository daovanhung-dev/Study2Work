---
title: "Lịch sử update"
order: 1
dd_id: "65"
api_name: "Lấy tiến độ toàn lớp"
source_sheet: "Lịch sử"
status: "Draft — Needs Confirmation"
---

# Lịch sử cập nhật

| Phiên bản | Ngày | Người cập nhật | Nội dung | Trạng thái |
|---|---|---|---|---|
| 1.0 | 2026-10-24 | Codex | Tạo DD theo catalog #65 và AC-26; tách contract trực tiếp khỏi phương án tổng hợp progress được suy luận. | Draft — Needs Confirmation |
| 1.1 | 2026-10-25 | Codex | Wire API #65 theo fallback progress roster DERIVED; bổ sung current source, tests, formula/latest-row/paging details; giữ discrepancy Page<Course> và DD Draft. | Draft — Needs Confirmation |

## Nguồn thay đổi

- [API catalog](../../../../../docs/lists/list_api.md) — endpoint, auth, input, response và business code.
- [AC-26 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [activity diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — vị trí #65 trong luồng theo dõi tiến độ.
- [Worklog tạo DD #65](../../../../../.agents/worklog/2026-10-24/create-study-api65-dd.md) — plan, ma trận truy vết và ranh giới evidence.
- [Worklog triển khai API #65](../../../../../.agents/worklog/2026-10-25/implement-api65-mentor-course-progress.md) — source trace, quyết định DERIVED, implementation và local verification.

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
