# OPEN_QUESTIONS — Study API #102

**Status:** Draft — Needs Confirmation
**Endpoint:** `GET /api/v1/admin/reports/community-impact`

## Q-102-01 — Metric set and meaning

**Evidence:** AC-38 yêu cầu aggregate learning/community metrics; `Report.metrics` chỉ là `ImpactMetric[]`, không định nghĩa keys/formulas.

**Impact:** Client không biết metric nào ổn định hoặc metric có đo người, lượt ghi danh hay trạng thái hiện tại.

**Đề xuất DERIVED:** distinct learner IDs theo enrollment date; enrollment rows có `completed_at` theo completion date; root topic và reply rows theo `parent_id`/`created_at`.

**Cần xác nhận:** Phê duyệt metric set, population, date column, status predicates, duplicate semantics, label/unit và thứ tự.

## Q-102-02 — Segment values and invalid segment behavior

**Evidence:** Catalog chỉ khai báo `segment?:string`; reusable `Report` không có field segment hoặc enum. Diagram chỉ nói dashboard/filter.

**Impact:** Không rõ segment là loại metrics hay demographic/course dimension; không biết request lạ xử lý thế nào.

**Đề xuất DERIVED:** `learning` chọn Q1/Q2, `community` chọn Q3/Q4, bỏ trống trả đủ bốn metrics.

**Cần xác nhận:** Chốt vocabulary, case/blank normalization, unknown value behavior và metric ordering; không tự thêm status/error code.

## Q-102-03 — Date-string format, default and invalid-range mapping

**Evidence:** Input `from`/`to` là string; output `Report.period` dùng `date`; AC-38 yêu cầu validate range. Catalog chỉ nêu 401/403/500.

**Impact:** Chưa biết parser/default, `from > to` behavior, timezone/date boundary, max period hoặc error response được duyệt.

**Đề xuất DERIVED:** ISO `YYYY-MM-DD` và cùng effective window proposal với #101 để dashboard thống nhất.

**Cần xác nhận:** Phê duyệt format/default/inclusive semantics và mapping cho parse/range failure mà không tự phát minh HTTP/business code.

## Q-102-04 — Admin/report authorization source

**Evidence:** Catalog và AC-38 yêu cầu Admin có quyền xem report/analytics. Current Study `app/utils/auth.py` có Student guard; chưa có Admin claim/report-permission policy.

**Impact:** Chưa thể chứng minh quyền được kiểm tra trước khi đọc aggregate data.

**Cần xác nhận:** Issuer/claim, role mapping, report permission và principal identity. Không coi catalog requirement là runtime authorization.

## Q-102-05 — Enrollment completion and learner population

**Evidence:** Legacy `enrollments` có `user_id`, `enrolled_at`, nullable `completed_at`, `status`; DDL cho phép null `user_id`, DB guide/ERD mô tả bắt buộc; enum/status rule không đầy đủ.

**Impact:** Distinct learner count bỏ qua null IDs; completion row count có thể khác unique users/courses; status predicate chưa xác định.

**Cần xác nhận:** Chọn `completed_at` hay status làm completion signal, population/status filter, uniqueness and orphan/null handling.

## Q-102-06 — Community visibility and moderation

**Evidence:** Legacy `discussions.status` default `ACTIVE`; values/soft-delete/moderation visibility incomplete. API #100 separately proposes soft delete; diagram does not set report visibility.

**Impact:** Counts without status filter include rows that may be hidden/deleted; active-only counts may lose historical contribution.

**Cần xác nhận:** Gross-created versus currently-visible/active contribution semantics; status/deleted/report predicates and retention policy.

## Q-102-07 — Comment storage versus discussion replies

**Evidence:** AC-19 diagram says `INSERT Comment + update counters`; legacy ERD/DDL have no separate Comment table, but model root/reply rows through `discussions.parent_id`.

**Impact:** Q3/Q4 are only legacy candidate mappings and may omit intended comments if a different persistence model is used.

**Đề xuất DERIVED:** Use self-referential `discussions` root/reply rows because that is the available legacy candidate; never claim it matches live implementation.

**Cần xác nhận:** Approved comment persistence and how it maps to discussion topic/reply aggregates.

## Q-102-08 — Legacy versus pilot/report snapshot source

**Evidence:** Legacy Study DDL uses BIGINT tables/timestamps. V1-PILOT has UUID course enrollment/progress entities plus `report_snapshots`, but no #102 report code, segment JSON contract, writer, or API mapping.

**Impact:** No executable source or live-schema availability is proven.

**Cần xác nhận:** Select live aggregate relations or snapshot model; if snapshot, define report code, dimensions, metrics JSON/version, freshness/writer and API mapping.

## Q-102-09 — Aggregate consistency and `generated_at`

**Evidence:** Report has `generated_at`; catalog/diagram do not state transaction snapshot, clock, timezone, cache or freshness.

**Impact:** Independent metrics could observe different committed states and client freshness is unclear.

**Cần xác nhận:** Read isolation/consistent snapshot, clock/timezone, freshness and whether generated_at records query or snapshot generation.

## Q-102-10 — AC-38 export integration

**Evidence:** #103 catalog row returns `ApiEnvelope<Report>` with 202 `DESIGN_OPERATION_ACCEPTED`; Operation-tracking text says export returns `Operation` and client polls `/api/v1/operations/{operation_id}`.

**Impact:** #102 dashboard/filter output and export job/result contract are not yet coherent end-to-end.

**Cần xác nhận:** Contract owner chọn date contract và response/operation model, đồng thời chốt liên kết export/poll. Không tự sửa catalog trong DD #102.

**Macro-review AC-38 (2026-10-24):** Đã rà #101 → #102 → nhánh export/view-only #103. #102 query `from/to:string` chưa khớp #101 `date`; segment/filter semantics và metric proposal vẫn mở. #103 `Report` row xung đột Operation tracking. API #18 còn ID int64/UUID, owner/Admin, result `Payment`/ExportAsset và storage/lifecycle chưa chốt. #101–#103 đều chưa có route+view Study; giữ câu hỏi mở.
