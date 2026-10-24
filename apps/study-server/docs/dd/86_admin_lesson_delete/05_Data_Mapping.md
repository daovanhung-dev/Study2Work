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
- Yêu cầu lesson-management permission theo AC-34.
- Credential thiếu/sai/hết hạn → HTTP 401 DESIGN_AUTHENTICATION_REQUIRED.
- Thiếu role/permission → HTTP 403 DESIGN_ACCESS_DENIED.
- Current helper chỉ có Student guard; Admin claim, permission provider và guard chưa có.
- Hoàn tất authorize trước mọi query để không làm lộ lesson existence hoặc dependency.

### 0.2. Quyền truy cập

| Target/API | Claim/policy | Condition | Status |
|---|---|---|---|
| Authorization header | Bearer JWT | Token hợp lệ | DIRECT requirement; route chưa có. |
| Principal | Admin role | Principal có role Admin | DIRECT requirement; claim mapping SOURCE_REQUIRED. |
| AC-34 policy | lesson-management permission | Principal được phép quản lý lesson | DIRECT precondition; policy implementation SOURCE_REQUIRED. |

<a id="step-1-nhan-request"></a>

## 1. Nhận request

- lesson_id lấy từ path, required int64 theo catalog.
- Không thêm positive/minimum constraint chưa có nguồn.
- Catalog và diagram không khai báo body hoặc query.
- X-Trace-Id theo current middleware convention; không phải field nghiệp vụ.
- Path parse/range error có thể map 422 DESIGN_VALIDATION_ERROR vì code có trong catalog; exact parser behavior cần xác nhận.

<a id="step-2-tim-lesson"></a>

## 2. Tìm lesson

### 2.1. Q1 — Candidate existence lookup

Câu query chỉ là legacy BIGINT schema candidate; chưa chạy và không chứng minh live schema.

```sql
SELECT l.id
FROM lessons AS l
WHERE l.id = :lesson_id
LIMIT 1
```

- Bind :lesson_id từ path bằng parameter binding.
- Chỉ lấy định danh; DeleteResult không trả Lesson metadata.
- Có row → tiếp tục Q2.
- Không có row → candidate HTTP 404 DESIGN_RESOURCE_NOT_FOUND sau authorization.
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

Legacy resources.lesson_id có FK tới lessons.id. Live FK và điều kiện references nào chặn thao tác cần xác nhận.

### 3.2. Q2b — Lesson progress

```sql
SELECT EXISTS (
    SELECT 1
    FROM lesson_progress AS lp
    WHERE lp.lesson_id = :lesson_id
)
```

Legacy lesson_progress.lesson_id có FK tới lessons.id. DDL không xác định progress status nào được giữ, xóa hoặc block; không lọc theo status khi chưa có policy.

### 3.3. Candidate branch

- DERIVED recommendation: nếu Q2a hoặc Q2b trả true, dừng trước mutation và trả HTTP 422 DESIGN_VALIDATION_ERROR.
- Không xóa, sửa hoặc cascade resource/progress rows.
- Nếu không có reference/progress, tiếp tục soft-delete theo physical policy/schema đã được duyệt.
- Blocker set và 422 condition cần owner xác nhận; catalog chỉ xác nhận status/code có trong error set.
- Không suy ra enrollment/content moderation, completion, publication, parent course hoặc quiz policy ngoài quan hệ có evidence.

<a id="step-4-soft-delete-theo-policy"></a>

## 4. Soft-delete theo policy

### 4.1. M1 — Logical soft-delete recommendation

- AC-34 node n12 cho phép “Soft delete / delete theo policy”.
- DERIVED recommendation: ưu tiên soft-delete để giữ lịch sử lesson và tránh phá references.
- Legacy lessons không có deleted_at, is_deleted, archived_at hoặc soft-delete status contract.
- V1-PILOT lessons dùng UUID và cũng không có deletion marker; không dùng archived_at của course thay cho lesson deletion.
- Do đó không viết UPDATE/DELETE SQL, không tạo cột/table và không hard-delete/cascade như fallback.
- Physical relation, marker, timestamp source, visibility predicate và affected-row semantics là SOURCE_REQUIRED.
- DERIVED transaction recommendation: dependency check và approved soft-delete atomic; transaction caller/locking/isolation cần xác nhận.
- API #86 không có audit step trong AC-34; không sao chép audit của API #85.

### 4.2. Mutation Matrix

