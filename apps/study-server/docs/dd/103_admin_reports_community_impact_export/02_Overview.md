---
title: "Overview"
order: 2
dd_id: "103"
api_name: "Xuất báo cáo tác động cộng đồng"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #103 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-38 |
| Method | GET |
| Endpoint | /api/v1/admin/reports/community-impact/export |
| Purpose | Yêu cầu tạo file export cho báo cáo tác động cộng đồng. |
| Consumer/Actor | Admin có quyền xem report/analytics |
| Authentication | Bearer JWT |
| Authorization | Admin/report permission là DIRECT requirement; claim/guard SOURCE_REQUIRED trong source hiện tại. |
| Query | filters?:string, format?:string |
| Response row | HTTP 202, ApiEnvelope<Report> — DIRECT theo endpoint row |
| Response tracking | HTTP 202, data:Operation — DIRECT theo Operation tracking paragraph; mâu thuẫn với endpoint row |
| Errors | 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 503 DESIGN_DEPENDENCY_UNAVAILABLE; 500 DESIGN_INTERNAL_ERROR |
| AC-38 position | #101 summary → #102 community metrics → optional #103 export hoặc nhánh view-only |
| Runtime state | UNWIRED / NOT_FOUND; không có route/module/query/test/export worker cho #103 |
| Side effects | Chấp nhận job; generate file và lưu tạm nếu server-side — logical effect DIRECT, physical implementation SOURCE_REQUIRED |
| Transaction | Acceptance/queue atomicity và operation lifecycle chưa được chỉ định. |

## Sources

- [API catalog, reusable schemas và Operation tracking](../../../../../docs/lists/list_api.md) — row #103, các schema Report, Operation, ExportAsset và mục Operation tracking.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, điều kiện tiên quyết và các API của AC-38.
- [AC-38 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — nhánh export tùy chọn, format, lưu file tạm, kết quả trên UI và node poll Operation.
- [Study DB ERD](../../diagrams/DB_UNICA_ERD.drawio) và [DB table guide](../../diagrams/DB_UNICA_TABLES.md) — không định nghĩa mapping Operation/export của Study.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — schema ứng viên; không chứng minh metadata đang chạy.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — có file_objects và report_snapshots nhưng chưa có mapping #103; không trộn với mô hình legacy.
- [API #18 Operation overview](../18_operations/02_Overview.md) và [open questions](../18_operations/OPEN_QUESTIONS.md) — hợp đồng poll và các gap về ID, quyền, vòng đời, kết quả.
- [API #93 response precedent](../93_admin_notifications_create/OPEN_QUESTIONS.md) — cùng xung đột giữa payload producer trực tiếp và Operation tracking.
- [API #101 overview](../101_admin_reports_summary/02_Overview.md) và [open questions](../101_admin_reports_summary/OPEN_QUESTIONS.md) — hợp đồng summary và các gap về ngày/metric.
- [API #102 overview](../102_admin_reports_community_impact/02_Overview.md) và [open questions](../102_admin_reports_community_impact/OPEN_QUESTIONS.md) — báo cáo cộng đồng/bộ lọc ứng viên; vẫn Draft.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [avatar-only storage provider](../../../app/service/object_storage/avatar.py) — ranh giới source Study hiện tại.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — quy ước envelope, lỗi an toàn và trace dùng chung.

## Tables read

| Relation/logical resource | Purpose | Basis/status |
|---|---|---|
| Báo cáo cộng đồng #102 | Nguồn ứng viên cho file export | Phụ thuộc logic; chưa có query/service |
| Operation | Nhận job bất đồng bộ và trạng thái poll | Reusable schema DIRECT; persistence vật lý của Study SOURCE_REQUIRED |
| ExportAsset | Kết quả artifact tải xuống ứng viên | Reusable schema DIRECT; đặt trong Operation.result là DERIVED |
| V1-PILOT file_objects | Candidate metadata lưu file | Mô hình thiết kế riêng; chưa duyệt purpose/mapping export |
| V1-PILOT report_snapshots | Phương án lưu report đã tính trước | Snapshot không đại diện cho export job/file; chưa có report code hoặc writer mapping cho #103 |

## Tables write

- AC-38 mô tả nhận operation và có thể tạo file tạm.
- Chưa có bảng vật lý, queue, storage provider, transaction boundary hoặc quy tắc lưu giữ của Study được duyệt.
- Không dùng bảng operations của Work Server hoặc tự suy ra cột DB.

## Mục chú ý

- Cùng catalog có hai khai báo payload thành công: endpoint row ghi Report; Operation tracking ghi Operation.
- HTTP 202 và tham chiếu poll gợi ý luồng bất đồng bộ, nhưng chưa chốt payload hoặc schema kết quả Operation.
- Schema Operation hiện khai báo result?:Payment; ExportAsset là candidate phù hợp với artifact export hơn, nhưng chưa được nối vào Operation.
- Row API #18 dùng operation_id kiểu int64 trong khi Operation.id dùng chung và AC diagram dùng UUID; quyền owner/Admin của #18 cũng chưa thống nhất.
- Định dạng JSON của bộ lọc, format mặc định, lỗi input, retry, quyền tải xuống và thời hạn file chưa được quy định.
- Không thêm error ngoài đúng bốn code trong row #103.

## Giả định — chỉ là đề xuất DERIVED

- filters có thể serialize cùng các bộ lọc from/to/segment của #102; không thêm field lọc khác.
- format ứng viên theo AC-38 là CSV, XLSX và PDF; cần xác nhận mặc định và chuẩn hóa chữ hoa/thường.
- Nhận job bất đồng bộ trả Operation và job hoàn tất có thể cung cấp ExportAsset. Đây là draft đề xuất, không phải contract trực tiếp trong row.
- GET gọi lặp có thể tạo job export khác cho đến khi quy tắc idempotency/trùng request được duyệt.

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | 【Khái quát】 |  |
| 3 | `B3` | Get thông tin…. |  |
| 5 | `A5` | 【Mục chú ý】 |  |
| 7 | `B7` | Không có |  |

</details>
