---
title: "Data Mapping"
order: 5
dd_id: "77"
api_name: "Xóa khóa học Admin theo policy AC-32"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
Admin Bearer principal -> shared ADMIN guard -> parse signed-int64 course_id -> Q1 lock non-DELETED course -> Q2 check enrollment/content blockers -> M1 set status=DELETED and updated_at=CURRENT_TIMESTAMP -> map UPDATE RETURNING to DeleteResult -> commit -> 200 DESIGN_RESOURCE_DELETED; blocker -> 422; missing/already-deleted -> 404; DB/mapping/commit failure -> rollback + 500
~~~

## Mục lục

- [0. Check quyền](#step-0-check-quyen)
- [1. Validate data input](#step-1-validate-data-input)
- [2. Get thông tin](#step-2-get-thong-tin)
- [3. Check policy and soft-delete](#step-3-check-policy-and-soft-delete)
- [4. Check mutation result](#step-4-check-mutation-result)
- [5. Map response](#step-5-map-response)
- [6. Trả response hoặc lỗi](#step-6-tra-response-hoac-loi)
- [Request Usage Matrix](#request-usage-matrix)
- [Query Matrix](#query-matrix)
- [Mutation Matrix](#mutation-matrix)
- [Response Source Matrix](#response-source-matrix)

<a id="step-0-check-quyen"></a>

## 0. Check quyền

### 0.1. Xác thực và authorization

- Xác thực Bearer JWT và shared role `ADMIN` trước mọi path parsing/lookup.
- Token thiếu/sai/hết hạn dùng 401 `DESIGN_AUTHENTICATION_REQUIRED` theo catalog.
- Principal thiếu role `ADMIN` dùng 403 `DESIGN_ACCESS_DENIED` theo catalog.
- Shared guard không chứng minh permission course-management riêng; đây là fallback `DERIVED`.

### 0.2. Thứ tự truy cập

- Không chạy Q1/Q2 trước khi authorization thành công.
- Không tiết lộ course existence hoặc enrollment/content dependency cho caller trái quyền.

<a id="step-1-validate-data-input"></a>

## 1. Validate data input

### 1.1. `course_id`

- Nhận path raw `course_id` theo `int64` bắt buộc trong catalog.
- Parse signed decimal integer; malformed hoặc overflow trả catalog 422.
- Signed-int64 âm/zero được query theo ID và sẽ trả 404 nếu không có course tương ứng.
- Không nhận body hoặc query.

<a id="step-2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Q1 — candidate course existence lookup

Legacy `courses.id/status` là BIGSERIAL/`VARCHAR(20)` candidate; live schema chưa xác minh. Runtime khóa course chưa soft-delete.

~~~sql
SELECT id
FROM courses
WHERE id = :course_id
  AND status IS DISTINCT FROM 'DELETED'
FOR UPDATE
~~~

- Bind `:course_id` từ path bằng parameter binding; không ghép chuỗi SQL.
- Chỉ đọc định danh cần cho branch; không tải Course/owner/PII vì DeleteResult không yêu cầu.
- Không ghép bảng V1-PILOT UUID `courses` hoặc `course_versions` vào candidate BIGINT model.

### 2.2. Q1 result branch

- Có một row có đúng `id`: tiếp tục Q2.
- Không có row, kể cả status đã `DELETED`: 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Projection/query failure: 500 `DESIGN_INTERNAL_ERROR` và rollback.

<a id="step-3-check-policy-and-soft-delete"></a>

## 3. Check policy and soft-delete

### 3.1. Enrollment and course content dependency — Q2

Legacy DDL/migrations have `enrollments`, `contents`, `lessons`, `quizzes` and `assignments` relations with `course_id`. Runtime checks them using bounded `EXISTS` projections in one query.

~~~sql
SELECT
    EXISTS (
        SELECT 1
        FROM enrollments AS enrollment
        WHERE enrollment.course_id = :course_id
    ) AS has_enrollments,
    (
        EXISTS (
            SELECT 1
            FROM contents AS content
            WHERE content.course_id = :course_id
              AND content.deleted_at IS NULL
        )
        OR EXISTS (
            SELECT 1
            FROM lessons AS lesson
            WHERE lesson.course_id = :course_id
        )
        OR EXISTS (
            SELECT 1
            FROM quizzes AS quiz
            WHERE quiz.course_id = :course_id
        )
        OR EXISTS (
            SELECT 1
            FROM assignments AS assignment
            WHERE assignment.course_id = :course_id
        )
    ) AS has_content
~~~

- Any enrollment row blocks, regardless of status/completion, to preserve learner history; this is `DERIVED`.
- Any active generic `contents` row blocks; `contents.deleted_at IS NOT NULL` rows do not block.
- Any `lessons`, `quizzes` or `assignments` row blocks because these candidate relations have no soft-delete marker.
- If `has_enrollments OR has_content`, return 422 and never mutate child rows.
- The exact dependency set/predicates are `DERIVED`; live table presence and owner policy remain unverified.

### 3.2. Chọn nhánh

- Both flags false: continue to M1.
- Either flag true: return catalog 422 and roll back the course lock transaction.
- Do not delete enrollment, progress or content rows to clear the blocker.

### 3.3. M1 — logical soft-delete

- AC-32 yêu cầu soft delete; runtime đặt legacy candidate `courses.status='DELETED'` và `updated_at=CURRENT_TIMESTAMP`.
- Đây là fallback `DERIVED` theo API #72; không thêm course column, table hoặc migration.
- `updated_at` từ DB `RETURNING` được ánh xạ vào `DeleteResult.deleted_at`.
- Không hard-delete, cascade, đổi metadata/mentor, cập nhật child rows hoặc ghi audit #76.
- Q1 khóa row trước Q2/M1; dependency check và marker update cùng transaction.

<a id="step-4-check-mutation-result"></a>

## 4. Check mutation result

- `UPDATE ... RETURNING` trả đúng ID và timestamp: map result rồi commit.
- Lock không tìm thấy course hoặc course đã `DELETED`: 404 theo fallback.
- Dependency blocker: 422; không thay đổi bảng con.
- Query, projection, timestamp mapping hoặc commit failure: rollback và trả 500 `DESIGN_INTERNAL_ERROR`.
- Không chạy physical `DELETE`, cascade hoặc audit mutation.

<a id="step-5-map-response"></a>

## 5. Map response

### 5.1. Success `DeleteResult`

- `response.data.id = course_id` sau khi course được soft-delete thành công.
- `response.data.status = "deleted"` theo reusable schema.
- `response.data.deleted_at = courses.updated_at` đọc từ `UPDATE RETURNING`.
- Timestamp đến từ DB; không dùng application clock.
- `updated_at` mapping là `DERIVED`, không phải dedicated deletion timestamp.

### 5.2. Envelope

- Thành công: HTTP 200, `DESIGN_RESOURCE_DELETED`, `ApiEnvelope<DeleteResult>`.
- Lỗi: giữ exact catalog 401/403/404/422/500 codes.
- `meta = {}` theo `success_response`; không thêm pagination hoặc dependency fields.
- Propagate/generate trace ID theo shared convention.
- API error helper mặc định `data:null`; shared route-template middleware đã áp dụng cho DELETE #77.

<a id="step-6-tra-response-hoac-loi"></a>

## 6. Trả response hoặc lỗi

1. Authorize shared `ADMIN` trước path parsing và lookup.
2. Validate raw `course_id` as signed int64; malformed/overflow → 422.
3. Q1 no-row/already-`DELETED` → 404.
4. Q2 enrollment/content blocker → 422, rollback lock transaction, no mutation.
5. M1 updates `status` and `updated_at`; map `RETURNING` result before commit.
6. Query/projection/commit failure → rollback + safe 500.
7. Return `ApiEnvelope<DeleteResult>` with the DB timestamp.
8. Do not return SQL, dependency identities, learner data or raw policy/database details.

Chi tiết: [06_Error.md](./06_Error.md).

## Request Usage Matrix

| Request item | Nguồn | Mapping step | Query/mutation use | Branch/response use | Gap |
|---|---|---|---|---|---|
| Authorization | Catalog + AC-32 DIRECT | 0.1 | Shared ADMIN guard trước mọi query | 401/403 | Finer course-management permission `SOURCE_REQUIRED`. |
| `course_id` | Catalog DIRECT | 1.1/Q1/Q2/M1 | Bound signed-int64 course identity | `data.id`; malformed/overflow 422; missing/already deleted 404 | Legacy BIGINT mapping is DERIVED; live schema unknown. |
| Body | Không khai báo | N/A | None | None | DIRECT absence. |
| Query | Không khai báo | N/A | None | None | DIRECT absence. |
| `Idempotency-Key` | Không có trong catalog | N/A | Không được đọc hoặc bind | N/A | Repeat DELETE returns 404 by DERIVED fallback; no key/replay behavior. |

## Query Matrix

| Query ID | Type | Candidate source | Columns/condition | Result/branch | Evidence/status |
|---|---|---|---|---|---|
| Q1 | `SELECT ... FOR UPDATE` | Legacy `courses` | `id=:course_id AND status IS DISTINCT FROM 'DELETED'` | Row → Q2; no row → 404 | Legacy DDL + API #72 fallback; live schema unknown. |
| Q2 | `SELECT EXISTS` | Legacy `enrollments`, `contents`, `lessons`, `quizzes`, `assignments` | `course_id=:course_id`; `contents.deleted_at IS NULL` | Either boolean true → 422; both false → M1 | Exact blocker set/predicates DERIVED from catalog title + checked-in DDL/runtime. |
| Q3 | `UPDATE ... RETURNING` | Legacy `courses` | Set `status='DELETED'`, `updated_at=CURRENT_TIMESTAMP`; filter non-DELETED row | Correct row/timestamp → commit; no row → 404 | API #72 precedent; live schema unknown. |

## Mutation Matrix

| Mutation ID | Operation | Target table | Condition | Fields/effect | Transaction/failure | Status |
|---|---|---|---|---|---|---|
| M1 | Soft-delete marker | Legacy candidate `courses` | Q1 exists; both Q2 flags false | Set `status='DELETED'`, `updated_at=CURRENT_TIMESTAMP` | Q1/Q2/M1 in one transaction; rollback on failure | Intent DIRECT; physical mapping DERIVED from #72. |
| Hard delete/cascade | Excluded | N/A | N/A | No physical parent/child delete | N/A | Not supported by AC-32 soft-delete intent. |
| Audit event | Not specified for #77 | N/A | N/A | Do not copy #76 audit write by analogy | N/A | Needs separate owner requirement if required. |

## Response Source Matrix

| Response field | Type | Source type | Table/column or generator | Transform/null rule | Gap/status |
|---|---|---|---|---|---|
| `success` | boolean | Envelope | Branch | true on success; false on error | DIRECT convention. |
| `businessCode` | string | Catalog | Success/error branch | Exact code only | DIRECT. |
| `message` | string | Application | Safe localized text | Exact text unspecified | DERIVED. |
| `data.id` | int64 | Legacy candidate | `courses.id` from UPDATE RETURNING | Required; match requested ID | DERIVED; live schema unknown. |
| `data.status` | literal `"deleted"` | Reusable schema | Constant | Exact lowercase literal | DIRECT. |
| `data.deleted_at` | date-time | Legacy candidate | `courses.updated_at` from UPDATE RETURNING | Required; serialize DB datetime | DERIVED by API #72 precedent; no dedicated timestamp. |
| `data.reason` | Not declared in DeleteResult | N/A | No source | Do not add field | DIRECT schema boundary. |
| `meta` | object | Envelope | `{}` | Empty object; no pagination | Current `success_response()` behavior. |
| `traceId` | uuid | Middleware | Current request trace | Propagate or generate | Current shared convention; route locally wired. |
| Error `data` | null by guideline | Response helper | Current helper defaults to `null` | Match current error helper | Current source behavior. |

## Cross-API boundary

- #75 owns course metadata update; #76 owns status update and the diagram’s audit event; #77 owns the soft-delete request only.
- #73 list/#74 detail currently expose course status and do not filter `DELETED`; the Admin can see the tombstone status. This is a chosen local visibility fallback, not a catalog rule.
- #75 can update metadata without changing `DELETED`; #76 can set a listed status on the same row. Restore/immutability semantics are not changed in this one-API task and remain an owner decision.
- Public course queries already require `PUBLISHED`; behavior of Mentor course/content write APIs for a DELETED course is outside this API task and remains a follow-up risk.

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
