# PLAN_RESULT — Study API #02

**API:** `POST /api/v1/auth/verify-email/send` — Gửi mã/link xác thực email nếu bật verification
**Trạng thái:** `Draft — Needs Confirmation`; package DD đã đủ artifact, các chính sách provider/dispatch còn mở
**Output folder:** `apps/study-server/docs/dd/02_auth_verify_email_send/`

## Cơ sở contract và nguồn

- [Catalog API #02 và reusable `ActionResult`](../../../../../docs/lists/list_api.md): public/no Bearer; body `user_id:int64!`, `email:email!`; response `ApiEnvelope<ActionResult>`; HTTP `202 DESIGN_OPERATION_ACCEPTED`; errors `422 DESIGN_VALIDATION_ERROR` và `500 DESIGN_INTERNAL_ERROR`. `ActionResult` gồm `status:string`, `reason?:string`.
- [Index AC-01](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [diagram AC-01](../../diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio): API #02 nằm sau bước tạo tài khoản; provider gửi verification; diagram yêu cầu log/retry khi delivery thất bại.
- Current source: [router](../../../app/api/v1.py), [API #02 view](../../../app/modules/guest/api_02_auth_verify_email_send/view.py), [model](../../../app/modules/guest/api_02_auth_verify_email_send/models.py), [validator](../../../app/modules/guest/api_02_auth_verify_email_send/validate.py), [provider](../../../app/service/email/provider.py), và [test source](../../../tests/modules/guest/api_02_auth_verify_email_send/test_verify_email_send.py). Test source được đọc, không chạy trong task docs.
- API #01 connected boundary: [API #01 open questions](../01_auth_register/OPEN_QUESTIONS.md) và [verification report](../01_auth_register/VERIFICATION_REPORT.md) ghi nhận API #01 hiện chưa gọi API #02.
- Template: registry-wired `createDD-markdown`, bộ [8 Markdown sheets](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/), và [Study workflow](../../../../../.agents/server-study/workflows/README.md). Study yêu cầu folder Markdown, không yêu cầu ZIP.

## Kết quả theo kế hoạch

| Hạng mục | Kết quả |
|---|---|
| Contract | Giữ nguyên method/path, public auth, request/response shape, HTTP status và đúng error set từ catalog. |
| Expected/current | Giữ AC-01 log/retry sau acceptance là expected behavior; ghi current synchronous provider call, 500 khi exception, không retry worker và default stub không gửi email. |
| DB mapping | Không có query hoặc mutation DB được API #02 contract/source xác nhận; không tạo mapping giả. |
| Điểm nối AC-01 | Ghi rõ API #01 chỉ log `verification_dispatch_pending`, chưa invoke API #02/provider. |
| Package | 8 sheet hiện có + `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`. |
| Phạm vi thay đổi | Chỉ Markdown DD và worklog/inventory; không sửa runtime, tests, schema, catalog, diagram hay client. |

## Expected behavior và current source

| Chủ đề | Expected behavior | Current source |
|---|---|---|
| Dispatch | Khi verification được bật trong flow AC-01, gọi API #02 và gửi verification qua provider. | API #01 hiện chỉ log pending marker; API #02 route nhận request và gọi provider nếu được gọi trực tiếp. |
| Acceptance/retry | AC-01 mô tả log/retry delivery failure sau acceptance. | View gọi provider đồng bộ; exception trả HTTP 500; không có queue/retry worker. |
| Delivery | Email Provider gửi mã/link verification. | Provider mặc định là stub, trả `accepted` mà không gửi email hoặc tạo token/link. |
| Persistence | Không có DB mapping API #02 được contract xác nhận. | Route không inject DB; module không query/write database. |
| Input | `user_id:int64!`, `email:email!`. | Model dùng `int`/`str`; validator yêu cầu raw `user_id` là integer và trim/validate email qua shared helper; int64 range chưa được kiểm tra trong module. |

## Tables read/write và side effect

- Tables read: `N/A — không có query được contract/source xác nhận`.
- Tables write: `N/A — không có DB mutation được contract/source xác nhận`.
- External side effect: dispatch tới `VerificationEmailProvider`; current default implementation chỉ là stub.

## Câu hỏi còn mở

Các quyết định về owner/feature gate, acceptance và retry, provider/token lifecycle, user-email binding, public abuse controls, validation policy và `ActionResult.status/reason` được ghi trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

