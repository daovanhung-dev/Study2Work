---
title: "Định nghĩa table"
order: 7
dd_id: "103"
api_name: "Xuất báo cáo tác động cộng đồng"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | SOURCE_REQUIRED — chưa có Study Operation/export table được duyệt |
| Logical resource | Operation; ExportAsset |
| Operation | Async acceptance; physical store/queue chưa xác định |
| Data Mapping step | Step 4 — accept job/generate artifact; Step 6 — poll API #18 |

## Ranh giới nguồn vật lý\n\nLuồng side effect được mô tả tại [05_Data_Mapping.md](./05_Data_Mapping.md#step-4-accept-job-và-tạo-artifact); các quyết định còn mở xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

- API #103 có logical operation và side effect tạo file tạm có điều kiện theo AC-38.
- Legacy Study DB.sql/ERD không định nghĩa bảng Operation hoặc export của Study.
- V1-PILOT file_objects là candidate metadata cho file nhưng chưa có purpose/mapping export được duyệt.
- V1-PILOT report_snapshots là aggregate snapshot, không phải queue hoặc file artifact.
- Không tạo mapping cột SELECT/INSERT/UPDATE/DELETE khi chưa có physical schema contract.
- Mapping là SOURCE_REQUIRED; điều này không có nghĩa endpoint không có side effect.

## Các field ứng viên của Logical Operation

| No | Field | Logical type | Physical column/table | Source or mapping | Status |
|---:|---|---|---|---|---|
| 1 | id | uuid | SOURCE_REQUIRED | Operation schema | Nguồn cấp ID vật lý và xung đột kiểu path API #18 chưa được giải quyết |
| 2 | kind | OperationKind | SOURCE_REQUIRED | Operation schema | Giá trị enum/kind export chưa được quy định |
| 3 | status | OperationStatus | SOURCE_REQUIRED | Operation schema | Trạng thái ban đầu và lifecycle chưa được quy định |
| 4 | owner_id | int64 | SOURCE_REQUIRED | Operation schema | Mapping principal Admin chưa được quy định |
| 5 | submitted_at | date-time | SOURCE_REQUIRED | Operation schema | Clock/source chưa được quy định |
| 6 | updated_at | date-time | SOURCE_REQUIRED | Operation schema | Nguồn state transition chưa được quy định |
| 7 | completed_at | date-time optional | SOURCE_REQUIRED | Operation schema | Completion semantics chưa được quy định |
| 8 | result | Payment optional in current reusable schema | SOURCE_REQUIRED | Operation schema | Mâu thuẫn với candidate export artifact |

## Field candidate của Logical ExportAsset

| No | Field | Logical type | Physical source | Status |
|---:|---|---|---|---|
| 1 | download_url | uri | Temporary file storage candidate | Cấp URL/authorization SOURCE_REQUIRED |
| 2 | format | ExportFormat | Requested format candidate | Enum/default SOURCE_REQUIRED |
| 3 | expires_at | date-time | Temporary file lifecycle candidate | TTL/cleanup SOURCE_REQUIRED |

## Mapping Mutation

**Áp dụng khi**

API GET có logical async job/file side effects trong AC-38, nhưng physical target chưa được xác định. Bảng dưới đây không giả lập physical schema.

| ID | Logical operation | Target | Mapping |
|---|---|---|---|
| M1 | Accept job | Operation/queue | SOURCE_REQUIRED; không có approved Study table/queue |
| M2 | Store file | File Storage | Conditional server-side generation; provider/metadata/TTL SOURCE_REQUIRED |
| M3 | Delete expired file | Cleanup worker | Không thuộc endpoint contract trực tiếp; lifecycle SOURCE_REQUIRED |

## Mapping đọc

| Logical source | Query mapping | Status |
|---|---|---|
| Community report | Reuse #102 report logic/filter | SOURCE_REQUIRED; #102 service/query not implemented |
| Operation status | GET API #18 by operation_id | Direct API reference; ID/auth/lifecycle gaps remain |

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
