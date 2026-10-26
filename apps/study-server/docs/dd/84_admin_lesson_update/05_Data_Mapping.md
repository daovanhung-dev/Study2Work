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
- [2. Validate body fallback](#step-2-check-body-proposal)
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
- Shared auth helper hiện yêu cầu role `ADMIN`; AC-34 lesson-management permission chưa có policy riêng trong Study source.
- Authorize trước khi chạy UPDATE.

### 0.2. Quyền truy cập

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Authorization header | Bearer credential | Token hợp lệ | DIRECT requirement; shared guard đang chạy. |
| Principal policy | Admin role | Principal có role Admin | DIRECT requirement; shared guard kiểm tra role. |
| AC-34 policy | lesson-management permission | Principal được phép quản lý lesson | DIRECT precondition; fine-grained policy chưa có trong current source. |

<a id="step-1-nhan-request"></a>

## 1. Nhận request

### 1.1. Path

- lesson_id lấy từ path và có kiểu int64 theo catalog.
- Không thêm positive/minimum rule vì catalog không nêu.
- Path không parse được/out-of-range trả 422 DESIGN_VALIDATION_ERROR theo catalog PUT #84.

### 1.2. Header và body

- Authorization lấy từ request header.
- X-Trace-Id được current middleware truyền hoặc khởi tạo; không phải input nghiệp vụ.
- JSON body là DERIVED runtime fallback; catalog/diagram chỉ xác nhận path. Content-Type là `application/json`.

<a id="step-2-check-body-proposal"></a>

## 2. Validate body fallback

### 2.1. Candidate full replacement

- `title` là strict string tối đa 200 ký tự theo legacy `VARCHAR(200)` và API #47 precedent; chuỗi rỗng được phép, không trim.
- `content` là required member kiểu string hoặc null; null ghi NULL, omission bị từ chối.
- `video_url` là required member kiểu string hoặc null; null ghi NULL, không có URI/scheme/host validator.
- `order` là strict signed int32; không áp positivity, uniqueness hoặc reorder rule.
- JSON model từ chối member thiếu/sai type/thừa; lỗi trả 422 DESIGN_VALIDATION_ERROR trước UPDATE.
- Không sửa status trong body; state change thuộc API #85.
- Không sửa course_id; chuyển lesson giữa course chưa có contract.
- ID lấy từ path, không duplicate trong body.

<a id="step-3-update-lesson"></a>

## 3. Update lesson

### 3.1. Q1 — Implemented DERIVED UPDATE theo lesson ID

SQL dưới đây là implementation DERIVED trên legacy DDL candidate; fake-session tests xác minh binding/flow nhưng không chứng minh live schema.

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
    l.id,
    l.course_id,
    l.name AS title,
    l.content,
    l.video_url,
    l.sort_order AS "order",
    l.status
```

- :lesson_id bind từ path.
- :title bind từ body `title`.
- :content bind từ body `content`, gồm NULL khi request truyền null.
- :video_url bind từ body `video_url`, gồm NULL khi request truyền null.
- :order bind từ body `order`.
- `updated_at = CURRENT_TIMESTAMP` là DERIVED theo legacy DDL và API #75 precedent; không có lesson trigger trong DDL/migrations đã rà soát.
- WHERE chỉ dùng candidate id; Admin permission phải hoàn tất trước query.
- Không JOIN/sửa courses, resources, progress, audit hoặc bảng khác.
- Không SET status; status transition thuộc #85.
- RETURNING cung cấp response projection, không cần pre-read hoặc query thứ hai.
- View commit sau khi projection Lesson hợp lệ; rollback trên no-row, query/mapping/commit failure.

### 3.2. Query Matrix

| Query | Type | Table | Conditions | Result/status |
|---|---|---|---|---|
| Q1 | UPDATE RETURNING | Legacy lessons AS l | l.id = :lesson_id | Implemented DERIVED one-row update; live schema unknown. |
| Q1 | SET | Legacy lessons AS l | name=:title | DERIVED body-to-column mapping. |
| Q1 | SET | Legacy lessons AS l | content=:content | DERIVED body-to-column mapping. |
| Q1 | SET | Legacy lessons AS l | video_url=:video_url | DERIVED body-to-column mapping. |
| Q1 | SET | Legacy lessons AS l | sort_order=:order | DERIVED body-to-column mapping. |
| Q1 | SET | Legacy lessons AS l | updated_at=CURRENT_TIMESTAMP | DERIVED server timestamp; no trigger found in checked DDL/migrations. |
| Q1 | RETURNING | Legacy lessons AS l | id | Candidate response source. |
| Q1 | RETURNING | Legacy lessons AS l | course_id | Candidate response source; nullable discrepancy. |
| Q1 | RETURNING | Legacy lessons AS l | name | Candidate response source for data.title. |
| Q1 | RETURNING | Legacy lessons AS l | content | Candidate response source. |
| Q1 | RETURNING | Legacy lessons AS l | video_url | Candidate response source. |
| Q1 | RETURNING | Legacy lessons AS l | sort_order | Candidate response source for data.order. |
| Q1 | RETURNING | Legacy lessons AS l | status | Candidate unchanged status response source. |
| Q1 no row | Result branch | UPDATE RETURNING | No returned row | Implemented 404 DESIGN_RESOURCE_NOT_FOUND; rollback. |

### 3.3. Mutation Matrix

| Mutation | Target | Field | Value source | Status |
|---|---|---|---|---|
| M1 UPDATE | lessons candidate | name | Body title | DERIVED; legacy DDL only. |
| M1 UPDATE | lessons candidate | content | Body content | DERIVED; null writes SQL NULL. |
| M1 UPDATE | lessons candidate | video_url | Body video_url | DERIVED; null writes SQL NULL; no URI validation. |
| M1 UPDATE | lessons candidate | sort_order | Body order | DERIVED strict int32; no positivity/uniqueness rule. |
| M1 UPDATE | lessons candidate | updated_at | Server current timestamp | DERIVED; no trigger found in checked repository DDL/migrations. |
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
- Legacy `course_id` có thể NULL nhưng response yêu cầu int64; mapping lỗi trả 500 an toàn, rollback; không thay NULL bằng 0.
- View commit sau khi response Lesson được map; mapping failure không lưu thay đổi.

### 4.2. Không có row

- Không có row từ Q1 -> HTTP 404 DESIGN_RESOURCE_NOT_FOUND; view rollback.
- Soft-delete visibility chưa có policy/marker chung.
- Không đọc resource trước authorization.

### 4.3. Database, mapping hoặc commit failure

- Không trả raw SQL hoặc stack trace.
- Trả 500 DESIGN_INTERNAL_ERROR theo catalog.
- View rollback an toàn trên query, no-row, mapping hoặc commit failure.

### 4.4. Response Source Matrix

| Response field | Candidate source | Transform/null rule | Status |
|---|---|---|---|
| success | Envelope branch | true success / false error | DIRECT shape |
| businessCode | Catalog | Exact code per branch | DIRECT |
| message | Application | `Lesson updated.` on success; safe messages on errors | DERIVED wording |
| data.id | Q1 returned id | Copy | Legacy DDL candidate |
| data.course_id | Q1 returned course_id | Copy; null conflicts with required int64 | Legacy discrepancy; null mapping returns safe 500 |
| data.title | Q1 returned title alias | `name AS title` | API #09 mapping precedent |
| data.content | Q1 returned content | Copy; null preserved as JSON null | Nullable legacy field |
| data.video_url | Q1 returned video_url | Copy; null preserved as JSON null | TEXT/reusable Lesson field; no URI validator |
| data.order | Q1 returned order alias | `sort_order AS "order"` | API #09 mapping precedent |
| data.status | Q1 returned status | Copy unchanged | Enum/casing unresolved |
| meta | Envelope convention | Empty object candidate on success | No API-specific data |
| traceId | Current trace middleware | Propagate or generate UUID | Current-source convention |

### 4.5. Schema boundary

- Catalog/diagram body schema absent; current request/SQL are DERIVED implementation fallback.
- Legacy DDL chỉ là candidate; V1-PILOT dùng UUID/versioned lesson khác biệt.
- Live database/migration state chưa xác minh.
- Focused endpoint tests exercise route and fake-session mapping; live database behavior remains unverified.

<a id="step-5-tra-response"></a>

## 5. Trả response

### 5.1. Thành công

- Trả HTTP 200 DESIGN_RESOURCE_UPDATED khi mutation, mapping và commit thành công.
- Dùng ApiEnvelope<Lesson> trực tiếp theo catalog.
- Không đổi sang Page/array và không thêm audit/dependency fields.
- Theo AC-34, sau success client gọi API #82 để reload danh sách; cardinality và filter `type` của #82 vẫn cần xác nhận.

### 5.2. Lỗi

- 401 DESIGN_AUTHENTICATION_REQUIRED cho authentication failure.
- 403 DESIGN_ACCESS_DENIED cho role/permission denial.
- 404 DESIGN_RESOURCE_NOT_FOUND cho row không tồn tại theo UPDATE.
- 422 DESIGN_VALIDATION_ERROR cho raw path sai và body sai/thiếu/thừa field theo runtime model.
- 500 DESIGN_INTERNAL_ERROR cho DB/mapping/commit failure.
- Current helper trả `data:null` cho error. Xem [06_Error.md](./06_Error.md).

### Request Usage Matrix

| Input | Step/use | Query/mutation/response use | Status |
|---|---|---|---|
| Authorization | 0 | Authenticate/authorize before custom path parse and DB | DIRECT; shared ADMIN role guard |
| lesson_id | 1.1/3.1 | Q1 WHERE; data.id | Type DIRECT; invalid path -> 422 |
| title | 2.1 | Q1 name; data.title | DERIVED, required string <=200 |
| content | 2.1 | Q1 content; data.content | DERIVED, required nullable string |
| video_url | 2.1 | Q1 video_url; data.video_url | DERIVED, required nullable string; no URI check |
| order | 2.1 | Q1 sort_order; data.order | DERIVED, required strict int32 |
| Query parameters | — | None declared | DIRECT absence |
| course_id body | — | Not changed | Excluded; course relation is preserved |
| status body | — | Not changed | Separate API #85 |

### Mục tiêu transaction

- Mutation là một UPDATE statement với RETURNING.
- View sở hữu commit point: commit sau projection hợp lệ; rollback khi lỗi trước hoặc trong commit.
- `query_one` không tự commit; API view sở hữu transaction boundary.

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
