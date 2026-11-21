---
title: "Overview"
order: 2
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | `2` |
| Module | `GUEST / ACCOUNT & DISCOVERY` |
| Method | `POST` |
| Endpoint | `/api/v1/auth/verify-email/send` |
| Purpose | `Gửi mã/link xác thực email khi verification được bật` |
| Consumer/Actor | `Guest / registration flow` |
| Authentication | `Public; không yêu cầu Bearer token` |
| Authorization | `N/A — public verification dispatch` |
| Basis | `DIRECT — approved design contract + AC-01` |
| Status | `Draft — Needs Confirmation` |
| Transaction | `N/A — không có transaction DB được source xác nhận` |
| Side effects | `Expected theo AC-01: dispatch tới Email Provider và log/retry delivery failure sau acceptance. Current source: gọi provider đồng bộ; exception trả 500; chưa có retry worker; provider mặc định không gửi email thật.` |

## Sources

- [`docs/lists/list_api.md`](../../../../../docs/lists/list_api.md) — API #2 endpoint, input, response và business codes.
- [`AC-01 Đăng ký tài khoản`](../../../docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) — điều kiện verification, dispatch flow và provider retry note.
- [`createDD-markdown template`](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) — cấu trúc 8 file DD.
- [`API #02 route`](../../../app/api/v1.py), [`view`](../../../app/modules/guest/api_02_auth_verify_email_send/view.py), [`provider`](../../../app/service/email/provider.py) và [test source](../../../tests/modules/guest/api_02_auth_verify_email_send/test_verify_email_send.py) — current implementation evidence; tests được đọc nhưng không chạy trong task docs.
- [API #01 dispatch open question](../01_auth_register/OPEN_QUESTIONS.md) — điểm nối account creation → verification.

## Tables read

- `N/A — chưa có bảng đọc được ERD/contract xác nhận cho API #2`.

## Tables write

- `N/A — không có DB mutation được source xác nhận`.

## Mục chú ý

- `API #2 là side effect gửi verification; không tạo DD riêng cho Email Provider.`
- `API chỉ được dispatch khi verification được bật theo tên API/AC-01; không thêm field verification_enabled vào request.`
- `HTTP 202 là protocol status; không thêm HTTPStatus vào JSON envelope.`

## Assumptions

- `Expected design: request được chấp nhận khi dispatch đã được xếp xử lý; delivery failure sau acceptance được log và retry bất đồng bộ. Current source chưa có queue/retry worker; xem VERIFICATION_REPORT.md.`
- `data.status = "accepted"` là giá trị minh họa suy ra từ `DESIGN_OPERATION_ACCEPTED`; tập giá trị chính thức chưa được đặc tả thêm.
- `meta` dùng `{}` vì contract API #2 không khai báo operation_id hoặc metadata khác.

## Conflicts

- `DISCREPANCY/TBD: chưa có schema xác nhận cho verification token, link, expiry, retry tracking hoặc email log.`
- `DISCREPANCY/TBD: chưa có rule xác nhận user_id tồn tại hoặc khớp với email; DD không tự thêm query/business validation.`
- `DISCREPANCY: route/view/provider source hiện tại đã được đọc; chưa có provider gửi email thật, token/link/expiry hoặc retry worker được triển khai.`

## Security note

- `Không yêu cầu Bearer token; không log token/link xác thực hoặc dữ liệu nhạy cảm ngoài thông tin cần cho dispatch.`
- `Không trả raw upstream body, stack trace hoặc secret trong response.`

## Performance note

- `Expected design dùng dispatch bất đồng bộ để HTTP 202 không phụ thuộc thời gian provider; current view gọi provider đồng bộ.`
- `Retry policy/count và deduplication key chưa được source xác nhận; không tự đặt giá trị.`


---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | 【Khái quát】 |  |
| 3 | `B3` | Get thông tin…. |  |
| 5 | `A5` | 【Mục chú ý】 |  |
| 7 | `B7` | Không có |  |

</details>

