# OPEN_QUESTIONS — Study API #101

**Status:** Draft — Needs Confirmation
**Endpoint:** `GET /api/v1/admin/reports/summary`

## Q-101-01 — KPI set, key, label and formula

**Evidence:** AC-38 chỉ yêu cầu aggregate KPI summary. Reusable `Report` định nghĩa `metrics:ImpactMetric[]`, không quy định metric cụ thể.

**Impact:** Dashboard không thể dựa vào tên, đơn vị, semantics hay công thức ổn định.

**Decision needed:** Phê duyệt metric keys, labels, định nghĩa population, công thức, đơn vị và thứ tự hiển thị. Bốn row counts trong DD là `DERIVED` proposal.

## Q-101-02 — Effective date range and defaults

**Evidence:** Query `from?:date`, `to?:date` đều optional; response `Report.period` bắt buộc có cả `from` và `to`.

**Impact:** Chưa xác định period trả về khi thiếu một hoặc cả hai query bound.

**Decision needed:** Chốt default window và semantics inclusive/exclusive. Rolling 30 ngày trong DD chỉ là `DERIVED` proposal.

## Q-101-03 — Invalid range and date error mapping

**Evidence:** Catalog #101 liệt kê đúng 401, 403 và 500; không khai báo 400/422 cho date parsing hoặc `from > to`.

**Impact:** Không thể xác định response được duyệt cho ngày sai định dạng hoặc range đảo ngược.

**Decision needed:** Xác nhận parser, timezone/calendar boundary, invalid-range behavior và mapping theo business code hiện có; không tự thêm error code.

## Q-101-04 — Legacy aggregate versus pilot snapshot

**Evidence:** Legacy DDL có timestamp candidates nhưng không có report relation. Pilot `report_snapshots` có `report_code`, period, `dimensions`, `metrics`, watermark/version; chưa thấy report-code contract, JSON schema, writer hoặc mapping với API #101.

**Impact:** Chưa chọn được nguồn query executable hoặc chứng minh những bảng nào hiện có trong live DB.

**Decision needed:** Chọn live aggregate source hay snapshot; nếu snapshot, chỉ định report code, schema JSON, writer/freshness, retention, watermark và API mapping.

## Q-101-05 — Population and filters per candidate metric

**Evidence:** Legacy timestamp columns không tự xác định user role, course status, enrollment status/uniqueness hay discussion root/reply scope.

**Impact:** Các count có thể trả nghĩa khác nhau dù dùng cùng kỳ thời gian.

**Decision needed:** Chốt population và predicate cho từng metric; các query không lọc status/role/root hiện chỉ là `DERIVED` proposal.

## Q-101-06 — Admin/report authorization

**Evidence:** Catalog yêu cầu Admin Bearer JWT; current Study shared helper chỉ có Student guard, chưa có Admin claim/policy.

**Impact:** Chưa có current source evidence cho cách nhận diện hoặc authorize Admin trước khi đọc dữ liệu tổng hợp.

**Decision needed:** Chỉ định issuer/claim, role mapping, report permission policy và principal identity. Không coi catalog requirement là runtime guard đã có.

## Q-101-07 — `generated_at` and consistency

**Evidence:** `Report.generated_at` có kiểu date-time; catalog/diagram không định nghĩa clock, timezone, snapshot consistency hay cách nhiều aggregate queries cùng đọc dữ liệu.

**Impact:** Client không biết thời điểm dữ liệu và các metric có cùng read snapshot hay không.

**Decision needed:** Chốt clock/timezone, read consistency và liệu metrics được tính trực tiếp hay lấy từ snapshot. UTC assembly time trong DD là `DERIVED` proposal.

## Q-101-08 — Empty metric behavior and numeric bounds

**Evidence:** `ImpactMetric.value` là decimal-string; catalog không quy định empty-result behavior, count range hoặc overflow behavior.

**Impact:** Không rõ trả metric value `"0"`, bỏ metric, hay coi metric unavailable; downstream formatting chưa có giới hạn.

**Decision needed:** Phê duyệt zero/missing semantics, numeric range và serialization expectations.

## Q-101-09 — Cross-API AC-38 contract consistency

**Evidence:** #102 khai báo date query kiểu string, khác #101 kiểu date. #103 endpoint row nêu `ApiEnvelope<Report>` với HTTP 202, còn operation-tracking paragraph nói export trả `Operation`.

**Impact:** Chưa chắc cùng date semantics và export response model khi kết hợp dashboard, community metrics và async export.

**Decision needed:** Contract owner xác nhận date semantics, response model và producer/poll contract; không tự sửa catalog.

**Macro-review AC-38 (2026-10-24):** Đã rà #101 → #102 → nhánh export/view-only #103. #101 `date` vẫn khác #102 `string`; #103 `Report` row vẫn xung đột với Operation tracking. API #18 còn ID int64/UUID, owner/Admin, result `Payment`/ExportAsset và storage/lifecycle chưa chốt. #101–#103 đều chưa có route+view Study; giữ câu hỏi mở.
