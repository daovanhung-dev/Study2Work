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
Admin Bearer principal -> authorize course management -> receive course_id:int64 -> Q1 candidate course lookup -> Q2 enrollment/content eligibility under approved policy -> M1 logical soft-delete using approved persistence -> map DeleteResult -> 200 DESIGN_RESOURCE_DELETED; policy blocker -> catalog 422; source/runtime errors -> catalog 500
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

- Xác thực Bearer JWT và quyền Admin/course management trước mọi lookup.
- Token thiếu/sai/hết hạn dùng 401 `DESIGN_AUTHENTICATION_REQUIRED` theo catalog.
- Principal không có quyền Admin/course management dùng 403 `DESIGN_ACCESS_DENIED` theo catalog.
- Study hiện chỉ có shared Student guard; không tái sử dụng guard đó cho Admin.
- Claim, permission source, numeric/UUID identity binding và scope boundary chưa có nguồn.

### 0.2. Thứ tự truy cập

- Không chạy Q1/Q2 trước khi authorization thành công.
- Không tiết lộ course existence hoặc enrollment/content dependency cho caller trái quyền.

<a id="step-1-validate-data-input"></a>

## 1. Validate data input

### 1.1. `course_id`

- Nhận path `course_id` theo `int64` bắt buộc trong catalog.
- Không tự thêm minimum, body hoặc query rule.
- Catalog khai báo 422 `DESIGN_VALIDATION_ERROR`; malformed/overflow/positive-range mapping chưa được source xác nhận.

<a id="step-2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Q1 — candidate course existence lookup

Legacy `courses.id` là BIGSERIAL candidate trong DDL artifact; live schema chưa xác minh. Đây là query candidate, không phải runtime SQL đã duyệt.

~~~sql
SELECT c.id
FROM courses AS c
WHERE c.id = :course_id
LIMIT 1
~~~

- Bind `:course_id` từ path bằng parameter binding; không ghép chuỗi SQL.
- Chỉ đọc định danh cần cho branch; không tải Course/owner/PII vì DeleteResult không yêu cầu.
- Không ghép bảng V1-PILOT UUID `courses` hoặc `course_versions` vào candidate BIGINT model.

### 2.2. Q1 result branch

- Có một row: tiếp tục Q2 theo dependency policy đã được duyệt.
- Không có row: candidate 404 `DESIGN_RESOURCE_NOT_FOUND` sau authorization.
- Query/mapping failure: 500 `DESIGN_INTERNAL_ERROR` theo catalog.

<a id="step-3-check-policy-and-soft-delete"></a>

## 3. Check policy and soft-delete

### 3.1. Enrollment dependency — Q2a candidate

Legacy DDL có `enrollments.course_id` tham chiếu `courses.id`; status mặc định `ACTIVE`. Catalog không xác định status nào chặn và DDL/live FK không xác nhận policy.

~~~sql
SELECT EXISTS (
    SELECT 1
    FROM enrollments AS e
    WHERE e.course_id = :course_id
)
~~~

- Q2a chỉ là legacy relation candidate; xác nhận live relation, status predicate và cách giữ lịch sử trước implementation.
- Proposal `DERIVED`: nếu policy coi enrollment hiện hữu là blocker thì không chạy M1 và trả 422 `DESIGN_VALIDATION_ERROR`.
- Không xóa enrollment hoặc progress để “dọn” dependency.

### 3.2. Course content dependency — Q2b

- Catalog title yêu cầu kiểm tra content; legacy DDL không có generic Content table/relation.
- `lessons.course_id` là một khả năng đại diện course content, nhưng không chứng minh toàn bộ content hoặc API #50 generic Content persistence.
- Q2b physical relation, columns, predicates, version/status inclusion và dependency set là `SOURCE_REQUIRED`; không viết SQL giả định.
- Proposal `DERIVED`: nếu policy xác định có content hiện hữu là blocker, không chạy M1 và trả 422 `DESIGN_VALIDATION_ERROR`.

### 3.3. Chọn nhánh theo policy