| Mutation | Target/effect | Condition | Fields/effect | Status |
|---|---|---|---|---|
| M1 | Logical lesson soft-delete | Q1 exists; approved dependency policy permits | Mark lesson deleted; physical fields unknown | DIRECT policy option; soft-delete choice DERIVED; physical mapping SOURCE_REQUIRED |
| M1 | Legacy lessons | No approved marker | No SQL or column is specified | SOURCE_REQUIRED |
| Dependency rows | resources, lesson_progress | Any row candidate blocks | No child delete/update/cascade | DERIVED block proposal; no child mutation |
| Audit | None in #86 flow | N/A | Do not copy #85 status audit | No direct requirement |

<a id="step-5-map-deleteresult"></a>

## 5. Map DeleteResult

### 5.1. Success response source

- data.id = approved lesson target ID after delete policy completes.
- data.status = literal "deleted" from reusable DeleteResult schema.
- data.deleted_at = persisted timestamp from the approved soft-delete source.
- Do not use request time or an unpersisted application clock as deleted_at.
- DeleteResult field/type is DIRECT; target persistence and timestamp mapping remain SOURCE_REQUIRED.
- Do not return Lesson fields, dependency details or audit data.

### 5.2. Result/error branches

- No lesson from Q1 → candidate 404 DESIGN_RESOURCE_NOT_FOUND.
- Reference/progress blocker under proposed policy → candidate 422 DESIGN_VALIDATION_ERROR.
- Query, persistence, timestamp mapping, response mapping or commit failure → 500 DESIGN_INTERNAL_ERROR.
- Do not return raw SQL, stack trace, dependency identifiers or learner information.
- Repeated delete/idempotency behavior is unresolved; do not silently return success/404/422 on a prior deletion.

<a id="step-6-tra-response-hoac-loi"></a>

## 6. Trả response hoặc lỗi

1. Authorize Admin before Q1.
2. Parse required path ID according to int64 contract.
3. Q1 checks target existence; no row uses candidate 404.
4. Q2a/Q2b check approved reference/progress scope.
5. Candidate blocker maps to catalog 422 and makes no mutation.
6. Approved logical soft-delete runs only with a selected physical marker and timestamp source.
7. Map full DeleteResult, including persisted deleted_at, then return HTTP 200 DESIGN_RESOURCE_DELETED.
8. Preserve exact 401/403/404/422/500 catalog errors; no new code/status.
9. Return only after the approved transaction completes.
10. Theo AC-34, sau success client gọi API #82 để reload danh sách; kết quả còn phụ thuộc cardinality/filter contract của #82 và visibility policy soft-delete chưa được duyệt.

## Request Usage Matrix

| Request item | Source/use | Query/mutation use | Response/error use | Status |
|---|---|---|---|---|
| Authorization | Header Bearer JWT | Admin/lesson permission before Q1 | 401/403; no dependency leakage | DIRECT; Admin claims SOURCE_REQUIRED |
| lesson_id | Required path int64 | Q1, Q2a, Q2b, approved M1 target | data.id after successful operation; no-row 404 | DIRECT type; legacy BIGINT candidate |
| Body/query | None | None | None | DIRECT absence |
| X-Trace-Id | Shared middleware | No SQL binding | traceId/header correlation | Current-source convention |

## Query Matrix

| Query | Type | Source/target | Predicate/result | Status |
|---|---|---|---|---|
| Q1 | SELECT | Legacy lessons candidate | id = :lesson_id | DERIVED existence query; live schema unknown |
| Q2a | EXISTS | Legacy resources candidate | lesson_id = :lesson_id | DIRECT dependency category; physical relation/policy candidate |
| Q2b | EXISTS | Legacy lesson_progress candidate | lesson_id = :lesson_id | DIRECT progress category; status/block semantics SOURCE_REQUIRED |
| Q2 result | Branch | Q2a/Q2b | Any candidate reference → no mutation, 422 proposal | DERIVED; owner confirmation required |
| M1 | Logical soft-delete | No approved physical source | Persist deleted state and timestamp | AC-34 option DIRECT; recommendation DERIVED; physical mapping SOURCE_REQUIRED |

## Response Source Matrix

| Response field | Contract/source | Mapping | Gap/status |
|---|---|---|---|
| success | ApiEnvelope<T> | true on success; false on error | DIRECT envelope field |
| businessCode | Catalog | Exact success/error code | DIRECT; no additional code |
| message | Application | Safe localized message | Exact wording DERIVED |
| data.id | DeleteResult / approved target | Lesson ID after operation | DIRECT field; physical source candidate |
| data.status | DeleteResult | Literal deleted | DIRECT exact value |
| data.deleted_at | DeleteResult | Approved persisted deletion timestamp | DIRECT type; physical mapping SOURCE_REQUIRED |
| meta | Envelope | Empty object candidate | No dependency metadata in contract |
| traceId | Current middleware | Propagate/generate UUID | Current-source convention |
| Error data | API guideline/current helper | Guideline null; current helper defaults {} | DISCREPANCY before runtime wiring |

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
