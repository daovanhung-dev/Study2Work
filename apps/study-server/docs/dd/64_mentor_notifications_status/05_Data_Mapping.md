---
title: "Data Mapping"
order: 5
dd_id: "64"
api_name: "Theo dõi trạng thái gửi"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Luồng xử lý thiết kế

1. Xác thực Bearer JWT và role Mentor.
2. Đọc `notification_id` từ path theo kiểu `int64`.
3. Xác định notification và kiểm tra caller có quyền xem; permission relation chưa có nguồn.
4. Đọc delivery state đã lưu theo notification; physical source/query chưa được phê duyệt. GET không gọi lại Push/Email.
5. Ánh xạ response theo `ApiEnvelope<Operation>` direct; hiện không có mapping từ notification delivery sang Operation.
6. Trả HTTP 200 khi resource/status được đọc; các lỗi dùng đúng catalog 401/403/404/500.

### Mục lục

- [0. Xác thực](#step-0-auth)
- [1. Nhận request](#step-1-request)
- [2. Kiểm tra resource và quyền](#step-2-access)
- [3. Đọc delivery state](#step-3-read-delivery)
- [4. Map response](#step-4-map-response)
- [5. Trả response/lỗi](#step-5-response-errors)

<a id="step-0-auth"></a>

## 0. Xác thực

- Thiếu hoặc token Bearer/JWT không hợp lệ → 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Token hợp lệ nhưng role không phải Mentor → 403 `DESIGN_ACCESS_DENIED`.
- Không lấy owner/sender ID từ request; principal claim và kiểu ID số chưa có Mentor runtime source.
- Không đọc delivery data trước khi hoàn tất authorization.

<a id="step-1-request"></a>

## 1. Nhận request

| Field | Kiểu trực tiếp | Sử dụng | Validation/status |
|---|---|---|---|
| `notification_id` | int64! path | Khóa logic để xác định notification/status | Kiểu DIRECT; không có range khác; physical key SOURCE_REQUIRED. |
| Body/query | Không khai báo | Không có | DIRECT từ catalog. |

- Nếu path không parse được thành int64, catalog chưa khai báo HTTP/business mapping riêng; không tự thêm 400/422.
- Không tự thêm `operation_id`, `course_id`, `status` hoặc pagination filter.

<a id="step-2-access"></a>

## 2. Kiểm tra resource và quyền

- AC-25 precondition yêu cầu Mentor có quyền gửi tới học viên thuộc course; catalog yêu cầu role Mentor.
- API #64 chỉ nhận notification ID; contract không cung cấp course ID, sender ID hoặc permission claim.
- Cần kiểm tra notification tồn tại và caller được phép xem trước khi trả delivery state.
- Quan hệ vật lý, direct sender/owner predicate và thứ tự 403/404 chưa được duyệt. Không dùng `notifications.sender_id` như runtime fact dù legacy DDL có candidate column.
- Nếu resource không tồn tại, catalog cho phép 404 `DESIGN_RESOURCE_NOT_FOUND`; nếu caller bị từ chối quyền, catalog cho phép 403 `DESIGN_ACCESS_DENIED`. Trường hợp không tìm thấy do query đã scope quyền cần policy chống lộ sự tồn tại.

<a id="step-3-read-delivery"></a>

## 3. Đọc delivery state

### Q1 — Đọc logical notification và permission scope

| Target | Cột logic cần biết | Điều kiện logic | Bằng chứng/trạng thái |
|---|---|---|---|
| Notification | `id` | Khớp `notification_id` | Contract ID int64; physical schema/live status chưa xác nhận. |
| Notification | owner/sender/course scope | Khớp permission đã duyệt | Không được API/schema/diagram chốt; SOURCE_REQUIRED. |

### Q2 — Đọc logical delivery summary

| Target | Dữ liệu logic cần biết | Điều kiện logic | Bằng chứng/trạng thái |
|---|---|---|---|
| NotificationDelivery | status và counts | Theo notification | Reusable schema; chưa có physical source khớp ID. |
| Delivery attempts | status/channel/attempt | Cần quy tắc aggregate đã duyệt | Pilot table có attempt rows nhưng UUID, không có recipient ID; không dùng làm query live. |

- Legacy `notifications.is_read` là trạng thái đọc, không đại diện trạng thái gửi.
- Không đếm từng row delivery attempt như một người nhận; retry có thể tạo nhiều attempt cho cùng channel.
- Nếu notification tồn tại nhưng chưa có delivery row, behavior pending/queued chưa được định nghĩa; không trả 404 chỉ vì chưa có receipt.
- Không chốt aggregate, latest-attempt selection, per-channel status precedence hay “partial success” khi chưa có rule.

<a id="step-4-map-response"></a>

## 4. Map response

| Field response | Nguồn logic trực tiếp | Mapping | Gap |
|---|---|---|---|
| `HTTPStatus` | Nhánh response | Cố định 200 | Catalog DIRECT. |
| `success` | Nhánh đọc thành công | `true` | Theo envelope convention. |
| `businessCode` | Catalog | `DESIGN_RESOURCE_RETRIEVED` | DIRECT. |
| `message` | Ứng dụng | Safe message | Literal chưa quy định. |
| `data` | Operation schema | Operation object | Không có source/persistence được duyệt. |
| `data.id` | Operation | Operation UUID | Chưa có liên kết từ path notification_id. |
| `data.kind` | Operation | Enum trực tiếp | Giá trị/lifecycle SOURCE_REQUIRED. |
| `data.status` | Operation | OperationStatus | Không tự dùng pilot notification_status. |
| `data.owner_id` | Operation | int64 owner | Principal/owner relation SOURCE_REQUIRED. |
| `data.submitted_at` | Operation | date-time | Operation source chưa có. |
| `data.updated_at` | Operation | date-time | Operation source chưa có. |
| `data.completed_at` | Operation | Optional date-time | Field có thể omit/null theo serializer chưa chốt. |
| `data.result` | Operation | Optional Payment schema | Không phải delivery summary; không tạo Payment giả. |
| `data.result.id` | Payment | int64 | SOURCE_REQUIRED; không có nghĩa vụ thanh toán trong flow notification. |
| `data.result.order_id` | Payment | int64 | SOURCE_REQUIRED; không có nghĩa vụ thanh toán trong flow notification. |
| `data.result.provider` | Payment | PaymentProvider | Enum và source SOURCE_REQUIRED. |
| `data.result.amount` | Payment | decimal-string | SOURCE_REQUIRED; không có nghĩa vụ thanh toán trong flow notification. |
| `data.result.status` | Payment | PaymentStatus | Enum và source SOURCE_REQUIRED. |
| `data.result.transaction_code` | Payment | Optional string | SOURCE_REQUIRED; không có nghĩa vụ thanh toán trong flow notification. |
| `data.result.paid_at` | Payment | Optional date-time | SOURCE_REQUIRED; không có nghĩa vụ thanh toán trong flow notification. |
| `meta` | Envelope | `{}` nếu không có metadata riêng | Policy current source khác error guideline. |
| `traceId` | Request trace | Trace UUID | Runtime endpoint chưa có. |

- `NotificationDelivery.notification_id/status/queued/sent/failed` không được map vào các Operation fields bằng suy đoán.
- Nếu contract đổi để #64 trả `NotificationDelivery`, cần thêm nguồn/định nghĩa cho từng count và status trước khi viết query.

<a id="step-5-response-errors"></a>

## 5. Trả response và lỗi

- Thành công: HTTP 200, `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Operation>` theo catalog direct.
- Token thiếu/sai: 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Sai role hoặc access policy từ chối: 403 `DESIGN_ACCESS_DENIED`.
- Notification không tồn tại: 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Lỗi persistence/mapping nội bộ: 500 `DESIGN_INTERNAL_ERROR`.
- GET không tạo transaction mutation, không dispatch provider và không thay đổi trạng thái read/delivery.
- Error guidelines yêu cầu `data:null`; current helper mặc định `{}`. Middleware design allowlist chưa có path #64; đây là discrepancy khi wired, không phải runtime hiện tại.
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
