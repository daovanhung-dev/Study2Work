---
title: "Định nghĩa table"
order: 7
dd_id: "34"
api_name: "Upload file"
source_sheet: "table"
status: "Draft — Ready for Review"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | uploads |
| Logical table | UploadAsset metadata |
| Operation | INSERT |
| Data Mapping step | 4 |

Target schema là checked-in legacy BIGINT Study DDL. Migration chỉ được thêm vào source; chưa được áp dụng lên live database.

## Insert mapping

**Áp dụng khi**

- Object Storage upload thành công và course scope check đã đạt.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| 1 | id | UploadAsset ID | BIGSERIAL | 64-bit | N/A | Y | ● | Database generated ID | RETURNING id | 4 | Durable int64 reference. |
| 2 | owner_id | Owner user ID | BIGINT | 64-bit | N/A | Y |  | JWT numeric subject | Authorization | 0 | REFERENCES users(id). |
| 3 | purpose | Upload purpose | VARCHAR | 20 | N/A | Y |  | SUBMISSION or LECTURE | Multipart purpose | 2 | CHECK restricts current enum. |
| 4 | course_id | Course context ID | BIGINT | 64-bit | N/A | N |  | Student optional; Mentor LECTURE required | Multipart field | 2 | REFERENCES courses(id). |
| 5 | storage_key | Object key | TEXT | N/A | N/A | Y |  | `uploads/<UUID>` | Server UUID | 3 | Unique; never client supplied. |
| 6 | file_name | Original file name | TEXT | N/A | N/A | Y |  | Filename or `upload` | Multipart filename | 2 | Used as metadata, not key. |
| 7 | url | Public URL | TEXT | N/A | N/A | Y |  | Public base URL plus key | Object Storage config | 3 | Persisted and returned. |
| 8 | content_type | Content type | TEXT | N/A | N/A | Y |  | Multipart Content-Type or octet-stream | File part header | 2 | No MIME allowlist. |
| 9 | size_bytes | Actual size in bytes | BIGINT | 64-bit | N/A | Y |  | Byte count from received stream | Uploaded bytes | 2 | CHECK size_bytes >= 0. |
| 10 | status | Upload status | VARCHAR | 20 | N/A | Y |  | Constant `UPLOADED` | API constant/DB default | 4 | CHECK restricts current lifecycle state. |

## Update mapping

**Áp dụng khi**

- N/A — API #34 creates an UploadAsset and does not update existing rows.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No update operation. |

## Delete mapping

**Áp dụng khi**

- No business delete endpoint is defined. Compensation only calls Object Storage delete when metadata transaction fails.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---|---|---|---|---:|---|
| 1 | storage_key | = | Server-generated UUID for attempted upload | 5.2 | Best-effort S3 cleanup; no uploads row is retained after rolled-back INSERT. |

## Constraints and indexes

- `uploads.id` is `BIGSERIAL PRIMARY KEY`.
- `uploads.owner_id` references `users(id)`.
- `uploads.course_id` optionally references `courses(id)`.
- `uploads.purpose` accepts `SUBMISSION` or `LECTURE` only.
- `uploads.storage_key` is unique.
- `uploads.size_bytes` must be non-negative.
- `uploads.status` defaults to and is constrained to `UPLOADED`.
- `idx_uploads_owner_purpose_course` supports future owner/purpose/course asset resolution.

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
