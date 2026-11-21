---
title: "Data Mapping"
order: 5
dd_id: "99"
api_name: "Điều chỉnh trạng thái kiểm duyệt discussion"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

```text
Admin Bearer JWT
  -> xác thực principal và role Admin [DIRECT contract; guard SOURCE_REQUIRED]
  -> validate discussion_id, action, reason [fields DIRECT; detailed rules SOURCE_REQUIRED]
  -> tìm discussion được chọn [legacy discussions candidate]
  -> cập nhật logical moderation state + ghi logical audit [AC-37 DIRECT; physical mapping SOURCE_REQUIRED]
  -> tạo ApiEnvelope<Page<Discussion>> [DIRECT response; pagination proposal DERIVED]
  -> Admin chọn tiếp API #100 nếu cần delete, hoặc kết thúc [AC-37 DIRECT flow]
```

API #99 không thực hiện DELETE. Không có query report/detail trong request; `reason` là audit context của hành động moderation, không phải filter của API #97.

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Catalog yêu cầu Bearer JWT và role Admin.
- Current `validate_current_user_request` chỉ chấp nhận Student; không dùng helper đó như Admin authorization.
- JWT claim format, Admin subject mapping, permission scope và concealment policy chưa có Study source.

### 0.2. Query/check quyền

| Check | Candidate source | Rule | Status |
|---|---|---|---|
| Authenticate token | Bearer JWT | Token phải hợp lệ | DIRECT auth mechanism; exact Admin token policy `SOURCE_REQUIRED` |
| Authorize role | Admin claims/policy | Principal phải có role Admin | DIRECT role; claim spelling/policy `SOURCE_REQUIRED` |
| Resolve actor ID for audit | Admin principal | Map actor to audit identity | `SOURCE_REQUIRED`; no physical mapping selected |

Không có SQL access-check được catalog hoặc AC-37 định nghĩa. Không thêm tenant/permission predicate.

### 0.3. Check kết quả

- Thiếu/sai authentication có thể dùng 401 `DESIGN_AUTHENTICATION_REQUIRED` theo catalog; xem [06_Error.md](./06_Error.md).
- Principal đã xác thực nhưng không phải Admin có thể dùng 403 `DESIGN_ACCESS_DENIED` theo catalog; xem [06_Error.md](./06_Error.md).
- Cách xử lý identity/policy lỗi nội bộ chưa được định nghĩa ngoài 500 catalog.

## 1. Validate data input

| Input | Direct rule | Unresolved rule |
|---|---|---|
| `discussion_id` | Required path, int64 | Parse overflow/malformed path-to-code mapping |
| `action` | Required body string | Allowed tokens, case, blank handling, transition eligibility |
| `reason` | Required body string | Blank handling, length, taxonomy, normalization and audit redaction |

Catalog cho phép 422 `DESIGN_VALIDATION_ERROR`; không suy ra min/max, state precondition hoặc field-error shape riêng.
Chi tiết error contract: [06_Error.md](./06_Error.md).

## 2. Get thông tin

### 2.1. Query

