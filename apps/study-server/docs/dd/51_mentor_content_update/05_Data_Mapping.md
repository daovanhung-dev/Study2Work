---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "51"
api_name: "Cập nhật nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

```text
HTTP request
  -> FastAPI validates JSON body (DERIVED schema) and binds raw content_id
  -> shared Bearer/JWT guard role=MENTOR
  -> parse content_id as signed int64 (invalid -> 404)
  -> SELECT active contents + courses row FOR UPDATE
  -> require courses.mentor_id == numeric JWT sub
  -> INSERT previous Content into content_versions with next version_no
  -> UPDATE contents editable fields + status=PENDING_REVIEW
  -> validate returned Content projection
  -> commit once
  -> HTTP 200 DESIGN_RESOURCE_UPDATED
```

Local tests exercise the route/view using fake DB responses. They do not prove migration 007 or live schema availability.

## 0. Check quyền

### 0.1. Thực hiện check quyền

- `validate_current_user_request(..., role="MENTOR")` validates Bearer, token claims and role before database access.
- Stored `contents.course_id` determines the owner lookup; the client cannot select another course.
- Lock `contents` and its parent `courses` row during owner check and mutation.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| JWT principal | `roles` | Contains `MENTOR` | Direct role requirement; common helper implementation. |
| `contents AS content` | `id` | `content.id = :content_id` | Path-selected target. |
| `contents AS content` | `deleted_at` | `IS NULL` | Soft-deleted item is treated as absent. |
| `courses AS course` | `id` | `course.id = content.course_id` | Stored parent relation. |
| `courses AS course` | `mentor_id` | Equals numeric JWT subject | Direct-owner fallback derived from API #49; assigned Mentor is not supported. |

### 0.3. Check kết quả

- Authentication missing/invalid: `401 DESIGN_AUTHENTICATION_REQUIRED`.
- Required role missing: `403 DESIGN_ACCESS_DENIED`.
- Malformed/out-of-range `content_id` or missing/deleted Content: `404 DESIGN_RESOURCE_NOT_FOUND`.
- Stored course owner differs from caller: `403 DESIGN_ACCESS_DENIED`.
- Snapshot/update/query/commit integrity failure: `500 DESIGN_INTERNAL_ERROR`.

## 1. Validate data input

- FastAPI validates the derived strict request model before entering the view; malformed body returns `422 DESIGN_VALIDATION_ERROR` through middleware.
- `content_type` and `title` must be strings; `payload` must be a JSON object; unknown fields are forbidden.
- `content_id` is parsed in the view as signed int64; malformed/out-of-range IDs map to 404 as in API #48.
- No enum members, trimming, length bounds, nested payload schema, concurrency token or new 409 is added.

### Request Usage Matrix

| Request item | Source | Mapping step | Validation | Query/mutation usage | Response usage | Gap/status |
|---|---|---:|---|---|---|---|
| `Authorization` | Header | 0 | Bearer JWT + role | Numeric subject authorizes stored course | Not echoed | Role DIRECT; principal-to-Mentor relation DERIVED. |
| `content_id` | Path | 1–2 | Signed int64 | Q1 target; M1 version key; M2 update key | `data.id` | Path DIRECT; malformed ID -> 404 implementation. |
| `content_type` | Body | 1, 5 | Strict string | M1 snapshot contains old value; M2 stores new value | `data.content_type` | Field/requiredness/full replacement DERIVED from #50. |
| `title` | Body | 1, 5 | Strict string | M1 snapshot contains old value; M2 stores new value | `data.title` | Constraints not defined. |
| `payload` | Body | 1, 5 | JSON object | M1 snapshot contains old value; M2 casts replacement to JSONB | `data.payload` | Subtype schema not defined. |
| `course_id` | Stored row | 2, 3, 5 | DB projection | Owner authorization and both writes | `data.course_id` | Never accepted in body. |
| `status` | Stored/server rule | 4–5 | Server-managed | M1 archives old; M2 sets `PENDING_REVIEW` | `data.status` | Transition DERIVED from AC-33/#50. |
| `parent_id`, `content_order` | Stored row | 2, 4–5 | DB projection | Snapshot and preserve in current row | `data.parent_id`, `data.order` | Preserve behavior DERIVED. |

