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
| --- | --- |
| API ID | `API-IAM-003` |
| Module | `Platform Identity` |
| Method | `POST` |
| Endpoint | `/api/v1/auth/resend-verification` |
| Purpose | Nhận email, luôn trả generic accepted, và chỉ khi account pending + cooldown hết mới revoke token cũ, tạo token hash mới và outbox email delivery. |
| Consumer/Actor | `Anonymous guest` |
| Authentication | `Anonymous`; HTTPS bắt buộc |
| Authorization | `N/A — Không yêu cầu role/permission` |
| Basis | `DIRECT` cho method/path/flow chính; `DERIVED` hoặc `SOURCE_REQUIRED` được đánh dấu tại field tương ứng |
| Status | `Draft — Needs Confirmation` |
| Transaction | `Conditional identity_db transaction` chỉ chạy khi account pending và cooldown đã hết; update revoke token cũ + insert token mới + outbox phải atomic. Generic no-op branch không mutation. |
| Side effects | Gửi verification email bất đồng bộ qua outbox.<br>Dedupe 10 phút và rate limit 3/giờ/email hash.<br>Không tiết lộ account existence/status. |

## Sources

- `04_DAC_TA_API.md:L19-L79, L89, L495-L523`.
- `03_THIET_KE_CO_SO_DU_LIEU.md:L101-L132, L234-L240`.
- `02_BIEU_DO_HE_THONG.md:L332-L377, L1738-L1762`.
- `01_TONG_QUAN_DU_AN.md:L338-L345, L648-L659, L704, L757`.
- `05_DAC_TA_MAN_HINH.md:L76`.
- `PLAN_01_IAM_IAM_ang_ky_va_xac_minh_email.md`.

## Tables read

- `user_emails`.
- `users`.
- `email_verification_tokens`.

## Tables write

- `email_verification_tokens`.
- `outbox_events`.

## Mục chú ý

- API name trong folder là working name DERIVED từ Plan/endpoint; chưa phải canonical display name.
- Các trường hoặc status chưa có contract field-level được ghi `SOURCE_REQUIRED`; không được triển khai như contract Final.
- Consumer UI: `SCR-IAM-002`; UI chỉ dùng để kiểm coverage, không thay đổi API contract.

## Assumptions

- Response data dùng `null` trong Draft example vì source chỉ nói accepted; exact response data rule SOURCE_REQUIRED.
- Email required/format validation có thể là 400 nhưng public enumeration-safe behavior cần confirm.
- Cooldown được tính từ token `created_at` như DERIVED implementation; source chỉ nêu 10 phút.

## Conflicts

- Endpoint anonymous nhưng `RESEND_COOLDOWN` chỉ trả khi session chứng minh ownership; không có session/header contract để chứng minh ownership.
- Outbox event type/payload cho email delivery chưa có trong event catalog.
- Token TTL/hash algorithm và exact generic success businessCode/status/message chưa được định nghĩa.

## Security note

- Luôn dùng email hash cho rate/dedupe; không log raw email.
- Không cho biết account không tồn tại, active, suspended hoặc pending.
- Revoke/insert token transition theo one-way procedure; persist hash only.
- Raw token delivery handoff phải tránh persist trong generic event payload.

## Performance note

- Dedupe `10 phút`.
- Rate limit `3/giờ/email hash`.
- Mutation p95 ≤ 1,5 giây; email delivery async.

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