| Query | Operation | Candidate table | Candidate fields | Purpose / status |
|---|---|---|---|---|
| Q1 | SELECT | Legacy `discussions AS d` | `d.id` | Candidate target key; legacy artifact only, not live-schema proof |
| Q1 | SELECT | Legacy `discussions AS d` | `d.course_id` | Candidate Discussion field; nullable in legacy DDL |
| Q1 | SELECT | Legacy `discussions AS d` | `d.user_id` | Candidate author key; nullable in legacy DDL |
| Q1 | SELECT | Legacy `discussions AS d` | `d.parent_id` | Candidate thread parent; nullable in legacy DDL |
| Q1 | SELECT | Legacy `discussions AS d` | `d.content` | Candidate Discussion content |
| Q1 | SELECT | Legacy `discussions AS d` | `d.status` | Candidate state field; approved moderation values unresolved |
| Q1 | SELECT | Legacy `discussions AS d` | `d.created_at` | Candidate timestamp; timezone convention unresolved |
| Q1 | SELECT | Legacy `discussions AS d` | `d.updated_at` | Candidate timestamp; update behavior not specified |
| Q2 | SELECT | Report relation | No approved table/key/columns | #99 request does not include report fields; no report query is specified |
| Q3 | SELECT | Candidate `users AS u` | `u.id` | Candidate author identifier; join and null policy unresolved |
| Q3 | SELECT | Candidate `users AS u` | `u.full_name` | Candidate author field; live schema unknown |
| Q3 | SELECT | Candidate `users AS u` | `u.avatar_url` | Optional response field candidate; null serialization unresolved |
| Q3 | SELECT | Child `discussions AS c` | `c.id` | Candidate comment identifier; membership unresolved |
| Q3 | SELECT | Child `discussions AS c` | `c.parent_id` | Candidate parent linkage; root/reply policy unresolved |
| Q3 | SELECT | Child `discussions AS c` | `c.content` | Candidate comment content |
| Q3 | SELECT | Child `discussions AS c` | `c.user_id` | Candidate comment author key; nullable in legacy DDL |
| Q3 | SELECT | Child `discussions AS c` | `c.created_at` | Candidate comment timestamp; order/timezone unresolved |

Q1 predicate `d.id = :discussion_id` is a candidate target lookup. It does not establish whether the path may identify a root, reply, hidden or locked discussion.
If Q1 finds no target row, 404 `DESIGN_RESOURCE_NOT_FOUND` is the catalogued code; row-missing-to-404 is a candidate mapping in [06_Error.md](./06_Error.md).

### 2.2. JOIN

- Discussion author projection would require a candidate relation from `discussions.user_id` to `users.id`; both join null policy and full live schema remain unverified.
- Comment projection is required by reusable `Discussion`; AC-37 Admin visibility must not inherit the Student `ACTIVE` filter from API #42 without an approved policy.
- No report relation is present in legacy DDL. AC-37 report detail belongs to the surrounding flow and is not a #99 response field.

### 2.3. WHERE

| Predicate | Basis | Status |
|---|---|---|
| Target ID equals path `discussion_id` | Natural candidate for path-targeted mutation | `DERIVED`; physical query not approved |
| Eligible moderation state | No state precondition in catalog or AC-37 | `SOURCE_REQUIRED` |
| Root-only versus reply target | #97/#98 do not settle queue grain | `SOURCE_REQUIRED` |
| Visibility/locked/deleted filtering | No rule for Admin moderation target | `SOURCE_REQUIRED` |

No state predicate may be added as an implementation requirement until approved.

### 2.4. ORDER BY

The target lookup is by path ID. Ordering of Discussion comments in the response is not defined; do not invent a timestamp/id ordering.

## 3. Insert/Update thông tin

### 3.1. Target table

| Logical operation | Candidate physical target | Status |
|---|---|---|
| Update moderation state | `discussions` is a candidate row source; `status` is a candidate column | Logical UPDATE direct from AC-37; physical write mapping `SOURCE_REQUIRED` |
| Record moderation audit | No approved legacy target | Logical audit direct from AC-37; physical table/fields `SOURCE_REQUIRED` |
| Delete discussion | None in this API | Separate API #100 only |

Candidate table and unresolved physical columns: [07_table.md](./07_table.md).

### 3.2. Conditions

- AC-37 direct flow names the logical actions ẩn/khóa/cảnh báo and requires moderation state plus audit.
- Tokens `hide|lock|warn` are `DERIVED` discussion examples only; exact request enum and casing remain open.
- State value and transition for each action are not defined. Legacy `status VARCHAR(20) DEFAULT 'ACTIVE'` does not define moderation tokens.
- Whether `warn` changes discussion state, creates another user-facing notice, or only writes audit is `SOURCE_REQUIRED`.
- Whether report/decision and state/audit writes must be atomic is `SOURCE_REQUIRED`.