## 2. Get thông tin

### 2.1. Query — Q1

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `contents AS content` | `id` | Content key | Bound to path. |
| `↑` | `course_id` | Stored course scope | Used in response and owner join. |
| `↑` | `content_type`, `title`, `payload`, `status` | Current editable state | Archived before update. |
| `↑` | `parent_id`, `content_order AS "order"` | Current tree placement | Preserved. |
| `courses AS course` | `mentor_id` | Direct owner | Compared with numeric principal. |

### 2.2. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| `contents AS content` | `N/A` | `BASE` |
| `courses AS course` | `course.id = content.course_id` | `INNER JOIN` |

### 2.3. WHERE

- `content.id = :content_id`.
- `content.deleted_at IS NULL`.
- Lock matching Content and Course rows using `FOR UPDATE OF content, course`.

### 2.4. ORDER BY

- N/A; Q1 returns at most one row.

### Query Matrix

| Query ID | Purpose | SQL constant | Result/branch |
|---|---|---|---|
| Q1 | Read and lock active Content with owner | `LOCK_MENTOR_CONTENT` | No row -> rollback and 404; owner mismatch -> rollback and 403. |
| Q2 | Insert snapshot of current state with next `version_no` | `ARCHIVE_CONTENT_VERSION` | Require returned integer version; missing/invalid projection -> rollback and 500. |
| Q3 | Update current projection | `UPDATE_CONTENT` | Require full returned Content projection; missing/invalid projection -> rollback and 500. |

## 3. Insert/Update thông tin

### 3.1. Target table

- `content_versions` — INSERT pre-update snapshot.
- `contents` — UPDATE current projection.

### 3.2. Conditions

- M1 `content_versions.content_id = locked contents.id`.
- M1 `version_no = COALESCE(MAX(version_no), 0) + 1` for that Content; Content row lock serializes #51 updates.
- M2 `contents.id = :content_id AND deleted_at IS NULL`.
- Course, parent and order values come from locked Content, not body.

### 3.3. Items update/insert

- M1 columns: `content_id`, `version_no`, `course_id`, `content_type`, `title`, `payload`, `status`, `parent_id`, `content_order`, `archived_by`.
- M1 `archived_by` is the Mentor who superseded this snapshot. It is not a source-backed original-author value.
- M2 updates only `content_type`, `title`, `payload`, `status='PENDING_REVIEW'`.
- Each write is specified in [07_table.md](./07_table.md) and [08_content_versions_insert.md](./08_content_versions_insert.md).

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| `content_id` | Parsed path `content_id` | Signed int64. |
| `course_id` | Locked Content row | Not client-controlled. |
| `content_type`, `title`, `payload` | Required body | Derived full replacement; payload serialized to JSON before JSONB cast. |
| `status`, `parent_id`, `content_order` | Locked Content row | Archived as previous state. |
| `archived_by` | Numeric JWT subject | Actor performing the subsequent update, not original author. |

## 4. Check kết quả execute query

### 4.1. Thành công

- Validate archived version projection and `UPDATE ... RETURNING` against request plus locked identity/tree fields.
- Build shared `ContentResponse`; commit snapshot and current row together.
- Return HTTP 200 `DESIGN_RESOURCE_UPDATED`.

### 4.2. Lỗi hệ thống

- SQL/serialization/mapping/commit failure -> rollback and safe HTTP 500 `DESIGN_INTERNAL_ERROR`.
- No partial snapshot or update is committed by the view.

### 4.3. Validate lỗi

- Body validation -> HTTP 422 `DESIGN_VALIDATION_ERROR` with `meta.fieldErrors`.
- Path parse and missing/deleted Content -> HTTP 404 `DESIGN_RESOURCE_NOT_FOUND`.

