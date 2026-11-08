# AD-17 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-17-API-001` | #91 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #91
- Orchestration/data notes: GET #91; direct catalog `ApiEnvelope<Quiz>` không có metric fields; local source trả derived `AdminQuizStatistics` (counts/average/pass metrics). Contract/schema mismatch chặn mapping; local DTO chưa được duyệt.
- BE/source status và gate: **R** local #91 route/module/query/model/validator/test source; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** direct Quiz vs local derived statistics response, metric/NULL/rounding approval, AC-35 quiz-management permission vs shared `ADMIN`, legacy schema/live DB, Study Web UNWIRED; screenshot distribution/completion/duration/background/connectivity claims unsupported; **RUNTIME NOT VERIFIED**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Nguồn truy vết

- [Screen inventory row 75](../../list_screen.md) and [AD-15 DD](../../screen_stitch/05_admin/AD-15_danh-sach-bai-kiem-tra/AD-15.md).
- [AC-35 activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio), nodes n4 and n11–n13, edge STATISTICS.
- [API catalog #91](../../../../../docs/lists/list_api.md), row #91.
- [API #91 overview](../../../../study-server/docs/dd/91_admin_quizzes_statistics/02_Overview.md), [request](../../../../study-server/docs/dd/91_admin_quizzes_statistics/03_Request.md), [response](../../../../study-server/docs/dd/91_admin_quizzes_statistics/04_Response.md), [data mapping](../../../../study-server/docs/dd/91_admin_quizzes_statistics/05_Data_Mapping.md), [errors](../../../../study-server/docs/dd/91_admin_quizzes_statistics/06_Error.md), and [open questions](../../../../study-server/docs/dd/91_admin_quizzes_statistics/OPEN_QUESTIONS.md); all Draft — Needs Confirmation.
- Current server source: [route](../../../../study-server/app/api/v1.py), [models](../../../../study-server/app/modules/admin/api_91_admin_quizzes_statistics/models.py), [validator](../../../../study-server/app/modules/admin/api_91_admin_quizzes_statistics/validate.py), [query](../../../../study-server/app/modules/admin/api_91_admin_quizzes_statistics/query.py), [handler](../../../../study-server/app/modules/admin/api_91_admin_quizzes_statistics/view.py), and [HTTP test source](../../../../study-server/tests/modules/admin/api_91_admin_quizzes_statistics/test_admin_quizzes_statistics.py).
- [Existing API test report](../../../../study-server/docs/testing/api-test-report-2026-11-01.md) records #91 success path PASS; it was not run in this session.
- UI prototype files: [original screenshot](../../screen_stitch/05_admin/AD-17_thong-ke-bai-kiem-tra/screen.png), [HTML](../../screen_stitch/05_admin/AD-17_thong-ke-bai-kiem-tra/code.html), [marker map](../../screen_stitch/05_admin/AD-17_thong-ke-bai-kiem-tra/AD-17_markers.json), [marker overlay](../../screen_stitch/05_admin/AD-17_thong-ke-bai-kiem-tra/AD-17_markers.svg), [annotated screenshot](../../screen_stitch/05_admin/AD-17_thong-ke-bai-kiem-tra/screen_annotated.png). Study Web checkout has no editable app source/router/API client.

### Trích từ DD nguồn: API #91 — direct catalog contract

| Trường | Direct contract |
|---|---|
| Method / endpoint | `GET /api/v1/admin/quizzes/{quiz_id}/statistics` |
| Auth | Bearer JWT; role=Admin theo catalog. AC-35 còn yêu cầu quiz-management permission. |
| Path | `quiz_id:int64!`; API catalog không khai báo body hoặc query parameter. |
| Success | HTTP 200, `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Quiz>`. Schema Quiz không khai báo analytics fields. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR`. |
| API DD status | `Draft — Needs Confirmation`; response schema, metrics, thresholds, schema và permission vẫn mở. |

### Trích từ DD nguồn: Local API #91 behavior — không thay direct contract

- Route: `apps/study-server/app/api/v1.py`, `GET /api/v1/admin/quizzes/{quiz_id}/statistics`; module `app/modules/admin/api_91_admin_quizzes_statistics/`.
- Handler chạy shared `ADMIN` auth trước parse; parser nhận chữ số dương tới signed-int64 max. ID malformed được map thành 404 theo DERIVED local behavior.
- SQL đọc một row từ `quizzes LEFT JOIN quiz_attempts`, nhóm theo quiz ID và `passing_score`. Dùng `attempt.id`, `submitted_at`, `score`; không dùng `quiz_answers`, không lọc status hoặc tombstone, không ghi và không commit.
- Local data fields: `quiz_id:int64`, `attempt_count:int64`, `submitted_attempt_count:int64`, `graded_attempt_count:int64`, `average_score:string|null`, `passed_attempt_count:int64|null`, `pass_rate_percent:string|null`. Đây là DTO hiện tại, **không phải** response type direct trong catalog.
- Công thức proposal trong API DD: mọi attempt row thuộc quiz; submitted khi `submitted_at IS NOT NULL`; graded khi `score IS NOT NULL`; average trên score khác NULL; nếu threshold có giá trị thì pass khi `score >= passing_score`; rate = passed / graded × 100; NULL threshold hoặc không có scored attempt làm pass metrics/rate NULL. Đây là DERIVED và chưa được duyệt.
- Missing quiz trả 404; DB/mapping lỗi rollback và trả 500 an toàn; shared auth trả 401/403. Không có 422 direct error. Existing test report ghi nhận success path PASS; test source dùng fake DB, không xác minh PostgreSQL/schema/deployment.

### Trích từ DD nguồn: Luồng dự kiến sau khi contract và frontend được wire

1. Từ AD-15, Admin chọn thao tác xem thống kê cho Quiz. Chỉ định danh Quiz nào được truyền sang route client vẫn cần đối chiếu ID thực tế; API #91 nhận `quiz_id:int64!`.
2. Client kiểm tra trạng thái phiên và quyền màn hình theo policy được duyệt. AC-35 nêu quiz-management permission; API local chỉ có shared `ADMIN`. Không được xem route-level/Admin shell copy là authorization.
3. Client lấy path `quizId`, chuẩn hóa theo contract numeric `int64`, sau đó gọi GET #91 với Bearer token. Direct catalog không khai báo body/query. Hiện không có router hoặc API caller trong Study Web.
4. Backend current source xác thực shared `ADMIN`, parse ID, query aggregate read-only trên legacy Quiz/QuizAttempt candidate. API DD đánh dấu metric/formula là DERIVED. Live schema và policy chưa được xác minh.
5. Với HTTP 200, direct response contract là `ApiEnvelope<Quiz>` nên client không có analytics fields được bảo đảm để ánh xạ. Không được tự tính analytics trên Quiz hoặc dùng local DTO như thể đã được duyệt. Chỉ sau khi response contract được owner chốt mới định nghĩa loading→no-data/ready và mapping.
6. Với 401/403/404/500, hiển thị trạng thái phù hợp theo business code; phần UI/auth-expiry/ retry hiện chưa có implementation hoặc approved interaction. Local source dùng 404 cả cho path malformed và Quiz vắng mặt.
7. Người dùng có thể quay lại AD-15 qua breadcrumb hoặc một trong hai link quay lại; cả ba anchor hiện trỏ tới `/admin/quizzes`. Param cần giữ lại hoặc không phải là quyết định route chưa được đặc tả.
8. Không có bằng chứng AD-17 được cập nhật push sau submit. AC-35 hiện mô tả GET aggregate; câu trong HTML nói tác vụ nền sau submit là static mockup copy.

### Trích từ DD nguồn: Luồng dữ liệu / API

```text
AD-15 (Quiz ID cần xác minh)
  → candidate route /admin/quizzes/:quizId/statistics
  → GET #91 (Bearer JWT, path quiz_id:int64!, không body/query)
  → DIRECT catalog: ApiEnvelope<Quiz> ── không có metric fields
  → LOCAL source: derived AdminQuizStatistics ── chưa được contract duyệt
  → UI no-data/ready mapping: BLOCKED đến khi thống nhất schema và metrics
```

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-17_thong-ke-bai-kiem-tra/AD-17.md)
