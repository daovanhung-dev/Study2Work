---
title: "Data Mapping"
order: 5
dd_id: "72"
api_name: "Xóa user theo policy AC-31"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
Admin Bearer principal -> xác thực/ủy quyền Admin user-management -> nhận user_id:int64 -> Q1 candidate kiểm tra target -> Q2 đánh giá ràng buộc theo policy đã duyệt -> áp dụng soft-delete/anonymization được duyệt, không hard-delete -> map DeleteResult nếu đủ nguồn -> 200 DESIGN_RESOURCE_DELETED hoặc exact catalog errors
~~~

# Mục lục

- [0. Check quyền](#step-0-check-quyen)
- [1. Validate data input](#step-1-validate-data-input)
- [2. Get thông tin](#step-2-get-thong-tin)
- [3. Check dependency và thực hiện policy](#step-3-check-dependency-va-thuc-hien-policy)
- [4. Check kết quả](#step-4-check-ket-qua)
- [5. Map response](#step-5-map-response)
- [Request Usage Matrix](#request-usage-matrix)
- [Query Matrix](#query-matrix)
- [Mutation Matrix](#mutation-matrix)
- [Response Source Matrix](#response-source-matrix)

<a id="step-0-check-quyen"></a>

## 0. Check quyền

### 0.1. Xác thực và authorization

- Xác thực Bearer JWT và quyền Admin/user-management trước khi kiểm tra user tồn tại.
- Token thiếu/sai/không hợp lệ dùng 401 DESIGN_AUTHENTICATION_REQUIRED theo catalog.
- Principal không có Admin role/quyền user management dùng 403 DESIGN_ACCESS_DENIED theo catalog.
- Claim, permission source, tenant/scope boundary và Admin guard chưa có Study source.
- Current shared guard chỉ yêu cầu Student; không tái sử dụng guard đó cho Admin.

### 0.2. Thứ tự truy cập

- Không chạy Q1 hoặc Q2 trước khi authorization thành công.
- Không để caller trái quyền phân biệt user tồn tại hay không.

<a id="step-1-validate-data-input"></a>

## 1. Validate data input

### 1.1. user_id

- Nhận path user_id theo int64 bắt buộc như catalog.
- Không thêm minimum, body field hoặc query parameter.
- Catalog có 422 DESIGN_VALIDATION_ERROR; exact malformed/overflow mapping cần theo contract và route parser được duyệt.

<a id="step-2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Q1 — candidate existence lookup

Legacy users là candidate theo DDL artifact; live relation/schema chưa được xác minh. Query này không được coi là runtime SQL đã duyệt.

~~~sql
SELECT u.id
FROM users AS u
WHERE u.id = :user_id
LIMIT 1
~~~

- Bind :user_id từ path; không ghép chuỗi SQL.
- Chỉ đọc định danh tối thiểu.
- Không đọc password_hash, email, phone hoặc profile nếu policy không yêu cầu.
- Không nối V1-PILOT UUID identity/profile tables.

### 2.2. Candidate result branch

- Một row: tiếp tục Q2 theo dependency/policy đã được duyệt.
- Không có row: 404 DESIGN_RESOURCE_NOT_FOUND là candidate branch theo detail-resource semantics; code/status trực tiếp theo catalog.
- Query/mapping failure: 500 DESIGN_INTERNAL_ERROR theo catalog.

## 3. Check dependency và thực hiện policy

<a id="step-3-check-dependency-va-thuc-hien-policy"></a>

### 3.1. Dependency check

AC-31 yêu cầu kiểm tra ràng buộc nhưng không chỉ ra quan hệ, predicate hoặc kết quả khi có liên kết. Legacy DDL artifact có các candidate references sau:

| Relation/column candidate | Ý nghĩa được mô tả trong DDL | Trạng thái |
|---|---|---|
| courses.mentor_id | Mentor gắn với khóa học | Candidate relation; live FK/policy chưa xác minh. |
| enrollments.user_id | User tham gia khóa học | Candidate relation; retention/block rule chưa có. |
| lesson_progress.user_id | User có dữ liệu tiến độ | Candidate relation; retention/block rule chưa có. |
| quiz_attempts.user_id | User có lịch sử làm bài | Candidate relation; retention/block rule chưa có. |
| assignment_submissions.user_id | User có bài nộp | Candidate relation; retention/block rule chưa có. |
| discussions.user_id | User là tác giả nội dung | Candidate relation; retention/anonymization rule chưa có. |
| notifications.user_id / sender_id | User là người nhận/người gửi | Candidate relation; retention rule chưa có. |
| payments.user_id | User có giao dịch thanh toán | Candidate relation; retention/anonymization rule chưa có. |
| refresh_tokens.user_id | Refresh credentials của user | DDL artifact có ON DELETE CASCADE; không áp dụng cascade vì flow này không hard-delete. |

Danh sách trên chỉ giúp policy owner xem xét phạm vi; không tạo Q2 SQL hoặc điều kiện chặn tự động. Live foreign keys và transaction behavior chưa được kiểm tra trên database.

### 3.2. Policy action

- AC-31 yêu cầu soft delete/anonymize theo policy; phải chọn policy và physical mapping trước khi implementation.
- Không hard-delete users hoặc bảng liên quan làm fallback.
- Không tự gán status DELETION_PENDING/ANONYMIZED vào legacy users; các giá trị đó chỉ xuất hiện trong enum của mô hình V1-PILOT UUID.
- Không tự xóa/cascade refresh tokens, payments, enrollments, submissions, discussions hoặc lịch sử.
- Bảng/cột mutation, PII transformation, audit record, deleted_at source, transaction và rollback đều SOURCE_REQUIRED.
- Nếu policy chặn thao tác, catalog có code 422 nhưng điều kiện và mapping phải được contract owner chốt; không định nghĩa business rule tại đây.

## 4. Check kết quả

<a id="step-4-check-ket-qua"></a>

- Target không tồn tại theo Q1: candidate 404 DESIGN_RESOURCE_NOT_FOUND.
- Policy cho phép và mutation đã được thực hiện theo schema/policy được duyệt: tiếp tục map response.
- Policy phát hiện ràng buộc: giữ ở status/code catalog phù hợp sau khi được xác nhận; 422 là code có trong catalog nhưng branch cụ thể SOURCE_REQUIRED.
- Input validation failure: 422 DESIGN_VALIDATION_ERROR theo catalog; chi tiết parse/path mapping chưa được xác nhận.
- Database, policy-service, mutation, commit hoặc response-source failure: 500 DESIGN_INTERNAL_ERROR.
- Không có code 409 trong contract; không thêm 409.
- Idempotency khi user đã soft-delete/anonymized chưa được xác định; không tự chọn success, 404 hoặc 422.

## 5. Map response

<a id="step-5-map-response"></a>

### 5.1. Thành công

Theo reusable DeleteResult:

- data.id: id của user target đã được xử lý thành công; nguồn cuối cùng phụ thuộc policy/schema.
- data.status: literal deleted theo catalog.
- data.deleted_at: timestamp theo nguồn được policy/schema phê duyệt. Legacy users hiện không có column này; không dùng giờ hệ thống làm giá trị persistable khi chưa có thiết kế.
- businessCode: DESIGN_RESOURCE_DELETED.
- meta: {} candidate.
- traceId: current request trace convention.

Không thể xác định đầy đủ success projection cho đến khi có nguồn deleted_at và mutation policy.

### 5.2. Lỗi

Giữ exact catalog status/code: 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 404 DESIGN_RESOURCE_NOT_FOUND, 422 DESIGN_VALIDATION_ERROR, 500 DESIGN_INTERNAL_ERROR. Error payload data null là guideline; current helper mặc định {}.

## Request Usage Matrix

| Request item | Nguồn | Mapping step | Query/mutation use | Branch/response use | Gap |
|---|---|---|---|---|---|
| Authorization | Catalog + AC-31 DIRECT | 0.1 | Không đưa vào SQL | 401/403 | Admin guard/claim/policy chưa có source. |
| user_id | Catalog DIRECT | 1.1/Q1 | Q1 candidate WHERE id=:user_id | data.id candidate; no-row candidate 404 | Legacy id relation và malformed path mapping chưa xác minh. |
| Request body | Không khai báo | N/A | None | None | DIRECT absence from catalog. |
| Query | Không khai báo | N/A | None | None | DIRECT absence from catalog. |

## Query Matrix

| Query ID | Type | Candidate source | Columns/condition | Result/branch | Evidence |
|---|---|---|---|---|---|
| Q1 | SELECT | Legacy users AS u | u.id; u.id=:user_id; LIMIT 1 | One row → policy review; no row → candidate 404 | Legacy DDL artifact; live schema unknown. |
| Q2 | SOURCE_REQUIRED | No approved dependency relation set | No SQL/predicate specified | Must not infer a blanket block/cascade rule | AC-31 says check constraints; detail absent. |
| Q3 | SOURCE_REQUIRED mutation | No approved physical soft-delete/anonymization target | No table/column specified | Required before success response | No legacy deleted_at; pilot schema is a different UUID model. |

## Mutation Matrix

| Mutation ID | Operation | Target table | Condition | Fields | Transaction/failure | Status |
|---|---|---|---|---|---|---|
| M1 | Soft-delete or anonymize according to approved policy | SOURCE_REQUIRED | Approved dependency and retention conditions | No fields specified | Boundary/rollback SOURCE_REQUIRED | Logical intent DIRECT; physical mutation SOURCE_REQUIRED. |
| Hard delete | Not specified and excluded from candidate | N/A | N/A | N/A | N/A | Must not be inferred from HTTP DELETE or DDL cascade. |

## Response Source Matrix

| Response field | Type | Source type | Table/column or generator | Transform/null rule | Gap/status |
|---|---|---|---|---|---|
| success | boolean | Envelope | Response branch | true on success; false on error | DIRECT envelope. |
| businessCode | string | Catalog | DESIGN_RESOURCE_DELETED or exact error code | Exact catalog code only | DIRECT. |
| message | string | Envelope | Safe localized message | Exact text unspecified | DERIVED. |
| data.id | int64 | DeleteResult | Successfully processed target ID | Required on success | Policy target/source needs approval. |
| data.status | literal "deleted" | DeleteResult schema | Constant | Exact lowercase literal | DIRECT. |
| data.deleted_at | date-time | DeleteResult schema | Approved deletion timestamp source | Required; no inferred fallback | SOURCE_REQUIRED; legacy schema has no source. |
| meta | object | Envelope | Empty object candidate | {} | Candidate; no pagination. |
| traceId | uuid | Middleware | Request trace | Validated/generated | Current shared convention; endpoint unwired. |
| error data | null by scope guideline | Error envelope | Current helper defaults to {} | Must reconcile before route wiring | DISCREPANCY. |

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