### 4.4. Ngoài trường hợp trên

- No additional HTTP business code or 409 is introduced.
- API #52 publish selection and AC-33 approval/author behavior remain unresolved outside this endpoint.

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `3. Data mapping`
- Dimension: `B1:BB61`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `63`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Flow xử lý data |  |
| 4 | `D4` | 0. |  |
| 4 | `E4` | Check quyền |  |
| 5 | `E5` | ・ |  |
| 5 | `F5` | Thực hiện check quyền |  |
| 6 | `E6` | ・ |  |
| 6 | `F6` | Get count khi get data từ … |  |
| 7 | `G7` | Table get |  |
| 7 | `K7` | : |  |
| 8 | `G8` | Conditions |  |
| 8 | `K8` | : |  |
| 10 | `E10` | ・ |  |
| 10 | `F10` | Trường hợp giá trị get được lớn hơn 0, thực hiện các xử lý tiếp theo |  |
| 11 | `E11` | ・ |  |
| 11 | `F11` | Trường hợp giá trị get được bằng 0, trả về status 2 |  |
| 13 | `D13` | 1. |  |
| 13 | `E13` | validate data input |  |
| 14 | `F14` | refer sheet [４．Error] |  |
| 16 | `D16` | 2. |  |
| 16 | `E16` | Get thông tin… |  |
| 18 | `F18` | Table get |  |
| 18 | `K18` | Column get |  |
| 18 | `P18` | Chú thích |  |
| 18 | `U18` | Remarks |  |
| 29 | `F29` | Target table / join condition |  |
| 30 | `F30` | Target table |  |
| 30 | `N30` | Join condition |  |
| 30 | `AL30` | 結合種類 |  |
| 31 | `F31` | txn_ams_t0320 AS a |  |
| 32 | `F32` | txn_amm_v0002 AS b |  |
| 32 | `N32` | ON a . chy_typ = b . kbn_typ AND b . dmin_cd = A AND b . kbnknr_cd = 001 |  |
| 32 | `AL32` | LEFT JOIN |  |
| 33 | `F33` | txn_amm_v0002 AS c |  |
| 33 | `N33` | ON a . chy_typ = c . kbn_typ AND c . dmin_cd = A AND c . kbnknr_cd = Z02 |  |
| 33 | `AL33` | LEFT JOIN |  |
| 35 | `F35` | ・ |  |
| 35 | `G35` | Điều kiện get data |  |
| 37 | `F37` | ・ |  |
| 37 | `G37` | Điều kiện sort |  |
| 41 | `D41` | 3. |  |
| 41 | `E41` | Insert/Update thông tin … |  |
| 42 | `E42` | Update table…. |  |
| 43 | `E43` | ・ |  |
| 43 | `F43` | Items update |  |
| 44 | `F44` | ・ |  |
| 44 | `G44` | Refer sheet [xxxx] |  |
| 45 | `E45` | ・ |  |
| 45 | `F45` | Điều kiện get data |  |
| 46 | `F46` | ・ |  |
| 46 | `G46` | auth_user. id = user hiện tại theo token |  |
| 48 | `D48` | 4. |  |
| 48 | `E48` | check kết quả execute query  |  |
| 49 | `E49` | 1. Thành công |  |
| 50 | `F50` | HTTPStatus = 200 |  |
| 51 | `F51` | Trả về kết quả status = 1 |  |
| 52 | `E52` | 2. Lỗi hệ thống phát sinh |  |
| 53 | `F53` | HTTPStatus = 500 |  |
| 54 | `F54` | Trả về kết quả status = 2 |  |
| 55 | `E55` | 3. Validate lỗi |  |
| 56 | `F56` | HTTPStatus = 400 |  |
| 57 | `F57` | Trả về kết quả status = 2 |  |
| 58 | `E58` | 4. Ngoài trường hợp trên |  |
| 59 | `F59` | Trả về kết quả status = 2 |  |

</details>
