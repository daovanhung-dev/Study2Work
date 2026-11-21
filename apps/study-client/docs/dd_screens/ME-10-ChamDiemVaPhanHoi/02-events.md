# ME-10 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ME-10-EV-001` | `Source heading` / D.1. API chung #55–#57 | See source event detail below |
| `ME-10-EV-002` | `ME10-E01` / D.2. ME10-E01 — Vào màn hình và tải Submission | See source event detail below |
| `ME-10-EV-003` | `ME10-E02` / D.3. ME10-E02 — Làm mới kết nối/chi tiết | See source event detail below |
| `ME-10-EV-004` | `ME10-E03` / D.4. ME10-E03 — Nhập hoặc sửa điểm | See source event detail below |
| `ME-10-EV-005` | `ME10-E04` / D.5. ME10-E04 — Nhập feedback và cập nhật bộ đếm ký tự | See source event detail below |
| `ME-10-EV-006` | `ME10-E05` / D.6. ME10-E05 — Lưu điểm qua API #56 (chỉ khi UI/contract được tách và duyệt) | See source event detail below |
| `ME-10-EV-007` | `ME10-E06` / D.7. ME10-E06 — Gửi feedback qua API #57 (độc lập #56) | See source event detail below |
| `ME-10-EV-008` | `ME10-E07` / D.8. ME10-E07 — Partial success, reconciliation và refresh #55 | See source event detail below |
| `ME-10-EV-009` | `ME10-E08` / D.9. ME10-E08 — Quay về ME-09 | See source event detail below |
| `ME-10-EV-010` | `ME10-E09` / D.10. ME10-E09 — Báo cáo sự cố tải file | See source event detail below |
| `ME-10-EV-011` | `ME10-E10` / D.11. ME10-E10 — Header/footer placeholder navigation | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

### D.1. API chung #55–#57

- **Auth:** `Authorization: Bearer JWT`; với body hợp lệ, shared helper yêu cầu numeric subject và role `MENTOR` trước custom path parse/DB access. Riêng #56/#57, FastAPI có thể chặn request ở Pydantic body validation trước khi gọi view guard; middleware trả 422 `DESIGN_VALIDATION_ERROR`. Direct `courses.mentor_id` owner scope là fallback DERIVED; assigned Mentor support chưa có.
- **Trace:** route dùng `get_trace_id(request)`; error helper serialize `traceId`, HTTP `X-Trace-Id` và `data:null`. Không đưa raw submission/file URL/SQL vào log UI.
- **HTTP/body:** #55 GET không body/query; #56/#57 POST JSON. Không có idempotency header/contract trong source đang xét. Success source dùng HTTP 200.
- **Response:** success envelope gồm `success`, `businessCode`, `message`, `data:Submission`, `meta`, `traceId`; nullable `content`, `score`, `feedback` có thể bị loại khỏi JSON. `files` hiện là array 0/1. Không có rubric/feedback attachment fields.
- **Source availability:** current Study Server routes exist; API focused tests exist but are not run here and use fake DB per context. Live DB/runtime remains unverified.

### D.2. ME10-E01 — Vào màn hình và tải Submission

