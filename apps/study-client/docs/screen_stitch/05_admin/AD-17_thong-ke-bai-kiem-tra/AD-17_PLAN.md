# AD-17 — Kế hoạch Detailed Design

## 1. Phạm vi và nguồn

- Screen ID: `AD-17`; tên theo inventory: **Thống kê bài kiểm tra (Page)**.
- Phiên này chỉ hoàn thiện AD-17. Không xử lý AD-18.
- Nguồn giao diện hiện có: `screen.png` (1600×1440) và `code.html`; giữ nguyên hai file này.
- Nguồn yêu cầu: `apps/study-client/docs/list_screen.md` row 75; `apps/study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio`, diagram AC-35; direct API catalog `docs/lists/list_api.md` row 91; API #91 DD Draft; Study Server #91 route/module/query/model/validator/tests; AD-15 inventory/DD; current Study Web tree.
- UI-only Screen DD chưa có skill canonical được wire trong `.agents/context-manifest.json`; không dùng API DD skill để tạo UI spec.

## 2. Expected behavior — contract trước khi thiết kế

- AC-35 precondition: Admin có **quiz-management permission**. Luồng statistics là `STATISTICS → GET /api/v1/admin/quizzes/{quiz_id}/statistics → Aggregate attempt statistics → hiển thị kết quả/thống kê`. AC-35 không định nghĩa metric, filter, response fields, công thức, làm tròn hoặc empty-state semantics.
- Inventory đề xuất route client `/admin/quizzes/:quizId/statistics`, API #91 và quan hệ AD-15 → AD-17; AD-15 là nơi quay lại. Route client chưa được tìm thấy trong Study Web source và sẽ được ghi là candidate, không phải runtime route đã xác minh.
- Direct catalog #91: `GET /api/v1/admin/quizzes/{quiz_id}/statistics`; Bearer JWT, role Admin; `path{quiz_id:int64!}`; không body/query; response `ApiEnvelope<Quiz>`; 200 `DESIGN_RESOURCE_RETRIEVED`; 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR`.
- Direct response `ApiEnvelope<Quiz>` không định nghĩa thống kê. Không suy ra số liệu từ Quiz metadata hoặc tự tính trên frontend. Bộ metric/formula trong API #91 DD là proposal DERIVED và cần Product/BE owner duyệt.
- Các màn hình liên quan: AD-15 danh sách quiz (entry/return); AC-16 #29–#32 tạo/lưu/nộp/đọc attempt chỉ là dependency nghiệp vụ của thống kê. Chưa có bằng chứng về push event hoặc background job cho AD-17.

## 3. Current behavior — evidence source tách biệt

- Screenshot là trạng thái rỗng: tên Quiz `--`, chưa có `quizId` hợp lệ, đồng bộ đang chờ, “Chưa có số liệu thống kê phân tích”; không có biểu đồ/số liệu.
- HTML có hai link về `/admin/quizzes`. Nút “Kiểm tra kết nối dữ liệu” chạy timer 700 ms, hiện feedback cố định nói API hoạt động và “Trống Analytics”, rồi khôi phục nhãn sau 3 giây. Không có fetch/XHR, retry, timeout mạng hay đọc response.
- HTML tuyên bố có phổ điểm, tỷ lệ hoàn thành, thời gian làm trung bình và nền tự tổng hợp sau submit. Những tuyên bố đó không được AC-35/direct catalog/local API projection hỗ trợ đầy đủ; local #91 không trả phân phối điểm, completion rate hoặc average duration. Đánh dấu các copy này là mockup-only, không phải behavior/runtime evidence.
- Study Server có route và module #91. Shared Bearer/JWT `ADMIN` guard chạy trước positive signed-int64 parsing và DB. Local handler đọc một row aggregate từ `quizzes LEFT JOIN quiz_attempts`, không ghi/commit, không đọc `quiz_answers`, không lọc status/tombstone; lỗi DB/mapping trả 500 và rollback; thiếu Quiz hoặc ID malformed trả 404.
- Local response model `AdminQuizStatistics` khác direct catalog `ApiEnvelope<Quiz>`. Các trường local: `quiz_id`, `attempt_count`, `submitted_attempt_count`, `graded_attempt_count`, `average_score`, `passed_attempt_count`, `pass_rate_percent`. Formula/NULL semantics trong API DD là DERIVED, bao gồm mọi attempt row; submitted khi `submitted_at IS NOT NULL`; graded khi `score IS NOT NULL`; average trên score có giá trị; pass theo `score >= passing_score`; pass metrics NULL nếu threshold NULL; rate dùng graded count và NULL khi không có score. Không có proposal score distribution/time/completion.
- API DD #91 vẫn `Draft — Needs Confirmation`; fake DB test/report không xác minh PostgreSQL/schema/deployment/fine-grained permission. AC-35 quiz-management permission chưa có policy source; local chỉ kiểm tra shared `ADMIN`. V1-PILOT UUID schema khác legacy BIGINT candidate.
- Study Web hiện chỉ có `docs/`, `dist/`, `node_modules/`, `tsconfig.tsbuildinfo`; không có editable source, package manifest, router hoặc API client. UI là `UNWIRED`; runtime không xác minh.

