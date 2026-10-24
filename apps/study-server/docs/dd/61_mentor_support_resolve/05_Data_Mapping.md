---
title: "Data Mapping"
order: 5
dd_id: "61"
api_name: "Đóng yêu cầu hỗ trợ"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

## Mục lục

- [1. Nhận metadata request](#step-1)
- [2. Kiểm tra quyền Mentor](#step-2)
- [3. Đọc và kiểm tra request_id](#step-3)
- [4. Đọc SupportRequest và trạng thái](#step-4)
- [5. Resolve request](#step-5)
- [6. Nạp lại response](#step-6)
- [7. Giao dịch và trả kết quả](#step-7)
- [8. Xử lý lỗi](#step-8)

<a id="step-1"></a>

## 1. Nhận metadata request

### 1.1. Xác thực Bearer JWT

- Đọc `Authorization` theo contract.
- Token thiếu/không hợp lệ → 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Catalog yêu cầu role Mentor; Study hiện chỉ có guard Student dùng bởi API khác. Mentor claim/subject mapping còn `SOURCE_REQUIRED`.

### 1.2. Nhận trace ID

- Đọc `X-Trace-Id` nếu client gửi theo API Guidelines.
- Khi được wired, propagate trace đã được middleware xác thực hoặc trace middleware tạo vào envelope/header.
- Đây là convention; API #61 hiện chưa có route.

<a id="step-2"></a>

## 2. Kiểm tra quyền Mentor

### 2.1. Xác nhận role

- Role khác Mentor hoặc thiếu quyền → 403 `DESIGN_ACCESS_DENIED`.
- Không dùng Student guard hiện hành như bằng chứng cho Mentor.

### 2.2. Giới hạn request theo scope

- AC-24 yêu cầu request thuộc phạm vi phụ trách của Mentor.
- Candidate đơn giản theo V1-PILOT là request được gán trực tiếp qua `assigned_to_subject_id`; subject mapping và cột này chưa được chọn làm predicate runtime.
- Request tồn tại nhưng ngoài scope → candidate 403; request không tồn tại → 404 theo catalog. Thứ tự check cần xác nhận nếu phải tránh resource enumeration.
- Không dùng `request_id` làm bằng chứng ownership.

<a id="step-3"></a>

## 3. Đọc và kiểm tra `request_id`

### 3.1. Path parameter

| Item | Type contract | Candidate source | Rule | Status |
|---|---|---|---|---|
| `request_id` | required int64 | No approved physical key; V1-PILOT `support_tickets.id` UUID | Dùng làm logical key duy nhất cho SupportRequest | Type DIRECT; physical mapping SOURCE_REQUIRED |

- Thiếu, sai kiểu hoặc overflow int64 → 422 `DESIGN_VALIDATION_ERROR` theo contract #61.
- Không thêm positive/minimum constraint vì catalog không khai báo.
- Không cast UUID candidate thành int64.

<a id="step-4"></a>

## 4. Đọc SupportRequest và trạng thái

### 4.1. Q1 — Request scope/existence/current status

| Target | Candidate fields | Điều kiện logic | Trạng thái |
|---|---|---|---|
| V1-PILOT `support_tickets` (candidate only) | `id`, `status`, `assigned_to_subject_id`, `resolved_at` | Tìm request theo logical ID và xác minh assignment Mentor | `SOURCE_REQUIRED`; ID UUID và subject mapping chưa khớp contract |

- Legacy Study DB/ERD không có support relation.
- Không viết SQL vật lý trước khi owner chọn schema và ID mapping.
- Không đọc/ghi `support_messages` ở bước này ngoài projection response sau khi đã kiểm soát scope.

<a id="step-5"></a>

## 5. Resolve request

### 5.1. M1 — State transition proposal

| Current status | Action | Result | Basis/status |
|---|---|---|---|
| `OPEN` | Cập nhật request status | `RESOLVED` | AC-24 direct status labels; pilot persistence candidate |
| `RESOLVED` | Không UPDATE, giữ timestamp ban đầu | Trả success idempotent | DERIVED — retry behavior cần xác nhận |
| Khác `OPEN`/`RESOLVED` | Không UPDATE | 422 `DESIGN_VALIDATION_ERROR` | DERIVED — allowed state set chưa được duyệt |

- Nhánh YES của AC-24 gọi #61 và cập nhật status `RESOLVED`.
- Nhánh NO không gọi #61; request giữ `OPEN` sau #60 theo diagram.
- Cách xử lý state ngoài OPEN/RESOLVED chỉ là proposal để dùng code 422 đã có trong catalog; không coi pilot enum là SupportStatus contract.

### 5.2. M1 — Ghi trạng thái và thời gian

- Khi request đang OPEN, ghi `status = RESOLVED`.
- Đề xuất gán `resolved_at` bằng thời gian hiện tại của server/DB ở lần chuyển trạng thái đầu tiên.
- Khi request đã RESOLVED, không ghi lại `resolved_at` để retry không thay thời điểm xử lý ban đầu.
- Không đặt `resolution_code`; API không nhận reason và sơ đồ không yêu cầu.
- Physical candidate `support_tickets.status/resolved_at` và trigger `updated_at/row_version` chỉ mô tả V1-PILOT, chưa phải runtime mapping.

### 5.3. Đồng thời và transaction

- Đề xuất kiểm tra trạng thái và ghi trong một transaction caller-owned.
- Để hai request resolve đồng thời không ghi đè timestamp, implementation có thể khóa dòng hoặc dùng conditional update rồi nạp lại trạng thái; chọn cơ chế sau khi schema runtime được duyệt.
- Nếu lỗi xảy ra trước commit, rollback trạng thái. Nếu state đã RESOLVED do request song song, trả kết quả thành công idempotent theo proposal.
- Đây là DERIVED transaction/concurrency behavior; API #61 hiện không có code.

<a id="step-6"></a>

## 6. Nạp lại response

### 6.1. Q2 — SupportRequest projection

- Nạp lại một `SupportRequest` sau update; status success phải là `RESOLVED`.
- Reuse projection logic ở API #59/#60; không tạo schema response riêng cho #61.
- Giữ thread hiện tại; #61 không insert/update/delete `SupportMessage`.
- `data.course_id`, `student`, author, attachment URL/status và numeric IDs vẫn `SOURCE_REQUIRED` do physical model/resolver chưa được duyệt.
- `resolved_at` lấy từ cột được duyệt nếu có; policy null/omit/timezone chưa chốt.

<a id="step-7"></a>

## 7. Giao dịch và trả kết quả

- Sau khi status change và full response projection thành công, trả HTTP 200 `DESIGN_RESOURCE_UPDATED` với `ApiEnvelope<SupportRequest>`.
- `message` là text an toàn, không lộ SQL, token hay internal detail; câu chữ chính xác chưa thuộc contract.
- Caller sở hữu commit/rollback theo DB helper convention. Không có API #61 source/runtime hiện tại.

<a id="step-8"></a>

## 8. Xử lý lỗi

- Bearer thiếu/invalid → 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Sai role hoặc request ngoài scope → 403 `DESIGN_ACCESS_DENIED`.
- Request không tồn tại → 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Path không parse được hoặc state ngoài allowed set theo DERIVED proposal → 422 `DESIGN_VALIDATION_ERROR`.
- DB/update/reload failure → 500 `DESIGN_INTERNAL_ERROR`; không trả stack trace.
- Không thêm 409 hoặc 503.
- Catalog không nêu check order của 403/404; giữ câu hỏi privacy trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

## Mapping table

- Candidate UPDATE mapping: [07_table.md](./07_table.md).
- API #61 không ghi SupportMessage; reply INSERT do [API #60](../60_mentor_support_reply/05_Data_Mapping.md) sở hữu.
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
