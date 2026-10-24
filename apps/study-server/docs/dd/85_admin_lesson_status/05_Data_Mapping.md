---
title: "Data Mapping"
order: 5
dd_id: "85"
api_name: "Đổi trạng thái lesson"
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
- [2. Check status proposal](#step-2-check-status-proposal)
- [3. Update và audit](#step-3-update-audit)
- [4. Check kết quả và map response](#step-4-check-ket-qua-va-map-response)
- [5. Trả response](#step-5-tra-response)
- [Requirement Matrix](#requirement-matrix)
- [Request Usage Matrix](#request-usage-matrix)
- [Query Matrix](#query-matrix)
- [Mutation Matrix](#mutation-matrix)
- [Response Source Matrix](#response-source-matrix)

<a id="step-0-check-quyen"></a>

## 0. Check quyền

### 0.1. Authenticate và authorize

- Xác thực Bearer JWT theo catalog.
- Yêu cầu role Admin theo catalog.
- Yêu cầu lesson-management permission theo AC-34.
- Credential thiếu/sai/hết hạn → HTTP 401 DESIGN_AUTHENTICATION_REQUIRED.
- Thiếu role/permission → HTTP 403 DESIGN_ACCESS_DENIED.
- Current Study auth helper chỉ có Student guard; Admin claim, permission provider và guard chưa có.
- Authorize trước khi truy vấn hoặc mutation.
- Actor subject dùng cho audit phải lấy từ principal đã authorize; claim mapping SOURCE_REQUIRED.

### 0.2. Quyền truy cập

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Authorization header | Bearer credential | Token hợp lệ | DIRECT requirement; route chưa có. |
| Principal policy | Admin role | Principal có role Admin | DIRECT requirement; claim source chưa có. |
| AC-34 policy | lesson-management permission | Principal được phép quản lý lesson | DIRECT precondition; implementation SOURCE_REQUIRED. |
| Audit actor | Admin subject ID | Được map từ principal | Audit intent cần actor; physical claim mapping SOURCE_REQUIRED. |

<a id="step-1-nhan-request"></a>

## 1. Nhận request

### 1.1. Path

- lesson_id lấy từ path và có kiểu int64 theo catalog.
- Không thêm positive/minimum rule vì catalog không nêu.
- Path không parse được/out-of-range có thể map 422 DESIGN_VALIDATION_ERROR theo error set; chi tiết cần xác nhận.

### 1.2. Header và body

- Authorization lấy từ request header.
- X-Trace-Id được current middleware truyền hoặc khởi tạo; không phải input nghiệp vụ.
- Catalog/diagram không khai báo body hoặc Content-Type.
- JSON object có field status là DERIVED proposal để nêu trạng thái đích; không phải contract đã duyệt.
- Không có query parameter.

<a id="step-2-check-status-proposal"></a>

## 2. Check status proposal

- status phải chỉ định một target theo LessonStatus sau khi owner cung cấp enum/casing.
- Catalog/diagram/reusable Lesson không liệt kê các enum member.
- Legacy DDL đặt default DRAFT nhưng không xác nhận DRAFT là target được chấp nhận hoặc là tập trạng thái đầy đủ.
- Không tạo whitelist, transition matrix, readiness gate hoặc side effect cho enrollment/content.
- Thiếu/sai target có thể map 422 DESIGN_VALIDATION_ERROR; code là DIRECT, điều kiện cụ thể SOURCE_REQUIRED.
- Same-status request, retry và idempotency behavior cần xác nhận.
- Validate input trước mutation; validator không truy vấn DB hay ghi audit theo Study convention.

<a id="step-3-update-audit"></a>

## 3. Update và audit

### 3.1. M1 — Candidate UPDATE theo lesson ID

SQL dưới đây chỉ là proposal trên legacy DDL; chưa chạy và không chứng minh live schema.

```sql
UPDATE lessons AS l
SET
    status = :status,
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

- :lesson_id bind từ path; :status bind từ request proposal.
- Chỉ đổi status và updated_at candidate; giữ nguyên relation, metadata, dependencies và progress.
- updated_at tồn tại trong legacy DDL; cập nhật bằng server time là DERIVED và cần xác nhận trigger/owner khác.
- WHERE predicate, table và returned columns là candidate từ legacy schema; live target chưa được chọn.
- Không có row trả về → candidate 404 DESIGN_RESOURCE_NOT_FOUND.
- Transaction commit/rollback thuộc caller/use case theo DB helper convention; API #85 caller chưa tồn tại.

### 3.2. M2 — Audit theo AC-34

- AC-34 diagram yêu cầu “UPDATE status + audit”; logical audit event là DIRECT intent.
- Legacy Study DDL không có audit relation.
- V1-PILOT có audit_events, nhưng pilot lessons.id là UUID và không có status field; audit resource_id cũng là UUID.
- Không viết INSERT, action name, old/new payload hoặc khóa resource giả định.
- Physical audit relation, actor/resource key mapping, status before/after, trace binding và append-only policy đều SOURCE_REQUIRED.
- DERIVED proposal: chỉ hoàn tất success khi status change và audit được lưu cùng transaction theo schema đã duyệt.
- DERIVED failure handling: nếu audit hoặc response projection thất bại sau mutation, rollback candidate và trả 500 DESIGN_INTERNAL_ERROR; transaction owner cần được chốt.
- Current helper query_one/query_many không commit; caller sở hữu transaction.

### 3.3. Query Matrix

| Query | Type | Table/source | Conditions/effect | Result/status |
|---|---|---|---|---|
| M1 | UPDATE RETURNING | Legacy lessons candidate | id = :lesson_id; SET status, candidate updated_at | One updated Lesson candidate; live schema unknown. |
| M2 | Logical audit append | No approved compatible relation | Admin changes lesson status | Diagram intent DIRECT; physical mapping SOURCE_REQUIRED; no SQL guessed. |
| M1 no row | Result branch | UPDATE RETURNING | No returned lesson | Candidate 404 DESIGN_RESOURCE_NOT_FOUND. |
| Other queries | None | Courses/dependencies/progress | No join, count or bulk scan | Not requested by status branch. |

### 3.4. Mutation Matrix

| Mutation | Target | Field/effect | Value source | Status |
|---|---|---|---|---|
| M1 UPDATE | Legacy lessons candidate | status | Body status proposal | Logical status change DIRECT; physical candidate DERIVED. |
| M1 UPDATE | Legacy lessons candidate | updated_at | Server current timestamp | DERIVED; timestamp ownership/live schema unresolved. |
| M2 audit append | Logical audit event | Record Admin status action | AC-34 | DIRECT intent; physical mapping SOURCE_REQUIRED. |
| No mutation | Lesson metadata/dependencies/progress | Preserve without cascade | N/A | Scope boundary; no policy supports writes. |

<a id="step-4-check-ket-qua-va-map-response"></a>

## 4. Check kết quả và map response

### 4.1. Có row trả về

- Khi UPDATE RETURNING trả đúng một row và response fields map được, tạo một Lesson.
- data.id = row.id.
- data.course_id = row.course_id; không đổi relation.
- data.title = row.name.
- data.content = row.content.
- data.video_url = row.video_url.
- data.order = row.sort_order.
- data.status = row.status sau update.
- Legacy course_id có thể NULL nhưng reusable Lesson yêu cầu int64; không map NULL thành 0.
- content/video_url nullable; null-versus-omit serialization cần xác nhận.
- Không trả audit record trong Lesson response.
- Audit phải được ghi thành công trong cùng transaction trước khi success được commit.

### 4.2. Không có row

- Không có row từ M1 → candidate HTTP 404 DESIGN_RESOURCE_NOT_FOUND.
- Soft-delete visibility chưa có policy/marker chung.
- Không đọc lesson trước authorization.

### 4.3. Database hoặc mapping failure

- Không trả raw SQL hoặc stack trace.
- Trả HTTP 500 DESIGN_INTERNAL_ERROR theo catalog.
- Rollback status nếu audit, projection, mapping hoặc commit thất bại; transaction owner chưa xác nhận implementation.

### 4.4. Response Source Matrix

| Response field | Candidate source | Transform/null rule | Status |
|---|---|---|---|
| success | Envelope branch | true success / false error | DIRECT reusable envelope shape |
| businessCode | Catalog | Exact code per branch | DIRECT |
| message | Application | Safe text; exact text unspecified | DERIVED wording |
| data.id | M1 returned id | Copy | Legacy candidate |
| data.course_id | M1 returned course_id | Copy; NULL conflicts with required int64 | Legacy discrepancy |
| data.title | M1 returned name | Alias name → title | Legacy candidate; API #09 precedent |
| data.content | M1 returned content | Copy; null/omit unresolved | Nullable candidate |
| data.video_url | M1 returned video_url | Copy; URI/null/omit unresolved | TEXT candidate |
| data.order | M1 returned sort_order | Alias sort_order → order | Legacy candidate; API #09 precedent |
| data.status | M1 returned status | Copy updated value | Contract field DIRECT; enum/casing unresolved |
| meta | Envelope convention | Empty object candidate on success | No API-specific data |
| traceId | Current trace middleware | Propagate or generate UUID | Current-source convention |

### 4.5. Schema boundary

- Catalog request body absent; candidate status field is not an implementation contract.
- Legacy BIGINT lesson schema and V1-PILOT UUID/versioned lesson schema are distinct.
- Legacy status column supports only a physical candidate; status values/transitions remain unknown.
- Audit storage cannot be paired with the selected lesson schema from current checked-in artifacts.
- No live-schema metadata, route, migration deployment or SQL execution is claimed.

<a id="step-5-tra-response"></a>

## 5. Trả response

- Thành công: HTTP 200, businessCode DESIGN_RESOURCE_UPDATED, một ApiEnvelope<Lesson>.
- Errors: preserve exact catalog statuses/codes 401/403/404/422/500.
- Error guideline yêu cầu data:null; current Study error_response defaults absent data thành {}. Đây là discrepancy khi tích hợp.
- Trace ID tuân theo middleware convention.
- Sau success, UI reload danh sách lesson theo AC-34.

## Requirement Matrix

| Requirement | Source | Status |
|---|---|---|
| PATCH status path, Bearer JWT, Admin, required path int64 | API #85 catalog | DIRECT |
| Lesson envelope and 200 update code | API #85 catalog | DIRECT |
| Exact 401/403/404/422/500 codes | API #85 catalog | DIRECT |
| Admin lesson-management permission | AC-34 precondition | DIRECT intent; policy source absent |
| Update status plus audit, then reload list | AC-34 nodes n9/n10/n13 | DIRECT intent |
| Body status field and JSON content type | Needed target for PATCH; absent from catalog/diagram | DERIVED proposal |
| Enum members, casing, transition/no-op/retry rules | Not defined by sources | SOURCE_REQUIRED |

## Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Bearer JWT | Admin authorization and audit actor candidate | DIRECT; claims/policy mapping SOURCE_REQUIRED |
| lesson_id | Required path int64 | M1 predicate and data.id | DIRECT type; legacy mapping candidate |
| Body status | Candidate JSON target | M1 SET and data.status | DERIVED; enum and validation SOURCE_REQUIRED |
| Query parameters | None | None | Direct absence |
| X-Trace-Id | Current middleware | Envelope/audit correlation candidate | Current-source convention; audit storage unknown |

## Query Matrix

| Step | Type | Source/target | Purpose/status |
|---|---|---|---|
| M1 | UPDATE RETURNING | Legacy lessons candidate | Change status by id; physical schema candidate, live schema unknown |
| M2 | Logical audit append | No approved physical source | Required by diagram; physical mapping SOURCE_REQUIRED |
| No-row branch | Result check | M1 result | Candidate 404 |
| No additional query | No dependency/list/progress query | N/A | Not required by status branch |

## Mutation Matrix

| Operation | Target | Condition | Fields/effect | Status |
|---|---|---|---|---|
| M1 UPDATE | Legacy lessons candidate | id = :lesson_id | Set status and candidate updated_at; preserve remaining lesson fields | DERIVED physical mapping |
| M2 audit append | Logical audit event | Accepted status change | Record Admin status operation | Direct intent; physical schema SOURCE_REQUIRED |
| Bulk/dependency mutation | None | No source condition | No cascade to resources/progress/enrollment | Out of scope |

## Response Source Matrix

| Response field | Candidate source/transform | Gap/status |
|---|---|---|
| HTTP status/businessCode | API #85 catalog | Exact set is DIRECT |
| data | One returned Lesson | ApiEnvelope<Lesson> DIRECT |
| data.id/course_id | Legacy lessons id/course_id | Candidate; nullable course_id discrepancy |
| data.title | Legacy name → title | Candidate alias |
| data.content/video_url | Legacy matching columns | Candidate; null/omit unresolved |
| data.order | Legacy sort_order → order | Candidate alias |
| data.status | Updated row status | Direct response field; enum/casing unknown |
| meta/traceId | Envelope and current middleware | Empty meta candidate; current trace convention |

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
