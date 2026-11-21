---
title: "Data Mapping"
order: 5
dd_id: "103"
api_name: "Xuất báo cáo tác động cộng đồng"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Mục lục

1. [Nhận request](#step-1-nhận-request)
2. [Authorize Admin](#step-2-authorize-admin)
3. [Validate filter và format](#step-3-validate-filter-và-format)
4. [Accept job và tạo artifact](#step-4-accept-job-và-tạo-artifact)
5. [Map response hoặc lỗi](#step-5-map-response-hoặc-lỗi)
6. [Cross-API poll](#step-6-cross-api-poll)

<a id="step-1-nhận-request"></a>
## Bước 1 — Nhận request

- Đọc Authorization Bearer header.
- Đọc query filters tùy chọn dưới dạng string.
- Đọc query format tùy chọn dưới dạng string.
- Không có path parameter hoặc request body.
- Chi tiết request: [03_Request.md](./03_Request.md).

<a id="step-2-authorize-admin"></a>
## Bước 2 — Xác thực quyền Admin

- Yêu cầu role Admin và quyền xem/report analytics trước khi nhận yêu cầu export.
- Issuer, role claim, permission key và guard cụ thể là SOURCE_REQUIRED.
- Auth helper dùng chung hiện chỉ có guard Student; đây không phải bằng chứng cho quyền Admin.
- Với lỗi authentication/access theo catalog, xem [06_Error.md](./06_Error.md#error-cases).

<a id="step-3-validate-filter-và-format"></a>
## Bước 3 — Kiểm tra filter và format

- Nếu thiếu filters, hành vi đề xuất là dùng cùng bộ lọc mặc định của #102; cả hai vẫn là DERIVED.
- Nếu có filters, parser đề xuất đọc JSON chỉ gồm from, to và segment theo #102; serialization và hành vi JSON sai là SOURCE_REQUIRED.
- #102 hiện vẫn Draft về date window và segment; không coi các đề xuất này là đã được duyệt.
- AC-38 liệt kê CSV, XLSX và PDF; cách viết enum, mặc định, MIME type và xử lý format không hỗ trợ là SOURCE_REQUIRED.
- Catalog #103 không có code 400 hoặc 422; không tự thêm.

<a id="step-4-accept-job-và-tạo-artifact"></a>
## Bước 4 — Nhận job và tạo artifact

### 4.1. Đọc dữ liệu báo cáo nguồn

- Đề xuất: tạo cùng báo cáo cộng đồng mà dashboard hiển thị qua API #102.
- Bộ lọc đề xuất phải giống trạng thái filter trên dashboard.
- Study hiện không có report service/query hoặc snapshot mapping đã được duyệt.
- Nguồn Report candidate vẫn theo DD #102; các metric trong đó chưa được duyệt.

### 4.2. Nhận xử lý bất đồng bộ

- AC-38 và Operation tracking mô tả export job bất đồng bộ.
- Flow đề xuất: lưu/đưa một Operation vào queue, sau đó trả 202 DESIGN_OPERATION_ACCEPTED.
- Queue, nơi lưu Operation, trạng thái ban đầu, transaction/atomic acceptance, hành vi GET lặp và retry policy là SOURCE_REQUIRED.
- Không coi job đã được nhận trước khi có durable acceptance; nguồn bảo đảm durability chưa được duyệt.

### 4.3. Tạo file

- Format candidate theo AC-38: CSV, XLSX hoặc PDF.
- Nếu file được tạo phía server, AC-38 yêu cầu lưu file tạm thời.
- Storage provider, object key, metadata table, access token/URL, TTL, cleanup và xử lý worker lỗi là SOURCE_REQUIRED.
- Reusable ExportAsset có download_url, format và expires_at, nhưng schema hiện tại chưa nối nó vào Operation.result.

### 4.4. Ranh giới trả response và poll

- Endpoint row trả Report; Operation tracking paragraph trả Operation.
- Response DERIVED được khuyến nghị là Operation tại 202, sau đó client gọi GET /api/v1/operations/{operation_id}; không tự thay endpoint row.
- API #18 vẫn Draft: path operation_id int64 khác UUID; owner/Admin rule và Operation.result?:Payment khác export result chưa được giải quyết.
- Nếu kết quả poll dùng ExportAsset, cần cập nhật shared Operation contract và DD #18 trước.

<a id="step-5-map-response-hoặc-lỗi"></a>
## Bước 5 — Ánh xạ response hoặc lỗi

- Nhánh success theo row: HTTP 202 DESIGN_OPERATION_ACCEPTED với ApiEnvelope<Report>; đúng row nhưng ý nghĩa payload mâu thuẫn với export bất đồng bộ.
- Nhánh theo tracking: HTTP 202 DESIGN_OPERATION_ACCEPTED với ApiEnvelope<Operation>; khớp Operation tracking nhưng vẫn mâu thuẫn producer row.
- Nhánh đề xuất để thảo luận triển khai: Operation vì cần định danh để poll theo AC-38.
- Nhánh lỗi chỉ dùng code catalog #103 tại [06_Error.md](./06_Error.md); lỗi sau 202 cần một Operation result/lifecycle được duyệt nhưng hiện chưa có.

<a id="step-6-cross-api-poll"></a>
## Bước 6 — Poll API liên quan

- Client có thể poll API #18 bằng operation_id nhận từ request export đã được chấp nhận.
- Kiểu operation id, owner/Admin rule, state transition và export result mapping vẫn SOURCE_REQUIRED; xem [câu hỏi mở API #18](../18_operations/OPEN_QUESTIONS.md).
- Khi operation hoàn tất, ExportAsset tạm thời là candidate DERIVED để tải; quyền truy cập và expiry policy chưa được xác lập.

## Ma trận sử dụng Request

| Request item | Use step | Validation/branch | Response/effect | Status |
|---|---|---|---|---|
| Authorization | 1, 2 | Bearer authentication; Admin/report permission | 401/403 or continue | DIRECT requirement; guard SOURCE_REQUIRED |
| filters | 1, 3, 4.1 | Optional report filter string; candidate mirrors #102 | Select report data | DIRECT field; serialization DERIVED; parser SOURCE_REQUIRED |
| format | 1, 3, 4.3 | Optional file format | Select CSV/XLSX/PDF candidate | DIRECT field and diagram names; default/enum SOURCE_REQUIRED |
| Body/path | 1 | None | No body/path effect | DIRECT |

## Ma trận truy vấn

| Query ID | Purpose | Type | Source/columns | Predicate/result | Status |
|---|---|---|---|---|---|
| Q1 | Phân tích filters | Parse trong bộ nhớ | Không có nguồn SQL | JSON candidate ánh xạ sang from/to/segment của #102 | DERIVED; parser contract SOURCE_REQUIRED |
| Q2 | Lấy dữ liệu báo cáo | Service/query nội bộ candidate | Kết quả logic của #102 | Cùng report/filter state với dashboard | SOURCE_REQUIRED; chưa có service/query |
| Q3 | Poll operation | API #18 GET | Logical Operation | Poll bằng operation_id | DIRECT reference; ID/auth/storage chưa rõ |

Không có SQL SELECT nào được chọn làm mapping thực thi cho API #103.

## Ma trận Mutation / side effect

| ID | Operation | Target | Value source | Transaction/failure | Status |
|---|---|---|---|---|---|
| M1 | Nhận yêu cầu export | Logical Operation/queue | Admin + filter + format đã parse | Persistence/atomicity và retry chưa rõ | AC-38/tracking DIRECT; physical mapping SOURCE_REQUIRED |
| M2 | Tạo file export | File artifact logic | Report output + format được chọn | Worker lifecycle/failure/cleanup chưa rõ | AC-38 DIRECT; implementation SOURCE_REQUIRED |
| M3 | Ghi file tạm | File Storage / ExportAsset candidate | File bytes + metadata sau khi tạo | Chỉ áp dụng nếu server-side generation; provider/TTL/download access chưa rõ | AC-38 DIRECT conditional; physical mapping SOURCE_REQUIRED |

## Ma trận nguồn Response

| Field/model response | Kiểu | Mapping/nguồn | Trạng thái |
|---|---|---|---|
| success | boolean | Envelope | Quy ước envelope dùng chung |
| businessCode | string | DESIGN_OPERATION_ACCEPTED | DIRECT catalog |
| message | string | Thông báo an toàn khi nhận job | Nội dung cụ thể SOURCE_REQUIRED |
| data | Report hoặc Operation | Hai payload được khai báo trong catalog | DIRECT; DISCREPANCY |
| data.period.from | date | Report.period.from theo endpoint row | DIRECT schema; kỳ báo cáo theo #102 Draft |
| data.period.to | date | Report.period.to theo endpoint row | DIRECT schema; kỳ báo cáo theo #102 Draft |
| data.metrics[] | ImpactMetric[] | Report.metrics theo endpoint row | DIRECT schema; metric set chưa chốt |
| data.metrics[].key | string | ImpactMetric.key | DIRECT schema; key ứng viên thuộc #102 Draft |
| data.metrics[].value | decimal-string | ImpactMetric.value | DIRECT schema; công thức #102 còn DERIVED |
| data.metrics[].label | string | ImpactMetric.label | DIRECT schema; nhãn chưa chốt |
| data.generated_at | date-time | Report.generated_at | DIRECT schema; clock/timezone chưa chốt |
| data.id | uuid | Operation.id theo tracking paragraph/schema | DIRECT; API #18 path row dùng int64 |
| data.kind | OperationKind | Operation.kind | DIRECT schema; enum value chưa chốt |
| data.status | OperationStatus | Operation.status | DIRECT schema; lifecycle chưa chốt |
| data.owner_id | int64 | Operation.owner_id | DIRECT schema; principal mapping SOURCE_REQUIRED |
| data.submitted_at | date-time | Operation.submitted_at | DIRECT schema; nguồn/clock SOURCE_REQUIRED |
| data.updated_at | date-time | Operation.updated_at | DIRECT schema; lifecycle SOURCE_REQUIRED |
| data.completed_at | date-time optional | Operation.completed_at | DIRECT schema; null/omit rule SOURCE_REQUIRED |
| data.result | Payment optional trong reusable schema | Operation.result | DIRECT schema; không khớp export artifact |
| ExportAsset.download_url | uri | File tạm candidate | DERIVED; storage/access SOURCE_REQUIRED |
| ExportAsset.format | ExportFormat | Format được yêu cầu/mặc định | Enum/default SOURCE_REQUIRED |
| ExportAsset.expires_at | date-time | Retention của file tạm | Expiry policy SOURCE_REQUIRED |
| meta | object | Envelope | Shape riêng của endpoint chưa quy định |
| traceId | uuid | API guideline | Quy ước trace dùng chung |

## Thứ tự xử lý đề xuất

1. Xác thực Bearer và yêu cầu quyền Admin xem report.
2. Đọc filters/format, không thêm query field.
3. Chỉ parse/validate khi đã có format và value rules được duyệt.
4. Dùng lại semantics báo cáo cộng đồng #102 để file khớp filter dashboard.
5. Nếu chọn Operation contract, chỉ trả HTTP 202 sau khi async Operation được nhận bền vững.
6. Tạo file theo format được chọn.
7. Chỉ lưu artifact tạm phía server khi dùng cách generate đó.
8. Cung cấp artifact hoàn tất theo poll result/download contract đã duyệt.
9. Chỉ trả đúng error 401/403/503/500 theo catalog; không lộ chi tiết storage nội bộ.

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
