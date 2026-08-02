---
title: "security_audit_events INSERT"
order: 10
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "API-IAM-018"
status: "NEEDS USER DECISION — Draft"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `TBL-IAM-017` |
| Logical table | `security_audit_events` |
| Operation | `INSERT` |
| Data Mapping step | `05_Data_Mapping.md#3-insertupdate-thong-tin` |

## Update mapping

**Áp dụng khi**

- `N/A — Operation không phải UPDATE.`

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| 1 | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N` |  | `N/A` | `N/A` | `N/A` | Operation không áp dụng |

## Insert mapping

**Áp dụng khi**

- `Theo Data Mapping và owner/version predicate.`

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| 1 | `id` | `id` | `uuid NOT NULL` | `N/A` | `N/A` | `Y` | `●` | `Generated UUID v7` | `Generated UUID v7` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 2 | `occurred_at` | `occurred_at` | `timestamptz NOT NULL DEFAULT now()` | `N/A` | `N/A` | `Y` | `` | `current_timestamp` | `current_timestamp` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 3 | `actor_id` | `actor_id` | `uuid NULL` | `N/A` | `N/A` | `N` | `` | `token/session actor hoặc NULL cho anonymous` | `token/session actor hoặc NULL cho anonymous` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 4 | `subject_id` | `subject_id` | `uuid NULL` | `N/A` | `N/A` | `N` | `` | `subject user ID khi có` | `subject user ID khi có` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 5 | `action` | `action` | `varchar(120) NOT NULL` | `N/A` | `N/A` | `Y` | `` | `Endpoint-specific action` | `Endpoint-specific action` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 6 | `outcome` | `outcome` | `audit_outcome NOT NULL` | `N/A` | `N/A` | `Y` | `` | `SUCCESS/DENIED/FAILURE` | `SUCCESS/DENIED/FAILURE` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 7 | `reason_code` | `reason_code` | `varchar(80) NULL` | `N/A` | `N/A` | `N` | `` | `Branch business code hoặc NULL` | `Branch business code hoặc NULL` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 8 | `trace_id` | `trace_id` | `varchar(64) NOT NULL` | `N/A` | `N/A` | `Y` | `` | `request.traceId` | `request.traceId` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 9 | `session_id` | `session_id` | `uuid NULL` | `N/A` | `N/A` | `N` | `` | `current session ID hoặc NULL` | `current session ID hoặc NULL` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 10 | `ip_hash` | `ip_hash` | `char(64) NULL` | `N/A` | `N/A` | `N` | `` | `hash(request IP) hoặc NULL` | `hash(request IP) hoặc NULL` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 11 | `user_agent_hash` | `user_agent_hash` | `char(64) NULL` | `N/A` | `N/A` | `N` | `` | `hash(User-Agent) hoặc NULL` | `hash(User-Agent) hoặc NULL` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 12 | `metadata` | `metadata` | `jsonb NOT NULL DEFAULT '{}'` | `N/A` | `N/A` | `Y` | `` | `Redacted metadata JSON` | `Redacted metadata JSON` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 13 | `prev_hash` | `prev_hash` | `char(64) NULL` | `N/A` | `N/A` | `N` | `` | `Previous chain hash hoặc NULL` | `Previous chain hash hoặc NULL` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 14 | `event_hash` | `event_hash` | `char(64) NOT NULL UNIQUE` | `N/A` | `N/A` | `Y` | `` | `Hash canonical event payload` | `Hash canonical event payload` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |
| 15 | `legal_hold_until` | `legal_hold_until` | `timestamptz NULL` | `N/A` | `N/A` | `N` | `` | `NULL trừ source approved` | `NULL trừ source approved` | `05_Data_Mapping.md#3-insertupdate-thong-tin` | `DIRECT` |

## Delete mapping

**Áp dụng khi**

- `N/A — Không có physical DELETE trong mapping này.`

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| 1 | `N/A` | `N/A` | `N/A` | `N/A` | Không hard-delete audit/history/token lifecycle nếu source không cho phép |

- Data Mapping: [05_Data_Mapping.md](./05_Data_Mapping.md#3-insertupdate-thong-tin).
- Schema mismatch columns: `N/A`.

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