- **Trigger:** mở proposed route; element #12/#15–18. Loại: route/load.
- **Điều kiện:** `submissionId` do ME-09 selection (#54 `data.items[].id`) hoặc approved deep link; active session/token. Route/source chưa tồn tại.
- **Input:** route param string; Bearer token; không có filter/query/body. API signed-int64 semantics. Không dùng session mock `SES-ME10-SYNC` làm trace/auth.
- **Xử lý tuần tự:**
  1. Nhận route param; nếu thiếu, chặn request và hiển thị invalid-link state. Kiểu path thật cần ký hiệu hóa nhất quán với UI route.
  2. Lấy auth state từ approved session provider; nếu thiếu, đặt `auth-required` và không gửi PII.
  3. Gọi #55 `GET /api/v1/mentor/submissions/{submission_id}` với Authorization; no query/body.
  4. Backend guard chạy trước parse/DB; malformed/overflow ID → `404 DESIGN_RESOURCE_NOT_FOUND`; valid ID → query row/relations/upload.
  5. 200 `DESIGN_RESOURCE_RETRIEVED`: validate envelope, map `data.id`, IDs, content, files, status, submitted_at, score, feedback. Null optional fields có thể vắng mặt. Không map rubric, tên, deadline, max score, attachments.
  6. `files=[]` thì hiển thị không có file metadata được resolve; không dựng file link từ sample. `files[0]` chỉ render sau kiểm tra status/URL policy đã được owner duyệt.
  7. Chuyển `loading → detail-loaded`; grade/feedback controls vẫn disabled nếu contract blocker còn.
- **Response/error:** dùng #55 mapping mục B.4. Với 401/403/404/500 không hiển thị mockup sample như data thật; có Retry chỉ khi đã chọn policy cho detail GET.
- **State/cache/output:** cập nhật detail cache key theo `submission_id` chỉ khi cache strategy được phê duyệt; checkout hiện không có client cache. Output là detail hoặc state lỗi.

### D.3. ME10-E02 — Làm mới kết nối/chi tiết

- **Trigger:** button #19; click.
- **Current:** button không có handler; badge “Đang đồng bộ” không tạo polling/timer.
- **Future input:** current route ID và auth/session; không thêm query.
- **Xử lý:**
  1. Khi #55 request đang chạy, disable refresh hoặc dedupe theo UI policy được duyệt.
  2. Gọi lại GET #55 (same path/auth); không gửi #56/#57.
  3. Map success qua E01; empty/no row → 404 state; 401/403/500 theo B.4.
  4. Khi lỗi mạng, giữ detail đã tải nếu có và đánh dấu stale; không tuyên bố đã sync.
- **Kết quả:** refresh state kết thúc ở loaded/stale/error. Cần chốt cancellation, timeout, retry và cache strategy; không có runtime evidence.

### D.4. ME10-E03 — Nhập hoặc sửa điểm

- **Trigger:** number input #25; `input/change`.
- **Current:** disabled, không có min/max/step/value; #24 ghi sample 0–100. Không có input event xử lý.
- **Expected gate:** chỉ enable sau khi field, scale, precision, range, `max_score` source, rubric mapping và #56 request contract được duyệt.
- **Input/validation khi gate mở:** body field `score` strict int32 theo current source. Backend fallback kiểm `0 <= score <= assignments.max_score`; source không chấp nhận decimal string. `max_score` không có trong #55 response nên client không thể validate bound từ detail hiện tại.
- **Xử lý:** lưu `scoreDraft` riêng; không tự round/normalize decimal hoặc dùng `/100` làm max; reject non-int32 locally nếu exact contract giữ nguyên; server #56 vẫn là authority. Dirty state giữ cho tới response success hoặc user discard.
- **Output:** dirty/validation state. Không có API call ở thao tác nhập. Current HTML không bật control.

### D.5. ME10-E04 — Nhập feedback và cập nhật bộ đếm ký tự

- **Trigger:** textarea #29 `input`; counter #28.
- **Input:** text Unicode nguyên trạng từ textarea; HTML không đặt maxlength, trim hoặc required.
- **Current xử lý:** inline JS đọc `.value.length` rồi đổi `#char-counter` thành `N ký tự`; không gọi API, sanitize, trim, persist, validate hoặc render Markdown. Chuỗi rỗng cho 0. JS chỉ đăng ký handler `input`.
- **Future state:** update `feedbackDraft`, đánh dấu feedback dirty; lưu draft khi điều hướng/rời màn hình cần quyết định; không tự xóa khi #56 grade save. Không áp giới hạn độ dài chưa có nguồn.
- **Output:** counter và local draft; không đổi backend.

### D.6. ME10-E05 — Lưu điểm qua API #56 (chỉ khi UI/contract được tách và duyệt)

- **Trigger dự kiến:** action “Lưu điểm” độc lập; ảnh hiện có chỉ một combined button disabled (#32), vì vậy event này **chưa được gắn vào click thực tế**.
- **API:** `POST /api/v1/mentor/submissions/{submission_id}/grade`; Bearer MENTOR; `Content-Type: application/json`; no query. Current source body strict `{ "score": int32, "rubric_items": string }`, extra keys forbidden. Key/format `rubric_items` là fallback DERIVED; source bỏ qua persistence.
- **Input gates:** valid route/session; detail loaded; no grade request in flight; score and rubric payload approved. Không cho gọi nếu chỉ có ảnh/placeholder hoặc chưa biết `max_score`/rubric serialization.
- **Route-validation branch:** trước khi route function/view được gọi, FastAPI kiểm tra Pydantic body bắt buộc; body thiếu/sai/extra field trả 422 `DESIGN_VALIDATION_ERROR` qua middleware và chưa tới MENTOR guard. Contract chưa xác nhận thứ tự này khi auth cũng thiếu/sai.
- **Xử lý tuần tự:**
  1. Snapshot `scoreDraft` + rubric representation theo approved contract; no defaults invented.
  2. Validate type/range contract client-side nếu đầy đủ; server remains authority.
  3. Mark `grade-saving`, send one POST #56; don't send #57 automatically.
  4. Với body hợp lệ, server MENTOR auth → path signed-int64 (malformed/overflow currently 404) → lock row `FOR UPDATE` → check candidate relation/direct owner → DERIVED range check → update `score=CAST(:score AS NUMERIC(6,2))`, `status='GRADED'`, preserve feedback → constrained upload mapping → validate Submission projection → commit riêng.
  5. 200 `DESIGN_RESOURCE_UPDATED`: take returned Submission, mark `grade-saved`, clear only grade dirty state; preserve feedback draft and feedback status.
  6. 422 body/range error: show `meta.fieldErrors` when present, preserve score draft. 401/403/404/500 map per B.4.
  7. On network timeout after POST, set `grade-outcome-unknown`; do not auto retry. Revalidate #55 and present returned state without claiming audit confirmation; retry policy still needs owner/product decision.
  8. After confirmed success, call #55 per F09 to revalidate current record; if refetch fails, retain `grade-saved` mutation result and mark detail stale (mutation is not rolled back).
- **Output:** independent grade result (`grade-saved`, field/auth/access/not-found error, or `grade-outcome-unknown`); successful #56 may leave feedback unchanged and is followed by #55 revalidation.
- **Current blockers:** rubric key/items do not have stable approved serialization or storage; score int/decimal scale and bound source unresolved; combined button semantics unresolved; client route/auth absent.

### D.7. ME10-E06 — Gửi feedback qua API #57 (độc lập #56)

- **Trigger dự kiến:** action “Gửi feedback” độc lập; chưa có control riêng trong ảnh. Không gọi ngầm từ combined button #32.
- **API:** `POST /api/v1/mentor/submissions/{submission_id}/feedback`; Bearer MENTOR; JSON; no query. Current source strict body `{ "feedback_text": string, "attachments": string }`, extra keys forbidden. Both wire-key/attachment shape have unresolved contract questions; `attachments` is opaque.
- **Input gates:** valid route/session; feedback draft; attachment mapping approved. Do not fabricate `attachments=""` or treat student file `files[]` as feedback attachments.
- **Route-validation branch:** trước khi route function/view được gọi, FastAPI kiểm tra Pydantic body bắt buộc; body thiếu/sai/extra field trả 422 `DESIGN_VALIDATION_ERROR` qua middleware và chưa tới MENTOR guard. Contract chưa xác nhận thứ tự này khi auth cũng thiếu/sai.
- **Xử lý tuần tự:**
  1. Snapshot feedback draft + approved attachment payload; preserve text on failure.
  2. Mark `feedback-saving`; send one POST #57 independent of #56 result. Current source does not require status GRADED.
  3. Với body hợp lệ, server MENTOR guard → signed-int64 parser (invalid/overflow current 422) → row lock → direct-owner check → update only `assignment_submissions.feedback` with `feedback_text` → preserve score/status → optional constrained lookup of student file → validate response → commit riêng.
  4. 200 `DESIGN_RESOURCE_UPDATED`: take returned Submission, mark `feedback-saved`, clear only feedback dirty state. Response includes feedback but no feedback attachments.
  5. 401/403/404/422/500 map per B.4. Keep draft for actionable errors. For transport ambiguity, set `feedback-outcome-unknown`, don't auto retry because current fallback overwrites a single field.
  6. After confirmed success, GET #55 revalidate; if it fails, preserve successful feedback state and mark detail stale.
- **Output:** independent feedback result (`feedback-saved`, field/auth/access/not-found error, or `feedback-outcome-unknown`); successful #57 preserves score/status and is followed by #55 revalidation.
- **Current source consequence:** repeated calls replace the one candidate feedback column. No history or idempotency key is implemented. Product/schema owner must decide overwrite/history, attachment persistence and Student visibility.

### D.8. ME10-E07 — Partial success, reconciliation và refresh #55

- **Trigger:** one mutation succeeded while the other failed, or successful POST followed by revalidation; not a separate API.
- **Input:** per-operation state and latest returned Submission; `submission_id`; error/trace ID.
- **Xử lý:**
  1. Maintain `gradeStatus` and `feedbackStatus` independently (`idle/dirty/saving/saved/error/outcome-unknown`).
  2. Never represent both as saved based on one API response. Never undo a committed #56 if #57 fails, or vice versa.
  3. After a POST success, issue GET #55 as F09 requires. Map current stored score/feedback; absent optional fields remain absent, not zero/empty.
  4. If GET succeeds, reconcile displayed detail while preserving the other unsaved draft. If GET fails, show committed API result and stale marker; do not repeat POST automatically.
  5. If POST outcome is unknown, GET #55 can show current stored values but cannot prove which request wrote them where same values pre-existed. Keep an explicit unknown/reconciliation state until user decision or approved server idempotency/audit behavior.
- **Output:** full success, grade-only success, feedback-only success, both failed, or stale/outcome-unknown. Cross-call atomicity is not provided by source.

### D.9. ME10-E08 — Quay về ME-09

- **Trigger:** breadcrumb #9, top link #14, bottom link #33, browser back if available; click/popstate.
- **Current:** anchors are `href="#"`; no router or history handler. Browser native fragment behavior only; no working navigation evidence.
- **Input:** current submission ID, any dirty/partial operation state, ME-09 prior URL/filter/page (not available in current source).
- **Processing:**
  1. If a mutation is in flight or form dirty, determine whether to block, prompt, or preserve draft per approved navigation policy; current asset has no prompt.
  2. Route to ME-09 only when valid route mapping exists. Do not lose committed partial status from UI without showing success/error first.
  3. Preserve list query/cache only if an approved route state contract exists; none is present.
- **Output:** proposed ME-09 list route; not wired. Do not call #54 solely because user clicked back unless list refresh policy says to.

### D.10. ME10-E09 — Báo cáo sự cố tải file

- **Trigger:** #20 click.
- **Current:** button has no handler. API #55–#57 do not report file issues; no report endpoint is mapped in ME-10 inventory.
- **Processing:** click has no app handler or network effect in the current HTML; no API result/error branch exists.
- **Input/output:** none currently. Do not send support API #58/#59 because its payload/scope is not a file-report contract. Product must supply destination, fields, privacy rules and API/route before implementation.

### D.11. ME10-E10 — Header/footer placeholder navigation

- **Trigger:** #1–#7, #37–#39 anchors.
- **Current:** `href="#"`; no router. #4 current active page only uses `aria-current="page"`.
- **Input:** click on an anchor; no application payload or state is attached in the asset.
- **Processing/output:** no API. Destinations for logo, overview, courses, support, notifications and footer documents are not present in asset contract; do not invent target routes. Notification dot is not backed by #43 here. Keep links inert/disabled or wire only after route map is approved.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
