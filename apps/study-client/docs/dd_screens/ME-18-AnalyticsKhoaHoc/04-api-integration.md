# ME-18 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ME-18-API-001` | #66 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #66
- Orchestration/data notes: Chỉ gọi #66 với numeric course_id sau khi carrier và response được duyệt; không có period/query/export. Catalog ApiEnvelope<Page<Course>> khác local summary. AC-26 đặt #66 trước chọn Student/#67; inventory tách ME-18 khỏi ME-17. KPI, ETL state, timeframe và CSV chưa có mapping.
- BE/source status và gate: **R**; #66 route/module/query/model/focused-test source có local implementation. **DD BLOCKED; IMPLEMENTATION BLOCKED:** response mismatch, KPI/period/event semantics, course ID/owner policy, ETL/export, AC-26 ordering; Study Web UNWIRED; RUNTIME NOT VERIFIED
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: B2. Current API #66 source flow

1. FastAPI route đọc raw course_id và Authorization header; OpenAPI khai báo required signed-int64 path và header. Không query/body/page-size.
2. Shared access-JWT guard yêu cầu role MENTOR trước truy cập DB.
3. parse_course_id nhận signed int64 trong range; malformed/out-of-range trả 404 DESIGN_RESOURCE_NOT_FOUND. Source không áp dụng client-positive-ID rule riêng.
4. FIND_MENTOR_COURSE lấy id/mentor_id. Không có course → 404; khác JWT sub → 403, trước aggregate. Query lỗi được rollback và trả 500 safe.
5. Aggregate lặp lại owner predicate, chỉ lấy lesson PUBLISHED, user role STUDENT và last_accessed_at khác null; group theo user_id, lesson_id và MAX timestamp trong cặp. Không có ACTIVE enrollment predicate.
6. Trả tracked_lesson_accesses=count distinct pairs, students_with_activity=count distinct Student IDs, last_activity_at=max timestamp. Empty aggregate → 0, 0, null.
7. View kiểm tra count không âm, students_with_activity không lớn hơn tracked pairs, timestamp đúng datetime/null và int64 range. Projection lỗi hoặc SQL lỗi → rollback + 500 DESIGN_INTERNAL_ERROR; không lộ SQL.
8. Success: HTTP 200, DESIGN_RESOURCE_RETRIEVED, ApiEnvelope<MentorCourseActivityAnalytics>; meta rỗng và traceId được giữ. Local response fields không khớp direct catalog Page<Course>.
9. API read-only; không có external service, ETL trigger, export, event ledger, #65/#67 call hoặc DB write.
10. Focused test source dùng fake DB; test không chạy trong phiên này và không xác nhận PostgreSQL/live schema/deployment.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/04_mentor/ME-18_analytics-khoa-hoc/ME-18.md)