- Nếu có enrollment/content thuộc tập blocker được owner duyệt: dừng trước mutation; trả 422 theo catalog với message an toàn. Câu này là proposal, không phải behavior đã được duyệt.
- Nếu không có blocker và policy/schema physical đã được chọn: tiếp tục M1.
- Nếu policy cho phép soft-delete khi còn dependency: chỉ thực hiện theo retention/history rules đã duyệt; không suy ra từ DDL.
- Không trả 409 vì catalog #77 không liệt kê `DESIGN_STATE_CONFLICT`.

### 3.4. M1 — logical soft-delete

- AC-32 diagram yêu cầu “Soft delete theo policy”; không thực hiện physical `DELETE FROM courses`.
- Physical relation, marker/column, status transition, timestamp source và affected-row semantics chưa có nguồn.
- Không dùng pilot `courses.archived_at` làm `deleted_at`; model này dùng UUID/versioned course.
- Không cập nhật CourseStatus, metadata, enrollment/content children hoặc audit event như side effect mặc định.
- Nếu persistence được duyệt, dependency check và M1 nên cùng transaction để tránh race; locking/isolation/transaction owner cần xác nhận.

<a id="step-4-check-mutation-result"></a>

## 4. Check mutation result

- Một logical soft-delete đã được persist và timestamp đọc được từ approved source: tiếp tục map response.
- Mutation không tìm thấy target do race: mapping 404 hay kết quả khác cần xác nhận cùng concurrency policy; không trả success khi marker không được ghi.
- Dependency blocker: trả 422 candidate như bước 3.3; không thay đổi bảng con.
- Query, mutation, timestamp mapping hoặc commit failure: rollback theo transaction được duyệt và trả 500 `DESIGN_INTERNAL_ERROR`.
- Hard-delete/cascade không phải fallback khi soft-delete storage chưa được chọn.

<a id="step-5-map-response"></a>

## 5. Map response

### 5.1. Success `DeleteResult`

- `response.data.id = course_id` sau khi course được soft-delete thành công.
- `response.data.status = "deleted"` theo reusable schema.
- `response.data.deleted_at = approved persisted soft-delete timestamp`.
- Không dùng `CURRENT_TIMESTAMP` làm source có thể khẳng định cho response nếu không có persistence rule.
- Chưa thể hoàn tất success mapping khi physical marker/timestamp còn `SOURCE_REQUIRED`.

### 5.2. Envelope

- Thành công: HTTP 200, `DESIGN_RESOURCE_DELETED`, `ApiEnvelope<DeleteResult>`.
- Lỗi: giữ exact catalog 401/403/404/422/500 codes.
- `meta = {}` là envelope candidate; không thêm pagination hoặc dependency fields.
- Propagate/generate trace ID theo shared convention.
- API guideline yêu cầu error `data:null`; current Study helper default `{}`. Đây là discrepancy, endpoint chưa wired.

<a id="step-6-tra-response-hoac-loi"></a>

## 6. Trả response hoặc lỗi

1. Authorize Admin trước lookup.
2. Validate path type theo direct contract.
3. Q1 no-row candidate → 404.
4. Q2a/Q2b theo dependency policy được duyệt.
5. Policy blocker candidate → 422, không mutation.
6. M1 approved soft-delete; nếu thất bại, rollback theo transaction được duyệt và trả 500.
7. Map đầy đủ `DeleteResult`; nếu timestamp source chưa được chọn, DD chưa implementation-ready.
8. Không trả SQL, dependency record, learner data hoặc internal policy detail.

Chi tiết: [06_Error.md](./06_Error.md).

## Request Usage Matrix

