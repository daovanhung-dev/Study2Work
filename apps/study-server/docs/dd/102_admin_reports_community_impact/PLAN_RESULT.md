# PLAN_RESULT — Study API #102

**Status:** Draft — Needs Confirmation
**Endpoint:** `GET /api/v1/admin/reports/community-impact`

| Thuộc tính | Giá trị |
|---|---|
| Output folder | `apps/study-server/docs/dd/102_admin_reports_community_impact/` |
| Basis | Catalog #102, reusable `ApiEnvelope<Report>`, AC-38 |
| Direct inputs | Bearer JWT/Admin; optional `from?:string`, `to?:string`, `segment?:string`; no body/path |
| Direct response | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Report>` |
| Direct errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 500 `DESIGN_INTERNAL_ERROR` |
| Candidate metrics | Distinct learners enrolled, course completion records, root topics, replies; all `DERIVED` |
| Candidate source | Legacy `enrollments` and self-referential `discussions`; live schema unverified |
| Alternative persistence | Pilot `report_snapshots`; no approved report-code/segment/API mapping |
| Runtime | `UNWIRED / NOT_FOUND`; no route/module/query/test #102 |
| Verification | Static DD checks only; no application tests |

## Kết quả theo plan

| Plan item | Result | Evidence/status |
|---|---|---|
| Giữ contract catalog #102 | Hoàn thành | Method/path, Admin Bearer, optional string queries, no body/path, Report, HTTP 200 và đúng 3 error codes. |
| Đọc AC-38/AC-18/AC-19/DB diagrams | Hoàn thành | Flow #101 → validate/permission + metrics #102 → dashboard/filter → optional #103; AC-19 Comment-vs-legacy discussion gap retained. |
| Thiết kế metric đơn giản | Hoàn thành có giới hạn | Bốn count metrics từ enrollment/completion và root/reply candidates; keys/formulas/segment đều `DERIVED`. |
| Dùng kỳ thống nhất với #101 | Đề xuất | ISO date parsing và cùng rolling-window proposal; #102 catalog chỉ nêu string, lỗi parse/range chưa có mapping. |
| Tách learning progress khỏi event analytics | Hoàn thành | Không dùng `lesson_progress`/quiz/assignment state làm event ledger; #66 and AC-18 boundary cited. |
| Tạo DD Markdown | Hoàn thành | 8 template sheets + 3 reports; không sửa runtime/schema/catalog/diagram/client. |
| Validate DD | Hoàn thành | Xem [VERIFICATION_REPORT.md](./VERIFICATION_REPORT.md); static only. |
| Macro-review AC-38 #101–#103 | Chưa thực hiện | Chờ DD #103; giữ string/date, segment và Report/Operation discrepancy mở. |

## Metric proposal `DERIVED`

| Key đề xuất | Candidate rule | Segment đề xuất | Giới hạn cần xác nhận |
|---|---|---|---|
| `unique_enrolled_learners` | `COUNT(DISTINCT enrollments.user_id)` theo `enrolled_at` trong kỳ | `learning` | `user_id` nullability/population và duplicate rules |
| `course_completions` | Đếm enrollment rows có `completed_at` trong kỳ | `learning` | `completed_at` meaning, status/uniqueness rules |
| `discussion_topics_created` | Đếm discussion rows có `parent_id IS NULL` theo `created_at` | `community` | AC-19 comment persistence; moderation visibility |
| `discussion_replies_created` | Đếm discussion rows có `parent_id IS NOT NULL` theo `created_at` | `community` | AC-19 comment persistence; moderation visibility |

Nếu không truyền `segment`, proposal trả cả bốn metrics; `learning` hoặc `community` chọn nhóm tương ứng. Metric values là decimal-string; count rỗng là `"0"`. Không có metric actor/content fields.

## Date/segment proposal `DERIVED`

- Parse `from`/`to` dạng ISO `YYYY-MM-DD`; effective range là inclusive.
- Dùng đúng window proposal #101: hai đầu vắng thì 30 ngày lịch tới hôm nay; chỉ `from` thì tới hôm nay; chỉ `to` thì 30 ngày kết thúc tại ngày đó.
- Catalog không chốt parser/default/timezone hoặc lỗi `from > to`; không thêm 400/422. Chuỗi segment ngoài `learning`/`community` cũng chưa có status/business-code mapping.

## AC-38 macro-review — completed 2026-10-24

| API | Finding | Status after review |
|---|---|---|
| #101 | `from/to` are `date`; effective window, metrics and `generated_at` remain proposals. | Open questions retained. |
| #102 | `from/to` are `string`; segment vocabulary and metric/date rules are unapproved. | Date type mismatch with #101 retained. |
| #103 | Endpoint row says HTTP 202 `Report`; Operation tracking says `Operation`; diagram describes export job and optional temporary storage. | Payload conflict retained; Operation proposal remains DERIVED. |
| API #18 | ID type, owner/Admin access, `result?:Payment`, Study persistence and export artifact lifecycle are unresolved. | Poll contract not implementation-ready. |

No catalog, schema, diagram or source contract was changed.
