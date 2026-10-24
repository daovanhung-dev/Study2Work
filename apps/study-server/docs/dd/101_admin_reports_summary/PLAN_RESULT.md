# PLAN_RESULT — Study API #101

**Status:** Draft — Needs Confirmation
**Endpoint:** `GET /api/v1/admin/reports/summary`

| Thuộc tính | Giá trị |
|---|---|
| Output folder | `apps/study-server/docs/dd/101_admin_reports_summary/` |
| Basis | Catalog #101, reusable `ApiEnvelope<Report>`, AC-38 |
| Direct inputs | Bearer JWT; role Admin; optional `from?:date`, `to?:date`; no body |
| Direct response | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Report>` |
| Candidate metrics | Four independent row counts, all `DERIVED` |
| Candidate source | Legacy `users`, `courses`, `enrollments`, `discussions` timestamps; live schema unverified |
| Alternative persistence | Pilot `report_snapshots`; no approved report-code/JSON/API mapping |
| Runtime | `UNWIRED / NOT_FOUND`; no route/module/query/test for #101 |
| Verification | Static DD checks only; no application tests |

## Kết quả theo plan

| Plan item | Result | Evidence/status |
|---|---|---|
| Giữ nguyên contract catalog | Hoàn thành | Method, path, Admin Bearer, query, no body, `Report`, HTTP 200 và đúng 3 error codes được giữ nguyên. |
| Đối chiếu AC-38 | Hoàn thành | #101 aggregate KPI summary → #102 community impact → optional #103 export; macro-review nhóm vẫn chờ #102–#103. |
| Tách direct schema khỏi metric proposal | Hoàn thành | `Report`, `DateRange`, `ImpactMetric` dùng đúng reusable schema; không gán metric keys/formulas thành contract. |
| Đánh giá nguồn dữ liệu | Hoàn thành có giới hạn | Legacy timestamps và pilot `report_snapshots` được ghi là candidates riêng; không có live-schema hoặc API mapping proof. |
| Tạo DD Markdown | Hoàn thành | 8 template sheets và 3 reports; không sửa runtime, schema, catalog, diagram hoặc client. |
| Validate DD | Hoàn thành | Xem [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md); kết quả static, không phải runtime acceptance. |
| AC-38 macro-review #101–#103 | Chưa thực hiện | Chờ DD #102 và #103; giữ các khác biệt contract mở. |

## Metric proposal `DERIVED`

| Key đề xuất | Candidate source | Phép tính | Giới hạn cần xác nhận |
|---|---|---|---|
| `user_records_created` | `users.created_at` | Đếm row trong kỳ | Role/population chưa chốt. |
| `course_records_created` | `courses.created_at` | Đếm row trong kỳ | Status inclusion chưa chốt. |
| `enrollment_records_created` | `enrollments.enrolled_at` | Đếm row trong kỳ | Status/duplicate semantics chưa chốt. |
| `discussion_records_created` | `discussions.created_at` | Đếm row trong kỳ | Root/reply scope chưa chốt. |

Metric value được serialize thành decimal-string; count rỗng là `"0"`. Tên, label, công thức, date window và semantics vẫn là proposal, không phải behavior đã duyệt.

## Date-window proposal `DERIVED`

Response `Report.period` cần đủ `from` và `to`, trong khi cả hai query bound đều optional. DD ghi proposal rolling 30 ngày tới ngày hiện tại nếu không có bound; `from` đơn lẻ kết thúc ở hôm nay; `to` đơn lẻ bắt đầu 30 ngày trước đó; có cả hai thì dùng inclusive range. Quy tắc `from > to`, timezone/calendar boundary và cách map lỗi chưa có trong catalog nên vẫn để mở.

## AC-38 macro-review — completed 2026-10-24

| API | Finding | Status after review |
|---|---|---|
| #101 | `from/to` are `date`; summary metric, period and Admin authorization rules remain unapproved. | Open questions retained. |
| #102 | `from/to` are `string`; `segment`, metrics and date parser remain proposals. | Date type mismatch with #101 retained. |
| #103 | Endpoint row says HTTP 202 `Report`; Operation tracking says `Operation`; export may create a job/file and poll API #18. | Payload conflict retained; Operation proposal remains DERIVED. |
| API #18 | ID type, owner/Admin access, `result?:Payment`, Study persistence and export artifact lifecycle are unresolved. | Poll contract not implementation-ready. |

No catalog, schema, diagram or source contract was changed.
