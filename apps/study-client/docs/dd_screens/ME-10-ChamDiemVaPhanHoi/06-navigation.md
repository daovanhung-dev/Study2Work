# ME-10 — Navigation

## 1. Route definition
- Current route in inventory: `/mentor/submissions/:submissionId`
- Status: candidate/design route; Study Web `UNWIRED` unless source code proves otherwise.
- Route params/types: `submissionId` (type/validation: see source DD; CẦN_XÁC_NHẬN if absent)
- Query params/defaults: preserve the inventory route string; detailed parsing rules only from source DD.
- Route guards: see source DD/API contract; do not create role policy.

## 2. Điểm vào
| From screen/route | Trigger | Params | Guard / fallback |
|---|---|---|---|
| [ME-09](../ME-09-DanhSachBaiCanCham/00-overview.md) | Theo DD nguồn/inventory | Theo source; không suy diễn | Xem source DD; route chưa xác nhận runtime |

## 3. Điểm ra
| Destination | Trigger | Params | Điều kiện |
|---|---|---|---|
| [ME-09](../ME-09-DanhSachBaiCanCham/00-overview.md) | Source event/inventory navigation | Theo source DD | Expected links; runtime chưa verify |

## 4. Back / refresh / deep link
- Back behavior: xem source DD; không mặc định browser history.
- Preserve filters/scroll/form state: chỉ nếu source có nêu, nếu không `CẦN_XÁC_NHẬN`.
- Refresh/direct URL: route trong inventory không chứng minh runtime.
- Invalid/missing ID: theo source DD/backend contract; không tự tạo validation.
- Not authenticated/authorized: theo source role guard; xem [Business Rules](05-business-rules.md).

## 5. Diagram
```mermaid
flowchart LR
  S0["ME-10 Chấm điểm và phản hồi"] --> S1["ME-09"]
```

## Source navigation and flow detail

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

### E.1. State matrix

| State | Điều kiện vào | UI/data | Event/exit |
|---|---|---|---|
| `route-invalid` | Missing/malformed route param before #55 | No submission data; link error/back path | E01; route semantics pending |
| `auth-required` | No valid session or #55/#56/#57 401 | Do not expose cached private content unless approved; no raw token | E01/E05/E06; reauth policy pending |
| `body-invalid` | #56/#57 Pydantic body is missing, malformed, or contains forbidden extra fields | Show 422 `DESIGN_VALIDATION_ERROR` and supplied field errors; this response does not establish authentication state | E05/E06; precedence versus auth needs confirmation |
| `loading` | #55 request pending | Skeleton/progress state; current mockup is a static waiting illustration | E01/E02 |
| `detail-loaded` | #55 200 | Map source fields only; rubric/score bound may be unavailable | E01/E02/E07 |
| `no-matched-file` | #55 succeeds with `files=[]` | Show no verified metadata; do not create a download link | E01 |
| `access-denied` | #55/#56/#57 403 | Hide protected body and show safe access error | E01/E05/E06 |
| `not-found` | #55/#56 path or row 404; #57 row 404 | Safe unavailable state; #57 malformed path is instead 422 | E01/E05/E06 |
| `dirty` | Score or feedback draft differs from loaded value | Keep per-form draft; save controls gated by decisions | E03/E04 |
| `grade-saving` | #56 in-flight | Disable grade action only; feedback action state remains separate | E05 |
| `grade-saved` | #56 200 | Update grade/status from response; trigger #55 revalidation | E05→E07 |
| `grade-error` | #56 401/403/404/422/500 | Preserve input; map field errors/trace | E05 |
| `feedback-saving` | #57 in-flight | Disable feedback action only; grade state remains separate | E06 |
| `feedback-saved` | #57 200 | Update returned feedback; trigger #55 revalidation | E06→E07 |
| `feedback-error` | #57 401/403/404/422/500 | Preserve draft; map validation/access/trace | E06 |
| `partial-success` | One POST saved; other fails/has not been requested | Show independent result, allow only approved next operation | E05/E06/E07 |
| `outcome-unknown` | POST sent, transport ends before response | Do not claim failure or auto retry; revalidate #55 | E05/E06→E07 |
| `stale-detail` | Mutation success but GET #55 revalidation fails | Show committed operation state plus refresh-needed indication | E07/E02 |
| `conflict` | Inventory lists this state | Current #55–#57 source has no 409 trigger; don't fabricate one | Needs backend rule/code before wiring |
| `returning` | User leaves to ME-09 | Resolve dirty/in-flight policy first; preserve partial success | E08 |

