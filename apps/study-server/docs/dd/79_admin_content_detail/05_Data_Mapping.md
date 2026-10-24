---
title: "Data Mapping"
order: 5
dd_id: "79"
api_name: "Lấy chi tiết content và metadata review"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
Admin Bearer principal -> authorize Admin -> parse content_id:int64 -> Q1 logical Content lookup by ID -> AC-33 Q2 version and Q3 author reads remain SOURCE_REQUIRED -> map exact catalog Content fields -> 200 DESIGN_RESOURCE_RETRIEVED; absent Content 404; query/mapping failure 500
~~~

## Mục lục

- [0. Check quyền](#step-0-check-quyen)
- [1. Validate data input](#step-1-validate-data-input)
- [2. Get thông tin](#step-2-get-thong-tin)
- [3. Map response](#step-3-map-response)
- [4. Trả response hoặc lỗi](#step-4-tra-response-hoac-loi)
- [Request Usage Matrix](#request-usage-matrix)
- [Query Matrix](#query-matrix)
- [Mutation Matrix](#mutation-matrix)
- [Response Source Matrix](#response-source-matrix)

<a id="step-0-check-quyen"></a>

## 0. Check quyền

### 0.1. Xác thực Admin

- Đọc Authorization Bearer JWT theo catalog.
- Xác thực token trước mọi Content, version hoặc author read.
- Principal cần role Admin theo catalog.
- Current validate_current_user_request chỉ chấp nhận role STUDENT; không dùng guard này cho #79.
- Admin claim/guard/permission policy và principal identity chưa có source hiện tại; endpoint chưa được wire.

### 0.2. Thứ tự truy cập

- Không chạy Q1/Q2/Q3 trước khi authentication và authorization thành công.
- Không trả Content, version hoặc author data cho principal chưa được authorize.
- Chưa có policy về Admin scope/tenant; không tự thêm permission table hoặc claim name.

### 0.3. Kết quả authorization

- Thiếu/sai Bearer hoặc token không hợp lệ: 401 DESIGN_AUTHENTICATION_REQUIRED theo catalog.
- Principal đã xác thực nhưng thiếu role Admin: 403 DESIGN_ACCESS_DENIED theo catalog.
- Không tiết lộ có hay không có content_id khi authorization thất bại.

<a id="step-1-validate-data-input"></a>

## 1. Validate data input

### 1.1. content_id

- Nhận path content_id kiểu int64 bắt buộc theo catalog.
- Không thêm min/max nghiệp vụ hoặc đổi ID sang UUID.
- Catalog #79 không liệt kê 422; malformed/overflow path behavior chưa có contract.
- Không nhận version_id, expected_row_version, body hoặc query parameter.

### 1.2. Input parsing boundary

- Nếu path value không được framework parse thành int64, current middleware chưa allowlist /api/v1/admin/content/{content_id} và có thể dùng fallback VALIDATION_ERROR; đây là conditional future-wiring discrepancy.
- Không thêm 422 hoặc business code mới vào DD.

<a id="step-2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Q1 — logical Content lookup

AC-33 n5 truyền content_id cho detail; n6 đọc content/version/author. Catalog định nghĩa Content response tám field. Vì chưa có physical Content relation tương thích, Q1 chỉ mô tả logical operation.

| Logical field | Value/source | Rule/status |
|---|---|---|
| id | Path content_id | Candidate Content.id = :content_id; khóa vật lý SOURCE_REQUIRED. |
| course_id | Logical Content | Required response field; physical relation SOURCE_REQUIRED. |
| content_type | Logical Content | Required; enum/value source chưa có. |
| title | Logical Content | Required; column source chưa có. |
| payload | Logical Content | Required object; member schema SOURCE_REQUIRED. |
| status | Logical Content | Return value read; enum and stale-state policy unresolved. |
| parent_id | Logical Content | Optional; null/omit rule and relation SOURCE_REQUIRED. |
| order | Logical Content | Required; sibling order, not review queue order. |

Q1 không áp dụng status predicate. #78 đã chọn queue row theo PENDING_REVIEW; AC-33 không nói #79 phải recheck status. Giữ đây là proposal DERIVED; nếu item bị đổi status giữa queue và detail thì behavior cần xác nhận.

### 2.2. Q2 — selected Content version

- AC-33 n6 trực tiếp yêu cầu đọc version.
- Không có version ID trong path, query hoặc response contract.
- Không có generic BIGINT ContentVersion schema được chọn; V1-PILOT course_versions và content_blocks là UUID/course-version scoped.
- Không chọn version mới nhất, pending revision, published revision hoặc lịch sử nếu chưa có owner rule.
- Không viết SQL hoặc join giả định; Q2 là logical SOURCE_REQUIRED.

### 2.3. Q3 — Content author

- AC-33 n6 trực tiếp yêu cầu đọc author.
- Catalog Content không có author field/author schema; identity mapping cho Admin-visible author projection chưa được mô tả.
- content_review_decisions.reviewer_subject_id là reviewer, không phải author.
- course_versions.created_by_subject_id là creator của course version trong V1-PILOT; không chứng minh tác giả cho logical Content row.
- Không viết SQL hoặc trả author PII; Q3 là logical SOURCE_REQUIRED.

### 2.4. Physical source boundary

- Legacy DB.sql có lessons và resources nhưng không có generic Content/version/author relation.
- V1-PILOT content_blocks.id là UUID, gắn lesson_id UUID và chứa content_json; không khớp Content BIGINT fields course_id, content_type, title, payload.
- V1-PILOT content_review_decisions là append-only decision record với UUID resource_version_id và reviewer; không phải Content/version source.
- Không remap UUID thành int64, không coi relation trong DDL artifact là live/deployed schema.

### 2.5. Kết quả query

- Q1 không có logical Content cho ID: catalog có 404 DESIGN_RESOURCE_NOT_FOUND; semantics là candidate detail-resource branch.
- Lỗi query hoặc mapping: 500 DESIGN_INTERNAL_ERROR theo catalog.
- Query đọc version/author chưa thể hoàn thiện mapping thành current source; cần schema/contract decision trước implementation.

<a id="step-3-map-response"></a>

## 3. Map response

### 3.1. Direct ApiEnvelope<Content>

- data là một Content theo catalog; không bọc Page/list.
- Map đúng tám field của reusable Content schema.
- data.status phản ánh row được đọc; không ép PENDING_REVIEW khi #79 chưa có status filter được duyệt.
- Không thêm version, author, review_reason, reviewer, decision history hoặc audit fields.
- AC-33 metadata read và serialized response hiện không khớp; contract owner cần quyết định metadata có được trả cho client hay chỉ dùng nội bộ.

### 3.2. Envelope

- Success: HTTP 200 DESIGN_RESOURCE_RETRIEVED.
- Errors: chỉ 401/403/404/500 với exact catalog codes.
- meta={} là candidate envelope convention; API #79 không có pagination.
- API guideline yêu cầu error data:null; current error_response() default data={} nếu không truyền. Endpoint chưa wired.

### Request Usage Matrix

| Request item | Source | Mapping step | Query use | Branch/response use | Gap |
|---|---|---|---|---|---|
| Authorization | Catalog Bearer/Admin | 0.1 | Authorize trước Q1/Q2/Q3 | 401/403 | Admin guard/claim SOURCE_REQUIRED. |
| content_id | Catalog int64 required | 1.1 | Candidate bind Content.id = :content_id | Map data.id; no row candidate 404 | Physical key SOURCE_REQUIRED. |
| Body | Not declared | N/A | None | None | DIRECT absence. |
| Query | Not declared | N/A | None | None | DIRECT absence. |

### Query Matrix

| Query ID | Type | Candidate source | Logical fields/conditions | Result/branch | Evidence/status |
|---|---|---|---|---|---|
| Q1 | SELECT, logical | Content source SOURCE_REQUIRED | Candidate id=:content_id; read eight reusable Content fields | Content detail; no row → catalog 404 | ID lookup DERIVED; table/columns SOURCE_REQUIRED. |
| Q2 | SELECT, logical only | Content version/revision | Select version tied to Content | AC-33 detail metadata | Read intent DIRECT; selector and storage SOURCE_REQUIRED. |
| Q3 | SELECT, logical only | Content author identity | Select author associated with selected Content/version | AC-33 detail metadata | Read intent DIRECT; identity/field projection SOURCE_REQUIRED. |

### Mutation Matrix

| Mutation ID | Operation | Target | Condition | Fields/effect | Status |
|---|---|---|---|---|---|
| N/A | None | N/A | API #79 is GET/read-only | No INSERT/UPDATE/DELETE, review decision or audit write | N/A — READ-ONLY API |

## Response Source Matrix

| Response field | Contract type | Source type | Table/column or generator | Transform/null rule | Gap/status |
|---|---|---|---|---|---|
| success | boolean | Envelope | Branch | true on success; false on error | Envelope convention. |
| businessCode | string | Catalog | Branch literal | DESIGN_RESOURCE_RETRIEVED or exact listed error | DIRECT. |
| message | string | Application | Safe localized message | Exact wording unspecified | DERIVED. |
| data | Content | Logical Q1 | Content result | Singular object | DIRECT type; physical source SOURCE_REQUIRED. |
| data.id | int64 | Content source | Logical identifier | Required | DIRECT field; key mapping SOURCE_REQUIRED. |
| data.course_id | int64 | Content source | Logical owner course | Required | SOURCE_REQUIRED. |
| data.content_type | ContentType | Content source | Logical type | Approved enum serialization only | SOURCE_REQUIRED. |
| data.title | string | Content source | Logical title | Preserve approved value | SOURCE_REQUIRED. |
| data.payload | object | Content source | Logical subtype payload | Do not invent members/default | SOURCE_REQUIRED. |
| data.status | ContentStatus | Content source | Current row status | Return stored logical status | Enum/storage/stale rule SOURCE_REQUIRED. |
| data.parent_id | int64? | Content source | Logical parent | Null/omit behavior unresolved | SOURCE_REQUIRED. |
| data.order | int32 | Content source | Logical sibling position | Does not imply queue order | SOURCE_REQUIRED. |
| meta | object | Envelope convention | Branch | {} candidate | No pagination contract. |
| traceId | uuid | Shared trace middleware | X-Trace-Id | Validate or generate per current convention | Route absent. |
| Error data | null by guideline | Error helper | Current helper default {} | Expected/current discrepancy | DISCREPANCY. |

AC-33 node n6 yêu cầu đọc version và author, nhưng chúng không phải field của reusable Content và chưa có response schema. Không map chúng vào response cho tới khi contract được cập nhật.

<a id="step-4-tra-response-hoac-loi"></a>

## 4. Trả response hoặc lỗi

- Thiếu/sai Bearer hoặc token không hợp lệ: 401 DESIGN_AUTHENTICATION_REQUIRED.
- Principal hợp lệ nhưng không có role Admin: 403 DESIGN_ACCESS_DENIED.
- Không có Content theo ID: candidate 404 DESIGN_RESOURCE_NOT_FOUND.
- Query/read/mapping failure: 500 DESIGN_INTERNAL_ERROR.
- Không thêm lỗi 422/409 cho malformed path, stale queue item hoặc version conflict; catalog #79 chưa liệt kê các mã này.

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