## 4. Blockers và phạm vi DD

| Blocker | Evidence | Quyết định thiết kế |
|---|---|---|
| Response contract | Direct catalog `ApiEnvelope<Quiz>` xung đột local response thống kê riêng | Không chốt mapping UI metrics; ghi cả hai contract và yêu cầu duyệt catalog/response trước implementation |
| Metric contract | AC-35 chỉ yêu cầu aggregate; copy HTML hứa thêm distribution/completion/duration | Không vẽ hoặc giả lập chart/KPI; đánh dấu copy mockup-only và liệt kê fields proposal riêng |
| Authorization | AC-35 quiz-management permission; source chỉ có `ADMIN` | Yêu cầu chốt permission policy; không coi role chung là đủ |
| Data/schema | Local SQL dùng legacy BIGINT, mọi status/tombstone rows, không đọc answer rows; schema live chưa xác minh | Chỉ mô tả local candidate; không khẳng định production totals, grade policy hay tombstone rule |
| Frontend wiring | Không có Study Web source/router/API client | Route, load states, mapping, retry/cache, expiry handling là yêu cầu thiết kế chưa implement |
| Connection CTA | Listener hiển thị feedback cố định không gọi API | Tài liệu hóa prototype hiện tại; không dùng làm trạng thái connectivity thật |

Kết quả dự kiến: DD đầy đủ truy vết nhưng **DD BLOCKED** và **IMPLEMENTATION BLOCKED** đến khi chốt API #91 response/metrics, permission và schema/wiring. **RUNTIME NOT VERIFIED**.

## 5. Kế hoạch đánh số element

Tạo marker duy nhất cho từng nhóm UI nhìn thấy. Tọa độ lưu theo ảnh gốc 1600×1440; annotated output giữ cùng bố cục ở độ phân giải 2× (3200×2880). Marker đặt cạnh nội dung, tránh che chữ. Các link `#` được đánh dấu là placeholder không có đích nghiệp vụ.

| ID | Element dự kiến |
|---:|---|
| 1 | Logo/brand Study2Work LMS |
| 2–6 | Các mục nav shell: Tổng quan, Người dùng, Khóa học & Nội dung, Kiểm duyệt, Báo cáo |
| 7 | Badge SYSTEM NORMAL (copy tĩnh) |
| 8 | Nút notification (không có handler trong prototype) |
| 9 | Danh tính Admin/avatar shell |
| 10 | Breadcrumb hệ thống/quản trị/không gian làm việc |
| 11 | Badge “Chuẩn xác thực RBAC” (copy tĩnh) |
| 12–14 | Breadcrumb cục bộ: Quản trị khảo thí, link Danh sách bài kiểm tra, trang Báo cáo thống kê |
| 15–16 | Tiêu đề và subtitle AD-17 |
| 17 | Link quay lại AD-15 phía trên |
| 18–19 | Nhãn card Quiz mục tiêu và badge “Thực thể Quiz độc lập” |
| 20–22 | KPI card placeholder: tên Quiz; ID route; trạng thái đồng bộ |
| 23–25 | Icon empty state, heading và nội dung giải thích |
| 26–27 | CTA quay lại AD-15 và nút kiểm tra kết nối |
| 28–29 | Hai note card về chính sách dữ liệu và quy trình phân tích |
| 30–33 | Footer copyright/brand, chính sách bảo mật, tiêu chuẩn RBAC, hỗ trợ kỹ thuật |

