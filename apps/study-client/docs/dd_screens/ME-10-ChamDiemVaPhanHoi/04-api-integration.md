# ME-10 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ME-10-API-001` | #55 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ME-10-API-002` | #56 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ME-10-API-003` | #57 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #55, #56, #57
- Orchestration/data notes: GET #55 → POST #56 điểm → POST #57 feedback khi người dùng yêu cầu → revalidate #55.
- BE/source status và gate: **D**; **BLOCK:** Rubric fields, score type, atomicity chưa khóa
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Source trace

- Screen requirements/flow: [screen inventory and F09](../../list_screen.md); [AC-23 API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md); [AC-23 activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio).
- API catalog: [API #55–#57](../../../../../docs/lists/list_api.md).
- Current routes: [Study API router](../../../../study-server/app/api/v1.py).
- Body validation/error mapping: [Study validation middleware](../../../../study-server/app/core/middleware.py).
- Current implementations: [#55 view](../../../../study-server/app/modules/mentor/api_55_mentor_submissions_detail/view.py), [#55 query](../../../../study-server/app/modules/mentor/api_55_mentor_submissions_detail/query.py), [#56 view/query/models](../../../../study-server/app/modules/mentor/api_56_mentor_submissions_grade/view.py), [#57 view/query/models](../../../../study-server/app/modules/mentor/api_57_mentor_submissions_feedback/view.py), reusable [Submission model](../../../../study-server/app/modules/mentor/api_54_mentor_submissions_list/models.py), [envelope helper](../../../../study-server/app/core/responses.py).
- Contract status/open questions: [#55](../../../../study-server/docs/dd/55_mentor_submissions_detail/OPEN_QUESTIONS.md), [#56](../../../../study-server/docs/dd/56_mentor_submissions_grade/OPEN_QUESTIONS.md), [#57](../../../../study-server/docs/dd/57_mentor_submissions_feedback/OPEN_QUESTIONS.md).
- Current schema context: [Study DB context](../../../../../.agents/server-study/database.md), [candidate legacy DDL](../../../../../infra/postgres/study-server/DB.sql); neither establishes live schema/deployment.
- UI wiring/accessibility context: [Study Web status](../../../../../.agents/web-work/study/AGENTS.md), [intended design target](../../../../../.agents/web-study/design.md).

### Trích từ DD nguồn: B.4. Mapping lỗi và business code

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

### Trích từ DD nguồn: D.1. API chung #55–#57

- **Auth:** `Authorization: Bearer JWT`; với body hợp lệ, shared helper yêu cầu numeric subject và role `MENTOR` trước custom path parse/DB access. Riêng #56/#57, FastAPI có thể chặn request ở Pydantic body validation trước khi gọi view guard; middleware trả 422 `DESIGN_VALIDATION_ERROR`. Direct `courses.mentor_id` owner scope là fallback DERIVED; assigned Mentor support chưa có.
- **Trace:** route dùng `get_trace_id(request)`; error helper serialize `traceId`, HTTP `X-Trace-Id` và `data:null`. Không đưa raw submission/file URL/SQL vào log UI.
- **HTTP/body:** #55 GET không body/query; #56/#57 POST JSON. Không có idempotency header/contract trong source đang xét. Success source dùng HTTP 200.
- **Response:** success envelope gồm `success`, `businessCode`, `message`, `data:Submission`, `meta`, `traceId`; nullable `content`, `score`, `feedback` có thể bị loại khỏi JSON. `files` hiện là array 0/1. Không có rubric/feedback attachment fields.
- **Source availability:** current Study Server routes exist; API focused tests exist but are not run here and use fake DB per context. Live DB/runtime remains unverified.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/04_mentor/ME-10_cham-diem-va-phan-hoi/ME-10.md)