| Request item | Nguồn | Mapping step | Query/mutation use | Branch/response use | Gap |
|---|---|---|---|---|---|
| Authorization | Catalog + AC-32 DIRECT | 0.1 | Không bind vào SQL; authorization trước Q1 | 401/403; actor chỉ nếu audit được duyệt | Admin guard/claim/scope `SOURCE_REQUIRED`. |
| `course_id` | Catalog DIRECT | 1.1/Q1/M1 | Q1 identity; Q2 dependency scope; M1 logical target | `data.id` nếu mutation thành công; no-row candidate 404 | Physical/live relation và malformed-path mapping chưa xác nhận. |
| Body | Không khai báo | N/A | None | None | DIRECT absence. |
| Query | Không khai báo | N/A | None | None | DIRECT absence. |
| `Idempotency-Key` | Không có trong catalog | N/A | Không dùng cho đến khi retryability được duyệt | Replay/repeated-delete behavior chưa xác định | Guidelines có điều kiện cho retryable mutation. |

## Query Matrix

| Query ID | Type | Candidate source | Columns/condition | Result/branch | Evidence/status |
|---|---|---|---|---|---|
| Q1 | SELECT | Legacy `courses AS c` | `c.id`; `c.id = :course_id`; `LIMIT 1` | One row → policy check; no row → candidate 404 | Legacy DDL artifact; live schema unknown. |
| Q2a | EXISTS | Legacy `enrollments AS e` | `e.course_id = :course_id`; no status predicate approved | Existing enrollment may block under approved policy | Catalog title + legacy DDL; active/status semantics SOURCE_REQUIRED. |
| Q2b | SOURCE_REQUIRED | No approved generic Content relation | Base relation/columns/predicate unknown; `lessons.course_id` is only a possible candidate | Must not invent a complete content check | Generic Content schema absent; pilot model differs. |
| Q3 | N/A | No owner/counter projection | No Course response read specified | N/A | DeleteResult contains no Course fields. |

## Mutation Matrix

| Mutation ID | Operation | Target table | Condition | Fields/effect | Transaction/failure | Status |
|---|---|---|---|---|---|---|
| M1 | Logical soft-delete | Physical target `SOURCE_REQUIRED` | Q1 exists; approved dependency policy permits | Mark course deleted; do not delete/modify children | Atomic with checks is DERIVED; rollback/owner/isolation unresolved | Intent DIRECT; mapping SOURCE_REQUIRED. |
| Hard delete/cascade | Excluded | N/A | N/A | No physical parent/child delete | N/A | Not supported by AC-32 soft-delete intent. |
| Audit event | Not specified for #77 | N/A | N/A | Do not copy #76 audit write by analogy | N/A | Needs separate owner requirement if required. |

## Response Source Matrix

| Response field | Type | Source type | Table/column or generator | Transform/null rule | Gap/status |
|---|---|---|---|---|---|
| `success` | boolean | Envelope | Branch | true on success; false on error | DIRECT convention. |
| `businessCode` | string | Catalog | Success/error branch | Exact code only | DIRECT. |
| `message` | string | Application | Safe localized text | Exact text unspecified | DERIVED. |
| `data.id` | int64 | DeleteResult | Target `course_id` after successful mutation | Required | Physical marker/target binding SOURCE_REQUIRED. |
| `data.status` | literal `"deleted"` | Reusable schema | Constant | Exact lowercase literal | DIRECT. |
| `data.deleted_at` | date-time | Persistence | Approved deletion timestamp | Required; no inferred fallback | SOURCE_REQUIRED; legacy source absent. |
| `data.reason` | Not declared in DeleteResult | N/A | No source | Do not add field | DIRECT schema boundary. |
| `meta` | object | Envelope | `{}` candidate | Empty object; no pagination | Candidate. |
| `traceId` | uuid | Middleware | Current request trace | Propagate or generate | Current shared convention; route unwired. |
| Error `data` | null by guideline | Response helper | Current helper defaults to `{}` | Reconcile before runtime wiring | DISCREPANCY. |

## Cross-API boundary

- #75 owns course metadata update; #76 owns status update and the diagram’s audit event; #77 owns the soft-delete request only.
- If #77 succeeds, #73 list/#74 detail should likely hide the deleted course, but the marker/filter is not selected. #75/#76 behavior for an already deleted target also remains open.
- This group visibility proposal does not add a physical filter or change any endpoint contract.

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