## 6. Event inventory dự kiến

- `EV-01 Screen entry / route parameter`: yêu cầu route candidate `quizId`; xác thực dương signed-int64 theo API path. Empty/malformed ID không được gửi request; mapping malformed → 404 hiện chỉ là local DERIVED behavior.
- `EV-02 Authentication/authorization`: API cần Bearer Admin; AC-35 thêm quiz-management permission chưa được source xác nhận. Hiện HTML không có auth check.
- `EV-03 Load statistics`: expected gọi GET #91 một lần sau route/auth validation; không có body/query. Frontend hiện chưa gọi API; chưa đặc tả retry/cache/auto-refresh vì không có contract.
- `EV-04 Handle success`: direct catalog Quiz shape không mang statistics, nên không thể map KPI/ready state. Local derived DTO chỉ là proposal; nếu được duyệt vẫn không đủ cho các claim distribution/completion/duration của mockup.
- `EV-05 Handle errors`: cover direct 401/403/404/500 codes; distinguish missing quiz from invalid/expired auth; no response UI implementation found. Network timeout/retry behavior remains unspecified.
- `EV-06 Return to AD-15`: two visible links target `/admin/quizzes`; preserve `quizId` only if approved navigation contract requires it (currently not specified).
- `EV-07 Check connection (prototype)`: click disables CTA, spins icon, changes label for 700 ms, shows static feedback and resets after 3 s. No request is sent; label/feedback cannot prove connectivity.
- `EV-08 Shell/footer placeholder controls`: nav, notification and footer `href="#"` links have no screen-specific route/handler source.
- `EV-09 Background attempt aggregation claim`: HTML says post-submit background aggregate activates this screen; AC-35/local #91 expose a GET-time aggregate and no event/job integration was found. Treat statement as unsupported mockup copy.

## 7. Trạng thái và kiểm soát điều hướng dự kiến

| State | Entry condition | Evidence / constraint |
|---|---|---|
| `unwired-prototype` | Current checked-in screen asset | Empty placeholder, no bound ID or API call |
| `loading` | Candidate future valid route and approved client wiring | Design expectation only; no frontend source |
| `no-data` | Approved response establishes zero attempts/no metric values | Current empty copy is static; semantics not yet approved |
| `ready` | Approved statistics response with agreed fields | Blocked; direct `ApiEnvelope<Quiz>` cannot establish this state |
| `unauthorized` / `forbidden` | API returns 401/403 | Direct API error set; client presentation not implemented |
| `not-found` | API returns 404 | Direct API code; local maps malformed path and absent row to 404 |
| `error` | API returns 500 or network failure | Direct 500; network behavior not specified |
| `connection-checking` / `connection-feedback` | Prototype CTA click | Timer-only UI state; feedback text is not a network result |

Navigation is AD-15 → candidate AD-17 for a selected Quiz and AD-17 → AD-15 via the existing link targets. AC-35 does not define a separate ID source or client route; AD-15 local item IDs are numeric, but the route remains unimplemented.

## 8. Authoring and audit sequence

1. Save this plan before any marker or DD artifact.
2. Create ordered `AD-17_markers.json` and SVG overlay; maintain one-to-one marker/element mapping.
3. Render `screen_annotated.png` at 2× from unchanged source image; visually inspect.
4. Write `AD-17.md` with sections A–F, detailed EV input/process/output and API/error mapping; keep expected, current, derived, and blocker labels distinct.
5. Update inventory row 75, reverse API #91 status, G-11 and global plan/checkpoint without disturbing earlier sessions.
6. Run static artifact/link/source-hash/coordinate/count/whitespace audit. Do not run app tests or claim runtime verification.
