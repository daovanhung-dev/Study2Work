# AD-17 — Thống kê bài kiểm tra · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-17` |
| Module | Admin |
| Route | `/admin/quizzes/:quizId/statistics` (candidate; Study Web route chưa wired)` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái tài liệu:** DD BLOCKED; **Trạng thái triển khai:** IMPLEMENTATION BLOCKED; **Runtime:** NOT VERIFIED |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-17.md](../../screen_stitch/05_admin/AD-17_thong-ke-bai-kiem-tra/AD-17.md), [AD-17_PLAN.md](../../screen_stitch/05_admin/AD-17_thong-ke-bai-kiem-tra/AD-17_PLAN.md), [AD-17_markers.json](../../screen_stitch/05_admin/AD-17_thong-ke-bai-kiem-tra/AD-17_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Admin xem attempt statistics theo fields trong response được duyệt; không tự dựng score distribution/completion/duration.
- In-scope: GET #91; direct catalog `ApiEnvelope<Quiz>` không có metric fields; local source trả derived `AdminQuizStatistics` (counts/average/pass metrics). Contract/schema mismatch chặn mapping; local DTO chưa được duyệt.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-35 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Admin xem attempt statistics theo fields trong response được duyệt; không tự dựng score distribution/completion/duration. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #91
- Liên kết màn hình dự kiến: [AD-15](../AD-15-DanhSachBaiKiemTra/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | unwired/loading/no-data/ready/unauthorized/forbidden/not-found/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-17 source screen.png](../../screen_stitch/05_admin/AD-17_thong-ke-bai-kiem-tra/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-17_thong-ke-bai-kiem-tra/screen_annotated.png))
- Luồng: GET #91; direct catalog `ApiEnvelope<Quiz>` không có metric fields; local source trả derived `AdminQuizStatistics` (counts/average/pass metrics). Contract/schema mismatch chặn mapping; local DTO chưa được duyệt.
- Priority: P2; Gate/source status: **R** local #91 route/module/query/model/validator/test source; API DD Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** direct Quiz vs local derived statistics response, metric/NULL/rounding approval, AC-35 quiz-management permission vs shared `ADMIN`, legacy schema/live DB, Study Web UNWIRED; screenshot distribution/completion/duration/background/connectivity claims unsupported; **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-17 — Thống kê bài kiểm tra

> **Trạng thái tài liệu:** DD BLOCKED
> **Trạng thái triển khai:** IMPLEMENTATION BLOCKED
> **Runtime:** NOT VERIFIED
> API #91 có route/module/test source trong Study Server; UI Study Web chưa có source/router/API client. API DD #91 vẫn `Draft — Needs Confirmation`.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | `AD-17` — Thống kê bài kiểm tra (Page). Tiêu đề trên prototype: “Báo cáo thống kê kết quả kiểm tra”. |
| Mục tiêu | Theo AC-35, Admin xem số liệu tổng hợp các attempt của một Quiz đã chọn. AC-35 không chốt tập metric hoặc response fields. |
| Actor / quyền | Expected: Admin có `quiz-management permission` (AC-35). Current API source chỉ gọi shared `ADMIN` guard; chưa tìm thấy policy xác nhận fine-grained permission tương đương. Đây là blocker, không được xem hai quyền là đồng nhất. |
| Điều kiện trước | Expected: phiên Admin hợp lệ, có quyền quản lý quiz, có `quiz_id` trong route và Quiz có thể tra cứu. Current UI không nạp auth/session hoặc Quiz. |
| Điều kiện sau | Expected: thống kê đã được hiển thị từ response được phê duyệt; không có ghi dữ liệu từ thao tác xem. Current prototype giữ trạng thái rỗng tĩnh; nút kiểm tra chỉ đổi nội dung theo timer. |
| Route | Inventory candidate: `/admin/quizzes/:quizId/statistics`. Chưa có client router trong Study Web; route là thiết kế candidate, không phải runtime route đã xác minh. API path trực tiếp: `/api/v1/admin/quizzes/{quiz_id}/statistics`. |
| Màn hình liên kết | AD-15 — Danh sách bài kiểm tra: entry theo Quiz được chọn và return target của hai link hiện có. AC-35 cũng liên quan tới #87–#90; thống kê gọi #91. AC-16 #29–#32 là nguồn attempt/submit/result liên quan, nhưng không có event/job wiring được tìm thấy. |
| Dữ liệu trên màn | Không có dữ liệu thống kê được render. Prototype chỉ có placeholder tên Quiz, ID và trạng thái đồng bộ. Không có chart, phổ điểm, completion rate hay duration metric. |
| Bảo mật | Direct catalog yêu cầu Bearer JWT, role Admin; AC-35 yêu cầu quiz-management permission. Local API kiểm tra Bearer/JWT và role `ADMIN`, nhưng không chứng minh policy AC-35. Không gửi user ID/role trong request. |
| Trạng thái hiện tại | Screen assets là static prototype. Study Web `UNWIRED`; API #91 có local route/source và test source. API direct contract và local DTO khác nhau. DB/schema production, permission cụ thể và metric proposal chưa được phê duyệt. |

### Nguồn và trạng thái bằng chứng

| Chủ đề | Expected / direct evidence | Current source evidence |
|---|---|---|
| Flow | AC-35: `STATISTICS → GET #91 → Aggregate attempt statistics → hiển thị`. | Study API #91 có query aggregate đồng bộ khi GET; không tìm thấy job/background trigger. |
| API success | `docs/lists/list_api.md` #91: `ApiEnvelope<Quiz>`, 200 `DESIGN_RESOURCE_RETRIEVED`. | Local route trả model `GetAdminQuizStatisticsEnvelope` với `AdminQuizStatistics` riêng. Không tương thích với schema Quiz trong catalog. |
| Proposed metrics | AC-35 không định nghĩa fields/formula. | API #91 DD đề xuất counts, average score, passed count/rate; đây là DERIVED, chưa owner-approved. Không gồm score distribution, completion rate hay average duration mà prototype copy đề cập. |
| Authentication | AC-35: Admin có quiz-management permission. | Local guard yêu cầu shared `ADMIN`; fine-grained policy chưa có nguồn xác nhận. |
| Data source | AC-35 nói aggregate attempts, không nêu table/schema. | Local SQL dùng legacy BIGINT `quizzes` và `quiz_attempts`, không lọc status/tombstone, không đọc `quiz_answers`. Live schema chưa xác minh; V1-PILOT UUID model là hệ khác. |
| Client | Inventory gợi ý route/page. | Study Web tree chỉ có docs/dist/node_modules/build metadata; không tìm thấy editable app, router, API client hay AD-17 caller. |

