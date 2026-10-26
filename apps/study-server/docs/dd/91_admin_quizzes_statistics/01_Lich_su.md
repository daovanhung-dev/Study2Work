---
title: "Lịch sử thay đổi"
order: 1
dd_id: "91"
api_name: "Xem thống kê quiz"
source_sheet: "Lịch sử"
format: markdown
status: "Draft — Needs Confirmation"
---

# Lịch sử thay đổi

| Phiên bản | Ngày | Người cập nhật | Nội dung thay đổi | Trạng thái |
|---|---|---|---|---|
| 0.1 | 2026-10-24 | Codex | Tạo DD theo catalog #91, AC-35/AC-16, DB design candidate và macro-review #87–#91. | Draft — Needs Confirmation |
| 0.2 | 2026-10-26 | Codex | Ghi nhận API #91 local runtime dùng `QuizStatistics` fallback DERIVED, guard ADMIN, aggregate SQL, errors và test; giữ conflict catalog/diagram mở. | Draft — Needs Confirmation |

## Quy tắc cập nhật

- Contract trực tiếp lấy từ [API catalog](../../../../../docs/lists/list_api.md).
- Mọi thay đổi về metric, response schema, tombstone hoặc quyền truy cập phải ghi rõ nguồn và trạng thái DIRECT/DERIVED/SOURCE_REQUIRED.
- Chỉ chuyển sang Approved/Final sau khi chốt các câu hỏi trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
---
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
