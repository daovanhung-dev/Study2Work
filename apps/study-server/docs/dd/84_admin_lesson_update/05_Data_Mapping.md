---
title: "Data Mapping"
order: 5
dd_id: "84"
api_name: "Cập nhật lesson"
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
- [2. Check body proposal](#step-2-check-body-proposal)
- [3. Update lesson](#step-3-update-lesson)
- [4. Check kết quả và map response](#step-4-check-ket-qua-va-map-response)
- [5. Trả response](#step-5-tra-response)

<a id="step-0-check-quyen"></a>

## 0. Check quyền

### 0.1. Authenticate và authorize

- Xác thực Bearer JWT theo catalog.
- Yêu cầu role Admin theo catalog.
- Yêu cầu lesson-management permission theo AC-34.
- Credential thiếu/sai/hết hạn -> HTTP 401 DESIGN_AUTHENTICATION_REQUIRED.
- Thiếu role/permission -> HTTP 403 DESIGN_ACCESS_DENIED.
- Current auth helper chỉ có Student guard; Admin claim, policy và guard chưa có.
- Authorize trước khi chạy UPDATE.

### 0.2. Quyền truy cập

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Authorization header | Bearer credential | Token hợp lệ | DIRECT requirement; route chưa có. |
| Principal policy | Admin role | Principal có role Admin | DIRECT requirement; claim source chưa có. |
| AC-34 policy | lesson-management permission | Principal được phép quản lý lesson | DIRECT precondition; implementation SOURCE_REQUIRED. |

<a id="step-1-nhan-request"></a>

## 1. Nhận request

### 1.1. Path

- lesson_id lấy từ path và có kiểu int64 theo catalog.
- Không thêm positive/minimum rule vì catalog không nêu.
- Path không parse được/out-of-range có thể map 422 DESIGN_VALIDATION_ERROR theo error set; chi tiết cần xác nhận.

### 1.2. Header và body

- Authorization lấy từ request header.
- X-Trace-Id được current middleware truyền hoặc khởi tạo; không phải input nghiệp vụ.
- JSON body và Content-Type chỉ là DERIVED proposal; catalog/diagram không xác nhận.

<a id="step-2-check-body-proposal"></a>

## 2. Check body proposal

### 2.1. Candidate full replacement

- title là candidate field; blank/trim/length rules chưa có nguồn.
- content là candidate field; null-to-clear và omission semantics cần xác nhận.
- video_url là candidate field; URI scheme/host/nullable rules cần xác nhận.
- order là candidate field; numeric bounds/order uniqueness rules cần xác nhận.
- HTTP 422 DESIGN_VALIDATION_ERROR là DIRECT code; exact validation conditions chưa được định nghĩa.
- Không sửa status trong body proposal; state change thuộc API #85.
- Không sửa course_id; chuyển lesson giữa course chưa có contract.
- ID lấy từ path, không duplicate trong body.

<a id="step-3-update-lesson"></a>

## 3. Update lesson

### 3.1. Q1 — Candidate UPDATE theo lesson ID

SQL dưới đây là proposal trên legacy DDL, chưa chạy và không chứng minh live schema.

```sql
UPDATE lessons AS l
SET
    name = :title,
    content = :content,
    video_url = :video_url,
    sort_order = :order,
    updated_at = CURRENT_TIMESTAMP
WHERE l.id = :lesson_id
RETURNING
    id,
    course_id,
    name,
    content,
    video_url,
    sort_order,
    status
```

- :lesson_id bind từ path.
- :title bind từ body title proposal.
- :content bind từ body content proposal.
- :video_url bind từ body video_url proposal.
- :order bind từ body order proposal.
- CURRENT_TIMESTAMP cho updated_at là DERIVED; cần xác nhận DB trigger/owner khác không quản lý timestamp.
- WHERE chỉ dùng candidate id; Admin permission phải hoàn tất trước query.
- Không JOIN/sửa courses, resources, progress, audit hoặc bảng khác.
- Không SET status; status transition thuộc #85.
- RETURNING cung cấp candidate response row, không cần pre-read.
- Transaction/commit boundary chưa xác nhận; helper convention giao transaction cho business caller.

### 3.2. Query Matrix

| Query | Type | Table | Conditions | Result/status |
|---|---|---|---|---|
| Q1 | UPDATE RETURNING | Legacy lessons AS l | l.id = :lesson_id | Candidate one-row update; live schema unknown. |
| Q1 | SET | Legacy lessons AS l | name=:title | DERIVED body-to-column mapping. |
| Q1 | SET | Legacy lessons AS l | content=:content | DERIVED body-to-column mapping. |
| Q1 | SET | Legacy lessons AS l | video_url=:video_url | DERIVED body-to-column mapping. |
| Q1 | SET | Legacy lessons AS l | sort_order=:order | DERIVED body-to-column mapping. |
| Q1 | RETURNING | Legacy lessons AS l | id | Candidate response source. |
| Q1 | RETURNING | Legacy lessons AS l | course_id | Candidate response source; nullable discrepancy. |
| Q1 | RETURNING | Legacy lessons AS l | name | Candidate response source for data.title. |
| Q1 | RETURNING | Legacy lessons AS l | content | Candidate response source. |
| Q1 | RETURNING | Legacy lessons AS l | video_url | Candidate response source. |
| Q1 | RETURNING | Legacy lessons AS l | sort_order | Candidate response source for data.order. |
| Q1 | RETURNING | Legacy lessons AS l | status | Candidate unchanged status response source. |
| Q1 no row | Result branch | UPDATE RETURNING | No returned row | Candidate 404 DESIGN_RESOURCE_NOT_FOUND. |

### 3.3. Mutation Matrix

| Mutation | Target | Field | Value source | Status |
|---|---|---|---|---|
| M1 UPDATE | lessons candidate | name | Body title | DERIVED; legacy DDL only. |
| M1 UPDATE | lessons candidate | content | Body content | DERIVED; null semantics open. |
| M1 UPDATE | lessons candidate | video_url | Body video_url | DERIVED; URI/null semantics open. |
| M1 UPDATE | lessons candidate | sort_order | Body order | DERIVED; range/uniqueness open. |
| M1 UPDATE | lessons candidate | updated_at | Server current timestamp | DERIVED; trigger/owner SOURCE_REQUIRED. |
| Not updated | lessons candidate | id, course_id, status, created_at | N/A | Not candidate writable fields; status is API #85. |

<a id="step-4-check-ket-qua-va-map-response"></a>

## 4. Check kết quả và map response

### 4.1. Có row trả về

- Khi UPDATE RETURNING trả đúng một row và required fields map được, tạo Lesson response.
- data.id = row.id.
- data.course_id = row.course_id.
- data.title = row.name.
- data.content = row.content.
- data.video_url = row.video_url.
- data.order = row.sort_order.
- data.status = row.status; #84 không thay đổi status.
- Legacy course_id có thể NULL nhưng response yêu cầu int64; không thay NULL bằng 0.
- Nếu response mapping lỗi sau UPDATE, transaction cần rollback; transaction owner chưa xác nhận.

### 4.2. Không có row

- Không có row từ Q1 -> candidate HTTP 404 DESIGN_RESOURCE_NOT_FOUND.
- Soft-delete visibility chưa có policy/marker chung.
- Không đọc resource trước authorization.

### 4.3. Database hoặc mapping failure

- Không trả raw SQL hoặc stack trace.
- Trả 500 DESIGN_INTERNAL_ERROR theo catalog.
- Rollback behavior cần khớp transaction owner tương lai.

### 4.4. Response Source Matrix

| Response field | Candidate source | Transform/null rule | Status |
|---|---|---|---|
| success | Envelope branch | true success / false error | DIRECT shape |
| businessCode | Catalog | Exact code per branch | DIRECT |
| message | Application | Safe text; exact text unspecified | DERIVED wording |
| data.id | Q1 returned id | Copy | Legacy candidate |
| data.course_id | Q1 returned course_id | Copy; null conflicts with required int64 | Legacy discrepancy |
| data.title | Q1 returned name | Alias name -> title | Legacy candidate; API #09 precedent |
| data.content | Q1 returned content | Copy; null/omit unresolved | Nullable candidate |
| data.video_url | Q1 returned video_url | Copy; URI/null/omit unresolved | TEXT candidate |
| data.order | Q1 returned sort_order | Alias sort_order -> order | Legacy candidate; API #09 precedent |
| data.status | Q1 returned status | Copy unchanged | Enum/casing unresolved |
| meta | Envelope convention | Empty object candidate on success | No API-specific data |
| traceId | Current trace middleware | Propagate or generate UUID | Current-source convention |

### 4.5. Schema boundary

- Catalog body schema absent; candidate SQL/body không phải implementation contract.
- Legacy DDL chỉ là candidate; V1-PILOT dùng UUID/versioned lesson khác biệt.
- Live database/migration state chưa xác minh.
- Không có successful runtime mapping claim vì route/module/test #84 chưa tồn tại.

<a id="step-5-tra-response"></a>

## 5. Trả response

### 5.1. Thành công

- Trả HTTP 200 DESIGN_RESOURCE_UPDATED khi mutation và mapping thành công.
- Dùng ApiEnvelope<Lesson> trực tiếp theo catalog.
- Không đổi sang Page/array và không thêm audit/dependency fields.
- Theo AC-34, sau success client gọi API #82 để reload danh sách; cardinality và filter `type` của #82 vẫn cần xác nhận.

### 5.2. Lỗi

- 401 DESIGN_AUTHENTICATION_REQUIRED cho authentication failure.
- 403 DESIGN_ACCESS_DENIED cho role/permission denial.
- 404 DESIGN_RESOURCE_NOT_FOUND cho row không tồn tại theo candidate.
- 422 DESIGN_VALIDATION_ERROR theo contract; rules cụ thể SOURCE_REQUIRED.
- 500 DESIGN_INTERNAL_ERROR cho DB/mapping failure.
- API guideline yêu cầu error data:null; helper hiện defaults data:{}; cần xử lý khi wire. Xem [06_Error.md](./06_Error.md).

### Request Usage Matrix

| Input | Step/use | Query/mutation/response use | Status |
|---|---|---|---|
| Authorization | 0 | Authenticate/authorize before mutation | DIRECT; implementation SOURCE_REQUIRED |
| lesson_id | 1.1/3.1 | Q1 WHERE; data.id | Type DIRECT; invalid mapping open |
| title | 2.1 | Q1 name; data.title | DERIVED |
| content | 2.1 | Q1 content; data.content | DERIVED; null/omit open |
| video_url | 2.1 | Q1 video_url; data.video_url | DERIVED; URI/null open |
| order | 2.1 | Q1 sort_order; data.order | DERIVED; bounds open |
| Query parameters | — | None declared | DIRECT absence |
| course_id body | — | Not changed | Excluded; confirmation required |
| status body | — | Not changed | Separate API #85 |

### Mục tiêu transaction

- Candidate mutation là một UPDATE statement với RETURNING.
- Transaction owner, commit point và mapping-failure rollback cần được xác nhận trước implementation.
- Study DB helper không tự commit; business caller sở hữu transaction.

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
