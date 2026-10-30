---
title: "Data Mapping"
order: 5
dd_id: "86"
api_name: "Xóa lesson"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

### Mục lục

- [0. Check quyền](#step-0-check-quyen)
- [1. Nhận request](#step-1-nhan-request)
- [2. Tìm lesson](#step-2-tim-lesson)
- [3. Check progress/reference và policy](#step-3-check-dependency-va-policy)
- [4. Soft-delete theo policy](#step-4-soft-delete-theo-policy)
- [5. Map DeleteResult](#step-5-map-deleteresult)
- [6. Trả response hoặc lỗi](#step-6-tra-response-hoac-loi)

<a id="step-0-check-quyen"></a>

## 0. Check quyền

### 0.1. Authenticate và authorize

- Xác thực Bearer JWT theo catalog.
- Yêu cầu role Admin theo catalog.
- Shared guard yêu cầu role ADMIN; AC-34 fine-grained lesson-management permission chưa có policy source.
- Credential thiếu/sai/hết hạn → HTTP 401 DESIGN_AUTHENTICATION_REQUIRED.
- Thiếu role/permission → HTTP 403 DESIGN_ACCESS_DENIED.
- `validate_current_user_request(..., role="ADMIN")` là guard dùng chung hiện tại.
- Hoàn tất authorize trước mọi query để không làm lộ lesson existence hoặc dependency.

### 0.2. Quyền truy cập

| Target/API | Claim/policy | Condition | Status |
|---|---|---|---|
| Authorization header | Bearer JWT | Token hợp lệ | DIRECT requirement; route chưa có. |
| Principal | ADMIN role | Principal có role ADMIN | DIRECT requirement; shared guard is wired. |
| AC-34 policy | lesson-management permission | Principal được phép quản lý lesson | DIRECT precondition; dedicated policy implementation SOURCE_REQUIRED. |

<a id="step-1-nhan-request"></a>

## 1. Nhận request

- lesson_id lấy từ path, required int64 theo catalog.
- Không thêm positive/minimum constraint chưa có nguồn.
- Catalog và diagram không khai báo body hoặc query.
- X-Trace-Id theo current middleware convention; không phải field nghiệp vụ.
- Raw signed-int64 parser maps format/range errors to 422 DESIGN_VALIDATION_ERROR.

<a id="step-2-tim-lesson"></a>

## 2. Tìm lesson

### 2.1. Q1 — Candidate existence lookup

Câu query khóa một row legacy BIGINT chưa có tombstone; đây là DDL candidate, không chứng minh live schema.

```sql
SELECT l.id, l.status
FROM lessons AS l
WHERE l.id = :lesson_id
  AND l.status IS DISTINCT FROM 'DELETED'
FOR UPDATE
```

- Bind :lesson_id từ path bằng parameter binding.
- Lấy ID/status để xác nhận target; `FOR UPDATE` tuần tự hóa blocker check và mutation.
- Có row → tiếp tục Q2 trong cùng transaction.
- Không có row hoặc status đã là `DELETED` → HTTP 404 DESIGN_RESOURCE_NOT_FOUND.
- Query/mapping failure → 500 DESIGN_INTERNAL_ERROR.

<a id="step-3-check-dependency-va-policy"></a>

## 3. Check progress/reference và policy

Catalog title yêu cầu check progress/reference. AC-34 n5 đọc lesson + dependencies trước khi chọn action. Các query dưới đây là candidate từ legacy DDL, không xác nhận active/live relation.

### 3.1. Q2a — Resource references

```sql
SELECT EXISTS (
    SELECT 1
    FROM resources AS r
    WHERE r.lesson_id = :lesson_id
)
```

Legacy `resources.lesson_id` tham chiếu `lessons.id`. Bất kỳ row nào là blocker cục bộ; live FK/policy chưa xác minh.

### 3.2. Q2b — Lesson progress

```sql
SELECT EXISTS (
    SELECT 1
    FROM lesson_progress AS lp
    WHERE lp.lesson_id = :lesson_id
)
```

Legacy `lesson_progress.lesson_id` tham chiếu `lessons.id`. Bất kỳ row nào là blocker cục bộ; không lọc status và không đọc dữ liệu người học.

### 3.3. Q2c — Attached upload references

```sql
SELECT EXISTS (
    SELECT 1
    FROM lesson_uploads
    WHERE lesson_id = :lesson_id
)
```

Legacy `lesson_uploads.lesson_id` tham chiếu Lesson và giữ thứ tự UploadAsset. Bất kỳ link nào là blocker; không xóa link hoặc upload.

### 3.3. Candidate branch

- Nếu Q2a, Q2b hoặc Q2c trả true, dừng trước mutation và trả HTTP 422 DESIGN_VALIDATION_ERROR.
- Không xóa, sửa hoặc cascade resource/progress/upload rows.
- Status audit rows từ API #85 được giữ làm lịch sử; chúng không cản logical tombstone.
- Nếu không có dependency, tiếp tục M1 trong transaction đang giữ row lock.
- Relation/blocker mapping là DERIVED từ legacy DDL và catalog intent; live constraints chưa được xác nhận.
- Không suy ra enrollment/content moderation, completion, publication, parent course hoặc quiz policy ngoài quan hệ có evidence.

<a id="step-4-soft-delete-theo-policy"></a>

## 4. Soft-delete theo policy

### 4.1. M1 — Legacy status tombstone

- AC-34 node n12 cho phép “Soft delete / delete theo policy”.
- DERIVED fallback: set `lessons.status='DELETED'` to preserve history, following API #77's legacy soft-delete marker.
- Legacy lessons have no `deleted_at`; set `updated_at=CURRENT_TIMESTAMP` and use its DB-returned value as `DeleteResult.deleted_at`.
- V1-PILOT lessons dùng UUID và cũng không có deletion marker; không dùng archived_at của course thay cho lesson deletion.
- Không tạo column/table, không hard-delete và không cascade.
- Active Admin list/detail/update/status and Mentor/resource reads exclude `DELETED` rows.
- UPDATE target still requires `status IS DISTINCT FROM 'DELETED'`; a concurrent/repeated delete with no returned row maps to 404.
- `FOR UPDATE`, dependency checks and update share the view-owned transaction; live lock/FK behavior is unverified.
- API #86 không có audit step trong AC-34; không sao chép audit của API #85.

### 4.2. Mutation Matrix

| Mutation | Target/effect | Condition | Fields/effect | Status |
|---|---|---|---|---|
| M1 | Legacy lessons | Q1 exists; Q2a/Q2b/Q2c are false | Set `status='DELETED'`, `updated_at=CURRENT_TIMESTAMP` | DERIVED local fallback |
| Dependency rows | resources, lesson_progress, lesson_uploads | Any row blocks with 422 | No child delete/update/cascade | DERIVED local policy |
| Audit | None in #86 flow | N/A | Do not copy #85 status audit | No direct requirement |

<a id="step-5-map-deleteresult"></a>

## 5. Map DeleteResult

### 5.1. Success response source

- data.id = approved lesson target ID after delete policy completes.
- data.status = literal "deleted" from reusable DeleteResult schema.
- data.deleted_at = DB-returned `lessons.updated_at` from the tombstone UPDATE.
- Do not use request time or an unpersisted application clock as deleted_at.
- DeleteResult field/type is DIRECT; `updated_at` timestamp mapping is DERIVED from API #77 precedent.
- Do not return Lesson fields, dependency details or audit data.

### 5.2. Result/error branches

- No active lesson from Q1, including repeat delete → 404 DESIGN_RESOURCE_NOT_FOUND.
- Any progress/resource/upload blocker → 422 DESIGN_VALIDATION_ERROR.
- Query, persistence, timestamp mapping, response mapping or commit failure → 500 DESIGN_INTERNAL_ERROR.
- Do not return raw SQL, stack trace, dependency identifiers or learner information.
- Repeated delete returns 404 locally because Q1 excludes rows marked `DELETED`; this is DERIVED because catalog does not define idempotency.

<a id="step-6-tra-response-hoac-loi"></a>

## 6. Trả response hoặc lỗi

1. Authorize Admin before Q1.
2. Parse required path ID according to int64 contract.
3. Q1 checks target existence; no row uses candidate 404.
4. Q2a/Q2b/Q2c check progress, resources and attached upload links.
5. Candidate blocker maps to catalog 422 and makes no mutation.
6. With no blockers, UPDATE the legacy status marker and persisted timestamp.
7. Map full DeleteResult, including persisted deleted_at, then return HTTP 200 DESIGN_RESOURCE_DELETED.
8. Preserve exact 401/403/404/422/500 catalog errors; no new code/status.
9. Return only after the approved transaction completes.
10. Theo AC-34, sau success client gọi API #82 để reload danh sách; #82 excludes `DELETED` rows in this local implementation.

## Request Usage Matrix

| Request item | Source/use | Query/mutation use | Response/error use | Status |
|---|---|---|---|---|
| Authorization | Header Bearer JWT | Shared ADMIN guard before Q1 | 401/403; no dependency leakage | DIRECT role; dedicated permission SOURCE_REQUIRED |
| lesson_id | Required path int64 | Q1, Q2a/Q2b/Q2c, M1 target | data.id after success; absent/repeated delete 404 | DIRECT type; legacy BIGINT candidate |
| Body/query | None | None | None | DIRECT absence |
| X-Trace-Id | Shared middleware | No SQL binding | traceId/header correlation | Current-source convention |

## Query Matrix

| Query | Type | Source/target | Predicate/result | Status |
|---|---|---|---|---|
| Q1 | SELECT FOR UPDATE | Legacy lessons candidate | id = :lesson_id and status distinct from DELETED | DERIVED target/lock query; live schema unknown |
| Q2a | EXISTS | Legacy resources candidate | lesson_id = :lesson_id | DERIVED reference blocker |
| Q2b | EXISTS | Legacy lesson_progress candidate | lesson_id = :lesson_id | DERIVED progress blocker, any status |
| Q2c | EXISTS | Legacy lesson_uploads candidate | lesson_id = :lesson_id | DERIVED attached-file reference blocker |
| Q2 result | Branch | Q2a/Q2b/Q2c | Any reference → no mutation, catalog 422 | DERIVED local policy |
| M1 | UPDATE | Legacy lessons candidate | status DELETED, updated_at CURRENT_TIMESTAMP | DERIVED from API #77; live schema unknown |

## Response Source Matrix

| Response field | Contract/source | Mapping | Gap/status |
|---|---|---|---|
| success | ApiEnvelope<T> | true on success; false on error | DIRECT envelope field |
| businessCode | Catalog | Exact success/error code | DIRECT; no additional code |
| message | Application | Safe localized message | Exact wording DERIVED |
| data.id | DeleteResult / lessons.id | Lesson ID after operation | DIRECT field; legacy BIGINT candidate |
| data.status | DeleteResult | Literal deleted | DIRECT exact value |
| data.deleted_at | DeleteResult / lessons.updated_at | DB timestamp written by M1 | DIRECT type; DERIVED mapping |
| meta | Envelope | Empty object candidate | No dependency metadata in contract |
| traceId | Current middleware | Propagate/generate UUID | Current-source convention |
| Error data | Current response helper and API #86 tests | `null` for errors | Current source behavior verified locally |

---

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