### E.2. Navigation and data handoff

| From → To | Trigger | Handoff | Current status |
|---|---|---|---|
| ME-09 → ME-10 | Select one #54 item | `data.items[].id` as `submissionId`; do not pass mockup identity or whole item as trusted detail | Expected route only; ME-09/ME-10 UI route absent |
| ME-10 → #55 | Route entry/refresh/revalidate | signed-int64 `submission_id` path | Study Server source exists; screen client not wired |
| ME-10 → #56 | Approved grade action | `submission_id`, strict `score`, `rubric_items` fallback | Source exists; grade UI contract blocked |
| ME-10 → #57 | Approved feedback action | `submission_id`, `feedback_text`, `attachments` fallback | Source exists; attachment/UI contract blocked |
| ME-10 → ME-09 | Breadcrumb/back links | Preserve list state only if route/state contract defines it | Mockup `href="#"`; no implementation |
| Header/footer → other screens | Link click | No defined screen/data mapping in this asset | Unwired; destinations unknown |

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

### B.1. Entry và tải chi tiết

```mermaid
flowchart LR
  ME09[ME-09 đã chọn submission] -->|ID từ #54 data.items[].id| ROUTE[Route đề xuất ME-10]
  ROUTE -->|GET #55| DETAIL[Submission detail]
  DETAIL -->|rubric thiếu trong response hiện tại| GAP[Blocker rubric]
  DETAIL -->|form được duyệt| GRADE[POST #56]
  DETAIL -->|feedback được duyệt| FEEDBACK[POST #57]
  GRADE -->|commit riêng| GRADESTATE[Grade saved / grade failed]
  FEEDBACK -->|commit riêng| FEEDBACKSTATE[Feedback saved / feedback failed]
  GRADESTATE --> REFETCH[GET #55 revalidate]
  FEEDBACKSTATE --> REFETCH
  REFETCH --> ME09
```

Sơ đồ kết hợp expected flow với current route source; nó không chứng minh UI navigation hoặc API deployment đã được wire. Không có đường dữ liệu rubric trong #55 hiện tại.

### B.2. Tuần tự tải #55

1. UI lấy `submissionId` từ route; kiểm tra có mặt và đúng dạng số nguyên theo rule được thống nhất. Không thay ID bằng `assignment_id` hay `user_id`.
2. Yêu cầu session token từ auth layer đã được phê duyệt. Study Web hiện không có auth/router source nên đây là dependency, không giả định local storage/cookie.
3. Gửi `GET /api/v1/mentor/submissions/{submission_id}` với `Authorization: Bearer <JWT>`; không có query/body. Request trace đi theo cơ chế `get_trace_id(request)` hiện hành.
4. Server xác minh Bearer, numeric subject và `MENTOR` role trước path parse/DB; đọc row, kiểm tra course owner và dựng reusable Submission projection.
5. Với success `200 DESIGN_RESOURCE_RETRIEVED`, đọc `data.id`, `assignment_id`, `user_id`, `content?`, `files[]`, `status`, `submitted_at`, `score?`, `feedback?`; optional null có thể bị omit. Không suy rubric/assignment title/deadline/max score.
6. Nếu `data.files=[]`, hiển thị không có file metadata khớp; không tự nối `file_url` hoặc phát sinh URL. Nếu API trả 403/404/500, không render mẫu thành dữ liệu thật.
7. Khi #55 thành công, state chi tiết chỉ đủ cho fields response; nút chấm/feedback vẫn bị chặn cho tới khi score/rubric/attachment contract được giải quyết.

### B.3. Các event và hai mutation

