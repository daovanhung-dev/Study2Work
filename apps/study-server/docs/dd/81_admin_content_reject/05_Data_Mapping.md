---
title: "Data Mapping"
order: 5
dd_id: "81"
api_name: "Từ chối nội dung"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

0. FastAPI xác thực JSON body theo `RejectAdminContentRequest`: required strict string `reason`, không nhận field thừa. Thiếu body/field hoặc sai type trả 422 qua DESIGN validation handler.
1. View gọi shared `validate_current_user_request(..., role="ADMIN")` trước raw path parsing và DB access; lấy actor từ numeric JWT `sub`.
2. Parse raw `content_id` thành signed-int64 sau auth; malformed/overflow trả 422 trước query.
3. Khóa active legacy candidate `contents` row theo ID bằng `SELECT ... FOR UPDATE`; không tìm thấy hoặc đã soft-delete trả 404.
4. Yêu cầu `status=PENDING_REVIEW`. State gate này là DERIVED từ AC-33 precondition và #78 queue; state khác trả 422, không ghi mutation.
5. Conditional UPDATE active row từ `PENDING_REVIEW` sang `REJECTED`, trả về đủ tám field Content bằng `RETURNING`.
6. Insert một `content_review_audit_logs` decision row với actor, old/new status và body reason. Đây là physical reason destination và decision record trong cùng một row; không insert thêm audit row thứ hai.
7. Validate response projection, commit sau cùng rồi trả HTTP 200 `DESIGN_RESOURCE_UPDATED` với direct `ApiEnvelope<Content>`; reason không xuất hiện trong response.

<a id="step-0-check-quyen"></a>
## 0. Check quyền

### 0.1. Thực hiện check quyền

- Gọi `validate_current_user_request(authorization, role="ADMIN", ...)`.
- Shared guard xác thực Bearer/JWT và trả numeric subject; actor audit không được lấy từ body.
- Role `ADMIN` là local mapping cho catalog Admin requirement. Dedicated moderation permission chưa có source.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| JWT principal | `roles` | Caller phải có role `ADMIN` | Shared helper hiện thực role check; finer permission chưa được xác nhận. |
| JWT principal | `sub` | Bind làm `actor_user_id` | Numeric actor từ token; không nhận từ request. |

### 0.3. Check kết quả

- Bearer thiếu/sai → 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Role không đạt → 403 `DESIGN_ACCESS_DENIED`.
- Shared ADMIN guard chạy trước raw path parse và database access. FastAPI kiểm tra schema body trước khi vào handler; body errors không truy cập DB.

<a id="step-1-validate"></a>
## 1. Validate data input

- `content_id`: required path signed-int64; view nhận raw string để xác thực sau ADMIN guard. Malformed/overflow → 422 `DESIGN_VALIDATION_ERROR` với field `content_id`.
- `reason`: required strict string trong `RejectAdminContentRequest`; không trim, không giới hạn length, không blank-only check, không reason code.
- Body missing, missing `reason`, non-string `reason`, JSON non-object hoặc extra field → 422 `DESIGN_VALIDATION_ERROR` qua shared `RequestValidationError` handler.
- Empty string được chấp nhận theo fallback giữ nguyên catalog rule “string required”; owner vẫn có thể chốt policy khác.
- Catalog không khai báo query parameters.

<a id="step-2-get-thong-tin"></a>
## 2. Get và khóa Content

`LOCK_ADMIN_CONTENT_FOR_REJECTION` đọc `id,status` từ checked-in legacy candidate `contents`, với điều kiện `id=:content_id AND deleted_at IS NULL`, `FOR UPDATE`.

- Không có active row → rollback và 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Row projection thiếu/sai identity/status type → rollback và safe 500.
- Status hiện tại khác `PENDING_REVIEW` → rollback và 422 `DESIGN_VALIDATION_ERROR`; đây là DERIVED eligibility mapping.
- Khóa chỉ cố định active row tại thời điểm request. #81 không mang revision ID/expected row version nên không chứng minh đây là revision Admin đã xem trong #79.

<a id="step-3-mutation"></a>
## 3. Mutation status và review decision

### 3.1. Conditional status update

`REJECT_ADMIN_CONTENT` chạy khi locked status là `PENDING_REVIEW`:

- Set `contents.status='REJECTED'`.
- Lặp điều kiện `id=:content_id`, `deleted_at IS NULL`, `status='PENDING_REVIEW'` để giữ state predicate.
- `RETURNING id, course_id, content_type, title, payload, status, parent_id, content_order AS order`.
- Không có returned row → rollback và catalog 404.

### 3.2. Persist reason and decision

`INSERT_ADMIN_CONTENT_REVIEW_DECISION` ghi một row vào `content_review_audit_logs`:

| Binding | Giá trị |
|---|---|
| `content_id` | Path ID đã parse |
| `actor_user_id` | Numeric JWT `sub` sau shared ADMIN guard |
| `previous_status` | Locked status `PENDING_REVIEW` |
| `new_status` | `REJECTED` |
| `reason` | Body reason giữ nguyên |
| `recorded_at` | Database default `CURRENT_TIMESTAMP` |

Migration 011/legacy `DB.sql` cung cấp BIGINT FKs và nullable `reason` candidate. Reusing this row for #81 is DERIVED from the direct logical reason requirement and the absence of a reason column on `contents`; it is not live schema proof. One row persists the reason and decision, with no second audit append.

<a id="step-4-result"></a>
## 4. Map response, commit và xử lý lỗi

- Reuse API #49 `ContentResponse`; require matching Content ID, resulting status `REJECTED`, object payload and all eight catalog fields.
- `content_order` maps to response `order`; `parent_id=NULL` is omitted by route serialization.
- Validate response before commit. The status update and reason-bearing decision insert share one transaction; commit only after both writes and projection succeed.
- Query, audit insert, malformed projection or commit failure → rollback and safe 500 `DESIGN_INTERNAL_ERROR`.
- Missing/non-pending targets roll back the row-lock transaction and return catalog 404/422 respectively.
- Success returns HTTP 200 `DESIGN_RESOURCE_UPDATED`, direct Content data, `meta={}` and trace ID in envelope/header. Reason, reviewer, audit ID, version and author are not returned.

## Schema and lifecycle boundary

- Runtime targets checked-in legacy BIGINT `contents`; V1-PILOT UUID decisions are not used.
- No new table, column, migration or `content_versions` write is introduced by #81.
- `REJECTED` leaves the #78 `PENDING_REVIEW` predicate; this is why a reloaded queue excludes the row. Publish/delete policy for rejected Content remains open.
- Migration 011 and fake-session tests do not prove live schema, migration deployment, FKs, grants or concurrency in PostgreSQL.

## Liên kết nguồn và điểm còn mở

- [API catalog #81](../../../../../docs/lists/list_api.md)
- [AC-33 diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [API #78 queue predicate](../78_admin_content_pending/05_Data_Mapping.md)
- [API #79 revision questions](../79_admin_content_detail/OPEN_QUESTIONS.md)
- [API #80 approval transaction](../80_admin_content_approve/05_Data_Mapping.md)
- [Legacy audit migration](../../../../../infra/postgres/study-server/migrations/011_content_review_audit_logs.sql)
- [Open questions #81](./OPEN_QUESTIONS.md)
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
