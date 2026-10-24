---
title: "Định nghĩa table"
order: 7
dd_id: "92"
api_name: "Lấy notification list"
source_sheet: "table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | N/A — chưa chọn source đầy đủ; legacy/Pilot chỉ là candidate khác mô hình. |
| Logical table | Notification — logical entity theo catalog/AC-36. |
| Operation | N/A — READ-ONLY API. |
| Data Mapping step | Q1 candidate trong `05_Data_Mapping.md#step-2-đọc-notification`; chưa có SQL được duyệt. |

## Candidate read sources — không phải mutation mapping

| Source | ID/grain | Các field candidate | Field contract còn thiếu hoặc không tương thích |
|---|---|---|---|
| Legacy `notifications` | BIGSERIAL; `user_id` nullable; recipient/sender relation | `title`, `content`, `type`, `is_read`, `created_at` | Không có channels/status/read_at/scheduled_at; không chứng minh campaign-level row. |
| V1-PILOT `notifications` | UUID, learner-scoped | `title`, `body`, `read_at`, `created_at` | Khác int64/actor grain; không có Notification-level channels/status/scheduled_at. |
| V1-PILOT `notification_deliveries` | UUID notification FK, per-channel delivery row | `channel`, delivery `status` | Không map sang Notification-level fields; schema chưa được chọn cho API. |

## Update mapping

**Áp dụng khi**

- N/A — READ-ONLY API; không có UPDATE.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---|---|---|---|---|---|
| — | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không có mutation. |

## Insert mapping

**Áp dụng khi**

- N/A — READ-ONLY API; không có INSERT.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---|---|---|---|---|---|
| — | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không có mutation. |

## Delete mapping

**Áp dụng khi**

- N/A — READ-ONLY API; không có DELETE.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| — | N/A | N/A | N/A | N/A | Không có mutation. |

## Query-only note

- Không ghi SQL có thể bị hiểu là executable khi chưa xác định campaign/recipient grain, status/channel source và response cardinality.
- API #92 không thay cho API #96 delivery status và không dùng `is_read` như trạng thái gửi.
- `07_table.md` giữ nguyên vai trò read-only/N/A theo template.

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `table`
- Dimension: `A1:BA35`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `19`
- Số vùng merge: `5`

<details>
<summary>Danh sách vùng merge</summary>

- `W34:BA34`
- `W14:BA14`
- `W15:BA15`
- `W19:BA19`
- `W32:BA32`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `A2` | № |  |
| 2 | `B2` | Tên table |  |
| 3 | `B3` | SB |  |
| 3 | `S3` | Độ dài |  |
| 3 | `T3` | Dấu phẩy thập phân |  |
| 3 | `U3` | Bắt buộc |  |
| 3 | `V3` | Main key |  |
| 3 | `W3` | Nội dung setting |  |
| 4 | `B4` | № |  |
| 4 | `C4` | Item ID |  |
| 4 | `I4` | Item name |  |
| 4 | `O4` | Kiểu |  |
| 5 | `A5` | 1 |  |
| 5 | `B5` | table id |  |
| 5 | `I5` | table name |  |
| 6 | `B6` | Update |  |
| 6 | `I6` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  > 0 |  |
| 21 | `B21` | Insert |  |
| 21 | `I21` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  = 0 |  |

</details>