- Mọi event có `Event ID` và quy trình tuần tự ở mục D. Các placeholder/nav links không phát sinh API.
- #56 chỉ được gọi từ thao tác “lưu điểm” đã tách và sau khi request body được tạo từ rule đã duyệt. Current fallback body cần `score:int32` và `rubric_items:string`; không tạo chuỗi rubric tùy ý.
- #57 chỉ được gọi từ thao tác “gửi feedback” đã tách. Current fallback body là `feedback_text:string`, `attachments:string`; attachment payload chưa có cách tạo an toàn từ giao diện.
- Mỗi API trả Submission response mới. Sau từng mutation success, revalidate #55 theo F09. Mutation đã commit không bị đảo lại nếu lần revalidation sau thất bại.
- Không gọi #57 tự động sau #56 hoặc ngược lại. Không gửi cả hai ngầm từ nút combined hiện tại. Không retry tự động khi POST timeout vì server có thể đã commit; hiển thị outcome unknown, tải lại #55 theo quyết định retry đã duyệt.

### B.4. Mapping lỗi và business code

| API | HTTP / business code trong current source | UI state và xử lý |
|---|---|---|
| #55 GET | 200 `DESIGN_RESOURCE_RETRIEVED` | Map Submission projection; không bổ sung rubric. |
| #55 | 401 `DESIGN_AUTHENTICATION_REQUIRED` | `auth-required`; xóa dữ liệu nhạy cảm đang hiển thị theo auth/session policy và không retry loop. |
| #55 | 403 `DESIGN_ACCESS_DENIED` | `access-denied`; không hiển thị submission. Direct-owner policy là DERIVED. |
| #55 | 404 `DESIGN_RESOURCE_NOT_FOUND` | `not-found`; current source dùng cho ID sai format/overflow hoặc không có row. |
| #55 | 500 `DESIGN_INTERNAL_ERROR` | `detail-error`; giữ traceId cho support, không hiện SQL/exception. |
| #56 POST | 200 `DESIGN_RESOURCE_UPDATED` | `grade-saved`; dùng data trả về, sau đó revalidate #55. |
| #56 | 401 / 403 / 404 | Auth/access/not-found state; giữ input đang nhập nếu policy session cho phép, không tự clear nhầm. Path sai hiện map 404. |
| #56 | 422 `DESIGN_VALIDATION_ERROR` | Field/body/range error; source range error có `meta.fieldErrors` cho `score` / `VALUE_OUT_OF_RANGE`. Giữ draft, không tạo rubric. |
| #56 | 500 `DESIGN_INTERNAL_ERROR` | `grade-error` hoặc `outcome-unknown` nếu lỗi transport sau submit; hiện source không trả 409. |
| #57 POST | 200 `DESIGN_RESOURCE_UPDATED` | `feedback-saved`; dùng data trả về, sau đó revalidate #55. |
| #57 | 401 / 403 / 404 | Auth/access/not-found; path sai hiện source map 422, còn 404 cho row không tồn tại. |
| #57 | 422 `DESIGN_VALIDATION_ERROR` | Request body/path invalid; giữ feedback draft. Không tự áp length/non-empty rule. |
| #57 | 500 `DESIGN_INTERNAL_ERROR` | `feedback-error` hoặc `outcome-unknown` nếu transport mơ hồ; không giả định rollback nếu response bị mất sau commit. |

Current `error_response()` trả envelope `{success:false,businessCode,message,data:null,meta,traceId}`; `meta.fieldErrors` có thể có khi gửi `ErrorDetail`. API error messages là source text, không phải localizable design strings. Chỉ dùng catalog codes; current source không định nghĩa 409 branch cho #55–#57, dù một số inventory state có chữ “conflict”.

Với #56/#57, route signature nhận Pydantic body model bắt buộc; FastAPI body validation và handler `RequestValidationError` có thể trả 422 `DESIGN_VALIDATION_ERROR` trước khi route function gọi view-level MENTOR guard. Request body hợp lệ mới đi tiếp vào view guard, rồi path parse/DB theo thứ tự riêng của từng API. API catalog chưa chốt precedence giữa malformed body và authentication failure; không suy luận rằng 422 xác nhận session hợp lệ.