### 3.3. Items update/insert

| Logical data | Input/source | Intended effect | Status |
|---|---|---|---|
| Moderation decision | `action` | Select one approved moderation outcome | Direct field; allowed values unresolved |
| Moderation reason | `reason` | Record why Admin selected the action | Direct field; persistence/constraints unresolved |
| Admin actor | Authenticated principal | Attribute the moderation event | Admin role direct; identity mapping unresolved |
| Discussion before/after state | Target Discussion | Preserve state change for response/audit | Physical fields and snapshot semantics unresolved |
| Trace identifier | Current request | Correlate response and audit if approved | Envelope convention; audit storage unresolved |

No physical UPDATE or INSERT statement is specified until the state enum and audit relation are approved. Candidate pilot `admin_adjustments`/`audit_events` use UUID keys and do not establish compatibility with legacy BIGINT `discussions`.
See [07_table.md](./07_table.md) for the separate state and audit field mapping gaps.

### 3.4. Parameters

| Parameter | Value/source | Purpose | Status |
|---|---|---|---|
| `discussion_id` | Path int64 | Select target | DIRECT input; physical key mapping candidate |
| `action` | Body string | Requested moderation action | DIRECT input; accepted value unresolved |
| `reason` | Body string | Moderation reason | DIRECT input; exact constraints unresolved |
| `admin_actor` | Admin JWT principal | Authorize and attribute audit | Role direct; claim/identity mapping unresolved |
| `trace_id` | Request trace | Envelope correlation | Common convention; audit mapping unresolved |

## 4. Check kết quả execute query

### 4.1. Thành công

- HTTP 200 with `DESIGN_RESOURCE_UPDATED` is direct from catalog.
- Return `ApiEnvelope<Page<Discussion>>`; preserve the exact generic response type.
- A Page containing the updated Discussion is a `DERIVED` proposal. Whether action `warn` leaves state unchanged and still returns a Discussion is unresolved.
- One-item pagination values `page=1`, `size=1`, `total=1`, `total_pages=1` are not approved contract values.
- Do not expose `action`, `reason`, report fields, audit fields or an ActionResult unless catalog changes.
- Field-level mapping: [04_Response.md](./04_Response.md).

### 4.2. Lỗi hệ thống

- Persistence, audit, query or response-mapping failure may use 500 `DESIGN_INTERNAL_ERROR` from the catalog.
- Transaction boundary and rollback behavior across state/audit writes are unresolved.
- Current middleware path allowlist excludes #99; a future route must be integrated with the design-code mapping to retain catalog 422/500 codes.
- Error cases: [06_Error.md](./06_Error.md).

### 4.3. Validate lỗi

- Required path/body shape and any approved action/reason rule may map to 422 `DESIGN_VALIDATION_ERROR`.
- Do not add blank-only, length, format, taxonomy, invalid-state or malformed-path rules without an approved source.
- Error detail fields should follow the shared API guideline when the endpoint is implemented.
- Error cases: [06_Error.md](./06_Error.md).

### 4.4. Ngoài trường hợp trên

- Do not return business codes outside the catalog set for this API.
- The shared guideline expects error `data:null`; current `error_response` defaults absent error data to `{}`. API #99 is not wired, so this is a conditional integration discrepancy.
- A delete choice continues to API #100; no delete side effect belongs here.
- Catalogued errors: [06_Error.md](./06_Error.md).

## Liên kết nguồn và điểm còn mở

- [AC-37 diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [API #97 report filter](../97_admin_discussions_reported/03_Request.md)
- [API #98 moderation detail questions](../98_admin_discussions_detail/OPEN_QUESTIONS.md)
- [API #42 Page precedent](../42_discussions_detail/04_Response.md)
- [Open questions #99](./OPEN_QUESTIONS.md)

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