### API #91 — direct catalog contract

| Trường | Direct contract |
|---|---|
| Method / endpoint | `GET /api/v1/admin/quizzes/{quiz_id}/statistics` |
| Auth | Bearer JWT; role=Admin theo catalog. AC-35 còn yêu cầu quiz-management permission. |
| Path | `quiz_id:int64!`; API catalog không khai báo body hoặc query parameter. |
| Success | HTTP 200, `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Quiz>`. Schema Quiz không khai báo analytics fields. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR`. |
| API DD status | `Draft — Needs Confirmation`; response schema, metrics, thresholds, schema và permission vẫn mở. |

### Local API #91 behavior — không thay direct contract

- Route: `apps/study-server/app/api/v1.py`, `GET /api/v1/admin/quizzes/{quiz_id}/statistics`; module `app/modules/admin/api_91_admin_quizzes_statistics/`.
- Handler chạy shared `ADMIN` auth trước parse; parser nhận chữ số dương tới signed-int64 max. ID malformed được map thành 404 theo DERIVED local behavior.
- SQL đọc một row từ `quizzes LEFT JOIN quiz_attempts`, nhóm theo quiz ID và `passing_score`. Dùng `attempt.id`, `submitted_at`, `score`; không dùng `quiz_answers`, không lọc status hoặc tombstone, không ghi và không commit.
- Local data fields: `quiz_id:int64`, `attempt_count:int64`, `submitted_attempt_count:int64`, `graded_attempt_count:int64`, `average_score:string|null`, `passed_attempt_count:int64|null`, `pass_rate_percent:string|null`. Đây là DTO hiện tại, **không phải** response type direct trong catalog.
- Công thức proposal trong API DD: mọi attempt row thuộc quiz; submitted khi `submitted_at IS NOT NULL`; graded khi `score IS NOT NULL`; average trên score khác NULL; nếu threshold có giá trị thì pass khi `score >= passing_score`; rate = passed / graded × 100; NULL threshold hoặc không có scored attempt làm pass metrics/rate NULL. Đây là DERIVED và chưa được duyệt.
- Missing quiz trả 404; DB/mapping lỗi rollback và trả 500 an toàn; shared auth trả 401/403. Không có 422 direct error. Existing test report ghi nhận success path PASS; test source dùng fake DB, không xác minh PostgreSQL/schema/deployment.
