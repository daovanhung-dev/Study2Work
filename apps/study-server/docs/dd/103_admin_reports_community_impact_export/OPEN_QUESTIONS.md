# OPEN_QUESTIONS — Study API #103

**Status:** Draft — Needs Confirmation
**Endpoint:** GET /api/v1/admin/reports/community-impact/export

<a id="q-103-01-response-report-or-operation"></a>
## Q-103-01 — Payload 202 là Report hay Operation?

**Bằng chứng**

- Row #103 của docs/lists/list_api.md ghi HTTP 202 DESIGN_OPERATION_ACCEPTED với ApiEnvelope<Report>.
- Operation tracking paragraph cùng file nói export endpoint trả data:Operation.
- AC-38 mô tả tạo job và tham chiếu API poll #18.
- API #93 có cùng kiểu producer-row/Operation-tracking discrepancy; DD #93 giữ nguyên cả hai.

**Ảnh hưởng**

Client không biết response 202 có chứa report data để hiển thị hay Operation ID để poll/tải file.

**Đề xuất DERIVED**

Dùng Operation cho response acceptance, vì 202 + job + poll path cần một operation identifier. Đây chỉ là khuyến nghị, không thay thế contract row.

**Cần xác nhận**

Chọn payload response chính thức; cập nhật catalog row/Operation tracking/AC diagram đồng bộ nếu cần.

<a id="q-103-02-operation-contract"></a>
## Q-103-02 — Operation ID, quyền poll và kết quả export

**Bằng chứng**

- Reusable Operation.id là UUID; API #18 path row khai báo operation_id:int64; AC diagrams dùng UUID.
- API #18 có owner-only và owner/Admin conflict, chưa có Study physical store/lifecycle.
- Operation.result hiện được khai báo là Payment; report export cần file artifact.
- Reusable ExportAsset có download_url, format và expires_at nhưng chưa được nối vào Operation.result.

**Ảnh hưởng**

Client có thể không poll được ID trả từ producer; không biết cách tải artifact sau khi job hoàn tất.

**Đề xuất DERIVED**

API #18 dùng Operation ID thống nhất và completed result tham chiếu ExportAsset; cần sửa shared schema/producer cùng lúc trước implementation.

**Cần xác nhận**

Chốt kiểu ID, auth owner/Admin, OperationKind/Status, result type theo job và response poll trước khi coding.

<a id="q-103-03-filter-and-format"></a>
## Q-103-03 — Cấu trúc filters, format và validation

**Bằng chứng**

- Catalog khai báo filters?:string và format?:string; không định nghĩa serialization, enum, default hoặc validation.
- AC-38 nêu CSV/XLSX/PDF và nhánh export/job.
- API #102 có from/to/segment strings, nhưng parsing/default/segment semantics vẫn là DERIVED.

**Ảnh hưởng**

Không thể đảm bảo file khớp bộ lọc dashboard hoặc phân biệt input sai với dependency failure.

**Đề xuất DERIVED**

Serialize filters thành JSON chỉ gồm from/to/segment của #102; dùng cùng filter mặc định. Xem CSV/XLSX/PDF là các format được hỗ trợ.

**Cần xác nhận**

Chốt encoding, limits, case/default, handling format/filter không hợp lệ. Không tự thêm 400/422 vì catalog không có các code này.

<a id="q-103-04-acceptance-retry"></a>
## Q-103-04 — Acceptance, side effect của GET và retry

**Bằng chứng**

- Method trực tiếp là GET nhưng AC-38/catalog tracking nói endpoint nhận và tạo export job.
- API guidelines nói Idempotency-Key cho retryable mutations nhưng #103 không khai báo header.
- Không có Study queue, worker, Operation store hoặc acceptance transaction trong source.

**Ảnh hưởng**

Không rõ mỗi lần gọi tạo job mới hay dùng lại job cũ; client retry có thể tạo file/job trùng.

**Đề xuất DERIVED**

Mỗi request accepted tạo một Operation riêng; chỉ trả 202 sau durable acceptance. Đây chưa có physical implementation source.

**Cần xác nhận**

Chốt semantics GET/retry/deduplication, acceptance boundary và status khi dependency lỗi trước/sau acceptance; giữ method GET cho tới khi contract owner đổi.

<a id="q-103-05-storage-and-download"></a>
## Q-103-05 — Temporary storage, download URL và expiry

**Bằng chứng**

- AC-38 yêu cầu temporary storage nếu file được generate phía server.
- ExportAsset schema có download_url, format, expires_at.
- Current Study object storage provider chỉ xử lý avatar; V1-PILOT file_objects chưa có export purpose/mapping cho #103.

**Ảnh hưởng**

Không thể triển khai upload/download, giới hạn quyền truy cập, TTL hoặc cleanup chỉ từ DD hiện tại.

**Đề xuất DERIVED**

Dùng artifact tạm có URL hạn dùng và metadata theo ExportAsset; không chọn physical table/provider.

**Cần xác nhận**

Chọn storage service, key/metadata mapping, owner scope, download authorization, TTL, cleanup và behavior khi storage lỗi.

<a id="q-103-06-admin-authorization"></a>
## Q-103-06 — Admin/report permission

**Bằng chứng**

- Catalog/AC-38 yêu cầu Admin có quyền report/analytics.
- Current Study shared auth source có Student guard; chưa có Admin/report policy được xác nhận.

**Ảnh hưởng**

Chưa thể chứng minh chỉ Admin có quyền export hoặc quyền truy cập qua API #18.

**Cần xác nhận**

Chốt issuer/role/permission claim và áp dụng nhất quán cho export request và poll/download path.

<a id="q-103-07-report-consistency"></a>
## Q-103-07 — Export có cùng dữ liệu dashboard không?

**Bằng chứng**

- AC-38 đặt #103 sau dashboard/filter #102.
- API #102 vẫn draft về metric population, date-window, segment và query source.
- API #101 query ngày có kiểu date; #102 dùng string.

**Ảnh hưởng**

File export có thể khác dashboard nếu format filters, effective dates hoặc metric semantics không thống nhất.

**Đề xuất DERIVED**

Export dùng cùng filter state và cùng report-generation logic của #102; không tạo metric formula thứ hai.

**Cần xác nhận**

Chốt query/filter serialization và canonical metric/date implementation cho #101/#102 trước khi coi output là stable.

<a id="q-103-08-error-lifecycle"></a>
## Q-103-08 — Error trước và sau acceptance

**Bằng chứng**

- #103 catalog errors chỉ gồm 401, 403, 503 và 500.
- AC-38 có queue/job và file storage; API #18 poll trả Operation nhưng result/lifecycle chưa chốt.

**Ảnh hưởng**

Invalid format/filter và lỗi worker sau HTTP 202 không có response mapping đã duyệt.

**Cần xác nhận**

Chốt 503 acceptance boundary, worker failure representation, error details qua poll và input validation mapping; không thêm business code trong DD.

## Trạng thái

Các câu hỏi trên giữ API ở Draft — Needs Confirmation. DD không sửa catalog hoặc API #18 contract.
