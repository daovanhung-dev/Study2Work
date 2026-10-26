---
title: "Data Mapping"
order: 5
dd_id: "80"
api_name: "Phê duyệt nội dung"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

0. Xác thực Bearer JWT và role `ADMIN` qua shared guard.
1. Đọc raw `content_id` từ path; catalog không khai báo body hoặc query.
2. Parse signed-int64 sau auth; malformed/out-of-range trả catalog 422 trước DB.
3. Khóa active legacy `contents` row theo ID; thiếu/soft-deleted trả 404.
4. Yêu cầu current status `PENDING_REVIEW`; state khác trả catalog 422.
5. Update status thành `APPROVED`, lấy đúng tám Content fields từ `RETURNING`.
6. Append audit row với actor numeric JWT `sub`, trạng thái cũ/mới và `reason=NULL` trong cùng transaction.
7. Validate response projection, commit sau cùng rồi trả HTTP 200 `DESIGN_RESOURCE_UPDATED` với `ApiEnvelope<Content>`.

## 0. Check quyền

- Dùng `validate_current_user_request(..., role="ADMIN")` trước path parsing và DB access.
- Shared guard trả numeric JWT `sub`; actor audit không đến từ request.
- Role `ADMIN` là local fallback cho catalog Admin requirement. Dedicated moderation permission chưa được xác minh.
- Thiếu/sai Bearer → 401; role không đạt → 403.

## 1. Validate data input

- `content_id` là required signed-int64 path theo catalog; endpoint không nhận body/query.
- Dùng raw path string để parse có kiểm soát sau auth.
- Malformed/out-of-range → 422 `DESIGN_VALIDATION_ERROR` với field `content_id`; không chạm DB.
- Signed-int64 hợp lệ nhưng không khớp active row → 404 theo catalog.

<a id="step-2-get-thong-tin"></a>
## 2. Get và khóa Content

`LOCK_ADMIN_CONTENT_FOR_APPROVAL` đọc `id,status` từ legacy candidate `contents`, điều kiện `id=:content_id AND deleted_at IS NULL`, `FOR UPDATE`.

- Không tìm thấy row active → 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Sai shape/identity/status projection → safe 500.
- Khóa chỉ bảo vệ row hiện tại ở thời điểm #80; request không mang revision ID/expected row version, nên không chứng minh đây là đúng revision mà Admin đã xem ở #79.

## 3. Eligibility và status update

- AC-33 precondition và API #78 queue dùng `PENDING_REVIEW`; API #80 dùng điều kiện này như fallback DERIVED.
- Status hiện tại khác `PENDING_REVIEW` → 422 `DESIGN_VALIDATION_ERROR`; không ghi audit.
- `APPROVE_ADMIN_CONTENT` đổi active row sang `APPROVED`, lặp `deleted_at IS NULL` và `status='PENDING_REVIEW'` trong UPDATE predicate.
- API #52 có transition riêng giữa `APPROVED` và `PUBLISHED`; #80 chọn `APPROVED` làm trạng thái sau review. Lựa chọn này là DERIVED, không phải state policy được owner duyệt.
- `RETURNING` trả `id`, `course_id`, `content_type`, `title`, `payload`, `status`, `parent_id`, `content_order AS order`.

## 4. Append review audit

`INSERT_ADMIN_CONTENT_REVIEW_AUDIT` ghi:

| Binding | Giá trị |
|---|---|
| `content_id` | ID từ path đã parse |
| `actor_user_id` | Numeric JWT `sub` đã xác thực |
| `previous_status` | `PENDING_REVIEW` |
| `new_status` | `APPROVED` |
| `reason` | `NULL` cho approve không có body |

Audit table `content_review_audit_logs` và migration 011 là physical fallback DERIVED theo legacy BIGINT ID. API #81 hiện được wire locally và dùng cùng relation để lưu reason trong một decision row; đây là lựa chọn DERIVED theo candidate schema, vẫn chờ contract owner xác nhận và chưa được kiểm chứng trên DB live.

## 5. Map response

- Reuse API #49 `ContentResponse`, giữ đúng tám field catalog.
- `payload` phải là JSON object; identity/status phải khớp update result; malformed projection → 500 và rollback.
- `content_order` map sang response `order`.
- `parent_id=NULL` bị omit bởi route serialization convention.
- Không trả actor, reason, audit ID, version, author hoặc row-version metadata.

## 6. Transaction và response

- Lock, update, audit insert và response validation dùng cùng caller-owned transaction.
- Chỉ commit sau khi cả Content projection và audit insert thành công.
- Query, projection, audit hoặc commit failure → rollback và safe 500 `DESIGN_INTERNAL_ERROR`.
- Success dùng `DESIGN_RESOURCE_UPDATED`, `data` là Content trực tiếp, `meta={}`, trace ID trong body/header.

## 7. Schema/status boundary

- Runtime query nhắm checked-in legacy BIGINT `contents`; không dùng V1-PILOT UUID `content_review_decisions`.
- Migration 011 và `DB.sql` chỉ là source candidate. Test fake session không xác nhận live tables, FK/indexes, grants hoặc migration deployment.
- API #80 không ghi `content_versions`, không publish notifications và không suy ra original author.

## Liên kết nguồn

- [API catalog #80](../../../../../docs/lists/list_api.md)
- [AC-33 diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [API #52 separate publication flow](../52_mentor_content_publish/02_Overview.md)
- [API #79 revision questions](../79_admin_content_detail/OPEN_QUESTIONS.md)
- [API #81 shared reason boundary](../81_admin_content_reject/OPEN_QUESTIONS.md)
- [Legacy audit migration](../../../../../infra/postgres/study-server/migrations/011_content_review_audit_logs.sql)
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
